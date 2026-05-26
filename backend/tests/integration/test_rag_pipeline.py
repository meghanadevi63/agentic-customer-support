from unittest.mock import patch


@patch(
"backend.agents.response_agent.ChatGroq"
)
@patch(
"backend.agents.retrieval_agent.search_knowledge_base"
)
def test_rag_pipeline(
    mock_search,
    mock_llm
):

    from backend.agents.retrieval_agent import RetrievalAgent
    from backend.agents.response_agent import ResponseAgent


    mock_search.invoke.return_value=(
        "Refund policy"
    )

    llm=mock_llm.return_value

    llm.invoke.return_value.content=(
        "Refunds take 5 days"
    )


    retrieval=RetrievalAgent()

    response=ResponseAgent()


    state={

        "query":"refund",

        "intent":"refund",

        "retrieved_docs":[],

        "customer_profile":{},

        "conversation_history":[],

        "agent_trace":[],

        "response":"",

        "escalation_required":False
    }


    state=retrieval.run(state)

    state=response.run(state)

    assert len(
        state["retrieved_docs"]
    )==1

    assert (
        state["response"]
        ==
        "Refunds take 5 days"
    )