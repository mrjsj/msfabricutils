import json
import sys
from functools import partial
from typing import Annotated, Literal

import rich
from cyclopts import Group, Parameter

from msfabricutils.types import (
    ComplexType,
    OutFile,
)
from msfabricutils.types.item_definition import save_item_to_path

global_args = Group(name="Global Arguments", default_parameter=Parameter(show_default=False, negative=""))


def get_definition_command(
    *,
    workspace_id: str,
    kql_database_id: str,
    item_path: Annotated[OutFile, Parameter(name="*")],
    format: str,
    help: Annotated[bool, Parameter(group=global_args, help="Show this help and exit")] = False,
    verbose: Annotated[bool, Parameter(group=global_args, help="Show verbose output")] = False,
    debug: Annotated[bool, Parameter(group=global_args, help="Show debug output")] = False,
    output: Annotated[Literal["json", "none"], Parameter(group=global_args, help="Output format")] = "json",
):
    """Execute get_definition command

    Args:
        workspace_id (str): The ID of the workspace
        item_id (str): The ID of the kql database
        item_path (Annotated[OutFile, Parameter(name="*")]): The path of the item
        format (str): The format of the kql database
    """

    try:
        if isinstance(item_path, ComplexType):
            item_path = item_path.to_dict()

        from msfabricpysdkcore import FabricClientCore

        client = FabricClientCore()
        result = partial(client.get_item_definition, type="kqlDatabases")(workspace_id=workspace_id, item_id=kql_database_id, format=format)
        save_item_to_path(result, item_path.file_path) if item_path.file_path else None

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
