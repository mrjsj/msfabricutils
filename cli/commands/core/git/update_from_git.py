import json
import sys
from typing import Annotated, Literal

import rich
from cyclopts import Group, Parameter

from msfabricutils.types import (
    ComplexType,
    GitConflictResolution,
    GitUpdateOptions,
)

global_args = Group(name="Global Arguments", default_parameter=Parameter(show_default=False, negative=""))


def update_from_git_command(
    *,
    workspace_id: str,
    remote_commit_hash: str,
    conflict_resolution: Annotated[GitConflictResolution, Parameter(name="*")],
    options: Annotated[GitUpdateOptions, Parameter(name="*")],
    workspace_head: str,
    help: Annotated[bool, Parameter(group=global_args, help="Show this help and exit")] = False,
    verbose: Annotated[bool, Parameter(group=global_args, help="Show verbose output")] = False,
    debug: Annotated[bool, Parameter(group=global_args, help="Show debug output")] = False,
    output: Annotated[Literal["json", "none"], Parameter(group=global_args, help="Output format")] = "json",
):
    """Execute update_from_git command

    Args:
        workspace_id (str): The ID of the workspace
        remote_commit_hash (str): The remote commit hash
        conflict_resolution (Annotated[GitConflictResolution, Parameter(name="*")]): The conflict resolution
        options (Annotated[GitUpdateOptions, Parameter(name="*")]):
        workspace_head (str): The workspace head
    """

    try:
        if isinstance(conflict_resolution, ComplexType):
            conflict_resolution = conflict_resolution.to_dict()
        if isinstance(options, ComplexType):
            options = options.to_dict()

        from msfabricpysdkcore import FabricClientCore

        client = FabricClientCore()
        result = client.update_from_git(
            workspace_id=workspace_id,
            remote_commit_hash=remote_commit_hash,
            conflict_resolution=conflict_resolution,
            options=options,
            workspace_head=workspace_head,
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
