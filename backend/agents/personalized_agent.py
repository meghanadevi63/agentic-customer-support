# backend/agents/personalized_agent.py
import json
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

class PersonalizedAgent:
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)

    def run(self, state: dict):
        profile = state.get("customer_profile", {})
        query = state.get("query", "")
        intent = state.get("intent", "general_query")
        
        profile_context = json.dumps(profile, indent=2)

        system_prompt = f"""
        You are an elite customer support assistant. You have access to the customer's real-time database.
        
        CUSTOMER DATA:
        {profile_context}

        RULES:
        1. ALWAYS respond in English, regardless of the customer's preferred language.
            1.1 Address the customer by their 'name' found in the profile.
        2. If they ask about orders or payments, look at the 'orders' and 'payments' arrays in the context.
        3. Mention specific IDs (Order ID, Transaction ID) and Statuses (Delayed, Failed, etc.).
        4. Be empathetic. If a payment failed, apologize and explain why (failure_reason).
        5. Stay concise.
        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query)
        ]
        
        response = self.llm.invoke(messages)
        state["response"] = response.content
        return state