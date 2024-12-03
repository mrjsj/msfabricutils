from azure.identity import DefaultAzureCredential


def get_onelake_access_token():
    audience = "https://storage.azure.com"
    try:
        import notebookutils

        token = notebookutils.credentials.getToken(audience)
    except ModuleNotFoundError:
        token = DefaultAzureCredential().get_token(f"{audience}/.default").token

    return token


def get_fabric_bearer_token():
    audience = "https://analysis.windows.net/powerbi/api"
    try:
        import notebookutils

        token = notebookutils.credentials.getToken(audience)
    except ModuleNotFoundError:
        token = DefaultAzureCredential().get_token(f"{audience}/.default").token

    return token
