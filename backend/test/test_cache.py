import pytest
from fastapi.testclient import TestClient
from backend.main import app
from datetime import datetime
import geohash
import requests

client = TestClient(app)

# ============================================================
# Mock cache implementations (match real cache interfaces)
# ============================================================

class MockForecastCache:
    def __init__(self):
        self.store = {}
        self.load_calls = 0
        self.save_calls = 0

    def load_cache(self, key):
        self.load_calls += 1
        return self.store.get(key)

    def save_cache(self, key, value):
        self.save_calls += 1
        self.store[key] = value


class MockTilesCache:
    def __init__(self):
        self.store = {}
        self.load_calls = 0
        self.save_calls = 0

    def load_cache(self, tile_type, z, x, y):
        self.load_calls += 1
        return self.store.get((tile_type, z, x, y))

    def save_cache(self, tile_type, z, x, y, value):
        self.save_calls += 1
        self.store[(tile_type, z, x, y)] = value


# ============================================================
# Fixture: patch module-level caches
# ============================================================

@pytest.fixture
def patched_caches(monkeypatch):
    # IMPORTANT: adjust this import path if your file lives elsewhere
    from backend.app.services import google_pollen

    forecast_cache = MockForecastCache()
    tiles_cache = MockTilesCache()

    monkeypatch.setattr(google_pollen, "forecast_cache", forecast_cache)
    monkeypatch.setattr(google_pollen, "tiles_cache", tiles_cache)

    return forecast_cache, tiles_cache


# ============================================================
# Forecast cache tests
# ============================================================

def test_forecast_cache_miss(patched_caches, monkeypatch):
    forecast_cache, _ = patched_caches

    def mock_google_response(*args, **kwargs):
        class MockResp:
            def raise_for_status(self): pass
            def json(self):
                return {
                    "dailyInfo": [
                        {
                            "date": {"year": 2025, "month": 1, "day": 1},
                            "pollenTypeInfo": [
                                {
                                    "code": "GRASS",
                                    "indexInfo": {"value": 3}
                                }
                            ]
                        }
                    ]
                }
        return MockResp()

    monkeypatch.setattr(
        "backend.app.services.google_pollen.requests.get",
        mock_google_response
    )

    response = client.get("/forecast?lat=-37.8&lng=145.0")

    assert response.status_code == 200
    assert forecast_cache.load_calls == 1
    assert forecast_cache.save_calls == 1


def test_forecast_cache_hit(patched_caches, monkeypatch):
    forecast_cache, _ = patched_caches

    h = geohash.encode(-37.8, 145.0, precision=5)
    cached_payload = {"01/01/2025": 2}
    forecast_cache.store[h] = cached_payload

    def fail_if_called(*args, **kwargs):
        pytest.fail("External API should not be called on cache hit")

    monkeypatch.setattr(
        "backend.app.services.google_pollen.requests.get",
        fail_if_called
    )

    response = client.get("/forecast?lat=-37.8&lng=145.0")

    assert response.status_code == 200
    assert response.json() == cached_payload
    assert forecast_cache.load_calls == 1
    assert forecast_cache.save_calls == 0


def test_forecast_invalid_coordinates_skip_cache(patched_caches):
    forecast_cache, _ = patched_caches

    response = client.get("/forecast?lat=999&lng=999")

    assert response.status_code == 400
    assert forecast_cache.load_calls == 0
    assert forecast_cache.save_calls == 0


# ============================================================
# Tile cache tests
# ============================================================

def test_tile_cache_hit(patched_caches):
    _, tiles_cache = patched_caches

    png_bytes = b"\x89PNG\r\n\x1a\n"
    tiles_cache.store[("grass", 1, 2, 3)] = png_bytes

    response = client.get("/pollen/grass/1/2/3")

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert response.content == png_bytes
    assert tiles_cache.save_calls == 0


def test_tile_cache_miss(patched_caches, monkeypatch):
    _, tiles_cache = patched_caches

    def mock_tile_fetch(*args, **kwargs):
        class MockResp:
            content = b"\x89PNG\r\n\x1a\n"
            def raise_for_status(self): pass
        return MockResp()

    monkeypatch.setattr(
        "backend.app.services.google_pollen.requests.get",
        mock_tile_fetch
    )

    response = client.get("/pollen/grass/1/2/3")

    assert response.status_code == 200
    assert tiles_cache.save_calls == 1


def test_tile_fetch_failure_not_cached(patched_caches, monkeypatch):
    _, tiles_cache = patched_caches

    def mock_fail(*args, **kwargs):
        raise requests.exceptions.RequestException("Google API down")

    monkeypatch.setattr(
        "backend.app.services.google_pollen.requests.get",
        mock_fail
    )

    response = client.get("/pollen/grass/1/2/3")

    assert response.status_code == 500
    assert tiles_cache.save_calls == 0



### Testing it go thru the router