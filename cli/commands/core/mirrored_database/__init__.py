from cyclopts import App

from .create import create_command
from .delete import delete_command
from .get import get_command
from .get_definition import get_definition_command
from .list import list_command
from .mirroring import mirroring_app
from .update import update_command
from .update_definition import update_definition_command

mirrored_database_app = App(name="mirrored-database", help="[yellow]Commands for mirrored_database[/yellow]")
mirrored_database_app.command(create_command, name="create")
mirrored_database_app.command(delete_command, name="delete")
mirrored_database_app.command(get_command, name="get")
mirrored_database_app.command(get_definition_command, name="get-definition")
mirrored_database_app.command(list_command, name="list")
mirrored_database_app.command(update_command, name="update")
mirrored_database_app.command(update_definition_command, name="update-definition")
mirrored_database_app.command(mirroring_app)
