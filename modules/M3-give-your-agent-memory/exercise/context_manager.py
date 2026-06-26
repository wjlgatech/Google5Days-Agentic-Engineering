#!/usr/bin/env python3
"""
M3 — Give Your Agent Memory  ·  context engineering in ~140 lines, zero deps.

M1 = the loop. M2 = hands (tools). M3 = what the agent KNOWS, turn by turn. An LLM is
stateless; statefulness is engineered. Day 3's job is "no more and no less than the most
relevant information in the context window" — fighting context rot (attention decays as the
window grows) without forgetting what matters.

Two systems, both real here:
  - SESSION  = short-term: the chronological events of one conversation + a state scratchpad.
               When it grows too big we COMPACT (summarize old events, keep the last N).
  - MEMORY   = long-term: distilled facts that persist, each with provenance + importance.
               We CONSOLIDATE (dedupe/update vs create), RETRIEVE by a blended score
               (relevance + recency + importance — not vector-similarity alone), and PRUNE.

  assemble_context() then packs system + top memories + recent events + query INTO A BUDGET —
  that budget cap is the context-rot defense made literal.

Run it:
    python3 context_manager.py             # demo a short conversation
    python3 context_manager.py --selftest  # deterministic check used by scripts/check.sh
"""
from __future__ import annotations
import sys

STOP = {"user", "the", "a", "an", "of", "to", "on", "in", "is", "and", "for", "now", "with"}

def _sig(text: str) -> set[str]:
    """Significant words (a stand-in for embeddings): >3 chars, non-stopword."""
    return {w.strip(".,!?'\"").lower() for w in text.split()
            if len(w.strip(".,!?'\"")) > 3 and w.strip(".,!?'\"").lower() not in STOP}

# ---- SESSION: short-term memory (Day 3). ----

class Session:
    def __init__(self): self.events: list[str] = []; self.state: dict = {}
    def add(self, ev: str): self.events.append(ev)
    def compact(self, keep_n: int) -> str | None:
        """Summarize all but the last keep_n events into one summary event. Persisted so the
        expensive op isn't repeated; the verbose originals are dropped (cost + context-rot)."""
        if len(self.events) <= keep_n:
            return None
        old, recent = self.events[:-keep_n], self.events[-keep_n:]
        summary = f"[summary of {len(old)} earlier turns: " + "; ".join(e[:24] for e in old) + "]"
        self.events = [summary] + recent
        return summary

# ---- MEMORY: long-term, curated, provenance-tracked (Day 3). ----

class Memory:
    __slots__ = ("text", "importance", "created", "source")
    def __init__(self, text, importance, created, source):
        self.text, self.importance, self.created, self.source = text, importance, created, source

class MemoryStore:
    def __init__(self): self._mem: list[Memory] = []
    def all(self): return list(self._mem)

    def consolidate(self, text: str, importance: float, turn: int, source: str) -> str:
        """Day-3 ETL Consolidation step: merge/update if a similar memory exists, else create.
        Avoids duplication + contradiction. Returns 'updated' or 'created'."""
        sig = _sig(text)
        for m in self._mem:
            if len(sig & _sig(m.text)) >= 2:           # same topic -> UPDATE in place
                m.text = text                          # newest phrasing wins (descriptive, not predictive)
                m.importance = max(m.importance, importance)
                m.source = source                      # refresh provenance
                return "updated"
        self._mem.append(Memory(text, importance, turn, source))   # else CREATE
        return "created"

    def retrieve(self, query: str, now: int, k: int = 3) -> list[Memory]:
        """Blended score = relevance + recency + importance (NOT relevance alone — Day 3
        warns vector-similarity-only surfaces old/trivial-but-similar memories)."""
        q = _sig(query) or {"_"}
        def score(m: Memory) -> float:
            relevance = len(q & _sig(m.text)) / len(q)
            recency = 0.9 ** (now - m.created)
            return relevance * 1.0 + recency * 0.4 + m.importance * 0.4
        return sorted(self._mem, key=score, reverse=True)[:k]

    def prune(self, now: int, ttl: int) -> int:
        """Forget stale, low-importance memories (TTL + time-decay). Returns count removed."""
        before = len(self._mem)
        self._mem = [m for m in self._mem if not (m.importance < 0.3 and (now - m.created) > ttl)]
        return before - len(self._mem)

