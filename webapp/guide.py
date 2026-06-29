"""
Shared routing core for the hub's guide agent.

Uses a FREE, OpenAI-compatible LLM (Google Gemini's free tier) instead of a paid key — see
the `free-llm` playbook. The browser calls this server-to-server, so Gemini's no-CORS rule
doesn't apply, and the free tier is rate-limited-but-free: worst case is a 429, which the
landing page treats like any other failure and falls back to its in-browser router. That
deterministic client-side router is the last rung of the fallback chain:

    Gemini (free cloud)  →  client-side rule-based router (offline, always works)

Both `app.py` (local FastAPI) and `api/agent.py` (Vercel function) import `route()` from here.
"""
import json
import os
import urllib.request

ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
MODEL = "gemini-2.5-flash-lite"  # free tier; verified to honor json_schema structured output

MODULES = {
    "M1": "Your First Agent Loop (model + tools + orchestration, in a loop)",
    "M2": "Give Your Agent Hands (tools with contracts, MCP)",
    "M3": "Give Your Agent Memory (context engineering: sessions + memory)",
    "M4": "Is Your Agent Any Good? (evaluate the trajectory, not just the answer)",
    "M5": "Ship It Without Breaking It (evaluation-gated deploy, AgentOps)",
}
SCHEMA = {
    "type": "object",
    "properties": {
        "module": {"type": "string", "enum": list(MODULES)},
        "reason": {"type": "string"},
        "greeting": {"type": "string"},
    },
    "required": ["module", "reason", "greeting"],
}


class NoBackend(Exception):
    """No LLM key configured — caller should return 503 so the page routes client-side."""


def route(level: str, goal: str) -> dict:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise NoBackend("GEMINI_API_KEY not set")
    catalog = "\n".join(f"{k}: {v}" for k, v in MODULES.items())
    body = {
        "model": MODEL,
        "max_tokens": 400,
        "response_format": {"type": "json_schema", "json_schema": {"name": "route", "schema": SCHEMA}},
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are the guide for the Agentic Engineering Hub, a 5-module course. "
                    "Pick the single best module to start from for this learner and write a "
                    "one-sentence reason plus a short, warm greeting pitched to their level.\n"
                    f"Modules:\n{catalog}"
                ),
            },
            {"role": "user", "content": f"Level: {level}\nGoal: {goal or '(none given)'}"},
        ],
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode(),
        method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode())
    out = json.loads(data["choices"][0]["message"]["content"])
    module = out.get("module") if out.get("module") in MODULES else "M1"
    return {
        "module": module,
        "reason": (out.get("reason") or "")[:240],
        "greeting": (out.get("greeting") or "")[:240],
        "model": MODEL,
    }
