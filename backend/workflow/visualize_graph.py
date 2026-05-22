# backend/workflow/visualize_graph.py

from pathlib import Path

from backend.workflow.graph import graph


BASE_DIR = Path(__file__).resolve().parents[2]

DOCS_DIR = BASE_DIR / "docs"

DOCS_DIR.mkdir(exist_ok=True)


graph_image = graph.get_graph().draw_mermaid_png()


with open(
    DOCS_DIR / "workflow_graph.png",
    "wb"
) as f:

    f.write(graph_image)


print(
    "\nGraph saved to docs/workflow_graph.png"
)