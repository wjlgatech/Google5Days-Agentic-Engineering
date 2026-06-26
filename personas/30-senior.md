# 🏗️ The 30-year-old Senior Engineer — your path

**You want:** judgment — when to use an agent vs. a deterministic workflow, how to keep it
reliable, and how to build platform pieces your team reuses.
**Your edge:** you design the boundaries (deterministic shell, probabilistic core).

## Your first win
**[M1 · Your First Agent Loop → 30-senior](../modules/M1-your-first-agent-loop/30-senior.md)** —
see the loop as an architecture: where reliability, reuse, and the testable seam live.

## The map
1. **M1 — the loop as architecture** ← start here
2. M2 — Agent Tools / MCP (task-shaped tools, the contract, interoperability)
3. M3 — Context Engineering (state design: sessions, memory ETL, async off the hot path)
4. M4 — Agent Quality (trajectory eval, LLM-as-judge, the Four Pillars)
5. M5 — Prototype → Production (AgentOps, evaluation-gated CI/CD, A2A)

## Your habits
- Keep a **hard testable shell around a soft model core**; bound the planner's blast radius.
- Make tools **idempotent & safe-to-retry** (Day 5).
- Prefer the **smallest pattern that works** — resist the all-powerful super-agent.

## Your reusable assets
Extract loops, tool contracts, and checks into shared libs. Adopt the hub's deterministic
[`scripts/check.sh`](../scripts/check.sh) pattern as your team's definition of "done".
Contribute new modules/tools back — that's platform thinking.
