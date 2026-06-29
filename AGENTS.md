# AGENTS.md — guide for AI agents working in this repo

This repo is the **Agentic Engineering Hub**: a persona-adaptive learning system + reusable
coding-agent tools + a human/AI collaboration loop, built on the five Google *5-Day Agentic
Engineering* whitepapers ([`docs/`](docs/), distilled in [`docs/PRINCIPLES.md`](docs/PRINCIPLES.md)).

## What "done" means here
`bash scripts/check.sh` is the source of truth (objectives O1–O10 in
[`docs/OBJECTIVES.md`](docs/OBJECTIVES.md)). It must exit **0**. Green = structurally complete
and internally consistent. It is **not** approval — content quality (HJ1–HJ3) is a human call.
Never fake a green; an honest ❌ beats a bad fix.

## Repo map
- `docs/PRINCIPLES.md` — the content spine (provenance-tagged: `[FACT]`/`[DECISION]`/`[ASSUMPTION]`). If a file contradicts it, the file is wrong.
- `docs/OBJECTIVES.md` + `scripts/check.sh` — the verification harness.
- `personas/` — 5 on-ramps (15/20/30/40/50). Every module is written for all five.
- `modules/Mn-*/` — learning modules. Each has the **7 parts** (plain explanation · concrete example · hands-on · real-world · failure mode · measurable output · next step) **in each persona file**, plus a runnable artifact with a `--selftest`.
- `tools/<name>/` — reusable tools. Each ships `contract.json` (all **8 fields**: purpose, inputs, outputs, when_to_use, when_not_to_use, workflow, validation, failure_handling) + `SKILL.md` + `prompt.md`.
- `loop/` — the closed loop (`Intent→…→Decide`) + templates.
- `memory/decisions/` + `memory/lessons/` — org memory; JSON validated against `schemas/`.
- `schemas/` — structured-output contracts (module, tool, decision, lesson).
- `tests/` — `pytest` wrappers that import each `modules/M*/exercise/*.py` and assert its `selftest()` returns 0 (auto-discovers new modules). The authoritative check is still `scripts/check.sh` (O10); this is the dev-facing test view. Run: `pytest tests/ -q`.
- `themes.css` — brand-aesthetic **theme seam**: one CSS-variable token contract (`--canvas/--surface/--edge/--ink/--muted/--accent/--accent2/--radius/--shadow/--font-*`), N swappable bodies chosen by `data-theme` on `<html>`. `index.html` reads only these tokens (no hardcoded `#fff`/dark literals) and is set to `data-theme="google"` (Material 3). Swap the attribute → swap the whole look; adding a brand = one new `[data-theme]` block, zero component edits.
- `index.html` — the human hub. Its `#guide` section is **agentic**: a client-side persona router and a live JS port of the M1 loop (both run offline). If `window.AGENT_BACKEND` is set it calls `webapp/`.
- `webapp/` — the guide-agent backend, **deployed** at `https://webapp-nu-hazel.vercel.app` and wired into the page via `window.AGENT_BACKEND`. Routing core in `guide.py` (stdlib + a **free** Gemini OpenAI-compatible call — the `free-llm` playbook, no paid key); shells `api/agent.py` (Vercel function) + `app.py` (local FastAPI). Fallback chain: Gemini → client-side router (page never breaks). Not a learning module; not gated by `check.sh`.

## How to extend (the compounding motion)
1. **Add a module:** copy `modules/M1-your-first-agent-loop/`; fill 7 parts × 5 personas; add a runnable artifact + `--selftest`. Use the **exact** part headings the check greps for (Plain / Concrete example / Hands-on / Real-world / Failure mode / Measurable output / Next step).
2. **Add a tool:** copy `tools/spec-to-green/`; fill `contract.json` (all 8 fields, validates against `schemas/tool.schema.json`); add `SKILL.md` + `prompt.md` for portability.
3. **Record learning:** add `memory/lessons/L###.json` (its fix ideally a new check line) and `memory/decisions/D###.json`. Convert relative dates to absolute.
4. **Re-run `bash scripts/check.sh -v`** until green.

## House rules
- Prefer **deterministic enforcement** (schemas, checks, hooks) for anything that must be correct; use prompts/judgment for the rest (Day 2/4/5).
- Surface **human-judgment gates** to the human with the real artifact — never self-answer them (mission: humans own truth claims + high-stakes approval).
- Separate **facts / assumptions / decisions / opinions**; preserve provenance (Principle #4).
- Per the global policy: a feature change updates `CHANGELOG.md` + the docs it touches in the same change.
