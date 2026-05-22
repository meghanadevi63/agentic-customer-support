# backend/main.py

from fastapi import FastAPI
from pydantic import BaseModel

from backend.workflow.graph import graph


app = FastAPI(

    title="Agentic Customer Support API",

    description="Multi-Agent Customer Support System",

    version="1.0"
)


class ChatRequest(
    BaseModel
):

    query:str

    thread_id:str


@app.get("/")
def home():

    return {

        "message":

        "Customer Support API running"
    }


@app.post(
    "/chat"
)
def chat(
    request: ChatRequest
):


    state = {

        "query":
        request.query,

        "intent":
        None,

        "confidence":
        None,

        "retrieved_docs":
        [],

        "response":
        None,

        "escalation_required":
        False,

        "escalated":
        False,

        "conversation_history":[],

        "next_node":
        None,

        "agent_trace":[]
    }


    config = {

        "configurable":{

            "thread_id":
            request.thread_id
        }

    }


    # Load existing checkpoint state

    snapshot = graph.get_state(
        config
    )


    if snapshot.values:

        state[
            "conversation_history"
        ] = snapshot.values.get(

            "conversation_history",

            []
        )


    # Append current user message

    state[
        "conversation_history"
    ].append(

        {

            "role":"user",

            "content":
            request.query
        }

    )


    result = graph.invoke(

        state,

        config=config
    )


    return {

        "query":
        request.query,

        "intent":
        result[
            "intent"
        ],

        "response":
        result[
            "response"
        ],

        "escalated":
        result[
            "escalated"
        ],

        "trace":
        result[
        "agent_trace"
        ]
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "backend.main:app",

        host="0.0.0.0",

        port=8000,

        reload=True
    )