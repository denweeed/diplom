import pymongo
from typing import Union

from pymongo import MongoClient
from fastapi import FastAPI, Request
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
