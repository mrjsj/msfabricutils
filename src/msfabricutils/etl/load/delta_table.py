
import polars as pl
from deltalake import DeltaTable, write_deltalake

from msfabricutils.etl.helpers import get_max_column_value
from msfabricutils.etl.helpers.get_or_create_delta_table import get_or_create_delta_table
from msfabricutils.etl.helpers.merge_helpers import (
    build_merge_predicate,
    build_when_matched_update_columns,
    build_when_matched_update_predicate,
)
from msfabricutils.etl.types import PolarsFrame


def upsert(
    table_or_uri: str | DeltaTable,
    df: PolarsFrame,
    primary_key_columns: str | list[str],
    update_exclusion_columns: str | list[str] | None = None,
    predicate_exclusion_columns: str | list[str] | None = None,
) -> dict[str, str]:
    """
    Upserts dataframe into a Delta table using the provided primary key columns.

    Args:
        table_or_uri (str): The URI of the target Delta table.
        df (PolarsFrame): The dataframe to upsert.
        primary_key_columns (str | list[str]): Primary key column(s) for the upsert.
        update_exclusion_columns (str | list[str] | None): Columns which will not be updated in the merge.
        predicate_exclusion_columns (str | list[str] | None): Columns to exclude from the upsert. Difference between source and target of these columns will not trigger an update, however if there is a difference in the other columns, the row will be *also* be updated with the `excluded_columns`.

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
            primary_key_columns=["id"],
            static_audit_columns=["created_at"],
            dynamic_audit_columns=["modified_at", "valid_to"],
        )
        ```
    """

    if isinstance(primary_key_columns, str):
        primary_key_columns = [primary_key_columns]

    if update_exclusion_columns is None:
        update_exclusion_columns = []

    if isinstance(update_exclusion_columns, str):
        update_exclusion_columns = [update_exclusion_columns]        

    if predicate_exclusion_columns is None:
        predicate_exclusion_columns = []

    if isinstance(predicate_exclusion_columns, str):
        predicate_exclusion_columns = [predicate_exclusion_columns]

    if isinstance(df, pl.LazyFrame):
        df = df.collect()

    df = df.to_arrow()

    if isinstance(table_or_uri, str):
        dt = get_or_create_delta_table(table_or_uri, df.schema)
    else:
        dt = table_or_uri

    merge_predicate = build_merge_predicate(primary_key_columns)

    predicate_update_columns = [
        column
        for column in df.column_names
        if column
        not in primary_key_columns + predicate_exclusion_columns + update_exclusion_columns
    ]
    when_matched_update_predicates = build_when_matched_update_predicate(predicate_update_columns)

    update_columns = [
        column
        for column in df.column_names
        if column not in primary_key_columns + update_exclusion_columns
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


def overwrite(table_or_uri: str | DeltaTable, df: PolarsFrame) -> None:
    """
    Overwrites the entire Delta table with the provided dataframe.

    Args:
        table_or_uri (str): The URI of the target Delta table.
        df (PolarsFrame): The dataframe to write to the Delta table.

    Example:
        ```python
        from msfabricutils.etl import overwrite
        import polars as pl

        data = pl.DataFrame({...})

        overwrite("path/to/delta_table", data)
        ```
    """

    if isinstance(table_or_uri, str):
        dt = get_or_create_delta_table(table_or_uri, df.schema)
    else:
        dt = table_or_uri

    if isinstance(df, pl.LazyFrame):
        df = df.collect()

    df = df.to_arrow()

    write_deltalake(
        table_or_uri=dt,
        data=df,
        mode="overwrite",
    )


def replace_range(
    table_or_uri: str | DeltaTable,
    df: PolarsFrame,
    range_column: str,
) -> None:
    """
    Replaces a range of data in the Delta table based on a specified column.

    Args:
        table_or_uri (str): The URI of the target Delta table.
        df (PolarsFrame): The dataframe to write to the Delta table.
        range_column (str): The column used to determine the range of data to replace. This replaces the data in the range of the `range_column` in the delta table based off the min and max values of the `range_column` in the dataframe.

    Example:
        ```python
        from msfabricutils.etl import replace_range
        import polars as pl

        data = pl.DataFrame({...})

        replace_range("path/to/delta_table", data, range_column="date")
        ```
    """

    if isinstance(table_or_uri, str):
        dt = get_or_create_delta_table(table_or_uri, df.schema)
    else:
        dt = table_or_uri

    min_value, max_value = (
        df.select(
            pl.col(range_column).min(),
            pl.col(range_column).max(),
        )
        .collect()
        .row(0)
    )

    predicate = f'{range_column} >= "{min_value}" AND {range_column} <= "{max_value}"'

    if isinstance(df, pl.LazyFrame):
        df = df.collect()

    df = df.to_arrow()

    write_deltalake(
        table_or_uri=dt,
        data=df,
        mode="overwrite",
        predicate=predicate,
    )


def append(table_or_uri: str | DeltaTable, df: PolarsFrame) -> None:
    """
    Appends the provided dataframe to the Delta table.

    Args:
        table_or_uri (str): The URI of the target Delta table.
        df (PolarsFrame): The dataframe to append to the Delta table.

    Example:
        ```python
        from msfabricutils.etl import append
        import polars as pl

        data = pl.DataFrame({...})

        append("path/to/delta_table", data)
        ```
    """

    if isinstance(table_or_uri, str):
        dt = get_or_create_delta_table(table_or_uri, df.schema)
    else:
        dt = table_or_uri

    if isinstance(df, pl.LazyFrame):
        df = df.collect()

    df = df.to_arrow()

    write_deltalake(
        table_or_uri=dt,
        data=df,
        mode="append",
    )


def incremental(table_or_uri: str | DeltaTable, df: PolarsFrame, incremental_column: str) -> None:
    """
    Appends new data to the Delta table based on an incremental column.

    Args:
        table_or_uri (str): The URI of the target Delta table.
        df (PolarsFrame): The dataframe to append to the Delta table.
        incremental_column (str): The column used to determine new data to append. The source dataframe will only append rows where the value of the `incremental_column` is greater than the max value of the `incremental_column` in the delta table.

    Example:
        ```python
        from msfabricutils.etl import incremental
        import polars as pl

        data = pl.DataFrame({...})

        incremental("path/to/delta_table", data, incremental_column="timestamp")
        ```
    """

    if isinstance(table_or_uri, str):
        dt = get_or_create_delta_table(table_or_uri, df.schema)
    else:
        dt = table_or_uri

    max_value = get_max_column_value(table_or_uri, incremental_column)

    df = df.filter(pl.col(incremental_column) > max_value)

    if isinstance(df, pl.LazyFrame):
        df = df.collect()

    df = df.to_arrow()

    write_deltalake(
        table_or_uri=dt,
        data=df,
        mode="append",
    )


