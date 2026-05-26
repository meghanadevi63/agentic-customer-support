from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


@patch("backend.main.save_interaction")
@patch("backend.main.fetch_customer_profile")
@patch("backend.main.graph")
def test_chat_api(
        mock_graph,
        mock_profile,
        mock_save
):

    mock_profile.return_value = {
        "name":"Aarav"
    }

    mock_graph.get_state.return_value.values = {}

    mock_graph.invoke.return_value = {

        "intent":"refund",

        "response":"Refund initiated",

        "escalated":False,

        "agent_trace":[]
    }

    response = client.post(

        "/chat",

        json={

            "query":"refund request",

            "thread_id":"T1",

            "customer_id":"CUS001"
        }

    )

    assert response.status_code == 200

    data=response.json()

    assert data["intent"]=="refund"

    assert data["response"]=="Refund initiated"