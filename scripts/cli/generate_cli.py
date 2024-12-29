import os
from importlib import import_module
from pathlib import Path
from typing import Any, Dict, Literal, List, Optional
from pydantic import BaseModel, ValidationError

import yaml
import sys

import importlib

complex_types_module = importlib.import_module("msfabricutils.types")
complex_types = complex_types_module.__all__

TEMPLATE_COMMAND = '''import sys
from json import JSONDecodeError
from typing import Annotated, Literal, List
from functools import partial
import json
from console import console
from msfabricutils.types import (
    Principal,
    ItemInfo,
    ItemType,
    ConnectionRequest,
    GatewayRequest,
    GitProviderDetails,
    GitConflictResolution,
    GitUpdateOptions,
    GitUpdateCredentials,
    ItemDefinition,
    ScheduleConfig,
    ExecutionData,
    DataAccessRole,
    SparkProperties,
    CreationPayload,
    FileFormatOptions,
    PoolProperties,
    ComplexType,
    OutFile
)
import time
from msfabricutils.types.item_definition import save_item_to_path
import rich
from msfabricpysdkcore.item import Item
from cyclopts import Group, Parameter, validators
from rich.console import Console
from rich.status import Status
{groups}

global_args = Group(
    name = "Global Arguments",
    default_parameter=Parameter(show_default=False, negative="")
)

def {name}_command(
    *,
    {args}
    help: Annotated[bool, Parameter(group=global_args, help="Show this help and exit")] = False,
    verbose: Annotated[bool, Parameter(group=global_args, help="Show verbose output")] = False,
    debug: Annotated[bool, Parameter(group=global_args, help="Show debug output")] = False,
    output: Annotated[Literal["json", "none"], Parameter(group=global_args, help="Output format")] = "json"
):
    """Execute {name} command

{docstring}
    """
    
    try: 
{load_item_definition}
{complex_type_to_dict}


        
        from msfabricpysdkcore import {client_name}
        client = {client_name}()
        result = {cmd_function}(
            {function_args}
        )
{save_item_to_path}

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
            from msfabricutils import __version__ as msfabricutils_version
            from importlib.metadata import version
            msfabricpysdkcore_version = version("msfabricpysdkcore")

            rich.print("")
            rich.print("[bold yellow]Dependency versions:[/bold yellow]")
            rich.print(f"msfabricutils=={{msfabricutils_version}}")
            rich.print(f"msfabricpysdkcore=={{msfabricpysdkcore_version}}")
            sys.exit(1)
        rich.print(f"[bold red][Error]:[/bold red]\\n{{str(e)}}\\n\\nIf this error is unexpected, please run the command again with the --debug flag\\nCopy the output, and create an issue at: https://github.com/mrjsj/msfabricutils/issues")
        sys.exit(1)

'''
   

#     {item_path_str}


#     try:
#         with Status("Running ...", spinner="bouncingBall"):
#             client = FabricClient{cmd_area}()
#         rich.print_json(str(result))
#         sys.exit(0)
#     except JSONDecodeError:
#         rich.print(str(result))
#         sys.exit(0)
#     except Exception as e:
#         if debug:
#             console = Console()
#             console.print_exception()
#             sys.exit(1)
#         rich.print(f"[bold red][Error]:[/bold red]\\n{{str(e)}}\\n\\nIf this error is unexpected, please run the command again with the --debug flag\\nCopy the output, and create an issue at: https://github.com/mrjsj/msfabricutils/issues")
#         sys.exit(1)
# '''

TEMPLATE_INIT = """from cyclopts import App
{imports}

{app_name} = App(name="{name}", help="{help_text}")
{commands}
"""


def kebab_to_snake(name: str) -> str:
    return name.replace("-", "_")

def snake_to_kebab(name: str) -> str:
    return name.replace("_", "-")


class Arg(BaseModel):
    name: str
    alias: Optional[str] = None
    exclude_param: Optional[bool] = False
    description: str
    type: str
    required: Optional[bool] = True
    default: Optional[Any] = None

