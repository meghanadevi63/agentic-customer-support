# backend/tools/support_tool.py

from langchain.tools import tool


@tool
def collect_feedback():

    """
    Collect customer feedback
    """


    return """

Was your issue resolved?

1=Poor
5=Excellent

"""