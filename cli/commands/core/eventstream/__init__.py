from cyclopts import App

from .create import create_command
from .delete import delete_command
from .get import get_command
from .get_definition import get_definition_command
from .list import list_command
from .update import update_command
from .update_definition import update_definition_command

eventstream_app = App(name="eventstream", help="[yellow]Commands for eventstream[/yellow]")
eventstream_app.command(create_command, name="create")
eventstream_app.command(delete_command, name="delete")
eventstream_app.command(get_command, name="get")
eventstream_app.command(get_definition_command, name="get-definition")
eventstream_app.command(list_command, name="list")
eventstream_app.command(update_command, name="update")
eventstream_app.command(update_definition_command, name="update-definition")
