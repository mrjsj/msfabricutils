import json
import sys
from typing import Annotated, Literal

import rich
from cyclopts import Group, Parameter

from msfabricutils.types import (
    ComplexType,
    ExecutionData,
)

global_args = Group(name="Global Arguments", default_parameter=Parameter(show_default=False, negative=""))


def run_on_demand_table_maintenance_command(
    *,
    workspace_id: str,
    lakehouse_id: str,
    execution_data: Annotated[ExecutionData, Parameter(name="*")],
    job_type: Literal["TableMaintenance"],
    wait_for_completion: bool,
    help: Annotated[bool, Parameter(group=global_args, help="Show this help and exit")] = False,
    verbose: Annotated[bool, Parameter(group=global_args, help="Show verbose output")] = False,
    debug: Annotated[bool, Parameter(group=global_args, help="Show debug output")] = False,
    output: Annotated[Literal["json", "none"], Parameter(group=global_args, help="Output format")] = "json",
):
    """Execute run_on_demand_table_maintenance command

    Args:
        workspace_id (str): The ID of the workspace
        lakehouse_id (str): The ID of the lakehouse
        execution_data (Annotated[ExecutionData, Parameter(name="*")]): The execution data
        job_type (Literal["TableMaintenance"]): The job type
        wait_for_completion (bool): Whether to wait for the operation to complete
    """

    try:
        if isinstance(execution_data, ComplexType):
            execution_data = execution_data.to_dict()

        from msfabricpysdkcore import FabricClientCore

        client = FabricClientCore()
        result = client.run_on_demand_table_maintenance(
            workspace_id=workspace_id,
            lakehouse_id=lakehouse_id,
            execution_data=execution_data,
            job_type=job_type,
            wait_for_completion=wait_for_completion,
        )

        if output == "none":
            sys.exit(0)

        # Not pretty
        if isinstance(result, list):
            result = [json.loads(str(item)) for item in result]
            result = json.dumps(result)
        elif isinstance(result, dict):
            result = str(result)

        rich.print_json(result)
        sys.exit(0)
    except Exception as e:
        if debug:
            from rich.console import Console

            console = Console()
            console.print_exception()
            from importlib.metadata import version

            from msfabricutils import __version__ as msfabricutils_version

            msfabricpysdkcore_version = version("msfabricpysdkcore")

            rich.print("")
            rich.print("[bold yellow]Dependency versions:[/bold yellow]")
            rich.print(f"msfabricutils=={msfabricutils_version}")
            rich.print(f"msfabricpysdkcore=={msfabricpysdkcore_version}")
            sys.exit(1)
        rich.print(
            f"[bold red][Error]:[/bold red]\n{str(e)}\n\nIf this error is unexpected, please run the command again with the --debug flag\nCopy the output, and create an issue at: https://github.com/mrjsj/msfabricutils/issues"
        )
        sys.exit(1)
