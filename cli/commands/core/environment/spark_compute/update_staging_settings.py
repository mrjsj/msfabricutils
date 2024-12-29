import json
import sys
from typing import Annotated, Literal

from console import console
from cyclopts import Group, Parameter
from msfabricpysdkcore.item import Item

from msfabricutils.types import (
    ComplexType,
    SparkProperties,
)

global_args = Group(name="Global Arguments", default_parameter=Parameter(show_default=False, negative=""))


def update_staging_settings_command(
    *,
    workspace_id: str,
    environment_id: str,
    driver_cores: int,
    driver_memory: str,
    dynamic_executor_allocation: bool,
    executor_cores: int,
    executor_memory: str,
    instance_pool: str,
    runtime_version: str,
    spark_properties: SparkProperties,
    help: Annotated[bool, Parameter(group=global_args, help="Show this help and exit")] = False,
    verbose: Annotated[bool, Parameter(group=global_args, help="Show verbose output")] = False,
    debug: Annotated[bool, Parameter(group=global_args, help="Show debug output")] = False,
    output: Annotated[Literal["json", "yaml", "csv", "table"], Parameter(group=global_args, help="Output format")] = "json",
):
    """Execute update_staging_settings command

    Args:
        workspace_id (str): The ID of the workspace
        environment_id (str): The ID of the environment
        driver_cores (int): The number of driver cores
        driver_memory (str): The memory for the driver
        dynamic_executor_allocation (bool): Whether to dynamically allocate executors
        executor_cores (int): The number of executor cores
        executor_memory (str): The memory for the executor
        instance_pool (str): The instance pool
        runtime_version (str): The runtime version
        spark_properties (SparkProperties): The spark properties as JSON string
    """
    try:
        if isinstance(spark_properties, ComplexType):
            spark_properties = spark_properties.to_dict()

        # time.sleep(1)
        from msfabricpysdkcore import FabricClientCore

        client = FabricClientCore()
        result = client.update_staging_settings(
            workspace_id=workspace_id,
            environment_id=environment_id,
            driver_cores=driver_cores,
            driver_memory=driver_memory,
            dynamic_executor_allocation=dynamic_executor_allocation,
            executor_cores=executor_cores,
            executor_memory=executor_memory,
            instance_pool=instance_pool,
            runtime_version=runtime_version,
            spark_properties=spark_properties,
        )
        if isinstance(result, Item):
            result = str(result)
        if isinstance(result, dict):
            result = json.dumps(result, indent=2)
        console.print_json(result)
        sys.exit(0)
    except Exception as e:
        if debug:
            console.print_exception()
            from importlib.metadata import version

            from msfabricutils import __version__ as msfabricutils_version

            msfabricpysdkcore_version = version("msfabricpysdkcore")

            console.print("")
            console.print("[bold yellow]Dependency versions:[/bold yellow]")
            console.print(f"msfabricutils=={msfabricutils_version}")
            console.print(f"msfabricpysdkcore=={msfabricpysdkcore_version}")
            sys.exit(1)
        console.print(
            f"[bold red][Error]:[/bold red]\n{str(e)}\n\nIf this error is unexpected, please run the command again with the --debug flag\nCopy the output, and create an issue at: https://github.com/mrjsj/msfabricutils/issues"
        )
        sys.exit(1)
