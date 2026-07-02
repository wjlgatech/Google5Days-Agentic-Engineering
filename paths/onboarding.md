# Team onboarding path (cohort mode)

The hub isn't just for one learner — a **team** can compound on it. This is the shared track a
new teammate follows, and the convention that turns individual learning into org memory.

## The track (½ day → first shipped guard)
1. **Run the gate once** — `make check` (104 checks + tests). This is our definition of "green".
2. **M1 → M5, at your level** — pick your row in [`../personas/LEARNING-PATHS.md`](../personas/LEARNING-PATHS.md)
   and work M1 (loop) → M2 (tools) → M3 (memory) → M4 (quality) → M5 (ship). Each is runnable.
3. **Bank your first lesson** — the moment something bites you, add `memory/lessons/L###.json`
   with a `system_improvement.guard` (a shell cmd that fails if the bug returns) and an `author`.
   Re-run `make check`: the gate grows by one (**O14**). You just made the whole team safer.

## Cohort convention (how individual learning becomes org memory)
- **Shared memory.** `memory/decisions/` and `memory/lessons/` are the team's store, not one
  person's. Every lesson carries an `author` so credit and context travel with it.
- **The gate is our CI.** A lesson's `guard` runs on every push (`.github/workflows/ci.yml`), so a
  bug one teammate hit can never silently return for anyone.
- **New modules are declared, not hand-written.** `python3 scripts/new-module.py M6-… "Title"`
  scaffolds a schema-conformant module (passes O4/O10 by construction) — so onboarding a *topic*
  is as cheap as onboarding a person.
- **The tools are callable by agents too.** `tools/spec-to-green/mcp_server.py` exposes the
  spec→green discipline over MCP, so a teammate's coding agent uses the same bar we do.

> The compounding claim, made literal: a person learns → banks a guarded lesson → the gate
> ratchets up → the next teammate starts from a higher floor.
