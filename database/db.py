import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load .env locally (won't affect Streamlit Cloud)
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in environment variables.")

client = MongoClient(MONGO_URI)
db = client["skillsync_db"]

users_collection = db["users"]
reports_collection = db["reports"]