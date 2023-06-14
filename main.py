import pymongo
from pymongo.results import InsertOneResult
from pymongo import MongoClient
from fastapi import FastAPI
import settings
from datetime import datetime
from fastapi import FastAPI, Request
from src.models import ProductBase
from src.settings import MONGO_URI, MONGO_DB, PRODUCTS_COLLECTION


app = FastAPI()

client = MongoClient(settings.MONGO_URI)
db = client[settings.mongodb_database]
collection = db[settings.mongodb_collection]


@app.on_event("startup")
def startup():
    app.state.client = MongoClient(MONGO_URI)
    app.state.mongo_db = app.state.client[MONGO_DB]
    app.state.mongo_collection = app.state.mongo_db[PRODUCTS_COLLECTION]


@app.on_event("shutdown")
def shutdown():
    app.state.client.close()


@app.get("/")
def read_root(request: Request):
    customfcs = request.app.state.custom
    return {"Hello": "customfcs"}


def get_product_from_database(product_id):
    # Retrieve a product from the database based on the given identifier
    product = app.state.mongo_collection.find_one({'_id': product_id})

    return product


# Define the endpoint to add a new Product to MongoDB
@app.post("/products", status_code=201)
def add_product_to_db(product: ProductBase):
    # Create a new document with the product data
    product_data = {
        'name': product.name,
        'price': product.price,
        'type': product.type.value,
        'region': product.region
    }
    # Insert the document into the MongoDB collection
    insert_result: InsertOneResult = app.state.mongo_collection.insert_one(product_data)
    # Get the inserted document ID
    inserted_id = insert_result.inserted_id
    # Retrieve the newly created document from the collection
    new_product = app.state.mongo_collection.find_one({'_id': inserted_id})
    # Return the new product as a dictionary
    return new_product


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
