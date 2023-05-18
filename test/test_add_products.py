import pytest
from fastapi.testclient import TestClient
from main import app
from src.models import ProductCreate


@pytest.fixture
def client():
    return TestClient(app)


def test_add_product_to_db(client):
    product_data = {
        'name': 'Product Name',
        'price': 9.99,
        'type': 'food',
        'region': 'Europe'
    }

    response = client.post('/products', json=product_data)
    assert response.status_code == 201
    assert response.json() == product_data


def test_add_product_with_negative_price(client):
    product_data = {
        'name': 'Product Name',
        'price': -9.99,
        'type': 'food',
        'region': 'Europe'
    }

    response = client.post('/products', json=product_data)
    assert response.status_code == 422


def test_add_product_with_empty_name(client):
    product_data = {
        'name': '',
        'price': 9.99,
        'type': 'food',
        'region': 'Europe'
    }

    response = client.post('/products', json=product_data)
    assert response.status_code == 422


def test_add_product_with_invalid_type(client):
    product_data = {
        'name': 'Product Name',
        'price': 9.99,
        'type': 'invalid_type',
        'region': 'Europe'
    }

    response = client.post('/products', json=product_data)
    assert response.status_code == 422
