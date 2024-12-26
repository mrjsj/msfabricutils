import json
import logging

import typer
from typing_extensions import Annotated

from msfabricutils.rest_api import (
    environment_cancel_publish,
    environment_create,
    environment_delete,
    environment_delete_staging_library,
    environment_get,
    environment_get_published_libraries,
    environment_get_spark_compute_published_settings,
    environment_get_spark_compute_staging_settings,
    environment_get_staging_libraries,
    environment_list,
    environment_publish,
    environment_update,
    environment_update_spark_compute_staging_settings,
    environment_upload_staging_library,
)

app = typer.Typer(
    help="[bold]create, get, list, update, delete[/bold]",
    rich_markup_mode="rich",
)


@app.command(help="Create an environment.", rich_help_panel="Environment")
def create(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to create the environment in.",
        ),
    ],
    display_name: Annotated[
        str,
        typer.Option(
            "--display-name",
            rich_help_panel="Arguments",
            show_default=False,
            help="The display name of the environment.",
        ),
    ],
    description: Annotated[
        str,
        typer.Option(
            "--description",
            rich_help_panel="Arguments",
            show_default=False,
            help="The description of the environment.",
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

    response = environment_create(
        workspace_id=workspace_id,
        display_name=display_name,
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


@app.command(help="Get an environment.", rich_help_panel="Environment")
def get(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to get the environment from.",
        ),
    ],
    environment_id: Annotated[
        str,
        typer.Option(
            "--environment-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the environment to get.",
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

    response = environment_get(
        workspace_id=workspace_id,
        environment_id=environment_id,
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


@app.command(help="List environments for a workspace.", rich_help_panel="Environment")
def list(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to list environments for.",
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

    response = environment_list(
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


@app.command(help="Update an environment.", rich_help_panel="Environment")
def update(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to update the environment in.",
        ),
    ],
    environment_id: Annotated[
        str,
        typer.Option(
            "--environment-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the environment to update.",
        ),
    ],
    display_name: Annotated[
        str,
        typer.Option(
            "--display-name",
            rich_help_panel="Arguments",
            show_default=False,
            help="The display name of the environment.",
        ),
    ] = None,
    description: Annotated[
        str,
        typer.Option(
            "--description",
            rich_help_panel="Arguments",
            show_default=False,
            help="The description of the environment.",
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

    response = environment_update(
        workspace_id=workspace_id,
        environment_id=environment_id,
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


@app.command(help="Delete an environment.", rich_help_panel="Environment")
def delete(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to delete the environment from.",
        ),
    ],
    environment_id: Annotated[
        str,
        typer.Option(
            "--environment-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the environment to delete.",
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

    response = environment_delete(
        workspace_id=workspace_id,
        environment_id=environment_id,
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
    help="Get spark compute published settings for an environment.", rich_help_panel="Spark Compute"
)
def get_spark_compute_published_settings(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to get the spark compute published settings for.",
        ),
    ],
    environment_id: Annotated[
        str,
        typer.Option(
            "--environment-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the environment to get the spark compute published settings for.",
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

    response = environment_get_spark_compute_published_settings(
        workspace_id=workspace_id,
        environment_id=environment_id,
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
    help="Get spark compute staging settings for an environment.", rich_help_panel="Spark Compute"
)
def get_spark_compute_staging_settings(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to get the spark compute staging settings for.",
        ),
    ],
    environment_id: Annotated[
        str,
        typer.Option(
            "--environment-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the environment to get the spark compute staging settings for.",
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

    response = environment_get_spark_compute_staging_settings(
        workspace_id=workspace_id,
        environment_id=environment_id,
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
    help="Update spark compute staging settings for an environment.",
    rich_help_panel="Spark Compute",
)
def update_spark_compute_staging_settings(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to update the spark compute staging settings for.",
        ),
    ],
    environment_id: Annotated[
        str,
        typer.Option(
            "--environment-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the environment to update the spark compute staging settings for.",
        ),
    ],
    instance_pool_name: Annotated[
        str,
        typer.Option(
            "--instance-pool-name",
            rich_help_panel="Arguments",
            show_default=False,
            help="The name of the instance pool to use for Spark Compute settings.",
        ),
    ] = None,
    instance_pool_type: Annotated[
        str,
        typer.Option(
            "--instance-pool-type",
            rich_help_panel="Arguments",
            show_default=False,
            help="The type of the instance pool to use for Spark Compute settings.",
        ),
    ] = None,
    driver_cores: Annotated[
        int,
        typer.Option(
            "--driver-cores",
            rich_help_panel="Arguments",
            show_default=False,
            help="The number of cores to use for the driver.",
        ),
    ] = None,
    driver_memory: Annotated[
        str,
        typer.Option(
            "--driver-memory",
            rich_help_panel="Arguments",
            show_default=False,
            help="The memory to use for the driver.",
        ),
    ] = None,
    executor_cores: Annotated[
        int,
        typer.Option(
            "--executor-cores",
            rich_help_panel="Arguments",
            show_default=False,
            help="The number of cores to use for the executors.",
        ),
    ] = None,
    executor_memory: Annotated[
        str,
        typer.Option(
            "--executor-memory",
            rich_help_panel="Arguments",
            show_default=False,
            help="The memory to use for the executors.",
        ),
    ] = None,
    dynamic_executor_allocation_enabled: Annotated[
        bool,
        typer.Option(
            "--dynamic-executor-allocation-enabled",
            rich_help_panel="Arguments",
            show_default=False,
            help="Whether to enable dynamic executor allocation.",
        ),
    ] = None,
    min_executors: Annotated[
        int,
        typer.Option(
            "--min-executors",
            rich_help_panel="Arguments",
            show_default=False,
            help="The minimum number of executors to use for dynamic executor allocation.",
        ),
    ] = None,
    max_executors: Annotated[
        int,
        typer.Option(
            "--max-executors",
            rich_help_panel="Arguments",
            show_default=False,
            help="The maximum number of executors to use for dynamic executor allocation.",
        ),
    ] = None,
    spark_acls_enable: Annotated[
        str,
        typer.Option(
            "--spark-acls-enable",
            rich_help_panel="Arguments",
            show_default=False,
            help="Whether to enable Spark ACLs.",
        ),
    ] = None,
    spark_admin_acls: Annotated[
        str,
        typer.Option(
            "--spark-admin-acls",
            rich_help_panel="Arguments",
            show_default=False,
            help="The admin ACLs to use for Spark.",
        ),
    ] = None,
    runtime_version: Annotated[
        str,
        typer.Option(
            "--runtime-version",
            rich_help_panel="Arguments",
            show_default=False,
            help="The runtime version to use for Spark Compute settings.",
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

    response = environment_update_spark_compute_staging_settings(
        workspace_id=workspace_id,
        environment_id=environment_id,
        instance_pool_name=instance_pool_name,
        instance_pool_type=instance_pool_type,
        driver_cores=driver_cores,
        driver_memory=driver_memory,
        executor_cores=executor_cores,
        executor_memory=executor_memory,
        dynamic_executor_allocation_enabled=dynamic_executor_allocation_enabled,
        min_executors=min_executors,
        max_executors=max_executors,
        spark_acls_enable=spark_acls_enable,
        spark_admin_acls=spark_admin_acls,
        runtime_version=runtime_version,
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


@app.command(help="Get published libraries for an environment.", rich_help_panel="Libraries")
def get_published_libraries(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to get the published libraries for.",
        ),
    ],
    environment_id: Annotated[
        str,
        typer.Option(
            "--environment-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the environment to get the published libraries for.",
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

    response = environment_get_published_libraries(
        workspace_id=workspace_id,
        environment_id=environment_id,
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


@app.command(help="Get staging libraries for an environment.", rich_help_panel="Libraries")
def get_staging_libraries(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to get the staging libraries for.",
        ),
    ],
    environment_id: Annotated[
        str,
        typer.Option(
            "--environment-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the environment to get the staging libraries for.",
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

    response = environment_get_staging_libraries(
        workspace_id=workspace_id,
        environment_id=environment_id,
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


@app.command(help="Delete a staging library for an environment.", rich_help_panel="Libraries")
def delete_staging_library(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to delete the staging library from.",
        ),
    ],
    environment_id: Annotated[
        str,
        typer.Option(
            "--environment-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the environment to delete the staging library from.",
        ),
    ],
    library_to_delete: Annotated[
        str,
        typer.Option(
            "--library-to-delete",
            rich_help_panel="Arguments",
            show_default=False,
            help="The library file to delete. Must include the file extension.",
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

    response = environment_delete_staging_library(
        workspace_id=workspace_id,
        environment_id=environment_id,
        library_to_delete=library_to_delete,
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


@app.command(help="Upload a staging library for an environment.", rich_help_panel="Libraries")
def upload_staging_library(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to upload the staged library to.",
        ),
    ],
    environment_id: Annotated[
        str,
        typer.Option(
            "--environment-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the environment to upload the staging library to.",
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

    response = environment_upload_staging_library(
        workspace_id=workspace_id,
        environment_id=environment_id,
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


@app.command(help="Publish an environment.", rich_help_panel="Environment")
def publish(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to publish the environment for.",
        ),
    ],
    environment_id: Annotated[
        str,
        typer.Option(
            "--environment-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the environment to publish.",
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

    response = environment_publish(
        workspace_id=workspace_id,
        environment_id=environment_id,
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


@app.command(help="Cancel a publish operation for an environment.", rich_help_panel="Environment")
def cancel_publish(
    workspace_id: Annotated[
        str,
        typer.Option(
            "--workspace-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the workspace to cancel the publish operation for.",
        ),
    ],
    environment_id: Annotated[
        str,
        typer.Option(
            "--environment-id",
            rich_help_panel="Arguments",
            show_default=False,
            help="The id of the environment to cancel the publish operation for.",
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

    response = environment_cancel_publish(
        workspace_id=workspace_id,
        environment_id=environment_id,
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
