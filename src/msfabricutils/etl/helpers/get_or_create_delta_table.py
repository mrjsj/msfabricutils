import polars as pl
from deltalake import DeltaTable

from msfabricutils.core.auth import get_storage_options


def get_or_create_delta_table(table_uri: str, schema: pl.Schema) -> DeltaTable:
    """
    Retrieves a Delta table or creates a new one if it does not exist.

    Args:
        table_uri (str): The URI of the Delta table.
        schema (pl.Schema): The Polars schema to create the Delta table with.

    Returns:
        The Delta table.
    """

    storage_options = get_storage_options() if table_uri.startswith("abfss://") else None

    if DeltaTable.is_deltatable(table_uri, storage_options=storage_options):
        dt = DeltaTable(table_uri, storage_options=storage_options)
    else:
        dt = DeltaTable.create(table_uri, schema, storage_options=storage_options)

    return dt

