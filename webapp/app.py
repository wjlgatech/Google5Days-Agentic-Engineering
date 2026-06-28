"""
Agentic landing-page backend for the Agentic Engineering Hub.

The hub's index.html runs a rule-based router in the browser by default. When this
backend is reachable (set `window.AGENT_BACKEND` on the page), the router upgrades to
a real Claude model: it reads the visitor's level + goal and returns which module to
start with, a one-line reason, and a short greeting.

Run:
    python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...      # see .env.example
    .venv/bin/python app.py                  # serves on :8000

Then on the page (e.g. in the browser console, or a deploy-time inline script):
    window.AGENT_BACKEND = "http://localhost:8000"
"""
import json
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Agentic Engineering Hub — guide agent")

# The static page may be served from file:// or GitHub Pages, so allow any origin.
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["POST", "GET"], allow_headers=["*"]
)

MODEL = "claude-opus-4-8"  # latest/most-capable; do not downgrade silently
MODULES = {
    "M1": "Your First Agent Loop (model + tools + orchestration, in a loop)",
    "M2": "Give Your Agent Hands (tools with contracts, MCP)",
    "M3": "Give Your Agent Memory (context engineering: sessions + memory)",
    "M4": "Is Your Agent Any Good? (evaluate the trajectory, not just the answer)",
    "M5": "Ship It Without Breaking It (evaluation-gated deploy, AgentOps)",
}
# Structured output: the model must return exactly this shape, so the page can route on it.
SCHEMA = {
    "type": "object",
    "properties": {
        "module": {"type": "string", "enum": list(MODULES)},
        "reason": {"type": "string"},
        "greeting": {"type": "string"},
    },
    "required": ["module", "reason", "greeting"],
    "additionalProperties": False,
}


class Ask(BaseModel):
    level: str
    goal: str = ""


@app.get("/api/health")
def health():
    return {"status": "ok", "model": MODEL, "llm": bool(os.environ.get("ANTHROPIC_API_KEY"))}


@app.post("/api/agent")
def agent(ask: Ask):
    # No key configured → 503 so the page falls back to its in-browser router.
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return JSONResponse(
            {"error": "ANTHROPIC_API_KEY not set; using client-side routing"}, status_code=503
        )

    import anthropic  # imported lazily so the app starts even without the SDK installed

    client = anthropic.Anthropic()
    catalog = "\n".join(f"  {k}: {v}" for k, v in MODULES.items())
    resp = client.messages.create(
        model=MODEL,
        max_tokens=512,
        system=(
            "You are the guide for the Agentic Engineering Hub, a 5-module course. "
            "Given a learner's level and goal, pick the single best module to start with "
            "and write a one-sentence reason and a short, warm greeting pitched to their level.\n"
            f"Modules:\n{catalog}"
        ),
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
        messages=[{"role": "user", "content": f"Level: {ask.level}\nGoal: {ask.goal or '(none given)'}"}],
    )
    text = next((b.text for b in resp.content if b.type == "text"), "{}")
    return json.loads(text)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
