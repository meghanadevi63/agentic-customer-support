# backend/agents/escalation_agent.py

from backend.workflow.state import SupportState
from backend.tools.escalation_tool import create_ticket

class EscalationAgent:

    def run(self, state: SupportState):
        query = state["query"].lower()
        customer_id = state.get("customer_id", "GUEST")
        thread_id = state.get("thread_id", "UNKNOWN")
        confidence = state.get("confidence", 1)

        escalation_keywords = [
            "fraud", "legal", "lawsuit", "angry", "complaint", 
            "scam", "refund not received", "manager", "human agent"
        ]

        if confidence < 0.6:
            state["escalation_required"] = True

        for word in escalation_keywords:
            if word in query:
                state["escalation_required"] = True
                break

        if state["escalation_required"]:
           
            ticket_response = create_ticket.invoke({
                "customer_id": customer_id,
                "thread_id": thread_id,
                "issue": query
            })

            state["response"] += f"\n\nYour issue requires specialist review.\n{ticket_response}\nA support specialist will contact you shortly."

            state["escalated"] = True
            state["escalation_required"] = False
            state["next_node"] = "followup_agent"

            # TRACE INFO
            ticket_id_extracted = "Created"
            if "TKT-" in ticket_response:
                ticket_id_extracted = "TKT-" + ticket_response.split("TKT-")[1].split()[0]

            state["agent_trace"].append("Supervisor evaluating state...")
            state["agent_trace"].append("Supervisor routed → escalation_agent")
            state["agent_trace"].append({
                "agent": "Escalation Agent",
                "escalated": True,
                "ticket": ticket_id_extracted,
                "database_save": "Success" if "SUCCESS" in ticket_response else "Failed"
            })

        print("\nEscalation status:", state["escalated"])
        return state