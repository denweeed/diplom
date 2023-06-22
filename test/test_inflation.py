import pytest
from fastapi.testclient import TestClient
from main import app
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_calculate_inflation_with_mock_data(monkeypatch):
    # Mock the mongo_collection.find method to return sample data
    def mock_find(query):
        return [
            {"price": 10},
            {"price": 20},
            {"price": 15}
        ]

    monkeypatch.setattr(app.state.mongo_collection, "find", mock_find)

    # Make a GET request to the /inflation endpoint
    response = client.get("/inflation")

    # Assert that the response status code is 200 OK
    assert response.status_code == 200

    # Assert that the response body contains the expected inflation rate
    expected_inflation_rate = 25.0
    assert response.json() == expected_inflation_rate
