#backend/tools/test_retrieval_tool.py
from backend.tools.retrieval_tool import (
    search_knowledge_base
)


result = search_knowledge_base.invoke(

    {
        "query":
        "payment failed"
    }

)

print(result[:1000])