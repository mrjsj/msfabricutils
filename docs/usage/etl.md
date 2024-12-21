# ETL

The ETL module provides a set of helper functions for extracting, transforming, and loading data in a Fabric Lakehouse.



## Basic extract, transform, load

```python
from msfabricutils.etl import (
    read_parquet,
    upsert_scd_type_1
)
import polars as pl

# Create a source parquet file
df = pl.DataFrame({
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"]
})
df.write_parquet("source.parquet")

# Read the source parquet file
source_df = read_parquet("source.parquet")

# Upsert to a target table
upsert(
    table_uri="target_table",
    df=source_df,
    primary_key_columns="id"
)
```



## Advanced example

Consider an example, where

- The source needs to be incrementially loaded
- The source has duplicate rows
- The target table need audit columns, such as created_at, updated_at etc.
- The target table should have normalized column names

The following code will read the delta table, deduplicate the rows, normalize the column names, add audit columns and upsert to the target table.
The result will be a new row for AliceS and BobB in the target table.

```python
from msfabricutils.etl import (
    get_default_config,
    source_delta,
    get_incremental_column_value,
    deduplicate_transform,
    normalize_column_names_transform,
    add_audit_columns_transform,
    upsert_scd_type_1,
)

source_table_path = "source_table"
target_table_path = "target_table"

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
source_df = read_delta(source_table_path)

# Get the incremental column value
incremental_column_value = get_incremental_column_value(target_table_path, "batch_id")

# Filter the source dataframe to only get the rows with a modified_at greater than the incremental column value
filtered_df = source_df.filter(pl.col("batch_id") > incremental_column_value)

# Deduplicate the source dataframe
deduped_df = deduplicate_transform(filtered_df, primary_key_columns="ID", deduplication_order_columns="batch_id")

# Normalize the column names using a normalization strategy
def normalize_column_names(text: str) -> str:
    return text.lower().replace(" ", "_")

normalized_df = normalize_column_names_transform(deduped_df, normalize_column_names)

# Add audit columns
audit_columns = config.get_audit_columns()
audit_df = add_audit_columns_transform(normalized_df, audit_columns)

# Upsert to a target table
static_audit_columns = config.get_static_audit_columns()
upsert(target_table_path, audit_df, primary_key_columns="id", update_exclusion_columns=static_audit_columns)


```

| id  | first_name | batch_id | __created_at            | __modified_at           | __deleted_at      | __valid_from            | __valid_to        |
| --- | ---------- | -------- | -----------------       | -----------------       | ----------------- | ----------------------- | ----------------- |
| i64 | str        | i64      | datetime[μs, UTC]       | datetime[μs, UTC]       | datetime[μs, UTC] | datetime[μs, UTC]       | datetime[μs, UTC] |
| 3   | Charlie    | 1        | 2024-01-01 00:00:00 UTC | 2024-01-01 00:00:00 UTC | null              | 2024-01-01 00:00:00 UTC | null              |
| 2   | BobB       | 2        | 2024-01-01 00:00:00 UTC | 2024-01-01 00:00:00 UTC | null              | 2024-01-01 00:00:00 UTC | null              |
| 1   | AliceS     | 2        | 2024-01-01 00:00:00 UTC | 2024-01-01 00:00:00 UTC | null              | 2024-01-01 00:00:00 UTC | null              |

