from pathlib import Path

from loaders import KnowledgeLoader


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = BASE_DIR / "data"

print("DATA PATH:", DATA_PATH)


loader = KnowledgeLoader(DATA_PATH)

docs = loader.load_all()

print(f"\nTotal documents loaded: {len(docs)}")


if docs:

    print("\nSample document:\n")

    print(docs[1])

    print(docs[0].page_content[:500])

else:

    print("No documents found")