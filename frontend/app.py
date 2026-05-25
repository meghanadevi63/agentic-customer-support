# frontend/app.py

import streamlit as st
import requests
import uuid
import json
from pathlib import Path
from streamlit_lottie import st_lottie

# --- CONFIGURATION ---
#BASE_URL = "http://localhost:8000"

#BASE_URL = "http://192.168.0.6:8000"

BASE_URL = "http://192.168.1.125:8000"
API_URL = f"{BASE_URL}/chat"

st.set_page_config(
    page_title="Agentic Customer Support",
    page_icon="🤖",
    layout="wide"
)

# --- CALLBACK FUNCTIONS (NEW: Added for stability) ---

def load_selected_chat(thread_id):
    """
    Callback function to load a past chat transcript.
    This runs before the page rerenders, preventing the disappearing button bug.
    """
    try:
        t_resp = requests.get(f"{BASE_URL}/history/transcript/{thread_id}")
        if t_resp.status_code == 200:
            transcript = t_resp.json()
            loaded_messages = []
            for m in transcript:
                loaded_messages.append({"role": "user", "content": m['query']})
                loaded_messages.append({
                    "role": "assistant", 
                    "content": m['bot_response'], 
                    "intent": m.get("intent"),
                    "trace": m.get("trace", [])
                })
            # Update session state
            st.session_state.messages = loaded_messages
            st.session_state.thread_id = thread_id
    except Exception as e:
        st.error(f"Failed to load transcript: {e}")

# --- LOAD LOTTIE ---
BASE_DIR = Path(__file__).resolve().parent

def load_lottie():
    animation_path = BASE_DIR / "Robot says hello.json"
    try:
        with open(animation_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except: return None

robot_animation = load_lottie()

# --- SESSION STATE INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "customer_id" not in st.session_state:
    st.session_state.customer_id = "CUS1001" 

# --- SIDEBAR ---
with st.sidebar:
    st.title(":material/settings: Support Controls")
    st.markdown("---")

    # 1. DYNAMIC CUSTOMER LOGIN
    st.subheader("👤 User Login")
    user_input = st.text_input("Enter Customer ID (e.g., CUS1001 - CUS1100):", 
                                  value=st.session_state.customer_id)
    
    if user_input != st.session_state.customer_id:
        st.session_state.customer_id = user_input
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    st.info(f"Active Profile: **{st.session_state.customer_id}**")

    # 2. SESSION CONTROLS
    col1, col2 = st.columns(2)
    with col1:
        if st.button(":material/add: New Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.thread_id = str(uuid.uuid4())
            st.rerun()
    with col2:
        if st.button(":material/delete: Clear UI", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.markdown("---")

    # 3. STABLE CHAT HISTORY (IMPROVEMENT: Fixed disappearing buttons)
    st.subheader(":material/history: Past Conversations")
    try:
        h_resp = requests.get(f"{BASE_URL}/history/sessions/{st.session_state.customer_id}")
        if h_resp.status_code == 200:
            sessions = h_resp.json()
            if not sessions:
                st.caption("No history found for this ID.")
            
            for sess in sessions:
                clean_query = sess['first_query'][:25].replace("\n", " ")
                is_active = st.session_state.thread_id == sess['_id']
                
               
                st.button(
                    f"💬 {clean_query}...", 
                    key=f"hist_{sess['_id']}", 
                    use_container_width=True, 
                    type="primary" if is_active else "secondary",
                    on_click=load_selected_chat,
                    args=(sess['_id'],)
                )
    except:
        st.error("History Offline")

# --- HEADER ---
col_h1, col_h2 = st.columns([4, 1])
with col_h1:
    st.title("🤖 Agentic Customer Support System")
    st.caption(f"Personalized RAG Bot | Profile: {st.session_state.customer_id} | Thread: {st.session_state.thread_id[:8]}")
with col_h2:
    if robot_animation:
        st_lottie(robot_animation, height=100, key="robot")

# --- CHAT DISPLAY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        if message["role"] == "assistant":
            # COMBINED DEBUG AND TRACE INFO
            with st.expander("🔍 Agent Intelligence & Trace"):
                col_db1, col_db2 = st.columns(2)
                col_db1.metric("Intent", str(message.get("intent")).upper())
                col_db2.metric("Thread ID", st.session_state.thread_id[:8])
                
                st.markdown("**Reasoning Path:**")
                if "trace" in message and message["trace"]:
                    for step in message["trace"]:
                        if isinstance(step, str):
                            st.caption(f"⚙️ {step}")
                        else:
                            with st.container(border=True):
                                st.markdown(f"**Agent:** {step.get('agent')}")
                                for k, v in step.items():
                                    if k != 'agent':
                                        st.write(f"*{k.title()}:* {v}")
                else:
                    st.caption("Historical transcript (Details not available for this session).")

# --- INPUT AREA ---
prompt = st.chat_input("Ask your question...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing profile & generating response..."):
            try:
                r = requests.post(API_URL, json={
                    "query": prompt,
                    "thread_id": st.session_state.thread_id,
                    "customer_id": st.session_state.customer_id
                })
                
                if r.status_code == 200:
                    data = r.json()
                    st.markdown(data["response"])
                    
                    if data.get("escalated"):
                        st.warning("⚠️ This issue has been escalated to a specialist.")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data["response"],
                        "intent": data["intent"],
                        "escalated": data["escalated"],
                        "trace": data.get("trace", [])
                    })
                    st.rerun()
                else:
                    st.error(f"API Error: {r.status_code}")
            except Exception as e:
                st.error(f"Connection Failed: {e}")