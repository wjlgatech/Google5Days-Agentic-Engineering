# M1 for the 💼 50-year-old EVP / Executive — Your First Agent Loop

*Goal: 15 minutes to strategic clarity — what an agent actually is, where the value and risk
sit, and the few questions that separate real capability from expensive theater.*

## Plain explanation (no jargon)

An AI agent is software that **pursues a goal in a loop**: it reads the objective, picks a
tool, acts, checks the result, and repeats. The "AI" part (the model) is increasingly a
commodity you rent. Your durable advantage is everything *around* the loop — the proprietary
**tools**, **data/context**, **evaluation**, and **governance**. Translation: *don't buy a
model; build the operating capability that compounds.* (Day 5: building an agent is easy;
trusting it is the work — ~80% of the cost is reliability, security, validation.)

## Concrete example

The same loop that answers "what is 6 × 7 and when is sunset" is, with different tools, what
resolves a customer ticket, reconciles an invoice, or drafts a contract. One pattern, many
P&L lines. The strategic question is never "which model?" — it's *"which workflows, with which
proprietary tools and data, gated by which controls?"*

## Hands-on exercise (yes, you too)

Have someone run this in front of you (or do it — it needs nothing installed):
```bash
cd modules/M1-your-first-agent-loop/exercise && python3 agent_loop.py --selftest   # all ✓ = it provably works
```
Then ask your team **three questions** and watch whether they have crisp answers:
1. *What is our deterministic "all-✓" test for this initiative?* (If none → it's a demo.)
2. *Where is the human approval before anything irreversible?* (Governance.)
3. *How fast does a production failure become a permanent test?* (Compounding vs. decay.)

## Real-world use case

Capital allocation. AI-native competitors compound: every fixed failure makes the next
quarter cheaper (Day 5 Observe→Act→Evolve). Laggards re-buy demos that silently rot. Your job
is to fund the **capability and operating model** (tools + evaluation + governance + the
feedback loop), not a pile of disconnected pilots — and to insist every funded initiative
ships with an eval gate and an owner.

## Failure mode

**Investing in demos instead of operating capability.** Symptoms: no measurable success
metric, no human-in-the-loop control, no monitoring (the "surprise weekend bill" and the
agent "tricked into giving products away" are real Day 5 cautionary tales), and a portfolio of
incompatible agents nobody can govern ("agent sprawl"). The antidote is governance and
evaluation-gating *as a funding condition*, from day one.

## Measurable output

A **one-page investment thesis** for one AI initiative stating: the business metric it moves
(£/$ or time), its deterministic success gate, its governance/HITL control, and its
failure→improvement loop. **Done when** Finance and Risk would both sign it — i.e., value and
control are explicit, not hand-waved. (The toy's `--selftest` is the smallest possible proof
that "done" can be made objective.)

## Next step

- Set the standard: **no AI initiative gets funded without a named success metric + eval gate
  + owner** (Day 4/5 evaluation-gated deployment as policy).
- Have your AI Director walk the **M4 (Quality)** and **M5 (Production)** modules and report
  the operating-model gaps.
- Read the executive summary in the top-level [`README.md`](../../README.md) and the decision
  log in [`memory/decisions/`](../../memory/decisions/) — that's organizational memory
  compounding in practice.
