import pytest
from src.models import ProductType


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

    # Post the product data to the API endpoint
    response = client.post('/products', json=product_data)
    assert response.status_code == 201
    assert response.json() == product_data

    # Retrieve the product from the database
    added_product = client.app.state.mongo_collection.find_one({'name': product_data['name']})

    # Validate the retrieved product data
    assert added_product is not None
    assert added_product['name'] == product_data['name']
    assert added_product['price'] == product_data['price']
    assert added_product['type'] == product_data['type'].value
    assert added_product['region'] == product_data['region']