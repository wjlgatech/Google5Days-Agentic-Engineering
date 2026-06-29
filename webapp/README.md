# Guide-agent backend (deployed)

The hub's landing page (`../index.html`) is **agentic on its own** — a persona-router loop and a
live M1 loop run client-side, offline, zero deps. This backend is the **live upgrade**: when it's
reachable, the router calls a real LLM instead of in-browser keyword matching.

**Live:** `https://webapp-nu-hazel.vercel.app/api/agent` — already wired into the page via
`window.AGENT_BACKEND`.

## How it works

- **Free LLM, no paid key.** Uses Google **Gemini's free tier** (`gemini-2.5-flash-lite`) through
  its OpenAI-compatible endpoint — the `free-llm` playbook. No card, ~1,500 req/day. The browser
  calls *this backend*, which calls Gemini **server-to-server**, so Gemini's no-CORS rule never
  applies, and the rate-limited-but-free tier means an abused public endpoint just 429s (no bill).
- **Graceful fallback chain.** `Gemini (free cloud) → client-side rule-based router (offline)`.
  If the key is missing the function returns 503; any upstream/rate error returns 502; either way
  the page silently falls back to its in-browser router, so the site never breaks.
- **Shared core.** Routing logic lives in `guide.py` (stdlib only — `urllib`, JSON-schema
  structured output). Two thin shells import it: `api/agent.py` (Vercel function) and `app.py`
  (local FastAPI).

## Endpoints

- `POST /api/agent` `{level, goal}` → `{module, reason, greeting, model}`
- `GET  /api/agent` → health `{status, model, llm}`

## Run locally

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
export GEMINI_API_KEY=AIza...        # free: https://aistudio.google.com/apikey
.venv/bin/python app.py               # http://localhost:8000
# then in the page console: window.AGENT_BACKEND = "http://localhost:8000"
```

## Redeploy (Vercel)

```bash
vercel deploy --prod --yes --scope <your-scope> -e GEMINI_API_KEY="$GEMINI_API_KEY"
```

Swap the LLM by editing `MODEL`/`ENDPOINT` in `guide.py` — any OpenAI-compatible free provider
(NVIDIA NIM, Groq, …) works; see the `free-llm` skill for verified ids and the fallback chain.
