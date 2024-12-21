from datetime import datetime, timezone

import polars as pl
import pytest
from freezegun import freeze_time
from polars.exceptions import ColumnNotFoundError
from polars.testing import assert_frame_equal

from msfabricutils.etl import get_default_config
from msfabricutils.etl.transform import (
    add_audit_columns,
    apply_scd_type_2,
    deduplicate,
    normalize_column_names,
    reorder_columns_by_prefix,
    reorder_columns_by_suffix,
)


@freeze_time("2024-12-06 12:00:00")
def test_add_audit_columns():
    config = get_default_config()

    df = pl.DataFrame({"data": [1, 2, 3]})

    audit_columns = config.get_audit_columns()

    actual_df = add_audit_columns(df, audit_columns)

    datetime_now = datetime(2024, 12, 6, 12, 0, tzinfo=timezone.utc)

    expected_df = pl.DataFrame(
        {
            "data": [1, 2, 3],
            "__created_at": [datetime_now, datetime_now, datetime_now],
            "__modified_at": [datetime_now, datetime_now, datetime_now],
            "__deleted_at": [None, None, None],
            "__valid_from": [datetime_now, datetime_now, datetime_now],
            "__valid_to": [None, None, None],
        },
        schema_overrides={
            "__deleted_at": pl.Datetime(time_zone="UTC"),
            "__valid_to": pl.Datetime(time_zone="UTC"),
        },
    )

    assert_frame_equal(actual_df, expected_df)

def test_reorder_columns_by_suffix():
    # Test case with alphabetical sorting within groups
    df = pl.DataFrame({
        "name_key": ["a", "b"],
        "age_key": [1, 2],
        "name_value": ["x", "y"],
        "age_value": [10, 20],
        "other": [True, False]
    })

    actual_df = reorder_columns_by_suffix(df, suffix_order=["_key", "_value"])

    expected_df = pl.DataFrame({
        "age_key": [1, 2],
        "name_key": ["a", "b"],
        "age_value": [10, 20],
        "name_value": ["x", "y"],
        "other": [True, False]
    })

    assert_frame_equal(actual_df, expected_df)

def test_reorder_columns_by_suffix_no_sorting():
    # Test case without alphabetical sorting within groups
    df = pl.DataFrame({
        "name_key": ["a", "b"],
        "age_key": [1, 2],
        "name_value": ["x", "y"],
        "age_value": [10, 20],
        "other": [True, False]
    })

    actual_df = reorder_columns_by_suffix(
        df, 
        suffix_order=["_key", "_value"], 
        sort_alphabetically_within_group=False
    )

    # Columns should maintain their original order within groups
    expected_df = pl.DataFrame({
        "name_key": ["a", "b"],
        "age_key": [1, 2],
        "name_value": ["x", "y"],
        "age_value": [10, 20],
        "other": [True, False]
    })

    assert_frame_equal(actual_df, expected_df)

def test_reorder_columns_by_prefix():
    # Test case with alphabetical sorting within groups
    df = pl.DataFrame({
        "dim_name": ["a", "b"],
        "dim_age": [1, 2],
        "fact_sales": [100, 200],
        "fact_quantity": [5, 10],
        "other": [True, False]
    })

    actual_df = reorder_columns_by_prefix(df, prefix_order=["dim_", "fact_"])

    expected_df = pl.DataFrame({
        "dim_age": [1, 2],
        "dim_name": ["a", "b"],
        "fact_quantity": [5, 10],
        "fact_sales": [100, 200],
        "other": [True, False]
    })

    assert_frame_equal(actual_df, expected_df)

def test_reorder_columns_by_prefix_no_sorting():
    # Test case without alphabetical sorting within groups
    df = pl.DataFrame({
        "dim_name": ["a", "b"],
        "dim_age": [1, 2],
        "fact_sales": [100, 200],
        "fact_quantity": [5, 10],
        "other": [True, False]
    })

    actual_df = reorder_columns_by_prefix(
        df, 
        prefix_order=["dim_", "fact_"], 
        sort_alphabetically_within_group=False
    )

    # Columns should maintain their original order within groups
    expected_df = pl.DataFrame({
        "dim_name": ["a", "b"],
        "dim_age": [1, 2],
        "fact_sales": [100, 200],
        "fact_quantity": [5, 10],
        "other": [True, False]
    })

    assert_frame_equal(actual_df, expected_df)

