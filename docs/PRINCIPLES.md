# PRINCIPLES — the distilled spine of the Agentic Engineering Hub

> Every principle here is traced to its source: the five Google *5-Day Agentic Engineering*
> whitepapers in [`docs/`](.). We separate **fact** (what a paper states), **decision** (how
> this hub applies it), and **assumption** (our extrapolation) so provenance stays visible
> — Design Principle #4.

This file is the *source of truth* for content. Modules, tools, the loop, and the persona
paths all derive from it. If a module contradicts this file, the module is wrong.

---

## The one-sentence thesis of the five days

> **Building an agent is easy; making it reliable, reusable, and trustworthy is the
> engineering** — and that engineering is a *loop*, not a phase.

The five days are five faces of one loop:

| Day | Paper | The face it teaches | Loop stage it owns |
|---|---|---|---|
| 1 | Introduction to Agents | What an agent *is* — model + tools + orchestration + runtime, run in a loop | **Intent → Plan** |
| 2 | Agent Tools (+ MCP) | How an agent *acts* — task-shaped tools with clear contracts | **Specification → Execute** |
| 3 | Context Engineering | What an agent *knows* — sessions (now) + memory (across time) | **Execute (state)** |
| 4 | Agent Quality | Whether to *trust* it — evaluate the trajectory, not just the answer | **Validate → Evaluate → Diagnose** |
| 5 | Prototype → Production | How it *survives contact with reality* — AgentOps, evaluation-gated deploy | **Learn → Decide → (loop)** |

