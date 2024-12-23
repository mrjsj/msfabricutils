from importlib.metadata import PackageNotFoundError, version

from msfabricutils.common.fabric_duckdb_connection import FabricDuckDBConnection
from msfabricutils.core import (
    get_azure_storage_access_token,
    get_fabric_bearer_token,
    get_onelake_access_token,
    get_workspace,
    get_workspace_lakehouse_tables,
    get_workspace_lakehouses,
    get_workspaces,
)

__all__ = (
    "FabricDuckDBConnection",
    "get_fabric_bearer_token",
    "get_azure_storage_access_token",
    "get_onelake_access_token",
    "get_workspace",
    "get_workspace_lakehouse_tables",
    "get_workspace_lakehouses",
    "get_workspaces",
)


try:
    __version__ = version("msfabricutils")
except PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"
