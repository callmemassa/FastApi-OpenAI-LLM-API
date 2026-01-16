import time
import logging
from typing import Any, Optional, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

# ---------- logging ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger("api")

# ---- mute noisy HTTP logs from httpx/openai internals ----
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)

# ---------- app ----------
app = FastAPI()

client = OpenAI()

MODEL_NAME = "gpt-4.1-nano"


class AskRequest(BaseModel):
    question: str


def _usage_to_dict(usage_obj: Any) -> Optional[Dict[str, int]]:
    if usage_obj is None:
        return None

    out: Dict[str, int] = {}
    for k in ("input_tokens", "output_tokens", "total_tokens"):
        v = getattr(usage_obj, k, None)
        if isinstance(v, int):
            out[k] = v

    if not out and isinstance(usage_obj, dict):
        for k in ("input_tokens", "output_tokens", "total_tokens"):
            v = usage_obj.get(k)
            if isinstance(v, int):
                out[k] = v

    return out or None


@app.post("/ask")
def ask(req: AskRequest):
    question = (req.question or "").strip()
    if not question:
        raise HTTPException(status_code=400, detail="question is empty")

    t0 = time.perf_counter()
    log.info('REQ /ask | model=%s | question="%s"', MODEL_NAME, question)

    try:
        resp = client.responses.create(
            model=MODEL_NAME,
            input=[
                {"role": "system", "content": "Answer briefly and clearly."},
                {"role": "user", "content": question},
            ],
            max_output_tokens=300,
        )

        latency_ms = int((time.perf_counter() - t0) * 1000)
        answer = (resp.output_text or "").strip()

        usage = _usage_to_dict(getattr(resp, "usage", None))

        log.info(
            "OK  /ask | model=%s | latency_ms=%s | usage=%s",
            MODEL_NAME,
            latency_ms,
            usage,
        )

        return {
            "answer": answer,
            "model": MODEL_NAME,
            "usage": usage,
            "latency_ms": latency_ms
        }

    except Exception as e:
        latency_ms = int((time.perf_counter() - t0) * 1000)
        log.exception(
            "ERR /ask | model=%s | latency_ms=%s | error=%s",
            MODEL_NAME,
            latency_ms,
            str(e),
        )
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"ok": True}