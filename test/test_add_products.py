import pytest
from src.models import ProductType
from main import get_product_from_database


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


def test_add_product_to_db(client):
    product_data = {
        'name': 'Product Name',
        'price': 9.99,
        'type': ProductType.FOOD,
        'region': 'Europe'
    }

    response = client.post('/products', json=product_data)
    assert response.status_code == 201
    assert response.json() == product_data

    product_id = response.json().get('id')
    added_product = get_product_from_database(product_id)
    assert added_product is not None
    assert added_product.name == product_data['name']
    assert added_product.price == product_data['price']
    assert added_product.type == product_data['type']
    assert added_product.region == product_data['region']
