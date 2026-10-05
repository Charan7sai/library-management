import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]

client.admin.command("ping")
print("Connected to MongoDB")

result = db.books.insert_one({
    "isbn": "978-0000000001",
    "title": "Test Book",
    "author": "Test Author",
    "genres": ["Test"],
    "totalCopies": 1,
    "availableCopies": 1
})
print("Inserted:", result.inserted_id)