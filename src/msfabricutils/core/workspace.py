from msfabricutils.core.generic import get_paginated, get_page


def get_workspaces():
    endpoint = "workspaces"
    data_key = "value"

    return get_paginated(endpoint, data_key)


def get_workspace(workspace_id: str):
    endpoint = f"workspaces/{workspace_id}"

    return get_page(endpoint)
