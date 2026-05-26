# backend/tests/test_crm_system.py
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.tools.crm_tool import fetch_customer_profile, save_interaction
from backend.agents.personalized_agent import PersonalizedAgent

def test_full_flow():
    # 1. SETUP TEST DATA
    test_id = "CUS1001" # Aarav Sharma from your seed data
    test_thread = "THREAD-TEST-999"
    test_query = "Why is my order ORD629903 delayed?"
    
    print(f"[TEST] Target Customer: {test_id}")
    print(f"[TEST] Query: {test_query}\n")

    # 2. FETCH PROFILE
    print("[STEP 1] Fetching profile from Atlas...")
    profile = fetch_customer_profile(test_id)
    if "error" in profile:
        print("!! Failed to fetch profile. Check MongoDB connection.")
        return
    print(f"Successfully fetched profile for: {profile['name']}\n")

    # 3. RUN AGENT
    print("[STEP 2] Generating Personalized Response...")
    agent = PersonalizedAgent()
    state = {
        "query": test_query,
        "customer_profile": profile,
        "intent": "shipping_issue"
    }
    updated_state = agent.run(state)
    response_text = updated_state["response"]
    print(f"BOT RESPONSE:\n{response_text}\n")

    # 4. SAVE TO DB
    print("[STEP 3] Saving interaction back to Atlas...")
    int_id = save_interaction(
        customer_id=test_id,
        thread_id=test_thread,
        query=test_query,
        response=response_text,
        intent="shipping_issue"
    )
    print(f"Saved successfully with ID: {int_id}")
    print("\n[SUCCESS] Test Complete. Check your Atlas 'interactions' collection!")

if __name__ == "__main__":
    test_full_flow()