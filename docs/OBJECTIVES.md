# OBJECTIVES — the verification registry

> This is the **source of truth** for "done." A future `/goal-10x` run discovers this file
> and its runner ([`scripts/check.sh`](../scripts/check.sh)) and drives every objective to
> green. This is the hub practicing what Day 4/5 preach: **evaluation-gated, deterministic
> where correctness matters, judgment surfaced to a human where it doesn't.**

Run the harness:

```bash
bash scripts/check.sh          # all objectives, exits non-zero on any failure
bash scripts/check.sh -v       # verbose: print every check
```

## Machine-checked objectives (deterministic gate)

| ID | Objective | Check |
|---|---|---|
| **O1** | Repo skeleton exists | README.md, index.html, CHANGELOG.md, AGENTS.md, docs/PRINCIPLES.md present |
| **O2** | All schemas are valid JSON | every `schemas/*.schema.json` parses |
| **O3** | The 5 personas exist & route to a module | `personas/{15-explorer,20-junior,30-senior,40-director,50-executive}.md`, each links a module |
| **O4** | Module M1 is complete | the 7 required parts present **in each of the 5 persona files** |
| **O5** | The reusable tool is complete | `tools/spec-to-green` carries all 8 contract fields + valid `contract.json` |
| **O6** | The closed loop is documented | `loop/README.md` names all 9 stages in order |
| **O7** | Provenance preserved | `docs/PRINCIPLES.md` cites all 5 days |
| **O8** | HTML hub is real & wired | `index.html` is non-trivial and references the module + the tool |
| **O9** | Org memory is seeded & schema-valid | ≥1 decision + ≥1 lesson, each parsing against its schema |
| **O10** | Runnable exercises work | every `modules/*/exercise/*.py` self-tests green |
| **O11** | Modules compose on a live run | `scripts/e2e.py`: a real M1 run → evaluated by M4 → gated by M5, all green |
| **O12** | No broken promises | every module advertised in `index.html` exists on disk, and every module on disk is advertised (bidirectional) |
| **O13** | Capstone path is complete | `personas/LEARNING-PATHS.md` exists and references all 5 modules (M1–M5) and all 5 personas |
| **O14** | Lessons ratchet (the loop compounds) | every `memory/lessons/*.json` with a `system_improvement.guard` has its `cmd` run by the gate (exit 0). Banking a lesson grows the gate by one with **no edit to `check.sh`** — evidence becomes a permanent check; the bar ratchets up. The compounding loop, mechanized. |

## Human-judgment gates (NOT machine-scored — surfaced, never self-certified)

Per the mission ("humans retain responsibility for truth claims, high-stakes decisions, and
final approval") and Day 4 ("a human writes the rubric"):

- **HJ1 — Is the content actually *good*?** Does M1 teach the loop clearly to its persona?
  (A check can confirm the 7 parts exist; only a human confirms they're worth reading.)
- **HJ2 — Is the persona framing right?** Does the 50-year-old executive version speak to
  ROI/governance, not syntax?
- **HJ3 — Is the next module the right one to build?** (Decided at run's end, with the human.)

A green `check.sh` means *structurally complete and internally consistent* — it does **not**
mean "approved." Approval is HJ1–HJ3, and it's yours.
