import pymongo
from pymongo.mongo_client import MongoClient
import certifi
import os
from typing import Optional

# Connection URL (Using the one from the original code)
MONGODB_URL = "mongodb+srv://guptaaryann02_db_user:MkLsi06mWHgb7vzG@cluster0.cwzknrg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

class DatabaseManager:
    def __init__(self, url: str = MONGODB_URL):
        self.url = url
        self.client: Optional[MongoClient] = None

    def connect(self):
        try:
            self.client = MongoClient(self.url, tlsCAFile=certifi.where())
            self.client.admin.command('ping')
            print("Connected to MongoDB!")
        except Exception as e:
            print(f"MongoDB Connection Error: {e}")
            self.client = None

    def get_collection(self, db_name: str = "roomy", collection_name: str = "roomdata"):
        if not self.client:
            self.connect()
        
        if self.client:
            return self.client[db_name][collection_name]
        return None

db_manager = DatabaseManager()

def get_db_collection():
    collection = db_manager.get_collection()
    if collection is None:
        raise Exception("Could not connect to database")
    return collection
