from typing import Any

from msfabricutils.core.generic import get_item_from_paginated, get_page, get_paginated


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

    return get_paginated(endpoint, data_key)


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
        return get_page(endpoint)
    
    if workspace_name is not None:
        endpoint = "workspaces"
        data_key = "value"
        item_key = "displayName"
        item_value = workspace_name

        return get_item_from_paginated(endpoint, data_key, item_key, item_value)
    
    raise ValueError("Either `workspace_id` or `workspace_name` must be provided")
