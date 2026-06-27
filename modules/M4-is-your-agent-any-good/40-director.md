# M4 for the 🎯 40-year-old AI Director — Is Your Agent Any Good?

*Goal: make evaluation the core discipline of your AI function — the thing that separates a
trustworthy program from a pile of demos.*

## Plain explanation

Evaluation is the operating discipline ("Evaluation Engineering"). You can't manage what you can't
measure, and agent quality is multi-dimensional: the **Four Pillars** (Effectiveness, Efficiency,
Robustness, Safety) over the **trajectory**, not just final-answer accuracy. The org capability is
a hybrid eval system — automated metrics + LLM-as-a-Judge for scale, humans for the rubric and the
high-stakes calls — feeding a flywheel: Define Quality → Instrument → Evaluate → Feedback Loop.

## Concrete example

The evaluator returns a deterministic verdict *and* a `NEEDS_HUMAN` gate. That division is your
governance model in miniature: automate what's objective, reserve judgment for humans, and never
let a metric auto-approve quality. Scale it: golden datasets owned by domain experts, CI gates on
every change, online monitors that page when quality drifts, and a 48-hour loop from prod failure
to new eval case.

## Hands-on (your team runs it — you read the result)

You don't type this — have an engineer run it in front of you (needs nothing installed) and read the result together:
```bash
cd modules/M4-is-your-agent-any-good/exercise && python3 trajectory_eval.py --selftest
```
Director's lens:
1. **Define quality** for one initiative across the Four Pillars — what's the target for each?
2. **Name the golden set owner** and the rubric author (a domain expert, not the model).
3. **Set the drift alert:** which quality metric, what threshold, who gets paged — and the SLA to
   turn a failure into a golden case.

## Real-world use case

Standing up evaluation as a function: a golden-dataset program, an eval harness in CI, a quality
dashboard separate from the system dashboard, and a feedback loop into the golden set. This module
+ the hub's deterministic [`scripts/check.sh`](../../scripts/check.sh) + the human gates in
[`docs/OBJECTIVES.md`](../../docs/OBJECTIVES.md) are a copyable miniature of that discipline.

## Failure mode

**Confusing activity with quality, and gaming metrics.** Symptoms: a single vanity score, no
golden set, no trajectory evaluation, one dashboard hiding silent degradation, and teams optimizing
the metric instead of the outcome. Plus over-automation — letting an AI judge sign off what needs a
human rubric. The director failure is funding capability without funding its evaluation.

## Measurable output

A one-page **evaluation standard**: the Four-Pillar targets per tier, the golden-set owner + rubric
author, the CI gate, and the drift-alert + failure→golden-set SLA. **Done when** no production agent
runs without continuous trajectory evaluation and a named rubric owner.

## Next step

- Wire evaluation into deployment → **M5 (Production)**: evaluation-gated CI/CD + Observe→Act→Evolve.
- Standardize trajectory logging across teams so every agent is evaluable-by-design.
