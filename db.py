import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]

def _supports_transactions():
    info = client.admin.command("hello")
    return "setName" in info or info.get("msg") == "isdbgrid"

SUPPORTS_TRANSACTIONS = _supports_transactions()