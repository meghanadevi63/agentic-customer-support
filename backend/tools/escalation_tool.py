# backend/tools/escalation_tool.py

from langchain.tools import tool

import uuid


@tool
def create_ticket(
    issue:str
):

    """
    Create escalation ticket
    """


    ticket = (

        "TKT-"

        +

        str(
            uuid.uuid4()
        )[:8]

    )


    return (

        f"Created Ticket: {ticket}\n"

        f"Issue:{issue}"

    )