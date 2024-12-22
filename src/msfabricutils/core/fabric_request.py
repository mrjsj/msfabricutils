import logging

import requests

from msfabricutils.core.auth import get_fabric_bearer_token


def paginated_get_request(endpoint: str, data_key: str) -> list[dict[str, str]]:
    """
    Retrieves paginated data from the specified API endpoint.

    This function makes repeated GET requests to the specified endpoint of the
    Fabric REST API, handling pagination automatically. It uses a bearer token
    for authentication and retrieves data from each page, appending the results
    to a list. Pagination continues until no `continuationToken` is returned.

    Args:
        endpoint (str): The API endpoint to retrieve data from.
        data_key (str): The key in the response JSON that contains the list of data to be returned.

    Returns:
        A list of dictionaries containing the data from all pages.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
    """
    base_url = "https://api.fabric.microsoft.com/v1"
    token = get_fabric_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}

    responses = []
    continuation_token = None
    while True:
        params = {"continuationToken": continuation_token} if continuation_token else {}

        response = requests.get(f"{base_url}/{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        data: dict = response.json()

        responses.extend(data.get(data_key))

        continuation_token = data.get("continuationToken")
        if not continuation_token:
            break

    return responses


def get_item_from_paginated_get_request(endpoint: str, data_key: str, item_key: str, item_value: str) -> dict[str, str]:
    """
    Recursively paginates the API endpoint until specified item is found and returns it.

    This function makes repeated GET requests to the specified endpoint of the
    Fabric REST API, handling pagination automatically. It uses a bearer token
    for authentication and retrieves data from each page, appending the results
    to a list. Pagination continues until the specified item is found or no
    `continuationToken` is returned.

    Args:
        endpoint (str): The API endpoint to retrieve data from.
        data_key (str): The key in the response JSON that contains the list of data to be returned.
        item_key (str): The key in the data dictionary that contains the item to be returned.
        item_value (str): The value of the item to be returned.

    Returns:
        A dictionary containing the item to be returned.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
        ValueError: If the item is not found.
    """
    base_url = "https://api.fabric.microsoft.com/v1"
    token = get_fabric_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}

    continuation_token = None
    while True:
        params = {"continuationToken": continuation_token} if continuation_token else {}

        response = requests.get(f"{base_url}/{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        data: dict = response.json()

        for item in data.get(data_key):
            if item.get(item_key) == item_value:
                return item

        continuation_token = data.get("continuationToken")
        if not continuation_token:
            break

    raise ValueError(f"Item with {item_key} {item_value} not found")


def get_request(endpoint: str, content_only: bool = True) -> requests.Response | dict[str, str]:
    """
    Retrieves data from a specified API endpoint.

    This function makes a GET request to the specified endpoint of the Azure Fabric API,
    using a bearer token for authentication. It returns the JSON response as a list of
    dictionaries containing the data returned by the API.

    Args:
        endpoint (str): The API endpoint to send the GET request to.
        content_only (bool): Whether to return the content of the response only.
    
    Returns:
        A list of dictionaries containing the data returned from the API or the response object.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
    """
    base_url = "https://api.fabric.microsoft.com/v1"
    token = get_fabric_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {}

    response = requests.get(f"{base_url}/{endpoint}", headers=headers, params=params)

    if content_only:
        if response.status_code >= 400:
            logging.error(f"Request failed with status code {response.status_code}: {response.json()}")
        response.raise_for_status()
        return response.json()

    return response


def post_request(endpoint: str, data: dict[str, str], content_only: bool = True) -> requests.Response | dict[str, str]:
    """
    Sends a POST request to a specified API endpoint.

    This function makes a POST request to the specified endpoint of the Azure Fabric API,
    using a bearer token for authentication. It sends the provided data in JSON format
    and returns either the JSON response or the full response object.

    Args:
        endpoint (str): The API endpoint to send the POST request to.
        data (dict[str, str]): The data to be sent in the request body.
        content_only (bool): Whether to return the content of the response only.

    Returns:
        Either the JSON response as a dictionary or the full response object.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
    """
    base_url = "https://api.fabric.microsoft.com/v1"
    token = get_fabric_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(f"{base_url}/{endpoint}", headers=headers, json=data)

    if content_only:
        if response.status_code >= 400:
            logging.error(f"Request failed with status code {response.status_code}: {response.json()}")
        response.raise_for_status()
        return response.json()

    return response


def patch_request(endpoint: str, data: dict[str, str], content_only: bool = True) -> requests.Response | dict[str, str]:
    """
    Sends a PATCH request to a specified API endpoint.

    This function makes a PATCH request to the specified endpoint of the Azure Fabric API,
    using a bearer token for authentication. It sends the provided data in JSON format
    and returns either the JSON response or the full response object.

    Args:
        endpoint (str): The API endpoint to send the PATCH request to.
        data (dict[str, str]): The data to be sent in the request body.
        content_only (bool): Whether to return the content of the response only.

    Returns:
        Either the JSON response as a dictionary or the full response object.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
    """
    base_url = "https://api.fabric.microsoft.com/v1"
    token = get_fabric_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.patch(f"{base_url}/{endpoint}", headers=headers, json=data)

    if content_only:
        if response.status_code >= 400:
            logging.error(f"Request failed with status code {response.status_code}: {response.json()}")
        response.raise_for_status()
        return response.json()

    return response


def delete_request(endpoint: str) -> requests.Response:
    """
    Sends a DELETE request to a specified API endpoint.

    This function makes a DELETE request to the specified endpoint of the Azure Fabric API,
    using a bearer token for authentication.

    Args:
        endpoint (str): The API endpoint to send the DELETE request to.

    Returns:
        The response object from the DELETE request.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or returns an error.
    """
    base_url = "https://api.fabric.microsoft.com/v1"
    token = get_fabric_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.delete(f"{base_url}/{endpoint}", headers=headers)
    if response.status_code >= 400:
        logging.error(f"Request failed with status code {response.status_code}: {response.json()}")
    response.raise_for_status()
    return response
