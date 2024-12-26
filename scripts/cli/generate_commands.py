import os
import re
from enum import Enum
from typing import Any, Dict, List, Optional

from jinja2 import Template
from pydantic import BaseModel, field_validator
from yaml import safe_load

BASE_URL = "https://api.fabric.microsoft.com/v1"


class ArgType(str, Enum):
    PAYLOAD = "payload"
    PATH = "path"
    QUERY = "query"
    LRO = "lro"
    LOAD_CONTENT = "load_content"
    SAVE_CONTENT = "save_content"


class Type(str, Enum):
    STRING = "str"
    BOOLEAN = "bool"
    INTEGER = "int"


class Method(str, Enum):
    GET = "get"
    POST = "post"
    PATCH = "patch"
    DELETE = "delete"


class SubcommandArg(BaseModel):
    name: str
    type: str
    description: str
    required: Optional[bool] = None
    arg_type: Optional[ArgType] = None
    arg_group_type_id: Optional[str] = None
    default: Optional[Any] = None

    @field_validator("name")
    def validate_name(cls, v):
        if not re.match(r"^[a-z-]+$", v):
            raise ValueError("name must contain only lowercase letters and hyphens")
        return v

    @field_validator("description")
    def validate_description(cls, v):
        if not v[-1] == ".":
            raise ValueError("description must end with a period")
        return v


class CustomPayload(BaseModel):
    condition: Optional[str] = None
    value: str


class Subcommand(BaseModel):
    endpoint: str
    method: str
    description: str
    panel: str
    args: List[SubcommandArg]
    custom_payload: Optional[CustomPayload] = None

    @field_validator("description")
    def validate_description(cls, v):
        if not v[-1] == ".":
            raise ValueError("description must end with a period")
        return v


class Command(BaseModel):
    command: str
    subcommands: Dict[str, Subcommand]


api_template = """
import json
import logging
from uuid import UUID
from typing import List
from msfabricutils.enums import PrincipalType, WorkspaceRole

import logging
import base64
import requests
import typer
from typing_extensions import Annotated

from msfabricutils import get_fabric_bearer_token
from msfabricutils.core.operations import wait_for_long_running_operation
from msfabricutils.common.remove_none import remove_none
from msfabricutils.common.shorten_dict_values import shorten_dict_values
{%- for name, subcommand in subcommands.items() %}

def {{ module_name | replace('-', '_') }}_{{ name | replace('-', '_') }}(
    {%- for arg in subcommand.args %}
    {{ arg.snake_case }}: {{ arg.type.split('|')[1] if '|' in arg.type else arg.type }}{{ ' = None' if not arg.required else '' }},
    {%- endfor %}
    {%- for arg in subcommand.args if arg.arg_type == 'lro' %}
    timeout: int = 60 * 5,
    {%- endfor %}    
    preview: bool = True,
) -> requests.Response:
    \"\"\"
    {{ subcommand.description }}

    Args:
    {%- for arg in subcommand.args %}
        {{ arg.snake_case }} ({{ (arg.type.split('|')[1] if '|' in arg.type else arg.type).strip() }}{{ ' | None' if not arg.required else '' }}): {{ arg.description }}
    {%- endfor %}
    {%- for arg in subcommand.args if arg.arg_type == 'lro' %}
        timeout (int): Timeout for the long running operation (seconds). Defaults to 5 minutes.
    {%- endfor %}
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    \"\"\"

    url = f"{{ base_url.strip('/') }}/{{ subcommand.endpoint.strip('/') }}" # noqa
    url = f"{url}?"
    {%- for arg in subcommand.args if arg.arg_type == 'query' %}
    if {{ arg.snake_case }} is not None:
        url = f"{url}{{arg.camel_case}}={% raw %}{{% endraw %}{{arg.snake_case}}{% raw %}}{% endraw %}&"
    {%- endfor %}
    url = url.rstrip('&?')    
    
    method = "{{ subcommand.method }}"
    token = get_fabric_bearer_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    {%- for arg in subcommand.args if arg.arg_type == 'load_content' %}
    {%- for content_file in arg.content_files %}

    with open({{ arg.snake_case }}.rstrip('/') + "/{{ content_file }}", "r") as f:
        {{ content_file.strip('.').split('.')[0].replace('-', '_') }} = base64.b64encode(f.read().encode()).decode()
    {%- endfor %}

    {%- endfor %}

    data = {}
    {%- for arg in subcommand.args if arg.arg_type == 'payload' %}
    data["{{ arg.camel_case }}"] = {{ arg.snake_case }}
    {%- endfor %}
    {%- if subcommand.custom_payload %}
    {%- if subcommand.custom_payload.condition %}
    if {{ subcommand.custom_payload.condition }}:
        custom_payload = {
            {{subcommand.custom_payload.value | trim}}
        }
        data = {
            **data,
            **custom_payload
        }
    {%- else %}
    custom_payload = {
        {{subcommand.custom_payload.value | trim}}}
    data = {
        **data,
        **custom_payload
    }
    {%- endif %}
    {%- endif %}

    data = remove_none(data)

    if preview:
        typer.echo(f"Method:\\n{method.upper()}\\n")
        typer.echo(f"URL:\\n{url}\\n")
        typer.echo(f"Data:\\n{json.dumps(shorten_dict_values(data, 35), indent=2)}\\n")
        typer.echo(f"Headers:\\n{json.dumps(shorten_dict_values(headers, 35), indent=2)}\\n")
        typer.confirm("Do you want to run the command?", abort=True)

    response = requests.request(method=method, url=url, json=data, headers=headers)
    # response.raise_for_status()
    
    match response.status_code:
        case 200 | 201:
            return response
        {%- for arg in subcommand.args if arg.arg_type == 'lro' %}
        case 202:
            if {{ arg.snake_case }} is True:
                operation_id = response.headers["x-ms-operation-id"]
                retry_after = response.headers["Retry-After"]
                return wait_for_long_running_operation(
                    operation_id=operation_id,
                    retry_after=retry_after,
                    timeout=timeout
                )
            return response
        {%- endfor %}
        case _:
            return response

{%- endfor %}
""".strip()

