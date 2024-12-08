import polars as pl

from msfabricutils.core.auth import get_storage_options
from msfabricutils.etl.types import PolarsFrame


def source_parquet(table_uri: str, eager: bool = False) -> PolarsFrame:
    """
    Reads a Parquet file from the specified abfss URI. Automatically handles the authentication with OneLake.

    Args:
        table_uri (str): The abfss URI of the Parquet file to read. Supports globbing.
        eager (bool, optional): If True, reads the file eagerly; otherwise, returns a lazy frame. Defaults to False.

    Returns:
        PolarsFrame: The data from the Parquet file.

    Example:
        Reading a single file
        ```python
        from msfabricutils.etl import source_parquet

        workspace_id = "12345678-1234-1234-1234-123456789012"
        lakehouse_id = "beefbeef-beef-beef-beef-beefbeefbeef"

        file_path = "my-parquet-file.parquet"
        folder_uri = f"abfss://{workspace_id}@onelake.dfs.fabric.microsoft.com/{lakehouse_id}/Files/"

        df = source_parquet(folder_uri + file_path, eager=True)
        ```

        Reading all Parquet files in a folder
        ```python
        from msfabricutils.etl import source_parquet

        workspace_id = "12345678-1234-1234-1234-123456789012"
        lakehouse_id = "beefbeef-beef-beef-beef-beefbeefbeef"

        folder_uri = f"abfss://{workspace_id}@onelake.dfs.fabric.microsoft.com/{lakehouse_id}/Files/"
        glob_df = source_parquet(folder_uri + "**/*.parquet", eager=True)
        ```
    """

    storage_options = get_storage_options() if table_uri.startswith("abfss://") else None

    if eager:
        return pl.read_parquet(
            source=table_uri, hive_partitioning=True, storage_options=storage_options
        )

    return pl.scan_parquet(
        source=table_uri, hive_partitioning=True, storage_options=storage_options
    )
