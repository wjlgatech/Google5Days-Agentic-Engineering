#!/usr/bin/env python3
"""
mcp_server.py — expose spec-to-green over MCP (the "Widen" 10X move: new market).

The hub's reusable tool becomes callable by ANY MCP client (Claude Desktop / Code / Cowork, or
another agent) — not just a human reading `contract.json`. Minimal JSON-RPC 2.0 over stdio,
newline-delimited, stdlib only. Wire it into an MCP client with:

    { "mcpServers": { "spec-to-green": { "command": "python3",
        "args": ["tools/spec-to-green/mcp_server.py"] } } }

It implements `initialize`, `tools/list`, and `tools/call` for one tool: `spec_to_green`, which
turns a fuzzy request into a verifiable spec (objective + a deterministic acceptance check +
out-of-scope) — the same discipline `tools/spec-to-green/contract.json` defines.
"""
import json
import re
import sys

TOOL = {
    "name": "spec_to_green",
    "description": "Turn a fuzzy request into a verifiable spec: objective, a deterministic "
                   "acceptance check to drive code to green, and explicit out-of-scope.",
    "inputSchema": {
        "type": "object",
        "properties": {"request": {"type": "string", "description": "The fuzzy ask."}},
        "required": ["request"],
    },
}


def spec_to_green(request: str) -> dict:
    """Deterministic: a fuzzy ask -> a spec with a machine-checkable acceptance test."""
    req = (request or "").strip()
    slug = re.sub(r"[^a-z0-9]+", "_", req.lower()).strip("_")[:40] or "task"
    return {
        "objective": req or "(none given)",
        "acceptance_check": f"pytest -k {slug} -q   # define a test that fails now and drives it green",
        "definition_of_done": "the acceptance_check exits 0 and no existing check regresses",
        "out_of_scope": "anything not required to make the acceptance_check pass",
    }


def handle(msg: dict):
    """Return a JSON-RPC result dict, or None for notifications."""
    mid, method, params = msg.get("id"), msg.get("method"), msg.get("params") or {}
    if method == "initialize":
        result = {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                  "serverInfo": {"name": "spec-to-green", "version": "1.0.0"}}
    elif method == "tools/list":
        result = {"tools": [TOOL]}
    elif method == "tools/call":
        if params.get("name") != "spec_to_green":
            return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": "unknown tool"}}
        spec = spec_to_green((params.get("arguments") or {}).get("request", ""))
        result = {"content": [{"type": "text", "text": json.dumps(spec, indent=2)}]}
    elif mid is None:
        return None  # a notification (e.g. notifications/initialized) — no reply
    else:
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"method not found: {method}"}}
    return {"jsonrpc": "2.0", "id": mid, "result": result}


def main() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        resp = handle(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
