# M4 for the 🧒 15-year-old Explorer — Is Your Agent Any Good?

*Goal: become a judge. Learn to tell a *lucky* answer from a *good* one — by watching how the
agent got there, not just what it said.*

## Plain explanation

Imagine grading a math test. A kid writes "42" — correct! But did they *solve* it, or copy the
kid next to them? In AI, the "working out" is called the **trajectory** — every step the agent
took. Day 4's big idea: **the trajectory is the truth.** An agent can give a right-looking
answer the totally wrong way (used a forbidden tool, guessed, got lucky). A good judge checks
the *path*, not just the last line.

## Concrete example

Two agents both "answer" the same question. Agent A: calculator → 42 → done. Clean. Agent B:
breaks twice, secretly uses a weather tool it wasn't allowed, then mumbles an answer. Same-ish
final words, totally different quality. Our evaluator scores A as **pass** and B as **fail** —
because it read the trajectory.

## Hands-on exercise

```bash
cd exercise
python3 trajectory_eval.py            # watch GOOD score 1.0 and BAD score 0.17
python3 trajectory_eval.py --selftest # all ✓
```
Look at the `findings` for the BAD run — it literally lists what went wrong. Then notice the
`NEEDS_HUMAN` line: the computer refuses to decide if an answer is *nicely written* — that's a
human's call.

## Real-world use case

This is how the good AI apps stay good: they keep grading their agents' trajectories so a broken
one gets caught *before* it reaches you. The apps that don't grade quietly get worse over time
and nobody notices until it's bad.

## Failure mode

**"It answered, so it's good."** Nope. A confident wrong answer is the most dangerous kind. Always
ask *how* did it get there — and never let the computer decide the stuff that needs human taste.

## Measurable output

```bash
python3 trajectory_eval.py --selftest   # all ✓ (good passes, bad fails, pairwise picks the winner)
```
**You win when** every check is ✓ and you can explain *why* the BAD run failed by reading its
findings.

## Next step

- Try grading a *real* run: copy the step-list your M1 agent prints and feed it in.
- Curious how pros compare two answers fairly? → it's called **pairwise judging**; read the
  20-junior version. Then move to **M5** (shipping it for real).
