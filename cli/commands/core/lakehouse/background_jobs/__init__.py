from cyclopts import App

from .run_on_demand_table_maintenance import run_on_demand_table_maintenance_command

background_jobs_app = App(name="background-jobs", help="[yellow]Commands for background_jobs[/yellow]")
background_jobs_app.command(run_on_demand_table_maintenance_command, name="run-on-demand-table-maintenance")
