# Loop instance — copy this for any module, tool, or startup experiment

> Fill in every stage. Empty stages are where agents (and teams) silently go wrong. Stages
> ①, ⑥-rubric, and ⑨-high-stakes are **human-owned**.

| Stage | Prompt | Your answer |
|---|---|---|
| ① **Intent** | What's the mission, for whom, and what does "done" look like (one metric)? | |
| ② **Plan** | Sequential or multi-agent? Which model(s)/tools? | |
| ③ **Specification** | Acceptance criteria as deterministic assertions; write the failing check first. | |
| ④ **Execute** | Smallest action toward green; manage session + memory state. | |
| ⑤ **Validate** | Did the final output meet the objective? (Black-Box, pass/fail) | |
| ⑥ **Evaluate** | Score the trajectory across the Four Pillars; rubric is human-written. | |
| ⑦ **Diagnose** | If it failed/scored low — which trajectory step broke, and why (root cause)? | |
| ⑧ **Learn** | Record a lesson; ideally the fix is a new line in the check. | `memory/lessons/L###.json` |
| ⑨ **Decide** | Next step; record the decision; re-enter the loop. | `memory/decisions/D###.json` |

**Stop rule:** same failure 3× → halt and escalate with the trajectory. Never fake a green.
