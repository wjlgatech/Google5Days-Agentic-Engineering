---
name: spec-to-green
description: Turn a fuzzy task into a verifiable spec with a deterministic check, then drive code to green against it. Use when a task is fuzzy/multi-step and correctness matters and you want proof-of-done, not a confident "looks good". Not for one-line obvious changes or subjective goals.
---

# spec-to-green

You are running the `spec-to-green` workflow. Your job is to make "done" **provable**, never
merely claimed. Follow these steps; do not skip the failing-check step.

## Steps

1. **Intent.** Restate the request in ONE sentence and state what "done" looks like. If a
   genuine fork exists, ask ≤2 clarifying questions; otherwise state your assumption and go.

2. **Detect the verification source** (do not hardcode one):
   - a project objective registry + runner (e.g. `docs/OBJECTIVES.md` + a harness), else
   - the repo's own check/test command (`make check` · `pnpm check`/`test` · `pytest`/`ruff`
     · `cargo test` · `go test ./...`), else
   - co-define 3–7 verifiable acceptance criteria with the human.

3. **Spec + failing check FIRST.** Write each acceptance criterion as a deterministic
   assertion. Add/extend the check so it currently fails **red**. Show the red. (This is the
   Day-5 evaluation gate; writing the check after the code defeats the purpose.)

4. **Smallest green change.** Make the minimal edit that turns one criterion green. Re-run the
   check. Repeat criterion by criterion.

5. **Bounded fix loop.** Run → read each failure → fix the *named* file → re-run. Stop after
   the **same failure 3×** and escalate with exactly what you tried.

6. **Evaluate the trajectory, not just the final diff** (Day 4). Score against the Four
   Pillars (Effectiveness, Efficiency, Robustness, Safety). Surface any **human-judgment
   gate** — never self-certify subjective quality.

7. **Compound.** Record one decision (`memory/decisions/`) and, if anything failed on the
   way, one lesson (`memory/lessons/`) whose fix is ideally a new line in the check.

## Hard rules
- Never fake a green. An honest ❌ with the trajectory beats a bad fix.
- If information is missing and there's no safe assumption, ask — don't guess on correctness.
- Prefer a deterministic check over your own judgment for anything that must be correct.
