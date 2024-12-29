from cyclopts import App

from .create import create_command
from .delete import delete_command
from .get import get_command
from .list import list_command
from .update import update_command

ml_model_app = App(name="ml-model", help="[yellow]Commands for ml_model[/yellow]")
ml_model_app.command(create_command, name="create")
ml_model_app.command(delete_command, name="delete")
ml_model_app.command(get_command, name="get")
ml_model_app.command(list_command, name="list")
ml_model_app.command(update_command, name="update")
