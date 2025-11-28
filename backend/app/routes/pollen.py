from fastapi import APIRouter
from app.services.google_pollen import fetch_pollen_tile
from fastapi import APIRouter
from app.services.google_pollen import fetch_and_cache_pollen, extract_grass_forecast

router = APIRouter()

@router.get("/pollen/{tile_type}/{z}/{x}/{y}")
def get_tile(tile_type: str, z: int, x: int, y: int):
    return fetch_pollen_tile(tile_type, z, x, y)


@router.get("/forecast")
def forecast(lat: float, lng: float):
    data = fetch_and_cache_pollen(lat, lng)
    return extract_grass_forecast(data)
