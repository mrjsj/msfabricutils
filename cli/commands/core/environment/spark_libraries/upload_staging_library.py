import json
import sys
from typing import Annotated, Literal

import rich
from cyclopts import Group, Parameter

global_args = Group(name="Global Arguments", default_parameter=Parameter(show_default=False, negative=""))


def upload_staging_library_command(
    *,
    workspace_id: str,
    environment_id: str,
    file_path: str,
    help: Annotated[bool, Parameter(group=global_args, help="Show this help and exit")] = False,
    verbose: Annotated[bool, Parameter(group=global_args, help="Show verbose output")] = False,
    debug: Annotated[bool, Parameter(group=global_args, help="Show debug output")] = False,
    output: Annotated[Literal["json", "none"], Parameter(group=global_args, help="Output format")] = "json",
):
    """Execute upload_staging_library command

    Args:
        workspace_id (str): The ID of the workspace
        environment_id (str): The ID of the environment
        file_path (str): The file path to upload
    """

    try:
        from msfabricpysdkcore import FabricClientCore

        client = FabricClientCore()
        result = client.upload_staging_library(workspace_id=workspace_id, environment_id=environment_id, file_path=file_path)

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
