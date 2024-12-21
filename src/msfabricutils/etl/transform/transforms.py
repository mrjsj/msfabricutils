from typing import Callable

import polars as pl
from polars.exceptions import ColumnNotFoundError

from msfabricutils.etl.config import Column
from msfabricutils.etl.types import PolarsFrame


def add_audit_columns(df: PolarsFrame, audit_columns: list[Column]) -> PolarsFrame:
    """
    Adds audit columns to the given DataFrame or LazyFrame based on the configuration.

    Args:
        df (PolarsFrame): The DataFrame or LazyFrame to which audit columns will be added.
        audit_columns (list[Column]): A list of audit columns to put on the DataFrame.

    Returns:
        The DataFrame or LazyFrame with the added audit columns.

    Example:
        ```python
        from msfabricutils.etl import add_audit_columns
        import polars as pl

        audit_columns = [
            Column(
               "created_at", pl.lit(datetime.now(timezone.utc)).cast(pl.Datetime("us", "UTC"))
            )
        ]
        df = pl.DataFrame({"data": [1, 2, 3]})
        updated_df = add_audit_columns(df, audit_columns)
        ```
    """

    df = df.with_columns(
        [audit_column.default_value.alias(audit_column.name) for audit_column in audit_columns]
    )
    return df


def deduplicate(
    df: PolarsFrame,
    primary_key_columns: str | list[str] | None = None,
    deduplication_order_columns: str | list[str] | None = None,
    deduplication_order_descending: bool | list[bool] = True,
) -> PolarsFrame:
    """
    Removes duplicate rows from the DataFrame based on primary key columns.

    Args:
        df (PolarsFrame): The DataFrame or LazyFrame from which duplicates will be removed.
        primary_key_columns (list[str] | None): The columns to use as primary keys for deduplication.
        deduplication_order_columns (list[str] | None): The columns to determine the order of rows for deduplication.
        deduplication_order_descending (bool | list[bool]): Whether to sort the deduplication order in descending order.

    Returns:
        PolarsFrame: The DataFrame or LazyFrame with duplicates removed.

    Example:
        ```python
        import polars as pl

        df = pl.DataFrame({
            "id": [1, 2, 2, 3],
            "value": ["a", "b", "b", "c"]
        })
        deduped_df = deduplicate(df, primary_key_columns=["id"])
        ```
    """

    if isinstance(primary_key_columns, str):
        primary_key_columns = [primary_key_columns]

    # Temporary fix start
    # See GitHub issue: https://github.com/pola-rs/polars/issues/20209
    # TODO: Remove this once the issue is fixed.
    # .unique() does not check if subset columns exist in the dataframe if it is empty, so it's silently ignores.

    if isinstance(df, pl.LazyFrame):
        columns = df.collect_schema().names()
    else:
        columns = df.schema.names()

    if primary_key_columns:
        for column in primary_key_columns:
            if column not in columns:
                raise ColumnNotFoundError(
                    f"unable to find column `{column}`. Valid columns: {columns}"
                )

    # Temporary fix end

    if deduplication_order_columns:
        df = df.sort(
            deduplication_order_columns, descending=deduplication_order_descending, nulls_last=True
        )

    df = df.unique(subset=primary_key_columns, keep="first")

    return df


def normalize_column_names(
    df: PolarsFrame, normalization_strategy: Callable[[str], str]
) -> PolarsFrame:
    """
    Normalizes the column names of the DataFrame using a provided normalization strategy.

    Args:
        df (PolarsFrame): The DataFrame or LazyFrame whose column names will be normalized.
        normalization_strategy (Callable[[str], str]): A callable which takes a string and returns a modified string.

    Returns:
        PolarsFrame: The DataFrame or LazyFrame with normalized column names.

    Example:
        ```python
        import polars as pl

        def my_strategy(old_column_name: str) -> str:
            new_name = old_column_name.replace(" ").lower()
            return new_name

        df = pl.DataFrame({"First Name": [1, 2], "Last Name": [3, 4]})
        normalized_df = normalize_column_names(df, my_strategy)
        ```
    """

    if isinstance(df, pl.LazyFrame):
        columns = df.collect_schema().names()
    else:
        columns = df.schema.names()

    column_mapping = {old_name: normalization_strategy(old_name) for old_name in columns}

    df = df.rename(column_mapping)

    return df


