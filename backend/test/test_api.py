import pytest
import json
from httpx import Response
from fastapi.testclient import TestClient
from backend.main import app
from datetime import datetime

client = TestClient(app)

with open("test/data/mock_response.json", "r") as f:
    mock_response = json.load(f)

@pytest.mark.asyncio
async def test_api_fetching_success():

    response = client.get("/forecast?lat=-37.8&lng=145.0&days=5")
    assert response.status_code == 200

    # checking for correct json filtering
    json = response.json()
    for date_str, value in json.items():
        # Validate date format
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            pytest.fail(f"Invalid date format: {date_str}")

        # Validate integer range
        assert isinstance(value, int), f"Value is not int: {value}"
        assert 0 <= value <= 5, f"Value out of range: {value}"


def test_invalid_lat_lng_range():
    response = client.get("/forecast?lat=999&lng=200")
    assert response.status_code == 400


def test_lat_lng_type_validation():
    response = client.get("/forecast?lat=abc&lng=hello")
    assert response.status_code == 422  # automatic FastAPI validation


def test_outside_australia_bounds():
    # Example: New York City coordinates
    response = client.get("/forecast?lat=40.7&lng=-74.0")

    assert response.status_code == 400
    assert "outside australia" in response.json()["detail"].lower()