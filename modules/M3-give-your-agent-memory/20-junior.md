# M3 for the 🛠️ 20-year-old Junior Engineer — Give Your Agent Memory

*Goal: build the session + memory plumbing real agents need, and learn the failure modes
(context rot, duplication, stale recall) before they bite you in production.*

## Plain explanation

Context engineering = dynamically assembling the right payload each turn: system prompt + tools
+ retrieved memories + recent history + the query, capped to a budget. **Session** = short-term
(events + a `state` scratchpad); **Memory** = long-term, *curated* (not raw transcript). Memory
generation is an ETL pipeline: **extract → consolidate (merge/update/create) → store →
retrieve**, ideally run **async off the hot path** so you never block the user.

## Concrete example

In the exercise, `consolidate("...window seat...")` twice yields **one** updated memory, not two
— because it detects the shared topic. `retrieve()` ranks by **relevance + recency +
importance** (a blend), and `assemble_context()` drops the *oldest* events to fit a char budget.
That budget loop is context-rot defense you can actually unit-test.

## Hands-on exercise

```bash
cd modules/M3-give-your-agent-memory/exercise && python3 context_manager.py --selftest
```
Junior reps:
1. **Crude stemming:** make `_sig` strip a trailing `s` so `seat`≈`seats`; add a test that
   `retrieve('seat preference')` now returns the seat memory. (See the README's "real
   limitation" — fixing it *is* the lesson.)
2. **Token budget:** change `assemble_context` to cap by word count; test the cap holds.
3. **Wire it up:** feed `assemble_context(...)` into M1's loop as the per-turn context. Your
   agent now remembers across turns without re-sending the whole history.

## Real-world use case

This is the shape of ADK Sessions + a Memory Bank: events/state for the conversation, a
background memory service that extracts & consolidates, and retrieval that injects a few facts
into the prompt. RAG sits alongside (facts about the world); memory is facts about the user.

## Failure mode

**Context rot, duplication, and stale recall.** Sending the whole transcript every turn rots
attention and runs up cost; not consolidating yields contradictory memories; relying on vector
relevance alone surfaces old-but-similar trivia (blend in recency + importance). Also
**dialogue injection** — injecting a memory the model mistakes for something actually said.

## Measurable output

```bash
python3 context_manager.py --selftest && echo PASS
```
**Done when** your stemming + budget tests pass and (bonus) the M1 loop reasons over an
assembled, budgeted context. Commit it.

## Next step

- Add the *facts* half → a tiny RAG retriever beside the memory store (later module).
- Then **M4 (Agent Quality)**: now that the agent acts *and* remembers, measure whether it's
  any good — evaluate the trajectory, including whether it retrieved the right context.
