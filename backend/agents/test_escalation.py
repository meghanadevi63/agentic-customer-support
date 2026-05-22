#backend/agents/test_escalation.py
from backend.agents.escalation_agent import EscalationAgent


state = {

    "query":
    "I think this payment is fraud and I want legal action",

    "intent":"payment_issue",

    "confidence":0.9,

    "retrieved_docs":[],

    "response":"Initial support response",

    "escalation_required":False,

    "conversation_history":[],

    "next_node":None
}


agent=EscalationAgent()

state=agent.run(state)

print()

print(state["response"])