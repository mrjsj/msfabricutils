from msfabricutils.core.generic import get_paginated


def get_workspace_lakehouses(workspace_id: str):
    endpoint = f"workspaces/{workspace_id}/lakehouses"
    data_key = "value"

    return get_paginated(endpoint, data_key)


def get_workspace_lakehouse_tables(workspace_id: str, lakehouse_id: str):
    endpoint = f"workspaces/{workspace_id}/lakehouses/{lakehouse_id}/tables"
    data_key = "data"

    return get_paginated(endpoint, data_key)
