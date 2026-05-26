from unittest.mock import MagicMock, patch
from backend.agents.intent_agent import IntentAgent


# mock structured output object
class MockIntentResult:
    def __init__(self, intent, confidence):
        self.intent = intent
        self.confidence = confidence


def base_state(query):
    return {
        "query": query,
        "intent": "",
        "confidence": 0,
        "agent_trace": []
    }


@patch("backend.agents.intent_agent.ChatGroq")
def test_refund_intent(mock_groq):

    mock_llm = MagicMock()

    mock_structured = MagicMock()

    mock_structured.invoke.return_value = (
        MockIntentResult(
            "refund",
            0.95
        )
    )

    mock_llm.with_structured_output.return_value = (
        mock_structured
    )

    mock_groq.return_value = mock_llm


    agent = IntentAgent()

    state = base_state(
        "I want refund"
    )

    result = agent.run(state)

    assert result["intent"] == "refund"

    assert result["confidence"] == 0.95

    assert len(
        result["agent_trace"]
    ) > 0


@patch("backend.agents.intent_agent.ChatGroq")
def test_shipping_intent(mock_groq):

    mock_llm = MagicMock()

    mock_structured = MagicMock()

    mock_structured.invoke.return_value = (
        MockIntentResult(
            "shipping",
            0.90
        )
    )

    mock_llm.with_structured_output.return_value = (
        mock_structured
    )

    mock_groq.return_value = mock_llm


    agent=IntentAgent()

    state=base_state(
        "Where is my package?"
    )

    result=agent.run(state)

    assert result["intent"]=="shipping"


@patch("backend.agents.intent_agent.ChatGroq")
def test_account_issue(mock_groq):

    mock_llm=MagicMock()

    mock_structured=MagicMock()

    mock_structured.invoke.return_value=(
        MockIntentResult(
            "account_issue",
            0.87
        )
    )

    mock_llm.with_structured_output.return_value=(
        mock_structured
    )

    mock_groq.return_value=mock_llm


    agent=IntentAgent()

    state=base_state(
        "Forgot password"
    )

    result=agent.run(state)

    assert result["intent"]=="account_issue"


@patch("backend.agents.intent_agent.ChatGroq")
def test_general_query(mock_groq):

    mock_llm=MagicMock()

    mock_structured=MagicMock()

    mock_structured.invoke.return_value=(
        MockIntentResult(
            "general_query",
            0.80
        )
    )

    mock_llm.with_structured_output.return_value=(
        mock_structured
    )

    mock_groq.return_value=mock_llm


    agent=IntentAgent()

    state=base_state(
        "Hello"
    )

    result=agent.run(state)

    assert result["intent"]=="general_query"


@patch("backend.agents.intent_agent.ChatGroq")
def test_empty_query(mock_groq):

    mock_llm=MagicMock()

    mock_structured=MagicMock()

    mock_structured.invoke.return_value=(
        MockIntentResult(
            "general_query",
            0.40
        )
    )

    mock_llm.with_structured_output.return_value=(
        mock_structured
    )

    mock_groq.return_value=mock_llm


    agent=IntentAgent()

    state=base_state("")

    result=agent.run(state)

    assert result["intent"] is not None


@patch("backend.agents.intent_agent.ChatGroq")
def test_agent_trace_added(mock_groq):

    mock_llm=MagicMock()

    mock_structured=MagicMock()

    mock_structured.invoke.return_value=(
        MockIntentResult(
            "refund",
            0.99
        )
    )

    mock_llm.with_structured_output.return_value=(
        mock_structured
    )

    mock_groq.return_value=mock_llm


    agent=IntentAgent()

    state=base_state(
        "Refund request"
    )

    result=agent.run(state)

    traces=result["agent_trace"]

    assert len(traces)>=3