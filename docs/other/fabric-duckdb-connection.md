# DuckDB Utilities

## Quick Start
```python
from msfabricutils import FabricDuckDBConnection, get_onelake_access_token

#Initialize connection
access_token = get_onelake_access_token()
conn = FabricDuckDBConnection(access_token=access_token)

# Register lakehouses from different workspaces
conn.register_workspace_lakehouses(
    workspace_id='12345678-1234-5678-1234-567812345678', # Sales workspace
    lakehouses=['sales']
)

conn.register_workspace_lakehouses(
    workspace_id='87654321-8765-4321-8765-432187654321', # Marketing workspace
    lakehouses=['marketing']
)

# Query across workspaces using fully qualified names
df = conn.sql("""
    SELECT
        c.customer_id,
        c.name,
        c.region,
        s.segment,
        s.lifetime_value
    FROM sales_workspace.sales.main.customers c
    JOIN marketing_workspace.marketing.main.customer_segments s
    ON c.customer_id = s.customer_id
    WHERE c.region = 'EMEA'
""").df()
```

## Table Name Formats
The connection wrapper will automatically resolve table names to the fully qualified name, if there is no ambiguity between registed tables.

- 4-part: workspace.lakehouse.schema.table
- 3-part: lakehouse.schema.table
- 2-part: lakehouse.table or schema.table
- 1-part: table

::: msfabricutils.common.fabric_duckdb_connection