from cyclopts import App

from .create import create_command
from .delete import delete_command
from .get import get_command
from .list import list_command
from .update import update_command

custom_pools_app = App(name="custom-pools", help="[yellow]Commands for custom_pools[/yellow]")
custom_pools_app.command(create_command, name="create")
custom_pools_app.command(delete_command, name="delete")
custom_pools_app.command(get_command, name="get")
custom_pools_app.command(list_command, name="list")
custom_pools_app.command(update_command, name="update")
