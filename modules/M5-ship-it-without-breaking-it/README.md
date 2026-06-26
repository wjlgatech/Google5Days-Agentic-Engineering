# M5 — Ship It Without Breaking It (Prototype → Production)

> The fifth and final module — the one the whole hub points at. Day 5: *"Building an agent is
> easy. Trusting it is hard."* ~80% of the work is the **last mile** — the infrastructure,
> security, and validation that make an agent safe to release. The core rule is
> **evaluation-gated deployment**: no version reaches users without passing a comprehensive
> evaluation. Conforms to [`schemas/module.schema.json`](../../schemas/module.schema.json);
> gated by [`scripts/check.sh`](../../scripts/check.sh) (O4/O10).

**Loop stage owned:** ⑧ Learn → ⑨ Decide (→ loop) &nbsp;·&nbsp; **Source:** Day 5 (Prototype → Production / AgentOps).

**What you can do after this module:** wire an evaluation gate into a release pipeline, roll out
safely with a canary, reserve the prod sign-off for a human, and close the loop —
**Observe → Act → Evolve** — so production failures become permanent tests.

## Plug in at your level

| You are… | Start here |
|---|---|
| 🧒 ~15, curious | [`15-explorer.md`](15-explorer.md) |
| 🛠️ ~20, junior engineer | [`20-junior.md`](20-junior.md) |
| 🏗️ ~30, senior engineer | [`30-senior.md`](30-senior.md) |
| 🎯 ~40, AI director | [`40-director.md`](40-director.md) |
| 💼 ~50, EVP / executive | [`50-executive.md`](50-executive.md) |

## The artifact

[`exercise/deploy_gate.py`](exercise/) — a real, zero-dependency **evaluation-gated deploy
pipeline** that **imports M4's evaluator** and makes it the gate: a candidate is `BLOCKED` unless
every eval case passes, then a `canary` must stay healthy, then a human signs off (`PROMOTED` /
`HELD_FOR_SIGNOFF` / `ROLLED_BACK`). It also `evolve()`s a production failure into a new golden
case. Run `python3 deploy_gate.py --selftest`.

## The mental model — this closes the hub's loop

```
 candidate ─▶ ① GATE (M4 eval: every case must pass)  ──fail──▶ BLOCKED (never ships)
                 │ pass
                 ▼
             ② CANARY (1% traffic, still healthy?)     ──fail──▶ ROLLED_BACK
                 │ healthy
                 ▼
             ③ HUMAN SIGN-OFF (prod is a human call)   ──none──▶ HELD_FOR_SIGNOFF
                 │ approved
                 ▼  PROMOTED  ──▶  ④ OBSERVE → ACT → EVOLVE
                                     (a prod failure becomes a new eval case ↩ back to ①)
```

That last arrow is the whole point of the hub: **Intent → Plan → Spec → Execute → Validate →
Evaluate → Diagnose → Learn → Decide → (loop)**. M5 is where Learn/Decide feed back into the
next Intent. It builds *on top of* M4 (evaluation) — deployment is the last mile, not a new brain.

Prereq: [M4 · Is Your Agent Any Good?](../M4-is-your-agent-any-good/). After M5 you've walked all
five Google whitepaper days end-to-end — now run the [loop](../../loop/README.md) on something
real.
