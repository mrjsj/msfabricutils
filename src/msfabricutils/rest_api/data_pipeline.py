import json

import requests
import typer

from msfabricutils import get_fabric_bearer_token
from msfabricutils.common.remove_none import remove_none
from msfabricutils.common.shorten_dict_values import shorten_dict_values
from msfabricutils.core.operations import wait_for_long_running_operation


def data_pipeline_create(
    workspace_id: str,
    display_name: str,
    description: str = None,
    await_lro: bool = None,
    timeout: int = 60 * 5,
    preview: bool = True,
) -> requests.Response:
    """
    Create a data pipeline.

    Args:
        workspace_id (str): The id of the workspace to create the data pipeline in.
        display_name (str): The display name of the data pipeline.
        description (str | None): The description of the data pipeline.
        await_lro (bool | None): Whether to await the long running operation.
        timeout (int): Timeout for the long running operation (seconds). Defaults to 5 minutes.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/dataPipelines"  # noqa
    url = f"{url}?"
    url = url.rstrip("&?")

    method = "post"
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


def data_pipeline_get(
    workspace_id: str,
    data_pipeline_id: str,
    preview: bool = True,
) -> requests.Response:
    """
    Get a data pipeline.

    Args:
        workspace_id (str): The id of the workspace to get the data pipeline from.
        data_pipeline_id (str): The id of the data pipeline to get.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/dataPipelines/{data_pipeline_id}"  # noqa
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


def data_pipeline_list(
    workspace_id: str,
    continuation_token: str = None,
    preview: bool = True,
) -> requests.Response:
    """
    List data pipelines for a workspace.

    Args:
        workspace_id (str): The id of the workspace to list data pipelines for.
        continuation_token (str | None): A token for retrieving the next page of results.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/dataPipelines"  # noqa
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


def data_pipeline_update(
    workspace_id: str,
    data_pipeline_id: str,
    display_name: str = None,
    description: str = None,
    preview: bool = True,
) -> requests.Response:
    """
    Update a data pipeline.

    Args:
        workspace_id (str): The id of the workspace to update the data pipeline in.
        data_pipeline_id (str): The id of the data pipeline to update.
        display_name (str | None): The display name of the data pipeline.
        description (str | None): The description of the data pipeline.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/dataPipelines/{data_pipeline_id}"  # noqa
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


def data_pipeline_delete(
    workspace_id: str,
    data_pipeline_id: str,
    preview: bool = True,
) -> requests.Response:
    """
    Delete a data pipeline.

    Args:
        workspace_id (str): The id of the workspace to delete the data pipeline from.
        data_pipeline_id (str): The id of the data pipeline to delete.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/dataPipelines/{data_pipeline_id}"  # noqa
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
