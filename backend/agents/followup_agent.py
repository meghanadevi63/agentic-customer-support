# backend/agents/followup_agent.py

from langchain_groq import ChatGroq
from backend.workflow.state import SupportState

class FollowupAgent:

    def __init__(self):
        """
        Initialize the LLM for the Followup Agent.
        Using a low temperature (0.3) to ensure polite and consistent closing remarks.
        """
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3
        )

    def run(self, state: SupportState):
        # 1. Extract context from the state
        customer_name = state.get("customer_profile", {}).get("name", "Customer")
        is_escalated = state.get("escalated", False)
        
        # 2. Construct the Detailed Prompt
        prompt = f"""
        You are a professional and empathetic customer support closer. 
        Your task is to write a brief, 1-sentence closing remark and a feedback request.

        CONTEXT:
        Customer Name: {customer_name}
        Was the issue Escalated to a human?: {is_escalated}

        RULES:
        1. LANGUAGE: Respond in ENGLISH ONLY.
        2. PERSONALIZATION: Address the customer by their first name.
        3. SCENARIO A (NOT ESCALATED): Thank them for reaching out and express hope that the information helped.
        4. SCENARIO B (ESCALATED): Acknowledge that a specialist is reviewing their case and will be in touch shortly.
        5. TONE: Be professional, warm, and concise.
        6. MANDATORY CLOSING: You must end the response exactly with this phrase:
           "How would you rate my assistance today? (1=Poor, 5=Excellent)"

        Max length: 2 sentences total.
        """

        # 3. Invoke the LLM
        result = self.llm.invoke(prompt)

        # 4. Append the AI closing to the existing response
        if state["response"]:
            state["response"] += f"\n\n{result.content}"
        else:
            state["response"] = result.content

        # 5. TRACE INFO
        state["agent_trace"].append("Supervisor evaluating state...")
        state["agent_trace"].append("Supervisor routed → followup_agent")
        state["agent_trace"].append(
            {
                "agent": "Followup Agent",
                "status": "Personalized closing generated",
                "mode": "Escalation" if is_escalated else "Resolution"
            }
        )

        print(f"\nFollow-up added (Mode: {'Escalated' if is_escalated else 'Resolved'})")

        return state