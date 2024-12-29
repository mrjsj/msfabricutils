import json
import sys
from typing import Annotated, Literal

import rich
from cyclopts import Group, Parameter

global_args = Group(name="Global Arguments", default_parameter=Parameter(show_default=False, negative=""))


def update_command(
    *,
    workspace_id: str,
    pool_id: str,
    name: str,
    node_family: str,
    node_size: str,
    auto_scale: bool,
    dynamic_executor_allocation: bool,
    return_item: bool,
    help: Annotated[bool, Parameter(group=global_args, help="Show this help and exit")] = False,
    verbose: Annotated[bool, Parameter(group=global_args, help="Show verbose output")] = False,
    debug: Annotated[bool, Parameter(group=global_args, help="Show debug output")] = False,
    output: Annotated[Literal["json", "none"], Parameter(group=global_args, help="Output format")] = "json",
):
    """Execute update command

    Args:
        workspace_id (str): The ID of the workspace
        pool_id (str): The ID of the pool
        name (str): The name of the pool
        node_family (str): The node family
        node_size (str): The node size
        auto_scale (bool): Whether to auto scale
        dynamic_executor_allocation (bool): Whether to use dynamic executor allocation
        return_item (bool): Whether to return the item
    """

    try:
        from msfabricpysdkcore import FabricClientCore

        client = FabricClientCore()
        result = client.update_workspace_custom_pool(
            workspace_id=workspace_id,
            pool_id=pool_id,
            name=name,
            node_family=node_family,
            node_size=node_size,
            auto_scale=auto_scale,
            dynamic_executor_allocation=dynamic_executor_allocation,
            return_item=return_item,
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
