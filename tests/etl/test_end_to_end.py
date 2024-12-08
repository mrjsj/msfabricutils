from datetime import datetime, timezone

import polars as pl
from freezegun import freeze_time
from polars.testing import assert_frame_equal

from msfabricutils.etl import (
    add_audit_columns_transform,
    deduplicate_transform,
    get_default_config,
    get_incremental_column_value,
    normalize_column_names_transform,
    source_delta,
    upsert_scd_type_1,
)


@freeze_time("2024-01-01")
def test_end_to_end(tmp_path):

    source_table_path = str(tmp_path / "source_table")
    target_table_path = str(tmp_path / "target_table")

    # Create a source table
    source_df = pl.DataFrame({
        "ID": [1, 2, 3, 1, 2],
        "FirstName": ["Alice", "Bob", "Charlie", "AliceS", "BobB"],
        "batch_id": [1, 1, 1, 2, 2]
    })
    source_df.write_delta(source_table_path)

    # Get the default config
    config = get_default_config()

    # Read the source delta table
    source_df = source_delta(source_table_path)

    # Get the incremental column value
    incremental_column_value = get_incremental_column_value(target_table_path, "batch_id")

    # Filter the source dataframe to only get the rows with a modified_at greater than the incremental column value
    filtered_df = source_df.filter(pl.col("batch_id") > incremental_column_value)

    # Deduplicate the source dataframe
    deduped_df = deduplicate_transform(filtered_df, primary_key_columns="ID", deduplication_order_columns="batch_id")

    # Normalize the column names
    normalized_df = normalize_column_names_transform(deduped_df, config)

    # Add audit columns
    audit_df = add_audit_columns_transform(normalized_df, config)

    # Upsert to a target table
    upsert_scd_type_1(target_table_path, audit_df, primary_key_columns="ID", config=config)

    # Read the target table
    target_df = pl.read_delta(target_table_path)

    # Test that the target table is as expected
    datetime_now = datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc)

    expected_df = pl.DataFrame(
        {
            "id": [3, 1, 2],
            "first_name": ["Charlie", "AliceS", "BobB"],
            "batch_id": [1, 2, 2],
            "__created_at": [datetime_now, datetime_now, datetime_now],
            "__modified_at": [datetime_now, datetime_now, datetime_now],
            "__deleted_at": [None, None, None],
            "__valid_from": [datetime_now, datetime_now, datetime_now],
            "__valid_to": [None, None, None],
        },
        schema_overrides={
            "__created_at": pl.Datetime(time_zone="UTC"),
            "__modified_at": pl.Datetime(time_zone="UTC"),
            "__deleted_at": pl.Datetime(time_zone="UTC"),
            "__valid_to": pl.Datetime(time_zone="UTC"),
            "__valid_from": pl.Datetime(time_zone="UTC"),
        }
    )  

    print(target_df)
    
    assert_frame_equal(target_df, expected_df, check_row_order=False)
