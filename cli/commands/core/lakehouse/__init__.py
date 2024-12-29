from cyclopts import App

from .background_jobs import background_jobs_app
from .create import create_command
from .delete import delete_command
from .get import get_command
from .list import list_command
from .tables import tables_app
from .update import update_command

lakehouse_app = App(name="lakehouse", help="[yellow]Commands for lakehouse[/yellow]")
lakehouse_app.command(background_jobs_app)
lakehouse_app.command(create_command, name="create")
lakehouse_app.command(delete_command, name="delete")
lakehouse_app.command(get_command, name="get")
lakehouse_app.command(list_command, name="list")
lakehouse_app.command(update_command, name="update")
lakehouse_app.command(tables_app)
