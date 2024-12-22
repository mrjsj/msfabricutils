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

    workspace = [workspace for workspace in workspaces if workspace["id"] == WORKSPACE_ID]

    assert len(workspace) == 1
    assert isinstance(workspace[0], dict)
    assert workspace[0]["displayName"] == WORKSPACE_NAME
    assert workspace[0]["id"] == WORKSPACE_ID

def test_get_workspace_by_id():
    workspace = get_workspace(workspace_id=WORKSPACE_ID)

    assert isinstance(workspace, dict)
    assert workspace is not None

    assert workspace["displayName"] == WORKSPACE_NAME
    assert workspace["id"] == WORKSPACE_ID

def test_get_workspace_by_name():
    workspace = get_workspace(workspace_name=WORKSPACE_NAME)

    assert isinstance(workspace, dict)
    assert workspace is not None

    assert workspace["displayName"] == WORKSPACE_NAME
    assert workspace["id"] == WORKSPACE_ID