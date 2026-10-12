
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from hydra_db import HydraDB

load_dotenv(Path(__file__).parent / ".env", override=True)

client = HydraDB(token=os.environ["HYDRA_DB_API_KEY"])

DATABASE = "default-tenant"
COLLECTION = "customer-success-brain"

for attempt in range(20):
    result = client.context.list(
        database=DATABASE,
        collection=COLLECTION,
        type="knowledge"
    )

    ids = [s.id for s in (result.data.sources or [])]

    status = client.context.status(
        database=DATABASE,
        collection=COLLECTION,
        ids=ids
    )

    statuses = status.data.statuses or []
    counts = {}

    for item in statuses:
        state = item.indexing_status or "unknown"
        counts[state] = counts.get(state, 0) + 1

    print(f"Check {attempt + 1}: {counts}", flush=True)

    if any(item.error_code or item.error_message for item in statuses):
        print("Indexing error detected:")
        for item in statuses:
            if item.error_code or item.error_message:
                print(item.id, item.error_message)
        break

    if len(statuses) == 9 and all(
        item.indexing_status in {"completed", "indexed", "ready"}
        for item in statuses
    ):
        print("All documents indexed!")
        break

    time.sleep(10)
else:
    print("Polling finished. Check status again later.")