import pymongo
from pymongo import MongoClient
from fastapi import FastAPI, Request
from pydantic.main import BaseModel
from pydantic import root_validator, ValidationError
from enum import Enum
from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from pymongo import MongoClient
from bson.objectid import ObjectId

app = FastAPI(
    title="product"
)

DATABASE_URL = "sqlite:///./products.db"

# Create a SQLAlchemy engine and sessionmaker
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Create a Database object for async queries
database = Database(DATABASE_URL)

# Create a MongoDB client and database
client = MongoClient('localhost', 27017)
mongo_db = client.products_database

Base = declarative_base()


class ProductType(str, Enum):
    FOOD = 'food'
    EVERYDAY_USE = 'everyday_use'


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    type = Column(SQLEnum(ProductType), nullable=False)
    region = Column(String(50), nullable=False)
    created_at = Column(Date, nullable=False)


# Create the table in the database
Base.metadata.create_all(engine)


@app.on_event("startup")
def startup():
    app.state.custom = 4
    print("startup")


client = MongoClient('localhost', 27017)


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


@app.post('/products')
async def add_product(product: Product):
    try:
        products.append(product.dict())
        return {'status': 'success', 'data': product.dict()}, 201
    except ValidationError as e:
        return {'status': 'error', 'message': e.errors()}, 400


@app.get('/products/all')
async def get_all_products():
    return {'status': 'success', 'data': products}, 200


# Define the endpoint to create a new Product
@app.post("/products")
async def create_product(product: ProductCreate):
    # Convert the Pydantic model to a SQLAlchemy model
    db_product = Product(**product.dict())

    # Use a SQLAlchemy session to insert the new Product into the database
    db = SessionLocal()
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # Use a Database object to fetch the newly inserted Product from the database
    query = Product.__table__.select().where(Product.id == db_product.id)
    product_db = await database.fetch_one(query)

    # Add the new Product to MongoDB
    product_id = str(ObjectId())
    mongo_db.products.insert_one({'_id': product_id, **product.dict()})
    # Return the new Product as a dictionary
    return dict(product_db)


# Define the endpoint to get all products
@app.get("/products")
async def read_products():
    # Use a Database object to fetch all Products from the database
    query = Product.__table__.select()
    products_db = await database.fetch_all(query)

    # Get all Products from MongoDB
    products_mongo = list(mongo_db.products.find())

    # Combine the Products from both databases
    products = []
    for product_db in products_db:
        product = dict(product_db)
        product['_id'] = str(ObjectId())
        products.append(product)
    products.extend(products_mongo)

    # Return all Products as a list of dictionaries
    return {'status': 'success', 'data': products}
