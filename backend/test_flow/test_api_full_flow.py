# backend/tests/test_api_full_flow.py

import requests
import uuid
import time

# Use localhost if testing on the same machine, or your IP
BASE_URL = "http://127.0.0.1:8000" 

def test_backend_integration():
    # 1. SETUP TEST PARAMETERS
    customer_id = "CUS1001"
    thread_id = f"TEST-THREAD-{uuid.uuid4().hex[:6]}"
    query = "Hi, I am Aarav. Can you tell me the status of my order ORD629903?"

    print(f"[STAGE 1] Sending Chat Request...")
    print(f"Customer: {customer_id} | Thread: {thread_id}")
    print(f"Query: {query}\n")

    # 2. TEST THE CHAT ENDPOINT
    chat_payload = {
        "query": query,
        "thread_id": thread_id,
        "customer_id": customer_id
    }

    response = requests.post(f"{BASE_URL}/chat", json=chat_payload)
    
    # --- FIXED TYPO HERE ---
    if response.status_code != 200:
        print(f"[ERROR] Chat request failed: {response.text}")
        return

    chat_data = response.json()
    print(f"[SUCCESS] Received Bot Response:")
    print(f"Bot: {chat_data['response']}")
    print(f"Intent Detected: {chat_data['intent']}\n")

    # Verify if personalization worked
    if "Aarav" in chat_data['response'] or "ORD629903" in chat_data['response']:
        print("[CHECK] Personalization: PASSED (Bot recognized customer/order)\n")
    else:
        print("[CHECK] Personalization: FAILED\n")

    # 3. TEST THE HISTORY SESSION ENDPOINT
    time.sleep(2) # Give Atlas a moment to index the new write
    print(f"[STAGE 2] Fetching Session History for {customer_id}...")
    
    sess_response = requests.get(f"{BASE_URL}/history/sessions/{customer_id}")
    sessions = sess_response.json()
    
    found_thread = any(s['_id'] == thread_id for s in sessions)
    if found_thread:
        print(f"[SUCCESS] Thread {thread_id} was correctly found in history!\n")
    else:
        print(f"[ERROR] Thread {thread_id} not found in MongoDB.\n")

    # 4. TEST THE TRANSCRIPT ENDPOINT
    print(f"[STAGE 3] Fetching Transcript for Thread: {thread_id}...")
    trans_response = requests.get(f"{BASE_URL}/history/transcript/{thread_id}")
    transcript = trans_response.json()

    if len(transcript) > 0:
        print(f"[SUCCESS] Retrieved {len(transcript)} messages from the thread.")
    else:
        print("[ERROR] Transcript is empty.")

    print("\n[INFO] Full Backend Integration Test Complete.")

if __name__ == "__main__":
    test_backend_integration()