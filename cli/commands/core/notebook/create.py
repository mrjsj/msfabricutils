import json
import sys
from typing import Annotated, Literal

import rich
from cyclopts import Group, Parameter

from msfabricutils.types import (
    ItemDefinition,
)

global_args = Group(name="Global Arguments", default_parameter=Parameter(show_default=False, negative=""))


def create_command(
    *,
    workspace_id: str,
    display_name: str,
    definition: Annotated[ItemDefinition, Parameter(name="*")],
    format: Annotated[Literal["ipynb"], Parameter(help="The format of the notebook")] = None,
    description: str,
    help: Annotated[bool, Parameter(group=global_args, help="Show this help and exit")] = False,
    verbose: Annotated[bool, Parameter(group=global_args, help="Show verbose output")] = False,
    debug: Annotated[bool, Parameter(group=global_args, help="Show debug output")] = False,
    output: Annotated[Literal["json", "none"], Parameter(group=global_args, help="Output format")] = "json",
):
    """Execute create command

    Args:
        workspace_id (str): The ID of the workspace
        display_name (str): The display name of the notebook
        definition (Annotated[ItemDefinition, Parameter(name="*")]): The definition of the notebook
        format (Annotated[Literal["ipynb"], Parameter(help="The format of the notebook")] = None): The format of the notebook
        description (str): The description of the notebook
    """

    try:
        if isinstance(definition, ItemDefinition):
            definition = definition.load_from_path(format=format).to_dict()

        from msfabricpysdkcore import FabricClientCore

        client = FabricClientCore()
        result = client.create_notebook(workspace_id=workspace_id, display_name=display_name, definition=definition, description=description)

        if output == "none":
            sys.exit(0)

        # Not pretty
        if isinstance(result, list):
            result = [json.loads(str(item)) for item in result]
            result = json.dumps(result)
        else:
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
