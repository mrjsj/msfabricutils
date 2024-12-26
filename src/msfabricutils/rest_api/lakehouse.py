import json
from typing import List

import requests
import typer

from msfabricutils import get_fabric_bearer_token
from msfabricutils.common.remove_none import remove_none
from msfabricutils.common.shorten_dict_values import shorten_dict_values
from msfabricutils.core.operations import wait_for_long_running_operation


def lakehouse_create(
    workspace_id: str,
    display_name: str,
    description: str = None,
    enable_schemas: bool = None,
    await_lro: bool = None,
    timeout: int = 60 * 5,
    preview: bool = True,
) -> requests.Response:
    """
    Create a lakehouse.

    Args:
        workspace_id (str): The id of the workspace to create the lakehouse in.
        display_name (str): The display name of the lakehouse.
        description (str | None): The description of the lakehouse.
        enable_schemas (bool | None): Whether the lakehouse is schema enabled.
        await_lro (bool | None): Whether to await the long running operation.
        timeout (int): Timeout for the long running operation (seconds). Defaults to 5 minutes.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses"  # noqa
    url = f"{url}?"
    url = url.rstrip("&?")

    method = "post"
    token = get_fabric_bearer_token()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    data = {}
    data["displayName"] = display_name
    data["description"] = description
    if enable_schemas is True:
        custom_payload = {
            "enableSchemas": True,
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


def lakehouse_get(
    workspace_id: str,
    lakehouse_id: str,
    preview: bool = True,
) -> requests.Response:
    """
    Get a lakehouse.

    Args:
        workspace_id (str): The id of the workspace to get the lakehouse from.
        lakehouse_id (str): The id of the lakehouse to get.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}"  # noqa
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


def lakehouse_list(
    workspace_id: str,
    continuation_token: str = None,
    preview: bool = True,
) -> requests.Response:
    """
    List lakehouses for a workspace.

    Args:
        workspace_id (str): The id of the workspace to list lakehouses for.
        continuation_token (str | None): A token for retrieving the next page of results.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses"  # noqa
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


def lakehouse_update(
    workspace_id: str,
    lakehouse_id: str,
    display_name: str = None,
    description: str = None,
    preview: bool = True,
) -> requests.Response:
    """
    Update a lakehouse.

    Args:
        workspace_id (str): The id of the workspace to update.
        lakehouse_id (str): The id of the lakehouse to update.
        display_name (str | None): The display name of the lakehouse.
        description (str | None): The description of the lakehouse.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}"  # noqa
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


def lakehouse_delete(
    workspace_id: str,
    lakehouse_id: str,
    preview: bool = True,
) -> requests.Response:
    """
    Delete a lakehouse.

    Args:
        workspace_id (str): The id of the workspace to delete.
        lakehouse_id (str): The id of the lakehouse to delete.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}"  # noqa
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


def lakehouse_run_background_job(
    workspace_id: str,
    lakehouse_id: str,
    job_type: str,
    table_name: str,
    schema_name: str = None,
    v_order: bool = None,
    z_order_columns: List[str] = None,
    retention_period: str = None,
    await_lro: bool = None,
    timeout: int = 60 * 5,
    preview: bool = True,
) -> requests.Response:
    """
    Run on-demand table maintenance job instance.

    Args:
        workspace_id (str): The id of the workspace to create a job for.
        lakehouse_id (str): The id of the lakehouse to create a job for.
        job_type (str): The type of the job to create. Must be \"TableMaintenance\".
        table_name (str): The name of the table to run the job on.
        schema_name (str | None): The name of the schema to run the job on. Only applicable for schema enabled lakehouses.
        v_order (bool | None): If table should be v-ordered.
        z_order_columns (List[str] | None): List of columns to z-order by.
        retention_period (str | None): Retention periode in format d:hh:mm:ss. Overrides the default retention period.
        await_lro (bool | None): Whether to await the long running operation.
        timeout (int): Timeout for the long running operation (seconds). Defaults to 5 minutes.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/jobs/instances"  # noqa
    url = f"{url}?"
    if job_type is not None:
        url = f"{url}jobType={job_type}&"
    url = url.rstrip("&?")

    method = "post"
    token = get_fabric_bearer_token()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    data = {}
    custom_payload = {
        "executionData": {
            "tableName": table_name,
            "schemaName": schema_name,
            "optimizeSettings": {"vOrder": v_order, "zOrderBy": z_order_columns},
            "vacuumSettings": {"retentionPeriod": retention_period},
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


def lakehouse_list_tables(
    workspace_id: str,
    lakehouse_id: str,
    continuation_token: str = None,
    max_results: int = None,
    preview: bool = True,
) -> requests.Response:
    """
    List tables in a lakehouse.

    Args:
        workspace_id (str): The id of the workspace to list tables for.
        lakehouse_id (str): The id of the lakehouse to list tables for.
        continuation_token (str | None): A token for retrieving the next page of results.
        max_results (int | None): The maximum number of results to return.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/tables"  # noqa
    url = f"{url}?"
    if continuation_token is not None:
        url = f"{url}continuationToken={continuation_token}&"
    if max_results is not None:
        url = f"{url}maxResults={max_results}&"
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


def lakehouse_load_table(
    workspace_id: str,
    lakehouse_id: str,
    table_name: str,
    relative_path: str,
    path_type: str,
    format: str = None,
    header: bool = None,
    delimiter: str = None,
    mode: str = None,
    file_extension: str = None,
    recursive: bool = None,
    await_lro: bool = None,
    timeout: int = 60 * 5,
    preview: bool = True,
) -> requests.Response:
    """
    Load a table.

    Args:
        workspace_id (str): The id of the workspace to load the table for.
        lakehouse_id (str): The id of the lakehouse to load the table for.
        table_name (str): The name of the table to load.
        relative_path (str): The relative path to the table to load.
        path_type (str): The type of the path to load. Either \"File\" or \"Folder\".
        format (str | None): The format of the files to load. Must be \"Parquet\" or \"Csv\".
        header (bool | None): Whether the file has a header row. Only applicable for csv files.
        delimiter (str | None): The delimiter of the csv files. Only applicable for csv files.
        mode (str | None): The mode to load the table in. Either \"Overwrite\" or \"Append\".
        file_extension (str | None): The file extension of the files to load.
        recursive (bool | None): Whether to search data files recursively or not, when loading from a folder.
        await_lro (bool | None): Whether to await the long running operation.
        timeout (int): Timeout for the long running operation (seconds). Defaults to 5 minutes.
        preview (bool): Whether to preview the request. You will be asked to confirm the request before it is executed. Defaults to True.

    Returns:
        The response from the request.
    """

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/tables/{table_name}/load"  # noqa
    url = f"{url}?"
    url = url.rstrip("&?")

    method = "post"
    token = get_fabric_bearer_token()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    data = {}
    data["relativePath"] = relative_path
    data["pathType"] = path_type
    data["format"] = format
    data["header"] = header
    data["delimiter"] = delimiter
    data["mode"] = mode
    data["fileExtension"] = file_extension
    data["recursive"] = recursive

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
