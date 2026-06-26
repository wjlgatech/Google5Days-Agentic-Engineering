# M1 for the 🧒 15-year-old Explorer — Your First Agent Loop

*Goal: build a real AI-style agent and watch it think — in about 10 minutes, no setup, no
account, no money.*

## Plain explanation (what's going on)

An "agent" sounds fancy. It isn't. An agent is just a **loop**: it reads a mission, looks at
what it has, picks a **tool**, uses it, looks at the result, and repeats until the job's done.
Like beating a video-game level: *see the room → pick a weapon → swing → see what happened →
go again.* The AI "brain" is swappable — the loop is the real machine. (Google's Day 1 paper
literally says an agent is "a system in a loop with tools to accomplish an objective.")

## Concrete example

You ask: *"What is 6 × 7, and when is sunset?"* The agent thinks "there's math here" → uses a
**calculator tool** → gets `42` → thinks "they also asked about sunset" → uses a **sunset
tool** → gets a time → stitches them into one answer. Two tools, one loop. You'll watch it
print each step.

## Hands-on exercise (do this now)

```bash
cd exercise
python3 agent_loop.py "What is 8 * 9, and what time is sunset roughly?"
```
You'll see lines like `🧠 thought … 🔧 calculator('8 * 9') -> 72`. **That printout is the
agent thinking out loud.** Now make it smarter: open `agent_loop.py`, copy the calculator
tool, and make a `tool_shout` that returns text in CAPS. Add it to the `TOOLS` list. Run again.

## Real-world use case

This exact loop is how a coding assistant fixes your bug (tool = "edit file", "run tests"),
how a travel bot books a trip (tool = "search flights"), how a game NPC decides what to do.
Different tools, *same loop you just ran.*

## Failure mode (the trap)

**Giving the agent no way to check itself.** If a tool breaks and the agent doesn't notice, it
keeps going confidently — wrong. Notice how our calculator returns an *error message that
tells the agent how to fix its input* instead of crashing. Good tools fail loudly and helpfully.

## Measurable output (your proof)

```bash
python3 agent_loop.py --selftest   # prints ✓/✗ for each check; you want all ✓
```
**You succeeded when:** the self-test is all ✓ *and* your new `tool_shout` works. That green
check is your trophy — a thing that *proves* it works, not just "looks like it works."

## Next step

- Did that feel easy? → Add a third tool and a self-test line for it, keep it green.
- Want the AI brain? → Read the `think_with_llm` comment at the bottom of the file; that's how
  you plug in a real model next. Then come back for **M2 (tools)**.
- Tell a friend what an "agent loop" is in one sentence. If you can, you *get* it.
