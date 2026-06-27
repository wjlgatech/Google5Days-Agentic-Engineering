# Changelog

All notable changes to the Agentic Engineering Hub. Format: [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Fixed
- **HJ1 cold-read sweep · M1 exercises across all 5 personas.** A human walk-through of the M1
  path (the kind the 102-check gate can't perform) surfaced three classes of break, all fixed
  and each fix verified by simulating the student's edits and running the result:
  - **Dead-tool trap (15-explorer, 20-junior).** The "add your own tool" exercises pointed only
    at the `TOOLS` registry, but the rule-based `think()` planner has no rule to *select* a new
    tool — so a student who followed the steps saw zero change. Both lessons now spell out three
    edits (write → register-with-key → add a planner rule) and `agent_loop.py` carries `YOUR TURN`
    guide comments at both spots (comments only; shipped self-test unchanged, still 6/6).
  - **False debugging promise (20-junior).** The lesson said change `\d+`→`\d` and "watch a test
    go ✗" — but the self-test mission `6 * 7` is single-digit, so the match is identical and every
    test stayed green. Replaced with the verified break `\d+`→`\d\d+` (drops single-digit matches →
    `calculator used` and `answer has 42` go red), with the trajectory explanation.
  - **Wrong path (all 5 personas).** Lessons said `cd exercise`, which fails from the repo root the
    README quickstart leaves you in. Now `cd modules/M1-your-first-agent-loop/exercise`.
  Also: the `TOOLS` "list" → "dict (needs a name key)" wording, and a self-test line for the
  student's own tool so their addition is *proven green*, not eyeballed — closing the "grow the
  test, don't just use it" habit the personas preach. Gate still 102/102.

### Added
- **M5 · Ship It Without Breaking It (Prototype → Production)** — fifth and final module,
  completing all 5 whitepaper days: the 7 parts × 5 personas + a runnable, zero-dependency
  `deploy_gate.py` implementing Day 5 — an **evaluation-gated deploy pipeline that imports M4's
  evaluator** as its gate (BLOCKED → canary → human sign-off → PROMOTED / ROLLED_BACK /
  HELD_FOR_SIGNOFF), plus `evolve()` that turns a production failure into a golden eval case
  (Observe→Act→Evolve). Self-test 10/10. This closes the hub's Intent→…→Decide loop. Wired into
  `index.html` and `README.md`.
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

### Added (marketing)
- **`docs/marketing/`** — a long-form article (`ARTICLE-from-prompt-to-proof.md`, ~1,400 words,
  fully referenced) and a ~190-word short post (`SHORT-POST.md`), connecting the hub to the
  FDE-os thesis and grounded in cited sources (MIT NANDA "GenAI Divide" 2025; FDE demand/comp
  data; the five Google whitepapers).

### Added
- **Capstone learning paths** — `personas/LEARNING-PATHS.md`: threads all five modules (M1→M5)
  into one coherent journey **per persona**, each step naming its runnable artifact and outcome,
  and ending in an **integrative capstone project** + a measurable "graduated when." Linked from
  `personas/README.md`, `index.html`, and `README.md`; gated by a new **O13** check (the doc must
  reference all 5 modules and all 5 personas).

### Changed
- **No-broken-promises check (O12)** — closes a harness blind spot: O4 only iterated *existing*
  module dirs, so a deleted module passed silently. O12 cross-checks `index.html`'s module cards
  against `modules/` **bidirectionally** — every advertised module must exist, and every on-disk
  module must be advertised. Verified to catch a deletion (hiding M3 turns the harness RED).
  check.sh: 91/91 green.
- **End-to-end capstone check (O11)** — `scripts/e2e.py` runs the real chain on a **live** run:
  M1 executes an agent loop → M4 evaluates its actual trajectory → M5 gates the release. Added
  to `scripts/check.sh` (O11) and `docs/OBJECTIVES.md`. The hub's "it all composes into one
  loop" claim is now machine-verified, not just asserted. check.sh: 81/81 green.
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
