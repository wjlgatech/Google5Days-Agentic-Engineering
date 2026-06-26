# From Prompt to Proof: A Runnable School for the Evaluated Loop

*How a stack of five Google whitepapers became a school you can actually run — one that teaches
a 15-year-old and an AI director from the same files, and proves it works on every save.*

---

## The $40 billion magic trick that keeps failing

Here's a number that should stop you cold. In 2025, MIT's NANDA initiative studied 300 enterprise
AI deployments and found that **95% of them delivered no measurable return** — despite $30–40
billion spent.[^mit] Not because the models were dumb. The models were fine. They failed the way
a brilliant new hire fails on their first Tuesday: they didn't know *where the work actually
breaks*.

MIT had a name for it: the **learning gap**. Brittle workflows, weak context, models that ace the
demo and faceplant when the data feed is late.

Now here's the twist. The job created to close that gap is the **fastest-growing role in AI**:
the **Forward Deployed Engineer (FDE)** — postings up **1,165% year-over-year**, base pay at
Palantir running **$171K–$295K**.[^fde][^levels] An FDE embeds with real users, watches reality
bite, and turns what they learn into software that survives contact with Tuesday.

And — as William Wu, PhD argues in the piece that sparked this project — **that job has no
school.**[^wu] You can't major in "knowing what to build, where it breaks, and how to prove it
helps."

So we built one. This repo is that school. And it's not a PDF — **you run it.**

---

## The one idea: the unit of work moved from the *prompt* to the *evaluated loop*

If you remember one sentence, make it Wu's:

> **"The model is becoming cheaper. Deployment intelligence is becoming more valuable."**[^wu]

Think about how you used AI a year ago: you typed a clever prompt and hoped. That's the old unit
of work — a one-off magic spell. It doesn't compound, can't be tested, and rots the moment the
model or the data changes.

The new unit of work is **the evaluated loop**: a versioned, tested artifact that *observes
reality, acts, checks itself, and learns* — over and over. Same shape an FDE lives:
**Deploy → Observe → Build → Validate → Productize → Repeat.**[^wu]

**For the 15-year-old:** it's the difference between getting a *lucky* answer on a test and
actually learning to *solve the problem* — so you can do it again next week, harder.

**For the AI director:** it's the difference between a pile of demos (the 95%) and a compounding
capability (the 5%). The thing you can govern, measure, and trust isn't a prompt. It's a loop with
a gate on it.

That's the whole bet of this hub.

---

## Where the curriculum comes from (so it isn't vibes)

In 2026 Google published five "5-Day Agentic Engineering" whitepapers — a clean, expert map of
how real agents get built and trusted.[^g1][^g4][^g5] We didn't summarize them. We **compiled them
into one loop** and made each day a runnable module:

| Day | What it teaches | The hub module (runs in your terminal) |
|---|---|---|
| 1 · Introduction to Agents | an agent is *"a loop with tools to accomplish a goal"* | **M1** — run a real agent loop |
| 2 · Agent Tools | a tool is a function **+ a contract** | **M2** — a tool registry that validates calls |
| 3 · Context Engineering | sessions (now) + memory (across time) | **M3** — a context manager that beats "context rot" |
| 4 · Agent Quality | *"the trajectory is the truth"* — grade the path, not the answer | **M4** — a trajectory evaluator |
| 5 · Prototype → Production | **evaluation-gated deployment** | **M5** — a deploy gate that ships only what passes |

Read that table again and notice: it's literally the FDE loop, formalized. Day 4 says *"an agent
can pass 100 unit tests and still fail catastrophically — its failure is a flaw in judgment, not a
bug in the code."*[^g4] Day 5 says *"no version should reach users without first passing a
comprehensive evaluation."*[^g5] That's the deployment gap, named and closed by people who've
shipped at scale.

---

## What makes it a *school*, not a blog post

**1. It adapts to you — same files, five front doors.**
Every module is written for five people at once: a curious **15-year-old**, a **junior engineer**,
a **senior engineer**, an **AI director**, and an **executive**. The 15-year-old gets a 10-minute
win with a vending-machine analogy; the director gets the same lesson reframed as operating model,
risk, and ROI. Pick your level; the depth is already there underneath.

**2. Every lesson ends in a runnable artifact — and proves itself.**
No module is "done" because it sounds good. It's done when its code passes a self-test. M1 *runs* a
real agent (no API key, no setup). M4 *scores* a real run. M5 *gates* a real release — and it does
this by **importing M4's evaluator**, so deployment is literally built on top of evaluation, exactly
like the real world.

