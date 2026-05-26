from backend.agents.supervisor_agent import SupervisorAgent


def base_state():
    return {
        "query":"test",
        "intent":None,
        "retrieved_docs":[],
        "response":"",
        "next_node":None,
        "escalation_required":False
    }


def test_priority_next_node():

    agent=SupervisorAgent()

    state=base_state()

    state["next_node"]="response_agent"

    result=agent.route(state)

    assert result=="response_agent"

    assert state["next_node"] is None


def test_missing_intent():

    agent=SupervisorAgent()

    state=base_state()

    state["intent"]=None

    result=agent.route(state)

    assert result=="intent_agent"


def test_retrieval_route():

    agent=SupervisorAgent()

    state=base_state()

    state["intent"]="refund"

    state["retrieved_docs"]=[]

    result=agent.route(state)

    assert result=="retrieval_agent"


def test_escalation_route():

    agent=SupervisorAgent()

    state=base_state()

    state["intent"]="complaint"

    state["retrieved_docs"]=["policy"]

    state["escalation_required"]=True

    result=agent.route(state)

    assert result=="escalation_agent"


def test_response_route():

    agent=SupervisorAgent()

    state=base_state()

    state["intent"]="refund"

    state["retrieved_docs"]=["refund policy"]

    state["response"]=""

    result=agent.route(state)

    assert result=="response_agent"


def test_followup_route():

    agent=SupervisorAgent()

    state=base_state()

    state["intent"]="refund"

    state["retrieved_docs"]=["refund policy"]

    state["response"]="Refund initiated"

    result=agent.route(state)

    assert result=="followup_agent"


def test_retrieved_docs_none():

    agent=SupervisorAgent()

    state=base_state()

    state["intent"]="shipping"

    state["retrieved_docs"]=[]

    result=agent.route(state)

    assert result=="retrieval_agent"