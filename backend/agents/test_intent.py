# backend/agents/test_intent.py
# backend/agents/test_intent.py

from backend.agents.intent_agent import IntentAgent


state = {

    "query":
    "My payment failed and amount got deducted",

    "intent":None,

    "confidence":None,

    "retrieved_docs":[],

    "response":None,

    "escalation_required":False,

    "conversation_history":[],

    "next_node":None
}


agent = IntentAgent()

updated_state = agent.run(state)

print("\nUpdated State:\n")

print(updated_state)