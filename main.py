import pymongo
from pymongo import MongoClient
from fastapi import FastAPI, Request
from pydantic.main import BaseModel
from pydantic import root_validator, ValidationError
from enum import Enum
from datetime import date
from bson import ObjectId

app = FastAPI(title="product")

client = MongoClient('mongodb://localhost:27017')
mongo_db = client['product_db']


class ProductType(str, Enum):
    FOOD = 'food'
    EVERYDAY_USE = 'everyday_use'


@app.on_event("startup")
def startup():
    app.state.custom = 4
    print("startup")


@app.get("/")
def read_root(request: Request):
    customfcs = request.app.state.custom
    return {"Hello": "customfcs"}


class ProductCreate(BaseModel):
    name: str
    price: float
    type: ProductType
    region: str


class Product(BaseModel):
    id: int
    name: str
    price: float
    type: ProductType
    region: str
    created_at: date

    @root_validator(pre=True)
    def validate_id(cls, values):
        if 'id' not in values:
            values['id'] = len(products) + 1
        return values


products = []


@app.get('/products/all')
async def get_all_products():
    return {'status': 'success', 'data': products}, 200


# Define the endpoint to add a new Product to MongoDB
@app.post("/products/add")
async def add_product_to_db(product: ProductCreate):
    # Generate a new ObjectId for the product
    product_id = str(ObjectId())

    # Create a new document with the product data
    product_data = {
        '_id': product_id,
        'name': product.name,
        'price': product.price,
        'type': product.type,
        'region': product.region
    }

    # Insert the new product document into the MongoDB collection
    mongo_db.products.insert_one(product_data)

    # Return the new product as a dictionary
    return {'status': 'success', 'data': product_data}
