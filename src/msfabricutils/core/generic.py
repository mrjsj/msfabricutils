import requests
from msfabricutils.core.auth import get_fabric_bearer_token


def get_paginated(endpoint: str, data_key: str) -> list[dict]:
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


def get_page(endpoint: str) -> list[dict]:
    base_url = "https://api.fabric.microsoft.com/v1"
    token = get_fabric_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {}

    response = requests.get(f"{base_url}/{endpoint}", headers=headers, params=params)
    response.raise_for_status()

    return response.json()
