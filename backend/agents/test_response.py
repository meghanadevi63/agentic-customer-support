#backend/agents/test_response.py
from backend.agents.response_agent import ResponseAgent
from backend.agents.retrieval_agent import RetrievalAgent
from backend.agents.intent_agent import IntentAgent


state={

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


intent=IntentAgent()

state=intent.run(state)


retrieval=RetrievalAgent()

state=retrieval.run(state)


response=ResponseAgent()

state=response.run(state)