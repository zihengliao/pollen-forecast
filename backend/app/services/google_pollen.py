import requests
from fastapi import HTTPException, Response
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_POLLEN_API_KEY = os.getenv("GOOGLE_POLLEN_API_KEY")

def fetch_pollen_tile(tile_type: str, z: int, x: int, y: int):
    url = (
        f"https://pollen.googleapis.com/v1/mapTypes/{tile_type}/heatmapTiles/"
        f"{z}/{x}/{y}?key={GOOGLE_POLLEN_API_KEY}"
    )

    resp = requests.get(url)

    # If Google returns an error, raise it
    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code,
            detail=resp.text
        )

    # Return raw PNG bytes
    return Response(content=resp.content, media_type="image/png")
