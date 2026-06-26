# Tool: `spec-to-green`

> **The reference reusable tool of this hub.** It is the worked example of mission Pillar 2
> (a reusable coding-agent tool with a full 8-field contract) *and* of the Day 2 design rules.
> Copy this directory's shape to build the next tool. Machine-readable contract:
> [`contract.json`](contract.json) (validated against
> [`schemas/tool.schema.json`](../../schemas/tool.schema.json) by `scripts/check.sh`).

**One line:** *Turn a fuzzy request into a verifiable spec with a deterministic check, then
drive code to green against it — so "done" is proven, not claimed.*

This tool exists because of the single most important lesson in the five whitepapers: **"An
agent can pass 100 unit tests and still fail catastrophically — its failure is a flaw in
judgment, not a bug in the code"** (Day 4). The defense is to *write the check before the
code* and gate on it (Day 5: evaluation-gated deployment). `spec-to-green` makes that the
default workflow.

---

## The 8-field contract

| Field | Value |
|---|---|
| **Purpose** | Turn a fuzzy feature request into a verifiable spec **with a deterministic check**, then drive code to green against that check. |
| **Inputs** | A natural-language task; the target repo (test/check command auto-detected); optional acceptance hints. |
| **Outputs** | (1) a spec with machine-checkable acceptance criteria, (2) a check command/script, (3) a diff that makes it pass, (4) a trajectory log. |
| **When to use** | Fuzzy/multi-step task, correctness matters, you want proof-of-done. The `Specification→Validate` stages of the loop. |
| **When NOT to use** | One-line obvious changes; exploratory spikes; inherently subjective success (→ human gate). |
| **Workflow** | Intent → detect verification source → write spec + failing check → smallest green change → bounded fix loop → evaluate trajectory → record decision+lesson. |
| **Validation** | The repo's check exits 0 **and** every acceptance assertion is exercised. A human can re-run and reproduce green. |
| **Failure handling** | Missing info → ≤2 questions or explicit assumption; tool fails → report exact error + last file; same failure 3× → halt + escalate; subjective → human gate. |

Plus two Day-2/Day-5 flags: **idempotent: true** (safe to re-run) and **deterministic_gate:
true** (correctness rests on a check, not model judgment).

## How it maps to the loop

`spec-to-green` *is* loop stages ③ Specification → ⑤ Validate, with ⑥–⑨ as its tail. It is
the engine behind this very repo: [`scripts/check.sh`](../../scripts/check.sh) is the check it
would have written; [`docs/OBJECTIVES.md`](../../docs/OBJECTIVES.md) is the spec.

## Use it across agents (portable)

- **Claude Code:** [`SKILL.md`](SKILL.md) — drop into `.claude/skills/` or invoke its steps.
- **Codex / Hermes / Gemini / any OpenAI-compatible:** [`prompt.md`](prompt.md) — a
  model-agnostic prompt template carrying the same contract.
- **Any CI:** wire step "Validation" to your pipeline's required check (Day 5 pre-merge gate).

## Failure modes this tool itself guards against (Day 2/4)

- **Faking green** — it refuses; an honest ❌ with the trajectory beats a bad fix.
- **Unbounded thrash** — halts after the same failure 3× and escalates.
- **Silent subjectivity** — routes "is this *good*?" to a human instead of self-scoring.
