import environs
from pathlib import Path

env = environs.Env()

BASE_DIR = Path(__file__).parent

MONGO_URI = env.str("MONGO_URI", "mongodb://localhost:8081")
MONGO_DB = env.str("MONGO_DB", default="inflation")
PRODUCTS_COLLECTION = env.str("PRODUCTS_COLLECTION", default="products")
