from pymongo import MongoClient
from fastapi import FastAPI
import settings
from datetime import datetime

app = FastAPI()

client = MongoClient(settings.MONGO_URI)
db = client[settings.mongodb_database]
collection = db[settings.mongodb_collection]


@app.on_event("startup")
def startup():
    print("startup")

    client = MongoClient(settings.MONGO_URI)
    app.state.client = client
    app.state.db = client[settings.MONGO_DB]
    app.state.products = app.state.db[settings.PRODUCTS_COLLECTION]


@app.get("/health-check")
def read_root():
    return "ok"


@app.get("/inflation")
def calculate_inflation(type_product: str = "all"):
    # Selection of products of the same type "food"
    if type_product == "all":
        products = collection.find()
    else:
        products = collection.find({"Type": type_product})

    result = []

    for product in products:
        current_price = product["Price"]

    previous_prices = collection.find({
        "Product": product["Product"],
        "Created At": {"$lt": datetime.now()}
    }).sort("Created At", -1)

    previous_prices_list = [prev["Price"] for prev in previous_prices]

    if previous_prices_list:
        previous_price = previous_prices_list[0]
        inflation = ((current_price - previous_price) / previous_price) * 100
    else:
        inflation = None

        product_info = {
            "Product": product["Product"],
            "Type": product["Type"],
            "Current Price": current_price,
            "Previous Prices": previous_prices_list,
            "Inflation": inflation
        }
        result.append(product_info)

    return result
