from cyclopts import App

from .create import create_command
from .delete import delete_command
from .get import get_command
from .list import list_command

one_lake_shortcuts_app = App(name="one-lake-shortcuts", help="[yellow]Commands for one_lake_shortcuts[/yellow]")
one_lake_shortcuts_app.command(create_command, name="create")
one_lake_shortcuts_app.command(delete_command, name="delete")
one_lake_shortcuts_app.command(get_command, name="get")
one_lake_shortcuts_app.command(list_command, name="list")
