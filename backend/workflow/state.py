# backend/workflow/state.py

from typing import Any, TypedDict, List, Optional,Dict


class SupportState(TypedDict):

    query: str

    customer_id: str

    thread_id: str
    
    customer_profile: Optional[Dict[str, Any]]
    
    intent: Optional[str]

    confidence: Optional[float]

    retrieved_docs: List[str]

    response: Optional[str]

    escalated: bool
    
    escalation_required: bool

    conversation_history: List[dict]

    next_node: Optional[str]

    agent_trace:list