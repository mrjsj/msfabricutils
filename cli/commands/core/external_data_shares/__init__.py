from cyclopts import App

from .create import create_command
from .get import get_command
from .list_in_item import list_in_item_command
from .revoke import revoke_command

external_data_shares_app = App(name="external-data-shares", help="[yellow]Commands for external_data_shares[/yellow]")
external_data_shares_app.command(create_command, name="create")
external_data_shares_app.command(get_command, name="get")
external_data_shares_app.command(list_in_item_command, name="list-in-item")
external_data_shares_app.command(revoke_command, name="revoke")
