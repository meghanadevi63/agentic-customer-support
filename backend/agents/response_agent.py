# backend/agents/response_agent.py

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from backend.workflow.state import SupportState


load_dotenv()


class ResponseAgent:

    def __init__(self):

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.2
        )


    def run(
        self,
        state: SupportState
    ):


        query = state["query"]

        intent = state["intent"]

        context = "\n\n".join(
            state["retrieved_docs"]
        )

        history = "\n".join(

            [

                f"{m['role']}: {m['content']}"

                for m in state.get(
                    "conversation_history",
                    []
                )

            ]

        )
        prompt = f"""

You are a professional customer support assistant.

Intent:
{intent}

Conversation History:
{history}

Customer Question:
{query}

Knowledge Base Context:
{context}



Rules:

Rules:

1. Use only retrieved context
2. Never invent information
3. Mention exact procedures if available
4. If payment deducted but order failed, explain support process
5. Be concise
6. Only say "I could not find enough information"
   if context is truly unrelated
7. Always maintain a polite and empathetic tone
8. Never mention escalation tickets
9. Never say specialist review initiated
10. Escalation decisions are handled separately
11. Never say "contact me"
12. Say "contact the support team" instead

"""


        result = self.llm.invoke(
            prompt
        )


        state["response"] = result.content


        # TRACE INFO

        state[
            "agent_trace"
        ].append(

            "Supervisor evaluating state..."
        )


        state[
            "agent_trace"
        ].append(

            "Supervisor routed → response_agent"
        )


        state[
            "agent_trace"
        ].append(

            {

                "agent":
                "Response Agent",

                "status":
                "Response generated",

                "length":
                f"{len(result.content)} chars"

            }

        )


        print(
            "\nGenerated Response:\n"
        )

        print(
            result.content
        )


        query_lower=query.lower()


        if any(

            word in query_lower

            for word in [

                "fraud",

                "legal",

                "lawsuit",

                "scam"

            ]

        ):


            state[
                "escalation_required"
            ]=True



        # ALWAYS SAVE HISTORY

        state[
            "conversation_history"
        ].append(

            {

                "role":"assistant",

                "content":
                result.content

            }

        )


        return state