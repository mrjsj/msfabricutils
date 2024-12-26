import json
import logging
from typing import List

import typer
from typing_extensions import Annotated

from msfabricutils.rest_api import (
    lakehouse_create,
    lakehouse_delete,
    lakehouse_get,
    lakehouse_list,
    lakehouse_list_tables,
    lakehouse_load_table,
    lakehouse_run_background_job,
    lakehouse_update,
)

app = typer.Typer(
    help="[bold]create, get, list, update, delete[/bold]",
    rich_markup_mode="rich",
)


@app.command(help="Create a lakehouse.", rich_help_panel="Lakehouse")
def create(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to create the lakehouse in.",
        ),
    ],
    display_name: Annotated[
        str,
        typer.Option(
            "--display-name",
            rich_help_panel="Arguments",
            show_default=False,
            help="The display name of the lakehouse.",
        ),
    ],
    description: Annotated[
        str,
        typer.Option(
            "--description",
            rich_help_panel="Arguments",
            show_default=False,
            help="The description of the lakehouse.",
        ),
    ] = None,
    enable_schemas: Annotated[
        bool,
        typer.Option(
            "--enable-schemas",
            rich_help_panel="Arguments",
            show_default=True,
            help="Whether the lakehouse is schema enabled.",
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

    response = lakehouse_create(
        workspace_id=workspace_id,
        display_name=display_name,
        description=description,
        enable_schemas=enable_schemas,
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


@app.command(help="Get a lakehouse.", rich_help_panel="Lakehouse")
def get(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to get the lakehouse from.",
        ),
    ],
    lakehouse_id: Annotated[
        str,
        typer.Option(
            "--lakehouse-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the lakehouse to get.",
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

    response = lakehouse_get(
        workspace_id=workspace_id,
        lakehouse_id=lakehouse_id,
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


@app.command(help="List lakehouses for a workspace.", rich_help_panel="Lakehouse")
def list(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to list lakehouses for.",
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

    response = lakehouse_list(
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


@app.command(help="Update a lakehouse.", rich_help_panel="Lakehouse")
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
    lakehouse_id: Annotated[
        str,
        typer.Option(
            "--lakehouse-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the lakehouse to update.",
        ),
    ],
    display_name: Annotated[
        str,
        typer.Option(
            "--display-name",
            rich_help_panel="Arguments",
            show_default=False,
            help="The display name of the lakehouse.",
        ),
    ] = None,
    description: Annotated[
        str,
        typer.Option(
            "--description",
            rich_help_panel="Arguments",
            show_default=False,
            help="The description of the lakehouse.",
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

    response = lakehouse_update(
        workspace_id=workspace_id,
        lakehouse_id=lakehouse_id,
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


@app.command(help="Delete a lakehouse.", rich_help_panel="Lakehouse")
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
    lakehouse_id: Annotated[
        str,
        typer.Option(
            "--lakehouse-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the lakehouse to delete.",
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

    response = lakehouse_delete(
        workspace_id=workspace_id,
        lakehouse_id=lakehouse_id,
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


@app.command(help="Run on-demand table maintenance job instance.", rich_help_panel="Job")
def run_background_job(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to create a job for.",
        ),
    ],
    lakehouse_id: Annotated[
        str,
        typer.Option(
            "--lakehouse-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the lakehouse to create a job for.",
        ),
    ],
    job_type: Annotated[
        str,
        typer.Option(
            "--job-type",
            rich_help_panel="Arguments",
            show_default=False,
            help='The type of the job to create. Must be "TableMaintenance".',
        ),
    ],
    table_name: Annotated[
        str,
        typer.Option(
            "--table-name",
            rich_help_panel="Arguments",
            show_default=False,
            help="The name of the table to run the job on.",
        ),
    ],
    schema_name: Annotated[
        str,
        typer.Option(
            "--schema-name",
            rich_help_panel="Arguments",
            show_default=False,
            help="The name of the schema to run the job on. Only applicable for schema enabled lakehouses.",
        ),
    ] = None,
    v_order: Annotated[
        bool,
        typer.Option(
            "--v-order",
            rich_help_panel="Arguments",
            show_default=False,
            help="If table should be v-ordered.",
        ),
    ] = None,
    z_order_columns: Annotated[
        List[str],
        typer.Option(
            "--z-order-columns",
            rich_help_panel="Arguments",
            show_default=False,
            help="List of columns to z-order by.",
        ),
    ] = None,
    retention_period: Annotated[
        str,
        typer.Option(
            "--retention-period",
            rich_help_panel="Arguments",
            show_default=False,
            help="Retention periode in format d:hh:mm:ss. Overrides the default retention period.",
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

    response = lakehouse_run_background_job(
        workspace_id=workspace_id,
        lakehouse_id=lakehouse_id,
        job_type=job_type,
        table_name=table_name,
        schema_name=schema_name,
        v_order=v_order,
        z_order_columns=z_order_columns,
        retention_period=retention_period,
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


@app.command(help="List tables in a lakehouse.", rich_help_panel="Table")
def list_tables(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to list tables for.",
        ),
    ],
    lakehouse_id: Annotated[
        str,
        typer.Option(
            "--lakehouse-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the lakehouse to list tables for.",
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
    max_results: Annotated[
        int,
        typer.Option(
            "--max-results",
            rich_help_panel="Arguments",
            show_default=False,
            help="The maximum number of results to return.",
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

    response = lakehouse_list_tables(
        workspace_id=workspace_id,
        lakehouse_id=lakehouse_id,
        continuation_token=continuation_token,
        max_results=max_results,
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


@app.command(help="Load a table.", rich_help_panel="Table")
def load_table(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to load the table for.",
        ),
    ],
    lakehouse_id: Annotated[
        str,
        typer.Option(
            "--lakehouse-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the lakehouse to load the table for.",
        ),
    ],
    table_name: Annotated[
        str,
        typer.Option(
            "--table-name",
            rich_help_panel="Arguments",
            show_default=False,
            help="The name of the table to load.",
        ),
    ],
    relative_path: Annotated[
        str,
        typer.Option(
            "--relative-path",
            rich_help_panel="Arguments",
            show_default=False,
            help="The relative path to the table to load.",
        ),
    ],
    path_type: Annotated[
        str,
        typer.Option(
            "--path-type",
            rich_help_panel="Arguments",
            show_default=False,
            help='The type of the path to load. Either "File" or "Folder".',
        ),
    ],
    format: Annotated[
        str,
        typer.Option(
            "--format",
            rich_help_panel="Arguments",
            show_default=False,
            help='The format of the files to load. Must be "Parquet" or "Csv".',
        ),
    ] = None,
    header: Annotated[
        bool,
        typer.Option(
            "--header",
            rich_help_panel="Arguments",
            show_default=False,
            help="Whether the file has a header row. Only applicable for csv files.",
        ),
    ] = None,
    delimiter: Annotated[
        str,
        typer.Option(
            "--delimiter",
            rich_help_panel="Arguments",
            show_default=False,
            help="The delimiter of the csv files. Only applicable for csv files.",
        ),
    ] = None,
    mode: Annotated[
        str,
        typer.Option(
            "--mode",
            rich_help_panel="Arguments",
            show_default=False,
            help='The mode to load the table in. Either "Overwrite" or "Append".',
        ),
    ] = None,
    file_extension: Annotated[
        str,
        typer.Option(
            "--file-extension",
            rich_help_panel="Arguments",
            show_default=False,
            help="The file extension of the files to load.",
        ),
    ] = None,
    recursive: Annotated[
        bool,
        typer.Option(
            "--recursive",
            rich_help_panel="Arguments",
            show_default=False,
            help="Whether to search data files recursively or not, when loading from a folder.",
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

    response = lakehouse_load_table(
        workspace_id=workspace_id,
        lakehouse_id=lakehouse_id,
        table_name=table_name,
        relative_path=relative_path,
        path_type=path_type,
        format=format,
        header=header,
        delimiter=delimiter,
        mode=mode,
        file_extension=file_extension,
        recursive=recursive,
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
