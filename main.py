import pymongo
from typing import Union

from pymongo import MongoClient
from fastapi import FastAPI, Request

app = FastAPI()


@app.on_event("startup")
def startup():
    print("startup")

    client = MongoClient('mongodb://localhost:8081/')
    app.state.client = client
    app.state.db = client['inflation']
    app.state.products = app.state.db['products']


@app.get("/health-check")
def read_root():
    return "ok"
