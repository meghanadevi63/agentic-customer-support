#backend/workflow/test_graph.py
from backend.workflow.graph import graph


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


result=graph.invoke(
    state
)


print()

print(
result["response"]
)