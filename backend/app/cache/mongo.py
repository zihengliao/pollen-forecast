from pymongo import MongoClient
import os

mongo = MongoClient(os.getenv("mongodb://localhost:27017"))
db = mongo["pollen"]
collection = db["cache"]

def save_cache(data):
    collection.update_one(
        {"_id": "latest"},
        {"$set": {"data": data}},
        upsert=True
    )

def load_cache():
    doc = collection.find_one({"_id": "latest"})
    return doc["data"] if doc else None
