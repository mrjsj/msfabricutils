from typing import Literal

ItemType = Literal[
    "Dashboard",
    "DataPipeline",
    "Datamart",
    "Environment",
    "Eventhouse",
    "Eventstream",
    "KQLDashboard",
    "KQLDatabase",
    "KQLQueryset",
    "Lakehouse",
    "MLExperiment",
    "MLModel",
    "MirroredDatabase",
    "MirroredWarehouse",
    "Notebook",
    "PaginatedReport",
    "Reflex",
    "Report",
    "SQLEndpoint",
    "SemanticModel",
    "SparkJobDefinition",
    "Warehouse"
]