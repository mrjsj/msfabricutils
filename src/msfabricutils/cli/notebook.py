import glob
import logging
import os
from dataclasses import dataclass

from msfabricutils.core.notebook import (
    create_workspace_notebook,
    delete_workspace_notebook,
    get_workspace_notebook,
    update_workspace_notebook_definition,
)


@dataclass
class CreateNotebookArgs:
    workspace_id: str
    path: str
    name: str
    description: str

@dataclass
class BulkCreateNotebookArgs:
    workspace_id: str
    path: list[str]
    on_conflict: str
    no_wait: bool

@dataclass
class DeleteNotebookArgs:
    workspace_id: str
    on_conflict: str
    id: str | None = None
    name: str | None = None


def create_notebook_command(args: CreateNotebookArgs):
    """Creates a notebook."""

    workspace_id = args.workspace_id
    path = args.path
    name = args.name
    description = args.description
    on_conflict = args.on_conflict
    no_wait = args.no_wait
    notebook_id = None
    try:
        notebook = get_workspace_notebook(workspace_id, notebook_name=name)
        notebook_id = notebook["id"]
        logging.info(f"Notebook {name} already exists")
    except ValueError:
        logging.info(f"Notebook {name} does not exist")


    if notebook_id is not None:

        if on_conflict == "ignore":
            logging.info(f"Notebook `{name}` already exists, skipping update")
            return notebook

        if on_conflict == "error":
            raise ValueError(f"Notebook {name} already exists")
        
        if on_conflict == "update":
            logging.info(f"Updating notebook with `{name}` with description `{description}`")
            notebook = update_workspace_notebook_definition(workspace_id, notebook_id, path, description)
            logging.info(f"Notebook `{name}` successfully updated")

    else:
        logging.info(f"Creating notebook with `{name}` with description `{description}`")
        notebook = create_workspace_notebook(workspace_id, path, name, description, wait_for_completion=not no_wait)
        logging.info(f"Notebook `{name}` successfully created")
        notebook_id = notebook["id"]

    return notebook

def bulk_create_notebook_command(args: BulkCreateNotebookArgs):
    """Creates one or more notebooks."""

    raise NotImplementedError("Bulk create notebooks is not implemented yet")
    paths = []
    for path in args.path:
        path = path if path.endswith(".Notebook") else path + ".Notebook"
        # print(path)
        paths.extend(glob.glob(path))

    paths = list(set(paths))
    formatted_paths = ", ".join(paths)

    if len(paths) == 0:
        logging.info(f"No notebooks found in current directory `{os.getcwd()}` given the provided paths: {formatted_paths}")
        return ""



def delete_notebook_command(args: DeleteNotebookArgs):
    """Deletes one or more notebooks."""
    workspace_id = args.workspace_id
    notebook_id = args.id
    notebook_name = args.name
    on_conflict = args.on_conflict

    if notebook_id is None and notebook_name is None:
        raise ValueError("Either `notebook_id` or `notebook_name` must be provided")

    if notebook_id is None:
        try:
            notebook = get_workspace_notebook(workspace_id, notebook_name=notebook_name)
            notebook_id = notebook["id"]
            logging.info(f"Notebook {notebook_name} exists")
        except ValueError:
            logging.info(f"Notebook {notebook_name} does not exist")
            
    if workspace_id is None and on_conflict == "error":
        raise ValueError(f"Notebook {notebook_name} does not exist")

    if workspace_id is None and on_conflict == "ignore":
        logging.info(f"Notebook {notebook_name} does not exist, skipping deletion")
        return

    logging.info(f"Deleting notebook {notebook_id}")
    response = delete_workspace_notebook(workspace_id, notebook_id)
    response.raise_for_status()
    logging.info(f"Notebook {notebook_id} successfully deleted")