# backend/workflow/graph.py

from langgraph.graph import StateGraph, END

from backend.workflow.state import SupportState

from backend.agents.supervisor_agent import SupervisorAgent
from backend.agents.intent_agent import IntentAgent
from backend.agents.retrieval_agent import RetrievalAgent
from backend.agents.response_agent import ResponseAgent
from backend.agents.escalation_agent import EscalationAgent
from backend.agents.followup_agent import FollowupAgent

from langgraph.checkpoint.memory import InMemorySaver
# Initialize agents


supervisor = SupervisorAgent()

intent = IntentAgent()

retrieval = RetrievalAgent()

response = ResponseAgent()

escalation = EscalationAgent()

followup=FollowupAgent()

# Create graph


builder = StateGraph(
    SupportState
)


# Add nodes


builder.add_node(
    "supervisor",
    lambda state: state
)

builder.add_node(
    "intent_agent",
    intent.run
)

builder.add_node(
    "retrieval_agent",
    retrieval.run
)

builder.add_node(
    "response_agent",
    response.run
)

builder.add_node(
    "escalation_agent",
    escalation.run
)

builder.add_node(
    "followup_agent",
    followup.run
)

# Supervisor routing


def route(
    state: SupportState
):

    next_node = supervisor.route(
        state
    )

    print(
        f"\nSupervisor routed → {next_node}"
    )

    return next_node



# Entry point


builder.set_entry_point(
    "supervisor"
)


# Dynamic routing


builder.add_conditional_edges(
    "supervisor",
    route,
    {

        "intent_agent":
        "intent_agent",

        "retrieval_agent":
        "retrieval_agent",

        "response_agent":
        "response_agent",

        "escalation_agent":
        "escalation_agent",

        "followup_agent":
        "followup_agent"
    }
)


# Return control
# back to supervisor


builder.add_edge(
    "intent_agent",
    "supervisor"
)

builder.add_edge(
    "retrieval_agent",
    "supervisor"
)

builder.add_edge(
    "response_agent",
    "supervisor"
)

builder.add_edge(
    "escalation_agent",
    "supervisor"
)

builder.add_edge(
    "followup_agent",
    END
)

checkpointer = InMemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)