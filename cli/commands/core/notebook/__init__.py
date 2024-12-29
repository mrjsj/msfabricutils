from cyclopts import App

from .create import create_command
from .delete import delete_command
from .get import get_command
from .get_definition import get_definition_command
from .list import list_command
from .update import update_command
from .update_definition import update_definition_command

notebook_app = App(name="notebook", help="[yellow]Commands for notebook[/yellow]")
notebook_app.command(create_command, name="create")
notebook_app.command(delete_command, name="delete")
notebook_app.command(get_command, name="get")
notebook_app.command(get_definition_command, name="get-definition")
notebook_app.command(list_command, name="list")
notebook_app.command(update_command, name="update")
notebook_app.command(update_definition_command, name="update-definition")
