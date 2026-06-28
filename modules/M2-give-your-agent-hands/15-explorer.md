# M2 for the 🧒 15-year-old Explorer — Give Your Agent Hands

*Goal: turn your agent from a thinker into a doer by building real **tools** — and make them
fail in a *helpful* way instead of crashing.*

## Plain explanation

In M1 your agent could *think* in a loop. But thinking isn't doing. **Tools** are the agent's
hands: search something, send something, calculate something. The trick the pros know: a good
tool comes with a little instruction label called a **contract** — its name, what it needs,
and *what to say when you use it wrong*. Like a vending machine that, instead of eating your
coin, says "put in 50¢ more." A tool that fails helpfully is worth ten that crash.

## Concrete example

A `refund_order` tool needs an order id and an amount. If you call it with the amount as the
word `"ten"` instead of the number `10`, our registry doesn't explode — it replies:
`ERROR: arg 'amount' must be float, got str. Convert it and retry.` The agent reads that and
fixes itself. That's the whole magic of M2.

## Hands-on exercise

```bash
cd modules/M2-give-your-agent-hands/exercise
python3 tool_registry.py            # watch good calls AND helpful errors
python3 tool_registry.py --selftest # get all ✓
```
Now add your own tool: copy `_search_orders`, make `_track_shipment(order_id)` that returns
`"on the truck"`, register it, and add one self-test line. Run again.

## Real-world use case

Every app you love that has "AI" — a shopping helper, a homework helper — is an agent calling
tools exactly like these. The difference between a toy and a real product is whether the tools
have good contracts and fail helpfully. You just built the real version.

## Failure mode

**A tool that crashes or says nothing useful when you call it wrong.** The agent then guesses,
and guesses go bad. Always make your error message say *how to fix it* — that one habit is
what separates pros from beginners.

## Measurable output

```bash
python3 tool_registry.py --selftest   # all ✓, including your new tool's test
```
**You win when** every check is ✓ and your `track_shipment` tool works *and* returns a helpful
error if called wrong.

## Next step

- Easy? → wire this into M1: make your agent loop call tools through the registry.
- Curious how tools talk *between* different AIs? → that's **MCP** (Model Context Protocol),
  the next level up. Peek at [`tools/spec-to-green`](../../tools/spec-to-green/) to see a full
  grown-up contract.
