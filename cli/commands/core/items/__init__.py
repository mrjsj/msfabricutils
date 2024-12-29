from cyclopts import App

from .create import create_command
from .delete import delete_command
from .get import get_command
from .get_definition import get_definition_command
from .list import list_command
from .list_connections import list_connections_command
from .update import update_command
from .update_definition import update_definition_command

items_app = App(name="items", help="[yellow]Commands for items[/yellow]")
items_app.command(create_command, name="create")
items_app.command(delete_command, name="delete")
items_app.command(get_command, name="get")
items_app.command(get_definition_command, name="get-definition")
items_app.command(list_connections_command, name="list-connections")
items_app.command(list_command, name="list")
items_app.command(update_command, name="update")
items_app.command(update_definition_command, name="update-definition")
