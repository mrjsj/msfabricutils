from msfabricutils.core.generic import get_paginated


def get_workspace_lakehouses(workspace_id: str) -> list[dict]:
    """
    Retrieves lakehouses for a specified workspace.

    This function fetches a list of lakehouses from a specified workspace using the 
    `get_paginated` function. It constructs the appropriate endpoint and retrieves 
    paginated data associated with the workspace ID.

    Args:
        workspace_id (str): The ID of the workspace to retrieve lakehouses from.

    Returns:
        list[dict]: A list of dictionaries containing lakehouse data for the specified workspace.

    See Also:
        `get_paginated`: A helper function that handles paginated API requests.
    """    
    endpoint = f"workspaces/{workspace_id}/lakehouses"
    data_key = "value"

    return get_paginated(endpoint, data_key)


def get_workspace_lakehouse_tables(workspace_id: str, lakehouse_id: str) -> list[dict]:
    """
    Retrieves tables for a specified lakehouse within a workspace.

    This function fetches a list of tables from a specific lakehouse within a given workspace 
    using the `get_paginated` function. It constructs the appropriate endpoint and retrieves 
    paginated data associated with the workspace and lakehouse IDs.

    Args:
        workspace_id (str): The ID of the workspace containing the lakehouse.
        lakehouse_id (str): The ID of the lakehouse to retrieve tables from.

    Returns:
        list[dict]: A list of dictionaries containing table data for the specified lakehouse.

    See Also:
        `get_paginated`: A helper function that handles paginated API requests.
    """    
    endpoint = f"workspaces/{workspace_id}/lakehouses/{lakehouse_id}/tables"
    data_key = "data"

    return get_paginated(endpoint, data_key)
