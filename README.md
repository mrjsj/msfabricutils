# MSFabricUtils
A collection of Spark-free Python utilities for working with Microsoft Fabric.
## Features
### DuckDB Connection Wrapper
Seamless integration between DuckDB and Microsoft Fabric Lakehouses
Cross-workspace and cross-lakehouse querying capabilities
Automatic table registration and authentication
Support for Delta Lake tables
Flexible table name referencing (1-part to 4-part names)
## Installation
```bash
pip install msfabricutils
```
## Quick Start
```python
from msfabricutils import FabricDuckDBConnection
# Initialize connection
access_token = notebookutils.credentials.getToken('storage')
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

# Write results back to a lakehouse
conn.write(df, 'sales.customer_segments_emea', workspace_id='12345678-1234-5678-1234-567812345678')
```

## Documentation
For detailed documentation, examples, and API reference, visit our [GitHub Pages documentation](https://mrjsj.github.io/msfabricutils/).

## Table Name Formats
The DuckDB Connection wrapper supports multiple table name formats (if unambiguous):
- 4-part: workspace.lakehouse.schema.table
- 3-part: lakehouse.schema.table
- 2-part: lakehouse.table
- 1-part: table

# Contributing
Contributions are welcome! Here are some ways you can contribute:
Report bugs and feature requests through GitHub issues
Submit pull requests for bug fixes or new features
Improve documentation
Share ideas for new utilities

# License
This project is licensed under the MIT License - see the LICENSE file for details.
