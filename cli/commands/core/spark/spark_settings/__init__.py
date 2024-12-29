from cyclopts import App

from .get import get_command
from .update import update_command

spark_settings_app = App(name="spark-settings", help="[yellow]Commands for spark_settings[/yellow]")
spark_settings_app.command(get_command, name="get")
spark_settings_app.command(update_command, name="update")
