# Changelog

All notable changes to the Agentic Engineering Hub. Format: [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- **M4 · Is Your Agent Any Good? (Agent Quality)** — fourth fully-built module: the 7 parts ×
  5 personas + a runnable, zero-dependency `trajectory_eval.py` implementing Day 4 — Outside-In
  scoring (Black-Box task success → Glass-Box trajectory), the Four Pillars (Effectiveness /
  Efficiency / Robustness / Safety), pairwise judging, and a `NEEDS_HUMAN` gate it never
  self-answers (the rubric is human-owned). Self-test 11/11. Wired into `index.html` and `README.md`.
- **M3 · Give Your Agent Memory (Context Engineering)** — third fully-built module: the 7 parts
  × 5 personas + a runnable, zero-dependency `context_manager.py` implementing Day 3 — a Session
  with compaction, a MemoryStore with consolidation / blended retrieval (relevance + recency +
  importance) / pruning / provenance, and `assemble_context()` that packs the window to a budget
  (the context-rot defense). Self-test 8/8. The exercise also surfaces a deliberate naive-retrieval
  limitation as a teaching point. Wired into `index.html` and `README.md`.
- **M2 · Give Your Agent Hands (Agent Tools)** — second fully-built module: the 7 parts × 5
  personas + a runnable, zero-dependency `tool_registry.py` that validates every call against
  a tool contract and returns errors that teach recovery (Day 2 made executable). Wired into
  `index.html` and `README.md`.

### Changed
- **Verification harness generalized + tightened** (`scripts/check.sh`): O4 now iterates
  **every** `modules/*/` and matches the 7 parts on **heading lines** (`^#+ .*`) instead of
  anywhere in prose (closes the run-1 flaky-risk); O10 runs `--selftest` for **every** module
  exercise. Adding a module now auto-extends the gate with no harness edit (D002).

### Earlier this cycle
- **Hub operating system** — top-level `README.md`, self-contained `index.html` hub
  (zero-dep, GitHub-Pages ready), and `AGENTS.md` agent guide. Establishes the three mission
  pillars on one substrate.
- **Distilled principles** — `docs/PRINCIPLES.md`: the five Google whitepapers compressed into
  one spine, with `[FACT]`/`[DECISION]`/`[ASSUMPTION]` provenance tags. Maps the 5 days onto
  the closed loop. _Why:_ make the source principles the auditable source of truth for content.
- **The closed loop** — `loop/README.md` (9 stages `Intent→…→Decide` mapped to the 5 days) +
  `loop/templates/loop-instance.md`. _Why:_ a loop's output feeds its next input — the
  compounding mechanism (Design Principle #1).
- **M1 · Your First Agent Loop** — one fully-built module: the 7 mission-required parts written
  for all 5 personas (15/20/30/40/50), plus a runnable, zero-dependency `agent_loop.py` with a
  `--selftest`. The template every future module copies.
- **Tool · spec-to-green** — one reusable coding-agent tool with the full 8-field contract
  (`contract.json` + `SKILL.md` + portable `prompt.md`), valid against `schemas/tool.schema.json`.
- **Structured-output schemas** — `schemas/{module,tool,decision,lesson}.schema.json`. _Why:_
  prefer deterministic enforcement where correctness matters (Design Principle #5).
- **Verification harness** — `docs/OBJECTIVES.md` (registry O1–O10 + human gates HJ1–HJ3) and
  `scripts/check.sh` (deterministic gate; runs the exercise self-test). _Why:_ "done" must be
  provable, not claimed (Day 4/5 evaluation-gated).
- **Org memory seed** — `memory/decisions/D001` (deep-vertical decision) and
  `memory/lessons/L001` (the trajectory/action representation-mismatch bug hit while building
  the exercise, now guarded by a check).

### Investigated / Rejected
- **Broad scaffold (all modules/tools stubbed)** — rejected in favour of a deep vertical
  template; a proven, copyable M1 + tool compounds better than a wide-but-shallow map (D001).
- **Runnable app (CLI/server) form factor** — deferred; Markdown source-of-truth + a
  self-contained HTML hub matches how this hub is shared and keeps it zero-dependency.
