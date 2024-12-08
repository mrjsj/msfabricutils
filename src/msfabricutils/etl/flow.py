import re
from functools import partial, reduce
from typing import Callable, Literal

import polars as pl

from msfabricutils.common.string_normalization import character_translation, to_snake_case
from msfabricutils.etl import get_default_config
from msfabricutils.etl.config import Config
from msfabricutils.etl.helpers import get_incremental_column_value
from msfabricutils.etl.sinks.delta_table import upsert_scd_type_1
from msfabricutils.etl.sources import source_delta, source_parquet
from msfabricutils.etl.transforms.transforms import (
    add_audit_columns_transform,
    deduplicate_transform,
    normalize_column_names_transform,
)
from msfabricutils.etl.types import PolarsFrame


class Flow:
    """
    A class to manage ETL (Extract, Transform, Load) processes.

    This class allows users to define sources, transformations, and sinks
    for data processing workflows.

    Example:
        ```python
        flow = Flow()
        flow.add_default_config()
        flow.add_source_delta_table("path/to/delta", "source_alias")
        ```
    """

    def __init__(self):
        """
        Initializes a new Flow instance with default attributes.
        """
        self.config: Config = None
        self._sources: dict[str, tuple[Callable[[], PolarsFrame], str | None]] = {}
        self._transforms: list[Callable[[dict[str, PolarsFrame] | PolarsFrame], PolarsFrame]] = []
        self._post_transforms: list[Callable[[PolarsFrame], PolarsFrame]] = []
        self._target_file_or_table_uri: str | None = None
        self._incremental_value: Callable[[], int] | None = None
        self._sink: Callable[[PolarsFrame], None] | None = None

    def add_default_config(self) -> "Flow":
        """
        Adds the default configuration to the Flow instance.

        Returns:
            Flow: The current Flow instance with the default configuration added.

        Example:
            ```python
            flow = Flow().add_default_config()
            ```
        """
        self.config = get_default_config()
        return self

    def add_config_custom(self, config: Config) -> "Flow":
        """
        Adds a custom configuration to the Flow instance.

        Args:
            config (Config): A custom configuration object.

        Returns:
            Flow: The current Flow instance with the custom configuration added.

        Example:
            ```python
            custom_config = Config()
            flow = Flow().add_config_custom(custom_config)
            ```
        """
        self.config = config
        return self

    def add_source_delta_table(
        self, table_uri: str, source_alias: str, is_incremental: bool = True
    ) -> "Flow":
        """
        Adds a Delta table source to the Flow instance.

        Args:
            table_uri (str): The URI of the Delta table.
            source_alias (str): An alias for the source.
            is_incremental (bool, optional): Whether the source is incremental. Defaults to True.

        Returns:
            Flow: The current Flow instance with the Delta table source added.

        Example:
            ```python
            flow = Flow().add_source_delta_table("path/to/delta", "source_alias")
            ```
        """
        self._sources[source_alias] = (lambda: source_delta(table_uri), is_incremental)
        return self

    def add_source_parquet(
        self, table_uri: str, source_alias: str, is_incremental: bool = True
    ) -> "Flow":
        """
        Adds a Parquet source to the Flow instance.

        Args:
            table_uri (str): The URI of the Parquet file.
            source_alias (str): An alias for the source.
            is_incremental (bool, optional): Whether the source is incremental. Defaults to True.

        Returns:
            Flow: The current Flow instance with the Parquet source added.

        Example:
            ```python
            flow = Flow().add_source_parquet("path/to/file.parquet", "source_alias")
            ```
        """
        self._sources[source_alias] = (lambda: source_parquet(table_uri), is_incremental)
        return self

    def add_source_custom(
        self,
        source: Callable[[], PolarsFrame],
        source_alias: str,
        is_incremental: bool = True,
        *args,
        **kwargs,
    ) -> "Flow":
        """
        Adds a custom source to the Flow instance.

        Args:
            source (Callable[[], PolarsFrame]): A callable that returns a PolarsFrame.
            source_alias (str): An alias for the source.
            is_incremental (bool, optional): Whether the source is incremental. Defaults to True.
            *args: Additional positional arguments for the source.
            **kwargs: Additional keyword arguments for the source.

        Returns:
            Flow: The current Flow instance with the custom source added.

        Example:
            ```python
            flow = Flow().add_source_custom(my_custom_source, "custom_source_alias")
            ```
        """
        self._sources[source_alias] = (partial(source, *args, **kwargs), is_incremental)
        return self

    def add_transform_custom(
        self,
        transform: Callable[[dict[str, PolarsFrame] | PolarsFrame], PolarsFrame],
        *args,
        **kwargs,
    ) -> "Flow":
        """
        Adds a custom transformation to the Flow instance.

        Args:
            transform (Callable[[dict[str, PolarsFrame] | PolarsFrame], PolarsFrame]):
                A callable that performs a transformation on the data.
            *args: Additional positional arguments for the transform.
            **kwargs: Additional keyword arguments for the transform.

        Returns:
            Flow: The current Flow instance with the custom transformation added.

        Example:
            ```python
            flow = Flow().add_transform_custom(my_transform_function)
            ```
        """
        self._transforms.append(partial(transform, *args, **kwargs))
        return self

    def add_post_transform_audit_columns(self) -> "Flow":
        """
        Adds a post-transform to include audit columns.

        Returns:
            Flow: The current Flow instance with the audit columns post-transform added.

        Example:
            ```python
            flow = Flow().add_post_transform_audit_columns()
            ```
        """
        self._post_transforms.append(partial(add_audit_columns_transform, config=self.config))
        return self

    def add_post_transform_normalize_column_names(self) -> "Flow":
        """
        Adds a post-transform to normalize column names.

        Args:
            normalization_strategy (Callable[[str], str] | None): A callable for normalization.

        Returns:
            Flow: The current Flow instance with the normalize column names post-transform added.

        Example:
            ```python
            flow = Flow().add_post_transform_normalize_column_names()
            ```
        """

        self._post_transforms.append(partial(normalize_column_names_transform, config=self.config))
        return self

    def add_post_transform_deduplicate(
        self,
        primary_key_columns: str | list[str] = None,
        deduplication_order_columns: str | list[str] = None,
        deduplication_order_descending: bool | list[bool] = True,
    ) -> "Flow":
        """
        Adds a post-transform to deduplicate records.

        Args:
            primary_key_columns (str | list[str]): The primary key columns for deduplication.
            deduplication_order_columns (str | list[str]): The order columns for deduplication.
            deduplication_order_descending (bool | list[bool]): Whether to order descending.

        Returns:
            Flow: The current Flow instance with the deduplication post-transform added.

        Example:
            ```python
            flow = Flow().add_post_transform_deduplicate(primary_key_columns=['id'])
            ```
        """
        self._post_transforms.append(
            partial(
                deduplicate_transform,
                primary_key_columns=primary_key_columns,
                deduplication_order_columns=deduplication_order_columns,
                deduplication_order_descending=deduplication_order_descending,
            )
        )
        return self

    def add_default_post_transforms(self) -> "Flow":
        """
        Adds default post-transforms to the Flow instance.

        This includes deduplication, normalization of column names, and adding audit columns.

        Returns:
            Flow: The current Flow instance with default post-transforms added.

        Example:
            ```python
            flow = Flow().add_default_post_transforms()
            ```
        """
        self.add_post_transform_deduplicate()
        self.add_post_transform_normalize_column_names()
        self.add_post_transform_audit_columns()
        return self

    def add_sink_upsert_scd_type_1(
        self,
        table_uri: str,
        primary_key_columns: str | list[str] = None,
        incremental_column: str | None = None,
        except_columns: str | list[str] = None,
    ) -> "Flow":
        """
        Adds a sink for upserting SCD Type 1 records.

        Args:
            table_uri (str): The URI of the target table.
            primary_key_columns (str | list[str]): The primary key columns for the target table.
            incremental_column (str | None): The incremental column for the target table.
            except_columns (str | list[str] | None): Columns to exclude from the upsert.

        Returns:
            Flow: The current Flow instance with the SCD Type 1 sink added.

        Example:
            ```python
            flow = Flow().add_sink_upsert_scd_type_1("target_table_uri", primary_key_columns=["id"])
            ```
        """
        self._target_file_or_table_uri = table_uri
        self.target_table_incremental_column = incremental_column
        self._sink = partial(
            upsert_scd_type_1,
            table_uri=table_uri,
            config=self.config,
            primary_key_columns=primary_key_columns,
            except_columns=except_columns,
        )
        self._incremental_value = lambda: get_incremental_column_value(
            table_uri, incremental_column
        )
        return self

    def add_sink_custom(
        self, sink: Callable[[PolarsFrame], None], file_uri: str | None = None, *args, **kwargs
    ) -> "Flow":
        """
        Adds a custom sink to the Flow instance.

        Args:
            sink (Callable[[PolarsFrame], None]): A callable that defines the sink operation.
            file_uri (str | None): The URI of the file for the sink.
            *args: Additional positional arguments for the sink.
            **kwargs: Additional keyword arguments for the sink.

        Returns:
            Flow: The current Flow instance with the custom sink added.

        Example:
            ```python
            flow = Flow().add_sink_custom(my_sink_function, "output_file_uri")
            ```
        """
        self._target_file_or_table_uri = file_uri
        self._sink = partial(sink, *args, **kwargs)
        return self

    def run(self) -> None:
        """
        Executes the ETL flow.

        This method validates the flow, applies transformations, and writes the output to the sink.

        Example:
            ```python
            flow.run()
            ```
        """
        self._pre_validate_flow()
        self._filter_sources_for_incremental()

        df = self._do_transforms()
        df = self._do_post_transforms(df)
        self._post_validate_flow(df)

        self._sink(data=df)

    def _pre_validate_flow(self) -> None:
        """
        Validates the flow before execution.

        Raises:
            ValueError: If the configuration, sources, transforms, or sink are not set.

        Example:
            ```python
            flow._pre_validate_flow()  # This will raise an error if validation fails
            ```
        """
        if self.config is None:
            raise ValueError(
                "Config is not set, add a config using `add_config` or `add_default_config`."
            )

        if len(self._sources) == 0:
            raise ValueError(
                "No sources have been added to the flow, add at least one source using `add_source`."
            )

        if len(self._transforms) == 0 and len(self._sources) > 1:
            raise ValueError(
                "Transforms are not set, and there are multiple sources. Add at least one transform using `add_transform` to combine the sources."
            )

        if self._sink is None:
            raise ValueError("Sink is not set, add a sink using `add_sink`.")

    def _post_validate_flow(self, df: PolarsFrame) -> None:
        """
        Validates the flow after execution.

        Args:
            df (PolarsFrame): The resulting dataframe after transformations.

        Raises:
            ValueError: If the incremental column or audit columns are missing.

        Example:
            ```python
            flow._post_validate_flow(df)  # This will raise an error if validation fails
            ```
        """
        if self.config.incremental_column.name not in df.collect_schema().names():
            raise ValueError(
                f"Incremental column `{self.config.incremental_column.name}` is not in the dataframe. Was it dropped in a transform?"
            )

        columns = df.collect_schema().names() if isinstance(df, pl.LazyFrame) else df.schema.names()

        if any(
            audit_column.name not in columns for audit_column in self.config.get_audit_columns()
        ):
            raise ValueError(
                f"At least one audit columns: {', '.join(audit_column.name for audit_column in self.config.get_audit_columns())} is not in the dataframe. Was it dropped in a transform?"
            )

        for column in columns:
            if not bool(re.match(r"^[\w]+$", column)):
                raise ValueError(
                    f"Column names must contain only alphanumeric characters and underscores. Invalid column name: `{column}`"
                )

    def _do_transforms(self) -> PolarsFrame:
        """
        Applies the defined transformations to the sources.

        Returns:
            PolarsFrame: The transformed dataframe.

        Example:
            ```python
            transformed_df = flow._do_transforms()
            ```
        """
        if self._transforms:
            return reduce(lambda df, transform: transform(df), self._transforms, self._sources)
        else:
            return next(iter(self._sources.values()))

    def _do_post_transforms(self, df: PolarsFrame) -> PolarsFrame:
        """
        Applies the defined post-transforms to the dataframe.

        Args:
            df (PolarsFrame): The dataframe to apply post-transforms to.

        Returns:
            PolarsFrame: The dataframe after post-transforms.

        Example:
            ```python
            post_transformed_df = flow._do_post_transforms(df)
            ```
        """
        return reduce(lambda df, post_transform: post_transform(df), self._post_transforms, df)

    def _filter_sources_for_incremental(self) -> None:
        """
        Filters sources based on the incremental value.

        This method updates the sources to only include records that are
        greater than the incremental value.

        Example:
            ```python
            flow._filter_sources_for_incremental()  # This will filter the sources
            ```
        """
        incremental_value = self._incremental_value()
        for source_alias, (source, is_incremental) in self._sources.items():
            if is_incremental:
                self._sources[source_alias] = source().filter(
                    pl.col(self.config.incremental_column.name) > incremental_value
                )
            else:
                self._sources[source_alias] = source()


