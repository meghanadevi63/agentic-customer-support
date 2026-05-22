# backend/workflow/state.py

from typing import TypedDict, List, Optional


class SupportState(TypedDict):

    query: str

    intent: Optional[str]

    confidence: Optional[float]

    retrieved_docs: List[str]

    response: Optional[str]

    escalated: bool
    
    escalation_required: bool

    conversation_history: List[str]

    next_node: Optional[str]

    agent_trace:list