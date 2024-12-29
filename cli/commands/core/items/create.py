import json
import sys
from typing import Annotated, Literal

from console import console
from cyclopts import Group, Parameter
from msfabricpysdkcore.item import Item

from msfabricutils.types import (
    ComplexType,
    ItemDefinition,
    ItemType,
)

global_args = Group(name="Global Arguments", default_parameter=Parameter(show_default=False, negative=""))


def create_command(
    *,
    workspace_id: str,
    display_name: str,
    type: ItemType,
    definition: ItemDefinition,
    format: Annotated[str, Parameter(help="The format of the item")],
    description: str,
    wait_for_completion: bool,
    help: Annotated[bool, Parameter(group=global_args, help="Show this help and exit")] = False,
    verbose: Annotated[bool, Parameter(group=global_args, help="Show verbose output")] = False,
    debug: Annotated[bool, Parameter(group=global_args, help="Show debug output")] = False,
    output: Annotated[Literal["json", "yaml", "csv", "table"], Parameter(group=global_args, help="Output format")] = "json",
):
    """Execute create command

    Args:
        workspace_id (str): The ID of the workspace
        display_name (str): The display name of the item
        type (ItemType): The type of the item
        definition (ItemDefinition): The definition of the item
        format (Annotated[str, Parameter(help="The format of the item")]): The format of the item
        description (str): The description of the item
        wait_for_completion (bool): Whether to wait for the item to be created
    """
    try:
        if isinstance(definition, ItemDefinition):
            definition = ItemDefinition.from_path(path=definition, format=format).to_dict()
        if isinstance(type, ComplexType):
            type = type.to_dict()

        # time.sleep(1)
        from msfabricpysdkcore import FabricClientCore

        client = FabricClientCore()
        result = client.create_item(
            workspace_id=workspace_id,
            display_name=display_name,
            type=type,
            definition=definition,
            description=description,
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
