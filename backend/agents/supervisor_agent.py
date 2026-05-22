# backend/agents/supervisor_agent.py

from backend.workflow.state import SupportState


class SupervisorAgent:

    def route(self, state: SupportState):

        print("\nSupervisor evaluating state...\n")

        if state.get("next_node"):

            next_node = state["next_node"]

            state["next_node"] = None

            return next_node

        if not state.get("intent"):

            return "intent_agent"


        if len(state.get("retrieved_docs", [])) == 0:

            return "retrieval_agent"


        

        if state.get("escalation_required"):

            return "escalation_agent"


        if not state.get("response"):

            return "response_agent"


        return "followup_agent"