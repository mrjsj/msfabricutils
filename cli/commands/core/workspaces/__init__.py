from cyclopts import App

from .add_role_assignment import add_role_assignment_command
from .assign_to_capacity import assign_to_capacity_command
from .create import create_command
from .delete import delete_command
from .delete_role_assignment import delete_role_assignment_command
from .deprovision_identity import deprovision_identity_command
from .get import get_command
from .get_role_assignment import get_role_assignment_command
from .list import list_command
from .list_role_assignments import list_role_assignments_command
from .provision_identity import provision_identity_command
from .unassign_from_capacity import unassign_from_capacity_command
from .update import update_command
from .update_role_assignment import update_role_assignment_command

workspaces_app = App(name="workspaces", help="[yellow]Commands for workspaces[/yellow]")
workspaces_app.command(add_role_assignment_command, name="add-role-assignment")
workspaces_app.command(assign_to_capacity_command, name="assign-to-capacity")
workspaces_app.command(create_command, name="create")
workspaces_app.command(delete_command, name="delete")
workspaces_app.command(delete_role_assignment_command, name="delete-role-assignment")
workspaces_app.command(deprovision_identity_command, name="deprovision-identity")
workspaces_app.command(get_command, name="get")
workspaces_app.command(get_role_assignment_command, name="get-role-assignment")
workspaces_app.command(list_role_assignments_command, name="list-role-assignments")
workspaces_app.command(list_command, name="list")
workspaces_app.command(provision_identity_command, name="provision-identity")
workspaces_app.command(unassign_from_capacity_command, name="unassign-from-capacity")
workspaces_app.command(update_command, name="update")
workspaces_app.command(update_role_assignment_command, name="update-role-assignment")
