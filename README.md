# 🛠️ The Agentic Engineering Hub

> **Where humans and AI agents learn, build reusable capabilities, and ship real systems
> together — moving from curiosity → understanding → practice → production → compounding
> capability.**

Built on the five Google *5-Day Agentic Engineering* whitepapers (in [`docs/`](docs/)),
distilled into one operating system. Not a course you read — a **living system you run.**

[**▶ Open the hub (index.html)**](index.html) · [Principles](docs/PRINCIPLES.md) ·
[The Loop](loop/README.md) · [Objectives / how "done" is checked](docs/OBJECTIVES.md)

---

## Start in 60 seconds

```bash
git clone <this-repo> && cd Google5Days-Agentic-Engineering
python3 modules/M1-your-first-agent-loop/exercise/agent_loop.py --selftest   # run a real agent
open index.html                                                              # browse the hub
bash scripts/check.sh                                                        # see what "green" means
```

Then **pick your level** → [`personas/`](personas/):
🧒 [15](personas/15-explorer.md) · 🛠️ [20](personas/20-junior.md) ·
🏗️ [30](personas/30-senior.md) · 🎯 [40](personas/40-director.md) ·
💼 [50](personas/50-executive.md). &nbsp;Or see the whole journey →
**[Learning Paths (M1→M5, per persona)](personas/LEARNING-PATHS.md)**.

---

## The big idea: the five days are one loop

| Day (whitepaper) | Teaches | Loop stage |
|---|---|---|
| 1 · Introduction to Agents | an agent = model+tools+orchestration+runtime, in a loop | Intent → Plan |
| 2 · Agent Tools (+ MCP) | task-shaped tools with clear contracts | Specification → Execute |
| 3 · Context Engineering | sessions (now) + memory (across time) | Execute (state) |
| 4 · Agent Quality | evaluate the *trajectory*, not just the answer | Validate → Evaluate → Diagnose |
| 5 · Prototype → Production | AgentOps, evaluation-gated deployment | Learn → Decide → (loop) |

The hub's cycle — `Intent → Plan → Specification → Execute → Validate → Evaluate → Diagnose →
Learn → Decide` — is those five days as **one repeatable, compounding loop**
([`loop/README.md`](loop/README.md)).

## What's in here (the three pillars of the mission)

```
Google5Days-Agentic-Engineering/
├── README.md              ← you are here (the operating system)
├── index.html             ← self-contained hub for humans (zero deps, GitHub-Pages ready)
│                             — incl. an AGENTIC landing panel: an in-browser persona router
│                               + a live M1 agent loop (offline; upgrades to a live model via webapp/)
├── webapp/                ← OPTIONAL LLM backend (FastAPI + Claude) the landing page calls when hosted
├── docs/
│   ├── 2025_Day_*.pdf      ← the 5 source whitepapers
│   ├── PRINCIPLES.md       ← distilled spine, provenance preserved (fact/decision/assumption)
│   └── OBJECTIVES.md       ← the verification registry ("done" is defined here)
├── personas/              ← PILLAR 1: 5 adaptive on-ramps (15 / 20 / 30 / 40 / 50)
├── modules/
│   ├── M1-your-first-agent-loop/   ← FULLY-built module: 7 parts × 5 personas + runnable agent loop
│   ├── M2-give-your-agent-hands/   ← FULLY-built module: tools + contracts + runnable tool registry
│   ├── M3-give-your-agent-memory/  ← FULLY-built module: context engineering + runnable context manager
│   ├── M4-is-your-agent-any-good/  ← FULLY-built module: agent quality + runnable trajectory evaluator
│   └── M5-ship-it-without-breaking-it/ ← FULLY-built module: prototype→production + runnable deploy gate
├── tools/
│   └── spec-to-green/      ← PILLAR 2: one reusable agent tool, full 8-field contract, portable
├── loop/                  ← PILLAR 3: the closed-loop engine + per-stage templates
├── memory/                ← reusable org memory: decisions/ + lessons/ (the compounding store)
├── schemas/               ← structured-output contracts (module / tool / decision / lesson)
├── tests/                 ← pytest wrappers around each module's --selftest (dev-facing test view)
└── scripts/check.sh       ← the deterministic verification harness (run it; drive it green)
```

**Pillar 1 — Personalized, plug-and-play learning.** Every module has the 7 mission-required
parts (plain explanation · example · exercise · use case · failure mode · measurable output ·
next step) and is written for all 5 personas. M1 is the worked example + the template.

**Pillar 2 — Reusable tools for coding agents.** Every tool ships the 8-field contract
(purpose · inputs · outputs · when-to-use · when-NOT · workflow · validation · failure
handling), enforced by [`schemas/tool.schema.json`](schemas/tool.schema.json), portable across
Claude Code / Codex / Hermes / Gemini. `spec-to-green` is the worked example.

**Pillar 3 — A hub for human + AI collaboration.** The closed loop, structured schemas, and an
org-memory store ([`memory/`](memory/)) turn this from a static knowledge base into a **living
system**: each run records a decision + a lesson, so the next run starts smarter.

## How to add to the hub (the compounding motion)

1. **New module?** Copy `modules/M1-your-first-agent-loop/`, fill the 7 parts × 5 personas,
   add a runnable artifact + self-test. `bash scripts/check.sh` gates it (O4).
2. **New tool?** Copy `tools/spec-to-green/`, fill `contract.json` (all 8 fields), add
   `SKILL.md` + `prompt.md` for portability. The harness validates it (O5).
3. **Learned something / hit a failure?** Add a `memory/lessons/L###.json` whose fix is ideally
   a new check. Record the call in `memory/decisions/D###.json`.

Every addition makes the next one easier. That's the North Star: **purpose → action → evidence
→ wiser next decisions.**

## Design principles (and how the whitepapers enforce them)

See [`docs/PRINCIPLES.md`](docs/PRINCIPLES.md). In one line: *prefer deterministic enforcement
where correctness matters (schemas, `check.sh`, eval gates); use prompts/judgment for the rest;
keep humans accountable for mission, truth claims, and high-stakes approval.*

## Verification

`bash scripts/check.sh` runs objectives O1–O10 (structure, schema validity, module
completeness, tool contract, loop, provenance, HTML, org memory, runnable exercise). Green =
**structurally complete and internally consistent** — *not* "approved." Approval is the
human-judgment gates HJ1–HJ3 in [`docs/OBJECTIVES.md`](docs/OBJECTIVES.md). That line is
deliberate: the hub never self-certifies that its content is *good* — that stays yours.

---

*Sources: Google "5-Day Agentic Engineering" whitepapers (2026), in [`docs/`](docs/). This hub
is an independent learning/tooling system built on their principles; all provenance is tagged
in [`docs/PRINCIPLES.md`](docs/PRINCIPLES.md).*
