import json
import logging

import typer
from typing_extensions import Annotated

from msfabricutils.rest_api import (
    eventhouse_create,
    eventhouse_delete,
    eventhouse_get,
    eventhouse_get_definition,
    eventhouse_list,
    eventhouse_update,
    eventhouse_update_definition,
)

app = typer.Typer(
    help="[bold]create, get, list, update, delete[/bold]",
    rich_markup_mode="rich",
)


@app.command(help="Create an eventhouse.", rich_help_panel="Eventhouse")
def create(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to create the eventhouse in.",
        ),
    ],
    display_name: Annotated[
        str,
        typer.Option(
            "--display-name",
            rich_help_panel="Arguments",
            show_default=False,
            help="The display name of the eventhouse.",
        ),
    ],
    eventhouse_path: Annotated[
        str,
        typer.Option(
            "--eventhouse-path",
            rich_help_panel="Arguments",
            show_default=False,
            help="The path to the eventhouse to load content from.",
        ),
    ],
    description: Annotated[
        str,
        typer.Option(
            "--description",
            rich_help_panel="Arguments",
            show_default=False,
            help="The description of the eventhouse.",
        ),
    ] = None,
    await_lro: Annotated[
        bool,
        typer.Option(
            "--await-lro",
            rich_help_panel="Arguments",
            show_default=True,
            help="Whether to await the long running operation.",
        ),
    ] = False,
    timeout: Annotated[
        int,
        typer.Option(
            "--timeout", show_default=True, help="Timeout for the long running operation (seconds)"
        ),
    ] = 60 * 5,
    no_preview: Annotated[
        bool,
        typer.Option(
            "--no-preview",
            "--yes",
            "-y",
            rich_help_panel="Arguments",
            show_default=True,
            help="Preview the command before executing it. You will be asked to confirm the request before it is executed.",
        ),
    ] = False,
    quiet: Annotated[
        bool,
        typer.Option(
            "--quiet",
            show_default=True,
            help="Whether to run in quiet mode. Sets the logging level to WARNING.",
        ),
    ] = False,
):
    logger = logging.getLogger()
    if quiet:
        logger.setLevel(logging.WARNING)

    response = eventhouse_create(
        workspace_id=workspace_id,
        display_name=display_name,
        eventhouse_path=eventhouse_path,
        description=description,
        await_lro=await_lro,
        timeout=timeout,
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


@app.command(help="Get an eventhouse.", rich_help_panel="Eventhouse")
def get(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to get the eventhouse from.",
        ),
    ],
    eventhouse_id: Annotated[
        str,
        typer.Option(
            "--eventhouse-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the eventhouse to get.",
        ),
    ],
    no_preview: Annotated[
        bool,
        typer.Option(
            "--no-preview",
            "--yes",
            "-y",
            rich_help_panel="Arguments",
            show_default=True,
            help="Preview the command before executing it. You will be asked to confirm the request before it is executed.",
        ),
    ] = False,
    quiet: Annotated[
        bool,
        typer.Option(
            "--quiet",
            show_default=True,
            help="Whether to run in quiet mode. Sets the logging level to WARNING.",
        ),
    ] = False,
):
    logger = logging.getLogger()
    if quiet:
        logger.setLevel(logging.WARNING)

    response = eventhouse_get(
        workspace_id=workspace_id,
        eventhouse_id=eventhouse_id,
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


@app.command(help="List eventhouses for a workspace.", rich_help_panel="Eventhouse")
def list(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to list eventhouses for.",
        ),
    ],
    continuation_token: Annotated[
        str,
        typer.Option(
            "--continuation-token",
            rich_help_panel="Arguments",
            show_default=False,
            help="A token for retrieving the next page of results.",
        ),
    ] = None,
    no_preview: Annotated[
        bool,
        typer.Option(
            "--no-preview",
            "--yes",
            "-y",
            rich_help_panel="Arguments",
            show_default=True,
            help="Preview the command before executing it. You will be asked to confirm the request before it is executed.",
        ),
    ] = False,
    quiet: Annotated[
        bool,
        typer.Option(
            "--quiet",
            show_default=True,
            help="Whether to run in quiet mode. Sets the logging level to WARNING.",
        ),
    ] = False,
):
    logger = logging.getLogger()
    if quiet:
        logger.setLevel(logging.WARNING)

    response = eventhouse_list(
        workspace_id=workspace_id,
        continuation_token=continuation_token,
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


@app.command(help="Update an eventhouse.", rich_help_panel="Eventhouse")
def update(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to update.",
        ),
    ],
    eventhouse_id: Annotated[
        str,
        typer.Option(
            "--eventhouse-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the eventhouse to update.",
        ),
    ],
    display_name: Annotated[
        str,
        typer.Option(
            "--display-name",
            rich_help_panel="Arguments",
            show_default=False,
            help="The display name of the eventhouse.",
        ),
    ] = None,
    description: Annotated[
        str,
        typer.Option(
            "--description",
            rich_help_panel="Arguments",
            show_default=False,
            help="The description of the eventhouse.",
        ),
    ] = None,
    no_preview: Annotated[
        bool,
        typer.Option(
            "--no-preview",
            "--yes",
            "-y",
            rich_help_panel="Arguments",
            show_default=True,
            help="Preview the command before executing it. You will be asked to confirm the request before it is executed.",
        ),
    ] = False,
    quiet: Annotated[
        bool,
        typer.Option(
            "--quiet",
            show_default=True,
            help="Whether to run in quiet mode. Sets the logging level to WARNING.",
        ),
    ] = False,
):
    logger = logging.getLogger()
    if quiet:
        logger.setLevel(logging.WARNING)

    if not any([display_name, description]):
        raise typer.BadParameter(
            "At least one of the following arguments is required: --display-name, --description"
        )

    response = eventhouse_update(
        workspace_id=workspace_id,
        eventhouse_id=eventhouse_id,
        display_name=display_name,
        description=description,
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


@app.command(help="Delete an eventhouse.", rich_help_panel="Eventhouse")
def delete(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to delete.",
        ),
    ],
    eventhouse_id: Annotated[
        str,
        typer.Option(
            "--eventhouse-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the eventhouse to delete.",
        ),
    ],
    no_preview: Annotated[
        bool,
        typer.Option(
            "--no-preview",
            "--yes",
            "-y",
            rich_help_panel="Arguments",
            show_default=True,
            help="Preview the command before executing it. You will be asked to confirm the request before it is executed.",
        ),
    ] = False,
    quiet: Annotated[
        bool,
        typer.Option(
            "--quiet",
            show_default=True,
            help="Whether to run in quiet mode. Sets the logging level to WARNING.",
        ),
    ] = False,
):
    logger = logging.getLogger()
    if quiet:
        logger.setLevel(logging.WARNING)

    response = eventhouse_delete(
        workspace_id=workspace_id,
        eventhouse_id=eventhouse_id,
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


@app.command(help="Get the definition of an eventhouse.", rich_help_panel="EventhouseDefinition")
def get_definition(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to get the eventhouse definition from.",
        ),
    ],
    eventhouse_id: Annotated[
        str,
        typer.Option(
            "--eventhouse-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the eventhouse to get the definition from.",
        ),
    ],
    format: Annotated[
        str,
        typer.Option(
            "--format",
            rich_help_panel="Arguments",
            show_default=False,
            help='The format of the Eventhouse definition. Supported format is "eventhouse".',
        ),
    ] = None,
    await_lro: Annotated[
        bool,
        typer.Option(
            "--await-lro",
            rich_help_panel="Arguments",
            show_default=True,
            help="Whether to await the long running operation.",
        ),
    ] = False,
    timeout: Annotated[
        int,
        typer.Option(
            "--timeout", show_default=True, help="Timeout for the long running operation (seconds)"
        ),
    ] = 60 * 5,
    no_preview: Annotated[
        bool,
        typer.Option(
            "--no-preview",
            "--yes",
            "-y",
            rich_help_panel="Arguments",
            show_default=True,
            help="Preview the command before executing it. You will be asked to confirm the request before it is executed.",
        ),
    ] = False,
    quiet: Annotated[
        bool,
        typer.Option(
            "--quiet",
            show_default=True,
            help="Whether to run in quiet mode. Sets the logging level to WARNING.",
        ),
    ] = False,
):
    logger = logging.getLogger()
    if quiet:
        logger.setLevel(logging.WARNING)

    response = eventhouse_get_definition(
        workspace_id=workspace_id,
        eventhouse_id=eventhouse_id,
        format=format,
        await_lro=await_lro,
        timeout=timeout,
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


@app.command(help="Update the definition of an eventhouse.", rich_help_panel="EventhouseDefinition")
def update_definition(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to update.",
        ),
    ],
    eventhouse_id: Annotated[
        str,
        typer.Option(
            "--eventhouse-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the eventhouse to update.",
        ),
    ],
    eventhouse_path: Annotated[
        str,
        typer.Option(
            "--eventhouse-path",
            rich_help_panel="Arguments",
            show_default=False,
            help="The path to the eventhouse to load content from.",
        ),
    ],
    update_metadata: Annotated[
        bool,
        typer.Option(
            "--update-metadata",
            rich_help_panel="Arguments",
            show_default=True,
            help="When set to true, the item's metadata is updated using the metadata in the .platform file.",
        ),
    ] = False,
    await_lro: Annotated[
        bool,
        typer.Option(
            "--await-lro",
            rich_help_panel="Arguments",
            show_default=True,
            help="Whether to await the long running operation.",
        ),
    ] = False,
    timeout: Annotated[
        int,
        typer.Option(
            "--timeout", show_default=True, help="Timeout for the long running operation (seconds)"
        ),
    ] = 60 * 5,
    no_preview: Annotated[
        bool,
        typer.Option(
            "--no-preview",
            "--yes",
            "-y",
            rich_help_panel="Arguments",
            show_default=True,
            help="Preview the command before executing it. You will be asked to confirm the request before it is executed.",
        ),
    ] = False,
    quiet: Annotated[
        bool,
        typer.Option(
            "--quiet",
            show_default=True,
            help="Whether to run in quiet mode. Sets the logging level to WARNING.",
        ),
    ] = False,
):
    logger = logging.getLogger()
    if quiet:
        logger.setLevel(logging.WARNING)

    response = eventhouse_update_definition(
        workspace_id=workspace_id,
        eventhouse_id=eventhouse_id,
        eventhouse_path=eventhouse_path,
        update_metadata=update_metadata,
        await_lro=await_lro,
        timeout=timeout,
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
