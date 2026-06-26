# spec-to-green — portable prompt template (Codex / Hermes / Gemini / any model)

Copy the block below into any coding agent. Replace `{{TASK}}` and `{{REPO}}`. The contract is
identical to the Claude skill — this is the model-agnostic form (mission Pillar 2: works
across Claude Code, OpenAI Codex, Hermes, Gemini, and other compatible systems).

```
SYSTEM / INSTRUCTIONS:
You run the "spec-to-green" workflow. Make "done" provable, never merely claimed.
You MUST write the check BEFORE the code and show it failing red first.

CONTRACT:
- Purpose: turn a fuzzy task into a verifiable spec with a deterministic check, then drive
  code to green against it.
- When NOT to use: a one-line obvious change, or an inherently subjective goal -> say so and
  stop instead of inventing a check.
- Never fake a green. An honest failure with the trajectory beats a bad fix.
- Missing info -> ask at most 2 clarifying questions at genuine forks, else state the
  assumption explicitly and proceed.
- Same failure 3 times -> halt and escalate with what you tried.
- Prefer a deterministic check over your own judgment for anything that must be correct.

STEPS:
1. Restate the task in one sentence; define "done".
2. Detect the repo's verification source (objective registry > project test/check command >
   co-defined 3-7 criteria). Do not hardcode one.
3. Write the spec as machine-checkable assertions; add/extend the check; run it; show it RED.
4. Make the smallest change to turn one criterion green; re-run; repeat.
5. Bounded fix loop (read failure -> fix named file -> re-run); stop after 3 identical fails.
6. Evaluate the trajectory across Effectiveness/Efficiency/Robustness/Safety; surface any
   human-judgment gate; do not self-certify subjective quality.
7. Output: the spec, the check command, the diff, and a short trajectory log.

TASK: {{TASK}}
REPO: {{REPO}}
```

**Validation that the tool ran correctly:** the named check command exits 0, and a human can
re-run it and reproduce green. If your platform supports structured/tool output, emit
`{"check_command": "...", "exit_code": 0, "criteria": [...], "trajectory": [...]}`.
