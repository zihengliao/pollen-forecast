import requests
from app.cache.mongo import save_cache, load_cache

GOOGLE_URL = "https://airquality.googleapis.com/...your-url..."

def fetch_google_pollen():
    cached = load_cache()
    if cached:
        return cached
    return {"error": "No cached data yet"}

def fetch_and_cache_pollen():
    print("Refreshing pollen...")
    response = requests.get(GOOGLE_URL)
    data = response.json()
    save_cache(data)
