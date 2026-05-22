#backend/rag/ingest.py
from pathlib import Path
from dotenv import load_dotenv
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from loaders import KnowledgeLoader

os.environ["HF_TOKEN"] = os.getenv(
    "HUGGINGFACEHUB_API_TOKEN",
    ""
)

load_dotenv()


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = BASE_DIR / "data"

CHROMA_PATH = BASE_DIR / "chroma_db"


def create_vector_store():

    print("\nLoading documents...\n")

    loader = KnowledgeLoader(DATA_PATH)

    docs = loader.load_all()

    print(f"\nLoaded docs:{len(docs)}")


    splitter = RecursiveCharacterTextSplitter(

        chunk_size=500,

        chunk_overlap=100
    )


    chunks = splitter.split_documents(docs)

    print(f"Chunks created:{len(chunks)}")


    embeddings = HuggingFaceEmbeddings(

        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


    vectordb = Chroma.from_documents(

        documents=chunks,

        embedding=embeddings,

        persist_directory=str(CHROMA_PATH)
    )


    print("\nVector DB created successfully")

    print(f"\nSaved to:{CHROMA_PATH}")


if __name__=="__main__":

    create_vector_store()