def test_deduplicate_single_key():
    df = pl.DataFrame({
        "id": [1, 2, 2, 3],
        "value": ["a", "b1", "b2", "c"],
        "timestamp": [1, 2, 3, 4]
    })

    actual_df = deduplicate(
        df,
        primary_key_columns="id",
        deduplication_order_columns="timestamp",
        deduplication_order_descending=True
    )

    expected_df = pl.DataFrame({
        "id": [1, 2, 3],
        "value": ["a", "b2", "c"],
        "timestamp": [1, 3, 4]
    })

    assert_frame_equal(actual_df, expected_df, check_row_order=False)

def test_deduplicate_multiple_keys():
    df = pl.DataFrame({
        "id": [1, 1, 2, 2],
        "type": ["A", "A", "B", "B"],
        "value": ["old", "new", "old", "new"],
        "timestamp": [1, 2, 3, 4]
    })

    actual_df = deduplicate(
        df,
        primary_key_columns=["id", "type"],
        deduplication_order_columns="timestamp",
        deduplication_order_descending=True
    )

    expected_df = pl.DataFrame({
        "id": [1, 2],
        "type": ["A", "B"],
        "value": ["new", "new"],
        "timestamp": [2, 4]
    })

    assert_frame_equal(actual_df, expected_df, check_row_order=False)

def test_deduplicate_no_duplicates():
    df = pl.DataFrame({
        "id": [1, 2, 3],
        "value": ["a", "b", "c"]
    })

    actual_df = deduplicate(df, primary_key_columns="id")
    assert_frame_equal(actual_df, df, check_row_order=False)

def test_deduplicate_invalid_column():
    df = pl.DataFrame({
        "id": [1, 2, 3],
        "value": ["a", "b", "c"]
    })

    with pytest.raises(ColumnNotFoundError):
        deduplicate(df, primary_key_columns="non_existent")

def test_normalize_column_names():
    df = pl.DataFrame({
        "First Name": ["John", "Jane"],
        "Last Name": ["Doe", "Smith"],
        "AGE": [30, 25],
        "phone_number": [123, 456]
    })

    def normalize_strategy(col: str) -> str:
        return col.lower().replace(" ", "_")

    actual_df = normalize_column_names(df, normalize_strategy)

    expected_df = pl.DataFrame({
        "first_name": ["John", "Jane"],
        "last_name": ["Doe", "Smith"],
        "age": [30, 25],
        "phone_number": [123, 456]
    })

    assert_frame_equal(actual_df, expected_df, check_row_order=False)

def test_normalize_column_names_custom_strategy():
    df = pl.DataFrame({
        "First Name": ["John", "Jane"],
        "Last-Name": ["Doe", "Smith"]
    })

    def custom_strategy(col: str) -> str:
        return col.upper().replace(" ", "_").replace("-", "_")

    actual_df = normalize_column_names(df, custom_strategy)

    expected_df = pl.DataFrame({
        "FIRST_NAME": ["John", "Jane"],
        "LAST_NAME": ["Doe", "Smith"]
    })

    assert_frame_equal(actual_df, expected_df, check_row_order=False)

def test_normalize_column_names_empty_df():
    df = pl.DataFrame({
        "First Name": [],
        "Last Name": []
    })

    def normalize_strategy(col: str) -> str:
        return col.lower().replace(" ", "_")

    actual_df = normalize_column_names(df, normalize_strategy)

    expected_df = pl.DataFrame({
        "first_name": [],
        "last_name": []
    })

    assert_frame_equal(actual_df, expected_df, check_row_order=False)


