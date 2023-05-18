import pymongo
from pymongo import MongoClient
from fastapi import FastAPI, Request
from src.models import ProductCreate
from src.settings import MONGO_URI, MONGO_DB


app = FastAPI()

client = MongoClient(MONGO_URI)
mongo_db = client[MONGO_DB]


@app.on_event("startup")
def startup():
    app.state.custom = 4
    print("startup")


@app.get("/")
def read_root(request: Request):
    customfcs = request.app.state.custom
    return {"Hello": "customfcs"}


def get_all_products():
    # Retrieve all products from the collection and convert the cursor to a list
    products_data = list(mongo_db.products.find())
    return products_data


# Define the endpoint to add a new Product to MongoDB
@app.post("/products", status_code=201)
def add_product_to_db(product: ProductCreate):
    # Create a new document with the product data
    product_data = {
        'name': product.name,
        'price': product.price,
        'type': product.type,
        'region': product.region
    }
    # Return the new product as a dictionary
    return product_data
