# Exercise — ship it without breaking it

A real evaluation-gated deploy pipeline in ~120 lines, **zero dependencies**. It **imports M4's
evaluator** and makes it the gate — the Day-5 rule made literal: no version ships unless it
passes evaluation, a canary, and a human.

```bash
python3 deploy_gate.py             # walk a promoted release, a blocked one, and a rollback
python3 deploy_gate.py --selftest  # prove it works (what scripts/check.sh runs)
```

## What to notice
- **Evaluation-gated:** the BAD release is `BLOCKED_AT_GATE` and never produces a deploy record —
  it cannot reach users. (Day 5: "no agent version should reach users without first passing a
  comprehensive evaluation.")
- **Safe rollout:** a version that passes the gate but fails the **canary** is `ROLLED_BACK`, not
  promoted.
- **Humans own prod:** a healthy candidate without sign-off is `HELD_FOR_SIGNOFF` — the pipeline
  refuses to self-approve production.
- **The deploy record is your undo button:** version + per-case verdicts + rollout strategy
  ("version everything").
- **Observe → Act → Evolve:** `evolve(BAD, ...)` turns a production failure into a golden eval
  case; the grown suite then **blocks** the version that used to pass. The same break can't ship
  twice — that's the compounding loop closing.

## This is the hub eating its own dog food
`deploy_gate.py` does for an *agent* exactly what [`scripts/check.sh`](../../../scripts/check.sh)
does for *this repo*, and what [`tools/spec-to-green`](../../../tools/spec-to-green/) does for *a
task*: gate on a deterministic check, reserve judgment for a human. Same pattern, three layers.

## Make it yours
1. **Tighten the gate:** require `pass_rate >= 0.95` instead of all-pass; test it.
2. **Add a phase:** insert a "staging dogfood" step between gate and canary.
3. **Real evolve loop:** after a `ROLLED_BACK`, auto-`evolve()` the canary failure into the suite
   and re-run the gate — watch the pipeline get stricter on its own.
