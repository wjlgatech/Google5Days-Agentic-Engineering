# M3 — Give Your Agent Memory (Context Engineering)

> The third module. M1 gave a **loop**, M2 gave **hands**; M3 gives **what the agent knows,
> turn by turn**. Day 3's one-liner: an LLM is stateless, so statefulness is *engineered* —
> put "no more and no less than the most relevant information" in the context window.
> Conforms to [`schemas/module.schema.json`](../../schemas/module.schema.json); gated by
> [`scripts/check.sh`](../../scripts/check.sh) (O4/O10).

**Loop stage owned:** ④ Execute (state) &nbsp;·&nbsp; **Source:** Day 3 (Context Engineering).

**What you can do after this module:** distinguish a **session** from **memory**, compact a
growing conversation, consolidate/retrieve/prune long-term memories with provenance, and
assemble a context window that fits a budget — defeating *context rot*.

## Plug in at your level

| You are… | Start here |
|---|---|
| 🧒 ~15, curious | [`15-explorer.md`](15-explorer.md) |
| 🛠️ ~20, junior engineer | [`20-junior.md`](20-junior.md) |
| 🏗️ ~30, senior engineer | [`30-senior.md`](30-senior.md) |
| 🎯 ~40, AI director | [`40-director.md`](40-director.md) |
| 💼 ~50, EVP / executive | [`50-executive.md`](50-executive.md) |

## The artifact

[`exercise/context_manager.py`](exercise/) — a real, zero-dependency context manager:
**Session** (with compaction) + **MemoryStore** (consolidate · blended retrieve · prune ·
provenance) + `assemble_context()` that packs the window to a **budget**. Run
`python3 context_manager.py --selftest`.

## The mental model

```
 SESSION (short-term)         MEMORY (long-term, curated)
 ┌───────────────┐            ┌──────────────────────────────┐
 │ event,event…  │  compact   │ consolidate → store → prune  │
 │ + state/cart  │ ─────────▶ │ retrieve by relevance+recency│
 └───────┬───────┘            │            +importance       │
         │                    └───────────────┬──────────────┘
         └──────▶  assemble_context(..., budget)  ◀──────┘   ← context-rot defense
                          │
                          ▼   "no more, no less than the most relevant info"
```

- **RAG vs Memory** (Day 3): RAG makes an agent an expert on *facts* (static, shared); memory
  makes it an expert on *the user* (dynamic, per-user). This module builds the memory half;
  the hub's own [`memory/`](../../memory/) directory is that idea applied to the human+AI team.
- **Memories are descriptive, not predictive**, carry **provenance**, and get **pruned** when
  stale. Heavy memory work belongs **off the hot path** (async) in production.

Prereq: [M2 · Give Your Agent Hands](../M2-give-your-agent-hands/). Next: M4 (Agent Quality —
is the agent any *good*?).
