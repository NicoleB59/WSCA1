import os
from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "inventory_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "products")

print("Looking for .env at:", ENV_PATH)
print("MONGO_URI loaded:", MONGO_URI)
print("DB_NAME loaded:", DB_NAME)
print("COLLECTION_NAME loaded:", COLLECTION_NAME)

if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env file")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

try:
    client.admin.command("ping")
    print("Connected to MongoDB successfully.")
    collection.create_index("ProductID", unique=True)
    collection.create_index("Name")
except Exception as e:
    print("MongoDB connection failed:", e)
    raise