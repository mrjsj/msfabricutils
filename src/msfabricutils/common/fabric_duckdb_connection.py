from typing import Any

import duckdb
import sqlglot
from deltalake import write_deltalake
from sqlglot import exp

from msfabricutils.common import _separator_indices
from msfabricutils.core import (
    get_workspace,
    get_workspace_lakehouse_tables,
    get_workspace_lakehouses,
)


class FabricDuckDBConnection:
    """A DuckDB connection wrapper for Microsoft Fabric Lakehouses.

    Provides a seamless interface between DuckDB and Microsoft Fabric Lakehouses,
    allowing SQL queries across multiple lakehouses - even lakehouses across workspaces with automatic table registration.

    Features:
        - Automatic table registration from Fabric lakehouses
        - Cross-lakehouse and cross-workspace querying
        - Token-based authentication
        - Delta Lake table support

    Args:
        access_token (str): The Microsoft Fabric access token for authentication.
            In a notebook, use `notebookutils.credentials.getToken('storage')`.
        config (dict, optional): DuckDB configuration options. Defaults to {}.

    Example:
    ```python
    # Initialize connection
    access_token = notebookutils.credentials.getToken('storage')
    conn = FabricDuckDBConnection(access_token=access_token)

    # Register lakehouses from different workspaces
    conn.register_workspace_lakehouses(
        workspace_id='12345678-1234-5678-1234-567812345678',
        lakehouses=['sales', 'marketing']
    )
    conn.register_workspace_lakehouses(
        workspace_id='87654321-8765-4321-8765-432187654321',
        lakehouses=['marketing']
    )

    # Query across workspaces using fully qualified names
    df = conn.sql(\"\"\"
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
        \"\"\").df()
    ```
    """

    def __init__(self, access_token: str, config: dict = {}):
        self._registered_tables = []
        self._connection = duckdb.connect(config=config)
        self._default_schema = "main"
        self._access_token = access_token

    def __getattr__(self, name):
        if name == "sql" or name == "execute":

            def wrapper(*args, **kwargs):
                original_method = getattr(self._connection, name)

                # Modify the query/parameters here before passing to the actual method
                modified_args, modified_kwargs = self._modify_input_query(args, kwargs)

                return original_method(*modified_args, **modified_kwargs)

            return wrapper
        return getattr(self._connection, name)

    def __dir__(self):
        return list(super().__dir__()) + dir(self._connection)

    def refresh_access_token(self, access_token: str):
        """Refresh the access token for all registered lakehouses.

        Args:
            access_token (str): The new access token to use

        Example:
        ```python
        # Initialize connection
        conn = FabricDuckDBConnection(access_token='old_token')

        # When token expires, refresh it
        new_token = notebookutils.credentials.getToken('storage')
        conn.refresh_access_token(new_token)
        ```
        """
        self._access_token = access_token

        lakehouses_to_refresh = self._connection.sql("""
            SELECT DISTINCT
                table_catalog
            FROM information_schema.tables;
        """).fetchall()

        for lakehouse in lakehouses_to_refresh:
            self._create_or_replace_fabric_lakehouse_secret(lakehouse)

    def _preprocess_sql_query(self, query: str):
        """Preprocess a SQL query to handle table references and ensure proper qualification.

        Args:
            query (str): The SQL query to preprocess

        Returns:
            str: The preprocessed query with fully qualified table references

        Raises:
            Exception: If table references are ambiguous or tables don't exist
        """
        parsed = sqlglot.parse_one(sql=query, read="duckdb")
        tables_in_query = parsed.find_all(exp.Table)
        replace_by = {}
        for table in tables_in_query:
            table_name = str(table)

            # Skip functions, i.e. `read_parquet`.
            if isinstance(table.this, exp.Anonymous):
                continue

            table_alias_indices = _separator_indices(table_name, " ")

            if table_alias_indices:
                table_alias_start_index = table_alias_indices[0]
                table_name = table_name[:table_alias_start_index]

            separator_indices = _separator_indices(table_name, ".")

            if len(separator_indices) == 0:
                table_name = table_name.replace('"', "")

                matches = self._connection.sql(f"""
                    SELECT
                        table_catalog,
                        table_schema,
                        table_name
                    FROM information_schema.tables
                    WHERE table_name = '{table_name}'
                """).fetchall()

                if len(matches) > 1:
                    raise Exception(
                        f"Ambiguous reference to table {table_name} - use a fully qualified path."
                    )
                elif len(matches) == 0:
                    raise Exception(
                        f"Table {table_name} does not exist.\nIf it was recently created, ensure running `register_lakehouse_tables` to fully refresh the table catalog."
                    )

            elif len(separator_indices) == 1:
                catalog_or_schema_name = table_name[: separator_indices[0]].replace('"', "")
                table_name = table_name[separator_indices[0] + 1 :].replace('"', "")

                matches = self._connection.sql(f"""
                    SELECT
                        table_catalog,
                        table_schema,
                        table_name
                    FROM information_schema.tables
                    WHERE table_name = '{table_name}'
                    AND (
                        table_schema = '{catalog_or_schema_name}'
                        OR
                        table_catalog LIKE '%.{catalog_or_schema_name}'
                    )
                """).fetchall()

                if len(matches) > 1:
                    raise Exception(
                        f"Ambiguous reference to table {catalog_or_schema_name}.{table_name} - use a fully qualified path."
                    )
                elif len(matches) == 0:
                    raise Exception(
                        f"Table {catalog_or_schema_name}.{table_name} does not exist.\nIf it was recently created, ensure running `register_lakehouse_tables` to fully refresh the table catalog."
                    )

            elif len(separator_indices) == 2:
                workspace_or_catalog_name = table_name[: separator_indices[0]].replace('"', "")
                catalog_or_schema_name = table_name[
                    separator_indices[0] + 1 : separator_indices[1]
                ].replace('"', "")
                table_name = table_name[separator_indices[1] + 1 :].replace('"', "")

                matches = self._connection.sql(f"""
                    SELECT
                        table_catalog,
                        table_schema,
                        table_name
                    FROM information_schema.tables
                    WHERE table_name = '{table_name}'
                    AND (
                            (
                                table_schema = '{catalog_or_schema_name}'
                                AND
                                table_catalog LIKE '%.{workspace_or_catalog_name}'
                            )
                        OR
                        (
                            table_catalog = '{workspace_or_catalog_name}.{catalog_or_schema_name}'
                        )
                    )
                """).fetchall()

                if len(matches) > 1:
                    raise Exception(
                        f"Ambiguous reference to table {workspace_or_catalog_name}.{catalog_or_schema_name}.{table_name} - use a fully qualified path."
                    )
                elif len(matches) == 0:
                    raise Exception(
                        f"Table {workspace_or_catalog_name}.{catalog_or_schema_name}.{table_name} does not exist.\nIf it was recently created, ensure running `register_lakehouse_tables` to fully refresh the table catalog."
                    )

            elif len(separator_indices) == 3:
                workspace_name = table_name[: separator_indices[0]].replace('"', "")
                lakehouse_name = table_name[
                    separator_indices[0] + 1 : separator_indices[1]
                ].replace('"', "")
                schema_name = table_name[separator_indices[1] + 1 : separator_indices[2]].replace(
                    '"', ""
                )
                table_name = table_name[separator_indices[2] + 1 :].replace('"', "")

                matches = self._connection.sql(f"""
                    SELECT
                        table_catalog,
                        table_schema,
                        table_name
                    FROM information_schema.tables
                    WHERE table_name = '{table_name}'
                    AND table_schema = '{schema_name}'
                    AND table_catalog = '{workspace_name}.{lakehouse_name}'
                """).fetchall()

                if len(matches) > 1:
                    raise Exception(
                        f"Ambiguous reference to table {workspace_name}.{lakehouse_name}.{schema_name}.{table_name} - use a fully qualified path."
                    )
                elif len(matches) == 0:
                    raise Exception(
                        f"Table {workspace_name}.{lakehouse_name}.{schema_name}.{table_name} does not exist.\nIf it was recently created, ensure running `register_lakehouse_tables` to fully refresh the table catalog."
                    )

            else:
                continue

            catalog_name, schema_name, table_name = matches[0]
            replace_by[table] = f'"{catalog_name}"."{schema_name}"."{table_name}"'

        return str(exp.replace_tables(parsed, replace_by))

    def _modify_input_query(self, args, kwargs):
        """Modify query arguments before passing to DuckDB connection.

        Args:
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            tuple: Modified (args, kwargs)
        """
        modified_args = list(args)

        if "query" in kwargs:
            kwargs["query"] = self._preprocess_input(kwargs["query"])

        elif modified_args and isinstance(modified_args[0], str):
            modified_args[0] = self._preprocess_input(modified_args[0])

        return modified_args, kwargs

    def _preprocess_input(self, query: str) -> str:
        """Preprocess a multi-statement SQL input.

        Args:
            query (str): The SQL input to preprocess

        Returns:
            str: The preprocessed SQL statements
        """
        query_separator_indices = _separator_indices(query, ";")
        query_separator_indices = [0] + [idx + 1 for idx in query_separator_indices]

        queries = []
        for i, j in zip(query_separator_indices, query_separator_indices[1:] + [None]):
            query_part = query[i:j]

            if len(query_part.strip()) > 1:
                query_part = self._preprocess_sql_query(query_part) + ";"

            queries.append(query_part)

        return "".join(queries)

    def _attach_lakehouse(self, workspace_name: str, lakehouse: str) -> None:
        self._connection.sql(f"""
            ATTACH ':memory:' AS "{workspace_name}.{lakehouse}";
        """)

    def _create_or_replace_fabric_lakehouse_secret(self, catalog_name: str) -> None:
        self._connection.sql(f"""
            USE "{catalog_name}";                     
            CREATE OR REPLACE SECRET fabric_lakehouse_secret (
                TYPE AZURE,
                PROVIDER ACCESS_TOKEN,
                ACCESS_TOKEN '{self._access_token}'
            )
        """)

    def _register_lakehouse_tables(
        self, workspace_name: str, workspace_id: str, lakehouse_id: str, lakehouse_name: str
    ) -> None:
        tables = get_workspace_lakehouse_tables(workspace_id, lakehouse_id)

        if not tables:
            table_information = {
                "workspace_id": workspace_id,
                "workspace_name": workspace_name,
                "lakehouse_id": lakehouse_id,
                "lakehouse_name": lakehouse_name,
                "schema_name": None,
                "table_name": None,
                "table_location": None,
            }

            self._registered_tables.append(table_information)

        for table in tables:
            self._connection.sql(f"""
                CREATE OR REPLACE VIEW {self._default_schema}.{table["name"]} AS
                SELECT 
                    * 
                FROM
                    delta_scan('{table["location"]}')
            """)

            is_table_registered = any(
                registered_table
                for registered_table in self._registered_tables
                if registered_table["workspace_id"] == workspace_id
                and registered_table["lakehouse_id"] == lakehouse_id
                and registered_table["table_name"] == table["name"]
            )

            if not is_table_registered:
                table_information = {
                    "workspace_id": workspace_id,
                    "workspace_name": workspace_name,
                    "lakehouse_id": lakehouse_id,
                    "lakehouse_name": lakehouse_name,
                    "schema_name": self._default_schema,
                    "table_name": table["name"],
                    "table_location": table["location"],
                }

                self._registered_tables.append(table_information)
            print(
                f"Table `{workspace_name}.{lakehouse_name}.{self._default_schema}.{table['name']}` registered ..."
            )

    def register_workspace_lakehouses(self, workspace_id: str, lakehouses: str | list[str] = None):
        """Register one or more lakehouses from a workspace for querying.

        Args:
            workspace_id (str): The ID of the Microsoft Fabric workspace
            lakehouses (str | list[str], optional): Name(s) of lakehouse(s) to register.

        Raises:
            Exception: If a lakehouse uses the schema-enabled preview feature

        Example:
        ```python
        # Initialize connection with access token
        access_token = notebookutils.credentials.getToken('storage')
        conn = FabricDuckDBConnection(access_token=access_token)

        # Register a single lakehouse
        conn.register_workspace_lakehouses(
            workspace_id='12345678-1234-5678-1234-567812345678',
            lakehouses='sales_lakehouse'
        )

        # Register multiple lakehouses
        conn.register_workspace_lakehouses(
            workspace_id='12345678-1234-5678-1234-567812345678',
            lakehouses=['sales_lakehouse', 'marketing_lakehouse']
        )
        ```
        """

        if isinstance(lakehouses, str):
            lakehouses = [lakehouses]

        workspace_info = get_workspace(workspace_id)

        workspace_name = workspace_info["displayName"]

        lakehouse_properties = get_workspace_lakehouses(workspace_id)

        selected_lakehouses = [
            lakehouse
            for lakehouse in lakehouse_properties
            if lakehouse["displayName"] in lakehouses
        ]

        for lakehouse in selected_lakehouses:
            is_schema_enabled = lakehouse.get("properties").get("defaultSchema") is not None

            lakehouse_name = lakehouse.get("displayName")
            lakehouse_id = lakehouse.get("id")

            if is_schema_enabled:
                raise Exception(f"""
                    The lakehouse `{lakehouse_name}` is using the schema-enabled preview feature.\n
                    This utility class does support schema-enabled lakehouses (yet).
                """)

            self._attach_lakehouse(workspace_name, lakehouse_name)
            self._create_or_replace_fabric_lakehouse_secret(f"{workspace_name}.{lakehouse_name}")
            self._register_lakehouse_tables(
                workspace_name, workspace_id, lakehouse_id, lakehouse_name
            )

    def print_lakehouse_catalog(self):
        """Print a hierarchical view of all registered lakehouses, schemas, and tables.

        Example:
        ```python
        conn.print_lakehouse_catalog()
        📁 Database: workspace1.sales_lakehouse
        └─📂 Schema: main
            ├─📄 customers
            ├─📄 orders
            └─📄 products
        📁 Database: workspace1.marketing_lakehouse
        └─📂 Schema: main
            ├─📄 campaigns
            └─📄 customer_segments
        ```
        """

        query = """
            SELECT 
                table_catalog as lakehouse_name,
                table_schema as schema_name,
                table_name
            FROM information_schema.tables
            ORDER BY table_catalog, table_schema, table_name
        """

        results = self._connection.sql(query).fetchall()

        current_lakehouse = None
        current_lakehouse_schema = None

        for lakehouse_name, schema_name, table_name in results:
            if current_lakehouse != lakehouse_name:
                current_lakehouse = lakehouse_name
                print(f"📁 Database: {lakehouse_name}")

            lakehouse_schema = (lakehouse_name, schema_name)
            if current_lakehouse_schema != lakehouse_schema:
                current_lakehouse_schema = lakehouse_schema
                print(f"  └─📂 Schema: {schema_name}")

            print(f"     ├─📄 {table_name}")

    def write(
        self,
        df: Any,
        full_table_name: str,
        workspace_id: str = None,
        workspace_name: str = None,
        *args: Any,
        **kwargs: Any,
    ):
        """Write a DataFrame to a Fabric Lakehouse table.

        Args:
            df: The DataFrame to write
            full_table_name (str): Table name in format '<lakehouse_name>.<table_name>'
            workspace_id (str, optional): The workspace ID. Required if multiple workspaces are registered
            workspace_name (str, optional): The workspace name. Alternative to workspace_id
            *args (Any): Additional positional arguments passed to write_deltalake
            **kwargs (Any): Additional keyword arguments passed to write_deltalake. Commonly used kwargs:
                    mode (str): 'error' or 'overwrite'. Defaults to 'error'
                    partition_by (list[str]): Columns to partition by

        Raises:
            Exception: If table_name format is invalid or workspace cannot be determined
        """
        table_parts = full_table_name.split(".")

        if len(table_parts) != 2:
            raise Exception(
                "The parameter `full_table_name` must consist of three parts, i.e. `<lakehouse_name>.<table_name>`."
            )

        lakehouse_name = table_parts[0]
        table_name = table_parts[1]

        if not workspace_id and not workspace_name:
            workspace_ids = list(
                set([registed_table["workspace_id"] for registed_table in self._registered_tables])
            )

            if len(workspace_ids) > 1:
                raise Exception(
                    "The FabricDuckDBConnection has registered multiple workspaces, so `workspace_id` or `workspace_name` must be supplied."
                )

        table_information = [
            table
            for table in self._registered_tables
            if (table["workspace_id"] == workspace_id or table["workspace_name"] == workspace_name)
            and table["lakehouse_name"] == lakehouse_name
        ][0]

        lakehouse_id = table_information["lakehouse_id"]
        workspace_id = table_information["workspace_id"]
        workspace_name = table_information["workspace_name"]

        table_uri = f"abfss://{workspace_id}@onelake.dfs.fabric.microsoft.com/{lakehouse_id}/Tables/{table_name}"

        write_deltalake(
            table_or_uri=table_uri,
            data=df,
            *args,
            **kwargs,
        )

        self._connection.sql(f"""
            CREATE OR REPLACE VIEW "{workspace_name}.{lakehouse_name}".main.{table_name} AS
            SELECT 
                * 
            FROM
                delta_scan('{table_uri}')
        """)