class Command(BaseModel):
    name: str
    description: Optional[str] = None
    function: Optional[str] = None
    args: Optional[List[Arg]] = None
    commands: Optional[List["Command"]] = None

class Area(BaseModel):
    name: str
    client: Literal["FabricClientCore", "FabricClientAdmin"]
    commands: List[Command]

class CommandsFile(BaseModel):
    areas: List[Area]



def generate_cli_structure(commands: CommandsFile, base_path: Path):
    commands_dir = base_path / "commands"
    
    if os.path.exists(commands_dir):
        shutil.rmtree(commands_dir)

    commands_dir.mkdir(exist_ok=True)

    def process_area(area: Area, area_path: Path):
        area_path.mkdir(exist_ok=True)
        
        # Create __init__.py for area
        imports = []
        command_registrations = []
        
        area_snake_case = snake_to_kebab(area.name)
        area_kebab_case = kebab_to_snake(area.name)
        
        for command in area.commands:
            command_snake_case = kebab_to_snake(command.name)
            command_kebab_case = snake_to_kebab(command.name)
            if command.commands:  # Has subcommands
                imports.append(f"from .{command_snake_case} import {command_snake_case}_app")
                command_registrations.append(f"{area_snake_case}_app.command({command_snake_case}_app)")
                # Create subcommand directory and process
                subcmd_path = area_path / command_snake_case
                process_command(command, subcmd_path, client_name=area.client)
            else:  # Leaf command
                # Put command directly in area folder
                imports.append(f"from .{command_snake_case} import {command_snake_case}_command")
                command_registrations.append(f"{area.name}_app.command({command_snake_case}_command)")
                generate_command_file(command, area_path, client_name=area.client)
        
        init_content = TEMPLATE_INIT.format(
            imports="\n".join(imports),
            app_name=f"{area_snake_case}_app",
            name=area_kebab_case,
            help_text=f"Commands for {area_snake_case}",
            commands="\n".join(command_registrations)
        )
        
        if area.name == "admin":
            return
        
        with open(area_path / "__init__.py", "w") as f:
            f.write(init_content)

    def process_command(command: Command, cmd_path: Path, client_name: Literal["FabricClientCore", "FabricClientAdmin"]):
        if cmd_path.parent.name == "admin" and command.name == "admin":
            cmd_path = cmd_path.parent

        cmd_path.mkdir(exist_ok=True)

        if cmd_path.name.endswith("deployment-pipelines"):
            a = 1

        command_snake_case = kebab_to_snake(command.name)
        command_kebab_case = snake_to_kebab(command.name)
        
        if not command.commands:  # Leaf command
            generate_command_file(command, cmd_path.parent, client_name=client_name)
            return
        
        # Has subcommands
        imports = []
        command_registrations = []
        
        for subcmd in command.commands:

            subcmd_snake_case = kebab_to_snake(subcmd.name)
            subcmd_kebab_case = snake_to_kebab(subcmd.name)
            if subcmd.commands:  # Has further subcommands
                imports.append(f"from .{subcmd_snake_case} import {subcmd_snake_case}_app")
                command_registrations.append(f"{command_snake_case}_app.command({subcmd_snake_case}_app)")
                subcmd_path = cmd_path / subcmd_snake_case
                process_command(subcmd, subcmd_path, client_name=client_name)
            else:  # Leaf command
                imports.append(f"from .{subcmd_snake_case} import {subcmd_snake_case}_command")
                command_registrations.append(f"{command_snake_case}_app.command({subcmd_snake_case}_command, name='{subcmd_kebab_case}')")
                generate_command_file(subcmd, cmd_path, client_name=client_name)
        
        init_content = TEMPLATE_INIT.format(
            imports="\n".join(imports),
            app_name=f"{command_snake_case}_app",
            name=command_kebab_case,
            help_text=command.description or f"[yellow]Commands for {command_snake_case}[/yellow]",
            commands="\n".join(command_registrations)
        )
        
        with open(cmd_path / "__init__.py", "w") as f:
            f.write(init_content)

    def generate_command_file(command: Command, parent_path: Path, client_name: Literal["FabricClientCore", "FabricClientAdmin"]):
        # if not command.args:
        #     return
        
        if parent_path.name.endswith("external_data_shares"):
            a = 1

        if command.name.startswith("list-"):
            a = 1
        command_snake_case = kebab_to_snake(command.name)
        command_kebab_case = snake_to_kebab(command.name)
        
        if command.args:
            args_str = "".join(f"{arg.alias or arg.name}: {arg.type}," for arg in command.args)
            docstring_str = "\n".join(f"        {arg.name} ({arg.type}): {arg.description}"
                                for arg in command.args)
            docstring_str = "    Args:\n" + docstring_str if docstring_str != "" else ""
            arg_dict = "{" + ", ".join(f"'{arg.name}': {arg.name}" for arg in command.args) + "}"
            function_args = ", ".join(f"{arg.name}={arg.alias or arg.name}" for arg in command.args if not arg.exclude_param)

        else:
            args_str = ""
            docstring_str = ""
            arg_dict = ""
            function_args = ""
        if command.function.startswith("partial("):
            func_parts = command.function.split("(")
            cmd_function = func_parts[0] + "(client." + func_parts[1]
        else:
            cmd_function = f"client.{command.function}"

        
        load_item_definition = "\n".join([f"        if isinstance({arg.alias or arg.name}, ItemDefinition):\n            {arg.alias or arg.name} = definition.load_from_path(format=format).to_dict()" for arg in command.args if "ItemDefinition" in arg.type])

        complex_type_to_dict_str = "\n".join([f"        if isinstance({arg.alias or arg.name}, ComplexType):\n            {arg.alias or arg.name} = {arg.alias or arg.name}.to_dict()" for arg in command.args if any(complex_type in arg.type for complex_type in complex_types) and "ItemDefinition" not in arg.type])    

        save_item_to_path_str = "\n".join([f"        save_item_to_path(result, {arg.alias or arg.name}.file_path) if {arg.alias or arg.name}.file_path else None" for arg in command.args if "OutFile" in arg.type])


        command_content = TEMPLATE_COMMAND.format(
            name=command_snake_case,
            args=args_str,
            groups="",
            imports="",
            # path=str(parent_path.relative_to(base_path)),
            docstring=docstring_str,
            # arg_dict=arg_dict
            function_args=function_args,
            client_name=client_name,
            cmd_function=cmd_function,
            complex_type_to_dict=complex_type_to_dict_str,
            load_item_definition=load_item_definition,
            save_item_to_path=save_item_to_path_str
        )
        
        with open(parent_path / f"{command_snake_case}.py", "w") as f:
            f.write(command_content)

    # Process each area
    for area in commands.areas:
        area_path = commands_dir / area.name
        process_area(area, area_path)

if __name__ == "__main__":
    import shutil # noqa
    import os # noqa
    import json # noqa
    import rich # noqa
    base_path = Path("cli")
    commands_output_path = base_path / "commands"
    if os.path.exists(commands_output_path):
        shutil.rmtree(commands_output_path)

    commands_yaml_input_path = Path("scripts/cli/sdk-funcs.yaml")
    commands_data = yaml.safe_load(open(commands_yaml_input_path))

    try:
        commands = CommandsFile.model_validate(commands_data)
    except ValidationError as e:
        raise Exception from None
        #rich.print(f"[bold red][Error]:[/bold red]\\n{{str(e)}}\\n\\nIf this error is unexpected, please run the command again with the --debug flag\\nCopy the output, and create an issue at: https://github.com/mrjsj/msfabricutils/issues")
        # sys.exit(1)
    
    rich.print([command for command in commands.areas[0].commands[0].commands if command.name == "external-data-shares"])
    generate_cli_structure(commands, base_path)