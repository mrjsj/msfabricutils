import json
import sys
from typing import Annotated, Literal

from console import console
from cyclopts import Group, Parameter
from msfabricpysdkcore.item import Item

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
    output: Annotated[Literal["json", "yaml", "csv", "table"], Parameter(group=global_args, help="Output format")] = "json",
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
        # time.sleep(1)
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
