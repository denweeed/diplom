import pymongo
from pymongo.results import InsertOneResult
from pymongo import MongoClient
from fastapi import FastAPI
import settings
from datetime import datetime, timedelta
from fastapi import FastAPI, Request
from src.models import ProductBase
from dateutil.relativedelta import relativedelta


app = FastAPI()


@app.on_event("startup")
def startup():
    app.state.client = MongoClient(settings.MONGO_URI)
    app.state.mongo_db = app.state.client[settings.MONGO_DB]
    app.state.mongo_collection = app.state.mongo_db[settings.PRODUCTS_COLLECTION]


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
        'created_at': datetime.utcnow()
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
    products_current_period = app.state.mongo_collection.find({
        "created_at": {
            "$lt":datetime.utcnow(),
            "$gt":datetime.utcnow() - relativedelta(months=settings.PERIOD_MONTHS)
        }
    })

    products_previous_period = app.state.mongo_collection.find({
        "created_at": {
            "$lt": datetime.utcnow() - relativedelta(years=1),
            "$gt": datetime.utcnow() - relativedelta(years=1) - relativedelta(months=settings.PERIOD_MONTHS)
        }
    })

    total_sum_current_period = 0
    total_sum_previous_period = 0

    for product in products_current_period:
        price = product["price"]
        total_sum_current_period += price

    for product in products_previous_period:
        price = product["price"]
        total_sum_previous_period += price

    inflation_rate = (total_sum_current_period - total_sum_previous_period) / total_sum_previous_period * 100

    return inflation_rate





