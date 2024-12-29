from cyclopts import App

from .create import create_command
from .delete import delete_command
from .get import get_command
from .get_definition import get_definition_command
from .list import list_command
from .update import update_command
from .update_definition import update_definition_command

eventhouse_app = App(name="eventhouse", help="[yellow]Commands for eventhouse[/yellow]")
eventhouse_app.command(create_command, name="create")
eventhouse_app.command(delete_command, name="delete")
eventhouse_app.command(get_command, name="get")
eventhouse_app.command(get_definition_command, name="get-definition")
eventhouse_app.command(list_command, name="list")
eventhouse_app.command(update_command, name="update")
eventhouse_app.command(update_definition_command, name="update-definition")
