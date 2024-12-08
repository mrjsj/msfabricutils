
from datetime import datetime, timezone

import polars as pl
from freezegun import freeze_time
from polars.testing import assert_frame_equal

from msfabricutils.etl import get_default_config
from msfabricutils.etl.transforms.transforms import add_audit_columns_transform


@freeze_time("2024-12-06 12:00:00")
def test_add_audit_columns():
    config = get_default_config()
    
    df = pl.DataFrame(
        {
            "data": [1, 2, 3]
        }
    )

    actual_df = add_audit_columns_transform(df, config)

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
            "__valid_to": pl.Datetime(time_zone="UTC")
        }
    )

    assert_frame_equal(actual_df, expected_df)
