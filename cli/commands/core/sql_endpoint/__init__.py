from cyclopts import App

from .list import list_command

sql_endpoint_app = App(name="sql-endpoint", help="[yellow]Commands for sql_endpoint[/yellow]")
sql_endpoint_app.command(list_command, name="list")
