# Exercise — run your first agent loop

A complete agent in ~80 lines, **zero dependencies**, no API key. It implements Day 1's
5-step loop literally and prints its own trajectory so you can *see* how an agent thinks.

```bash
# 1) Run it on the built-in mission
python3 agent_loop.py

# 2) Give it your own mission
python3 agent_loop.py "What is 12 * 9, and what time is sunset roughly?"

# 3) Prove it works (this is what scripts/check.sh runs — Day 4 measurable output)
python3 agent_loop.py --selftest    # exits 0 when green
```

## What to notice
- There is **no LLM here on purpose.** An agent is "a system in a loop with tools" — the loop
  and the tools are the engineering; the model is swappable (Day 1).
- The agent keeps a **trajectory** (thought → action → observation). That trajectory *is the
  truth* (Day 4) — quality lives there, not just in the final answer.
- The calculator tool returns an **error that teaches recovery** ("Retry with digits…") — a
  Day 2 tool-contract rule.

## Make it yours (graduated)
1. **Add a tool.** Write `tool_uppercase(s)` and register it in `TOOLS`. Add a self-test
   assertion. Keep it green.
2. **Go real.** Uncomment `think_with_llm` and replace the rule-based planner with a model
   call (Claude/Gemini/etc.). The loop stays identical — that's the lesson.
3. **Break it on purpose.** Make a tool throw; watch the loop stay robust (Day 4 robustness).
