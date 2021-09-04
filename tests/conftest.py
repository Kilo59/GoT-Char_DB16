"""
tests.conftest.py
~~~~~~~~~~~~~~~~~
Shared testing fixtures
"""
import pytest


@pytest.fixture(scope="session")
def monkey_session():
    """Session scoped monkeypatch"""
    with pytest.MonkeyPatch.context() as monkeypatch:
        yield monkeypatch
