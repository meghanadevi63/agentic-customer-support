# backend/tools/crm_tool.py
import os
import datetime
import random
from typing import Dict, Any, List
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = "mongodb+srv://chandumeghanadevi123:CHANDU632004@cluster0.tto7ema.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def get_db():
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    return client["support_bot_db"]

def fetch_customer_profile(customer_id: str) -> Dict[str, Any]:
    """Fetches full customer profile including orders and payments."""
    db = get_db()
    try:
        profile = db["customers"].find_one({"customer_id": customer_id})
        if profile:
            profile.pop("_id", None)
            return profile
        return {"error": "Customer not found"}
    finally:
        db.client.close()

def fetch_interaction_history(customer_id: str, limit: int = 3) -> List[Dict[str, Any]]:
    """Fetches the last N interactions for context."""
    db = get_db()
    try:
        history = list(db["interactions"].find({"customer_id": customer_id}).sort("timestamp", -1).limit(limit))
        for h in history:
            h.pop("_id", None)
        return history
    finally:
        db.client.close()

def save_interaction(customer_id: str, thread_id: str, query: str, response: str, intent: str):
    """Saves the current conversation turn to Atlas."""
    db = get_db()
    try:
        interaction_id = f"INT{random.randint(40000, 99999)}"
        doc = {
            "_id": interaction_id,
            "interaction_id": interaction_id,
            "customer_id": customer_id,
            "thread_id": thread_id,
            "query": query,
            "intent": intent,
            "bot_response": response,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        db["interactions"].insert_one(doc)
        return interaction_id
    finally:
        db.client.close()



def get_customer_sessions(customer_id: str):
    """
    Returns a list of unique thread_ids and the first query of each 
    so the user can pick a past chat from a list.
    """
    db = get_db()
    try:
        # Aggregate to find unique thread_ids for this customer
        pipeline = [
            {"$match": {"customer_id": customer_id}},
            {"$sort": {"timestamp": 1}}, # Oldest first to get the first question
            {"$group": {
                "_id": "$thread_id",
                "first_query": {"$first": "$query"},
                "last_active": {"$last": "$timestamp"}
            }},
            {"$sort": {"last_active": -1}} # Newest active sessions at top
        ]
        return list(db["interactions"].aggregate(pipeline))
    finally:
        db.client.close()

def get_thread_transcript(thread_id: str):
    """
    Fetches every message in a specific thread to display in the UI.
    """
    db = get_db()
    try:
        messages = list(db["interactions"].find({"thread_id": thread_id}).sort("timestamp", 1))
        for m in messages:
            m.pop("_id", None)
        return messages
    finally:
        db.client.close()


def create_atlas_ticket(customer_id: str, thread_id: str, issue: str):
    """
    Inserts a real ticket document into the MongoDB tickets collection.
    """
    db = get_db()
    try:
        ticket_id = f"TKT-{random.randint(10000, 99999)}"
        new_ticket = {
            "_id": ticket_id,
            "ticket_id": ticket_id,
            "customer_id": customer_id,
            "thread_id": thread_id,
            "issue": issue,
            "status": "Open",
            "priority": "HIGH",
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        db["tickets"].insert_one(new_ticket)
        return ticket_id
    except Exception as e:
        print(f"[ERROR] Database insertion failed: {e}")
        return None
    finally:
        db.client.close()