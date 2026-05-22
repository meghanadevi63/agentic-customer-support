# backend/workflow/full_system_test.py

from backend.workflow.graph import graph


test_queries = [

    "My payment failed and amount got deducted",

    "I want to cancel my subscription",

    "I forgot my password and cannot login",

    "My order delivery is delayed",

    "I think this is fraud and I want legal action"
]


for i, query in enumerate(test_queries,1):

    print("\n")
    print("="*80)

    print(
        f"TEST CASE {i}"
    )

    print(
        f"QUERY: {query}"
    )

    print("="*80)


    state = {

        "query":query,

        "intent":None,

        "confidence":None,

        "retrieved_docs":[],

        "response":None,

        "escalation_required":False,

        "escalated":False,   # NEW

        "conversation_history":[],

        "next_node":None
    }


    result = graph.invoke(
        state
    )


    print("\nFINAL OUTPUT:\n")

    print(
        result["response"]
    )


    print("\nIntent:")

    print(
        result["intent"]
    )


    print("\nEscalated:")

    print(
        result["escalated"]
    )


    print("\nRetrieved docs:")

    print(
        len(
            result["retrieved_docs"]
        )
    )