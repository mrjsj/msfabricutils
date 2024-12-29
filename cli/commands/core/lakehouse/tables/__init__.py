from cyclopts import App

from .list import list_command
from .load import load_command

tables_app = App(name="tables", help="[yellow]Commands for tables[/yellow]")
tables_app.command(list_command, name="list")
tables_app.command(load_command, name="load")
