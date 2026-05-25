# backend/agents/response_agent.py

import json
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

    def run(self, state: SupportState):
        query = state["query"]
        intent = state["intent"]
        
        # --- NEW: Extract customer data ---
        profile = state.get("customer_profile", {})
        profile_str = json.dumps(profile, indent=2)
        # ----------------------------------

        context = "\n\n".join(state.get("retrieved_docs", []))

        history = "\n".join(
            [
                f"{m['role']}: {m['content']}"
                for m in state.get("conversation_history", [])
            ]
        )

        # Updated Prompt to include Customer Profile
        prompt = f"""
You are a professional, personalized customer support assistant. 

CUSTOMER DATABASE PROFILE:
{profile_str}

Intent:
{intent}

Conversation History:
{history}

Customer Question:
{query}

Knowledge Base Context:
{context}

Rules:
1. Use the retrieved context AND the Customer Database Profile for accuracy.
2. ALWAYS respond in English, regardless of the customer's preferred language.
3. Address the customer by their 'name' found in the database profile.
4. If the user asks about an order or payment, mention the specific 'order_id' or 'transaction_id' and its 'status' from the profile.
5. Never invent information or IDs not present in the profile.
6. Mention exact procedures if available in context.
7. If payment was deducted but order failed (found in profile), explain the support process clearly.
8. Be concise (maximum 4-5 sentences).
9. Only say "I could not find enough information" if context and profile are truly unrelated.
10. Always maintain a polite and empathetic tone.
11. Never mention escalation tickets or specialist reviews in this response.
12. Never say "contact me"; say "let me help you to contact the support team" instead.
"""

        result = self.llm.invoke(prompt)
        state["response"] = result.content

        # TRACE INFO
        state["agent_trace"].append("Supervisor evaluating state...")
        state["agent_trace"].append("Supervisor routed → response_agent")
        state["agent_trace"].append(
            {
                "agent": "Response Agent",
                "status": "Response generated",
                "length": f"{len(result.content)} chars",
                "customer_recognized": profile.get("name", "Unknown") # Added to trace
            }
        )

        print("\nGenerated Response:\n")
        print(result.content)

        query_lower = query.lower()
        if any(
            word in query_lower
            for word in ["fraud", "legal", "lawsuit", "scam"]
        ):
            state["escalation_required"] = True

        # ALWAYS SAVE HISTORY
        state["conversation_history"].append(
            {
                "role": "assistant",
                "content": result.content
            }
        )

        return state