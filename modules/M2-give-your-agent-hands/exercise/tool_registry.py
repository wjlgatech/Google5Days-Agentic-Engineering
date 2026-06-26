#!/usr/bin/env python3
"""
M2 — Give Your Agent Hands  ·  tools with CONTRACTS, in ~110 lines, zero deps.

M1 showed the loop. M2 shows the *hands*: tools. The lesson of Day 2 is that a tool is not
just a function — it's a function **plus a contract** (name, description, typed params, and an
error that teaches recovery). The registry below validates a call against the contract
*before* running it (a deterministic gate), so a wrong call returns a helpful error instead of
crashing or silently doing the wrong thing.

Three Day-2 rules made executable here:
  1. "Publish tasks, not API calls."  -> each tool is one task-shaped action.
  2. Validate inputs against a schema. -> register-time + call-time checks.
  3. Errors must teach recovery.       -> every error string says how to fix the call.

Run it:
    python3 tool_registry.py                # demo a few calls
    python3 tool_registry.py --selftest     # deterministic check used by scripts/check.sh
"""
from __future__ import annotations
import sys, json

# ---- A tool = a callable + a CONTRACT. The contract is the Day-2 8-field idea, shrunk to
#      what a runtime needs to validate a call. (The full 8-field human contract lives in the
#      module's persona docs and tools/spec-to-green/contract.json.) ----

class Tool:
    def __init__(self, name, description, params, fn, *, idempotent=True):
        # params: {param_name: {"type": "str|int|float|bool", "required": bool, "desc": str}}
        self.name, self.description, self.params, self.fn = name, description, params, fn
        self.idempotent = idempotent
    def contract(self) -> dict:
        return {"name": self.name, "description": self.description,
                "params": self.params, "idempotent": self.idempotent}

_TYPES = {"str": str, "int": int, "float": (int, float), "bool": bool}

class Registry:
    """Holds tools and validates every call against the tool's contract before dispatch."""
    def __init__(self): self._tools: dict[str, Tool] = {}
    def register(self, tool: Tool):
        # Register-time validation: a tool with a sloppy contract never enters the system.
        if not tool.name or " " in tool.name:
            raise ValueError("tool name must be non-empty and space-free (Day 2: specific names)")
        if not tool.description:
            raise ValueError(f"tool '{tool.name}' needs a description (the LLM reads it to choose)")
        for pn, spec in tool.params.items():
            if spec.get("type") not in _TYPES:
                raise ValueError(f"tool '{tool.name}' param '{pn}' has bad type {spec.get('type')!r}")
        self._tools[tool.name] = tool
    def list(self) -> list[str]: return sorted(self._tools)
    def call(self, name: str, args: dict) -> str:
        # Call-time validation -> errors that TEACH RECOVERY (Day 2), never a raw crash.
        t = self._tools.get(name)
        if t is None:
            return f"ERROR: no tool named '{name}'. Available: {self.list()}. Call one of these."
        for pn, spec in t.params.items():
            if spec.get("required") and pn not in args:
                return (f"ERROR: tool '{name}' is missing required arg '{pn}' ({spec.get('desc','')}). "
                        f"Retry as {name}({pn}=...).")
        for pn, val in args.items():
            if pn not in t.params:
                return f"ERROR: tool '{name}' has no param '{pn}'. Valid params: {list(t.params)}."
            want = t.params[pn]["type"]
            if not isinstance(val, _TYPES[want]) or (want != "bool" and isinstance(val, bool)):
                return (f"ERROR: arg '{pn}' for '{name}' must be {want}, got {type(val).__name__}. "
                        f"Convert it and retry.")
        try:
            return t.fn(**args)
        except Exception as e:                       # robustness (Day 4): tools fail safely
            return f"ERROR: tool '{name}' raised {type(e).__name__}: {e}. Check the inputs and retry."

# ---- Two task-shaped tools (not thin API wrappers). ----

def _search_orders(query: str) -> str:
    db = {"shoes": "order #A12 (shipped)", "hat": "order #B7 (processing)"}
    return db.get(query.lower(), f"no orders match '{query}'")

def _refund(order_id: str, amount: float) -> str:
    return f"refunded ${amount:.2f} on {order_id}"

def build_registry() -> Registry:
    r = Registry()
    r.register(Tool("search_orders", "Find a customer's order by keyword.",
                    {"query": {"type": "str", "required": True, "desc": "keyword like 'shoes'"}},
                    _search_orders))
    r.register(Tool("refund_order", "Issue a refund for a specific order.",
                    {"order_id": {"type": "str", "required": True, "desc": "e.g. 'order #A12'"},
                     "amount":   {"type": "float", "required": True, "desc": "dollars to refund"}},
                    _refund, idempotent=False))   # refunds are NOT safe to blindly retry (Day 5)
    return r

# ---- Self-test = the measurable output (Day 4). scripts/check.sh runs this. ----

def selftest() -> int:
    r = build_registry()
    checks = {
        "valid call works":        r.call("search_orders", {"query": "shoes"}) == "order #A12 (shipped)",
        "unknown tool teaches":    r.call("nope", {}).startswith("ERROR") and "Available" in r.call("nope", {}),
        "missing arg teaches":     "missing required arg 'query'" in r.call("search_orders", {}),
        "wrong type teaches":      "must be float" in r.call("refund_order", {"order_id": "x", "amount": "ten"}),
        "unknown param teaches":   "no param 'qty'" in r.call("search_orders", {"query": "shoes", "qty": 3}),
        "contracts complete":      all(t and r._tools[t].description and r._tools[t].params for t in r.list()),
        "refund flagged non-idem": r._tools["refund_order"].idempotent is False,
        "bad registration caught": _expect_register_error(),
    }
    print("--- self-test ---")
    for name, ok in checks.items():
        print(f"  {'✓' if ok else '✗'} {name}")
    return 0 if all(checks.values()) else 1

def _expect_register_error() -> bool:
    try:
        Registry().register(Tool("bad name", "x", {}, lambda: "x")); return False
    except ValueError:
        return True

def _demo():
    r = build_registry()
    for name, args in [("search_orders", {"query": "shoes"}),
                       ("search_orders", {}),                       # missing arg -> teaching error
                       ("refund_order", {"order_id": "order #A12", "amount": 19.99})]:
        print(f"call {name}({args}) -> {r.call(name, args)}")
    print("\ncontracts:", json.dumps([r._tools[t].contract() for t in r.list()], indent=2))

if __name__ == "__main__":
    sys.exit(selftest()) if "--selftest" in sys.argv else _demo()
