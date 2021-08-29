"""tests.test_basic.py"""
from pprint import pformat as pf

import pytest
from fastapi.testclient import TestClient

from api.main import APP, get_config


@pytest.mark.parametrize(
    "database_url",
    [
        "postgres://localhost",
        "postgresql://localhost:5432",
        "postgres://user@localhost/got",
        "sqlite:///database.db",
        "sqlite://",
    ],
)
def test_database_url(database_url: str):
    config = get_config(database_url=database_url)

    if database_url.startswith("postgres"):
        assert config.database_url.startswith("postgresql://")
    else:
        assert config.database_url == database_url


@pytest.fixture
def api_client() -> TestClient:
    return TestClient(APP)


@pytest.mark.parametrize(
    "path, expected", [("/", 200), ("/docs", 200), ("/houses", 200)]
)
def test_status_codes(api_client, path, expected):
    response = api_client.get(path)
    print(f"{response.request.url} -> {response}")
    assert response.status_code == expected


@pytest.mark.parametrize(
    "query_params",
    [
        {},
        {"limit": None},
        {"limit": None, "skip": None},
        {"limit": 0},
        {"limit": 0, "skip": 0},
        {"limit": 1},
        {"limit": 1, "skip": 1},
        {"limit": 999},
        {"limit": 1, "skip": 999},
    ],
)
def test_get_houses(api_client, query_params):
    response = api_client.get("/houses", params=query_params)
    print(f"{response.request.url} -> {response}")

    houses = response.json()
    print(f"\n {pf(houses)}")

    limit = query_params.get("limit")
    if limit is None:
        assert houses
    else:
        assert len(houses) <= limit


if __name__ == "__main__":
    pytest.main(["--vv"])
