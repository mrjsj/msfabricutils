from .capacity import app as capacity_app
from .dashboard import app as dashboard_app
from .data_pipeline import app as data_pipeline_app
from .datamart import app as datamart_app
from .environment import app as environment_app
from .eventhouse import app as eventhouse_app
from .eventstream import app as eventstream_app
from .kql_dashboard import app as kql_dashboard_app
from .kql_database import app as kql_database_app
from .kql_queryset import app as kql_queryset_app
from .lakehouse import app as lakehouse_app
from .long_running_operation import app as long_running_operation_app
from .mirrored_database import app as mirrored_database_app
from .mirrored_warehouse import app as mirrored_warehouse_app
from .ml_experiment import app as ml_experiment_app
from .ml_model import app as ml_model_app
from .notebook import app as notebook_app
from .paginated_report import app as paginated_report_app
from .reflex import app as reflex_app
from .report import app as report_app
from .semantic_model import app as semantic_model_app
from .spark_job_definition import app as spark_job_definition_app
from .sql_endpoint import app as sql_endpoint_app
from .warehouse import app as warehouse_app
from .workspace import app as workspace_app

COMMANDS = {
    "capacity": capacity_app,
    "dashboard": dashboard_app,
    "data-pipeline": data_pipeline_app,
    "datamart": datamart_app,
    "environment": environment_app,
    "eventhouse": eventhouse_app,
    "eventstream": eventstream_app,
    "kql-dashboard": kql_dashboard_app,
    "kql-database": kql_database_app,
    "kql-queryset": kql_queryset_app,
    "lakehouse": lakehouse_app,
    "long-running-operation": long_running_operation_app,
    "mirrored-database": mirrored_database_app,
    "mirrored-warehouse": mirrored_warehouse_app,
    "ml-experiment": ml_experiment_app,
    "ml-model": ml_model_app,
    "notebook": notebook_app,
    "paginated-report": paginated_report_app,
    "reflex": reflex_app,
    "report": report_app,
    "semantic-model": semantic_model_app,
    "spark-job-definition": spark_job_definition_app,
    "sql-endpoint": sql_endpoint_app,
    "warehouse": warehouse_app,
    "workspace": workspace_app,
}
