# M2 for the 🏗️ 30-year-old Senior Engineer — Give Your Agent Hands

*Goal: treat the tool boundary as the most security- and reliability-critical seam in an agent,
and design a tool layer your org reuses without re-litigating it each time.*

## Plain explanation

The tool layer is where a probabilistic planner touches real systems — so it's where you put
**deterministic** enforcement: schema validation, allow-lists, idempotency, least-privilege.
Day 2's design rules (task-shaped, granular, concise outputs, schema-validated, recovery-teaching
errors) aren't style — they're the contract that lets you reason about blast radius. The
registry here is a minimal reference: validation is at the boundary, not in the prompt.

## Concrete example

`refund_order` is registered `idempotent=False` — a deliberate signal that retry logic must not
blindly replay it (Day 5: non-idempotent tools cause duplicate charges). Validation runs before
dispatch, so a malformed model call is a *handled error*, not a side effect. That's the seam:
everything past `registry.call` is testable, allow-listed, and typed.

## Hands-on exercise

```bash
cd exercise && python3 tool_registry.py --selftest
```
Senior moves:
1. **Allow-list + least privilege:** add a `permissions` field per tool; deny a call the caller
   isn't authorized for (model Day 1's `before_tool_callback`).
2. **Idempotency keys:** make `refund_order` reject a duplicate `(order_id, key)` — prove a retry
   is safe.
3. **Output discipline:** cap a tool's output size and return a handle instead of a blob (Day 2:
   don't swamp context). Test the cap.

## Real-world use case

This is the shape of an **MCP** server and of a Gemini/ADK function-tool layer: discovery
(`tools/list`), validated dispatch (`tools/call`), structured results/errors. Knowing the bare
registry lets you evaluate MCP's enterprise gaps (auth, identity propagation, observability,
tool-shadowing/confused-deputy) and decide what to layer on — a senior call, not a vendor's.

## Failure mode

**Trusting the model (or an untrusted MCP server) at the boundary.** Prompt injection, tool
shadowing, dynamic capability injection, and "annotations are hints, not guarantees" all live
here. The architectural failure is putting validation in the system prompt instead of in
deterministic code at the dispatch point. Defense-in-depth: hard checks *around* model judgment.

## Measurable output

```bash
python3 tool_registry.py --selftest   # + your permission, idempotency, and output-cap tests green
```
**Done when** the boundary is fully deterministic: every tool is allow-listed, typed, size-capped,
and its idempotency is explicit — and a malformed/unauthorized call is a tested error path.

## Next step

- Standardize it → adopt the 8-field [`schemas/tool.schema.json`](../../schemas/tool.schema.json)
  org-wide; make every shared tool ship `contract.json` like [`tools/spec-to-green`](../../tools/spec-to-green/).
- Then **M3 (Context Engineering)**: state, sessions, and memory — and their isolation/PII seams.
