# Agentic landing-page backend (optional LLM upgrade)

The hub's landing page (`../index.html`) is **agentic on its own**: a persona-router loop and
a live M1 agent loop both run client-side, with zero dependencies, and work offline. This
backend is the **optional upgrade** in the hybrid design — when it's reachable, the router
swaps its in-browser keyword matching for a real Claude model.

## What it is

A small FastAPI service with one real endpoint, `POST /api/agent`. It takes the visitor's
`level` and `goal` and returns `{module, reason, greeting}` using `claude-opus-4-8` with a
JSON-schema structured output (so the page can route on the result deterministically). With no
`ANTHROPIC_API_KEY` set it returns `503`, and the page falls back to client-side routing — so
the site never breaks if the backend is absent or unconfigured.

## Run

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env          # then put your key in .env, or just export it:
export ANTHROPIC_API_KEY=sk-ant-...
.venv/bin/python app.py        # serves on http://localhost:8000
```

Check it: `curl localhost:8000/api/health` → `{"status":"ok","model":"claude-opus-4-8","llm":true}`.

## Wire it to the page

The page calls the backend only if `window.AGENT_BACKEND` is set. For local testing, open the
hub and run in the browser console:

```js
window.AGENT_BACKEND = "http://localhost:8000"
```

For a real deploy, host this service, set `ANTHROPIC_API_KEY` there, and add one line to
`index.html` before the main `<script>`:

```html
<script>window.AGENT_BACKEND = "https://your-host";</script>
```

If the host is down or the key is missing, the router silently uses its offline loop — the
landing page keeps working either way.
