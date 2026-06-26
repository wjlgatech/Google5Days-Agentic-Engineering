# M5 for the 🛠️ 20-year-old Junior Engineer — Ship It Without Breaking It

*Goal: build the deployment pipeline real agents need — an evaluation gate in CI, safe rollout,
and a feedback loop that turns prod failures into regression tests.*

## Plain explanation

Day 5's discipline is **AgentOps**: DevOps for autonomous, stateful systems. The non-negotiable
rule is **evaluation-gated deployment** — wire your M4 evals into CI so no version merges/ships
without passing them. Then a **CI/CD funnel** (fast pre-merge checks → staging dogfood → gated
prod), **safe rollout** (canary/feature-flags), and **Observe → Act → Evolve** (every prod
failure becomes a new golden case). Version *everything*: code, prompts, tool schemas, eval sets.

## Concrete example

`deploy_gate.py` imports M4's `evaluate` and uses it as the gate: a candidate whose suite has any
failing case returns `BLOCKED_AT_GATE` with no deploy record — it cannot reach users. A canary
failure → `ROLLED_BACK`. No human sign-off → `HELD_FOR_SIGNOFF`. And `evolve(BAD, ...)` appends a
failure as a golden case so the grown suite blocks the regression next time.

## Hands-on exercise

```bash
cd exercise && python3 deploy_gate.py --selftest
```
Junior reps:
1. **Tighten the gate:** require `pass_rate >= 0.95` instead of all-pass; test it on an isolated
   suite (one rule at a time).
2. **Add a phase:** insert a staging "dogfood" step between gate and canary.
3. **Auto-evolve:** after a `ROLLED_BACK`, `evolve()` the canary failure into the suite and re-run
   the gate — the pipeline gets stricter on its own.

## Real-world use case

This is the Google Cloud Agent Starter Pack shape: PR-check → staging → gated deploy, with eval as
the quality gate and Terraform/IaC for reproducible envs. Your CI job runs the eval suite; a red
suite blocks the merge. Same idea you just built, scaled.

## Failure mode

**Shipping without gates or idempotency.** No eval gate → an agent that worked yesterday silently
breaks today. **Non-idempotent tools** retried → duplicate charges (design tools safe-to-retry). No
monitoring → a weekend cost spike with no cause. No fast evolve loop → a known fix takes six months
and the insight rots. Also: letting the pipeline self-approve prod (keep the human gate).

## Measurable output

```bash
python3 deploy_gate.py --selftest && echo PASS
```
**Done when** your tightened gate + extra phase + auto-evolve all pass, and you can show a broken
version being blocked end-to-end. Commit it.

## Next step

- Put your eval suite in CI for a real project; make a red suite block the merge.
- You've completed all 5 days — now run the full [loop](../../loop/README.md) on a feature and let
  M4+M5 gate it.
