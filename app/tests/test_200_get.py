import re
import pickle
import pytest
import app.globals as globals_
from .load_graph import graph_b
from .base import client


@pytest.mark.parametrize("endpoint", [
    "/api/get/site",
    "/api/get/auds",
    "/api/get/ways",
    "/api/get/plans"
])
def test_200_get(endpoint):
    response = client.get(endpoint, params={
        "api_key":
            "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    })
    assert response.status_code == 200


@pytest.mark.parametrize("target", ["site", "auds", "ways", "plans"])
def test_get_stat(target):
    response = client.get("/api/get/stat", params={
        "api_key":
            "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
        "target": "site"
    })
    assert response.status_code == 200
    assert response.json()["unique_visitors"] == 1


def test_get_user_id():
    response = client.get("/api/get/user-id")
    assert response.status_code == 200
    assert response.json()["user_id"] is not None
    assert re.match(
        r"[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{8}",
        response.json()["user_id"]
    ) is not None


def test_get_popular():
    response = client.get("/api/get/popular")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_route():
    globals_.global_graph["BS"] = pickle.loads(graph_b)
    response = client.get("/api/get/route?from_=a-100&to=a-101")
    assert response.status_code == 200
    json_data = response.json()
    assert len(json_data["steps"]) == 1
    assert json_data["fullDistance"] == 855
