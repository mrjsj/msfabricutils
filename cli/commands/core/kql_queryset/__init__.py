from cyclopts import App

from .create import create_command
from .delete import delete_command
from .get import get_command
from .get_definition import get_definition_command
from .list import list_command
from .update import update_command
from .update_definition import update_definition_command

kql_queryset_app = App(name="kql-queryset", help="[yellow]Commands for kql_queryset[/yellow]")
kql_queryset_app.command(create_command, name="create")
kql_queryset_app.command(delete_command, name="delete")
kql_queryset_app.command(get_command, name="get")
kql_queryset_app.command(get_definition_command, name="get-definition")
kql_queryset_app.command(list_command, name="list")
kql_queryset_app.command(update_command, name="update")
kql_queryset_app.command(update_definition_command, name="update-definition")
