# Changelog

All notable changes to the Agentic Engineering Hub. Format: [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- **Widen · Lengthen · Heighten — the remaining three 10X axes, shipped (with before→after proof
  in [`docs/UPGRADE-EVIDENCE.md`](docs/UPGRADE-EVIDENCE.md), written for a 15-year-old).**
  - **↑ Heighten — module generator (`scripts/new-module.py`):** adding a module drops from
    **9 hand-authored files → 1 command**; output passes O4 (7 headings ×5 personas) + O10
    (self-test) by construction. Verified by generating to a temp dir and running both checks.
  - **→ Lengthen — CI + free-LLM fallback chain:** `.github/workflows/ci.yml` runs `make check`
    on **every push/PR** (was 0 automated); `webapp/guide.py` now tries an **ordered 4-provider
    chain** (Gemini → Groq → NVIDIA NIM → OpenRouter, was 1) via `active_providers(env)` +
    fall-through, so a rate-limit no longer kills the LLM path. Verified: `tests/test_fallback.py`
    (4 tests, chain order) + live Gemini still routes.
  - **↔ Widen — MCP + cohort:** `tools/spec-to-green/mcp_server.py` exposes the tool over **MCP**
    (verified with a real initialize/tools-list/tools-call session) so any agent client can call
    it; `paths/onboarding.md` + an `author` field on lessons turn single-player learning into a
    **team's shared, compounding memory**.
  - Net: `anyagent analyze` 62 → **65/100** (earned by adding tools+tests, not deleting); gate
    stays **104/104**; nothing broke.
- **O14 — the compounding loop, mechanized (Deepen 10X).** The hub's root claim ("evidence
  changes the next decision / a living system that compounds") was prose: `memory/` was hand-seeded
  and a lesson never became a check. Now a lesson carries an executable `system_improvement.guard
  {desc, cmd}`, and a new gate objective **O14** runs every guard — so **banking a lesson grows the
  gate by one with zero edits to `scripts/check.sh`**, and a broken guard turns the gate RED.
  Wired the two existing lessons (L001 startswith-key, L002 unknown-param path) to real guards;
  gate 102 → **104/104**. Proven by adding/removing a demo lesson (count moved 104→106; bad guard
  went RED). Schema (`schemas/lesson.schema.json`) + `docs/OBJECTIVES.md` updated.
- **`Makefile` — one finish line (`make check`).** Wraps `scripts/check.sh` + `pytest tests/` so CI
  and `anyagent goal` can discover/route to the check (previously it found none).
- **`docs/10X-PROPOSAL.md`** — grounded review + one seminal 10X move per axis (Deepen ✅ shipped;
  Widen = cohort/org mode + MCP `spec-to-green`; Lengthen = CI + free-LLM fallback chain;
  Heighten = a generator off `schemas/module.schema.json`).

### Changed
- **Google (Material 3) brand theme via a swappable seam.** Re-themed `index.html` to the
  `webapp-style` token contract and dropped in `themes.css`: the page now reads only design
  tokens (`--canvas/--surface/--ink/--accent/--radius/--shadow/--font-*`) instead of hardcoded
  dark-theme colors, and `<html data-theme="google">` selects the Material 3 body — white canvas
  with the multi-color radial wash, `#1A73E8`/`#EA4335` accents, 16px rounding, elevation shadow,
  Google Sans/Roboto type. Swapping `data-theme` now restyles the whole hub (9 bodies ship in
  `themes.css`); adding a brand is one `[data-theme]` block, zero component edits. Fixed two
  light-on-light readability bugs surfaced by the swap (the lede + two inline greys → `--muted`).
  Verified in a headless browser (canvas `#fff`, ink `#202124`, lede readable, both agent panels
  still work). Gate 102/102.

### Added
- **Live LLM backend — deployed to Vercel, free, and wired into the page.** The guide agent's
  backend now runs at `https://webapp-nu-hazel.vercel.app/api/agent` and `index.html` points
  `window.AGENT_BACKEND` at it, so the persona router uses a **real model** (not just keyword
  matching) out of the box. Per the `free-llm` playbook it calls **Google Gemini's free tier**
  (`gemini-2.5-flash-lite`, OpenAI-compatible) — no paid key, no card, ~1,500 req/day; the browser
  hits our backend, which calls Gemini **server-to-server** (no CORS issue), and the free tier
  means an abused public endpoint just rate-limits (no bill). Fallback chain: **Gemini → in-browser
  rule-based router** (503/502/timeout → page routes client-side; never breaks). Refactor: routing
  logic extracted to `webapp/guide.py` (stdlib only), shared by `api/agent.py` (Vercel function)
  and `app.py` (local FastAPI); dropped the `anthropic` dep. Verified live: `POST /api/agent`
  returns correct routing, and a real headless-browser run (page → Vercel → Gemini) routed
  "don't regress when we ship" → M5, tagged "routed by live LLM backend."
- **`tests/` — the honest "10x" quality lift (testing 0% → 57%).** `pytest` wrappers that import
  each `modules/M*/exercise/*.py` and assert its `selftest()` returns 0 (auto-discovers new
  modules; a presence test guards against a missing artifact). This is the pedagogy-safe fix the
  rejected `anyagent refactor` should have been: `anyagent analyze` now scores the repo **64/100**
  (testing 0→57%) — close to the refactor's 68, but earned by *adding* real test files rather than
  *deleting* the teaching comments. The authoritative check is still `scripts/check.sh` (O10);
  `tests/` is the dev-facing/CI view of the same selftests. Run: `pytest tests/ -q` (6 passed).
- **Agentic landing page (`index.html` `#guide`) + optional LLM backend (`webapp/`).** The hub's
  landing now opens with a working agent, not just links: (1) a **persona router** — a rule-based
  agent loop that reads the visitor's level + goal and routes them to the right module + persona
  path, and (2) a **live M1 agent loop** ported to JS (the calculator/sunset tools + rule-based
  planner from `agent_loop.py`), so a visitor watches an agent pick tools and think in-browser.
  Both run client-side with zero dependencies and work offline. **Hybrid upgrade:** when
  `window.AGENT_BACKEND` is set, the router calls `webapp/app.py` — a FastAPI `/api/agent`
  endpoint using `claude-opus-4-8` with a JSON-schema structured output; with no API key it
  returns 503 and the page falls back to client-side routing, so the site never breaks. Verified:
  11/11 logic checks in Node + a real headless-browser run (no console errors, both panels render
  correct output, recommended link resolves to an existing file). Gate still 102/102. Added a
  root `.gitignore` (`__pycache__/`, `.gstack/`, `.env`) and untracked churning `.pyc` caches.

### Investigated / Rejected
- **Automated OOP refactor of the exercises (`anyagent refactor`, score 57→68).** Measured: it
  raised the OOP-quality metric by stripping the Day-citation comments, the loop-stage
  annotations, and the `YOUR TURN` scaffolding the lessons depend on, and churned quotes/regex
  that desync the prose lessons. **Rejected** — on a *teaching* repo a higher OOP score on
  deliberately-simple artifacts is the wrong target; it would undo the HJ1 lesson↔code sync. The
  honest, pedagogy-safe improvement (the real "testing 0%" gap) is a `tests/` dir of pytest
  wrappers around the existing `--selftest`s — additive, leaves the teaching code untouched.

### Changed
- **HJ2 framing pass · director/executive altitude leak (all 5 modules).** A five-reader audit
  (one per module, shared altitude rubric) confirmed persona differentiation is genuinely real
  (build→debug→architect→operate→fund, scored 8–9.5/10) — but found one systemic drift: the
  **40-director** lessons showed a CLI block under a bare "Hands-on exercise" header with no
  delegation guard, and the **50-executive** lessons implied the exec runs code ("yes, you too",
  and M1's "or do it"). Reframed all 10 headings to signal delegation ("Hands-on — your team runs
  it, you read the result" / "someone runs it, you just watch"), added the missing "have an
  engineer run it in front of you" guard to every director lesson, and removed M1-exec's "or do
  it" invitation. Also trimmed a meta sentence in M1/15-explorer that overshot explorer altitude.
  Headings retain the "Hands-on" token the O4 gate keys on; gate still 102/102.

### Fixed
- **HJ1 cold-read sweep · M2–M5 exercises (all personas).** Extended the M1 walk-through to the
  remaining four modules, verifying each runnable exercise end-to-end:
  - **Wrong path (universal, 20 instances).** Every M2–M5 persona lesson said `cd exercise`,
    which fails from the repo root the README quickstart leaves you in. All now use the full
    `cd modules/<module>/exercise` path.
  - **M3 false proof (15-explorer).** The "make `seat`≈`seats`" fix is real and visible in the
    *demo* (`retrieve('seat preference')` top hit flips from "allergic to peanuts" → the seat
    memory), but the lesson pointed the proof at `--selftest`, which is 8/8 green with or without
    the fix — so a student couldn't tell their fix did anything. Repointed the proof at the demo
    before/after, and added a *verified* self-test snippet (builds its own plural-"seats" memory;
    ✗ before the fix, ✓ after) so the win is guarded by a green check, per the module's own habit.
  - **Verified clean:** M2's "add `_track_shipment`" exercise is *not* a dead-tool trap (the
    registry dispatches by name, so register + a self-test line genuinely suffices — confirmed by
    simulation); M4/M5 15-explorer exercises are read-only (observe output), so only the path bug
    applied. Gate still 102/102.
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
