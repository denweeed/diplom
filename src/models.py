from datetime import date
from pydantic import BaseModel, root_validator


class ProductType(str):
    FOOD = 'food'
    EVERYDAY_USE = 'everyday_use'


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
