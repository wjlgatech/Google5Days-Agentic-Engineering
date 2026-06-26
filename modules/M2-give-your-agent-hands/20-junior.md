# M2 for the 🛠️ 20-year-old Junior Engineer — Give Your Agent Hands

*Goal: write tools an agent (and your teammates) can actually rely on — task-shaped,
schema-validated, with errors that drive recovery. This is the daily craft of agent work.*

## Plain explanation

A tool = a function **+ a contract**. Day 2's rules: *publish tasks, not API calls*; keep tools
**granular** (single responsibility); validate inputs against a **schema**; and write **errors
that teach recovery** (the error goes back to the model, so "invalid input" is useless —
`"amount must be float, got str. Convert it and retry."` is gold). The registry in this
exercise enforces all of that at call time.

## Concrete example

`registry.call("refund_order", {"order_id": "x", "amount": "ten"})` returns a teaching error
instead of throwing, because the registry checks the contract's types first. Compare that to a
thin wrapper over a 40-parameter enterprise API — the model can't choose correctly and every
failure is a stack trace. Task-shaped + validated is the difference.

## Hands-on exercise

```bash
cd exercise && python3 tool_registry.py --selftest
```
Junior reps:
1. **Add validation:** make `refund_order` reject `amount <= 0` with a teaching error; add a
   test. (Validation lives in the tool, not the prompt.)
2. **Add a tool** `track_shipment(order_id)` with a full contract + test.
3. **Integrate:** import `build_registry()` into M1's `agent_loop.py` and route actions through
   `registry.call(...)`. Your agent now has *validated* hands; the loop is unchanged.

## Real-world use case

This is exactly how you expose capabilities to a coding agent or a customer-support agent:
each tool is one task with a typed contract, and the model self-corrects from your error
messages. Same shape as an **MCP** server's `tools/call` (name + validated args + structured
result or `isError`). Learn it here, recognize it everywhere.

## Failure mode

**Returning huge blobs or cryptic errors.** Giant outputs swamp the context window and persist
in history (cost + "context rot"); cryptic errors waste the model's chance to recover. Keep
outputs concise; make every error actionable. Also avoid the "mega-tool" that does five things.

## Measurable output

```bash
python3 tool_registry.py --selftest && echo PASS
```
**Done when** your new tool + validation tests pass, errors are all recovery-teaching, and (bonus)
the M1 loop runs through the registry. Commit it.

## Next step

- Formalize it → read [`tools/spec-to-green`](../../tools/spec-to-green/): the full 8-field
  contract + `prompt.md` that ports across Claude/Codex/Hermes/Gemini.
- Then **M3 (Context Engineering)**: now that your agent can *act*, give it *memory*.
