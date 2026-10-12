
import os
from pathlib import Path
from dotenv import load_dotenv
from hydra_db import HydraDB

load_dotenv(Path(__file__).parent / ".env", override=True)

client = HydraDB(token=os.environ["HYDRA_DB_API_KEY"])

DATABASE = "default-tenant"
COLLECTION = "customer-success-brain"

question = (
    "Why is Acme Health's production launch blocked? "
    "Identify unresolved issues, owners, and next actions."
)

print("Searching HydraDB...")
print("Question:", question)

try:
    response = client.query(
        database=DATABASE,
        collection=COLLECTION,
        query=question,
        max_results=8,
        graph_context=True,
    )

    if not response.success:
        print("Search failed:", response.error)
    else:
        data = response.data

        chunks = data.chunks or []
        print(f"\nRetrieved {len(chunks)} chunks")

        for i, chunk in enumerate(chunks, 1):
            print(f"\n--- Result {i} ---")
            print("Source:", chunk.source_title)
            print("Score:", chunk.relevancy_score)
            print("Content:", (chunk.chunk_content or "")[:1000])

        print("\n=== GRAPH ===")
        if data.graph and data.graph.paths:
            for path in data.graph.paths[:5]:
                print(path.combined_context)
        else:
            print("No graph paths available yet.")

        print("\n=== LLM CONTEXT ===")
        print((data.llm_prompt or "")[:5000])

except Exception as e:
    print("Search error:", type(e).__name__, str(e))
    raise
