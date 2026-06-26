# M1 — Your First Agent Loop

> **The reference module of this hub.** It is the worked example of mission Pillar 1 (a
> plug-and-play, persona-adaptive learning module) and the template every future module
> copies. Machine spec: it conforms to
> [`schemas/module.schema.json`](../../schemas/module.schema.json); structural completeness
> is enforced by [`scripts/check.sh`](../../scripts/check.sh) (objective O4).

**Loop stage owned:** ① Intent → ④ Execute &nbsp;·&nbsp; **Source:** Day 1 (the 5-step loop).

**What you can do after this module:** explain what an agent *is*, run one, read its
trajectory, and add a tool — at your level.

---

## Plug in at your level

The *same idea* (an agent is a loop with tools), reframed for who you are and what you're
responsible for. Each file is self-contained and has the **7 required parts** (plain
explanation · concrete example · hands-on exercise · real-world use case · failure mode ·
measurable output · next step).

| You are… | Start here | The version optimizes for… |
|---|---|---|
| 🧒 ~15, curious | [`15-explorer.md`](15-explorer.md) | confidence, fun, a visible win in 10 minutes |
| 🛠️ ~20, junior engineer | [`20-junior.md`](20-junior.md) | workflow, debugging, shipping the loop |
| 🏗️ ~30, senior engineer | [`30-senior.md`](30-senior.md) | architecture, reliability, reuse |
| 🎯 ~40, AI director | [`40-director.md`](40-director.md) | operating model, risk, evaluation |
| 💼 ~50, EVP / executive | [`50-executive.md`](50-executive.md) | ROI, governance, capability strategy |

Not sure? Start one level **below** where you think you are — the win is faster and the depth
is still there. (Day 1 progressive complexity / Levels 0–4.)

## The artifact (shared by all personas)

[`exercise/agent_loop.py`](exercise/) — a real, runnable, zero-dependency agent. Everyone runs
the same code; each persona file frames *why it matters to you* differently.

## The mental model (one diagram, all levels)

```
 ① Get the Mission ─▶ ② Scan ─▶ ③ Think ─▶ ④ Act (use a tool) ─▶ ⑤ Observe
        ▲                                                            │
        └──────────────── loop until the mission is done ◀───────────┘
```

That's it. Everything else in agentic engineering — tools (Day 2), context (Day 3), quality
(Day 4), production (Day 5) — hangs off this loop. See [`../../loop/README.md`](../../loop/README.md).
