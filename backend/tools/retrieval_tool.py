# backend/tools/retrieval_tool.py

from langchain.tools import tool

from backend.rag.retriever import retrieve


@tool
def search_knowledge_base(
    query: str
):

    """
    Search company knowledge base
    and return relevant support information
    """


    docs = retrieve(query)


    if not docs:

        return "No information found"


    unique_docs = []

    seen = set()


    for doc in docs:

        content = doc.page_content.strip()


        # remove duplicate chunks
        if content not in seen:

            seen.add(
                content
            )

            unique_docs.append(
                content
            )
    print("Original docs:",len(docs))

    print("Merged docs:",
      len(unique_docs))

    return "\n\n".join(
        unique_docs
    )