def get_default_flow() -> Flow:
    """
    Creates a default Flow instance with default configuration and post-transforms.

    Returns:
        Flow: A new Flow instance with default settings.

    Example:
        ```python
        default_flow = get_default_flow()
        ```
    """
    flow = Flow()
    flow.add_default_config()
    flow.add_default_post_transforms()
    return flow


def get_default_landing_to_raw_flow(
    source_file_base_uri: str,
    target_table_uri: str,
    *,
    source_type: Literal["delta", "parquet"] = "parquet",
    source_is_incremental: bool = True,
    target_load_type: Literal["scd_type_1"] = "scd_type_1",
    source_primary_key_columns: list[str] | None = None,
    source_deduplication_order_columns: list[str] | None = None,
    source_deduplication_order_descending: bool | list[bool] = True,
) -> Flow:
    """
    Creates a default flow for landing to raw data processing.

    Args:
        source_file_base_uri (str): The base URI for the source files.
        target_table_uri (str): The URI for the target table.
        source_type (Literal["delta", "parquet"]): The type of source (default is "parquet").
        source_is_incremental (bool): Whether the source is incremental (default is True).
        target_load_type (Literal["scd_type_1"]): The type of load for the target (default is "scd_type_1").
        source_primary_key_columns (list[str] | None): The primary key columns for the source.
        source_deduplication_order_columns (list[str] | None): The order columns for deduplication.
        source_deduplication_order_descending (bool | list[bool]): Whether to order descending.

    Returns:
        Flow: A new Flow instance configured for landing to raw processing.

    Example:
        ```python
        flow = get_default_landing_to_raw_flow("path/to/source", "path/to/target")
        ```
    """
    source_alias = source_type.split("/")[-1]

    if source_primary_key_columns is None and target_load_type.lower() == "scd_type_1":
        raise ValueError("`target_primary_key_columns` must be set for load type `scd_type_1`.")

    flow = Flow()

    flow.add_default_config()
    flow.add_post_transform_deduplicate(
        primary_key_columns=source_primary_key_columns,
        deduplication_order_columns=source_deduplication_order_columns,
        deduplication_order_descending=source_deduplication_order_descending,
    )
    flow.add_post_transform_normalize_column_names()
    flow.add_post_transform_audit_columns()

    match source_type.lower():
        case "delta":
            flow.add_source_delta_table(source_file_base_uri, source_alias, source_is_incremental)
        case "parquet":
            source_file_base_uri = source_file_base_uri.rstrip("/") + "/**/*.parquet"
            flow.add_source_parquet(source_file_base_uri, source_alias, source_is_incremental)
        case _:
            raise ValueError(
                f"Invalid source type: {source_type}. Must be one of: `delta`, `parquet`"
            )

    target_primary_key_columns = [
        to_snake_case(
            character_translation(column, translation_map=flow.config.character_translation_map)
        )
        for column in source_primary_key_columns
    ]

    match target_load_type.lower():
        case "scd_type_1":
            flow.add_sink_upsert_scd_type_1(
                target_table_uri,
                target_primary_key_columns,
                incremental_column=flow.config.incremental_column.name,
            )
        case _:
            raise ValueError(
                f"Invalid target load type: {target_load_type}. Must be one of: `scd_type_1`"
            )

    return flow
