from cyclopts import App

from .domains import domains_app
from .external_data_shares import external_data_shares_app
from .items import items_app
from .labels import labels_app
from .tenants import tenants_app
from .users import users_app
from .workspaces import workspaces_app

admin_app = App(name="admin", help="[yellow]Commands for admin[/yellow]")
admin_app.command(domains_app)
admin_app.command(external_data_shares_app)
admin_app.command(items_app)
admin_app.command(labels_app)
admin_app.command(tenants_app)
admin_app.command(users_app)
admin_app.command(workspaces_app)
