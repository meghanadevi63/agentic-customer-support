# backend/agents/escalation_agent.py

from backend.workflow.state import SupportState

from backend.tools.escalation_tool import (
    create_ticket
)


class EscalationAgent:

    def run(
        self,
        state: SupportState
    ):

        query = state["query"].lower()

        confidence = state.get(
            "confidence",
            1
        )


        escalation_keywords = [

            "fraud",

            "legal",

            "lawsuit",

            "angry",

            "complaint",

            "scam",

            "refund not received",

            "manager",

            "human agent"
        ]


        if confidence < 0.6:

            state[
                "escalation_required"
            ] = True


        for word in escalation_keywords:

            if word in query:

                state[
                    "escalation_required"
                ] = True

                break


        if state[
            "escalation_required"
        ]:


            ticket = create_ticket.invoke(

                {
                    "issue": query
                }

            )


            state["response"] += f"""

Your issue requires specialist review.

{ticket}

A support specialist will contact you shortly.
"""

            # FIX
            state[
                "escalated"
            ] = True


            state[
                "escalation_required"
            ] = False


            state[
                "next_node"
            ] = "followup_agent"


        # TRACE INFO

        

        ticket_id=None


        if state[
            "escalated"
        ]:

            try:

                if "TKT-" in ticket:

                    ticket_id=(

                        "TKT-"+
                        ticket.split(
                            "TKT-"
                        )[1].split()[0]

                    )

                else:

                    ticket_id="Created"

            except:

                ticket_id="Created"



            state[
                "agent_trace"
            ].append(

                "Supervisor evaluating state..."
            )


            state[
                "agent_trace"
            ].append(

                "Supervisor routed → escalation_agent"
            )


            state[
                "agent_trace"
            ].append(

                {

                    "agent":
                    "Escalation Agent",

                    "escalated":
                    state[
                        "escalated"
                    ],

                    "ticket":
                    ticket_id

                }

            )


        print(
            "\nEscalation:",
            state[
                "escalated"
            ]
        )


        return state