def test_apply_scd_type_2_old_records():
    # Arrange
    # Create source dataframe with new and updated records
    source_df = pl.DataFrame(
        {
            "id": [1, 3],
            "name": ["Alice", "Charlie"],
            "valid_from": [
                datetime(2023, 1, 1, tzinfo=timezone.utc),
                datetime(2023, 1, 1, tzinfo=timezone.utc),
            ],
            "valid_to": [None, None],
        },
        schema={
            "id": pl.Int64,
            "name": pl.Utf8,
            "valid_from": pl.Datetime(time_zone="UTC"),
            "valid_to": pl.Datetime(time_zone="UTC"),
        },
    )

    # Create target dataframe with existing records
    target_df = pl.DataFrame(
        {
            "id": [1, 2],
            "name": ["Alice Updated", "Bob"],
            "valid_from": [
                datetime(2024, 1, 1, tzinfo=timezone.utc),
                datetime(2024, 1, 1, tzinfo=timezone.utc),
            ],
            "valid_to": [None, None],
        },
        schema={
            "id": pl.Int64,
            "name": pl.Utf8,
            "valid_from": pl.Datetime(time_zone="UTC"),
            "valid_to": pl.Datetime(time_zone="UTC"),
        },        
    )

    # Act
    result_df = apply_scd_type_2(
        source_df=source_df,
        target_df=target_df,
        primary_key_columns="id",
        valid_from_column="valid_from",
        valid_to_column="valid_to",
    )

    # Assert
    expected_df = pl.DataFrame(
        {
            "id": [1, 1, 3],
            "name": ["Alice", "Alice Updated", "Charlie"],
            "valid_from": [
                datetime(2023, 1, 1, tzinfo=timezone.utc),
                datetime(2024, 1, 1, tzinfo=timezone.utc),
                datetime(2023, 1, 1, tzinfo=timezone.utc),
            ],
            "valid_to": [
                datetime(2024, 1, 1, tzinfo=timezone.utc),
                None,
                None,
            ],
        }
    )

    assert_frame_equal(result_df, expected_df, check_row_order=False)


def test_apply_scd_type_2_new_records():
    # Arrange
    # Create source dataframe with new and updated records
    source_df = pl.DataFrame(
        {
            "id": [1, 2],
            "name": ["Alice Updated", "Bob"],
            "valid_from": [
                datetime(2024, 1, 1, tzinfo=timezone.utc),
                datetime(2024, 1, 1, tzinfo=timezone.utc),
            ],
            "valid_to": [None, None],
        }
    )

    # Create target dataframe with existing records
    target_df = pl.DataFrame(
        {
            "id": [1, 3],
            "name": ["Alice", "Charlie"],
            "valid_from": [
                datetime(2023, 1, 1, tzinfo=timezone.utc),
                datetime(2023, 1, 1, tzinfo=timezone.utc),
            ],
            "valid_to": [None, None],
        },
        schema={
            "id": pl.Int64,
            "name": pl.Utf8,
            "valid_from": pl.Datetime(time_zone="UTC"),
            "valid_to": pl.Datetime(time_zone="UTC"),
        },
    )

    # Act
    result_df = apply_scd_type_2(
        source_df=source_df,
        target_df=target_df,
        primary_key_columns="id",
        valid_from_column="valid_from",
        valid_to_column="valid_to",
    )

    # Assert
    expected_df = pl.DataFrame(
        {
            "id": [1, 1, 2],
            "name": ["Alice", "Alice Updated", "Bob"],
            "valid_from": [
                datetime(2023, 1, 1, tzinfo=timezone.utc),
                datetime(2024, 1, 1, tzinfo=timezone.utc),
                datetime(2024, 1, 1, tzinfo=timezone.utc),
            ],
            "valid_to": [
                datetime(2024, 1, 1, tzinfo=timezone.utc),
                None,
                None,
            ],
        }
    )

    assert_frame_equal(result_df, expected_df, check_row_order=False)


def test_apply_scd_type_2_empty_target():
    # Arrange
    schema = {
        "id": pl.Int64,
        "name": pl.Utf8,
        "valid_from": pl.Datetime(time_zone="UTC"),
        "valid_to": pl.Datetime(time_zone="UTC"),
    }

    source_df = pl.DataFrame(
        {
            "id": [1],
            "name": ["Alice"],
            "valid_from": [datetime(2024, 1, 1, tzinfo=timezone.utc)],
            "valid_to": [None],
        },
        schema=schema,
    )

    target_df = pl.DataFrame(
        {"id": [], "name": [], "valid_from": [], "valid_to": []}, schema=schema
    )

    # Act
    result_df = apply_scd_type_2(
        source_df=source_df,
        target_df=target_df,
        primary_key_columns="id",
        valid_from_column="valid_from",
        valid_to_column="valid_to",
    )

    # Assert
    expected_df = source_df

    assert_frame_equal(result_df, expected_df, check_row_order=False)


