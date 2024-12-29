from cyclopts import App

from .list import list_command

datamart_app = App(name="datamart", help="[yellow]Commands for datamart[/yellow]")
datamart_app.command(list_command, name="list")
