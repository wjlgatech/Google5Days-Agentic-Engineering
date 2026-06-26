# M4 for the 🏗️ 30-year-old Senior Engineer — Is Your Agent Any Good?

*Goal: make quality an architectural pillar — instrument for it from line one, and design an
eval system that mixes deterministic gates, scalable AI judges, and human rubric ownership.*

## Plain explanation

Quality isn't a test phase; it's "evaluable-by-design." You instrument the agent to emit a
structured trajectory (plan, tool calls, args, observations, state changes) and build evaluation
as a first-class subsystem: Black-Box task success + Glass-Box trajectory scoring across the
**Four Pillars**, with a hybrid of cheap automated metrics → LLM-as-a-Judge → human review.
Pairwise comparison reduces judge variance. The verdict is deterministic; the rubric is human.

## Concrete example

The evaluator separates a deterministic gate (`verdict = pass/fail` from task-success + safety +
termination + overall threshold) from the `NEEDS_HUMAN` gate (subjective quality). That seam is
the design: CI can block on the deterministic part; humans own the rubric. In production this
extends to trace-based scoring (OpenTelemetry spans → an Agent-as-a-Judge over the trace) and
online monitors that alert when a quality score drifts below baseline.

## Hands-on exercise

```bash
cd exercise && python3 trajectory_eval.py --selftest
```
Senior moves:
1. **Trajectory adherence:** add a check that the agent followed a required plan order (e.g. must
   retrieve before it answers — ties to M3); test it on an isolated valid run.
2. **Sampling policy:** make evaluation dynamic — score 100% of failures, 10% of successes (cost
   vs. coverage); justify the ratio.
3. **Two dashboards:** separate System metrics (latency P50/P99, error rate, tokens/cost) from
   Quality metrics (task success, trajectory adherence, hallucination rate) — never one number.

## Real-world use case

This is the eval harness behind a real agent platform: golden datasets (typical/edge/adversarial),
CI regression on every change, trace-based diagnosis, and a feedback loop that turns prod failures
into new golden cases within hours. Senior calls: where deterministic checks suffice vs. where you
need a judge; how to bound eval cost; how to keep judges from being gamed.

## Failure mode

**Silent degradation** (200 OK, plausible-but-wrong) and **judge pitfalls**: trusting a single
metric as truth, inter-annotator disagreement treated as ground truth, verbose logging that adds
prod overhead, and conflating system health with model quality. Architectural failure: bolting
eval on at the end instead of instrumenting for it from the start.

## Measurable output

```bash
python3 trajectory_eval.py --selftest   # + your adherence check and sampling logic green
```
**Done when** the agent emits a structured trajectory, the deterministic gate runs in CI, the
human rubric is explicit, and system vs. quality metrics are separated with drift alerts.

## Next step

- Add an LLM/Agent-as-a-Judge over real traces; measure judge agreement with humans.
- Then **M5 (Production)**: wire these evals as the deployment gate + the Observe→Act→Evolve loop.
