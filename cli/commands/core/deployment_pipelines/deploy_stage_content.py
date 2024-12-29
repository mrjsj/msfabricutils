import json
import sys
from typing import Annotated, Literal

import rich
from cyclopts import Group, Parameter

global_args = Group(name="Global Arguments", default_parameter=Parameter(show_default=False, negative=""))


def deploy_stage_content_command(
    *,
    deployment_pipeline_id: str,
    source_stage_id: str,
    target_stage_id: str,
    created_workspace_details: list,
    items: list,
    note: str,
    wait_for_completion: bool,
    help: Annotated[bool, Parameter(group=global_args, help="Show this help and exit")] = False,
    verbose: Annotated[bool, Parameter(group=global_args, help="Show verbose output")] = False,
    debug: Annotated[bool, Parameter(group=global_args, help="Show debug output")] = False,
    output: Annotated[Literal["json", "none"], Parameter(group=global_args, help="Output format")] = "json",
):
    """Execute deploy_stage_content command

    Args:
        deployment_pipeline_id (str): The ID of the deployment pipeline
        source_stage_id (str): The ID of the source stage
        target_stage_id (str): The ID of the target stage
        created_workspace_details (list): A list of created workspace details
        items (list): A list of items
        note (str): A note
        wait_for_completion (bool): Whether to wait for the deployment to complete
    """

    try:
        from msfabricpysdkcore import FabricClientCore

        client = FabricClientCore()
        result = client.deploy_stage_content(
            deployment_pipeline_id=deployment_pipeline_id,
            source_stage_id=source_stage_id,
            target_stage_id=target_stage_id,
            created_workspace_details=created_workspace_details,
            items=items,
            note=note,
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
