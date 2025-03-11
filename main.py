import os
from pymongo import MongoClient

def get_db():
    mongo_uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri)

    db = client["MyDataBase"]
    return db


if __name__ == "__main__":
    db = get_db()
    print(db)

    collections = db.list_collection_names()
    print(collections)
