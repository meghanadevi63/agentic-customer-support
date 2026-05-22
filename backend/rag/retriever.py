# backend/rag/retriever.py

from pathlib import Path
from dotenv import load_dotenv
import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


load_dotenv()


# Optional HF auth
os.environ["HF_TOKEN"] = os.getenv(
    "HUGGINGFACEHUB_API_TOKEN",
    ""
)


BASE_DIR = Path(__file__).resolve().parents[2]

CHROMA_PATH = BASE_DIR / "chroma_db"


# Load ONCE


embeddings = HuggingFaceEmbeddings(

    model_name=
    "sentence-transformers/all-MiniLM-L6-v2"

)


vectordb = Chroma(

    persist_directory=str(
        CHROMA_PATH
    ),

    embedding_function=
    embeddings

)


retriever = vectordb.as_retriever(

    search_type="mmr",

    search_kwargs={

        "k":4,

        "fetch_k":10,

        "lambda_mult":0.7
    }
)


# Return existing retriever


def get_retriever():

    return retriever


def retrieve(
    query:str
):

    docs = retriever.invoke(
        query
    )

    return docs


if __name__ == "__main__":

    query = (
        "My payment failed "
        "and money got deducted"
    )


    docs = retrieve(
        query
    )


    print(
        "\nRETRIEVED DOCUMENTS:\n"
    )


    seen=set()


    for i,doc in enumerate(
        docs,
        1
    ):


        source = doc.metadata.get(

            "source",

            "Unknown"
        )


        if source in seen:

            continue


        seen.add(
            source
        )


        print("="*60)

        print(
            f"Result:{i}"
        )

        print(
            "Source:",
            source
        )

        print()

        print(
            doc.page_content[:500]
        )

        print()