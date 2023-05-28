from pymongo import MongoClient
from fastapi import FastAPI
import settings

app = FastAPI()


@app.on_event("startup")
def startup():
    print("startup")

    client = MongoClient(settings.MONGO_URI)
    app.state.client = client
    app.state.db = client[settings.MONGO_DB]
    app.state.products = app.state.db[settings.PRODUCTS_COLLECTION]


@app.get("/health-check")
def read_root():
    return "ok"


@app.get("/inflation")
def calculate_inflation(region: str = "all"):
    old_price = 100.0
    new_price = 120.0
    # Calculating inflation in the return statement
    inflation = ((new_price - old_price) / old_price) * 100

    return {'region': region, 'inflation': ((new_price - old_price) / old_price) * 100, 'old_price': old_price,'new_price': new_price}
