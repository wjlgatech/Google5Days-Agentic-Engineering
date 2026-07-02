"""
Shared routing core for the hub's guide agent — with a FREE-LLM FALLBACK CHAIN.

The "Lengthen" 10X move: one free provider is fragile (a 429 kills the LLM path). This tries an
ordered chain of OpenAI-compatible free providers and uses the first one whose key is configured,
falling through on any error. The last rung of the chain is the page's own in-browser router
(guaranteed, offline). Order is for correctness/availability, per the free-llm playbook:

    Gemini (free, no card) → Groq (fast) → NVIDIA NIM (frontier variety) → OpenRouter (paid) → <page router>

Set any of GEMINI_API_KEY / GROQ_API_KEY / NVIDIA_API_KEY / OPENROUTER_API_KEY. Both `app.py`
(local FastAPI) and `api/agent.py` (Vercel function) import `route()` from here.
"""
import json
import os
import urllib.request

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

# Ordered fallback chain. json_mode: how to force structured output on that provider's API.
PROVIDERS = [
    {"name": "gemini",     "key_env": "GEMINI_API_KEY",     "model": "gemini-2.5-flash-lite",
     "base_url": "https://generativelanguage.googleapis.com/v1beta/openai", "json_mode": "schema"},
    {"name": "groq",       "key_env": "GROQ_API_KEY",       "model": "llama-3.3-70b-versatile",
     "base_url": "https://api.groq.com/openai/v1", "json_mode": "object"},
    {"name": "nvidia",     "key_env": "NVIDIA_API_KEY",     "model": "z-ai/glm-5.1",
     "base_url": "https://integrate.api.nvidia.com/v1", "json_mode": "object"},
    {"name": "openrouter", "key_env": "OPENROUTER_API_KEY", "model": "meta-llama/llama-3.3-70b-instruct",
     "base_url": "https://openrouter.ai/api/v1", "json_mode": "object"},
]


class NoBackend(Exception):
    """No provider key configured — caller returns 503 so the page routes client-side."""


def active_providers(env) -> list:
    """Pure: the configured providers, in fallback order. Unit-tested; no network."""
    return [p for p in PROVIDERS if env.get(p["key_env"])]


def _messages(level: str, goal: str) -> list:
    catalog = "\n".join(f"{k}: {v}" for k, v in MODULES.items())
    return [
        {"role": "system", "content": (
            "You are the guide for the Agentic Engineering Hub, a 5-module course. Pick the single "
            "best module to start from for this learner and write a one-sentence reason plus a short, "
            "warm greeting pitched to their level. Reply with ONLY a JSON object with keys "
            "module (one of M1..M5), reason, greeting.\nModules:\n" + catalog)},
        {"role": "user", "content": f"Level: {level}\nGoal: {goal or '(none given)'}"},
    ]


def _response_format(json_mode: str):
    if json_mode == "schema":
        return {"type": "json_schema", "json_schema": {"name": "route", "schema": SCHEMA}}
    if json_mode == "object":
        return {"type": "json_object"}
    return None


def _parse(text: str) -> dict:
    """Defensive: providers may wrap JSON in prose/code fences."""
    t = text.strip()
    if t.startswith("```"):
        t = t.strip("`")
        t = t[t.find("{"):]
    start, end = t.find("{"), t.rfind("}")
    return json.loads(t[start:end + 1] if start >= 0 and end > start else t)


def _call(provider: dict, key: str, level: str, goal: str) -> dict:
    body = {"model": provider["model"], "max_tokens": 400, "messages": _messages(level, goal)}
    rf = _response_format(provider["json_mode"])
    if rf:
        body["response_format"] = rf
    req = urllib.request.Request(
        provider["base_url"].rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode())
    out = _parse(data["choices"][0]["message"]["content"])
    module = out.get("module") if out.get("module") in MODULES else "M1"
    return {"module": module, "reason": (out.get("reason") or "")[:240],
            "greeting": (out.get("greeting") or "")[:240], "model": provider["model"],
            "provider": provider["name"]}


def route(level: str, goal: str) -> dict:
    actives = active_providers(os.environ)
    if not actives:
        raise NoBackend("no provider key set (GEMINI/GROQ/NVIDIA/OPENROUTER_API_KEY)")
    last = None
    for p in actives:  # fall through the chain on any error
        try:
            return _call(p, os.environ[p["key_env"]], level, goal)
        except Exception as e:  # noqa: BLE001 — try the next rung
            last = e
    raise RuntimeError(f"all {len(actives)} provider(s) failed; last: {type(last).__name__}")
