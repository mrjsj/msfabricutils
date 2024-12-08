from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

import polars as pl

from msfabricutils.common import character_translation, to_snake_case


@dataclass
class IncrementalColumn:
    """
    Represents an incremental column in the configuration.

    Attributes:
        name (str): The name of the incremental column.
        data_type (pl.DataType): The data type of the incremental column.

    Example:
        ```python
        incremental_column = IncrementalColumn("batch_id", pl.Int64)
        ```
    """

    name: str
    data_type: pl.DataType


@dataclass
class AuditColumn:
    """
    Represents an audit column in the configuration.

    Attributes:
        name (str): The name of the audit column.
        default_value (pl.Expr): The default value expression for the audit column.

    Example:
        ```python
        audit_column = AuditColumn(
            "__created_at",
            pl.lit(datetime.now(timezone.utc)).cast(pl.Datetime("us", "UTC"))
        )
        ```
    """

    name: str
    default_value: pl.Expr


@dataclass()
class Config:
    """
    Configuration class that holds various columns and their properties.

    Attributes:
        incremental_column (IncrementalColumn): The incremental column configuration.
        column_created_at (AuditColumn): The created at audit column configuration.
        column_modified_at (AuditColumn): The modified at audit column configuration.
        column_deleted_at (AuditColumns): The deleted at audit column configuration.
        column_valid_from (AuditColumn): The valid from audit column configuration.
        column_valid_to (AuditColumn): The valid to audit column configuration.
        character_translation_map (dict[str, str]): A mapping of special characters to their translations.
        normalization_strategy (Callable[[str], str]): A function that takes a column name and returns the normalized name.
    """

    incremental_column: IncrementalColumn
    column_created_at: AuditColumn
    column_modified_at: AuditColumn
    column_deleted_at: AuditColumn
    column_valid_from: AuditColumn
    column_valid_to: AuditColumn
    character_translation_map: dict[str, str]
    normalization_strategy: Callable[[str], str]

    def __init__(self):
        # TODO: Change to `__run_id`
        self.incremental_column = IncrementalColumn("batch_id", pl.Int64)
        self.column_created_at = AuditColumn(
            "__created_at", pl.lit(datetime.now(timezone.utc)).cast(pl.Datetime("us", "UTC"))
        )
        self.column_modified_at = AuditColumn(
            "__modified_at", pl.lit(datetime.now(timezone.utc)).cast(pl.Datetime("us", "UTC"))
        )
        self.column_deleted_at = AuditColumn(
            "__deleted_at", pl.lit(None).cast(pl.Datetime("us", "UTC"))
        )
        self.column_valid_from = AuditColumn(
            "__valid_from", pl.lit(datetime.now(timezone.utc)).cast(pl.Datetime("us", "UTC"))
        )
        self.column_valid_to = AuditColumn(
            "__valid_to", pl.lit(None).cast(pl.Datetime("us", "UTC"))
        )
        self.character_translation_map = {
            " ": "_",
            "-": "_",
            "'": "_",
            '"': "_",
            "(": "_",
            ")": "_",
            ",": "_",
            ".": "_",
            ":": "_",
            ";": "_",
            "!": "_",
            "?": "_",
            "|": "_or",
            "[": "_",
            "]": "_",
            "{": "_",
            "}": "_",
            "&": "_and",
            "/": "_or",
            "\\": "_or",
            "%": "_percent",
            "+": "_plus",
            "*": "_times",
            "=": "_equals",
            "<": "_lt",
            ">": "_gt",
            "@": "_at",
            "$": "_dollar",
            "~": "_approximate",
        }
        self.normalization_strategy = lambda name: to_snake_case(
            character_translation(name, self.character_translation_map)
        )

    def get_static_audit_columns(self) -> list[AuditColumn]:
        """
        Returns a list of static audit columns, namely the `created_at` and `valid_from` columns.

        Returns:
            A list containing the static audit columns.

        Example:
            ```python
            static_columns = config.get_static_audit_columns()
            ```
        """
        return [
            self.column_created_at,
            self.column_valid_from,
        ]

    def get_dynamic_audit_columns(self) -> list[AuditColumn]:
        """
        Returns a list of dynamic audit columns, namely the `modified_at` and `valid_to` columns.

        Returns:
            A list containing the dynamic audit columns.

        Example:
            ```python
            dynamic_columns = config.get_dynamic_audit_columns()
            ```
        """
        return [
            self.column_modified_at,
            self.column_valid_to,
            self.column_deleted_at,
        ]

    def get_audit_columns(self) -> list[AuditColumn]:
        """
        Returns a list of all audit columns, namely the `created_at`, `modified_at`, `valid_from`, and `valid_to` columns.

        Returns:
            A list containing all audit columns.

        Example:
            ```python
            all_columns = config.get_audit_columns()
            ```
        """
        return [
            self.column_created_at,
            self.column_modified_at,
            self.column_deleted_at,
            self.column_valid_from,
            self.column_valid_to,
        ]


def create_config(
    incremental_column: IncrementalColumn,
    created_at: AuditColumn,
    modified_at: AuditColumn,
    deleted_at: AuditColumn,
    valid_from: AuditColumn,
    valid_to: AuditColumn,
) -> Config:
    """
    Creates a new Config instance with the provided audit and incremental columns.

    Args:
        incremental_column (IncrementalColumn): The incremental column.
        created_at (AuditColumn): The created at audit column.
        modified_at (AuditColumn): The modified at audit column.
        deleted_at (AuditColumn): The deleted at audit column.
        valid_from (AuditColumn): The valid from audit column.
        valid_to (AuditColumn): The valid to audit column.

    Returns:
        A new instance of the Config class.

    Example:
        ```python
        incremental_column = IncrementalColumn("batch_id", pl.Int64)
        ...
        valid_to = AuditColumn("__valid_to", pl.lit(datetime.now(timezone.utc)).cast(pl.Datetime("us", "UTC")))
        config = create_config(
            incremental_column,
            created_at,
            modified_at,
            deleted_at,
            valid_from,
            valid_to,
        )
        ```
    """
    return Config(
        incremental_column,
        created_at,
        modified_at,
        deleted_at,
        valid_from,
        valid_to,
    )


def get_default_config() -> Config:
    """
    Returns a default Config instance with preset values.

    Returns:
        A default instance of the Config class.

    Example:
        ```python
        default_config = get_default_config()
        ```
    """
    return Config()
