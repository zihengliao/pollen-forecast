import requests
from fastapi import HTTPException, Response
import os
from dotenv import load_dotenv
from timezonefinder import TimezoneFinder
from datetime import datetime, timezone
import pytz
from ..cache.mongo import TilesCache
from ..cache.mongo import ForecastCache
import geohash

forecast_cache = ForecastCache()
tiles_cache = TilesCache()


load_dotenv()
GOOGLE_POLLEN_API_KEY = os.getenv("GOOGLE_POLLEN_API_KEY")

def fetch_pollen_tile(tile_type: str, z: int, x: int, y: int):

    # lets see if we have it cached
    cached = tiles_cache.load_cache(tile_type, z, x, y)
    if cached:
        return Response(content=cached, media_type="image/png")
    
    # if not, fetch from google
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
    
    tiles_cache.save_cache(tile_type, z, x, y, resp.content)

    # Return raw PNG bytes
    return Response(content=resp.content, media_type="image/png")


def fetch_pollen_forecast(lat, lng):

    # check cache first
    h = geohash.encode(lat, lng, precision=6)
    cached = forecast_cache.load_cache(h)
    if cached:
        return cached
    
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

    data = response.json()
    forecast_data = extract_grass_forecast(data, lat, lng)
    forecast_cache.save_cache(h, forecast_data)
    
    return forecast_data


def extract_grass_forecast(pollen_data, latitude, longitude):
    result = {}

    for entry in pollen_data["dailyInfo"]:
        d = entry["date"]
        day = f"{d['year']}-{d['month']:02d}-{d['day']:02d}"
        time = datetime.now(timezone.utc)

        grass_value = None
        for item in entry["pollenTypeInfo"]:
            if item["code"] == "GRASS":
                grass_value = item["indexInfo"]["value"]
                break
        day = utc_to_local(
            latitude,
            longitude,
            datetime(d['year'], d['month'], d['day'], time.hour, time.minute, time.second)    # im including hour, min for accurate day conversion
        )[0].strftime("%d/%m/%Y")
        if grass_value is not None:
            result[day] = grass_value

    return result


def utc_to_local(lat, lng, utc_datetime):

    tf = TimezoneFinder()

    timezone_name = tf.timezone_at(lng=lng, lat=lat)

    if not timezone_name:
        raise ValueError("Could not determine timezone from coordinates")

    local_tz = pytz.timezone(timezone_name)
    local_dt = utc_datetime.astimezone(local_tz)

    return local_dt, timezone_name

