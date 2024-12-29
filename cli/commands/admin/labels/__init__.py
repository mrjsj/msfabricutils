from cyclopts import App

from .bulk_remove import bulk_remove_command
from .bulk_set import bulk_set_command

labels_app = App(name="labels", help="[yellow]Commands for labels[/yellow]")
labels_app.command(bulk_remove_command, name="bulk-remove")
labels_app.command(bulk_set_command, name="bulk-set")
