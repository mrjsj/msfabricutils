from msfabricutils.core.generic import get_paginated, get_page
from typing import Any

def get_workspaces() -> list[dict[str, Any]]:
    """
    Retrieves a list of workspaces.

    This function fetches a list of workspaces using the `get_paginated` function. 
    It constructs the appropriate endpoint and retrieves the paginated data associated 
    with workspaces.

    Returns:
        A list of dictionaries containing data for the available workspaces.

    See Also:
        `get_paginated`: A helper function that handles paginated API requests.
    """    
    endpoint = "workspaces"
    data_key = "value"

    return get_paginated(endpoint, data_key)


def get_workspace(workspace_id: str) -> dict[str, Any]:
    """
    Retrieves details of a specified workspace.

    This function fetches the details of a specific workspace by using the `get_page` 
    function. It constructs the appropriate endpoint based on the provided workspace ID.

    Args:
        workspace_id (str): The ID of the workspace to retrieve details for.

    Returns:
        A dictionary containing the details of the specified workspace.

    See Also:
        `get_page`: A helper function that retrieves a single page of data from the API.
    """    
    endpoint = f"workspaces/{workspace_id}"

    return get_page(endpoint)