command_template = """
import json
import logging
from uuid import UUID
from typing import List
from msfabricutils.enums import PrincipalType, WorkspaceRole

import requests
import typer
from typing_extensions import Annotated

from msfabricutils import get_fabric_bearer_token
from msfabricutils.core.operations import wait_for_long_running_operation
from msfabricutils.common.remove_none import remove_none
{%- for name, subcommand in subcommands.items() %}
from msfabricutils.rest_api import {{ module_name | replace('-', '_') }}_{{ name | replace('-', '_') }}
{%- endfor %}

app = typer.Typer(
    help="[bold]{{ (subcommands.keys() | list)[:5] | join(', ') }}[/bold]",
    rich_markup_mode="rich",
)


{%- for name, subcommand in subcommands.items() %}

@app.command(help="{{ subcommand.description }}", rich_help_panel="{{ subcommand.panel }}")
def {{ name | replace('-', '_') }}(
    {%- for arg in subcommand.args %}
    {{ arg.snake_case }}: Annotated[{{ arg.type.split('|')[0] }}, typer.Option("--{{ arg.name }}", rich_help_panel="Arguments", show_default={{ 'default' in arg }}, help="{{ arg.description }}")]{{ ' = ' + arg.default | string if 'default' in arg else ' = None' if not arg.required else '' }},
    {%- endfor %}
    {%- for arg in subcommand.args if arg.arg_type == 'lro' %}
    timeout: Annotated[int, typer.Option("--timeout", show_default=True, help="Timeout for the long running operation (seconds)")] = 60 * 5,
    {%- endfor %}
    no_preview: Annotated[bool, typer.Option("--no-preview", "--yes", "-y", rich_help_panel="Arguments", show_default=True, help="Preview the command before executing it. You will be asked to confirm the request before it is executed.")] = False,
    quiet: Annotated[bool, typer.Option("--quiet", show_default=True, help="Whether to run in quiet mode. Sets the logging level to WARNING.")] = False,
):
    logger = logging.getLogger()
    if quiet:
        logger.setLevel(logging.WARNING)


    {%- for group in subcommand.at_least_groups.values() %}
    {%- set args_snake_case = [] %}
    {%- set args_kebab_case = [] %}
    {%- for arg in group %}
    {%- set args_snake_case = args_snake_case.append(arg.snake_case) %}
    {%- set args_kebab_case = args_kebab_case.append("--" + arg.name) %}
    {%- endfor %}

    if not any([{{args_snake_case|join(', ')}}]):
        raise typer.BadParameter("At least one of the following arguments is required: {{args_kebab_case|join(', ')}}")
    {%- endfor %}

    {%- for group in subcommand.mut_groups.values() %}
    {%- set args_snake_case = [] %}
    {%- set args_kebab_case = [] %}
    {%- for arg in group %}
    {%- set args_snake_case = args_snake_case.append(arg.snake_case) %}
    {%- set args_kebab_case = args_kebab_case.append("--" + arg.name) %}
    {%- endfor %}    

    if all({{args_snake_case|join(', ')}}):
        raise typer.BadParameter("At most one of the following arguments is allowed: {{args_kebab_case|join(', ')}}")
    {%- endfor %}
    


    response = {{ module_name | replace('-', '_') }}_{{ name | replace('-', '_') }}(
        {%- for arg in subcommand.args %}
        {{ arg.snake_case }}={{ arg.snake_case }},
        {%- endfor %}
        {%- for arg in subcommand.args if arg.arg_type == 'lro' %}
        timeout=timeout,
        {%- endfor %}        
        preview=not no_preview,
    )

    try:
        content = response.json()
    except json.JSONDecodeError:
        content = response.text

    output = {  
        "url": response.url,
        "method": response.request.method,
        "status_code": response.status_code,
        "reason": response.reason,
        "headers": dict(response.headers),
        "content": content,
    }

    typer.echo(json.dumps(output, indent=2))
    return output
{%- endfor %}
""".strip()


