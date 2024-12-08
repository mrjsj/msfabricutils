from azure.identity import DefaultAzureCredential


def get_access_token(audience: str) -> str:
    """
    Retrieves an access token for a given audience.

    This function attempts to obtain an access token for a given audience.
    It first checks if the code is running in a Microsoft Fabric notebook environment
    and attempts to use the `notebookutils` library to get the token. If the library
    is not available, it falls back to using the `DefaultAzureCredential` from the Azure SDK
    to fetch the token.
    """

    try:
        import notebookutils  # type: ignore

        token = notebookutils.credentials.getToken(audience)
    except ModuleNotFoundError:
        token = DefaultAzureCredential().get_token(f"{audience}/.default").token

    return token


def get_onelake_access_token() -> str:
    """
    Retrieves an access token for OneLake storage.

    This function attempts to obtain an access token for accessing Azure storage.
    It first checks if the code is running in a Microsoft Fabric notebook environment
    and attempts to use the `notebookutils` library to get the token. If the library
    is not available, it falls back to using the `DefaultAzureCredential` from the Azure SDK
    to fetch the token.

    Returns:
        The access token used for authenticating requests to Azure OneLake storage.
    """
    audience = "https://storage.azure.com"
    return get_access_token(audience)


def get_fabric_bearer_token() -> str:
    """
    Retrieves a bearer token for Fabric (Power BI) API.

    This function attempts to obtain a bearer token for authenticating requests to the
    Power BI API. It first checks if the code is running in a Microsoft Fabric
    notebook environment and tries to use the `notebookutils` library to get the token.
    If the library is not available, it falls back to using the `DefaultAzureCredential`
    from the Azure SDK to fetch the token.

    Returns:
        The bearer token used for authenticating requests to the Fabric (Power BI) API.
    """
    audience = "https://analysis.windows.net/powerbi/api"
    return get_access_token(audience)


def get_azure_devops_access_token() -> str:
    """
    Retrieves a bearer token for Fabric (Power BI) API.

    This function attempts to obtain a bearer token for authenticating requests to the
    Power BI API. It first checks if the code is running in a Microsoft Fabric
    notebook environment and tries to use the `notebookutils` library to get the token.
    If the library is not available, it falls back to using the `DefaultAzureCredential`
    from the Azure SDK to fetch the token.

    Returns:
        The bearer token used for authenticating requests to the Azure Fabric (Power BI) API.
    """
    audience = "499b84ac-1321-427f-aa17-267ca6975798"
    return get_access_token(audience)


def get_storage_options() -> dict[str, str]:
    """
    Retrieves storage options including a bearer token for OneLake storage.

    This function calls `get_onelake_access_token` to obtain a bearer token
    and returns a dictionary containing the token and a flag indicating
    whether to use the Fabric endpoint.

    Returns:
        A dictionary containing the storage options for OneLake.

    Example:
        **Retrieve storage options**
        ```python
        from msfabricutils import get_storage_options

        options = get_storage_options()
        options
        {'bearer_token': 'your_token_here', 'use_fabric_endpoint': 'true'}
        ```
    """
    return {"bearer_token": get_onelake_access_token(), "use_fabric_endpoint": "true"}
