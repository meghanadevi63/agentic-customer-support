from unittest.mock import patch, MagicMock
from backend.agents.retrieval_agent import RetrievalAgent


def base_state(query="refund policy"):

    return {
        "query": query,
        "retrieved_docs": [],
        "agent_trace": []
    }


@patch("backend.agents.retrieval_agent.search_knowledge_base")
def test_document_retrieved(mock_tool):

    mock_tool.invoke = MagicMock(
        return_value="Refunds processed within 5 days"
    )

    agent = RetrievalAgent()

    state = base_state()

    result = agent.run(state)

    assert len(result["retrieved_docs"]) == 1

    assert (
        result["retrieved_docs"][0]
        ==
        "Refunds processed within 5 days"
    )


@patch("backend.agents.retrieval_agent.search_knowledge_base")
def test_empty_result(mock_tool):

    mock_tool.invoke = MagicMock(
        return_value=""
    )

    agent = RetrievalAgent()

    state = base_state()

    result = agent.run(state)

    assert len(result["retrieved_docs"]) == 1


@patch("backend.agents.retrieval_agent.search_knowledge_base")
def test_agent_trace_exists(mock_tool):

    mock_tool.invoke = MagicMock(
        return_value="Some policy"
    )

    agent = RetrievalAgent()

    state = base_state()

    result = agent.run(state)

    assert len(result["agent_trace"]) >= 3


@patch("backend.agents.retrieval_agent.search_knowledge_base")
def test_document_count(mock_tool):

    mock_tool.invoke = MagicMock(
        return_value="shipping information"
    )

    agent = RetrievalAgent()

    state = base_state()

    result = agent.run(state)

    trace = result["agent_trace"]

    assert trace[-1]["documents"] == 1


@patch("backend.agents.retrieval_agent.search_knowledge_base")
def test_query_passed(mock_tool):

    mock_tool.invoke = MagicMock(
        return_value="policy"
    )

    agent = RetrievalAgent()

    state = base_state(
        "cancel subscription"
    )

    agent.run(state)

    mock_tool.invoke.assert_called_once_with(
        {
            "query":
            "cancel subscription"
        }
    )


@patch("backend.agents.retrieval_agent.search_knowledge_base")
def test_special_characters(mock_tool):

    mock_tool.invoke = MagicMock(
        return_value="result"
    )

    agent = RetrievalAgent()

    state = base_state("@#$%^&*?")

    result = agent.run(state)

    assert (
        result["retrieved_docs"][0]
        ==
        "result"
    )