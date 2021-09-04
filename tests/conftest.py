"""
tests.conftest.py
~~~~~~~~~~~~~~~~~
Shared testing fixtures
"""
import pathlib

import pytest

ROOT = pathlib.Path(__file__).parents[1]
# TODO: don't rely on specific database path or name
SQLITE_DB = ROOT / "database.db"


@pytest.fixture(scope="session")
def monkey_session():
    """Session scoped monkeypatch"""
    with pytest.MonkeyPatch.context() as monkeypatch:
        yield monkeypatch


@pytest.fixture(scope="session", autouse=True)
def session_setup_teardown():
    # setup
    if SQLITE_DB.exists():
        SQLITE_DB.unlink()  # missing_ok py 3.8
    # yield
    yield
    # teardown
    if SQLITE_DB.exists():
        SQLITE_DB.unlink()
