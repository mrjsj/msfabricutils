from cyclopts import App

from .cancel_item_job_instance import cancel_item_job_instance_command
from .create_item_schedule import create_item_schedule_command
from .get_item_job_instance import get_item_job_instance_command
from .get_item_schedule import get_item_schedule_command
from .list_item_job_instances import list_item_job_instances_command
from .list_item_schedules import list_item_schedules_command
from .run_on_demand_item_job import run_on_demand_item_job_command
from .update_item_schedule import update_item_schedule_command

job_scheduler_app = App(name="job-scheduler", help="[yellow]Commands for job_scheduler[/yellow]")
job_scheduler_app.command(cancel_item_job_instance_command, name="cancel-item-job-instance")
job_scheduler_app.command(create_item_schedule_command, name="create-item-schedule")
job_scheduler_app.command(get_item_job_instance_command, name="get-item-job-instance")
job_scheduler_app.command(get_item_schedule_command, name="get-item-schedule")
job_scheduler_app.command(list_item_job_instances_command, name="list-item-job-instances")
job_scheduler_app.command(list_item_schedules_command, name="list-item-schedules")
job_scheduler_app.command(run_on_demand_item_job_command, name="run-on-demand-item-job")
job_scheduler_app.command(update_item_schedule_command, name="update-item-schedule")
