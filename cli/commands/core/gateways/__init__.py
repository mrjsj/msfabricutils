from cyclopts import App

from .add_role_assignment import add_role_assignment_command
from .create import create_command
from .delete import delete_command
from .delete_member import delete_member_command
from .delete_role_assignment import delete_role_assignment_command
from .get import get_command
from .get_role_assignment import get_role_assignment_command
from .list import list_command
from .list_members import list_members_command
from .list_role_assignments import list_role_assignments_command
from .update import update_command
from .update_member import update_member_command
from .update_role_assignment import update_role_assignment_command

gateways_app = App(name="gateways", help="[yellow]Commands for gateways[/yellow]")
gateways_app.command(add_role_assignment_command, name="add-role-assignment")
gateways_app.command(create_command, name="create")
gateways_app.command(delete_command, name="delete")
gateways_app.command(delete_member_command, name="delete-member")
gateways_app.command(delete_role_assignment_command, name="delete-role-assignment")
gateways_app.command(get_command, name="get")
gateways_app.command(get_role_assignment_command, name="get-role-assignment")
gateways_app.command(list_members_command, name="list-members")
gateways_app.command(list_role_assignments_command, name="list-role-assignments")
gateways_app.command(list_command, name="list")
gateways_app.command(update_command, name="update")
gateways_app.command(update_member_command, name="update-member")
gateways_app.command(update_role_assignment_command, name="update-role-assignment")
