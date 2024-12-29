from cyclopts import App

from .list import list_command

dashboard_app = App(name="dashboard", help="[yellow]Commands for dashboard[/yellow]")
dashboard_app.command(list_command, name="list")
