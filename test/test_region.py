import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture
def client():
    return TestClient(app)


def test_region_default():
    response = client.get("/inflation")
    assert response.status_code == 200
    assert response.json() == {'region': 'all'}


def test_region_eu():
    response = client.get("/inflation?region=eu")
    assert response.status_code == 200
    assert response.json() == {'region': 'eu'}
