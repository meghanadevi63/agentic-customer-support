# backend/main.py

from fastapi import FastAPI
from pydantic import BaseModel

from backend.workflow.graph import graph
from backend.tools.crm_tool import (
    fetch_customer_profile, 
    save_interaction, 
    get_customer_sessions, 
    get_thread_transcript,
    save_feedback
)

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

    customer_id: str

class FeedbackRequest(BaseModel):
    customer_id: str
    thread_id: str
    rating: int
    comment: str = ""



@app.get("/")
def home():

    return {

        "message":

        "Customer Support API running"
    }



@app.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    """Endpoint to save user rating to MongoDB."""
    fb_id = save_feedback(
        customer_id=request.customer_id,
        thread_id=request.thread_id,
        rating=request.rating,
        comment=request.comment
    )
    if fb_id:
        return {"status": "success", "feedback_id": fb_id}
    return {"status": "error", "message": "Failed to save to database"}

@app.get("/history/sessions/{customer_id}")
def sessions(customer_id: str):
    """Fetch all unique past chat threads for a specific customer."""
    return get_customer_sessions(customer_id)


@app.get("/history/transcript/{thread_id}")
def transcript(thread_id: str):
    """Fetch the full message list for a specific conversation thread."""
    return get_thread_transcript(thread_id)

@app.post(
    "/chat"
)
def chat(
    request: ChatRequest
):

    profile = fetch_customer_profile(request.customer_id)
    state = {

        "query":
        request.query,

        "thread_id": request.thread_id, 

        "customer_id": request.customer_id, 
        
        "customer_profile": profile,      

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


    
    save_interaction(
        customer_id=request.customer_id,
        thread_id=request.thread_id,
        query=request.query,
        response=result["response"],
        intent=result["intent"]
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