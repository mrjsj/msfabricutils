import json
import logging

import typer
from typing_extensions import Annotated

from msfabricutils.rest_api import (
    kql_database_create,
    kql_database_delete,
    kql_database_get,
    kql_database_get_definition,
    kql_database_list,
    kql_database_update,
    kql_database_update_definition,
)

app = typer.Typer(
    help="[bold]create, get, list, update, delete[/bold]",
    rich_markup_mode="rich",
)


@app.command(help="Create a kql database.", rich_help_panel="KqlDatabase")
def create(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to create the kql database in.",
        ),
    ],
    display_name: Annotated[
        str,
        typer.Option(
            "--display-name",
            rich_help_panel="Arguments",
            show_default=False,
            help="The display name of the kql database.",
        ),
    ],
    kql_database_path: Annotated[
        str,
        typer.Option(
            "--kql-database-path",
            rich_help_panel="Arguments",
            show_default=False,
            help="The path to the kql database to load content from.",
        ),
    ],
    description: Annotated[
        str,
        typer.Option(
            "--description",
            rich_help_panel="Arguments",
            show_default=False,
            help="The description of the kql database.",
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

    response = kql_database_create(
        workspace_id=workspace_id,
        display_name=display_name,
        kql_database_path=kql_database_path,
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


@app.command(help="Get a kql database.", rich_help_panel="KqlDatabase")
def get(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to get the kql database from.",
        ),
    ],
    kql_database_id: Annotated[
        str,
        typer.Option(
            "--kql-database-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the kql database to get.",
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

    response = kql_database_get(
        workspace_id=workspace_id,
        kql_database_id=kql_database_id,
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


@app.command(help="List kql databases for a workspace.", rich_help_panel="KqlDatabase")
def list(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to list kql databases for.",
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

    response = kql_database_list(
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


@app.command(help="Update a kql database.", rich_help_panel="KqlDatabase")
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
    kql_database_id: Annotated[
        str,
        typer.Option(
            "--kql-database-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the kql database to update.",
        ),
    ],
    display_name: Annotated[
        str,
        typer.Option(
            "--display-name",
            rich_help_panel="Arguments",
            show_default=False,
            help="The display name of the kql database.",
        ),
    ] = None,
    description: Annotated[
        str,
        typer.Option(
            "--description",
            rich_help_panel="Arguments",
            show_default=False,
            help="The description of the kql database.",
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

    response = kql_database_update(
        workspace_id=workspace_id,
        kql_database_id=kql_database_id,
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


@app.command(help="Delete a kql database.", rich_help_panel="KqlDatabase")
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
    kql_database_id: Annotated[
        str,
        typer.Option(
            "--kql-database-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the kql database to delete.",
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

    response = kql_database_delete(
        workspace_id=workspace_id,
        kql_database_id=kql_database_id,
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


@app.command(help="Get the definition of a kql database.", rich_help_panel="KqlDatabaseDefinition")
def get_definition(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to get the kql database definition from.",
        ),
    ],
    kql_database_id: Annotated[
        str,
        typer.Option(
            "--kql-database-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the kql database to get the definition from.",
        ),
    ],
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

    response = kql_database_get_definition(
        workspace_id=workspace_id,
        kql_database_id=kql_database_id,
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


@app.command(
    help="Update the definition of a kql database.", rich_help_panel="KqlDatabaseDefinition"
)
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
    kql_database_id: Annotated[
        str,
        typer.Option(
            "--kql-database-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the kql database to update.",
        ),
    ],
    kql_database_path: Annotated[
        str,
        typer.Option(
            "--kql-database-path",
            rich_help_panel="Arguments",
            show_default=False,
            help="The path to the kql database to load content from.",
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

    response = kql_database_update_definition(
        workspace_id=workspace_id,
        kql_database_id=kql_database_id,
        kql_database_path=kql_database_path,
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
