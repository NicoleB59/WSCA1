from fastapi import FastAPI, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
import requests

from database import collection
from models import ProductCreate

app = FastAPI(
    title="Inventory Management API",
    description="API for managing inventory stored in MongoDB",
    version="1.0.0"
)

def serialize_product(product):
    product["id"] = str(product["_id"])
    del product["_id"]
    return product

@app.get("/")
def home():
    return {"message": "Running"}

@app.get("/getSingleProduct")
def get_single_product(product_id: int = Query(..., gt=0)):
    product = collection.find_one({"ProductID": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return serialize_product(product)

@app.get("/getAll")
def get_all():
    products = list(collection.find())
    return [serialize_product(product) for product in products]

@app.post("/addNew")
def add_new(product: ProductCreate):
    existing = collection.find_one({"ProductID": product.ProductID})
    if existing:
        raise HTTPException(status_code=400, detail="ProductID already exists")

    product_dict = jsonable_encoder(product)
    result = collection.insert_one(product_dict)
    new_product = collection.find_one({"_id": result.inserted_id})
    return {
        "message": "Product added successfully",
        "product": serialize_product(new_product)
    }

@app.delete("/deleteOne")
def delete_one(product_id: int = Query(..., gt=0)):
    result = collection.delete_one({"ProductID": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": f"Product {product_id} deleted successfully"}

@app.get("/startsWith")
def starts_with(letter: str = Query(..., min_length=1, max_length=1)):
    regex = f"^{letter}"
    products = list(collection.find({"Name": {"$regex": regex, "$options": "i"}}))
    return [serialize_product(product) for product in products]

@app.get("/paginate")
def paginate(
    start_id: int = Query(..., gt=0),
    end_id: int = Query(..., gt=0)
):
    if start_id > end_id:
        raise HTTPException(status_code=400, detail="start_id must be less than or equal to end_id")

    products = list(
        collection.find({
            "ProductID": {"$gte": start_id, "$lte": end_id}
        }).sort("ProductID", 1).limit(10)
    )

    return [serialize_product(product) for product in products]

@app.get("/convert")
def convert(product_id: int = Query(..., gt=0)):
    product = collection.find_one({"ProductID": product_id})

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        response = requests.get(
            "https://api.frankfurter.dev/v2/rates?base=USD&quotes=EUR",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        exchange_rate = data[0]["rate"]
        usd_price = float(product["UnitPrice"])
        eur_price = round(usd_price * exchange_rate, 2)

        return {
            "ProductID": product["ProductID"],
            "Name": product["Name"],
            "UnitPriceUSD": usd_price,
            "ExchangeRateUSDtoEUR": exchange_rate,
            "UnitPriceEUR": eur_price
        }

    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Currency conversion service unavailable: {str(e)}")
    