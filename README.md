# FastAPI + OpenAI LLM API Demo

Small demo service: sends a question to an OpenAI model and returns a structured JSON response.
Think of the LLM as a warehouse assistant: you send a note, it walks the aisles, fills the basket, and comes back with an answer — plus a receipt.

## What it does
- `POST /ask` → sends your question to an LLM
- returns:
  - model
  - usage (tokens)
  - latency_ms
- logs request/response metadata in the server console

- ## Architecture
Client → FastAPI → OpenAI API → JSON response
The service acts as a thin backend layer that validates input,
forwards requests to an LLM, and returns structured responses
with usage and latency metrics.

## Requirements
- Python 3.10+ (works on 3.14 too)

## Setup

### 1) Create venv
```bash
python -m venv .venv
source .venv/bin/activate

2) Install deps
pip install -r requirements.txt

3) Set API key (env)
export OPENAI_API_KEY="YOUR_API_KEY"

Run

python -m uvicorn main:app --reload --port 8001

Open Swagger UI:
 • http://127.0.0.1:8001/docs

---

### Example request

```md
## Example request

### cURL
```bash
curl -X POST "http://127.0.0.1:8001/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is an LLM?"}'

---

### Example response

```md
## Example response
```json
{
  "answer": "LLM (Large Language Model) is ...",
  "model": "gpt-4.1-nano",
  "usage": {
    "input_tokens": 19,
    "output_tokens": 26,
    "total_tokens": 45
  },
  "latency_ms": 10149
}

Notes
 • Change model in MODEL_NAME inside main.py:
 • gpt-4.1-nano (cheapest)
 • gpt-4.1-mini (better reasoning)
 • --reload auto restarts server on code changes.
 • If you change environment variables, restart the server.

---

### requirements.txt

```txt
fastapi
uvicorn
openai
pydantic


⸻

3) .gitignore

.venv/
__pycache__/
*.pyc
.DS_Store
.idea/
.env


⸻


## Development
This repository follows a standard Git workflow.

