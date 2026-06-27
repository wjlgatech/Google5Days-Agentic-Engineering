# M5 for the 🏗️ 30-year-old Senior Engineer — Ship It Without Breaking It

*Goal: architect AgentOps — the evaluation-gated pipeline, safe-rollout strategy, externalized
state, observability, and the evolve loop — for systems that are autonomous, stateful, and
non-deterministic.*

## Plain explanation

Agents break DevOps assumptions: dynamic execution paths, persistent state, emergent behavior. So
AgentOps adds three pillars — automated evaluation, automated CI/CD, and observability — plus
interoperability (MCP for tools, A2A for agent-to-agent). The load-bearing principle is
**evaluation-gated deployment** on top of a **shift-left funnel** (cheap pre-merge checks → heavy
post-merge staging → gated prod), with **safe rollout** (canary/blue-green/flags) and
**idempotent, safe-to-retry tools**.

## Concrete example

`deploy_gate.py` composes M4's evaluator as the gate, then canary, then a human sign-off — each a
stop point. In production this maps to: stateless containerized agent (Cloud Run / Agent Engine)
with **externalized state** (sessions/memory in a managed store, per M3), retries with backoff,
IaC (Terraform) for identical envs, GitOps (every deploy a commit, every rollback a revert), and
OpenTelemetry traces feeding online quality monitors.

## Hands-on exercise

```bash
cd modules/M5-ship-it-without-breaking-it/exercise && python3 deploy_gate.py --selftest
```
Senior moves:
1. **Funnel phases:** split `gate` into pre-merge (fast subset) vs post-merge (full suite + load
   test); test each independently.
2. **Idempotency enforcement:** block promotion if the candidate uses a non-idempotent tool in a
   retry-able path (tie to M2's `idempotent` flag).
3. **Observability hook:** emit a structured deploy record (version, verdicts, trace ids) and
   define the drift alert that auto-triggers an `evolve()`.

## Real-world use case

Standing up an agent platform: stateless runtime + externalized state, an eval-gated CI/CD funnel,
a registry for tools/agents, A2A for multi-agent composition, and an Observe→Act→Evolve loop that
turns prod telemetry into golden cases within hours. Senior calls: MCP vs A2A boundaries, where to
spend the latency/cost budget, what to canary vs. blue-green, how to make rollback instant.

## Failure mode

**Treating agents like static microservices.** Symptoms: no eval gate (silent regressions),
synchronous state on the hot path, non-idempotent tools double-applying on retry, security as a
one-time checklist (prompt injection, memory poisoning, confused-deputy), and a slow evolve loop
that makes production insight worthless. Plus **agent silos** — incompatible frameworks that can't
collaborate (that's what A2A solves).

## Measurable output

```bash
python3 deploy_gate.py --selftest   # + your funnel phases, idempotency block, and evolve hook green
```
**Done when** the pipeline is a real funnel, state is externalized, tools are idempotent where
retried, deploys/rollbacks are GitOps, and the evolve loop is automated with drift alerts.

## Next step

- Add A2A/MCP boundaries + a registry as you scale past a single agent.
- You've completed all 5 days — wire M4+M5 as the standing gate for every agent your team ships.