def reorder_columns_by_suffix(
    df: PolarsFrame, suffix_order: list[str], sort_alphabetically_within_group: bool = True
) -> PolarsFrame:
    """
    Reorders DataFrame columns based on their suffixes according to the provided order.

    Args:
        df (PolarsFrame): The DataFrame or LazyFrame whose columns will be reordered.
        suffix_order (list[str]): List of suffixes in the desired order.
        sort_alphabetically_within_group (bool): Whether to sort columns alphabetically within each suffix group.

    Returns:
        PolarsFrame: The DataFrame or LazyFrame with reordered columns.

    Example:
        ```python
        import polars as pl

        df = pl.DataFrame({
            "name_key": ["a", "b"],
            "age_key": [1, 2],
            "name_value": ["x", "y"],
            "age_value": [10, 20]
        })
        reordered_df = reorder_columns_by_suffix(df, suffix_order=["_key", "_value"])
        ```
    """
    if isinstance(df, pl.LazyFrame):
        columns = df.collect_schema().names()
    else:
        columns = df.schema.names()

    if sort_alphabetically_within_group:
        columns = sorted(columns)

    reordered_columns = []
    for suffix in suffix_order:
        reordered_columns.extend(
            [
                column
                for column in columns
                if column.endswith(suffix) and column not in reordered_columns
            ]
        )

    reordered_columns.extend([column for column in columns if column not in reordered_columns])

    return df.select(reordered_columns)


def reorder_columns_by_prefix(
    df: PolarsFrame, prefix_order: list[str], sort_alphabetically_within_group: bool = True
) -> PolarsFrame:
    """
    Reorders DataFrame columns based on their prefixes according to the provided order.

    Args:
        df (PolarsFrame): The DataFrame or LazyFrame whose columns will be reordered.
        prefix_order (list[str]): List of prefixes in the desired order.
        sort_alphabetically_within_group (bool): Whether to sort columns alphabetically within each prefix group.

    Returns:
        PolarsFrame: The DataFrame or LazyFrame with reordered columns.

    Example:
        ```python
        import polars as pl

        df = pl.DataFrame({
            "dim_name": ["a", "b"],
            "dim_age": [1, 2],
            "fact_sales": [100, 200],
            "fact_quantity": [5, 10]
        })
        reordered_df = reorder_columns_by_prefix(df, prefix_order=["dim_", "fact_"])
        ```
    """
    if isinstance(df, pl.LazyFrame):
        columns = df.collect_schema().names()
    else:
        columns = df.schema.names()

    if sort_alphabetically_within_group:
        columns = sorted(columns)

    reordered_columns = []
    for suffix in prefix_order:
        reordered_columns.extend(
            [
                column
                for column in columns
                if column.startswith(suffix) and column not in reordered_columns
            ]
        )

    reordered_columns.extend([column for column in columns if column not in reordered_columns])

    return df.select(reordered_columns)


