from cyclopts import App

from .list_capacities_tenant_settings_overrides import list_capacities_tenant_settings_overrides_command
from .list_tenant_settings import list_tenant_settings_command

tenants_app = App(name="tenants", help="[yellow]Commands for tenants[/yellow]")
tenants_app.command(list_capacities_tenant_settings_overrides_command, name="list-capacities-tenant-settings-overrides")
tenants_app.command(list_tenant_settings_command, name="list-tenant-settings")
