import os

from dotenv import load_dotenv

from msfabricutils.core.sql_endpoint import get_workspace_sql_endpoints

load_dotenv()

WORKSPACE_ID = os.getenv("PYTEST_WORKSPACE_ID")
WORKSPACE_NAME = os.getenv("PYTEST_WORKSPACE_NAME")

def test_get_workspace_sql_endpoints_by_workspace_id():
    sql_endpoints = get_workspace_sql_endpoints(workspace_id=WORKSPACE_ID)
    assert isinstance(sql_endpoints, list)
    assert len(sql_endpoints) > 0

def test_get_workspace_sql_endpoints_by_workspace_name():
    sql_endpoints = get_workspace_sql_endpoints(workspace_name=WORKSPACE_NAME)
    assert isinstance(sql_endpoints, list)
    assert len(sql_endpoints) > 0