import json
import sys
from typing import Annotated, Literal

from console import console
from cyclopts import Group, Parameter
from msfabricpysdkcore.item import Item

from msfabricutils.types import (
    ComplexType,
    FileFormatOptions,
)

global_args = Group(name="Global Arguments", default_parameter=Parameter(show_default=False, negative=""))


def load_command(
    *,
    workspace_id: str,
    lakehouse_id: str,
    table_name: str,
    path_type: str,
    relative_path: str,
    file_extension: str,
    format_options: Annotated[FileFormatOptions, Parameter(name="*")],
    mode: Literal["Append", "Overwrite"],
    recursive: bool,
    wait_for_completion: bool,
    help: Annotated[bool, Parameter(group=global_args, help="Show this help and exit")] = False,
    verbose: Annotated[bool, Parameter(group=global_args, help="Show verbose output")] = False,
    debug: Annotated[bool, Parameter(group=global_args, help="Show debug output")] = False,
    output: Annotated[Literal["json", "yaml", "csv", "table"], Parameter(group=global_args, help="Output format")] = "json",
):
    """Execute load command

    Args:
        workspace_id (str): The ID of the workspace
        lakehouse_id (str): The ID of the lakehouse
        table_name (str): The name of the table
        path_type (str): The path type
        relative_path (str): The relative path
        file_extension (str): The file extension
        format_options (Annotated[FileFormatOptions, Parameter(name="*")]): The format options
        mode (Literal["Append", "Overwrite"]): The mode
        recursive (bool): Whether to load recursively
        wait_for_completion (bool): Whether to wait for the operation to complete
    """
    try:
        if isinstance(format_options, ComplexType):
            format_options = format_options.to_dict()

        # time.sleep(1)
        from msfabricpysdkcore import FabricClientCore

        client = FabricClientCore()
        result = client.load_table(
            workspace_id=workspace_id,
            lakehouse_id=lakehouse_id,
            table_name=table_name,
            path_type=path_type,
            relative_path=relative_path,
            file_extension=file_extension,
            format_options=format_options,
            mode=mode,
            recursive=recursive,
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
