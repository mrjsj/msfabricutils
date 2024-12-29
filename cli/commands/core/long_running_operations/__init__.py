from cyclopts import App

from .get_result import get_result_command
from .get_state import get_state_command

long_running_operations_app = App(name="long-running-operations", help="[yellow]Commands for long_running_operations[/yellow]")
long_running_operations_app.command(get_result_command, name="get-result")
long_running_operations_app.command(get_state_command, name="get-state")
