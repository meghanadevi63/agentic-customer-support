# backend/tools/escalation_tool.py

from langchain.tools import tool
from backend.tools.crm_tool import create_atlas_ticket

@tool
def create_ticket(customer_id: str, thread_id: str, issue: str):
    """
    Create a real escalation ticket in the database.
    Required arguments: customer_id, thread_id, and the issue description.
    """
    
    ticket_id = create_atlas_ticket(customer_id, thread_id, issue)

    if ticket_id:
        return f"SUCCESS: Created Ticket {ticket_id} "
    else:
        return "ERROR: Could not save ticket to database."