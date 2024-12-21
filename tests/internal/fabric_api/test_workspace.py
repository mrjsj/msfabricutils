import os

from dotenv import load_dotenv

from msfabricutils.core.workspace import get_workspace, get_workspaces

load_dotenv()

WORKSPACE_ID = os.getenv("PYTEST_WORKSPACE_ID")
WORKSPACE_NAME = os.getenv("PYTEST_WORKSPACE_NAME")

def test_get_workspaces():
    workspaces = get_workspaces()
    
    assert len(workspaces) > 0
    assert isinstance(workspaces, list)

def test_get_workspace_by_id():
    workspace = get_workspace(workspace_id=WORKSPACE_ID)

    assert isinstance(workspace, dict)
    assert workspace is not None

def test_get_workspace_by_name():
    workspace = get_workspace(workspace_name=WORKSPACE_NAME)

    assert isinstance(workspace, dict)
    assert workspace is not None