**3. The whole thing is gated — deterministically where it can be, by a human where it must be.**
One command, `bash scripts/check.sh`, runs **81 checks**: structure, valid schemas, every module's
7-part completeness, every tool's 8-field contract, and an **end-to-end test** that runs a *live*
M1 agent, evaluates it with M4, and ships it through M5. Green means *structurally complete and
internally consistent*. It does **not** mean "approved" — judging whether the writing is actually
*good* is reserved for a human. The hub never fakes a green, and never self-certifies taste.

That last line is the FDE's core discipline, baked into the tooling: *"reversible, observable,
measured, and honest about what broke."*[^wu]

---

## The proof is in the build itself

This isn't a brochure claim — it's observable in the repo's own history. The hub was built with the
same loop it teaches. Early on, a bug bit (a representation mismatch in the first agent); it was
caught by *reading the trajectory*, fixed, and **turned into a permanent test** — a `lesson` file
whose fix is a line in the check suite. Three modules later, the next two artifacts built **clean on
the first try**, because that lesson was now a reflex.

That's the flywheel from MIT's "learning gap" running *forward*: every failure becomes a safeguard,
so the same break can't ship twice. The repo's `memory/` folder is the organizational memory an FDE
team would kill for — decisions and lessons, versioned, reusable.

---

## Why this matters more as AI gets better, not less

The intuitive fear: "won't agents soon write all this themselves?" Wu's answer — and ours — is no,
and here's the sharp version for anyone allocating budget:

As building gets cheaper, **the premium shifts to knowing *what* to build, *where* it will break,
and *how to prove* it helps.**[^wu] That's not a model capability. It's an *evaluation* capability —
a school for the loop. The cheaper the model, the more the moat is the loop around it: your tools,
your context, your evals, your governance. This hub is a copyable, runnable starter for exactly
that capability — from a teenager's first agent to a governed production gate.

---

## Try it in 60 seconds

```bash
git clone <this-repo> && cd Google5Days-Agentic-Engineering
python3 modules/M1-your-first-agent-loop/exercise/agent_loop.py   # run a real agent, no setup
open index.html                                                   # browse the hub
bash scripts/check.sh                                             # watch 81 checks go green
```

Pick your level in `personas/`. Build the loop. Prove it works. Then do it again, harder — and
let every failure make the next build easier.

**The model is getting cheaper. Your loop is the asset. Come learn to build one that proves
itself.**

---

### Sources & references

[^wu]: Wu, William (PhD). *"The Fastest-Growing Job in AI Has No School, So I'm Building One That
Learns."* LinkedIn, 2026. <https://www.linkedin.com/pulse/fastest-growing-job-ai-has-school-so-im-building-one-learns-wu-phd-uoasc/>
— and the open-source curriculum it announces, [`wjlgatech/FDE-os`](https://github.com/wjlgatech/FDE-os).

[^mit]: MIT NANDA, *"The GenAI Divide: State of AI in Business 2025"* — finds ~95% of enterprise
generative-AI pilots deliver no measurable P&L impact (based on 150 interviews, 350 survey
responses, 300 deployments). Reported by *Fortune*, Aug 18 2025:
<https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo/>
· report PDF: <https://mlq.ai/media/quarterly_decks/v0.1_State_of_AI_in_Business_2025_Report.pdf>

[^fde]: Forward Deployed Engineer job postings up ~1,165% YoY (and 800%+ Jan–Sep 2025); see analysis
at Paraform, *"Forward-Deployed Engineers: How Demand Grew 10x in 18 Months"*:
<https://www.paraform.com/blog/forward-deployed-engineer-demand-quadrupled>

[^levels]: Palantir Forward Deployed Software Engineer compensation $171K–$295K (median ~$211K base),
Levels.fyi: <https://www.levels.fyi/companies/palantir/salaries/software-engineer/title/fdse>

[^g1]: Google, *"5-Day Agentic Engineering — Day 1: Introduction to Agents"* (2026). A. Blount,
A. Gulli, S. Saboo, M. Zimmermann, V. Vuskovic. (See `docs/2025_Day_1_Rewrite_v1_IntroductionToAgents.pdf`.)

[^g4]: Google, *"Day 4: Agent Quality"* (2026). M. Subasioglu, T. Bulmus, W. Bakkali, A. Nawalgaria.
(`docs/2025_Day_4_Rewrite_v1_AgentQuality.pdf`.) Source of *"the trajectory is the truth"* and the
"100 unit tests" warning.

[^g5]: Google, *"Day 5: Prototype to Production"* (2026). S. Kartakis, G. Hernandez Larios, R. Li,
E. Secchi, H. Xia, A. Nawalgaria. (`docs/2025_Day_5_Rewrite_v1_Prototype.pdf`.) Source of
*"Building an agent is easy. Trusting it is hard."* and evaluation-gated deployment.

*Primary sources (the five whitepapers) live in [`docs/`](../). Claims about this hub
(81 checks, runnable modules, the live end-to-end test) are reproducible: run
`bash scripts/check.sh`.*
