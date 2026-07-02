"""
Vercel serverless function: POST /api/agent  (also GET for health).

This is the deployed form of the guide agent. The routing logic lives in `guide.py`
(shared with the local FastAPI `app.py`); this file is just the Vercel HTTP shell + CORS.
"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler

# guide.py sits one directory up (webapp/), outside api/.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from guide import NoBackend, active_providers, route  # noqa: E402


class handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_OPTIONS(self):  # CORS preflight
        self._send(204, {})

    def do_GET(self):  # health
        self._send(200, {"status": "ok", "providers": [p["name"] for p in active_providers(os.environ)], "llm": bool(active_providers(os.environ))})

    def do_POST(self):
        n = int(self.headers.get("content-length") or 0)
        try:
            payload = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            payload = {}
        try:
            self._send(200, route(payload.get("level", "20-junior"), payload.get("goal", "")))
        except NoBackend:
            self._send(503, {"error": "no LLM key; using client-side routing"})
        except Exception as e:  # rate limit, upstream error → page falls back client-side
            self._send(502, {"error": type(e).__name__})
