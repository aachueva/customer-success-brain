import os
from pathlib import Path
from dotenv import load_dotenv
from hydra_db import HydraDB

load_dotenv(Path(__file__).parent / ".env")

client = HydraDB(
    token=os.environ["HYDRA_DB_API_KEY"]
)

print("Connecting to HydraDB...")

try:
    result = client.databases.list()
    print("Connection successful!")
    print(result.model_dump_json(indent=2))
except Exception as e:
    print("Connection failed:", type(e).__name__, str(e))