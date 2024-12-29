import json
import sys
from typing import Annotated, List, Literal

from console import console
from cyclopts import Group, Parameter
from msfabricpysdkcore.item import Item

from msfabricutils.types import (
    ComplexType,
    Principal,
)

global_args = Group(name="Global Arguments", default_parameter=Parameter(show_default=False, negative=""))


def bulk_assign_role_assignments_command(
    *,
    domain_id: str,
    type: Literal["Admins", "Contributors"],
    principals: List[Principal],
    help: Annotated[bool, Parameter(group=global_args, help="Show this help and exit")] = False,
    verbose: Annotated[bool, Parameter(group=global_args, help="Show verbose output")] = False,
    debug: Annotated[bool, Parameter(group=global_args, help="Show debug output")] = False,
    output: Annotated[Literal["json", "yaml", "csv", "table"], Parameter(group=global_args, help="Output format")] = "json",
):
    """Execute bulk_assign_role_assignments command

    Args:
        domain_id (str): The ID of the domain
        type (Literal["Admins", "Contributors"]): The type of the role assignment
        principals (List[Principal]): The list of principals
    """
    try:
        if isinstance(principals, ComplexType):
            principals = principals.to_dict()

        # time.sleep(1)
        from msfabricpysdkcore import FabricClientAdmin

        client = FabricClientAdmin()
        result = client.role_assignments_bulk_assign(domain_id=domain_id, type=type, principals=principals)
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
