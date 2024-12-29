from cyclopts import App

from .list import list_command

capacities_app = App(name="capacities", help="[yellow]Commands for capacities[/yellow]")
capacities_app.command(list_command, name="list")
