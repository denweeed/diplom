import pymongo
from pymongo.results import InsertOneResult
from pymongo import MongoClient
from fastapi import FastAPI
import settings
from datetime import datetime, timedelta
from fastapi import FastAPI, Request
from src.models import ProductBase
from src.settings import MONGO_URI, MONGO_DB, PRODUCTS_COLLECTION, CURRENT_PERIOD_MONTHS, PREVIOUS_PERIOD_MONTHS


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


def relativedelta(months):
    pass


@app.get("/inflation")
def calculate_inflation(type_product: str = "all", start_date: datetime = datetime.now(), end_date: datetime = datetime.now()):

    """
    Calculates the total sum of product prices within a specified period.

    Args:
        type_product (str, optional): The type of product to filter (default is "all").
        start_date (datetime): The start date of the period.
        end_date (datetime): The end date of the period.

    Returns:
        float: The total sum of product prices within the specified period.
    """
    products_current_period = collection.find()

    total_sum_current_period = 0

    for product in products_current_period:
        price = product["Price"]
        creation_date = datetime.strptime(product["Creation Date"], "%d.%m.%Y")

        # Filter out products outside the specified period
        if start_date <= creation_date <= end_date:
            total_sum_current_period += price

    products_previous_period = collection.find()

    total_sum_previous_period = 0

    for product in products_previous_period:
        price = product["Price"]
        creation_date = datetime.strptime(product["Creation Date"], "%d.%m.%Y")

        # Filter out products for the previous period
        previous_start_date = start_date - relativedelta(months=PREVIOUS_PERIOD_MONTHS)
        previous_end_date = end_date - relativedelta(months=PREVIOUS_PERIOD_MONTHS)
        if previous_start_date <= creation_date <= previous_end_date:
            total_sum_previous_period += price

    return total_sum_current_period, total_sum_previous_period
