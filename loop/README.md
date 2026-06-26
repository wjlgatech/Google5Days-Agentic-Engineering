# The Closed Loop — the hub's operating cycle

> Every meaningful workflow in this hub — learning a module, building a tool, running a
> startup experiment — follows **one** loop. It is the five Google whitepapers expressed as a
> single repeatable cycle. Run it once and you have an artifact; run it again and you have a
> *better* artifact plus a lesson. That second part is the whole point (Design Principle #1:
> compounding capability).

```
        ┌─────────────────────────────────────────────────────────────┐
        │                                                             ▼
   ① Intent ─▶ ② Plan ─▶ ③ Specification ─▶ ④ Execute ─▶ ⑤ Validate
        ▲                                                             │
        │                                                             ▼
   ⑨ Decide ◀─ ⑧ Learn ◀─ ⑦ Diagnose ◀─ ⑥ Evaluate ◀────────────────┘
   Next Step
```

Map to the whitepapers (provenance — [`docs/PRINCIPLES.md`](../docs/PRINCIPLES.md)):

| # | Stage | What you do | Whitepaper that grounds it | Artifact it produces |
|---|---|---|---|---|
| 1 | **Intent** | State the mission + who it's for + what "done" looks like | Day 1 "Get the Mission" | a one-line objective + success metric |
| 2 | **Plan** | Choose model/tools/approach; cast the team | Day 1 "Think It Through" | a plan (sequential vs multi-agent) |
| 3 | **Specification** | Write the contract before code: inputs/outputs/acceptance | Day 2 tool contract | a spec or tool contract (`schemas/`) |
| 4 | **Execute** | Take action — call tools, manage session + memory state | Day 1 "Take Action" + Day 3 context | code / artifact / output |
| 5 | **Validate** | Did the final output meet the objective? (Black-Box) | Day 4 Outside-In, layer 1 | pass/fail on task success |
| 6 | **Evaluate** | Score quality across the Four Pillars; judge the *trajectory* (Glass-Box) | Day 4 trajectory eval | a score + rubric verdict |
| 7 | **Diagnose** | If it failed/scored low — *why*? Which step in the trajectory broke? | Day 4 Glass-Box | a root cause |
| 8 | **Learn** | Persist the lesson: turn the failure into a durable system improvement | Day 4/5 failure→golden-set | a `memory/lessons/L###.json` |
| 9 | **Decide** | Choose the next step; record the decision; re-enter the loop | Day 5 Observe→Act→Evolve | a `memory/decisions/D###.json` |

## Why a loop and not a checklist

A checklist runs once and is thrown away. A loop's **output feeds its own next input** — the
lesson from stage 8 changes the plan in stage 2 next time. That is the difference between
*activity* (Design Principle #7) and *compounding progress*. Day 5 says it best: a known fix
that takes six months to deploy makes the insight worthless — so the loop must be *fast* and
*automated where it can be* (that's what [`scripts/check.sh`](../scripts/check.sh) is: stages
5–6 made deterministic).

## Where human judgment stays

Stages 1 (mission/values), 6 (the rubric — "what is an A+?"), and 9 (high-stakes go/no-go)
are **human-owned**. AI accelerates 2–5, 7–8, and *proposes* 6 and 9. See the HJ gates in
[`docs/OBJECTIVES.md`](../docs/OBJECTIVES.md).

## Templates

[`templates/`](templates/) has a fill-in-the-blank starter for each stage. Copy the loop into
any new module, tool, or startup experiment.
