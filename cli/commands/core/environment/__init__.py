from cyclopts import App

from .create import create_command
from .delete import delete_command
from .get import get_command
from .list import list_command
from .spark_compute import spark_compute_app
from .spark_libraries import spark_libraries_app
from .update import update_command

environment_app = App(name="environment", help="[yellow]Commands for environment[/yellow]")
environment_app.command(create_command, name="create")
environment_app.command(delete_command, name="delete")
environment_app.command(get_command, name="get")
environment_app.command(list_command, name="list")
environment_app.command(update_command, name="update")
environment_app.command(spark_compute_app)
environment_app.command(spark_libraries_app)
