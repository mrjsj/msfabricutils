from cyclopts import App

from .create import create_command
from .delete import delete_command
from .get import get_command
from .list import list_command
from .update import update_command

ml_experiment_app = App(name="ml-experiment", help="[yellow]Commands for ml_experiment[/yellow]")
ml_experiment_app.command(create_command, name="create")
ml_experiment_app.command(delete_command, name="delete")
ml_experiment_app.command(get_command, name="get")
ml_experiment_app.command(list_command, name="list")
ml_experiment_app.command(update_command, name="update")
