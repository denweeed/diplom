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

    @root_validator(pre=True)
    def validate_id(cls, values):
        products_data = values.get('products_data', [])
        if 'id' not in values:
            values['id'] = len(products_data) + 1
        return values