# Exercise — give your agent memory

A real context manager in ~140 lines, **zero dependencies**. It shows the two systems of Day 3
— **Session** (short-term) and **Memory** (long-term) — and how to pack a context window to a
budget so the model stays sharp.

```bash
python3 context_manager.py             # demo a short conversation
python3 context_manager.py --selftest  # prove it works (what scripts/check.sh runs)
```

## What to notice
- **Session compaction:** once the conversation passes `keep_n` turns, old events are
  summarized into one line and the verbose originals are dropped — saving tokens and attention.
- **Memory consolidation:** "prefers a window seat" + "wants a window seat reserved" become
  **one** updated memory, not two contradictory ones (the Day-3 merge/update/create step).
- **Blended retrieval:** results are ranked by **relevance + recency + importance**, not vector
  similarity alone.
- **Provenance + pruning:** every memory keeps its `source`; stale, low-importance trivia is
  forgotten.
- **The budget cap in `assemble_context()` is the context-rot defense** — it drops the *oldest*
  events first but always keeps the top memories and the query.

## A real limitation worth seeing (turn it into a lesson)
Run the demo and look at `retrieve('seat preference')` — the top hit may be "allergic to
peanuts", not the seat memory. Why? Our `_sig` matcher is naive: it doesn't know `seat` ≈
`seats` or `preference` ≈ `prefer` (no stemming/embeddings), so relevance is 0 for both and the
**importance** score decides. That's exactly Day 3's warning that keyword/relevance-only
retrieval is brittle — real systems use embeddings. *Seeing the failure is the lesson.*

## Make it yours
1. **Better matching:** make `_sig` strip a trailing `s` (crude stemming) so `seat`≈`seats`;
   re-run the demo and watch retrieval improve. Add a test.
2. **Token budget by words:** change `assemble_context` to cap by word count, not chars.
3. **Wire it to M1/M2:** feed `assemble_context(...)` as the context your agent loop reasons
   over each turn — now your agent remembers across turns.
