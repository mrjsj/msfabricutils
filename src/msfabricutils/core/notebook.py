import base64
import os

import requests

from msfabricutils.core.fabric_request import (
    delete_request,
    get_item_from_paginated_get_request,
    get_request,
    post_request,
)
from msfabricutils.core.operations import wait_for_long_running_operation


def get_workspace_notebooks(workspace_id: str) -> list[dict]:
    endpoint = f"workspaces/{workspace_id}/notebooks"
    return get_request(endpoint)


def get_workspace_notebook(
    workspace_id: str, notebook_id: str | None = None, notebook_name: str | None = None
) -> dict[str, str]:
    """
    Retrieves details of a specified notebook by either `notebook_id` or `notebook_name`.

    Args:
        workspace_id (str | None): The ID of the workspace containing the notebook.
        notebook_id (str | None): The ID of the notebook to retrieve details for.
        notebook_name (str | None): The name of the notebook to retrieve details for.

    Returns:
        A dictionary containing the details of the specified notebook.

    Example:
        By `workspace_id` and `notebook_id`:
        ```python
        from msfabricutils.core import get_workspace

        notebook = get_workspace_notebook(workspace_id="12345678-1234-1234-1234-123456789012", notebook_id="beefbeef-beef-beef-beef-beefbeefbeef")
        ```

        By `workspace_id` and `notebook_name`:
        ```python
        from msfabricutils.core import get_workspace_notebook
        notebook = get_workspace_notebook(workspace_id="12345678-1234-1234-1234-123456789012", notebook_name="My Notebook")
        ```
    """

    if notebook_id is not None:
        endpoint = f"workspaces/{workspace_id}/notebooks/{notebook_id}"
        return get_request(endpoint)

    if notebook_name is not None:
        endpoint = f"workspaces/{workspace_id}/notebooks"
        data_key = "value"
        item_key = "displayName"
        item_value = notebook_name

        return get_item_from_paginated_get_request(endpoint, data_key, item_key, item_value)

    raise ValueError("Either `notebook_id` or `notebook_name` must be provided")


def create_workspace_notebook(
    workspace_id: str,
    notebook_path: str,
    name: str | None = None,
    description: str | None = None,
    wait_for_completion: bool = True,
) -> requests.Response | dict[str, str]:
    """
    Creates a new notebook in the specified workspace.

    Args:
        workspace_id (str): The ID of the workspace where the notebook will be created.
        notebook_path (str): The path to the notebook files (containing notebook-content.py and .platform).
        name (str | None): Optional display name for the notebook. If not provided, 
            will use the basename of the notebook_path.
        description (str | None): Optional description for the notebook.
        wait_for_completion (bool): Whether to wait for the creation operation to complete. 
            Defaults to True.

    Returns:
        Either a Response object or a dictionary containing the notebook details,
        depending on the operation status and wait_for_completion setting.

    Example:
        ```python
        from msfabricutils.core import create_workspace_notebook

        notebook = create_workspace_notebook(
            workspace_id="12345678-1234-1234-1234-123456789012",
            notebook_path="/path/to/notebook",
            name="My New Notebook",
            description="Analysis notebook",
            wait_for_completion=True
        )
        ```
    """
    endpoint = f"workspaces/{workspace_id}/notebooks"

    notebook_name = name or os.path.basename(notebook_path).replace(".Notebook", "")

    notebook_content_file = notebook_path + "/notebook-content.py"
    notebook_platform_file = notebook_path + "/.platform"

    with open(notebook_content_file, "r") as f:
        notebook_content = f.read()
        encoded_notebook_content = base64.b64encode(notebook_content.encode()).decode()

    with open(notebook_platform_file, "r") as f:
        notebook_platform = f.read()
        encoded_notebook_platform = base64.b64encode(notebook_platform.encode()).decode()

    body = {
        "displayName": notebook_name,
        "description": description or "",
        "parts": [
            {
                "path": os.path.basename(notebook_content_file),
                "payload": encoded_notebook_content,
                "payloadType": "InlineBase64",
            },
            {
                "path": os.path.basename(notebook_platform_file),
                "payload": encoded_notebook_platform,
                "payloadType": "InlineBase64",
            },
        ],
    }

    response = post_request(endpoint, body, content_only=False)

    if response.status_code == 201:
        return response.json()

    if response.status_code == 202:
        if wait_for_completion:
            operation_id = response.headers["x-ms-operation-id"]
            retry_after = response.headers["Retry-After"]
            wait_for_long_running_operation(operation_id, retry_after)
            return get_workspace_notebook(workspace_id, notebook_name=name)

    return response


