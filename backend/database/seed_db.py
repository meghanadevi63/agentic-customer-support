# backend/database/seed_db.py

import json
import os
from pathlib import Path
from pymongo import MongoClient
from pymongo.server_api import ServerApi


MONGO_URI = os.getenv("MONGO_URI")

def seed_database():
    if not MONGO_URI:
        print("[ERROR] MONGO_URI not found in environment variables. Check your .env file.")
        return

    print("[INFO] Connecting to MongoDB Atlas...")
    
    # Connect to the cluster
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    db = client["support_bot_db"]

    try:
        # Ping the database to verify the connection
        client.admin.command('ping')
        print("[SUCCESS] Pinged your deployment. You successfully connected to MongoDB Atlas!\n")
    except Exception as e:
        print("[ERROR] Failed to connect to MongoDB. Please check your network and password.")
        print(e)
        return

    # Setup paths
    # This script is at: /backend/database/seed_db.py
    # So the project root is two folders up.
    CURRENT_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = CURRENT_DIR.parent.parent
    DATA_DIR = PROJECT_ROOT / "customer_data"

    print(f"[INFO] Looking for data files in: {DATA_DIR}\n")

    FILES_TO_COLLECTIONS = {
        "customers_seed.json": "customers",
        "interactions_seed.json": "interactions",
        "tickets_seed.json": "tickets",
        "feedback_seed.json": "feedback"
    }

    for filename, collection_name in FILES_TO_COLLECTIONS.items():
        file_path = DATA_DIR / filename
        
        if not file_path.exists():
            print(f"[WARNING] {filename} not found at {file_path}. Skipping.")
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if not data:
            print(f"[WARNING] {filename} is empty. Skipping.")
            continue

        collection = db[collection_name]
        
        # Clear old data to prevent duplicates if you run this multiple times
        collection.delete_many({})
        
        # Set the custom MongoDB _id to match your JSON IDs
        for item in data:
            if collection_name == "customers":
                item["_id"] = item.get("customer_id")
            elif collection_name == "interactions":
                item["_id"] = item.get("interaction_id")
            elif collection_name == "tickets":
                item["_id"] = item.get("ticket_id")
            elif collection_name == "feedback":
                item["_id"] = item.get("feedback_id")

        # Insert into MongoDB
        collection.insert_many(data)
        print(f"[SUCCESS] Successfully inserted {len(data)} records into '{collection_name}' collection!")

    print("\n[INFO] Atlas Database Seeding Complete!")

if __name__ == "__main__":
    seed_database()