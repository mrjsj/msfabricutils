import json
import sys
from typing import Annotated, Literal

from console import console
from cyclopts import Group, Parameter
from msfabricpysdkcore.item import Item

from msfabricutils.types import (
    ItemDefinition,
)

global_args = Group(name="Global Arguments", default_parameter=Parameter(show_default=False, negative=""))


def update_definition_command(
    *,
    workspace_id: str,
    mirrored_database_id: str,
    definition: ItemDefinition,
    help: Annotated[bool, Parameter(group=global_args, help="Show this help and exit")] = False,
    verbose: Annotated[bool, Parameter(group=global_args, help="Show verbose output")] = False,
    debug: Annotated[bool, Parameter(group=global_args, help="Show debug output")] = False,
    output: Annotated[Literal["json", "yaml", "csv", "table"], Parameter(group=global_args, help="Output format")] = "json",
):
    """Execute update_definition command

    Args:
        workspace_id (str): The ID of the workspace
        mirrored_database_id (str): The ID of the mirrored database
        definition (ItemDefinition): The definition of the mirrored database
    """
    try:
        if isinstance(definition, ItemDefinition):
            definition = ItemDefinition.from_path(path=definition, format=format).to_dict()

        # time.sleep(1)
        from msfabricpysdkcore import FabricClientCore

        client = FabricClientCore()
        result = client.update_mirrored_database_definition(
            workspace_id=workspace_id, mirrored_database_id=mirrored_database_id, definition=definition
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
