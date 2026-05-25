# backend/tests/test_history.py
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.tools.crm_tool import get_customer_sessions, get_thread_transcript

def test_history_retrieval():
    test_id = "CUS1001" # Aarav Sharma
    
    print(f"[TEST] Fetching chat history for: {test_id}")
    
    # 1. Get List of Threads
    sessions = get_customer_sessions(test_id)
    
    if not sessions:
        print("[!] No history found for this user.")
        return

    print(f"[SUCCESS] Found {len(sessions)} unique conversation threads.\n")
    
    for sess in sessions:
        print(f"Thread ID: {sess['_id']}")
        print(f"Started with: '{sess['first_query']}'")
        print(f"Last Active: {sess['last_active']}")
        print("-" * 30)

    # 2. Load the most recent thread transcript
    latest_thread = sessions[0]['_id']
    print(f"\n[STEP 2] Loading full transcript for thread: {latest_thread}")
    
    transcript = get_thread_transcript(latest_thread)
    
    for msg in transcript:
        print(f"\n[{msg['timestamp']}]")
        print(f"USER: {msg['query']}")
        print(f"BOT: {msg['bot_response']}")

if __name__ == "__main__":
    test_history_retrieval()