from cyclopts import App

from .create import create_command
from .delete import delete_command
from .get import get_command
from .list import list_command
from .update import update_command

data_pipeline_app = App(name="data-pipeline", help="[yellow]Commands for data_pipeline[/yellow]")
data_pipeline_app.command(create_command, name="create")
data_pipeline_app.command(delete_command, name="delete")
data_pipeline_app.command(get_command, name="get")
data_pipeline_app.command(list_command, name="list")
data_pipeline_app.command(update_command, name="update")
