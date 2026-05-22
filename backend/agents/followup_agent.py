# backend/agents/followup_agent.py

from backend.workflow.state import SupportState

from backend.tools.support_tool import (
    collect_feedback
)


class FollowupAgent:

    def run(
        self,
        state: SupportState
    ):


        followup = collect_feedback.invoke(
            {}
        )


        state[
            "response"
        ] += followup


        # TRACE INFO

        state[
            "agent_trace"
        ].append(

            "Supervisor evaluating state..."
        )


        state[
            "agent_trace"
        ].append(

            "Supervisor routed → followup_agent"
        )


        state[
            "agent_trace"
        ].append(

            {

                "agent":
                "Followup Agent",

                "status":
                "Follow-up added"

            }

        )


        print(
            "\nFollow-up added"
        )


        return state