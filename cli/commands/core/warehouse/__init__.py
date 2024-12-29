from cyclopts import App

from .create import create_command
from .delete import delete_command
from .get import get_command
from .list import list_command
from .update import update_command

warehouse_app = App(name="warehouse", help="[yellow]Commands for warehouse[/yellow]")
warehouse_app.command(create_command, name="create")
warehouse_app.command(delete_command, name="delete")
warehouse_app.command(get_command, name="get")
warehouse_app.command(list_command, name="list")
warehouse_app.command(update_command, name="update")
