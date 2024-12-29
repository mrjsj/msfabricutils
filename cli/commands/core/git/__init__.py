from cyclopts import App

from .commit import commit_command
from .connect import connect_command
from .disconnect import disconnect_command
from .get_connection import get_connection_command
from .get_my_git_credentials import get_my_git_credentials_command
from .get_status import get_status_command
from .initialize_connection import initialize_connection_command
from .update_from_git import update_from_git_command
from .update_my_git_credentials import update_my_git_credentials_command

git_app = App(name="git", help="[yellow]Commands for git[/yellow]")
git_app.command(commit_command, name="commit")
git_app.command(connect_command, name="connect")
git_app.command(disconnect_command, name="disconnect")
git_app.command(get_connection_command, name="get-connection")
git_app.command(get_my_git_credentials_command, name="get-my-git-credentials")
git_app.command(get_status_command, name="get-status")
git_app.command(initialize_connection_command, name="initialize-connection")
git_app.command(update_from_git_command, name="update-from-git")
git_app.command(update_my_git_credentials_command, name="update-my-git-credentials")
