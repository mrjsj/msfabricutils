from cyclopts import App

from .create import create_command
from .delete import delete_command
from .get import get_command
from .get_definition import get_definition_command
from .list import list_command
from .update import update_command
from .update_definition import update_definition_command

semantic_model_app = App(name="semantic-model", help="[yellow]Commands for semantic_model[/yellow]")
semantic_model_app.command(create_command, name="create")
semantic_model_app.command(delete_command, name="delete")
semantic_model_app.command(get_command, name="get")
semantic_model_app.command(get_definition_command, name="get-definition")
semantic_model_app.command(list_command, name="list")
semantic_model_app.command(update_command, name="update")
semantic_model_app.command(update_definition_command, name="update-definition")
