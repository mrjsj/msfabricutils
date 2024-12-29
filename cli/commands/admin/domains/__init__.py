from cyclopts import App

from .assign_workspaces_by_capacities import assign_workspaces_by_capacities_command
from .assign_workspaces_by_ids import assign_workspaces_by_ids_command
from .assign_workspaces_by_principals import assign_workspaces_by_principals_command
from .bulk_assign_role_assignments import bulk_assign_role_assignments_command
from .bulk_unassign_role_assignments import bulk_unassign_role_assignments_command
from .create import create_command
from .delete import delete_command
from .get import get_command
from .list import list_command
from .list_workspaces import list_workspaces_command
from .unassign_all_workspaces import unassign_all_workspaces_command
from .unassign_workspaces_by_ids import unassign_workspaces_by_ids_command
from .update import update_command

domains_app = App(name="domains", help="[yellow]Commands for domains[/yellow]")
domains_app.command(assign_workspaces_by_capacities_command, name="assign-workspaces-by-capacities")
domains_app.command(assign_workspaces_by_ids_command, name="assign-workspaces-by-ids")
domains_app.command(assign_workspaces_by_principals_command, name="assign-workspaces-by-principals")
domains_app.command(create_command, name="create")
domains_app.command(delete_command, name="delete")
domains_app.command(get_command, name="get")
domains_app.command(list_workspaces_command, name="list-workspaces")
domains_app.command(list_command, name="list")
domains_app.command(bulk_assign_role_assignments_command, name="bulk-assign-role-assignments")
domains_app.command(bulk_unassign_role_assignments_command, name="bulk-unassign-role-assignments")
domains_app.command(unassign_all_workspaces_command, name="unassign-all-workspaces")
domains_app.command(unassign_workspaces_by_ids_command, name="unassign-workspaces-by-ids")
domains_app.command(update_command, name="update")
