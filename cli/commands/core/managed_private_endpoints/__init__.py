from cyclopts import App

from .create import create_command
from .delete import delete_command
from .get import get_command
from .list import list_command

managed_private_endpoints_app = App(name="managed-private-endpoints", help="[yellow]Commands for managed_private_endpoints[/yellow]")
managed_private_endpoints_app.command(create_command, name="create")
managed_private_endpoints_app.command(delete_command, name="delete")
managed_private_endpoints_app.command(get_command, name="get")
managed_private_endpoints_app.command(list_command, name="list")
