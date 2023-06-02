import pytest
from src.models import ProductType
from main import app


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

    # Retrieve the product from the database based on the ID provided in the response
    product_id = response.json().get('id')
    product = app.state.mongo_collection.find_one({'_id': product_id})
    assert product is not None
    assert product['name'] == product_data['name']
    assert product['price'] == product_data['price']
    assert product['type'] == product_data['type']
    assert product['region'] == product_data['region']
