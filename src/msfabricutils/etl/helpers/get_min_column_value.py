import polars as pl
from deltalake import DeltaTable

from msfabricutils.core.auth import get_storage_options


def get_min_column_value(table_or_uri: str | DeltaTable, column_name: str) -> int:
    """
    Retrieves the maximum value of the specified column from a Delta table.

    Args:
        table_or_uri (str | DeltaTable): A string URI to a Delta table or a DeltaTable instance.
        column_name (str): The name of the column.

    Returns:
        The minimum value of the column, or 0 if the table does not exist.

    Example:
        ```python
        from msfabricutils.etl import get_min_column_value

        min_value = get_min_column_value("path/to/delta_table", "incremental_id")
        ```
    """

    storage_options = get_storage_options() if table_or_uri.startswith("abfss://") else None
    
    if isinstance(table_or_uri, str):
        if not DeltaTable.is_deltatable(table_or_uri, storage_options=storage_options):
            return 0

    return (
        pl.scan_delta(table_or_uri, storage_options=storage_options)
        .select(pl.col(column_name))
        .min()
        .collect()
        .item()
    )
