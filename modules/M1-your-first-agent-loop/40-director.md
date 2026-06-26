# M1 for the 🎯 40-year-old AI Director — Your First Agent Loop

*Goal: leave with a shared mental model and vocabulary your whole org can use to scope,
evaluate, and govern agent work — grounded by running the thing once yourself.*

## Plain explanation

Strip the hype: an agent is a **loop with tools, wrapped in operations**. The intelligence is
mostly commoditized; your differentiation is the **operating model around the loop** — tools,
evaluation, observability, and the feedback loop that turns failures into improvements
("AgentOps", Day 1/5). Day 5's headline is the one to internalize: *"Building an agent is easy;
trusting it is hard"* — ~80% of the effort is the last mile, not the model.

## Concrete example

Run the 80-line agent and watch it print its **trajectory**. Now scale that mental image: a
fleet of these, each with tools, identities, and eval gates. The questions that matter aren't
"which model?" but: *Who owns each tool? How do we evaluate the trajectory, not just the
output? What's the human-in-the-loop checkpoint? How fast can we turn a production failure
into a regression test?* (Day 4/5). The toy makes those abstract questions concrete.

## Hands-on exercise

```bash
cd exercise && python3 agent_loop.py --selftest
```
Director's lens (do all three):
1. **Map the levels.** Place a current initiative on Day 1's Levels 0–4 (Reasoning →
   Connected → Strategic → Multi-Agent → Self-Evolving). Most "AI projects" are Level 1–2.
2. **Name the eval gate.** For one initiative, write the single deterministic check that would
   make "done" provable (your version of `--selftest`). If you can't, the scope is too fuzzy.
3. **Define one HITL checkpoint** where a human must approve before an irreversible action.

## Real-world use case

Standing up an AI-native function: you need a reference loop, a tool registry with ownership,
an evaluation harness, observability (logs/traces/metrics), and a feedback loop into a golden
dataset. This module + [`docs/OBJECTIVES.md`](../../docs/OBJECTIVES.md) +
[`loop/README.md`](../../loop/README.md) are a miniature of exactly that operating model —
copyable into your org.

## Failure mode

**Confusing activity with progress** (Design Principle #7) and **"set it and forget it"** (Day
1): shipping demos with no eval gate, no observability, no owner. The result is silent
degradation (200 OK, plausibly-wrong output) and "agent sprawl" — dozens of un-governable
agents. The fix is organizational: evaluation-gated deployment + a registry, from day one.

## Measurable output

A one-page **AgentOps readiness scorecard** for one initiative: (1) its Level 0–4, (2) its
deterministic eval gate, (3) its HITL checkpoint, (4) its observability plan, (5) its
failure→golden-set loop. **Done when** all five have a named owner and the eval gate actually
runs in CI. (`python3 agent_loop.py --selftest` is the smallest possible version of that gate.)

## Next step

- Operationalize evaluation across teams → **M4 (Agent Quality)**: the Four Pillars + the
  Quality Flywheel.
- Plan the last mile → **M5 (Prototype → Production)**: CI/CD funnel, safe rollout, A2A/MCP.
- Govern reuse → adopt the 8-field tool contract org-wide
  ([`schemas/tool.schema.json`](../../schemas/tool.schema.json)).
