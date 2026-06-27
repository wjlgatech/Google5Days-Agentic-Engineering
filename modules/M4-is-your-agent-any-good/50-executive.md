# M4 for the 💼 50-year-old EVP / Executive — Is Your Agent Any Good?

*Goal: 15 minutes on the one capability that separates a trustworthy AI program from expensive
theater — **evaluation** — and what to demand before you trust an agent with anything that matters.*

## Plain explanation (no jargon)

The hard part of AI isn't building an agent; it's **trusting** it. Trust comes from evaluation —
continuously measuring whether the agent is actually good, across more than "did it answer." Quality
has four dimensions (does it work · is it efficient · is it reliable · is it safe), and you measure
the *whole decision path*, not just the final reply. An AI can help grade, but **a human writes the
standard** — especially for anything high-stakes. No evaluation = no trust = no business.

## Concrete example

Two agents give similar answers; one did it cleanly, the other broke twice and used a tool it
wasn't allowed to. Only looking at the final answer, they seem equal — and you'd ship a liability.
Evaluating the path, one passes and one fails. That's the difference between a program that compounds
trust and one that quietly degrades until it embarrasses you in front of a customer or regulator.

## Hands-on exercise (yes, you too)

Have someone run this in front of you (nothing to install):
```bash
cd modules/M4-is-your-agent-any-good/exercise && python3 trajectory_eval.py   # GOOD passes (1.0), BAD fails (0.17)
```
Then ask three questions about any AI initiative:
1. *How do we measure "good" — beyond "it answered"?* (the four dimensions)
2. *Who owns the standard for what "good" means?* (a human expert, not the model)
3. *How fast does a real-world failure become a permanent test?* (compounding vs. decay)

## Real-world use case

Capital and risk. AI-native winners fund **evaluation as a discipline**: standards, golden test
sets, continuous monitoring, and a fast loop from failure to fix. Laggards ship demos with no
measurement and inherit silent degradation and incident risk. Your investment should buy the
*evaluation capability*, because that's what makes every other AI dollar trustworthy.

## Failure mode

**Trusting agents you don't measure.** Symptoms: a single vanity metric, no independent standard,
no continuous evaluation, no human sign-off on high-stakes output. Result: an agent that worked in
the demo and silently breaks in production — discovered by a customer, not by you. The antidote is
policy: continuous evaluation + a human-owned quality standard as a condition of trust.

## Measurable output

A one-line **trust gate**: *no agent is trusted with material decisions without continuous
multi-dimensional evaluation and a human-owned quality standard.* **Done when** Risk and the business
owner both sign it.

## Next step

- Have your AI Director produce the **evaluation standard** (M4 · director view) and report coverage.
- Continue to **M5 (Production)**: evaluation becomes the *gate* that lets a version ship — and the
  monitor that keeps it honest after launch.
