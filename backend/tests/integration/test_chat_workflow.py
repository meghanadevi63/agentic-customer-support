from unittest.mock import patch


@patch(
"backend.workflow.graph.supervisor"
)
def test_workflow_route(
        mock_supervisor
):

    mock_supervisor.route.return_value=(
        "intent_agent"
    )

    from backend.workflow.graph import route

    state={

        "intent":None
    }

    result=route(state)

    assert (
        result
        ==
        "intent_agent"
    )


@patch(
"backend.workflow.graph.supervisor"
)
def test_followup_route(
        mock_supervisor
):

    mock_supervisor.route.return_value=(
        "followup_agent"
    )

    from backend.workflow.graph import route

    state={

        "response":"done"
    }

    result=route(state)

    assert (
        result
        ==
        "followup_agent"
    )