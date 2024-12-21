from msfabricutils.core.generic import get_item_from_paginated, get_paginated
from msfabricutils.core.workspace import get_workspace


def get_workspace_lakehouses(
    workspace_id: str | None = None, workspace_name: str | None = None
) -> list[dict]:
    """
    Retrieves lakehouses for a specified workspace by either `workspace_id` or `workspace_name`.

    Args:
        workspace_id (str | None): The ID of the workspace to retrieve lakehouses from.
        workspace_name (str | None): The name of the workspace to retrieve lakehouses from.

    Returns:
        A list of dictionaries containing lakehouse data for the specified workspace.

    Example:
        By `workspace_id`:
        ```python
        from msfabricutils.core import get_workspace_lakehouses

        lakehouses = get_workspace_lakehouses("12345678-1234-1234-1234-123456789012")
        ```

        By `workspace_name`:
        ```python
        from msfabricutils.core import get_workspace_lakehouses
        lakehouses = get_workspace_lakehouses(workspace_name="My Workspace")
        ```
    """
    data_key = "value"

    if workspace_id is not None:
        endpoint = f"workspaces/{workspace_id}/lakehouses"
        return get_paginated(endpoint, data_key)

    if workspace_name is not None:
        workspace_id = get_workspace(workspace_name=workspace_name)["id"]
        endpoint = f"workspaces/{workspace_id}/lakehouses"
        return get_paginated(endpoint, data_key)

    raise ValueError("Either `workspace_id` or `workspace_name` must be provided")


def get_workspace_lakehouse_tables(
    workspace_id: str | None = None,
    workspace_name: str | None = None,
    lakehouse_id: str | None = None,
    lakehouse_name: str | None = None,
) -> list[dict]:
    """
    Retrieves tables for a specified lakehouse within a workspace by either `workspace_id` or `workspace_name` and `lakehouse_id` or `lakehouse_name`.

    Args:
        workspace_id (str | None): The ID of the workspace containing the lakehouse.
        workspace_name (str | None): The name of the workspace containing the lakehouse.
        lakehouse_id (str | None): The ID of the lakehouse to retrieve tables from.
        lakehouse_name (str | None): The name of the lakehouse to retrieve tables from.

    Returns:
        A list of dictionaries containing table data for the specified lakehouse.

    Example:
        By `workspace_id` and `lakehouse_id`:
        ```python
        from msfabricutils.core import get_workspace_lakehouse_tables

        tables = get_workspace_lakehouse_tables(
            "12345678-1234-1234-1234-123456789012",
            "beefbeef-beef-beef-beef-beefbeefbeef"
        )
        ```

        By `workspace_name` and `lakehouse_name`:
        ```python
        from msfabricutils.core import get_workspace_lakehouse_tables

        tables = get_workspace_lakehouse_tables(
            workspace_name="My Workspace",
            lakehouse_name="My Lakehouse"
        )
        ```

        By `workspace_name` and `lakehouse_id`:
        ```python
        from msfabricutils.core import get_workspace_lakehouse_tables

        tables = get_workspace_lakehouse_tables(
            workspace_name="My Workspace",
            lakehouse_id="beefbeef-beef-beef-beef-beefbeefbeef"
        )
        ```

        By `workspace_id` and `lakehouse_name`:
        ```python
        from msfabricutils.core import get_workspace_lakehouse_tables

        tables = get_workspace_lakehouse_tables(
            workspace_id="12345678-1234-1234-1234-123456789012",
            lakehouse_name="My Lakehouse"
        )
        ```
    """
    if workspace_id is None and workspace_name is None:
        raise ValueError("Either `workspace_id` or `workspace_name` must be provided")
    
    if lakehouse_id is None and lakehouse_name is None:
        raise ValueError("Either `lakehouse_id` or `lakehouse_name` must be provided")
    
    if workspace_id is None:
        workspace_id = get_workspace(workspace_name=workspace_name)["id"]
    
    if lakehouse_id is None:
        endpoint = f"workspaces/{workspace_id}/lakehouses"
        data_key = "value"
        item_key = "displayName"
        item_value = lakehouse_name

        lakehouse_id = get_item_from_paginated(
            endpoint=endpoint,
            data_key=data_key,
            item_key=item_key,
            item_value=item_value
        )["id"]
    
    endpoint = f"workspaces/{workspace_id}/lakehouses/{lakehouse_id}/tables"
    data_key = "data"

    return get_paginated(endpoint, data_key)
