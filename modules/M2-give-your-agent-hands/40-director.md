# M2 for the 🎯 40-year-old AI Director — Give Your Agent Hands

*Goal: make the tool layer a governed, owned asset — because tools (not the model) are where
your proprietary advantage and your biggest risks both live.*

## Plain explanation

A fleet of agents is only as good, safe, and reusable as its **tools**. The model is rented and
commoditized; your **tools + the data they touch** are the moat and the liability. So tools need
the same governance as services: an owner, a contract, validation, idempotency classification,
permissions, and observability. Day 2's "publish tasks, not API calls" is also an org principle —
a registry of *capabilities*, not a tangle of point integrations ("agent sprawl").

## Concrete example

The exercise registry validates every call against a contract and flags `refund_order` as
non-idempotent. Scale that mental model: a central **tool/agent registry** where each tool has a
named owner, a typed contract, a permission scope, and a risk class — so a new agent *composes
approved tools* instead of re-wrapping the same API five insecure ways. MCP is the
interoperability standard that makes this reuse real (the "do this specific thing" protocol).

## Hands-on exercise

```bash
cd modules/M2-give-your-agent-hands/exercise && python3 tool_registry.py --selftest
```
Director's lens:
1. **Inventory:** list your org's top 10 agent tools; mark each task-shaped vs. thin-wrapper,
   owned vs. orphan, idempotent vs. not. Gaps = your roadmap.
2. **Set the contract standard:** mandate the 8-field contract
   ([`schemas/tool.schema.json`](../../schemas/tool.schema.json)) for any tool used in production.
3. **Name the high-risk sinks** (refunds, sends, deletes) that require human-in-the-loop approval.

## Real-world use case

Standing up a governed agent platform: a tool registry with ownership + contracts + permissions,
an MCP gateway for interoperability, and HITL gates on irreversible actions. This module +
[`schemas/`](../../schemas/) + [`tools/`](../../tools/) are a copyable miniature of that
capability layer.

## Failure mode

**Ungoverned tool sprawl.** Dozens of overlapping, unowned, over-privileged tools → security
holes (confused-deputy, over-broad scopes), duplicated work, and trapped knowledge. Plus
**trusting MCP defaults**: it standardizes the interface but leaves enterprise auth/identity/
observability to you. Govern from day one or pay later.

## Measurable output

A one-page **tool-governance standard**: the required contract, the permission/risk classification,
the HITL list, and the registry owner. **Done when** no production tool ships without an owner +
8-field contract, and a non-compliant tool is blocked in CI (the deterministic version of this
policy — like `tool_registry.register()` rejecting a bad contract).

## Next step

- Operationalize quality of tool *use* → **M4 (Agent Quality)**: evaluate tool selection and
  arg-formatting in the trajectory.
- Plan interoperability at scale → **M5 (Production)**: MCP vs. A2A, gateways, registries.
