from cyclopts import App

from .get_status import get_status_command
from .get_tables_status import get_tables_status_command
from .start import start_command
from .stop import stop_command

mirroring_app = App(name="mirroring", help="[yellow]Commands for mirroring[/yellow]")
mirroring_app.command(get_status_command, name="get-status")
mirroring_app.command(get_tables_status_command, name="get-tables-status")
mirroring_app.command(start_command, name="start")
mirroring_app.command(stop_command, name="stop")
