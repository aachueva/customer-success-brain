
import os
from pathlib import Path
from dotenv import load_dotenv
from hydra_db import HydraDB

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env", override=True)

client = HydraDB(token=os.environ["HYDRA_DB_API_KEY"])
DATABASE = "default-tenant"
COLLECTION = "customer-success-brain"

# Find the synthetic documents in the project
documents = [
    p for p in ROOT.rglob("*")
    if p.is_file()
    and p.suffix.lower() in {".txt", ".md"}
    and ".venv" not in p.parts
    and ".venv-old" not in p.parts
    and ".git" not in p.parts
    and any(part in {"data", "documents", "synthetic_data"} for part in p.parts)
]

print(f"Found {len(documents)} documents:")
for doc in documents:
    print(" -", doc.relative_to(ROOT))

if not documents:
    raise RuntimeError(
        "No documents found. Check the output of generate_data.py."
    )

# Upload each document individually
for doc in documents:
    print(f"\nUploading: {doc.name}")

    try:
        result = client.context.ingest(
            database=DATABASE,
            collection=COLLECTION,
            documents=[(doc.name, doc.read_bytes())],
            type="knowledge",
        )
        print(result.model_dump_json(indent=2))

    except Exception as e:
        print(f"FAILED: {doc.name}: {type(e).__name__}: {e}")
        raise

print("\nUpload requests completed.")
print("Check indexing status before searching.")
