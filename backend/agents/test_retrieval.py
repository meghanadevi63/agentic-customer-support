#backend/agents/test_retrieval.py

from backend.agents.retrieval_agent import RetrievalAgent


state={

    "query":
    "My payment failed and amount got deducted",

    "intent":"payment_issue",

    "confidence":0.9,

    "retrieved_docs":[],

    "response":None,

    "escalation_required":False,

    "conversation_history":[],

    "next_node":None
}


agent=RetrievalAgent()

updated_state=agent.run(state)


print()

print(
updated_state["retrieved_docs"][0][:500]
)