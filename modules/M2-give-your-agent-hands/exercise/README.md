# Exercise — give your agent hands

A real tool registry in ~110 lines, **zero dependencies**. It shows what makes a function a
*tool*: a **contract** + **validation** + **errors that teach recovery** (all Day 2).

```bash
python3 tool_registry.py             # demo: see good calls and teaching-errors
python3 tool_registry.py --selftest  # prove it works (what scripts/check.sh runs)
```

## What to notice
- Each tool is **task-shaped** (`search_orders`, `refund_order`) — not a thin wrapper over a
  giant API (Day 2's #1 rule).
- The registry **validates the call before running it**: unknown tool, missing arg, wrong
  type, unknown param — each returns an `ERROR:` string that says *how to fix it*. That string
  is what a real agent reads to recover.
- `refund_order` is flagged **not idempotent** — a Day 5 idea: some tools are unsafe to blindly
  retry.

## Make it yours
1. **Add a tool** `track_shipment(order_id)` with a contract; add a self-test assertion. Green.
2. **Tighten a contract:** make `amount` reject negatives; return a teaching error; test it.
3. **Wire it to M1:** import this registry into `agent_loop.py` so the planner's actions go
   through `registry.call(...)` — now your agent has *validated* hands.
