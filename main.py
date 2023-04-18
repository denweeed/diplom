import pymongo
from pymongo import MongoClient
from fastapi import FastAPI, Request
from pydantic.main import BaseModel
from pydantic import root_validator, ValidationError
from enum import Enum
from datetime import date

app = FastAPI(
    title="product"
)


@app.on_event("startup")
def startup():
    app.state.custom = 4
    print("startup")


client = MongoClient('localhost', 27017)


@app.get("/")
def read_root(request: Request):
    customfcs = request.app.state.custom
    return {"Hello": "customfcs"}


class ProductType(str, Enum):
    FOOD = 'food'
    EVERYDAY_USE = 'everyday_use'


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


# эдитпоин для добавления нового продукта
@app.post('/products')
async def add_product(product: Product):
    try:
        products.append(product.dict())
        return {'status': 'success', 'data': product.dict()}, 201
    except ValidationError as e:
        return {'status': 'error', 'message': e.errors()}, 400


# эдитпоинт для получения списка всех продуктов
@app.get('/products/all')
async def get_all_products():
    return {'status': 'success', 'data': products}, 200