# ---- ASSEMBLE: pack the window to a BUDGET = the context-rot defense (Day 3). ----

def assemble_context(system: str, session: Session, store: MemoryStore,
                     query: str, now: int, budget: int) -> str:
    """Build the payload, dropping OLDEST events first until it fits the char budget. Memories
    + query are always kept (they're the 'most relevant'); verbose history is what gets cut."""
    mems = [f"- {m.text} (src:{m.source})" for m in store.retrieve(query, now, k=3)]
    head = system + "\nMEMORIES:\n" + "\n".join(mems) + "\nQUERY: " + query + "\nRECENT:\n"
    events = list(session.events)
    while True:
        body = "\n".join(events)
        ctx = head + body
        if len(ctx) <= budget or not events:
            return ctx
        events.pop(0)                                  # drop the oldest recent event and retry

# ---- SELF-TEST = the measurable output (Day 4). scripts/check.sh runs this. ----

def selftest() -> int:
    checks = {}

    # SESSION compaction: keep last 2, summarize the rest.
    s = Session()
    for i in range(6): s.add(f"turn-{i} the user said something fairly long here")
    summ = s.compact(keep_n=2)
    checks["session compacts to keep_n+summary"] = (len(s.events) == 3 and summ is not None
                                                    and s.events[0].startswith("[summary"))

    # MEMORY consolidate: two similar facts -> ONE; an unrelated fact -> separate.
    m = MemoryStore()
    a = m.consolidate("User prefers a window seat on flights", 0.6, 1, "chat")
    b = m.consolidate("User wants a window seat reserved", 0.7, 4, "chat")   # same topic -> update
    c = m.consolidate("Allergic to peanuts", 0.9, 5, "profile")              # new topic -> create
    checks["consolidate updates same topic"] = (a == "created" and b == "updated" and c == "created")
    checks["consolidate dedupes to 2"] = (len(m.all()) == 2)
    checks["provenance preserved"] = all(x.source for x in m.all())

    # RETRIEVE: relevant+recent+important ranks first; blended, not relevance-only.
    top = m.retrieve("which window seat does the user like", now=5, k=1)[0]
    checks["retrieve ranks relevant first"] = ("window" in top.text.lower())

    # PRUNE: a stale low-importance memory is forgotten; important ones survive.
    m.consolidate("Mentioned the weather once", 0.1, 0, "chat")   # low importance, old
    removed = m.prune(now=99, ttl=10)
    checks["prune forgets stale trivia"] = (removed == 1 and len(m.all()) == 2)

    # ASSEMBLE: fits the budget (context-rot defense) AND keeps the top memory.
    ctx = assemble_context("SYS", s, m, "window seat", now=5, budget=200)
    checks["assembled context within budget"] = (len(ctx) <= 200)
    checks["assembled keeps top memory"] = ("window seat" in ctx)

    print("--- self-test ---")
    for name, ok in checks.items():
        print(f"  {'✓' if ok else '✗'} {name}")
    return 0 if all(checks.values()) else 1

def _demo():
    s, m = Session(), MemoryStore()
    convo = [("My name is Wen and I prefer window seats", 0.7, "chat"),
             ("I'm allergic to peanuts", 0.9, "profile"),
             ("Book me a flight to Tokyo", 0.4, "chat")]
    for turn, (msg, imp, src) in enumerate(convo, 1):
        s.add(f"turn{turn}: {msg}")
        print(f"consolidate -> {m.consolidate(msg, imp, turn, src)}: {msg}")
    s.compact(keep_n=2)
    print("\nretrieve('seat preference'):", [x.text for x in m.retrieve("seat preference", now=3)])
    print("\nassembled context (budget 240):\n" + assemble_context("SYS: travel agent", s, m, "any allergies?", now=3, budget=240))

if __name__ == "__main__":
    sys.exit(selftest()) if "--selftest" in sys.argv else _demo()
