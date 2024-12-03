from azure.identity import DefaultAzureCredential


def get_onelake_access_token() -> str:
    """
    Retrieves an access token for Azure OneLake storage.

    This function attempts to obtain an access token for accessing Azure storage. 
    It first checks if the code is running in a Microsoft Fabric notebook environment 
    and attempts to use the `notebookutils` library to get the token. If the library 
    is not available, it falls back to using the `DefaultAzureCredential` from the Azure SDK 
    to fetch the token.

    Returns:
        str: The access token used for authenticating requests to Azure OneLake storage.
    """    
    audience = "https://storage.azure.com"
    try:
        import notebookutils # type: ignore

        token = notebookutils.credentials.getToken(audience)
    except ModuleNotFoundError:
        token = DefaultAzureCredential().get_token(f"{audience}/.default").token

    return token


def get_fabric_bearer_token() -> str:
    """
    Retrieves a bearer token for Azure Fabric (Power BI) API.

    This function attempts to obtain a bearer token for authenticating requests to the 
    Azure Power BI API. It first checks if the code is running in a Microsoft Fabric 
    notebook environment and tries to use the `notebookutils` library to get the token. 
    If the library is not available, it falls back to using the `DefaultAzureCredential` 
    from the Azure SDK to fetch the token.

    Returns:
        str: The bearer token used for authenticating requests to the Azure Fabric (Power BI) API.
    """    
    audience = "https://analysis.windows.net/powerbi/api"
    try:
        import notebookutils # type: ignore

        token = notebookutils.credentials.getToken(audience)
    except ModuleNotFoundError:
        token = DefaultAzureCredential().get_token(f"{audience}/.default").token

    return token
