from cyclopts import App

from .add_role_assignment import add_role_assignment_command
from .create import create_command
from .delete import delete_command
from .delete_role_assignment import delete_role_assignment_command
from .get import get_command
from .get_role_assignment import get_role_assignment_command
from .list import list_command
from .list_role_assignments import list_role_assignments_command
from .list_supported_connection_types import list_supported_connection_types_command
from .update import update_command
from .update_role_assignment import update_role_assignment_command

connections_app = App(name="connections", help="[yellow]Commands for connections[/yellow]")
connections_app.command(add_role_assignment_command, name="add-role-assignment")
connections_app.command(create_command, name="create")
connections_app.command(delete_command, name="delete")
connections_app.command(delete_role_assignment_command, name="delete-role-assignment")
connections_app.command(get_command, name="get")
connections_app.command(get_role_assignment_command, name="get-role-assignment")
connections_app.command(list_role_assignments_command, name="list-role-assignments")
connections_app.command(list_command, name="list")
connections_app.command(list_supported_connection_types_command, name="list-supported-connection-types")
connections_app.command(update_command, name="update")
connections_app.command(update_role_assignment_command, name="update-role-assignment")
