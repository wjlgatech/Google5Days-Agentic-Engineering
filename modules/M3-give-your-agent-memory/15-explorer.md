# M3 for the 🧒 15-year-old Explorer — Give Your Agent Memory

*Goal: make your agent remember you between messages — and learn why "remember everything" is
actually a trap.*

## Plain explanation

Here's a weird secret: an AI model has **no memory at all**. Every time it answers, it only
sees what you hand it right then. So "memory" is something *you build around it*. Two kinds:
the **session** (what was just said — like short-term memory) and **long-term memory**
(important facts saved for later, like "I prefer window seats"). The skill is handing the model
*just the right stuff* — not too little, not too much. Too much and it gets distracted (that's
called **context rot**), like trying to study with 40 browser tabs open.

## Concrete example

You tell the agent "I'm allergic to peanuts." That's important → it gets saved as a memory
*with a label* (where it came from). Ten messages later you ask "is this snack ok?" — the agent
pulls that one memory back out and warns you. It didn't keep all 10 messages; it kept the *one
that mattered*.

## Hands-on exercise

```bash
cd modules/M3-give-your-agent-memory/exercise
python3 context_manager.py            # watch it save, summarize, and recall
python3 context_manager.py --selftest # all ✓
```
Then read the "real limitation" note in this folder's README and **fix it**: make the matcher
treat `seat` and `seats` as the same word. Re-run the demo — recall gets smarter.

## Real-world use case

This is why a good AI assistant remembers your name and preferences across days, but a basic
chatbot forgets you the second you close the tab. The ones that feel "smart" aren't smarter
models — they have better *memory engineering*.

## Failure mode

**Stuffing everything into the agent's head.** More isn't better — past a point the model loses
focus and gives worse answers (context rot). The fix is to *summarize old stuff* and *only pull
the few memories that matter* for this question.

## Measurable output

The real proof here is the **demo line**, not the self-test (the self-test is green either way —
it doesn't yet check this). Run the demo before and after your fix and watch the top hit change:
```bash
python3 context_manager.py | grep "seat preference"
# BEFORE your fix:  top hit is "I'm allergic to peanuts"   ← wrong
# AFTER  your fix:  top hit is "...I prefer window seats"   ← the seat memory wins
```
**You win when** that top hit flips to the seat memory. Then make it *stick* — add a check to
`selftest()` that builds its own plural-"seats" memory so it actually tests stemming:
```python
ms = MemoryStore()
ms.consolidate("User loves window seats", 0.5, 1, "chat")
ms.consolidate("Allergic to peanuts", 0.9, 1, "profile")
checks["seat≈seats recall"] = "seats" in ms.retrieve("seat preference", now=2)[0].text
```
Without your fix this check is ✗ (the peanut memory wins on importance); with it, ✓. Now your
fix is *guarded by a green check* — not just something you saw once.

## Next step

- Curious how the agent decides what's worth remembering? → that's **consolidation**; read the
  20-junior version.
- Want it to *know facts about the world* too (not just about you)? → that's **RAG**, coming in
  later modules. Then move to **M4** (is the agent any good?).
