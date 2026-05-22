# backend/agents/test_supervisor.py

from backend.agents.supervisor_agent import SupervisorAgent


state = {

    "query":"My payment failed and money deducted",

    "intent":None,

    "confidence":None,

    "retrieved_docs":[],

    "response":None,

    "escalation_required":False,

    "conversation_history":[],

    "next_node":None
}


supervisor = SupervisorAgent()

next_node = supervisor.route(state)

print("\nNext Node:", next_node)