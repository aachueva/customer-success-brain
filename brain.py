import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
ROOT = Path(__file__).parent
DATA_DIR = ROOT / 'data'
DB_DIR = ROOT / '.chroma'
COLLECTION = 'acme_health_docs'


def files():
    return sorted(DATA_DIR.glob('*.md'))


def index_documents():
    import chromadb
    client = chromadb.PersistentClient(path=str(DB_DIR))
    collection = client.get_or_create_collection(name=COLLECTION, metadata={'hnsw:space': 'cosine'})
    docs, ids, metadata = [], [], []
    for path in files():
        content = path.read_text(encoding='utf-8')
        # Small documents fit as one chunk; split longer documents for future use.
        chunks = [content[i:i+1200] for i in range(0, len(content), 1000)]
        for j, chunk in enumerate(chunks):
            ids.append(f'{path.stem}_{j}')
            docs.append(chunk)
            metadata.append({'source': path.name})
    if docs:
        collection.upsert(ids=ids, documents=docs, metadatas=metadata)
    return len(docs)


def retrieve(question, n=5):
    import chromadb
    client = chromadb.PersistentClient(path=str(DB_DIR))
    collection = client.get_or_create_collection(name=COLLECTION, metadata={'hnsw:space': 'cosine'})
    if collection.count() == 0:
        index_documents()
    result = collection.query(query_texts=[question], n_results=min(n, collection.count()))
    return [{'text': t, 'source': m['source'], 'distance': d}
            for t, m, d in zip(result['documents'][0], result['metadatas'][0], result['distances'][0])]


def readiness():
    # Transparent, deterministic scorecard from the provided synthetic evidence.
    return [
        {'metric': 'PHI protection', 'actual': 'Leak reproduced 2/50 tests', 'target': 'Zero confirmed leaks', 'status': 'BLOCKED', 'source': '03_support_ticket.md'},
        {'metric': 'Answer accuracy', 'actual': '91%', 'target': '>=95%', 'status': 'BLOCKED', 'source': '04_eval_report.md'},
        {'metric': 'Critical escalation', 'actual': '90%', 'target': '100%', 'status': 'BLOCKED', 'source': '04_eval_report.md'},
        {'metric': 'p95 latency', 'actual': '4.2s', 'target': '<3s', 'status': 'AT RISK', 'source': '05_performance.md'},
        {'metric': 'Audit retention sign-off', 'actual': 'Pending', 'target': 'Approved', 'status': 'BLOCKED', 'source': '02_architecture.md'},
    ]


def fallback_answer(question, sources):
    evidence = '\n\n'.join(f"[{s['source']}] {s['text'].strip()}" for s in sources)
    return ('**Offline evidence mode** — no API key is configured. These are retrieved excerpts, not an AI-generated assessment.\n\n'
            + evidence + '\n\n**Suggested next step:** Review the scorecard and assign owners to unresolved blockers.')


def answer(question, sources):
    key = os.getenv('OPENAI_API_KEY', '').strip()
    if not key:
        return fallback_answer(question, sources)
    from openai import OpenAI
    context = '\n\n'.join(f"SOURCE: {s['source']}\n{s['text']}" for s in sources)
    instructions = ("You are an enterprise Customer Success Brain. Answer ONLY using supplied evidence. "
                    "Cite source filenames in square brackets for every material claim. "
                    "Prioritize the latest dated and approved evaluations over older reports. "
                    "Distinguish blockers from risks and proposed mitigations from completed fixes. "
                    "Never invent owners, dates, numbers, or production approvals. "
                    "If evidence is missing, say what is unknown. Provide actionable next steps.")
    response = OpenAI(api_key=key).responses.create(
        model=os.getenv('OPENAI_MODEL', 'gpt-4.1-mini'),
        instructions=instructions,
        input=f'QUESTION:\n{question}\n\nEVIDENCE:\n{context}',
    )
    return response.output_text