def generate_module():
    subdir = "commands"
    commands_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), subdir)
    commands = [f for f in os.listdir(commands_dir) if f.endswith(".yaml") or f.endswith(".yml")]

    modules = []
    for command in commands:
        with open(os.path.join(commands_dir, command), "r") as f:
            yaml_data = safe_load(f)

        try:
            Command.model_validate(yaml_data)
        except Exception as e:
            print(f"Validation error in {command}: {e}")
            raise e
        # print("YAML Data:", yaml_data)
        # print("Subcommands:", yaml_data.get("subcommands", {}))
        command_name = yaml_data.get("command")
        if command_name is None:
            raise ValueError(f"Command not found in {command}!")
        if "subcommands" in yaml_data:
            subcommands = []
            for name, details in yaml_data["subcommands"].items():
                mut_groups = {}

                at_least_groups = {}

                for arg in details.get("args", []):
                    arg["snake_case"] = arg["name"].replace("-", "_")
                    arg["camel_case"] = arg["name"].split("-")[0] + "".join(
                        word.capitalize() for word in arg["name"].split("-")[1:]
                    )

                for arg in details.get("args", []):
                    if arg.get("arg_group_type_id"):
                        if arg.get("arg_group_type_id").startswith("mut"):
                            if arg.get("arg_group_type_id") not in mut_groups:
                                mut_groups[arg.get("arg_group_type_id")] = []
                            mut_groups[arg.get("arg_group_type_id")].append(arg)
                        elif arg.get("arg_group_type_id").startswith("at-least"):
                            if arg.get("arg_group_type_id") not in at_least_groups:
                                at_least_groups[arg.get("arg_group_type_id")] = []
                            at_least_groups[arg.get("arg_group_type_id")].append(arg)

                    # print(arg.get("custom_payload"))
                # print("Args:", details.get("args", []))
                details["mut_groups"] = mut_groups
                details["at_least_groups"] = at_least_groups
                # print(f"Mut groups: {mut_groups}")
                # print(f"At least groups: {at_least_groups}")
                # print(f"\nSubcommand {name}:")

                subcommands.append(name)
        template = Template(command_template)
        command_module = template.render(
            subcommands=yaml_data["subcommands"], module_name=command_name, base_url=BASE_URL
        )
        with open(f"src/msfabricutils/cli/commands/{command_name.replace('-', '_')}.py", "w") as f:
            f.write(command_module)
        modules.append(
            (command_name, [f"{command_name}_{subcommand}" for subcommand in subcommands])
        )

        template = Template(api_template)
        api_module = template.render(
            subcommands=yaml_data["subcommands"], module_name=command_name, base_url=BASE_URL
        )
        with open(f"src/msfabricutils/rest_api/{command_name.replace('-', '_')}.py", "w") as f:
            f.write(api_module)

    with open("src/msfabricutils/rest_api/__init__.py", "w") as f:
        for command, subcommands in modules:
            for subcommand in subcommands:
                f.write(
                    f"from .{command.replace('-', '_')} import {subcommand.replace('-', '_')}\n"
                )
        f.write("\n")
        f.write("__all__ = (\n")
        for command, subcommands in modules:
            for subcommand in subcommands:
                f.write(f'    "{subcommand.replace("-", "_")}",\n')
        f.write(")\n")

    with open("src/msfabricutils/cli/commands/__init__.py", "w") as f:
        for module, subcommands in sorted(modules):
            f.write(
                f"from .{module.replace('-', '_')} import app as {module.replace('-', '_')}_app\n"
            )

        f.write("\n")
        f.write("COMMANDS = {\n")
        for module, subcommands in sorted(modules):
            f.write(f"    '{module}': {module.replace('-', '_')}_app,\n")
        f.write("}")

    for module, subcommands in sorted(modules):
        with open(f"docs/core/fabric-api/{module.replace('-', '_')}.md", "w") as f:
            f.write(f"# {module.replace('-', ' ').title()}\n\n")
            f.write("!!! warning\n")
            f.write("    The functions are not fully tested yet.\n")
            f.write("    Use with caution.\n")
            f.write(
                "    Please report any issues to the [GitHub repository](https://github.com/mrjsj/msfabricutils/issues).\n\n"
            )
            f.write(f"::: msfabricutils.rest_api.{module.replace('-', '_')}\n\n")


if __name__ == "__main__":
    generate_module()
