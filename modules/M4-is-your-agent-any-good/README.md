# M4 — Is Your Agent Any Good? (Agent Quality)

> The fourth module. M1–M3 built an agent that loops, acts, and remembers. M4 asks the
> production question: **is it any good?** Day 4's answer — *"an agent can pass 100 unit tests
> and still fail catastrophically; its failure is a flaw in judgment, not a bug in the code."*
> So we evaluate the **trajectory**, not just the final answer. Conforms to
> [`schemas/module.schema.json`](../../schemas/module.schema.json); gated by
> [`scripts/check.sh`](../../scripts/check.sh) (O4/O10).

**Loop stage owned:** ⑤ Validate → ⑥ Evaluate → ⑦ Diagnose &nbsp;·&nbsp; **Source:** Day 4 (Agent Quality).

**What you can do after this module:** evaluate an agent run Outside-In (task success, then the
trajectory), score the **Four Pillars**, judge **pairwise**, and — crucially — know which
quality questions a machine must **not** answer (it surfaces them to a human).

## Plug in at your level

| You are… | Start here |
|---|---|
| 🧒 ~15, curious | [`15-explorer.md`](15-explorer.md) |
| 🛠️ ~20, junior engineer | [`20-junior.md`](20-junior.md) |
| 🏗️ ~30, senior engineer | [`30-senior.md`](30-senior.md) |
| 🎯 ~40, AI director | [`40-director.md`](40-director.md) |
| 💼 ~50, EVP / executive | [`50-executive.md`](50-executive.md) |

## The artifact

[`exercise/trajectory_eval.py`](exercise/) — a real, zero-dependency **trajectory evaluator**:
Outside-In scoring (Black-Box task success → Glass-Box trajectory), the **Four Pillars**
(Effectiveness · Efficiency · Robustness · Safety), **pairwise** judging, and a **NEEDS_HUMAN
gate** it never self-answers. Run `python3 trajectory_eval.py --selftest`. It can score the runs
your M1/M2/M3 exercises produce.

## The mental model

```
 a RUN ─▶ ① Black-Box: did the final answer meet the objective?   (task success)
          ② Glass-Box: open the trajectory —
                right tool? valid args? redundant/missing steps? terminated? safe?
          ─▶ FOUR PILLARS  Effectiveness · Efficiency · Robustness · Safety
          ─▶ overall ─▶ verdict (deterministic)   +   NEEDS_HUMAN (the rubric is human's)
```

This *is* the hub's own philosophy applied to agents: deterministic checks where correctness is
objective; a human gate where quality is judgment. The repo's [`scripts/check.sh`](../../scripts/check.sh)
is the same idea applied to *this codebase* — and `tools/spec-to-green` is the tool that writes
such checks.

Prereq: [M3 · Give Your Agent Memory](../M3-give-your-agent-memory/). Next: M5 (Prototype →
Production — ship it without it silently rotting).
