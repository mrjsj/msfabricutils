from cyclopts import App

from .capacities import capacities_app
from .connections import connections_app
from .dashboard import dashboard_app
from .data_pipeline import data_pipeline_app
from .datamart import datamart_app
from .deployment_pipelines import deployment_pipelines_app
from .environment import environment_app
from .eventhouse import eventhouse_app
from .eventstream import eventstream_app
from .external_data_shares import external_data_shares_app
from .gateways import gateways_app
from .git import git_app
from .items import items_app
from .job_scheduler import job_scheduler_app
from .kql_dashboard import kql_dashboard_app
from .kql_database import kql_database_app
from .kql_queryset import kql_queryset_app
from .lakehouse import lakehouse_app
from .long_running_operations import long_running_operations_app
from .managed_private_endpoints import managed_private_endpoints_app
from .mirrored_database import mirrored_database_app
from .mirrored_warehouse import mirrored_warehouse_app
from .ml_experiment import ml_experiment_app
from .ml_model import ml_model_app
from .notebook import notebook_app
from .one_lake_data_access_security import one_lake_data_access_security_app
from .one_lake_shortcuts import one_lake_shortcuts_app
from .paginated_report import paginated_report_app
from .report import report_app
from .semantic_model import semantic_model_app
from .spark import spark_app
from .spark_job_definition import spark_job_definition_app
from .sql_endpoint import sql_endpoint_app
from .warehouse import warehouse_app
from .workspaces import workspaces_app

core_app = App(name="core", help="Commands for core")
core_app.command(capacities_app)
core_app.command(connections_app)
core_app.command(deployment_pipelines_app)
core_app.command(external_data_shares_app)
core_app.command(gateways_app)
core_app.command(git_app)
core_app.command(items_app)
core_app.command(job_scheduler_app)
core_app.command(long_running_operations_app)
core_app.command(managed_private_endpoints_app)
core_app.command(one_lake_data_access_security_app)
core_app.command(one_lake_shortcuts_app)
core_app.command(workspaces_app)
core_app.command(dashboard_app)
core_app.command(datamart_app)
core_app.command(data_pipeline_app)
core_app.command(environment_app)
core_app.command(eventhouse_app)
core_app.command(eventstream_app)
core_app.command(kql_dashboard_app)
core_app.command(kql_database_app)
core_app.command(kql_queryset_app)
core_app.command(lakehouse_app)
core_app.command(mirrored_database_app)
core_app.command(mirrored_warehouse_app)
core_app.command(ml_experiment_app)
core_app.command(ml_model_app)
core_app.command(notebook_app)
core_app.command(paginated_report_app)
core_app.command(report_app)
core_app.command(semantic_model_app)
core_app.command(spark_app)
core_app.command(spark_job_definition_app)
core_app.command(sql_endpoint_app)
core_app.command(warehouse_app)
