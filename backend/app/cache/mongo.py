from pymongo import MongoClient
import os
import time
from dotenv import load_dotenv


load_dotenv()
class CacheManager:
    def __init__(self):
        mongo = MongoClient(os.getenv("MONGO_URL"))
        self.db = mongo["pollen"]

    # debating whether to define abstract methods + attributes but importance rn is minimal


class TilesCache(CacheManager):
    def __init__(self):
        super().__init__()
        self.collection = self.db["tiles_cache"]
        self.TILE_TTL = 60 * 60 * 12      # 0.5 day

    def save_cache(self, tile_type, z, x, y, data):
        self.collection.update_one(
            {"_id": f"{tile_type}_{z}_{x}_{y}"},
            {"$set": {"data": data, "timestamp": time.time()}},
            upsert=True
        )

    def load_cache(self, tile_type, z, x, y):
        doc = self.collection.find_one({"_id": f"{tile_type}_{z}_{x}_{y}"})
        if not doc:
            return None

        if time.time() - doc["timestamp"] > self.TILE_TTL:
            return None

        return doc["data"]
    

class ForecastCache(CacheManager):
    def __init__(self):
        super().__init__()
        self.collection = self.db["forecast_cache"]
        self.FORECAST_TTL = 60 * 60 * 6      # 6 hours
    
    def load_cache(self, geohash):
        key = geohash
        doc = self.collection.find_one({"_id": key})
        if not doc:
            return None

        if time.time() - doc["timestamp"] > self.FORECAST_TTL:
            return None

        return doc["data"]

    def save_cache(self, geohash, forecast_json):
        key = geohash
        self.collection.update_one(
            {"_id": key},
            {"$set": {"data": forecast_json, "timestamp": time.time()}},
            upsert=True
        )