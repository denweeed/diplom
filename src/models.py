from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class ProductType(Enum):
    FOOD = 'food'
    EVERYDAY_USE = 'everyday_use'


class ProductBase(BaseModel):
    name: str
    price: float
    type: ProductType
    region: str


class Product(ProductBase):
    id: Optional[int] = Field(alias='_id', title='Product ID', description='The unique identifier of the product',
                              readOnly=True)
    created_at: Optional[datetime] = Field(title='Creation Date',
                                           description='The date and time when the product was created', readOnly=True)

    old_price: float
    new_price: float
