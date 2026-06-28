# M1 for the 🛠️ 20-year-old Junior Engineer — Your First Agent Loop

*Goal: understand the agent loop well enough to read, debug, and extend one — the same
control flow you'll meet in every agent framework (ADK, LangGraph, CrewAI).*

## Plain explanation

An agent = **Model + Tools + Orchestration + Runtime**, run in a loop (Day 1's anatomy). The
*orchestration layer* is just a control loop: assemble context → call the planner → execute a
tool → append the observation → repeat. Strip the LLM away and you can see the skeleton
clearly — which is exactly what the exercise does, so you debug the *engineering*, not the
model's mood.

## Concrete example

`agent_loop.py` runs `think → act → observe` and stores each step as a
`(thought, action, observation)` tuple — that list is the agent's **short-term memory / session**
(Day 3). The final answer is just the concatenation of observations. When something's wrong,
you don't guess — you read the trajectory and see the exact step that broke.

## Hands-on exercise

```bash
cd modules/M1-your-first-agent-loop/exercise    # from the repo root
python3 agent_loop.py --selftest        # green baseline
```
Now practice the real junior-engineer skill — **debugging via the trajectory**:
1. Break the regex in `think()` — change `\d+` to `\d\d+` (now it only matches *multi-digit*
   numbers, so the single-digit `6 * 7` mission no longer matches). Re-run. Watch `calculator
   used` and `answer has 42` go ✗.
2. Read the printed trajectory: *which step* produced the bad observation? (The calculator
   rule never fired — the mission fell straight through to the sunset rule.)
3. Fix it. Re-run to green. You just did root-cause debugging on an agent.

Then **add a tool** (`tool_wordcount`) — three edits: write it, register it in the `TOOLS`
*dict* with a key (`"wordcount": tool_wordcount`), and add a rule in `think()` so the planner
actually selects it (a tool with no rule never runs — see the `YOUR TURN` comment). Prove it
with its own self-test assertion in `selftest()`.

## Real-world use case

This is the inner loop of a coding agent: tools are `read_file`, `edit`, `run_tests`; the
planner decides the next action; the loop continues until tests pass. Your day job with
coding agents *is* steering this loop — giving good missions, good tools, and reading the
trajectory when it stalls.

## Failure mode

**`output == expected` unit tests on a probabilistic system** (Day 1 anti-pattern). A model
may phrase the same correct answer ten ways. Test *behavior and trajectory* (did it call the
right tool with valid args?), not exact strings. Notice our self-test checks "calculator was
used" and "answer contains 42" — properties, not a brittle full-string match.

## Measurable output

```bash
python3 agent_loop.py --selftest && echo "PASS"
```
**Done when:** all self-tests pass, your new tool has a passing assertion, and you can point
at the exact trajectory step for any failure. Commit it — green check = shippable.

## Next step

- Swap the rule-based `think()` for a real model call (`think_with_llm` stub). Keep the tool
  contracts identical; observe that the loop is unchanged. → bridges to **M2 (Agent Tools)**.
- Learn to read traces properly before scaling up → **M4 (Agent Quality)**: the trajectory is
  the truth.
- Habit to build now: *write the check first, then make it green* — see
  [`tools/spec-to-green`](../../tools/spec-to-green/).
