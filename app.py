from database.db import users_collection

users_collection.insert_one({"test": "connection"})
print("MongoDB Connected Successfully!")