# M2 — Give Your Agent Hands (Agent Tools)

> The second module. M1 gave your agent a **loop**; M2 gives it **hands** — tools. The Day-2
> lesson in one line: *a tool is not just a function, it's a function **plus a contract**.*
> Conforms to [`schemas/module.schema.json`](../../schemas/module.schema.json); gated by
> [`scripts/check.sh`](../../scripts/check.sh) (O4/O10).

**Loop stage owned:** ③ Specification → ④ Execute &nbsp;·&nbsp; **Source:** Day 2 (Agent Tools & MCP).

**What you can do after this module:** write a task-shaped tool, give it the 8-field contract,
validate its inputs, and return errors that teach an agent how to recover — at your level.

## Plug in at your level

| You are… | Start here |
|---|---|
| 🧒 ~15, curious | [`15-explorer.md`](15-explorer.md) |
| 🛠️ ~20, junior engineer | [`20-junior.md`](20-junior.md) |
| 🏗️ ~30, senior engineer | [`30-senior.md`](30-senior.md) |
| 🎯 ~40, AI director | [`40-director.md`](40-director.md) |
| 💼 ~50, EVP / executive | [`50-executive.md`](50-executive.md) |

## The artifact

[`exercise/tool_registry.py`](exercise/) — a real, zero-dependency tool registry that
**validates a call against the tool's contract before running it** (a deterministic gate), and
returns recovery-teaching errors. Run `python3 tool_registry.py --selftest`.

## The mental model

```
  a TOOL = task-shaped function  +  CONTRACT (name · description · typed params · recovering errors)
  the REGISTRY validates the call ──▶ valid? run it.   invalid? return an error that says how to fix.
```

The 8 contract fields you'll meet again everywhere (the same ones every tool in
[`tools/`](../../tools/) ships): **purpose · inputs · outputs · when-to-use · when-NOT ·
workflow · validation · failure-handling**. M2 is where you learn *why* each field exists.

Prereq: [M1 · Your First Agent Loop](../M1-your-first-agent-loop/). Next: M3 (Context
Engineering — give your agent *memory*).
