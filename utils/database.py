from pymongo import MongoClient
import os

def get_database():
    """
    Connect to MongoDB and return the database instance.
    """
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("MONGO_URI is not set in the environment variables.")
    
    client = MongoClient(mongo_uri)
    db_name = mongo_uri.split("/")[-1].split("?")[0]  # Extract database name from URI
    return client[db_name]

def save_interview_data(data):
    """
    Save interview data to the MongoDB database.
    """
    db = get_database()
    collection = db["interviews"]  # Collection name
    result = collection.insert_one(data)
    return result.inserted_id