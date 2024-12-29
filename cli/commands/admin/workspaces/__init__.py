from cyclopts import App

from .get import get_command
from .list import list_command
from .list_git_connections import list_git_connections_command
from .list_workspace_access_details import list_workspace_access_details_command
from .restore import restore_command

workspaces_app = App(name="workspaces", help="[yellow]Commands for workspaces[/yellow]")
workspaces_app.command(get_command, name="get")
workspaces_app.command(list_git_connections_command, name="list-git-connections")
workspaces_app.command(list_workspace_access_details_command, name="list-workspace-access-details")
workspaces_app.command(list_command, name="list")
workspaces_app.command(restore_command, name="restore")
