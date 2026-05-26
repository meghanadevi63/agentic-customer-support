from unittest.mock import patch, MagicMock
from backend.agents.response_agent import ResponseAgent


class MockLLMResponse:
    def __init__(self, content):
        self.content = content


def base_state(query="refund status"):

    return {
        "query": query,

        "intent":"refund",

        "retrieved_docs":[
            "Refund policy: refunds processed in 5 days"
        ],

        "customer_profile":{
            "name":"Aarav",
            "order_id":"ORD123",
            "status":"Delayed"
        },

        "conversation_history":[],

        "agent_trace":[],

        "response":"",

        "escalation_required":False
    }


@patch("backend.agents.response_agent.ChatGroq")
def test_response_generated(mock_groq):

    mock_llm=MagicMock()

    mock_llm.invoke.return_value=(
        MockLLMResponse(
            "Hello Aarav, your refund is being processed."
        )
    )

    mock_groq.return_value=mock_llm

    agent=ResponseAgent()

    state=base_state()

    result=agent.run(state)

    assert result["response"]!=""

    assert "Aarav" in result["response"]


@patch("backend.agents.response_agent.ChatGroq")
def test_history_saved(mock_groq):

    mock_llm=MagicMock()

    mock_llm.invoke.return_value=(
        MockLLMResponse(
            "Refund initiated."
        )
    )

    mock_groq.return_value=mock_llm

    agent=ResponseAgent()

    state=base_state()

    result=agent.run(state)

    history=result["conversation_history"]

    assert len(history)==1

    assert history[0]["role"]=="assistant"


@patch("backend.agents.response_agent.ChatGroq")
def test_trace_added(mock_groq):

    mock_llm=MagicMock()

    mock_llm.invoke.return_value=(
        MockLLMResponse(
            "response"
        )
    )

    mock_groq.return_value=mock_llm

    agent=ResponseAgent()

    state=base_state()

    result=agent.run(state)

    assert len(
        result["agent_trace"]
    )>=3


@patch("backend.agents.response_agent.ChatGroq")
def test_fraud_escalation(mock_groq):

    mock_llm=MagicMock()

    mock_llm.invoke.return_value=(
        MockLLMResponse(
            "Investigating issue"
        )
    )

    mock_groq.return_value=mock_llm

    agent=ResponseAgent()

    state=base_state(
        "This is fraud"
    )

    result=agent.run(state)

    assert (
        result["escalation_required"]
        is True
    )


@patch("backend.agents.response_agent.ChatGroq")
def test_legal_escalation(mock_groq):

    mock_llm=MagicMock()

    mock_llm.invoke.return_value=(
        MockLLMResponse(
            "Support response"
        )
    )

    mock_groq.return_value=mock_llm

    agent=ResponseAgent()

    state=base_state(
        "I will file legal action"
    )

    result=agent.run(state)

    assert (
        result["escalation_required"]
        is True
    )


@patch("backend.agents.response_agent.ChatGroq")
def test_empty_docs(mock_groq):

    mock_llm=MagicMock()

    mock_llm.invoke.return_value=(
        MockLLMResponse(
            "General help"
        )
    )

    mock_groq.return_value=mock_llm

    agent=ResponseAgent()

    state=base_state()

    state["retrieved_docs"]=[]

    result=agent.run(state)

    assert result["response"]=="General help"


@patch("backend.agents.response_agent.ChatGroq")
def test_customer_profile_exists(mock_groq):

    mock_llm=MagicMock()

    mock_llm.invoke.return_value=(
        MockLLMResponse(
            "Hello Aarav"
        )
    )

    mock_groq.return_value=mock_llm

    agent=ResponseAgent()

    state=base_state()

    result=agent.run(state)

    traces=result["agent_trace"]

    assert (
        traces[-1]
        ["customer_recognized"]
        =="Aarav"
    )