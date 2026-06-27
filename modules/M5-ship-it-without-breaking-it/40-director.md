# M5 for the 🎯 40-year-old AI Director — Ship It Without Breaking It

*Goal: stand up AgentOps as the operating model that gets agents safely to production and keeps
them trustworthy — the last mile where most AI programs stall.*

## Plain explanation

Most agent projects die in the **last mile**: not the model, but the operational discipline to
deploy, secure, and continuously validate an autonomous system. That discipline is **AgentOps** —
evaluation-gated deployment, a CI/CD funnel, safe rollout, observability, and a fast loop from
production failure to fix. The operating principle: no version ships without passing eval, and
every failure becomes tomorrow's test.

## Concrete example

The deploy gate composes evaluation (M4) → canary → human sign-off, and `evolve()`s failures into
golden cases. Scale that into an operating model: a release pipeline every team uses, safe-rollout
standards (canary %, rollback SLA), an observability standard (logs/traces/metrics), security
embedded from day one (three-layer defense, guardrails, secrets in a vault), and a 48-hour SLA
from prod failure to new eval case.

## Hands-on exercise

```bash
cd modules/M5-ship-it-without-breaking-it/exercise && python3 deploy_gate.py --selftest
```
Director's lens:
1. **Readiness map:** for one initiative, mark which of the AgentOps pillars (eval, CI/CD,
   observability, security) exist and which are gaps.
2. **Set the rollout standard:** canary %, rollback trigger/SLA, and who holds the prod sign-off.
3. **Close the loop:** define the failure→golden-set SLA and who owns it. A six-month fix loop
   means production insight rots.

## Real-world use case

Operationalizing agents across teams: a shared eval-gated pipeline, IaC for reproducible envs, a
tool/agent registry, A2A for cross-team agent collaboration, and an Observe→Act→Evolve loop wired
to monitoring. This module + [`scripts/check.sh`](../../scripts/check.sh) + the human gates in
[`docs/OBJECTIVES.md`](../../docs/OBJECTIVES.md) are a copyable miniature of that operating model.

## Failure mode

**Underestimating the last mile.** Symptoms: demos that never reach production; no eval gate (silent
degradation); no monitoring (surprise costs, the "weekend bill"); guardrail gaps (an agent tricked
into giving products away); and agent sprawl that can't be governed or composed. The director
failure is funding capability without funding the operating model that makes it safe to ship.

## Measurable output

A one-page **AgentOps operating standard**: the eval gate, the CI/CD funnel, the rollout + rollback
SLA, the observability + security baseline, the prod sign-off owner, and the failure→golden-set SLA.
**Done when** no agent reaches production outside this pipeline.

## Next step

- Drive the readiness map → fund the gaps (most programs are missing eval + observability).
- You've completed all 5 days — the hub is now a copyable operating model from learning to
  production. Run the [loop](../../loop/README.md) on a real initiative.
