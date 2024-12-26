import base64
import json

import requests
import typer

from msfabricutils import get_fabric_bearer_token
from msfabricutils.common.remove_none import remove_none
from msfabricutils.common.shorten_dict_values import shorten_dict_values
from msfabricutils.core.operations import wait_for_long_running_operation


def eventhouse_create(
    workspace_id: str,
    display_name: str,
    eventhouse_path: str,
    description: str = None,
    await_lro: bool = None,
    timeout: int = 60 * 5,
    preview: bool = True,
) -> requests.Response:
    """
    Create an eventhouse.

    Args:
        workspace_id (str): The id of the workspace to create the eventhouse in.
        display_name (str): The display name of the eventhouse.
        eventhouse_path (str): The path to the eventhouse to load content from.
        description (str | None): The description of the eventhouse.
        await_lro (bool | None): Whether to await the long running operation.
        timeout (int): Timeout for the long running operation (seconds). Defaults to 5 minutes.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventhouses"  # noqa
    url = f"{url}?"
    url = url.rstrip("&?")

    method = "post"
    token = get_fabric_bearer_token()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    with open(eventhouse_path.rstrip("/") + "/EventhouseProperties.json", "r") as f:
        EventhouseProperties = base64.b64encode(f.read().encode()).decode()

    with open(eventhouse_path.rstrip("/") + "/.platform", "r") as f:
        platform = base64.b64encode(f.read().encode()).decode()

    data = {}
    data["displayName"] = display_name
    data["description"] = description
    custom_payload = {
        "definition": {
            "parts": [
                {
                    "path": "EventhouseProperties.json",
                    "payload": EventhouseProperties,
                    "payloadType": "InlineBase64",
                },
                {"path": ".platform", "payload": platform, "payloadType": "InlineBase64"},
            ]
        }
    }
    data = {**data, **custom_payload}

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
        case 202:
            if await_lro is True:
                operation_id = response.headers["x-ms-operation-id"]
                retry_after = response.headers["Retry-After"]
                return wait_for_long_running_operation(
                    operation_id=operation_id, retry_after=retry_after, timeout=timeout
                )
            return response
        case _:
            return response


def eventhouse_get(
    workspace_id: str,
    eventhouse_id: str,
    preview: bool = True,
) -> requests.Response:
    """
    Get an eventhouse.

    Args:
        workspace_id (str): The id of the workspace to get the eventhouse from.
        eventhouse_id (str): The id of the eventhouse to get.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = (
        f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventhouses/{eventhouse_id}"  # noqa
    )
    url = f"{url}?"
    url = url.rstrip("&?")

    method = "get"
    token = get_fabric_bearer_token()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

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


def eventhouse_list(
    workspace_id: str,
    continuation_token: str = None,
    preview: bool = True,
) -> requests.Response:
    """
    List eventhouses for a workspace.

    Args:
        workspace_id (str): The id of the workspace to list eventhouses for.
        continuation_token (str | None): A token for retrieving the next page of results.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventhouses"  # noqa
    url = f"{url}?"
    if continuation_token is not None:
        url = f"{url}continuationToken={continuation_token}&"
    url = url.rstrip("&?")

    method = "get"
    token = get_fabric_bearer_token()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

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


def eventhouse_update(
    workspace_id: str,
    eventhouse_id: str,
    display_name: str = None,
    description: str = None,
    preview: bool = True,
) -> requests.Response:
    """
    Update an eventhouse.

    Args:
        workspace_id (str): The id of the workspace to update.
        eventhouse_id (str): The id of the eventhouse to update.
        display_name (str | None): The display name of the eventhouse.
        description (str | None): The description of the eventhouse.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = (
        f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventhouses/{eventhouse_id}"  # noqa
    )
    url = f"{url}?"
    url = url.rstrip("&?")

    method = "patch"
    token = get_fabric_bearer_token()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    data = {}
    data["displayName"] = display_name
    data["description"] = description

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


def eventhouse_delete(
    workspace_id: str,
    eventhouse_id: str,
    preview: bool = True,
) -> requests.Response:
    """
    Delete an eventhouse.

    Args:
        workspace_id (str): The id of the workspace to delete.
        eventhouse_id (str): The id of the eventhouse to delete.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = (
        f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventhouses/{eventhouse_id}"  # noqa
    )
    url = f"{url}?"
    url = url.rstrip("&?")

    method = "delete"
    token = get_fabric_bearer_token()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

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


def eventhouse_get_definition(
    workspace_id: str,
    eventhouse_id: str,
    format: str = None,
    await_lro: bool = None,
    timeout: int = 60 * 5,
    preview: bool = True,
) -> requests.Response:
    """
    Get the definition of an eventhouse.

    Args:
        workspace_id (str): The id of the workspace to get the eventhouse definition from.
        eventhouse_id (str): The id of the eventhouse to get the definition from.
        format (str | None): The format of the Eventhouse definition. Supported format is \"eventhouse\".
        await_lro (bool | None): Whether to await the long running operation.
        timeout (int): Timeout for the long running operation (seconds). Defaults to 5 minutes.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventhouses/{eventhouse_id}/getDefinition"  # noqa
    url = f"{url}?"
    if format is not None:
        url = f"{url}format={format}&"
    url = url.rstrip("&?")

    method = "get"
    token = get_fabric_bearer_token()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

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
        case 202:
            if await_lro is True:
                operation_id = response.headers["x-ms-operation-id"]
                retry_after = response.headers["Retry-After"]
                return wait_for_long_running_operation(
                    operation_id=operation_id, retry_after=retry_after, timeout=timeout
                )
            return response
        case _:
            return response


def eventhouse_update_definition(
    workspace_id: str,
    eventhouse_id: str,
    eventhouse_path: str,
    update_metadata: bool = None,
    await_lro: bool = None,
    timeout: int = 60 * 5,
    preview: bool = True,
) -> requests.Response:
    """
    Update the definition of an eventhouse.

    Args:
        workspace_id (str): The id of the workspace to update.
        eventhouse_id (str): The id of the eventhouse to update.
        eventhouse_path (str): The path to the eventhouse to load content from.
        update_metadata (bool | None): When set to true, the item's metadata is updated using the metadata in the .platform file.
        await_lro (bool | None): Whether to await the long running operation.
        timeout (int): Timeout for the long running operation (seconds). Defaults to 5 minutes.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/eventhouses/{eventhouse_id}/updateDefinition"  # noqa
    url = f"{url}?"
    if update_metadata is not None:
        url = f"{url}updateMetadata={update_metadata}&"
    url = url.rstrip("&?")

    method = "post"
    token = get_fabric_bearer_token()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    with open(eventhouse_path.rstrip("/") + "/EventhouseProperties.json", "r") as f:
        EventhouseProperties = base64.b64encode(f.read().encode()).decode()

    with open(eventhouse_path.rstrip("/") + "/.platform", "r") as f:
        platform = base64.b64encode(f.read().encode()).decode()

    data = {}
    custom_payload = {
        "definition": {
            "parts": [
                {
                    "path": "EventhouseProperties.json",
                    "payload": EventhouseProperties,
                    "payloadType": "InlineBase64",
                },
                {"path": ".platform", "payload": platform, "payloadType": "InlineBase64"},
            ]
        }
    }
    data = {**data, **custom_payload}

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
        case 202:
            if await_lro is True:
                operation_id = response.headers["x-ms-operation-id"]
                retry_after = response.headers["Retry-After"]
                return wait_for_long_running_operation(
                    operation_id=operation_id, retry_after=retry_after, timeout=timeout
                )
            return response
        case _:
            return response
