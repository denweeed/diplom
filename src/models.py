from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class ProductType(Enum):
    FOOD = 'food'
    EVERYDAY_USE = 'everyday_use'


class ProductBase(BaseModel):
    name: str
    price: float
    type: ProductType
    region: str


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    created_at: datetime