The hub's closed loop — `Intent → Plan → Specification → Execute → Validate → Evaluate →
Diagnose → Learn → Decide Next Step` — is the five days expressed as one repeatable cycle.
See [`loop/README.md`](../loop/README.md).

---

## Day 1 — Introduction to Agents

**Source:** `2025_Day_1_Rewrite_v1_IntroductionToAgents.pdf` (Google, 2026).

- **[FACT] An agent is "LMs in a loop with tools to accomplish an objective."** Anatomy:
  **Model** (brain) · **Tools** (hands) · **Orchestration** (nervous system) · **Deployment**
  (body & legs). An agent is *a system dedicated to the art of context-window curation*.
- **[FACT] The 5-step agentic loop:** Get the Mission → Scan the Scene → Think It Through →
  Take Action → Observe & Iterate. (The "Think, Act, Observe" cycle.)
- **[FACT] Capability ladder (Levels 0–4):** 0 Core Reasoning · 1 Connected Problem-Solver ·
  2 Strategic Problem-Solver · 3 Collaborative Multi-Agent · 4 Self-Evolving.
- **[FACT] The developer's role shifts from "bricklayer" (writes explicit logic) to
  "director"** (sets instructions, casts tools, supplies context).
- **[FACT] Multi-agent patterns:** Coordinator, Sequential, Iterative Refinement
  (generator + critic), Human-in-the-Loop.
- **[FACT] An LM's greatest strength — flexibility — is also your biggest headache** (the
  source of unreliability). Engineering rigor across the *whole system* is what tames it.
- **[DECISION] The hub teaches the 5-step loop as the very first module** (`M1`) because it
  is the smallest complete mental model that produces a visible artifact today.

**Anti-patterns:** picking a model by benchmark score; "set it and forget it"; context
overload; one all-powerful super-agent instead of a team of specialists; `output == expected`
unit tests for probabilistic systems.

---

## Day 2 — Agent Tools & Interoperability (MCP)

**Source:** `2025_Day_2_Rewrite_v1_AgentTools.pdf`.

- **[FACT] Tools are the agent's "eyes and hands"** — they let a stateless predictor *know*
  (retrieve) and *do* (act).
- **[FACT] Publish tasks, not API calls.** A tool should encapsulate a user-facing *task*,
  not be a thin wrapper over a wide API. Make tools granular (single responsibility).
- **[FACT] A good tool contract:** descriptive specific name · documented input *and output*
  params (types + purpose) · short param lists · clear jargon-free description · examples for
  ambiguity · documented side-effects · concise output (don't swamp context) · schema
  validation · **error messages that tell the LLM how to recover**.
- **[FACT] MCP (Model Context Protocol)** standardizes the agent↔tool interface, solving the
  *N×M integration problem*. Primitives: server-side Tools/Resources/Prompts; client-side
  Sampling/Elicitation/Roots. *Only Tools is broadly supported (~99%).* MCP annotations
  (`readOnlyHint`, `idempotentHint`, `destructiveHint`) are **hints, not guarantees** — never
  trust them from untrusted servers.
- **[DECISION] Every reusable tool in this hub ships an 8-field contract** (Purpose, Inputs,
  Outputs, When to use, When NOT to use, Workflow, Validation, Failure handling) — enforced by
  [`schemas/tool.schema.json`](../schemas/tool.schema.json). This is the mission's tool
  requirement fused with Day 2's design rules.

**Anti-patterns:** thin API-wrapper tools; multi-step "mega-tools"; returning huge blobs;
non-descriptive errors; loading every tool's definition into context (bloat → degraded
reasoning). Security: tool shadowing, confused deputy, dynamic capability injection.

---

## Day 3 — Context Engineering

**Source:** `2025_Day_3_Rewrite_v1_ContextEngineering.pdf`.

- **[FACT] LLMs are stateless; statefulness is engineered.** *Context Engineering* =
  dynamically assembling the right information in the context window every turn. Goal: "no
  more and no less than the most relevant information to complete the task."
- **[FACT] Two systems:** **Sessions** (low-latency, chronological container for one
  conversation — events + state/scratchpad) and **Memory** (long-term, LLM-curated,
  per-user, persists *distilled* knowledge across sessions).
- **[FACT] RAG vs Memory:** *RAG makes an agent an expert on facts; memory makes it an
  expert on the user.* RAG = static/shared; memory = dynamic/per-user/isolated.
- **[FACT] Memory generation is an LLM-driven ETL pipeline:** Ingestion → Extraction &
  Filtering → Consolidation (merge/update/create/delete) → Storage (vector DB / knowledge
  graph). Run it **asynchronously, off the hot path.**
- **[FACT] Memories are descriptive, not predictive.** Track **provenance** (source +
  freshness) and prune stale/low-confidence ones (TTL, time-decay).
- **[DECISION] The hub *is* an externalized memory system** — [`memory/`](../memory/) holds
  decisions and lessons as the "long-term memory" of the human+AI team (Pillar 3 of the
  mission). Modules teach sessions-vs-memory using this very directory as the example.

**Anti-patterns / failure modes:** **context rot** (attention decays as context grows);
context overflow; "garbage in, confident garbage out"; dialogue injection; memory poisoning;
relying on vector relevance alone (blend relevance + recency + importance).

---

## Day 4 — Agent Quality

**Source:** `2025_Day_4_Rewrite_v1_AgentQuality.pdf`.

- **[FACT] Quality is an architectural pillar, not a final testing phase.** "An agent can
  pass 100 unit tests and still fail catastrophically — its failure isn't a bug in the code;
  it's a flaw in its judgment."
- **[FACT] The Trajectory is the Truth** — evaluate the whole decision path (plan → tool
  selection → arg formatting → tool-output interpretation → RAG → efficiency), not just the
  final answer ("the last sentence of a long story").
- **[FACT] Four Pillars of Quality:** Effectiveness · Efficiency · Robustness · Safety &
  Alignment.
- **[FACT] Evaluate "Outside-In":** Black-Box (final task success) first, then open the
  Glass-Box (trajectory) to diagnose *why*. Use a hybrid of **LLM-as-a-Judge** (prefer
  pairwise over single-score to cut bias) + **indispensable human judgment** — "an AI can
  help grade the test, but a human writes the rubric."
- **[FACT] The Agent Quality Flywheel:** Define Quality → Instrument for Visibility →
  Evaluate the Process → Architect the Feedback Loop (capture prod failures → golden set →
  next CI cycle).
- **[DECISION] The hub is "evaluable-by-design":** every module has a **measurable output**,
  every tool has a **Validation** field, and the repo ships a deterministic
  [`scripts/check.sh`](../scripts/check.sh) harness. Judgment-level quality (is this *good*?)
  is surfaced to a human, never self-certified — Design Principle: humans own truth claims.

**Anti-patterns:** silent degradation (200 OK, plausible-but-wrong); treating a metric
(BERTScore 0.8) as ground truth; one dashboard conflating system health with model quality;
gaming the metric.

---

## Day 5 — Prototype → Production (AgentOps)

**Source:** `2025_Day_5_Rewrite_v1_Prototype.pdf`.

- **[FACT] "Building an agent is easy. Trusting it is hard."** ~80% of the effort is the
  *last mile* — infrastructure, security, validation — not the core intelligence.
- **[FACT] Evaluation-Gated Deployment:** no version reaches users without passing a
  comprehensive eval. Version *everything* (code, prompts, model endpoints, tool schemas,
  memory structures, eval datasets) — your production "undo button."
- **[FACT] The production loop is Observe → Act → Evolve:** turn each production failure into
  tomorrow's golden-dataset test case. A known fix taking six months makes insight worthless.
- **[FACT] Protocols by abstraction:** **MCP** = "do this specific thing" (tools); **A2A** =
  "achieve this complex goal" (agent collaboration). Design idempotent, safe-to-retry tools.
- **[DECISION] The hub's compounding mechanism is exactly this loop:** every run ends by
  recording a decision + a lesson, and (when it earns it) a new objective or check — so the
  next run starts smarter. *"Bridging the last mile is not the final step; it is the first
  step in creating value."*

**Anti-patterns:** no guardrails (agent gives products away); no monitoring (surprise bill);
treating agents like static microservices; security as a one-time checklist; agent silos
that can't collaborate; non-idempotent tools causing duplicate side-effects on retry.

---

## The 8 hub design principles (from the mission) and how the papers enforce them

1. **Build for compounding capability** ← Day 5 Observe→Act→Evolve; Day 4 flywheel.
2. **Make learning executable** ← every module yields a *measurable output / artifact* (Day 4).
3. **Use progressive complexity** ← Day 1 Levels 0–4; the 5 personas.
4. **Separate facts / assumptions / decisions / opinions** ← Day 3 provenance; this file's tags.
5. **Prefer structured outputs** ← Day 2 schemas; `schemas/*.schema.json`; Day 4 rubrics.
6. **Design for reliable agentic loops** ← Day 1 loop; Day 4 trajectory; Day 5 evolve loop.
7. **Don't confuse activity with progress** ← Day 4 task-success metrics; OBJECTIVES.md.
8. **Turn failures into system improvements** ← Day 4/5 failure→golden-set; `memory/lessons/`.
