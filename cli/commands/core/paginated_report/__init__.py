from cyclopts import App

from .list import list_command
from .update import update_command

paginated_report_app = App(name="paginated-report", help="[yellow]Commands for paginated_report[/yellow]")
paginated_report_app.command(list_command, name="list")
paginated_report_app.command(update_command, name="update")
