from cyclopts import App

from .get import get_command
from .list import list_command
from .list_access_details import list_access_details_command

items_app = App(name="items", help="[yellow]Commands for items[/yellow]")
items_app.command(get_command, name="get")
items_app.command(list_access_details_command, name="list-access-details")
items_app.command(list_command, name="list")
