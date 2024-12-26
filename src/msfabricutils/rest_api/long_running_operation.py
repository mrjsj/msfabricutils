import json

import requests
import typer

from msfabricutils import get_fabric_bearer_token
from msfabricutils.common.remove_none import remove_none
from msfabricutils.common.shorten_dict_values import shorten_dict_values


def long_running_operation_get_state(
    operation_id: str,
    preview: bool = True,
) -> requests.Response:
    """
    Get the state of the long running operation.

    Args:
        operation_id (str): The ID of the long running operation.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/operations/{operation_id}"  # noqa
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


def long_running_operation_get_result(
    operation_id: str,
    preview: bool = True,
) -> requests.Response:
    """
    Get the result of the long running operation. Only available when the operation status is `Succeeded`.

    Args:
        operation_id (str): The ID of the long running operation.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/operations/{operation_id}/result"  # noqa
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
