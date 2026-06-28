# M4 for the 🛠️ 20-year-old Junior Engineer — Is Your Agent Any Good?

*Goal: build evals that catch judgment failures unit tests can't — trajectory checks, the Four
Pillars, pairwise judging — and wire them into CI.*

## Plain explanation

Traditional `assertEqual` breaks on agents: probabilistic outputs, and "passed 100 unit tests,
still failed in prod." Day 4's method is **Outside-In**: first Black-Box (did the final output
meet the goal?), then Glass-Box (open the trajectory — tool selection, arg formatting,
redundant/missing calls, did it read the tool output, did it terminate). Score the **Four
Pillars** (Effectiveness, Efficiency, Robustness, Safety), and use **pairwise** (A vs B) judging
because it's less biased than single-scoring.

## Concrete example

`evaluate(BAD)` returns `verdict=fail` with `findings=['task NOT met','1 redundant tool call',
"disallowed tool ['weather']", '2 error observations']`. None of that is visible in the final
answer string — it comes from grading the trajectory. And `pairwise(GOOD, BAD)` → `winner: A`.

## Hands-on exercise

```bash
cd modules/M4-is-your-agent-any-good/exercise && python3 trajectory_eval.py --selftest
```
Junior reps:
1. **Add a check:** detect a *missing* required tool (the mission needed a tool that was never
   called); add a self-test using an otherwise-valid run (isolate the rule you're testing).
2. **Score a real run:** capture M1's `(thought, action, observation)` trajectory into the
   `{trajectory, final_answer, expected}` shape and evaluate it.
3. **Make it a regression test:** save GOOD as a golden case; assert future versions still pass
   (this is the Day-4 flywheel: failures → golden set → CI).

## Real-world use case

This is `adk eval` / an LLM-as-a-Judge in miniature: golden eval cases lock a `final_response` +
trajectory; CI re-runs them on every change; an online monitor alerts when a quality score
drifts. The rule-based scorer here is the cheap first filter; an LLM judge is the next layer.

## Failure mode

**Eval pitfalls:** treating a metric (BERTScore 0.8) as ground truth; brittle exact-string
asserts; one dashboard conflating *system* health (latency/errors) with *model* quality; and
**gaming the metric**. Also: letting an automated judge auto-approve subjective quality — keep a
human gate (this evaluator returns `NEEDS_HUMAN` and means it).

## Measurable output

```bash
python3 trajectory_eval.py --selftest && echo PASS
```
**Done when** your new trajectory check passes, you've scored a real M1 run, and GOOD is a golden
regression case. Commit it.

## Next step

- Layer in an LLM-as-a-Judge at `# GO REAL`; keep pairwise + the human gate.
- Then **M5 (Prototype → Production)**: make passing these evals the *gate* that lets a version
  ship (evaluation-gated deployment).
