from cyclopts import App

from .get_published_settings import get_published_settings_command
from .get_staging_settings import get_staging_settings_command
from .update_staging_settings import update_staging_settings_command

spark_compute_app = App(name="spark-compute", help="[yellow]Commands for spark_compute[/yellow]")
spark_compute_app.command(get_published_settings_command, name="get-published-settings")
spark_compute_app.command(get_staging_settings_command, name="get-staging-settings")
spark_compute_app.command(update_staging_settings_command, name="update-staging-settings")
