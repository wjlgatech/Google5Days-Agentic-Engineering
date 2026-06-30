# 10X Proposal — Deepen · Widen · Lengthen · Heighten

A grounded review of the Agentic Engineering Hub and one seminal 10X move per axis.
Each move is anchored to a verified gap between what the hub *claims* and what it *mechanizes*.

## Baseline (verified 2026-06-30)
- 5 modules (M1–M5), 7 parts × 5 personas, runnable zero-dep exercises + selftests.
- The Loop (Intent→…→Decide), `tools/spec-to-green`, `memory/` (decisions+lessons), `schemas/`.
- `scripts/check.sh` gate, `tests/` pytest, agentic landing page + free-Gemini backend (Vercel),
  Google Material-3 theme via the `themes.css` seam. Live on GitHub Pages.
- `anyagent analyze` ≈ **64/100**.

Gaps found (claim vs mechanism):
- "Living/compounding system" — `memory/` was **hand-seeded**; a lesson never became a check.
- "5 modules = one loop" — proven at runtime (O11) but **5 separate scripts**, no shared kernel.
- Gate ran **only when a human ran it** — no CI, no Makefile (so `anyagent goal` found no check).
- `schemas/module.schema.json` exists but **nothing generates from it**.

---

## ↓ Deepen — make the root claim true ✅ SHIPPED
The hub's irreducible atom is *"evidence changes the next decision."* It was prose.
**Move:** a lesson's fix becomes a **live, enforced check automatically** — `system_improvement.guard
{desc,cmd}` on a lesson + objective **O14** that runs every guard. Banking a lesson grows the gate
by one with **zero edits to `check.sh`**; a broken guard turns it RED.
**Why 10X:** every other feature now inherits compounding; the hub stops *teaching* the loop and
*is* it. Gate: 102 → 104, proven by adding/removing a demo lesson (count moved, guard enforced).

## ↔ Widen — same engine, new market (Ansoff: market development)
Single-player today. **Move:** cohort/org mode — `memory/` becomes a *team's shared* store, the gate
becomes their *CI*, learning-paths become *onboarding tracks*; expose `spec-to-green` as an **MCP
server** other agents call. **Why 10X:** "a person learns" → "an org compounds"; the memory asset
gains network effects. **First step:** namespace `memory/` by contributor + a `paths/onboarding.md`.

## → Lengthen — self-enforcing infrastructure (Three Horizons / Wardley)
**Move:** GitHub Actions CI running the full bar (`make check` + O11 e2e + a live-Pages smoke test)
on **every PR**, plus the free-LLM **fallback chain** (NIM→Groq→Gemini) in `webapp/` so it survives
throttling. **Why 10X:** "I verified it" → "the system verifies itself, always"; custom → commodity.
**First step (done here):** a `Makefile check:` target — a single finish line CI and `anyagent goal`
can both route to.

## ↑ Heighten — extract the grammar (abstraction laddering / MDL)
The repo IS a grammar: **7 parts × 5 personas × {runnable+selftest} × 1 check-line.**
`schemas/module.schema.json` names it; nothing generates from it. **Move:** a generator that consumes
the schema, so a new module — or a whole new course on any topic — is **declared, not hand-authored
across 35 files.** **Why 10X:** marginal cost of a module drops ~10×; the hub generalizes from "a
course about agents" to "a compiler for compounding, gate-verified courses." **First step:**
`scripts/new-module.py M6 "<title>"` emitting persona stubs that pass O4 by construction.

---

## Recommended order
**Deepen first** (done) — it makes the central promise real and everything compounds on it:
Heighten's generator should emit modules whose lessons auto-ratchet (Deepen); Lengthen's CI enforces
the ratchet; Widen's cohort mode shares the ratcheted memory. Deepen is the root; the others scale it
out, up, and forward.
