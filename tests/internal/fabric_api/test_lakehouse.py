import os

from dotenv import load_dotenv

from msfabricutils.core.lakehouse import get_workspace_lakehouse_tables, get_workspace_lakehouses

load_dotenv()

WORKSPACE_ID = os.getenv("PYTEST_WORKSPACE_ID")
WORKSPACE_NAME = os.getenv("PYTEST_WORKSPACE_NAME")
LAKEHOUSE_ID = os.getenv("PYTEST_LAKEHOUSE_ID")
LAKEHOUSE_NAME = os.getenv("PYTEST_LAKEHOUSE_NAME")

def test_get_workspace_lakehouses():
    lakehouses = get_workspace_lakehouses(workspace_name=WORKSPACE_NAME)
    assert isinstance(lakehouses, list)
    assert len(lakehouses) > 0

def test_get_workspace_lakehouses_by_id():
    lakehouses = get_workspace_lakehouses(workspace_id=WORKSPACE_ID)
    assert isinstance(lakehouses, list)
    assert len(lakehouses) > 0

def test_get_workspace_lakehouses_by_name():
    lakehouses = get_workspace_lakehouses(workspace_name=WORKSPACE_NAME)
    assert isinstance(lakehouses, list)
    assert len(lakehouses) > 0

def test_get_workspace_lakehouse_tables_by_workspace_id_and_lakehouse_id():
    lakehouse = get_workspace_lakehouse_tables(workspace_id=WORKSPACE_ID, lakehouse_id=LAKEHOUSE_ID)
    assert isinstance(lakehouse, list)
    assert len(lakehouse) > 0

def test_get_workspace_lakehouse_tables_by_workspace_id_and_lakehouse_name():
    lakehouse = get_workspace_lakehouse_tables(workspace_id=WORKSPACE_ID, lakehouse_name=LAKEHOUSE_NAME)
    assert isinstance(lakehouse, list)
    assert len(lakehouse) > 0

def test_get_workspace_lakehouse_tables_by_workspace_name_and_lakehouse_id():
    lakehouse = get_workspace_lakehouse_tables(workspace_name=WORKSPACE_NAME, lakehouse_id=LAKEHOUSE_ID)
    assert isinstance(lakehouse, list)
    assert len(lakehouse) > 0

def test_get_workspace_lakehouse_tables_by_workspace_name_and_lakehouse_name():
    lakehouse = get_workspace_lakehouse_tables(workspace_name=WORKSPACE_NAME, lakehouse_name=LAKEHOUSE_NAME)
    assert isinstance(lakehouse, list)
    assert len(lakehouse) > 0
