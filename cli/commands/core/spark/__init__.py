from cyclopts import App

from .custom_pools import custom_pools_app
from .spark_settings import spark_settings_app

spark_app = App(name="spark", help="[yellow]Commands for spark[/yellow]")
spark_app.command(custom_pools_app)
spark_app.command(spark_settings_app)
