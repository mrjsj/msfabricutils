import json
import sys
from typing import Annotated, Literal

from console import console
from cyclopts import Group, Parameter
from msfabricpysdkcore.item import Item

from msfabricutils.types import (
    ComplexType,
    DataAccessRole,
)

global_args = Group(name="Global Arguments", default_parameter=Parameter(show_default=False, negative=""))


def create_or_update_data_access_roles_command(
    *,
    workspace_id: str,
    item_id: str,
    data_access_roles: DataAccessRole,
    dry_run: bool,
    etag_match: Literal["If-Match", "If-None-Match"],
    help: Annotated[bool, Parameter(group=global_args, help="Show this help and exit")] = False,
    verbose: Annotated[bool, Parameter(group=global_args, help="Show verbose output")] = False,
    debug: Annotated[bool, Parameter(group=global_args, help="Show debug output")] = False,
    output: Annotated[Literal["json", "yaml", "csv", "table"], Parameter(group=global_args, help="Output format")] = "json",
):
    """Execute create_or_update_data_access_roles command

    Args:
        workspace_id (str): The ID of the workspace
        item_id (str): The ID of the item
        data_access_roles (DataAccessRole): json string or json file path in format of list of DataAccessRole. If json string, quotes must be escaped, e.g. {\\"key\\": \\\"value\\"}
        dryrun (bool): Whether to run a dry run
        etag_match (Literal["If-Match", "If-None-Match"]): The etag match
    """
    try:
        if isinstance(data_access_roles, ComplexType):
            data_access_roles = data_access_roles.to_dict()

        # time.sleep(1)
        from msfabricpysdkcore import FabricClientCore

        client = FabricClientCore()
        result = client.create_or_update_data_access_roles(
            workspace_id=workspace_id, item_id=item_id, data_access_roles=data_access_roles, dryrun=dry_run, etag_match=etag_match
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