def update_workspace_notebook_definition(
    workspace_id: str,
    notebook_id: str,
    notebook_path: str,
    wait_for_completion: bool = True,
    update_metadata: bool = True,
) -> requests.Response | dict[str, str]:
    """
    Updates the definition of an existing notebook in the workspace.

    Args:
        workspace_id (str): The ID of the workspace containing the notebook.
        notebook_id (str): The ID of the notebook to update.
        notebook_path (str): The path to the updated notebook files (containing notebook-content.py and .platform).
        wait_for_completion (bool): Whether to wait for the update operation to complete. Defaults to True.
        update_metadata (bool): Whether to update the notebook's metadata. Defaults to True.

    Returns:
        Either a Response object or a dictionary containing the updated notebook details,
        depending on the operation status and wait_for_completion setting.

    Example:
        ```python
        from msfabricutils.core import update_workspace_notebook_definition

        updated_notebook = update_workspace_notebook_definition(
            workspace_id="12345678-1234-1234-1234-123456789012",
            notebook_id="beefbeef-beef-beef-beef-beefbeefbeef",
            notebook_path="/path/to/updated/notebook",
            wait_for_completion=True,
            update_metadata=True
        )
        ```
    """
    
    endpoint = f"workspaces/{workspace_id}/notebooks/{notebook_id}/updateDefinition?updateMetadata={update_metadata}"

    notebook_content_file = notebook_path + "/notebook-content.py"
    notebook_platform_file = notebook_path + "/.platform"

    with open(notebook_content_file, "r") as f:
        notebook_content = f.read()
        encoded_notebook_content = base64.b64encode(notebook_content.encode()).decode()

    with open(notebook_platform_file, "r") as f:
        notebook_platform = f.read()
        encoded_notebook_platform = base64.b64encode(notebook_platform.encode()).decode()

    body = {
        "definition": {
            "parts": [
                {
                    "path": os.path.basename(notebook_content_file),
                    "payload": encoded_notebook_content,
                    "payloadType": "InlineBase64",
                },
                {
                    "path": os.path.basename(notebook_platform_file),
                    "payload": encoded_notebook_platform,
                    "payloadType": "InlineBase64",
                },
            ],
        },
    }

    response = post_request(endpoint, body, content_only=False)

    if response.status_code == 200:
        notebook = get_workspace_notebook(workspace_id, notebook_id=notebook_id)
        return notebook

    if response.status_code == 202:
        if wait_for_completion:
            operation_id = response.headers["x-ms-operation-id"]
            retry_after = response.headers["Retry-After"]
            wait_for_long_running_operation(operation_id, retry_after)
            return get_workspace_notebook(workspace_id, notebook_id=notebook_id)

    return response    


def delete_workspace_notebook(workspace_id: str, notebook_id: str) -> requests.Response:
    """
    Deletes a notebook from the specified workspace.

    This function permanently removes a notebook from the workspace. The operation cannot be undone,
    so use with caution.

    Args:
        workspace_id (str): The ID of the workspace containing the notebook.
        notebook_id (str): The ID of the notebook to delete.

    Returns:
        requests.Response: The response from the delete request.

    Example:
        ```python
        from msfabricutils.core import delete_workspace_notebook

        response = delete_workspace_notebook(
            workspace_id="12345678-1234-1234-1234-123456789012",
            notebook_id="beefbeef-beef-beef-beef-beefbeefbeef"
        )
        ```

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
    """
    endpoint = f"workspaces/{workspace_id}/notebooks/{notebook_id}"
    return delete_request(endpoint)