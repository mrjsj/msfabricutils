from msfabricutils.core.fabric_request import paginated_get_request
from msfabricutils.core.workspace import get_workspace


def get_workspace_sql_endpoints(
    workspace_id: str | None = None, workspace_name: str | None = None
) -> list[dict]:
    """
    Retrieves SQL endpoints for a specified workspace by either `workspace_id` or `workspace_name`.

    This function fetches a list of SQL endpoints from a specified workspace

    Args:
        workspace_id (str | None): The ID of the workspace to retrieve SQL endpoints from.
        workspace_name (str | None): The name of the workspace to retrieve SQL endpoints from.

    Returns:
        A list of dictionaries containing SQL endpoint data for the specified workspace.

    Example:
        By `workspace_id`:
        ```python
        from msfabricutils.core import get_workspace_sql_endpoints

        sql_endpoints = get_workspace_sql_endpoints("12345678-1234-1234-1234-123456789012")
        ```

        By `workspace_name`:
        ```python
        from msfabricutils.core import get_workspace_sql_endpoints
        sql_endpoints = get_workspace_sql_endpoints(workspace_name="My Workspace")
        ```
    """
    data_key = "value"

    if workspace_id is not None:
        endpoint = f"workspaces/{workspace_id}/sqlEndpoints"
        return paginated_get_request(endpoint, data_key)

    if workspace_name is not None:
        workspace_id = get_workspace(workspace_name=workspace_name)["id"]
        endpoint = f"workspaces/{workspace_id}/sqlEndpoints"
        return paginated_get_request(endpoint, data_key)

    raise ValueError("Either `workspace_id` or `workspace_name` must be provided")
