from typing import Any

import requests

from msfabricutils.core.fabric_request import (
    delete_request,
    get_item_from_paginated_get_request,
    get_request,
    paginated_get_request,
    patch_request,
    post_request,
)


def get_workspaces() -> list[dict[str, Any]]:
    """
    Retrieves a list of workspaces.

    Returns:
        A list of dictionaries containing data for the available workspaces.

    Example:
        ```python
        from msfabricutils.core import get_workspaces

        workspaces = get_workspaces()
        ```
    """
    endpoint = "workspaces"
    data_key = "value"

    return paginated_get_request(endpoint, data_key)


def get_workspace(workspace_id: str | None = None, workspace_name: str | None = None) -> dict[str, Any]:
    """
    Retrieves details of a specified workspace by either `workspace_id` or `workspace_name`.

    Args:
        workspace_id (str | None): The ID of the workspace to retrieve details for.
        workspace_name (str | None): The name of the workspace to retrieve details for.

    Returns:
        A dictionary containing the details of the specified workspace.

    Example:
        By `workspace_id`:
        ```python
        from msfabricutils.core import get_workspace

        workspace = get_workspace("12345678-1234-1234-1234-123456789012")
        ```

        By `workspace_name`:
        ```python
        from msfabricutils.core import get_workspace
        workspace = get_workspace(workspace_name="My Workspace")
        ```
    """

    if workspace_id is not None:
        endpoint = f"workspaces/{workspace_id}"
        return get_request(endpoint)
    
    if workspace_name is not None:
        endpoint = "workspaces"
        data_key = "value"
        item_key = "displayName"
        item_value = workspace_name

        return get_item_from_paginated_get_request(endpoint, data_key, item_key, item_value)
    
    raise ValueError("Either `workspace_id` or `workspace_name` must be provided")


def create_workspace(workspace_name: str, description: str | None = None) -> dict[str, Any]:
    endpoint = "workspaces"
    data = {
        "displayName": workspace_name,
        "description": description or ""
    }

    return post_request(endpoint, data)


def assign_workspace_to_capacity(workspace_id: str, capacity_id: str) -> requests.Response:
    """
    Assigns a workspace to a capacity.

    Args:
        workspace_id (str): The ID of the workspace to assign to a capacity.
        capacity_id (str): The ID of the capacity to assign the workspace to.

    Returns:
        The response from the assign request.
    """
    endpoint = f"workspaces/{workspace_id}/assignToCapacity"
    data = {
        "capacityId": capacity_id
    }
    return post_request(endpoint, data)

def update_workspace(workspace_id: str, workspace_name: str | None = None, description: str | None = None) -> dict[str, Any]:
    """
    Updates a workspace.

    Args:
        workspace_id (str): The ID of the workspace to update.
        workspace_name (str | None): The name of the workspace to update.
        description (str | None): The description of the workspace to update.

    Returns:
        A dictionary containing the details of the updated workspace.
    """
    endpoint = f"workspaces/{workspace_id}"

    data = {}
    if workspace_name is not None:
        data["displayName"] = workspace_name
    if description is not None:
        data["description"] = description

    return patch_request(endpoint, data)


def delete_workspace(workspace_id: str) -> requests.Response:
    """
    Deletes a workspace.

    Args:
        workspace_id (str): The ID of the workspace to delete.

    Returns:
        The response from the delete request.
    """
    endpoint = f"workspaces/{workspace_id}"
    return delete_request(endpoint)

