from cyclopts import App

from .create_or_update_data_access_roles import create_or_update_data_access_roles_command
from .list_data_access_roles import list_data_access_roles_command

one_lake_data_access_security_app = App(name="one-lake-data-access-security", help="[yellow]Commands for one_lake_data_access_security[/yellow]")
one_lake_data_access_security_app.command(create_or_update_data_access_roles_command, name="create-or-update-data-access-roles")
one_lake_data_access_security_app.command(list_data_access_roles_command, name="list-data-access-roles")
