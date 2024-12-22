import logging
from dataclasses import dataclass

from msfabricutils.core.lakehouse import (
    create_workspace_lakehouse,
    delete_workspace_lakehouse,
    get_workspace_lakehouse,
    update_workspace_lakehouse,
)


@dataclass
class CreateLakehouseArgs:
    name: str
    workspace_id: str
    enable_schemas: bool
    on_conflict: str
    description: str | None = None


@dataclass
class DeleteLakehouseArgs:
    workspace_id: str
    on_conflict: str
    id: str | None = None
    name: str | None = None


def create_lakehouse_command(args: CreateLakehouseArgs):
    """Creates a lakehouse."""
    
    name = args.name
    workspace_id = args.workspace_id
    enable_schemas = bool(args.enable_schemas)
    description = args.description
    on_conflict = args.on_conflict

    lakehouse_id = None
    try:
        lakehouse = get_workspace_lakehouse(workspace_id, lakehouse_name=name)
        lakehouse_id = lakehouse["id"]
        logging.info(f"Lakehouse {name} created successfully with id {lakehouse_id}")
    except ValueError:
        logging.info(f"Lakehouse {name} does not exist")
        pass

    if lakehouse_id is not None:

        if on_conflict == "ignore":
            logging.info(f"Lakehouse `{name}` already exists, skipping update")
            return lakehouse

        if on_conflict == "error":
            raise ValueError(f"Lakehouse {name} already exists")
        
        if on_conflict == "update":
            logging.info(f"Updating lakehouse with `{name}` with description `{description}`")
            update_workspace_lakehouse(workspace_id, lakehouse_id, name, enable_schemas, description)
            lakehouse = get_workspace_lakehouse(workspace_id, name, enable_schemas, description)
            lakehouse_id = lakehouse["id"]
            logging.info(f"Lakehouse `{name}` successfully updated")

    else:
        logging.info(f"Creating lakehouse with `{name}` with description `{description}`")
        lakehouse = create_workspace_lakehouse(workspace_id, name, enable_schemas, description)
        logging.info(f"Lakehouse `{name}` successfully created")
        lakehouse_id = lakehouse["id"]

    return lakehouse


def delete_lakehouse_command(args: DeleteLakehouseArgs):
    """Deletes a lakehouse."""
    workspace_id = args.workspace_id
    lakehouse_id = args.id
    lakehouse_name = args.name
    on_conflict = args.on_conflict

    if lakehouse_id is None and lakehouse_name is None:
        raise ValueError("Either `lakehouse_id` or `lakehouse_name` must be provided")

    if lakehouse_id is None:
        try:
            lakehouse = get_workspace_lakehouse(workspace_id, lakehouse_name=lakehouse_name)
            lakehouse_id = lakehouse["id"]
            logging.info(f"Lakehouse {lakehouse_name} exists")
        except ValueError:
            logging.info(f"Lakehouse {lakehouse_name} does not exist")
            
    if workspace_id is None and on_conflict == "error":
        raise ValueError(f"Lakehouse {lakehouse_name} does not exist")

    if workspace_id is None and on_conflict == "ignore":
        logging.info(f"Lakehouse {lakehouse_name} does not exist, skipping deletion")
        return

    logging.info(f"Deleting lakehouse {lakehouse_id}")
    response = delete_workspace_lakehouse(workspace_id, lakehouse_id)
    response.raise_for_status()
    logging.info(f"Lakehouse {lakehouse_id} successfully deleted")