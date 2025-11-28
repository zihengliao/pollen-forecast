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


def fetch_and_cache_pollen(lat, lng):
    print("Refreshing pollen...")

    url = f"https://pollen.googleapis.com/v1/forecast:lookup?key={GOOGLE_POLLEN_API_KEY}"

    body = {
        "location.latitude": lat,
        "location.longitude": lng,
        "days": 5
    }

    response = requests.get(url, params=body)
    print("STATUS:", response.status_code)
    print("URL:", response.request.url)

    return response.json()


def extract_grass_forecast(pollen_data):
    result = {}

    for entry in pollen_data["dailyInfo"]:
        d = entry["date"]
        day = f"{d['year']}-{d['month']:02d}-{d['day']:02d}"

        grass_value = None
        for item in entry["pollenTypeInfo"]:
            if item["code"] == "GRASS":
                grass_value = item["indexInfo"]["value"]
                break

        if grass_value is not None:
            result[day] = grass_value

    return result
