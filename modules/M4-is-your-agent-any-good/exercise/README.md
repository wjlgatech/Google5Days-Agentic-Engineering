# Exercise — is your agent any good?

A real trajectory evaluator in ~150 lines, **zero dependencies**. It scores an agent run the
Day-4 way: Outside-In, across the Four Pillars, with pairwise judging — and it refuses to
self-certify the parts only a human should judge.

```bash
python3 trajectory_eval.py             # score a GOOD run and a BAD run, then pick a winner
python3 trajectory_eval.py --selftest  # prove it works (what scripts/check.sh runs)
```

## What to notice
- **Outside-In:** it first checks *task success* (did the final answer contain what was
  expected?), then opens the **Glass-Box** to see *why* — tool choice, arg validity, redundancy,
  termination, safety.
- **The trajectory is the truth:** the BAD run "answers" but fails — because the *path* shows
  repeated errors, a redundant call, and a disallowed tool. The final line alone would have
  hidden that.
- **Pairwise > single-score:** comparing GOOD vs BAD and picking a winner is more reliable than
  scoring each in isolation (it cancels judge bias).
- **The human gate:** every result carries `NEEDS_HUMAN: is the answer well-judged/clear?` — the
  evaluator *never* answers that. Day 4: "an AI can help grade the test, but a human writes the
  rubric."

## Make it yours
1. **Score a real run:** capture a trajectory from M1's `agent_loop.py` (the `(thought, action,
   observation)` list) into the `{trajectory, final_answer, expected}` shape and evaluate it.
2. **Add a pillar check:** penalize a "missing tool call" (the mission needed a tool that was
   never used); add a self-test.
3. **Go real:** at `# GO REAL`, swap the rule-based scorer for an LLM-as-a-Judge — pass the
   trajectory + a human-written rubric to a model for per-pillar scores. Keep the human gate.

## The trap this exercise teaches
A run can produce a confident final answer and still be **wrong or unsafe**. "It answered" is
not "it's good." Always grade the *trajectory*, and never let a metric (or a model) auto-approve
the judgment calls a human owns.
