from cyclopts import App

from .create import create_command
from .delete import delete_command
from .get import get_command
from .get_definition import get_definition_command
from .list import list_command
from .update import update_command
from .update_definition import update_definition_command

kql_database_app = App(name="kql-database", help="[yellow]Commands for kql_database[/yellow]")
kql_database_app.command(create_command, name="create")
kql_database_app.command(delete_command, name="delete")
kql_database_app.command(get_command, name="get")
kql_database_app.command(get_definition_command, name="get-definition")
kql_database_app.command(list_command, name="list")
kql_database_app.command(update_command, name="update")
kql_database_app.command(update_definition_command, name="update-definition")
