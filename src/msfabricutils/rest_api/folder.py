import json

import requests
import typer

from msfabricutils import get_fabric_bearer_token
from msfabricutils.common.remove_none import remove_none
from msfabricutils.common.shorten_dict_values import shorten_dict_values


def folder_create(
    workspace_id: str,
    display_name: str,
    parent_folder_id: str = None,    
    preview: bool = True,
) -> requests.Response:
    """
    Create a folder.

    Args:
        workspace_id (str): The workspace id.
        display_name (str): The display name of the folder.
        parent_folder_id (str | None): The parent folder ID. If not specified or null, the folder is created with the workspace as its parent folder.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/folders" # noqa
    url = f"{url}?"
    url = url.rstrip('&?')    
    
    method = "post"
    token = get_fabric_bearer_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {}
    data["displayName"] = display_name
    data["parentFolderId"] = parent_folder_id

    data = remove_none(data)

    if preview:
        typer.echo(f"Method:\n{method.upper()}\n")
        typer.echo(f"URL:\n{url}\n")
        typer.echo(f"Data:\n{json.dumps(shorten_dict_values(data, 35), indent=2)}\n")
        typer.echo(f"Headers:\n{json.dumps(shorten_dict_values(headers, 35), indent=2)}\n")
        typer.confirm("Do you want to run the command?", abort=True)

    response = requests.request(method=method, url=url, json=data, headers=headers)
    # response.raise_for_status()
    
    match response.status_code:
        case 200 | 201:
            return response
        case _:
            return response

def folder_get(
    workspace_id: str,
    folder_id: str,    
    preview: bool = True,
) -> requests.Response:
    """
    Get a folder.

    Args:
        workspace_id (str): The workspace id.
        folder_id (str): The id of the folder to get.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/folders/{folder_id}" # noqa
    url = f"{url}?"
    url = url.rstrip('&?')    
    
    method = "get"
    token = get_fabric_bearer_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {}

    data = remove_none(data)

    if preview:
        typer.echo(f"Method:\n{method.upper()}\n")
        typer.echo(f"URL:\n{url}\n")
        typer.echo(f"Data:\n{json.dumps(shorten_dict_values(data, 35), indent=2)}\n")
        typer.echo(f"Headers:\n{json.dumps(shorten_dict_values(headers, 35), indent=2)}\n")
        typer.confirm("Do you want to run the command?", abort=True)

    response = requests.request(method=method, url=url, json=data, headers=headers)
    # response.raise_for_status()
    
    match response.status_code:
        case 200 | 201:
            return response
        case _:
            return response

def folder_list(
    workspace_id: str,
    recursive: bool = None,
    root_folder_id: str = None,
    continuation_token: str = None,    
    preview: bool = True,
) -> requests.Response:
    """
    List folders.

    Args:
        workspace_id (str): The workspace id.
        recursive (bool | None): Lists folders in a folder and its nested folders, or just a folder only. True - All folders in the folder and its nested folders are listed, False - Only folders in the folder are listed.
        root_folder_id (str | None): This parameter allows users to filter folders based on a specific root folder. If not provided, the workspace is used as the root folder.
        continuation_token (str | None): A token for retrieving the next page of results.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/folders" # noqa
    url = f"{url}?"
    if recursive is not None:
        url = f"{url}recursive={recursive}&"
    if root_folder_id is not None:
        url = f"{url}rootFolderId={root_folder_id}&"
    if continuation_token is not None:
        url = f"{url}continuationToken={continuation_token}&"
    url = url.rstrip('&?')    
    
    method = "get"
    token = get_fabric_bearer_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {}

    data = remove_none(data)

    if preview:
        typer.echo(f"Method:\n{method.upper()}\n")
        typer.echo(f"URL:\n{url}\n")
        typer.echo(f"Data:\n{json.dumps(shorten_dict_values(data, 35), indent=2)}\n")
        typer.echo(f"Headers:\n{json.dumps(shorten_dict_values(headers, 35), indent=2)}\n")
        typer.confirm("Do you want to run the command?", abort=True)

    response = requests.request(method=method, url=url, json=data, headers=headers)
    # response.raise_for_status()
    
    match response.status_code:
        case 200 | 201:
            return response
        case _:
            return response

def folder_update(
    workspace_id: str,
    folder_id: str,
    display_name: str,    
    preview: bool = True,
) -> requests.Response:
    """
    Update a folder.

    Args:
        workspace_id (str): The workspace id.
        folder_id (str): The id of the folder to update.
        display_name (str): The display name of the folder.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/folders/{folder_id}" # noqa
    url = f"{url}?"
    url = url.rstrip('&?')    
    
    method = "patch"
    token = get_fabric_bearer_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {}
    data["displayName"] = display_name

    data = remove_none(data)

    if preview:
        typer.echo(f"Method:\n{method.upper()}\n")
        typer.echo(f"URL:\n{url}\n")
        typer.echo(f"Data:\n{json.dumps(shorten_dict_values(data, 35), indent=2)}\n")
        typer.echo(f"Headers:\n{json.dumps(shorten_dict_values(headers, 35), indent=2)}\n")
        typer.confirm("Do you want to run the command?", abort=True)

    response = requests.request(method=method, url=url, json=data, headers=headers)
    # response.raise_for_status()
    
    match response.status_code:
        case 200 | 201:
            return response
        case _:
            return response

def folder_delete(
    workspace_id: str,
    folder_id: str,    
    preview: bool = True,
) -> requests.Response:
    """
    Delete a folder.

    Args:
        workspace_id (str): The workspace id.
        folder_id (str): The id of the folder to delete.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/folders/{folder_id}" # noqa
    url = f"{url}?"
    url = url.rstrip('&?')    
    
    method = "delete"
    token = get_fabric_bearer_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {}

    data = remove_none(data)

    if preview:
        typer.echo(f"Method:\n{method.upper()}\n")
        typer.echo(f"URL:\n{url}\n")
        typer.echo(f"Data:\n{json.dumps(shorten_dict_values(data, 35), indent=2)}\n")
        typer.echo(f"Headers:\n{json.dumps(shorten_dict_values(headers, 35), indent=2)}\n")
        typer.confirm("Do you want to run the command?", abort=True)

    response = requests.request(method=method, url=url, json=data, headers=headers)
    # response.raise_for_status()
    
    match response.status_code:
        case 200 | 201:
            return response
        case _:
            return response

def folder_move(
    workspace_id: str,
    folder_id: str,
    target_folder_id: str = None,    
    preview: bool = True,
) -> requests.Response:
    """
    Moves the specified folder within the same workspace.

    Args:
        workspace_id (str): The workspace id.
        folder_id (str): The id of the folder to delete.
        target_folder_id (str | None): The destination folder ID. If not provided, the workspace is used as the destination folder.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/folders/{folder_id}/move" # noqa
    url = f"{url}?"
    url = url.rstrip('&?')    
    
    method = "post"
    token = get_fabric_bearer_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {}
    data["targetFolderId"] = target_folder_id

    data = remove_none(data)

    if preview:
        typer.echo(f"Method:\n{method.upper()}\n")
        typer.echo(f"URL:\n{url}\n")
        typer.echo(f"Data:\n{json.dumps(shorten_dict_values(data, 35), indent=2)}\n")
        typer.echo(f"Headers:\n{json.dumps(shorten_dict_values(headers, 35), indent=2)}\n")
        typer.confirm("Do you want to run the command?", abort=True)

    response = requests.request(method=method, url=url, json=data, headers=headers)
    # response.raise_for_status()
    
    match response.status_code:
        case 200 | 201:
            return response
        case _:
            return response