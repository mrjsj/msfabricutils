import logging
from dataclasses import dataclass

from msfabricutils.core.workspace import (
    assign_workspace_to_capacity,
    create_workspace,
    delete_workspace,
    get_workspace,
    update_workspace,
)


@dataclass
class WorkspaceCreateArgs:
    """Arguments for creating a workspace

    Args:
        name (str): The name of the workspace
        on_conflict (str): The action to take if the workspace already exists.
        description (str | None): The description of the workspace
        capacity_id (str | None): The capacity ID of the workspace
    """

    name: str
    on_conflict: str
    description: str | None = None
    capacity_id: str | None = None


@dataclass
class WorkspaceDeleteArgs:
    """Arguments for deleting a workspace

    Args:
        id (str): The ID of the workspace to delete
    """

    on_conflict: str
    id: str | None = None
    name: str | None = None

def create_workspace_command(args: WorkspaceCreateArgs) -> dict[str, str]:
    """Create a new workspace with the specified configuration.
    
    Args:
        args (WorkspaceCreateArgs): The arguments to create a workspace

    Returns:
        Workspace information as a dictionary
    """    

    logging.info(f"Creating workspace {args.__dict__}")

    name = args.name
    description = args.description
    capacity_id = args.capacity_id
    on_conflict = args.on_conflict

    workspace_id = None
    try:
        workspace = get_workspace(workspace_name=name)
        workspace_id = workspace["id"]
        logging.info(f"Workspace {name} already exists")
    except ValueError:
        logging.info(f"Workspace {name} does not exist")

    if workspace_id is not None and on_conflict == "error":
        raise ValueError(f"Workspace {name} already exists")

    if workspace_id is not None and on_conflict == "update":
        logging.info(f"Updating workspace with `{name}` with description `{description}`")
        update_workspace(workspace_id, name, description)
        logging.info(f"Workspace `{name}` successfully updated")

    if workspace_id is None:
        logging.info(f"Creating workspace with `{name}` with description `{description}`")
        workspace = create_workspace(name, description)
        logging.info(f"Workspace `{name}` successfully created")
        workspace_id = workspace["id"]

    if capacity_id is not None:
        logging.info(f"Assigning workspace `{workspace_id}` to capacity `{capacity_id}`")
        assign_workspace_to_capacity(workspace_id, capacity_id)
        logging.info(f"Workspace `{workspace_id}` successfully assigned to capacity `{capacity_id}`")

    return workspace


def delete_workspace_command(args: WorkspaceDeleteArgs) -> dict[str, str]:
    """Delete a workspace with the specified configuration.
    
    Args:
        args (WorkspaceDeleteArgs): The arguments to delete a workspace

    Returns:
        Workspace information as a dictionary
    """

    logging.info(f"Deleting workspace {args.__dict__}")
    
    workspace_id = args.id
    name = args.name
    on_conflict = args.on_conflict

    if workspace_id is None and name is None:
        raise ValueError("Either `id` or `name` must be provided")

    if workspace_id is None:
        try:
            workspace = get_workspace(workspace_name=name)
            workspace_id = workspace["id"]
            logging.info(f"Workspace {name} exists")
        except ValueError:
            logging.info(f"Workspace {name} does not exist")
            
    if workspace_id is None and on_conflict == "error":
        raise ValueError(f"Workspace {name} does not exist")

    if workspace_id is None and on_conflict == "ignore":
        logging.info(f"Workspace {name} does not exist, skipping deletion")
        return

    logging.info(f"Deleting workspace {workspace_id}")
    delete_workspace(workspace_id)
    logging.info(f"Workspace {workspace_id} successfully deleted")
