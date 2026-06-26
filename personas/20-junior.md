# 🛠️ The 20-year-old Junior Engineer — your path

**You want:** to be genuinely good at building and shipping with coding agents — not just
prompting them.
**Your edge:** you treat the agent as a system to engineer, debug, and test.

## Your first win
**[M1 · Your First Agent Loop → 20-junior](../modules/M1-your-first-agent-loop/20-junior.md)** —
read, break, and fix a real agent loop by reading its trajectory. That debugging skill is the
whole job.

## The map
1. **M1 — the loop** (read traces, extend tools) ← start here
2. M2 — Agent Tools & the 8-field contract (write tools people reuse)
3. M3 — Context Engineering (sessions vs. memory; don't blow the context window)
4. M4 — Agent Quality (evaluate the trajectory, not just the output)
5. M5 — Prototype → Production (CI gates, safe rollout)

## Your habits (start now)
- **Write the check first, then make it green** — practice with
  [`tools/spec-to-green`](../tools/spec-to-green/).
- **Debug via the trajectory**, never by guessing.
- **Test behavior, not exact strings** (probabilistic systems break brittle assertions).

## Your reusable assets
Every tool you build → give it the 8-field contract. Every bug you fix → add a check so it
can't come back. That's how each unit of work makes the next one easier (compounding).
