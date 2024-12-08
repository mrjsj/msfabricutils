import polars as pl
from deltalake import DeltaTable

from msfabricutils.core.auth import get_storage_options


def get_incremental_column_value(table_uri: str, incremental_column: str) -> int:
    """
    Retrieves the maximum value of the specified incremental column from a Delta table.

    Args:
        table_uri (str): The URI of the Delta table.
        incremental_column (str): The name of the incremental column.

    Returns:
        The maximum value of the incremental column, or 0 if the table does not exist.

    Example:
        ```python
        from msfabricutils.etl import get_incremental_column_value

        max_value = get_incremental_column_value("path/to/delta_table", "incremental_id")
        ```
    """

    storage_options = get_storage_options() if table_uri.startswith("abfss://") else None

    if not DeltaTable.is_deltatable(table_uri, storage_options=storage_options):
        return 0

    return (
        pl.scan_delta(table_uri, storage_options=storage_options)
        .select(pl.col(incremental_column))
        .max()
        .collect()
        .item()
    )
