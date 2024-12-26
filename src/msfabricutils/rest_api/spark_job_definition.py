import base64
import json

import requests
import typer

from msfabricutils import get_fabric_bearer_token
from msfabricutils.common.remove_none import remove_none
from msfabricutils.common.shorten_dict_values import shorten_dict_values
from msfabricutils.core.operations import wait_for_long_running_operation


def spark_job_definition_create(
    workspace_id: str,
    display_name: str,
    spark_job_definition_path: str,
    description: str = None,
    await_lro: bool = None,
    timeout: int = 60 * 5,
    preview: bool = True,
) -> requests.Response:
    """
    Create a spark job definition.

    Args:
        workspace_id (str): The id of the workspace to create the spark job definition in.
        display_name (str): The display name of the spark job definition.
        spark_job_definition_path (str): The path to the spark job definition to load content from.
        description (str | None): The description of the spark job definition.
        await_lro (bool | None): Whether to await the long running operation.
        timeout (int): Timeout for the long running operation (seconds). Defaults to 5 minutes.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/sparkJobDefinitions"  # noqa
    url = f"{url}?"
    url = url.rstrip("&?")

    method = "post"
    token = get_fabric_bearer_token()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    with open(spark_job_definition_path.rstrip("/") + "/SparkJobDefinitionV1.json", "r") as f:
        SparkJobDefinitionV1 = base64.b64encode(f.read().encode()).decode()

    with open(spark_job_definition_path.rstrip("/") + "/.platform", "r") as f:
        platform = base64.b64encode(f.read().encode()).decode()

    data = {}
    data["displayName"] = display_name
    data["description"] = description
    custom_payload = {
        "definition": {
            "parts": [
                {
                    "path": "SparkJobDefinitionV1.json",
                    "payload": SparkJobDefinitionV1,
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


def spark_job_definition_get(
    workspace_id: str,
    spark_job_definition_id: str,
    preview: bool = True,
) -> requests.Response:
    """
    Get a spark job definition.

    Args:
        workspace_id (str): The id of the workspace to get the spark job definition from.
        spark_job_definition_id (str): The id of the spark job definition to get.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/sparkJobDefinitions/{spark_job_definition_id}"  # noqa
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


def spark_job_definition_list(
    workspace_id: str,
    continuation_token: str = None,
    preview: bool = True,
) -> requests.Response:
    """
    List spark job definitions for a workspace.

    Args:
        workspace_id (str): The id of the workspace to list spark job definitions for.
        continuation_token (str | None): A token for retrieving the next page of results.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/sparkJobDefinitions"  # noqa
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


def spark_job_definition_update(
    workspace_id: str,
    spark_job_definition_id: str,
    display_name: str = None,
    description: str = None,
    preview: bool = True,
) -> requests.Response:
    """
    Update a spark job definition.

    Args:
        workspace_id (str): The id of the workspace to update.
        spark_job_definition_id (str): The id of the spark job definition to update.
        display_name (str | None): The display name of the spark job definition.
        description (str | None): The description of the spark job definition.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/sparkJobDefinitions/{spark_job_definition_id}"  # noqa
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


def spark_job_definition_delete(
    workspace_id: str,
    spark_job_definition_id: str,
    preview: bool = True,
) -> requests.Response:
    """
    Delete a spark job definition.

    Args:
        workspace_id (str): The id of the workspace to delete.
        spark_job_definition_id (str): The id of the spark job definition to delete.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/sparkJobDefinitions/{spark_job_definition_id}"  # noqa
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


def spark_job_definition_get_definition(
    workspace_id: str,
    spark_job_definition_id: str,
    await_lro: bool = None,
    timeout: int = 60 * 5,
    preview: bool = True,
) -> requests.Response:
    """
    Get the definition of a spark job definition.

    Args:
        workspace_id (str): The id of the workspace to get the spark job definition definition from.
        spark_job_definition_id (str): The id of the spark job definition to get the definition from.
        await_lro (bool | None): Whether to await the long running operation.
        timeout (int): Timeout for the long running operation (seconds). Defaults to 5 minutes.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/sparkJobDefinitions/{spark_job_definition_id}/getDefinition"  # noqa
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


def spark_job_definition_update_definition(
    workspace_id: str,
    spark_job_definition_id: str,
    spark_job_definition_path: str,
    update_metadata: bool = None,
    await_lro: bool = None,
    timeout: int = 60 * 5,
    preview: bool = True,
) -> requests.Response:
    """
    Update the definition of a spark job definition.

    Args:
        workspace_id (str): The id of the workspace to update.
        spark_job_definition_id (str): The id of the spark job definition to update.
        spark_job_definition_path (str): The path to the spark job definition to load content from.
        update_metadata (bool | None): When set to true, the item's metadata is updated using the metadata in the .platform file.
        await_lro (bool | None): Whether to await the long running operation.
        timeout (int): Timeout for the long running operation (seconds). Defaults to 5 minutes.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/sparkJobDefinitions/{spark_job_definition_id}/updateDefinition"  # noqa
    url = f"{url}?"
    if update_metadata is not None:
        url = f"{url}updateMetadata={update_metadata}&"
    url = url.rstrip("&?")

    method = "post"
    token = get_fabric_bearer_token()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    with open(spark_job_definition_path.rstrip("/") + "/SparkJobDefinitionV1.json", "r") as f:
        SparkJobDefinitionV1 = base64.b64encode(f.read().encode()).decode()

    with open(spark_job_definition_path.rstrip("/") + "/.platform", "r") as f:
        platform = base64.b64encode(f.read().encode()).decode()

    data = {}
    custom_payload = {
        "definition": {
            "parts": [
                {
                    "path": "SparkJobDefinitionV1.json",
                    "payload": SparkJobDefinitionV1,
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


def spark_job_definition_run_background_job(
    workspace_id: str,
    spark_job_definition_id: str,
    job_type: str,
    await_lro: bool = None,
    timeout: int = 60 * 5,
    preview: bool = True,
) -> requests.Response:
    """
    Run on-demand spark job instance.

    Args:
        workspace_id (str): The id of the workspace to create a job for.
        spark_job_definition_id (str): The id of the spark job definition to create a job for.
        job_type (str): The type of the job to create. Must be \"sparkJob\".
        await_lro (bool | None): Whether to await the long running operation.
        timeout (int): Timeout for the long running operation (seconds). Defaults to 5 minutes.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/sparkJobDefinitions/{spark_job_definition_id}/jobs/instances"  # noqa
    url = f"{url}?"
    if job_type is not None:
        url = f"{url}jobType={job_type}&"
    url = url.rstrip("&?")

    method = "post"
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
