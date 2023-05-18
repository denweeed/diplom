import pytest
from fastapi.testclient import TestClient
from main import app
from src.models import ProductCreate

client = TestClient(app)


@pytest.fixture
def product_data():
    return {
        'name': 'Product Name',
        'price': 9.99,
        'type': 'food',
        'region': 'Europe'
    }


def test_add_product_to_db(product_data):
    response = client.post('/products', json=product_data)
    assert response.status_code == 201
    assert response.json() == product_data
