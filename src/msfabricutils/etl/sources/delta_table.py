import polars as pl

from msfabricutils.core.auth import get_storage_options
from msfabricutils.etl.types import PolarsFrame


def source_delta(table_uri: str, eager: bool = False) -> PolarsFrame:
    """
    Reads a Delta table from the specified abfss URI. Automatically handles the authentication with OneLake.

    Args:
        table_uri (str): The abfss URI of the Delta table to read.
        eager (bool, optional): If True, reads the table eagerly; otherwise, returns a lazy frame. Defaults to False.

    Returns:
        PolarsFrame: The data from the Delta table.

    Example:
        ```python
        from msfabricutils.etl import source_delta

        workspace_id = "12345678-1234-1234-1234-123456789012"
        lakehouse_id = "beefbeef-beef-beef-beef-beefbeefbeef"
        table_name = "my-delta-table"
        table_uri = f"abfss://{workspace_id}@onelake.dfs.fabric.microsoft.com/{lakehouse_id}/Tables/{table_name}"

        df = source_delta(table_uri, eager=True)
        lazy_df = source_delta(table_uri, eager=False)
        ```
    """

    storage_options = get_storage_options() if table_uri.startswith("abfss://") else None

    if eager:
        return pl.read_delta(source=table_uri, storage_options=storage_options)

    return pl.scan_delta(source=table_uri, storage_options=storage_options)
