from unittest.mock import patch, MagicMock
from backend.agents.escalation_agent import EscalationAgent


def base_state(query="refund issue"):

    return {

        "query":query,

        "customer_id":"CUS001",

        "thread_id":"TH001",

        "confidence":1,

        "response":"Support reply",

        "escalated":False,

        "escalation_required":False,

        "next_node":None,

        "agent_trace":[]
    }


@patch(
"backend.agents.escalation_agent.create_ticket"
)
def test_fraud_escalation(mock_ticket):

    mock_ticket.invoke=MagicMock(

        return_value=
        "SUCCESS TKT-123 created"
    )

    agent=EscalationAgent()

    state=base_state(
        "this is fraud"
    )

    result=agent.run(state)

    assert result["escalated"] is True

    assert result["next_node"]=="followup_agent"


@patch(
"backend.agents.escalation_agent.create_ticket"
)
def test_low_confidence_escalates(mock_ticket):

    mock_ticket.invoke=MagicMock(

        return_value=
        "SUCCESS TKT-999 created"
    )

    agent=EscalationAgent()

    state=base_state()

    state["confidence"]=0.3

    result=agent.run(state)

    assert result[
        "escalated"
    ] is True


@patch(
"backend.agents.escalation_agent.create_ticket"
)
def test_ticket_called(mock_ticket):

    mock_ticket.invoke=MagicMock(

        return_value=
        "SUCCESS TKT-222 created"
    )

    agent=EscalationAgent()

    state=base_state(
        "manager complaint"
    )

    agent.run(state)

    mock_ticket.invoke.assert_called_once()


@patch(
"backend.agents.escalation_agent.create_ticket"
)
def test_trace_added(mock_ticket):

    mock_ticket.invoke=MagicMock(

        return_value=
        "SUCCESS TKT-333 created"
    )

    agent=EscalationAgent()

    state=base_state(
        "human agent"
    )

    result=agent.run(state)

    assert len(
        result["agent_trace"]
    )>=3


@patch(
"backend.agents.escalation_agent.create_ticket"
)
def test_ticket_id_extracted(mock_ticket):

    mock_ticket.invoke=MagicMock(

        return_value=
        "SUCCESS TKT-555 created"
    )

    agent=EscalationAgent()

    state=base_state(
        "lawsuit"
    )

    result=agent.run(state)

    trace=result[
        "agent_trace"
    ]

    assert (
        trace[-1]["ticket"]
        ==
        "TKT-555"
    )


@patch(
"backend.agents.escalation_agent.create_ticket"
)
def test_response_updated(mock_ticket):

    mock_ticket.invoke=MagicMock(

        return_value=
        "SUCCESS TKT-777 created"
    )

    agent=EscalationAgent()

    state=base_state(
        "fraud"
    )

    result=agent.run(state)

    assert (
        "specialist review"
        in
        result["response"]
    )