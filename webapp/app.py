"""
Local FastAPI server for the hub's guide agent (the same logic Vercel serves via api/agent.py).

The routing core lives in guide.py and calls a FREE OpenAI-compatible LLM (Gemini's free
tier) — no paid key, no cost; a 429 just makes the landing page fall back to its in-browser
router. See guide.py and webapp/README.md.

Run:
    python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
    export GEMINI_API_KEY=AIza...            # free: aistudio.google.com (see .env.example)
    .venv/bin/python app.py                  # serves on :8000

Then on the page (browser console, or a deploy-time inline script):
    window.AGENT_BACKEND = "http://localhost:8000"
"""
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from guide import NoBackend, active_providers, route

app = FastAPI(title="Agentic Engineering Hub — guide agent")
# The static page may be served from file:// or GitHub Pages, so allow any origin.
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["POST", "GET"], allow_headers=["*"]
)


class Ask(BaseModel):
    level: str
    goal: str = ""


@app.get("/api/health")
def health():
    return {"status": "ok", "providers": [p["name"] for p in active_providers(os.environ)], "llm": bool(active_providers(os.environ))}


@app.post("/api/agent")
def agent(ask: Ask):
    try:
        return route(ask.level, ask.goal)
    except NoBackend:
        return JSONResponse({"error": "no LLM key; using client-side routing"}, status_code=503)
    except Exception as e:  # rate limit / upstream error → page falls back client-side
        return JSONResponse({"error": type(e).__name__}, status_code=502)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
