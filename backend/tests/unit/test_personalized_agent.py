from unittest.mock import patch, MagicMock
from backend.agents.personalized_agent import PersonalizedAgent


class MockLLMResponse:
    def __init__(self, content):
        self.content = content


def base_state():

    return {

        "query":"Where is my order?",

        "intent":"shipping",

        "customer_profile":{

            "name":"Aarav",

            "orders":[
                {
                    "order_id":"ORD123",
                    "status":"Delayed"
                }
            ],

            "payments":[
                {
                    "transaction_id":"TXN111",
                    "status":"Failed"
                }
            ]
        },

        "response":""
    }


@patch(
"backend.agents.personalized_agent.ChatGroq"
)
def test_response_generated(mock_groq):

    mock_llm=MagicMock()

    mock_llm.invoke.return_value=(

        MockLLMResponse(
            "Hello Aarav, order ORD123 is delayed."
        )

    )

    mock_groq.return_value=mock_llm

    agent=PersonalizedAgent()

    state=base_state()

    result=agent.run(state)

    assert result["response"] != ""


@patch(
"backend.agents.personalized_agent.ChatGroq"
)
def test_customer_name_present(mock_groq):

    mock_llm=MagicMock()

    mock_llm.invoke.return_value=(

        MockLLMResponse(
            "Hello Aarav"
        )

    )

    mock_groq.return_value=mock_llm

    agent=PersonalizedAgent()

    state=base_state()

    result=agent.run(state)

    assert "Aarav" in result["response"]


@patch(
"backend.agents.personalized_agent.ChatGroq"
)
def test_order_id_present(mock_groq):

    mock_llm=MagicMock()

    mock_llm.invoke.return_value=(

        MockLLMResponse(
            "ORD123 delayed"
        )

    )

    mock_groq.return_value=mock_llm

    agent=PersonalizedAgent()

    state=base_state()

    result=agent.run(state)

    assert "ORD123" in result["response"]


@patch(
"backend.agents.personalized_agent.ChatGroq"
)
def test_payment_failure(mock_groq):

    mock_llm=MagicMock()

    mock_llm.invoke.return_value=(

        MockLLMResponse(
            "TXN111 failed"
        )

    )

    mock_groq.return_value=mock_llm

    agent=PersonalizedAgent()

    state=base_state()

    result=agent.run(state)

    assert "TXN111" in result["response"]


@patch(
"backend.agents.personalized_agent.ChatGroq"
)
def test_missing_profile(mock_groq):

    mock_llm=MagicMock()

    mock_llm.invoke.return_value=(

        MockLLMResponse(
            "General response"
        )

    )

    mock_groq.return_value=mock_llm

    agent=PersonalizedAgent()

    state={

        "query":"hello",

        "intent":"general_query",

        "customer_profile":{}
    }

    result=agent.run(state)

    assert result["response"]=="General response"


@patch(
"backend.agents.personalized_agent.ChatGroq"
)
def test_empty_query(mock_groq):

    mock_llm=MagicMock()

    mock_llm.invoke.return_value=(

        MockLLMResponse(
            "fallback"
        )

    )

    mock_groq.return_value=mock_llm

    agent=PersonalizedAgent()

    state=base_state()

    state["query"]=""

    result=agent.run(state)

    assert result["response"]=="fallback"