from fastapi import APIRouter
from backend.app.services.google_pollen import fetch_pollen_tile
from fastapi import APIRouter
from backend.app.services.google_pollen import fetch_pollen_forecast, extract_grass_forecast

router = APIRouter()

@router.get("/pollen/{tile_type}/{z}/{x}/{y}")
def get_tile(tile_type: str, z: int, x: int, y: int):
    return fetch_pollen_tile(tile_type, z, x, y)


@router.get("/forecast")
def forecast(lat: float, lng: float):
    return fetch_pollen_forecast(lat, lng)
