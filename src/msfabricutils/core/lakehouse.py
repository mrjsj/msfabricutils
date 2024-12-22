import requests

from msfabricutils.core.fabric_request import (
    delete_request,
    get_item_from_paginated_get_request,
    get_request,
    paginated_get_request,
    patch_request,
    post_request,
)
from msfabricutils.core.workspace import get_workspace


def get_workspace_lakehouses(
    workspace_id: str | None = None, workspace_name: str | None = None
) -> list[dict[str, str]]:
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
        return paginated_get_request(endpoint, data_key)

    if workspace_name is not None:
        workspace_id = get_workspace(workspace_name=workspace_name)["id"]
        endpoint = f"workspaces/{workspace_id}/lakehouses"
        return paginated_get_request(endpoint, data_key)

    raise ValueError("Either `workspace_id` or `workspace_name` must be provided")


def get_workspace_lakehouse(workspace_id: str | None = None, lakehouse_id: str | None = None, lakehouse_name: str | None = None) -> dict[str, str]:
    """
    Retrieves details of a specified lakehouse by either `lakehouse_id` or `lakehouse_name`.

    Args:
        workspace_id (str | None): The ID of the workspace containing the lakehouse.
        lakehouse_id (str | None): The ID of the lakehouse to retrieve details for.
        lakehouse_name (str | None): The name of the lakehouse to retrieve details for.

    Returns:
        A dictionary containing the details of the specified lakehouse.

    Example:
        By `workspace_id` and `lakehouse_id`:
        ```python
        from msfabricutils.core import get_workspace

        lakehouse = get_workspace_lakehouse(workspace_id="12345678-1234-1234-1234-123456789012", lakehouse_id="beefbeef-beef-beef-beef-beefbeefbeef")
        ```

        By `workspace_id` and `lakehouse_name`:
        ```python
        from msfabricutils.core import get_workspace_lakehouse
        lakehouse = get_workspace_lakehouse(workspace_id="12345678-1234-1234-1234-123456789012", lakehouse_name="My Lakehouse")
        ```
    """

    if lakehouse_id is not None:
        endpoint = f"workspaces/{workspace_id}/lakehouses/{lakehouse_id}"
        return get_request(endpoint)
    
    if lakehouse_name is not None:
        endpoint = f"workspaces/{workspace_id}/lakehouses"
        data_key = "value"
        item_key = "displayName"
        item_value = lakehouse_name

        return get_item_from_paginated_get_request(endpoint, data_key, item_key, item_value)
    
    raise ValueError("Either `lakehouse_id` or `lakehouse_name` must be provided")

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

        lakehouse_id = get_item_from_paginated_get_request(
            endpoint=endpoint,
            data_key=data_key,
            item_key=item_key,
            item_value=item_value
        )["id"]
    
    endpoint = f"workspaces/{workspace_id}/lakehouses/{lakehouse_id}/tables"
    data_key = "data"

    return paginated_get_request(endpoint, data_key)


def create_workspace_lakehouse(workspace_id: str, lakehouse_name: str, enable_schemas: bool = False, description: str | None = None) -> dict[str, str]:
    """
    Creates a new lakehouse in the specified workspace.

    Args:
        workspace_id (str): The ID of the workspace where the lakehouse will be created.
        lakehouse_name (str): The display name for the new lakehouse.
        enable_schemas (bool): Whether to enable schemas for the lakehouse. Defaults to False.
        description (str | None): Optional description for the lakehouse. Defaults to "test" if not provided.

    Returns:
        A dictionary containing the details of the created lakehouse.

    Example:
        ```python
        from msfabricutils.core import create_workspace_lakehouse

        lakehouse = create_workspace_lakehouse(
            workspace_id="12345678-1234-1234-1234-123456789012",
            lakehouse_name="My New Lakehouse",
            enable_schemas=True,
            description="Production lakehouse for data analytics"
        )
        ```
    """
    endpoint = f"workspaces/{workspace_id}/lakehouses"
    data = {
        "displayName": lakehouse_name,
        "description": description or "test",
    }

    if enable_schemas:
        data["creationPayload"] = {
            "enableSchemas": enable_schemas
        }

    import logging
    logging.info(f"Creating lakehouse {lakehouse_name} with data: {data}")

    return post_request(endpoint, data)


def update_workspace_lakehouse(workspace_id: str, lakehouse_id: str, lakehouse_name: str | None = None, description: str | None = None) -> dict[str, str]:
    """
    Updates an existing lakehouse in the specified workspace.

    Args:
        workspace_id (str): The ID of the workspace containing the lakehouse.
        lakehouse_id (str): The ID of the lakehouse to update.
        lakehouse_name (str | None): Optional new name for the lakehouse.
        description (str | None): Optional new description for the lakehouse.

    Returns:
        A dictionary containing the details of the updated lakehouse.

    Example:
        ```python
        from msfabricutils.core import update_workspace_lakehouse

        updated_lakehouse = update_workspace_lakehouse(
            workspace_id="12345678-1234-1234-1234-123456789012",
            lakehouse_id="beefbeef-beef-beef-beef-beefbeefbeef",
            lakehouse_name="Updated Lakehouse Name",
            description="Updated description"
        )
        ```
    """
    endpoint = f"workspaces/{workspace_id}/lakehouses/{lakehouse_id}"

    data = {}
    if lakehouse_name is not None:
        data["displayName"] = lakehouse_name
    if description is not None:
        data["description"] = description

    return patch_request(endpoint, data)


def delete_workspace_lakehouse(workspace_id: str, lakehouse_id: str) -> requests.Response:
    """
    Deletes a lakehouse from the specified workspace.

    Args:
        workspace_id (str): The ID of the workspace containing the lakehouse.
        lakehouse_id (str): The ID of the lakehouse to delete.

    Returns:
        The response from the delete request.

    Example:
        ```python
        from msfabricutils.core import delete_workspace_lakehouse

        response = delete_workspace_lakehouse(
            workspace_id="12345678-1234-1234-1234-123456789012",
            lakehouse_id="beefbeef-beef-beef-beef-beefbeefbeef"
        )
        ```
    """
    endpoint = f"workspaces/{workspace_id}/lakehouses/{lakehouse_id}"
    return delete_request(endpoint)
