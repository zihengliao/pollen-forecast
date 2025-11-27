from fastapi import APIRouter
from app.services.google_pollen import fetch_pollen_tile

router = APIRouter()

@router.get("/pollen/{tile_type}/{z}/{x}/{y}")
def get_tile(tile_type: str, z: int, x: int, y: int):
    return fetch_pollen_tile(tile_type, z, x, y)
