# Customer Success Brain

Hackathon MVP: evidence-grounded RAG assistant and transparent production-readiness dashboard for a synthetic healthcare customer.

## Setup (macOS)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env if you want LLM synthesis
python generate_data.py
python -m unittest discover -s tests -v
streamlit run app.py
```

The first retrieval run may download Chroma's local embedding model. Internet is needed for installation, first-time model download, and OpenAI API requests.

## Demo questions
1. Is Acme ready for production? What are the blockers and next steps?
2. Why does the older green status conflict with the latest evaluation?
3. What must Ravi, Dr. Kim, and Maya do before the go/no-go review?
4. Could we launch a restricted internal pilot instead?

## Safety and scope
All customer data is synthetic. Readiness scorecard is rule-based, not an AI-generated numeric score. The model is instructed to cite supplied evidence, but citations should still be manually checked. No real PHI or production systems are used.
