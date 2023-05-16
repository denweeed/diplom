import pymongo
from pymongo import MongoClient
from fastapi import FastAPI, Request
from bson import ObjectId
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


products_data = mongo_db.products.find()


@app.get('/products/all')
def get_all_products():
    return products_data


# Define the endpoint to add a new Product to MongoDB
@app.post("/products", status_code=201)
def add_product_to_db(product: ProductCreate):
    # Generate a new ObjectId for the product
    product_id = str(ObjectId())

    # Create a new document with the product data
    product_data = {
        'id': int(product_id),
        'name': product.name,
        'price': product.price,
        'type': product.type,
        'region': product.region
    }

    # Insert the new product document into the MongoDB collection
    mongo_db.products.insert_one(product_data)

    # Return the new product as a dictionary
    return product_data
