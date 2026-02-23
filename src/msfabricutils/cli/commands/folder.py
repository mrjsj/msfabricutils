import json
import logging

import typer
from typing_extensions import Annotated

from msfabricutils.rest_api import (
    folder_create,
    folder_delete,
    folder_get,
    folder_list,
    folder_move,
    folder_update,
)

app = typer.Typer(
    help="[bold]create, get, list, update, delete, and more ... [/bold]",
    rich_markup_mode="rich",
)

@app.command(help="Create a folder.", rich_help_panel="Folder")
def create(
    workspace_id: Annotated[str, typer.Option("--workspace-id", rich_help_panel="Arguments", show_default=False, help="The workspace id.")],
    display_name: Annotated[str, typer.Option("--display-name", rich_help_panel="Arguments", show_default=False, help="The display name of the folder.")],
    parent_folder_id: Annotated[str, typer.Option("--parent-folder-id", rich_help_panel="Arguments", show_default=False, help="The parent folder ID. If not specified or null, the folder is created with the workspace as its parent folder.")] = None,
    no_preview: Annotated[bool, typer.Option("--no-preview", "--yes", "-y", rich_help_panel="Arguments", show_default=True, help="Preview the command before executing it. You will be asked to confirm the request before it is executed.")] = False,
    quiet: Annotated[bool, typer.Option("--quiet", show_default=True, help="Whether to run in quiet mode. Sets the logging level to WARNING.")] = False,
):
    logger = logging.getLogger()
    if quiet:
        logger.setLevel(logging.WARNING)
    


    response = folder_create(
        workspace_id=workspace_id,
        display_name=display_name,
        parent_folder_id=parent_folder_id,        
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

@app.command(help="Get a folder.", rich_help_panel="Folder")
def get(
    workspace_id: Annotated[str, typer.Option("--workspace-id", rich_help_panel="Arguments", show_default=False, help="The workspace id.")],
    folder_id: Annotated[str, typer.Option("--folder-id", rich_help_panel="Arguments", show_default=False, help="The id of the folder to get.")],
    no_preview: Annotated[bool, typer.Option("--no-preview", "--yes", "-y", rich_help_panel="Arguments", show_default=True, help="Preview the command before executing it. You will be asked to confirm the request before it is executed.")] = False,
    quiet: Annotated[bool, typer.Option("--quiet", show_default=True, help="Whether to run in quiet mode. Sets the logging level to WARNING.")] = False,
):
    logger = logging.getLogger()
    if quiet:
        logger.setLevel(logging.WARNING)
    


    response = folder_get(
        workspace_id=workspace_id,
        folder_id=folder_id,        
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

@app.command(help="List folders.", rich_help_panel="Folder")
def list(
    workspace_id: Annotated[str, typer.Option("--workspace-id", rich_help_panel="Arguments", show_default=False, help="The workspace id.")],
    recursive: Annotated[bool, typer.Option("--recursive", rich_help_panel="Arguments", show_default=True, help="Lists folders in a folder and its nested folders, or just a folder only. True - All folders in the folder and its nested folders are listed, False - Only folders in the folder are listed.")] = True,
    root_folder_id: Annotated[str, typer.Option("--root-folder-id", rich_help_panel="Arguments", show_default=False, help="This parameter allows users to filter folders based on a specific root folder. If not provided, the workspace is used as the root folder.")] = None,
    continuation_token: Annotated[str, typer.Option("--continuation-token", rich_help_panel="Arguments", show_default=False, help="A token for retrieving the next page of results.")] = None,
    no_preview: Annotated[bool, typer.Option("--no-preview", "--yes", "-y", rich_help_panel="Arguments", show_default=True, help="Preview the command before executing it. You will be asked to confirm the request before it is executed.")] = False,
    quiet: Annotated[bool, typer.Option("--quiet", show_default=True, help="Whether to run in quiet mode. Sets the logging level to WARNING.")] = False,
):
    logger = logging.getLogger()
    if quiet:
        logger.setLevel(logging.WARNING)
    


    response = folder_list(
        workspace_id=workspace_id,
        recursive=recursive,
        root_folder_id=root_folder_id,
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

@app.command(help="Update a folder.", rich_help_panel="Folder")
def update(
    workspace_id: Annotated[str, typer.Option("--workspace-id", rich_help_panel="Arguments", show_default=False, help="The workspace id.")],
    folder_id: Annotated[str, typer.Option("--folder-id", rich_help_panel="Arguments", show_default=False, help="The id of the folder to update.")],
    display_name: Annotated[str, typer.Option("--display-name", rich_help_panel="Arguments", show_default=False, help="The display name of the folder.")],
    no_preview: Annotated[bool, typer.Option("--no-preview", "--yes", "-y", rich_help_panel="Arguments", show_default=True, help="Preview the command before executing it. You will be asked to confirm the request before it is executed.")] = False,
    quiet: Annotated[bool, typer.Option("--quiet", show_default=True, help="Whether to run in quiet mode. Sets the logging level to WARNING.")] = False,
):
    logger = logging.getLogger()
    if quiet:
        logger.setLevel(logging.WARNING)
    


    response = folder_update(
        workspace_id=workspace_id,
        folder_id=folder_id,
        display_name=display_name,        
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

@app.command(help="Delete a folder.", rich_help_panel="Folder")
def delete(
    workspace_id: Annotated[str, typer.Option("--workspace-id", rich_help_panel="Arguments", show_default=False, help="The workspace id.")],
    folder_id: Annotated[str, typer.Option("--folder-id", rich_help_panel="Arguments", show_default=False, help="The id of the folder to delete.")],
    no_preview: Annotated[bool, typer.Option("--no-preview", "--yes", "-y", rich_help_panel="Arguments", show_default=True, help="Preview the command before executing it. You will be asked to confirm the request before it is executed.")] = False,
    quiet: Annotated[bool, typer.Option("--quiet", show_default=True, help="Whether to run in quiet mode. Sets the logging level to WARNING.")] = False,
):
    logger = logging.getLogger()
    if quiet:
        logger.setLevel(logging.WARNING)
    


    response = folder_delete(
        workspace_id=workspace_id,
        folder_id=folder_id,        
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

@app.command(help="Moves the specified folder within the same workspace.", rich_help_panel="Folder")
def move(
    workspace_id: Annotated[str, typer.Option("--workspace-id", rich_help_panel="Arguments", show_default=False, help="The workspace id.")],
    folder_id: Annotated[str, typer.Option("--folder-id", rich_help_panel="Arguments", show_default=False, help="The id of the folder to delete.")],
    target_folder_id: Annotated[str, typer.Option("--target-folder-id", rich_help_panel="Arguments", show_default=False, help="The destination folder ID. If not provided, the workspace is used as the destination folder.")] = None,
    no_preview: Annotated[bool, typer.Option("--no-preview", "--yes", "-y", rich_help_panel="Arguments", show_default=True, help="Preview the command before executing it. You will be asked to confirm the request before it is executed.")] = False,
    quiet: Annotated[bool, typer.Option("--quiet", show_default=True, help="Whether to run in quiet mode. Sets the logging level to WARNING.")] = False,
):
    logger = logging.getLogger()
    if quiet:
        logger.setLevel(logging.WARNING)
    


    response = folder_move(
        workspace_id=workspace_id,
        folder_id=folder_id,
        target_folder_id=target_folder_id,        
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