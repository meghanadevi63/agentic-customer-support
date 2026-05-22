#backend/agents/intent_agent.py


from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_groq import ChatGroq

from backend.workflow.state import SupportState


load_dotenv()


class IntentOutput(BaseModel):

    intent: str = Field(
        description="Detected customer intent"
    )

    confidence: float = Field(
        description="Confidence score between 0 and 1"
    )


class IntentAgent:

    def __init__(self):

        self.llm = ChatGroq(

            model="llama-3.3-70b-versatile",

            temperature=0
        )


        self.structured_llm = (
            self.llm.with_structured_output(
                IntentOutput
            )
        )


    def run(
        self,
        state: SupportState
    ):

        query = state["query"]


        prompt = f"""

You are a customer support intent classifier.

Possible intents:

- payment_issue
- refund
- cancellation
- account_issue
- shipping
- technical_issue
- complaint
- general_query


Intent examples:

payment_issue:
- payment failed
- charged twice
- money deducted
- card charged
- invoice problem

refund:
- refund request
- return money
- delayed refund

cancellation:
- cancel plan
- close subscription
- unsubscribe

account_issue:
- forgot password
- login failed
- account locked
- reset password

shipping:
- delivery delayed
- tracking link issue
- shipment status
- order tracking
- package not delivered
- AWB issue

technical_issue:
- website crash
- app bug
- API not working
- page error

complaint:
- fraud
- legal action
- scam
- manager
- human agent
- angry complaint

general_query:
- unrelated questions
- greetings
- unsupported topics


Return only structured output.

Customer Query:

{query}

"""


        result = self.structured_llm.invoke(
            prompt
        )

        state["agent_trace"
        ].append(

            "Supervisor evaluating state..."
        )

        state[
            "agent_trace"
        ].append(

            "Supervisor routed → intent_agent"
        )


        state[
            "agent_trace"
        ].append(

            {

                "agent":
                "Intent Agent",

                "intent":
                result.intent,

                "confidence":
                result.confidence
            }

        )
        state["intent"] = result.intent

        state["confidence"] = result.confidence


        print("\nIntent identified:\n")

        print(
            result.intent,
            result.confidence
        )


        return state