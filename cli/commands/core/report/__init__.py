from cyclopts import App

from .create import create_command
from .delete import delete_command
from .get import get_command
from .get_definition import get_definition_command
from .list import list_command
from .update_definition import update_definition_command

report_app = App(name="report", help="[yellow]Commands for report[/yellow]")
report_app.command(create_command, name="create")
report_app.command(delete_command, name="delete")
report_app.command(get_command, name="get")
report_app.command(get_definition_command, name="get-definition")
report_app.command(list_command, name="list")
report_app.command(update_definition_command, name="update-definition")
