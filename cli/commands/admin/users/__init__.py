from cyclopts import App

from .list_access_entities import list_access_entities_command

users_app = App(name="users", help="[yellow]Commands for users[/yellow]")
users_app.command(list_access_entities_command, name="list-access-entities")
