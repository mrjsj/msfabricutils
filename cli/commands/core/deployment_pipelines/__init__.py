from cyclopts import App

from .deploy_stage_content import deploy_stage_content_command
from .get import get_command
from .list_deployment_pipelines import list_deployment_pipelines_command
from .list_stage_items import list_stage_items_command
from .list_stages import list_stages_command

deployment_pipelines_app = App(name="deployment-pipelines", help="[yellow]Commands for deployment_pipelines[/yellow]")
deployment_pipelines_app.command(deploy_stage_content_command, name="deploy-stage-content")
deployment_pipelines_app.command(get_command, name="get")
deployment_pipelines_app.command(list_stage_items_command, name="list-stage-items")
deployment_pipelines_app.command(list_stages_command, name="list-stages")
deployment_pipelines_app.command(list_deployment_pipelines_command, name="list-deployment-pipelines")