def test_apply_scd_type_2_multiple_primary_keys():
    # Arrange
    source_df = pl.DataFrame(
        {
            "customer_id": [1, 1],
            "product_id": [100, 101],
            "quantity": [5, 10],
            "valid_from": [
                datetime(2024, 1, 1, tzinfo=timezone.utc),
                datetime(2024, 1, 1, tzinfo=timezone.utc),
            ],
            "valid_to": [None, None],
        }
    )

    target_df = pl.DataFrame(
        {
            "customer_id": [1],
            "product_id": [100],
            "quantity": [3],
            "valid_from": [datetime(2023, 1, 1, tzinfo=timezone.utc)],
            "valid_to": [None],
        }
    )

    # Act
    result_df = apply_scd_type_2(
        source_df=source_df,
        target_df=target_df,
        primary_key_columns=["customer_id", "product_id"],
        valid_from_column="valid_from",
        valid_to_column="valid_to",
    )

    # Assert
    expected_df = pl.DataFrame(
        {
            "customer_id": [1, 1, 1],
            "product_id": [100, 100, 101],
            "quantity": [3, 5, 10],
            "valid_from": [
                datetime(2023, 1, 1, tzinfo=timezone.utc),
                datetime(2024, 1, 1, tzinfo=timezone.utc),
                datetime(2024, 1, 1, tzinfo=timezone.utc),
            ],
            "valid_to": [datetime(2024, 1, 1, tzinfo=timezone.utc), None, None],
        }
    )

    assert_frame_equal(result_df, expected_df, check_row_order=False)


def test_apply_scd_type_2_target_records_gets_updated():
    # Arrange
    schema = {
        "id": pl.Int64,
        "name": pl.Utf8,
        "valid_from": pl.Datetime(time_zone="UTC"),
        "valid_to": pl.Datetime(time_zone="UTC"),
    }

    source_df = pl.DataFrame(
        {
            "id": [1, 1, 1, 1],
            "name": ["Alice 3", "Alice 1", "Alice 5", "Alice 6"],
            "valid_from": [
                datetime(2024, 1, 1, tzinfo=timezone.utc),
                datetime(2023, 1, 1, tzinfo=timezone.utc),
                datetime(2025, 1, 1, tzinfo=timezone.utc),
                datetime(2026, 1, 1, tzinfo=timezone.utc),
            ],
            "valid_to": [None, None, None, None],
        },
        schema=schema,
    )

    target_df = pl.DataFrame(
        {
            "id": [1, 1],
            "name": ["Alice 4", "Alice 2"],
            "valid_from": [
                datetime(2024, 6, 1, tzinfo=timezone.utc),
                datetime(2023, 6, 1, tzinfo=timezone.utc),
            ],
            "valid_to": [None, datetime(2024, 6, 1, tzinfo=timezone.utc)],
        },
        schema=schema,
    )

    # Act
    result_df = apply_scd_type_2(
        source_df=source_df,
        target_df=target_df,
        primary_key_columns="id",
        valid_from_column="valid_from",
        valid_to_column="valid_to",
    )

    # Assert
    expected_df = pl.DataFrame(
        {
            "id": [1, 1, 1, 1, 1, 1],
            "name": ["Alice 1", "Alice 2", "Alice 3", "Alice 4", "Alice 5", "Alice 6"],
            "valid_from": [
                datetime(2023, 1, 1, tzinfo=timezone.utc),
                datetime(2023, 6, 1, tzinfo=timezone.utc),
                datetime(2024, 1, 1, tzinfo=timezone.utc),
                datetime(2024, 6, 1, tzinfo=timezone.utc),
                datetime(2025, 1, 1, tzinfo=timezone.utc),
                datetime(2026, 1, 1, tzinfo=timezone.utc),
            ],
            "valid_to": [
                datetime(2023, 6, 1, tzinfo=timezone.utc),
                datetime(2024, 1, 1, tzinfo=timezone.utc),
                datetime(2024, 6, 1, tzinfo=timezone.utc),
                datetime(2025, 1, 1, tzinfo=timezone.utc),
                datetime(2026, 1, 1, tzinfo=timezone.utc),
                None,
            ],
        }
    )

    assert_frame_equal(result_df, expected_df, check_row_order=False)
