# M1 for the 🏗️ 30-year-old Senior Engineer — Your First Agent Loop

*Goal: see the loop as an architecture you'll own — where reliability, reuse, and the
deterministic/probabilistic boundary actually live.*

## Plain explanation

The loop is a control plane around a non-deterministic core. Your leverage as a senior is
*not* the prompt — it's the **boundaries**: which steps are deterministic (the loop, tool
dispatch, validation) vs. probabilistic (planning). Day 1's framing: you shift from
"bricklayer" (explicit logic) to "director" (instructions + tools + context). The art is
keeping a hard, testable shell around a soft, flexible center.

## Concrete example

In `agent_loop.py` the orchestration (`run`), tool registry (`TOOLS`), and self-test are
deterministic; only `think()` would become probabilistic when you swap in a model. That seam
is deliberate: you can unit-test everything except the planner, and you can constrain the
planner's blast radius (max_steps, allow-listed tools, validated args). This is the
"defense-in-depth" idea (Day 1) at function scope: hardcoded guardrails *around* model judgment.

## Hands-on exercise

```bash
cd exercise && python3 agent_loop.py --selftest
```
Senior moves:
1. **Bound it:** confirm `max_steps` prevents infinite loops; add a test that a pathological
   mission still terminates (Day 4 robustness).
2. **Make a tool idempotent + safe-to-retry** (Day 5) and prove re-running it doesn't
   double-apply side effects.
3. **Extract the loop** into a reusable function signature you'd be happy to put in a shared
   lib — note how `think_fn` is already injected for testability/reuse.

## Real-world use case

Every framework you'll evaluate (ADK, LangGraph, CrewAI, AG2) is this loop plus features
(state stores, tracing, multi-agent routing). Knowing the bare loop lets you judge a framework
by what it adds, avoid lock-in, and decide *when a deterministic workflow beats an agent* —
often the senior call. Multi-agent patterns (Coordinator, Sequential, Iterative-Refinement,
HITL) are compositions of this same loop.

## Failure mode

**Building one all-powerful "super-agent"** instead of a team of specialists (Day 1
anti-pattern) — and **context overload**: stuffing the window degrades attention ("context
rot", Day 3). The senior failure is architectural: no seam between deterministic and
probabilistic, so nothing is testable and everything is brittle.

## Measurable output

```bash
python3 agent_loop.py --selftest    # + your termination & idempotency tests green
```
**Done when:** the loop is extracted/reusable, every deterministic part is unit-tested, the
planner's blast radius is bounded, and you can state the one invariant that must always hold
(it terminates and never calls an unlisted tool).

## Next step

- Formalize the tool boundary → **M2 (Agent Tools / MCP)**: task-shaped tools + the 8-field
  contract ([`tools/spec-to-green`](../../tools/spec-to-green/) is the worked example).
- Add real state → **M3 (Context Engineering)**: sessions vs. memory, async off the hot path.
- Adopt the habit org-wide: spec + deterministic check before code (Day 5 evaluation gate).
