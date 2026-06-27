# M3 for the 🏗️ 30-year-old Senior Engineer — Give Your Agent Memory

*Goal: design the state architecture — sessions, memory, RAG — with the right latency, isolation,
and consistency properties, and know which work belongs off the hot path.*

## Plain explanation

Context engineering is a systems problem dressed as a prompting problem. You're managing three
stores with different SLAs: **session** (low-latency, read every turn), **memory** (curated,
per-user, eventually-consistent, written async), and **RAG** (shared, static-ish facts). The
discipline is "no more, no less than the most relevant info" under a token budget — which means
compaction, blended retrieval, consolidation, and pruning are first-class, testable components,
not prompt tweaks.

## Concrete example

The exercise separates the hot path (`assemble_context` packs to a budget, dropping oldest
events) from the curation path (`consolidate`/`prune`). In production those split further:
memory generation is an **async LLM ETL** (extract→consolidate→store) behind a queue with
retries + dead-letter + optimistic locking, so a slow consolidation never blocks the user.
Retrieval blends relevance + recency + importance precisely because vector-similarity-only
recall is a known failure.

## Hands-on exercise

```bash
cd modules/M3-give-your-agent-memory/exercise && python3 context_manager.py --selftest
```
Senior moves:
1. **Isolation + provenance:** add a `user_id` scope to `MemoryStore`; prove one user can't
   retrieve another's memory (ACL). Keep provenance on every record.
2. **Consolidation conflicts:** make `consolidate` handle contradiction (newer high-confidence
   fact invalidates the old) and test it — descriptive, not predictive.
3. **Budget strategy:** compare keep-last-N vs. recursive summarization for compaction; measure
   tokens saved vs. info lost.

## Real-world use case

This is the design behind Agent Engine Sessions + Memory Bank, or any stateful assistant: a
framework-agnostic memory representation (plain dicts/strings — so a LangGraph↔ADK handoff is
possible), async curation, per-user isolation, and retrieval tuned past naive similarity. Senior
calls: where to spend the latency budget, what to persist vs. recompute, how to bound cost.

## Failure mode

**Blocking the hot path with curation, leaking memory across users, and trusting persisted
state.** Synchronous memory generation tanks UX; missing ACLs exfiltrate PII across user
boundaries; unvalidated writes enable **memory poisoning** via prompt injection. Plus context
rot from never compacting. Defenses: async curation, strict isolation, validate-before-persist,
budgeted assembly.

## Measurable output

```bash
python3 context_manager.py --selftest   # + your isolation, conflict, and budget tests green
```
**Done when** memory is per-user isolated with provenance, consolidation resolves contradictions,
curation is off the hot path, and assembly is provably budget-bounded.

## Next step

- Add the RAG half and a reranker; measure retrieval quality as its own metric.
- Then **M4 (Agent Quality)**: evaluate RAG/context handling *in the trajectory* — did the agent
  retrieve and use the right context, or hallucinate past it?
