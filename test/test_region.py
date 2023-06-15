import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_region_default(client):
    response = client.get("/inflation")
    assert response.status_code == 200
    assert response.json() == {'region': 'all'}


def test_region_eu():
    response = client.get("/inflation?region=eu")
    assert response.status_code == 200
    assert response.json() == {'region': 'eu'}


def test_calculate_inflation_all():
    response = client.get("/inflation")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    assert len(products) > 0

    for product in products:
        assert "Product" in product
        assert "Type" in product
        assert "Current Price" in product
        assert "Previous Prices" in product
        assert "Inflation" in product


def test_calculate_inflation_food():
    response = client.get("/inflation?type_product=FOOD")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    assert len(products) > 0

    for product in products:
        assert "Product" in product
        assert "Type" in product
        assert product["Type"] == "FOOD"
        assert "Current Price" in product
        assert "Previous Prices" in product
        assert "Inflation" in product


def test_calculate_inflation_nonexistent_type():
    response = client.get("/inflation?type_product=NONEXISTENT")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    assert len(products) == 0