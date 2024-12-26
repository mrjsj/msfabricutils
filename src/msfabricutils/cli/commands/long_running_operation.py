import json
import logging

import typer
from typing_extensions import Annotated

from msfabricutils.rest_api import (
    long_running_operation_get_result,
    long_running_operation_get_state,
)

app = typer.Typer(
    help="[bold]get-state, get-result[/bold]",
    rich_markup_mode="rich",
)


@app.command(
    help="Get the state of the long running operation.", rich_help_panel="Long Running Operation"
)
def get_state(
    operation_id: Annotated[
        str,
        typer.Option(
            "--operation-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The ID of the long running operation.",
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

    response = long_running_operation_get_state(
        operation_id=operation_id,
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
    help="Get the result of the long running operation. Only available when the operation status is `Succeeded`.",
    rich_help_panel="Long Running Operation",
)
def get_result(
    operation_id: Annotated[
        str,
        typer.Option(
            "--operation-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The ID of the long running operation.",
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

    response = long_running_operation_get_result(
        operation_id=operation_id,
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
