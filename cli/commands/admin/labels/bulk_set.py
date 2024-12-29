import json
import sys
from typing import Annotated, List, Literal

import rich
from cyclopts import Group, Parameter

from msfabricutils.types import (
    ComplexType,
    ItemInfo,
    Principal,
)

global_args = Group(name="Global Arguments", default_parameter=Parameter(show_default=False, negative=""))


def bulk_set_command(
    *,
    items: List[ItemInfo],
    label_id: str,
    assignment_method: Literal["Priviledged", "Standard"],
    delegated_principal: Principal,
    help: Annotated[bool, Parameter(group=global_args, help="Show this help and exit")] = False,
    verbose: Annotated[bool, Parameter(group=global_args, help="Show verbose output")] = False,
    debug: Annotated[bool, Parameter(group=global_args, help="Show debug output")] = False,
    output: Annotated[Literal["json", "none"], Parameter(group=global_args, help="Output format")] = "json",
):
    """Execute bulk_set command

    Args:
        items (List[ItemInfo]): The list of item IDs
        label_id (str): The ID of the label
        assignment_method (Literal["Priviledged", "Standard"]): The assignment method
        delegated_principal (Principal): The delegated principal
    """

    try:
        if isinstance(items, ComplexType):
            items = items.to_dict()
        if isinstance(delegated_principal, ComplexType):
            delegated_principal = delegated_principal.to_dict()

        from msfabricpysdkcore import FabricClientAdmin

        client = FabricClientAdmin()
        result = client.bulk_set_labels(items=items, label_id=label_id, assignment_method=assignment_method, delegated_principal=delegated_principal)

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
