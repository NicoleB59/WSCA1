import csv
import os
from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
CSV_PATH = BASE_DIR / "products.csv"

load_dotenv(dotenv_path=ENV_PATH)

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "inventory_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "products")

print("Using .env from:", ENV_PATH)
print("Using CSV from:", CSV_PATH)
print("DB_NAME:", DB_NAME)
print("COLLECTION_NAME:", COLLECTION_NAME)

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

products = []

with open(CSV_PATH, mode="r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    print("CSV columns:", reader.fieldnames)

    for row in reader:
        product = {
            "ProductID": int(row["ProductID"]),
            "Name": row["Name"].strip(),
            "UnitPrice": float(row["UnitPrice"]),
            "StockQuantity": int(row["StockQuantity"]),
            "Description": row["Description"].strip()
        }
        products.append(product)

print("Products read from CSV:", len(products))

if products:
    collection.delete_many({})
    result = collection.insert_many(products)
    print(f"Inserted {len(result.inserted_ids)} products into MongoDB.")
else:
    print("No products found in CSV.")