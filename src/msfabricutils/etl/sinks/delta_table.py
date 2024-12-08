import polars as pl
from deltalake import DeltaTable

from msfabricutils.etl import Config
from msfabricutils.etl.helpers.merge_helpers import (
    build_merge_predicate,
    build_when_matched_update_columns,
    build_when_matched_update_predicate,
)
from msfabricutils.etl.types import PolarsFrame


def upsert_scd_type_1(
    table_uri: str,
    df: PolarsFrame,
    primary_key_columns: str | list[str],
    config: Config | None = None,
    exclude_columns: str | list[str] | None = None,
) -> dict[str:str]:
    """
    Upserts dataframe into a Delta table using Slowly Changing Dimension (SCD) Type 1.

    Args:
        table_uri (str): The URI of the target Delta table.
        df (PolarsFrame): The dataframe to upsert.
        config (Config | None): Configuration object containing audit column information.
        primary_key_columns (str | list[str]): Primary key column(s) for the upsert.
        exclude_columns (str | list[str] | None): Columns to exclude from the upsert.

    Returns:
        Result of the merge operation.

    Example:
        ```python
        from msfabricutils.etl import Config, upsert_scd_type_1
        import polars as pl


        config = get_default_config()
        data = pl.DataFrame({...})

        upsert_scd_type_1(
            "path/to/delta_table",
            data,
            config,
            primary_key_columns=["id"]
        )
        ```
    """

    dynamic_audit_columns = config.get_dynamic_audit_columns() if config else []
    static_audit_columns = config.get_static_audit_columns() if config else []

    if exclude_columns is None:
        exclude_columns = []

    if isinstance(primary_key_columns, str):
        primary_key_columns = [primary_key_columns]
    primary_key_columns = [config.normalization_strategy(column) for column in primary_key_columns]

    if isinstance(exclude_columns, str):
        exclude_columns = [exclude_columns]

    if isinstance(df, pl.LazyFrame):
        df = df.collect()

    df = df.to_arrow()

    if DeltaTable.is_deltatable(table_uri):
        dt = DeltaTable(table_uri)
    else:
        dt = DeltaTable.create(table_uri, df.schema)

    merge_predicate = build_merge_predicate(primary_key_columns)

    predicate_update_columns = [
        column
        for column in df.column_names
        if column
        not in primary_key_columns + exclude_columns + static_audit_columns + dynamic_audit_columns
    ]

    when_matched_update_predicates = build_when_matched_update_predicate(predicate_update_columns)
    update_columns = [
        column
        for column in df.column_names
        if column not in primary_key_columns + exclude_columns + static_audit_columns
    ]

    when_matched_update_columns = build_when_matched_update_columns(update_columns)
    table_merger = (
        dt.merge(
            df,
            source_alias="source",
            target_alias="target",
            predicate=merge_predicate,
        )
        .when_matched_update(
            predicate=when_matched_update_predicates, updates=when_matched_update_columns
        )
        .when_not_matched_insert_all()
    )

    return table_merger.execute()
