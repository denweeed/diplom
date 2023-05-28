import pymongo
from pymongo import MongoClient
from fastapi import FastAPI, Request
from src.models import ProductBase
from src.settings import MONGO_URI, MONGO_DB, PRODUCTS_COLLECTION


app = FastAPI()


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
    app.state.mongo_collection.insert_one(product_data)
    # Return the new product as a dictionary
    return product_data