def apply_scd_type_2(
    source_df: PolarsFrame,
    target_df: PolarsFrame,
    primary_key_columns: str | list[str],
    valid_from_column: str,
    valid_to_column: str,
) -> PolarsFrame:
    """
    Applies Slowly Changing Dimension (SCD) Type 2 logic to merge source and target DataFrames.
    SCD Type 2 maintains historical records by creating new rows for changed data while preserving
    the history through valid_from and valid_to dates.

    The result maintains the full history of changes while ensuring proper date ranges for overlapping records.

    Args:
        source_df (PolarsFrame): The new/source DataFrame containing updated records.
        target_df (PolarsFrame): The existing/target DataFrame containing current records.
        primary_key_columns (str | list[str]): Column(s) that uniquely identify each entity.
        valid_from_column (str): Column name containing the validity start date.
        valid_to_column (str): Column name containing the validity end date.

    Returns:
        PolarsFrame: A DataFrame containing both current and historical records with updated validity periods.

    Example:
        ```python
        import polars as pl
        from datetime import datetime

        # Create sample source and target dataframes
        source_df = pl.DataFrame({
            "customer_id": [1, 2],
            "name": ["John Updated", "Jane"],
            "valid_from": [datetime(2024, 1, 1), datetime(2024, 1, 1)]
        })

        target_df = pl.DataFrame({
            "customer_id": [1, 2],
            "name": ["John", "Jane"],
            "valid_from": [datetime(2023, 1, 1), datetime(2023, 1, 1)],
            "valid_to": [None, None]
        })

        # Apply SCD Type 2
        result_df = apply_scd_type_2(
            source_df=source_df,
            target_df=target_df,
            primary_key_columns="customer_id",
            valid_from_column="valid_from",
            valid_to_column="valid_to"
        )

        print(result_df.sort("customer_id", "valid_from"))
        
        shape: (4, 4)
        ┌─────────────┬──────────────┬─────────────────────┬─────────────────────┐
        │ customer_id ┆ name         ┆ valid_from          ┆ valid_to            │
        │ ---         ┆ ---          ┆ ---                 ┆ ---                 │
        │ i64         ┆ str          ┆ datetime[μs]        ┆ datetime[μs]        │
        ╞═════════════╪══════════════╪═════════════════════╪═════════════════════╡
        │ 1           ┆ John         ┆ 2023-01-01 00:00:00 ┆ 2024-01-01 00:00:00 │
        │ 1           ┆ John Updated ┆ 2024-01-01 00:00:00 ┆ null                │
        │ 2           ┆ Jane         ┆ 2023-01-01 00:00:00 ┆ 2024-01-01 00:00:00 │
        │ 2           ┆ Jane Updated ┆ 2024-01-01 00:00:00 ┆ null                │
        └─────────────┴──────────────┴─────────────────────┴─────────────────────┘        
        ```

    Notes:
        - The function handles overlapping date ranges by adjusting valid_to dates
        - NULL in valid_to indicates a currently active record
        - Records in source_df will create new versions if they differ from target_df
        - Historical records are preserved with appropriate valid_to dates
    """
    if isinstance(primary_key_columns, str):
        primary_key_columns = [primary_key_columns]

    target_columns = target_df.schema.names() if isinstance(target_df, pl.DataFrame) else target_df.collect_schema().names()

    # Find records in the target table, which potentially need to be updated.
    # In combination with the following filter, it executes a non-equi join.
    # Essentially, we just want to find the rows in the target table which "surround" the row in the source table by the valid_from column.
    target_records_to_be_updated = (
        target_df.join(
            source_df,
            on=primary_key_columns,
            how="left",
            suffix="__source",
        )
    )

    target_records_to_be_updated = (
        target_records_to_be_updated
        .filter(
            (pl.col(valid_from_column) > pl.col(valid_from_column + "__source"))
            | 
            (
                (pl.col(valid_from_column + "__source") > pl.col(valid_from_column))
                & (
                    (pl.col(valid_from_column + "__source") <= pl.col(valid_to_column))
                    | pl.col(valid_to_column).is_null()
                )
            )
        )
    )

    # The above join can produce duplicates, if a target row surrounds multiple source rows, so they are removed.
    target_records_to_be_updated = target_records_to_be_updated.unique(
        subset=primary_key_columns + [valid_from_column]
    )

    # Remove columns from the source df.
    target_records_to_be_updated = (
        target_records_to_be_updated
        .select(target_columns)
    )


    upsert_df: PolarsFrame = pl.concat([target_records_to_be_updated, source_df])

    # Calculate the valid to column.
    # We do this for both the source and target rows, because target rows may need to be updated.
    upsert_df = upsert_df.with_columns(
        pl.col(valid_from_column)
        .shift(-1)
        .over(partition_by=primary_key_columns, order_by=valid_from_column)
        .alias(valid_to_column)
    )

    return upsert_df