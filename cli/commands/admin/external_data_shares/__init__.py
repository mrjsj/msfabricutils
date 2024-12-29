from cyclopts import App

from .list import list_command
from .revoke import revoke_command

external_data_shares_app = App(name="external-data-shares", help="[yellow]Commands for external_data_shares[/yellow]")
external_data_shares_app.command(list_command, name="list")
external_data_shares_app.command(revoke_command, name="revoke")
