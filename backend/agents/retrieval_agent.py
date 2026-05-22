# backend/agents/retrieval_agent.py

from backend.workflow.state import SupportState

from backend.tools.retrieval_tool import (
    search_knowledge_base
)


class RetrievalAgent:


    def run(
        self,
        state: SupportState
    ):


        query = state["query"]


        context = search_knowledge_base.invoke(

            {
                "query":query
            }

        )


        state["retrieved_docs"] = [

            context

        ]


        print("\nRetrieved Documents:\n")

        print(
            len(
                state["retrieved_docs"]
            )
        )
        


        state[
            "agent_trace"
        ].append(

            "Supervisor evaluating state..."
        )

        state[
            "agent_trace"
        ].append(

            "Supervisor routed → retrieval_agent"
        )


        state[
            "agent_trace"
        ].append(

            {

                "agent":
                "Retrieval Agent",

                "documents":
                len(
            state[
                    "retrieved_docs"
                ]
            ),

            }

        )


        return state