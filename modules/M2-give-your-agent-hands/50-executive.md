# M2 for the 💼 50-year-old EVP / Executive — Give Your Agent Hands

*Goal: 15 minutes on why **tools**, not models, are where AI value and AI risk actually live —
and what to demand before you fund an agent that can *act*.*

## Plain explanation (no jargon)

An agent that only talks is a chatbot. An agent that **acts** — issues refunds, sends emails,
updates records — creates real value *and* real liability. Those actions are "tools," and each
needs a **contract**: what it does, what it's allowed to do, and a human checkpoint for anything
irreversible. The model is rented; your **proprietary tools + the data they touch are the moat.**
Fund the hands and the controls, not another brain.

## Concrete example

A `refund_order` tool is flagged "not safe to auto-retry" — because a retry could double-refund a
customer. That one flag is the difference between a controlled system and a weekend incident.
Now picture every action your agents can take, each with — or without — that kind of guardrail.
The Day-5 cautionary tales are real: agents tricked into giving products away, or running up
surprise bills, because tools had no contracts and no limits.

## Hands-on exercise (yes, you too)

Have someone run this in front of you (needs nothing installed):
```bash
cd modules/M2-give-your-agent-hands/exercise && python3 tool_registry.py --selftest   # all ✓
```
Then ask three questions about any agent initiative:
1. *Which tools can this agent use, and who owns each one?*
2. *Which actions are irreversible, and where's the human approval?*
3. *Are these tools reused across the company, or rebuilt (insecurely) each time?*

## Real-world use case

Capital allocation again: AI-native winners build a **governed library of tools** their agents
compose; laggards let every team wire fragile, over-privileged integrations. The first compounds
and stays safe; the second sprawls into risk and rework. Your investment should buy the *capability
layer* (tools + contracts + governance), which is reusable, not one-off demos.

## Failure mode

**Funding agents that can act without governing what they can do.** Symptoms: no tool owners, no
permission limits, no human gate on irreversible actions, the same integration rebuilt five ways.
Result: security incidents, surprise costs, and trapped value. The antidote is policy: a contract
+ owner + risk class for every production tool, and human approval on high-stakes actions.

## Measurable output

A one-line **funding gate**: *no agent that can take irreversible action is funded without a tool
contract, a named owner, and a human-in-the-loop checkpoint.* **Done when** Risk and the business
owner both sign it — controls and value made explicit, not assumed.

## Next step

- Have your AI Director produce the **tool-governance standard** (M2 · director view) and report
  gaps.
- Continue to **M4 (Quality)** and **M5 (Production)** for the assurance and last-mile operating
  model that make funded agents trustworthy at scale.
