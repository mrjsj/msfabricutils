import os

from azure.core.exceptions import ClientAuthenticationError
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
    Alias for `get_azure_storage_access_token`
    """
    return get_azure_storage_access_token()

def get_azure_storage_access_token() -> str:
    """
    Retrieves an access token for Azure Storage.

    This function attempts to obtain an access token for accessing Azure storage.
    It first checks if the `AZURE_STORAGE_TOKEN` environment variable is set.
    Otherwise, it tries to get the token using `notebookutils.credentials.getToken`.
    Lastly, it falls back to using the `DefaultAzureCredential`.

    Returns:
        The access token used for authenticating requests to Azure Storage.
    """

    token = os.environ.get("AZURE_STORAGE_TOKEN")
    if token:
        return token
    
    try:
        audience = "https://storage.azure.com"
        return get_access_token(audience)
    except ClientAuthenticationError as e:
        raise ClientAuthenticationError(
            f"{str(e)}\n\n"
            "Additional troubleshooting steps:\n"
            "1. Ensure you can use any of the credentials methods to get an access token\n"
            "2. Set the `AZURE_STORAGE_TOKEN` environment variable with a valid access token"
        ) from e



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
    Retrieves a bearer token for Azure DevOps.

    This function attempts to obtain a bearer token for authenticating requests to Azure DevOps.

    Returns:
        The bearer token used for authenticating requests to Azure DevOps.
    """
    audience = "499b84ac-1321-427f-aa17-267ca6975798"
    return get_access_token(audience)


def get_storage_options() -> dict[str, str]:
    """
    Retrieves storage options including a bearer token for Azure Storage.

    This function calls `get_azure_storage_access_token` to obtain a bearer token
    and returns a dictionary containing the token.

    Returns:
        A dictionary containing the storage options for Azure Storage.

    Example:
        **Retrieve storage options**
        ```python
        from msfabricutils import get_storage_options

        options = get_storage_options()
        options
        {"bearer_token": "your_token_here"}
        ```
    """
    return {"bearer_token": get_azure_storage_access_token(), "allow_invalid_certificates": "true"}
