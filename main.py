from pymongo import MongoClient
from fastapi import FastAPI
import settings

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["products"]


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
def calculate_inflation(type_product: str = "all"):
    # Selection of products of the same type "food"
    if type_product == "all":
        products = collection.find({"type": "food"})
    else:
        products = collection.find({"type": "food", "type_product": type_product})

    # Creating a dictionary to store previous prices
    previous_prices = {}

    # Processing products and linking previous prices to current prices
    for product in products:
        product_id = product["id"]  # Product ID
        current_price = product["price"]  # Current product price

        # Find previous price by product id
        previous_price = previous_prices.get(product_id)
        # If the previous price is found, we calculate inflation
        if previous_price is not None:
            inflation = ((current_price - previous_price) / previous_price) * 100  # Calculation of inflation
            product["previous_price"] = previous_price  # Adding "previous_price" field to product
            product["inflation"] = inflation  # Adding the "inflation" field to the product

        # Save the current price as the previous price for the next cycle
        previous_prices[product_id] = current_price

    for product in products:
        print(product)

        # Further processing of results and data return

    return {"products": list(products)}
