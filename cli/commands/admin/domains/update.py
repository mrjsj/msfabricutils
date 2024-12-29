import json
import sys
from typing import Annotated, Literal

from console import console
from cyclopts import Group, Parameter
from msfabricpysdkcore.item import Item

global_args = Group(name="Global Arguments", default_parameter=Parameter(show_default=False, negative=""))


def update_command(
    *,
    domain_id: str,
    description: str,
    display_name: str,
    contributors_scope: Literal["AdminsOnly", "AllTenant", "SpecificUsersAndGroups"],
    return_item: bool,
    help: Annotated[bool, Parameter(group=global_args, help="Show this help and exit")] = False,
    verbose: Annotated[bool, Parameter(group=global_args, help="Show verbose output")] = False,
    debug: Annotated[bool, Parameter(group=global_args, help="Show debug output")] = False,
    output: Annotated[Literal["json", "yaml", "csv", "table"], Parameter(group=global_args, help="Output format")] = "json",
):
    """Execute update command

    Args:
        domain_id (str): The ID of the domain
        description (str): The description of the domain
        display_name (str): The display name of the domain
        contributors_scope (Literal["AdminsOnly", "AllTenant", "SpecificUsersAndGroups"]): The contributors scope of the domain
        return_item (bool): Whether to return the domain
    """
    try:
        # time.sleep(1)
        from msfabricpysdkcore import FabricClientAdmin

        client = FabricClientAdmin()
        result = client.update_domain(
            domain_id=domain_id, description=description, display_name=display_name, contributors_scope=contributors_scope, return_item=return_item
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
