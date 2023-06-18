import environs

from pathlib import Path

env = environs.Env()

BASE_DIR = Path(__file__).parent

MONGO_URI = env.str("MONGO_URI", "mongodb://localhost:8081")
MONGO_DB = "inflation"
PRODUCTS_COLLECTION = "products"
