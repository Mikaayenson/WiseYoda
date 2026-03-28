"""HTTP API (requires api extra)."""

import pytest

pytest.importorskip("fastapi")

from starlette.testclient import TestClient
from wise_yoda.api import build_app
from wise_yoda.wisdom import QUOTES_DB


@pytest.fixture
def client() -> TestClient:
    return TestClient(build_app(quotes_path=QUOTES_DB))


def test_health(client: TestClient) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_random(client: TestClient) -> None:
    r = client.get("/random")
    assert r.status_code == 200
    data = r.json()
    assert "description" in data
    assert "season" in data


def test_quote_404(client: TestClient) -> None:
    r = client.get("/quote", params={"season": 99, "episode": 99})
    assert r.status_code == 404


def test_search(client: TestClient) -> None:
    r = client.get("/search", params={"q": "fear"})
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_stats(client: TestClient) -> None:
    r = client.get("/stats")
    assert r.status_code == 200
    body = r.json()
    assert "total" in body
    assert "by_season" in body
