import json
import sys
from typing import Annotated, List, Literal

import rich
from cyclopts import Group, Parameter

from msfabricutils.types import (
    ComplexType,
    Principal,
)

global_args = Group(name="Global Arguments", default_parameter=Parameter(show_default=False, negative=""))


def assign_workspaces_by_principals_command(
    *,
    domain_id: str,
    principals: List[Principal],
    wait_for_completion: bool,
    help: Annotated[bool, Parameter(group=global_args, help="Show this help and exit")] = False,
    verbose: Annotated[bool, Parameter(group=global_args, help="Show verbose output")] = False,
    debug: Annotated[bool, Parameter(group=global_args, help="Show debug output")] = False,
    output: Annotated[Literal["json", "none"], Parameter(group=global_args, help="Output format")] = "json",
):
    """Execute assign_workspaces_by_principals command

    Args:
        domain_id (str): The ID of the domain
        principals (List[Principal]): The list of principal IDs
        wait_for_completion (bool): Whether to wait for the operation to complete
    """

    try:
        if isinstance(principals, ComplexType):
            principals = principals.to_dict()

        from msfabricpysdkcore import FabricClientAdmin

        client = FabricClientAdmin()
        result = client.assign_domains_workspaces_by_principals(domain_id=domain_id, principals=principals, wait_for_completion=wait_for_completion)

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
