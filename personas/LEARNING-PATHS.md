# Learning Paths — the whole journey, M1 → M5, for who you are

> The capstone map. The five modules aren't five topics — they're **one loop**, learned in
> order: build the loop (M1) → give it hands (M2) → give it memory (M3) → prove it's good (M4)
> → ship it safely (M5). This doc walks that arc *for each persona*, names the artifact you build
> at every step, and ends each path with an **integrative capstone** and a **measurable
> "graduated when."** Make learning executable (Design Principle #2): you're done when something
> *runs and passes*, not when you've read enough.

The shared spine (everyone climbs the same ladder, at their own altitude):

| Step | Module | The one-line outcome | Runnable artifact |
|---|---|---|---|
| 1 | **M1 · Your First Agent Loop** | an agent is "a loop with tools" — run one | `agent_loop.py` |
| 2 | **M2 · Give Your Agent Hands** | a tool = a function **+ a contract** | `tool_registry.py` |
| 3 | **M3 · Give Your Agent Memory** | sessions (now) + memory (across time) | `context_manager.py` |
| 4 | **M4 · Is Your Agent Any Good?** | grade the **trajectory**, not the answer | `trajectory_eval.py` |
| 5 | **M5 · Ship It Without Breaking It** | **evaluation-gated** deployment | `deploy_gate.py` |

These compose for real: [`scripts/e2e.py`](../scripts/e2e.py) runs a live M1 agent → evaluates it
with M4 → gates it with M5. The journey ends where it began — back at **Intent** — because the
whole thing is the [closed loop](../loop/README.md): *Intent → Plan → Spec → Execute → Validate →
Evaluate → Diagnose → Learn → Decide → (repeat)*.

---

## 🧒 15 — Explorer · *"From my first agent to my first shipped thing"*

You learn by **making**. Every step is a 10-minute win you can show a friend.

| Step | Do this | You walk away able to… |
|---|---|---|
| M1 | [Run a real agent](../modules/M1-your-first-agent-loop/15-explorer.md) & add a tool | explain what an agent *is* and run one |
| M2 | [Give it hands](../modules/M2-give-your-agent-hands/15-explorer.md) — tools that fail *helpfully* | build a tool with a "what to do if you use me wrong" label |
| M3 | [Give it memory](../modules/M3-give-your-agent-memory/15-explorer.md) — remember your name | make an agent that remembers you, without "context rot" |
| M4 | [Judge it](../modules/M4-is-your-agent-any-good/15-explorer.md) — lucky vs. good | tell a *lucky* answer from a *good* one by reading the path |
| M5 | [Ship it](../modules/M5-ship-it-without-breaking-it/15-explorer.md) — the robot bouncer | block a broken version before anyone sees it |

**🏆 Capstone — build a "Study Buddy" agent:** a little agent that quizzes you. Give it 2 tools
(M2), make it remember which topics you missed (M3), grade one of its runs (M4), and push it past
the deploy gate (M5).
**Graduated when:** your agent runs, its self-test is all ✓, *and* you can explain the loop —
"read the mission, pick a tool, act, check, repeat" — to a friend in one breath.

---

## 🛠️ 20 — Junior Engineer · *"Ship a small agent, end-to-end, with proof"*

You treat the agent as a system to engineer, debug, and test.

| Step | Do this | You walk away able to… |
|---|---|---|
| M1 | [Read & debug the loop](../modules/M1-your-first-agent-loop/20-junior.md) via its trajectory | root-cause an agent by reading the trajectory |
| M2 | [Write task-shaped tools](../modules/M2-give-your-agent-hands/20-junior.md) with the 8-field contract | ship tools with validation + recovery-teaching errors |
| M3 | [Plumb session + memory](../modules/M3-give-your-agent-memory/20-junior.md) | manage state without blowing the context budget |
| M4 | [Build evals](../modules/M4-is-your-agent-any-good/20-junior.md) — trajectory + Four Pillars | catch judgment failures unit tests miss; make golden cases |
| M5 | [Gate the release](../modules/M5-ship-it-without-breaking-it/20-junior.md) in CI | block a bad version at the eval gate |

**🏆 Capstone — a task agent in CI:** loop + 2 contracted tools + session/memory + an eval suite +
a deploy gate, wired so a red suite blocks the merge. Capture a real M1 trajectory and feed it
through M4→M5 (mirror [`scripts/e2e.py`](../scripts/e2e.py)).
**Graduated when:** your e2e passes, you have ≥1 golden regression case, and you can *demo* a bad
change being blocked at the gate.

---

## 🏗️ 30 — Senior Engineer · *"Architect a reliable, reusable agent platform"*

You design the boundaries: a hard, testable shell around a soft, probabilistic core.

| Step | Do this | You walk away able to… |
|---|---|---|
| M1 | [See the loop as architecture](../modules/M1-your-first-agent-loop/30-senior.md) | place the deterministic/probabilistic seam; bound the planner |
| M2 | [Design the tool boundary](../modules/M2-give-your-agent-hands/30-senior.md) — allow-list, idempotency | make the tool layer the deterministic security seam |
| M3 | [Design state](../modules/M3-give-your-agent-memory/30-senior.md) — isolation, async curation | put curation off the hot path; isolate per-user memory |
| M4 | [Make quality architectural](../modules/M4-is-your-agent-any-good/30-senior.md) | instrument evaluable-by-design; hybrid judge + human |
| M5 | [Architect AgentOps](../modules/M5-ship-it-without-breaking-it/30-senior.md) | eval-gated funnel, safe rollout, externalized state |

**🏆 Capstone — a reference agent + pipeline:** a bounded loop (terminates, only calls
allow-listed idempotent tools), externalized state with per-user isolation, trajectory evals, and
an evaluation-gated pipeline with an Observe→Act→Evolve hook.
**Graduated when:** every deterministic part is unit-tested, the planner's blast radius is bounded,
idempotency + isolation are proven, and the pipeline refuses to ship a version that fails eval.

---

## 🎯 40 — AI Director · *"Stand up an AI-native function that ships reliably"*

You build the operating model *around* the loop — the 95%-vs-5% difference.

| Step | Do this | You produce… |
|---|---|---|
| M1 | [Shared model + vocabulary](../modules/M1-your-first-agent-loop/40-director.md) | an AgentOps readiness scorecard (Level 0–4, eval gate, HITL) |
| M2 | [Govern tools](../modules/M2-give-your-agent-hands/40-director.md) as owned assets | a tool-governance standard (contract + owner + risk class) |
| M3 | [Govern memory/context](../modules/M3-give-your-agent-memory/40-director.md) as data | a memory-governance standard (isolation, provenance, retention) |
| M4 | [Make evaluation the discipline](../modules/M4-is-your-agent-any-good/40-director.md) | an evaluation standard (Four-Pillar targets, golden-set owner) |
| M5 | [Operationalize the last mile](../modules/M5-ship-it-without-breaking-it/40-director.md) | an AgentOps operating standard (gate, rollout, observability) |

**🏆 Capstone — an AgentOps readiness package** for one real initiative: its Level 0–4 placement
plus the four standards above, each with a **named owner** and a CI-runnable eval gate.
**Graduated when:** all five artifacts have owners, the eval gate actually runs in CI, and you can
say — with evidence — the desired outcome, the success metric, and the next action (no activity
mistaken for progress).

---

## 💼 50 — EVP / Executive · *"Fund capability that compounds, not demos that rot"*

You decide what to fund, and what controls are non-negotiable.

| Step | Do this | You produce… |
|---|---|---|
| M1 | [Strategic mental model](../modules/M1-your-first-agent-loop/50-executive.md) | the 3 questions that separate capability from theater |
| M2 | [Why tools are the moat](../modules/M2-give-your-agent-hands/50-executive.md) | a funding gate: no irreversible action without a tool contract + HITL |
| M3 | [Why memory is value + liability](../modules/M3-give-your-agent-memory/50-executive.md) | a funding gate: no remembering people without isolation + retention |
| M4 | [Why evaluation = trust](../modules/M4-is-your-agent-any-good/50-executive.md) | a trust gate: no material decisions without continuous evaluation |
| M5 | [Why the last mile is the value](../modules/M5-ship-it-without-breaking-it/50-executive.md) | a production gate: no customer exposure without gate + rollout + sign-off |

**🏆 Capstone — a one-page investment + governance thesis** for one initiative: the business metric
it moves, its deterministic success gate, its HITL control, its memory/retention policy, its
last-mile budget, and its failure→fix SLA.
**Graduated when:** **Finance and Risk would both sign it** — value and control are explicit, not
hand-waved.

---

## After the capstone — the loop never ends

Finishing M5 doesn't close the book; it returns you to **Intent** with a sharper plan. That's the
compounding North Star: *turn purpose into action, action into evidence, and evidence into wiser
next decisions.* Record what you learned in [`memory/`](../memory/), pick the next mission, and run
the [loop](../loop/README.md) again — harder.

> **One honest line, for every persona:** a green [`check.sh`](../scripts/check.sh) proves your work
> is *structurally complete*. Whether it's actually **good** — clear, wise, worth trusting — is a
> human's call. That judgment is the most valuable skill on this whole map. It stays yours.
