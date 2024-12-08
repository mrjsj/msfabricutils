import polars as pl
from polars.exceptions import ColumnNotFoundError

from msfabricutils.etl import Config
from msfabricutils.etl.types import PolarsFrame


def add_audit_columns_transform(df: PolarsFrame, config: Config) -> PolarsFrame:
    """
    Adds audit columns to the given DataFrame or LazyFrame based on the configuration.

    Args:
        df (PolarsFrame): The DataFrame or LazyFrame to which audit columns will be added.
        config (Config): The configuration object that provides the audit column definitions.

    Returns:
        The DataFrame or LazyFrame with the added audit columns.

    Example:
        ```python
        from msfabricutils.etl import get_default_config, add_audit_columns_transform
        import polars as pl


        config = get_default_config()
        df = pl.DataFrame({"data": [1, 2, 3]})
        updated_df = add_audit_columns_transform(df, config)

        ```
    """

    audit_columns = config.get_audit_columns()

    df = df.with_columns(
        [audit_column.default_value.alias(audit_column.name) for audit_column in audit_columns]
    )
    return df


def deduplicate_transform(
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
        deduped_df = deduplicate_transform(df, primary_key_columns=["id"])
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


def normalize_column_names_transform(df: PolarsFrame, config: Config) -> PolarsFrame:
    """
    Normalizes the column names of the DataFrame using a provided normalization strategy.

    Args:
        df (PolarsFrame): The DataFrame or LazyFrame whose column names will be normalized.
        config (Config): The configuration object that provides the normalization strategy.

    Returns:
        PolarsFrame: The DataFrame or LazyFrame with normalized column names.

    Example:
        ```python
        import polars as pl
        from msfabricutils.etl import get_default_config

        config = get_default_config()

        df = pl.DataFrame({"First Name": [1, 2], "Last Name": [3, 4]})
        normalized_df = normalize_column_names_transform(df, config)
        ```
    """

    if isinstance(df, pl.LazyFrame):
        columns = df.collect_schema().names()
    else:
        columns = df.schema.names()

    column_mapping = {old_name: config.normalization_strategy(old_name) for old_name in columns}

    df = df.rename(column_mapping)

    return df


# def filter_source(df: PolarsFrame, filter: Callable[[PolarsFrame], PolarsFrame]) -> PolarsFrame:
#     return filter(df)
