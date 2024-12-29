from cyclopts import App

from .list import list_command

mirrored_warehouse_app = App(name="mirrored-warehouse", help="[yellow]Commands for mirrored_warehouse[/yellow]")
mirrored_warehouse_app.command(list_command, name="list")
