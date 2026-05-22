#python backend/rag/view_loaded_content.py
from pathlib import Path
from loaders import KnowledgeLoader


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = BASE_DIR / "data"


print("\nLoading documents...\n")

loader = KnowledgeLoader(DATA_PATH)

docs = loader.load_all()


print("\n")
print("="*80)
print(f"TOTAL DOCUMENTS LOADED: {len(docs)}")
print("="*80)


# Save everything into a text file
output_path = BASE_DIR / "all_loaded_content.txt"


with open(
    output_path,
    "w",
    encoding="utf8"
) as f:

    for i, doc in enumerate(docs):

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        doc_type = doc.metadata.get(
            "type",
            "Unknown"
        )

        print("\n")
        print("="*80)

        print(
            f"Document {i+1}"
        )

        print(
            "Source:",
            source
        )

        print(
            "Type:",
            doc_type
        )

        print(
            "Characters:",
            len(doc.page_content)
        )


        # Write full content

        f.write("\n")
        f.write("="*100)
        f.write("\n")

        f.write(
            f"Document: {i+1}\n"
        )

        f.write(
            f"Source: {source}\n"
        )

        f.write(
            f"Type: {doc_type}\n"
        )

        f.write(
            f"Characters: {len(doc.page_content)}\n"
        )

        f.write("\nFULL CONTENT:\n\n")

        f.write(
            doc.page_content
        )

        f.write("\n\n")


print("\n")
print("="*80)
print(
    f"Saved complete content to:\n{output_path}"
)
print("="*80)