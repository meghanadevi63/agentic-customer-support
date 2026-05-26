from unittest.mock import patch, MagicMock
from backend.agents.followup_agent import FollowupAgent


class MockLLMResponse:
    def __init__(self, content):
        self.content = content


def base_state():

    return {

        "response":"Issue resolved",

        "escalated":False,

        "customer_profile":{
            "name":"Aarav"
        },

        "agent_trace":[]
    }


@patch(
"backend.agents.followup_agent.ChatGroq"
)
def test_response_appended(mock_groq):

    mock_llm=MagicMock()

    mock_llm.invoke.return_value=(
        MockLLMResponse(
            "Thanks Aarav. How would you rate my assistance today? (1=Poor, 5=Excellent)"
        )
    )

    mock_groq.return_value=mock_llm

    agent=FollowupAgent()

    state=base_state()

    result=agent.run(state)

    assert (
        "How would you rate"
        in
        result["response"]
    )


@patch(
"backend.agents.followup_agent.ChatGroq"
)
def test_escalation_mode(mock_groq):

    mock_llm=MagicMock()

    mock_llm.invoke.return_value=(
        MockLLMResponse(
            "Specialist reviewing case."
        )
    )

    mock_groq.return_value=mock_llm

    agent=FollowupAgent()

    state=base_state()

    state["escalated"]=True

    result=agent.run(state)

    trace=result["agent_trace"]

    assert (
        trace[-1]["mode"]
        ==
        "Escalation"
    )


@patch(
"backend.agents.followup_agent.ChatGroq"
)
def test_resolution_mode(mock_groq):

    mock_llm=MagicMock()

    mock_llm.invoke.return_value=(
        MockLLMResponse(
            "Glad I helped."
        )
    )

    mock_groq.return_value=mock_llm

    agent=FollowupAgent()

    state=base_state()

    result=agent.run(state)

    trace=result["agent_trace"]

    assert (
        trace[-1]["mode"]
        ==
        "Resolution"
    )


@patch(
"backend.agents.followup_agent.ChatGroq"
)
def test_trace_added(mock_groq):

    mock_llm=MagicMock()

    mock_llm.invoke.return_value=(
        MockLLMResponse(
            "response"
        )
    )

    mock_groq.return_value=mock_llm

    agent=FollowupAgent()

    state=base_state()

    result=agent.run(state)

    assert len(
        result["agent_trace"]
    )>=3


@patch(
"backend.agents.followup_agent.ChatGroq"
)
def test_customer_name(mock_groq):

    mock_llm=MagicMock()

    mock_llm.invoke.return_value=(
        MockLLMResponse(
            "Thanks Aarav"
        )
    )

    mock_groq.return_value=mock_llm

    agent=FollowupAgent()

    state=base_state()

    result=agent.run(state)

    assert (
        "Aarav"
        in
        result["response"]
    )


@patch(
"backend.agents.followup_agent.ChatGroq"
)
def test_empty_response(mock_groq):

    mock_llm=MagicMock()

    mock_llm.invoke.return_value=(
        MockLLMResponse(
            "Followup only"
        )
    )

    mock_groq.return_value=mock_llm

    agent=FollowupAgent()

    state=base_state()

    state["response"]=""

    result=agent.run(state)

    assert (
        result["response"]
        ==
        "Followup only"
    )