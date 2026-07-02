# Upgrade evidence — before vs after (explained for a 15-year-old)

We upgraded the hub along three axes. Here's the proof, in plain words. Every "after" number
was **measured**, not guessed — the command that measured it is in parentheses.

| What we improved | BEFORE | AFTER | Why it matters (plain words) |
|---|---|---|---|
| **↑ Adding a new lesson-module** | hand-type **9 files** (5 personas + readme + code), one typo breaks the test | **1 command** — `python3 scripts/new-module.py M6 "…"` | Like a **cookie cutter** vs. shaping each cookie by hand. The machine guarantees the shape (all 7 sections, in all 5 versions) so you can't forget one. *(verified: generated a module, all 7 headings present ×5, self-test green.)* |
| **→ Backend phone lines (LLM)** | **1 provider** — if it's busy (rate-limited), the smart helper goes dark | **4 providers**, tried in order | Like having **4 phone numbers** instead of 1. If the first is busy it dials the next. It never *lies* about which line answered. *(verified: `test_fallback.py` — 4 tests, chain order correct; live Gemini still answers.)* |
| **→ Does the robot check our work?** | **0** — the 104-check gate only ran when a human remembered | **runs on every push** (GitHub Actions) | Like a **spell-checker that runs every time you save**, not only when you remember. A broken change can't sneak in. *(added `.github/workflows/ci.yml` → `make check`.)* |
| **↔ Who can use our tool** | only a **human** reading a doc | any **AI agent** (MCP server) | Our best tool (`spec-to-green`) now has a **plug** other AIs can plug into — Claude Desktop, Code, or a teammate's agent. *(verified: real MCP session — initialize + tools/list + tools/call all answered.)* |
| **↔ One learner → a whole team** | one person's notes | **shared team memory + onboarding path** | Notes now carry an **author** and a **guard** (a mini-test). One teammate's bug becomes a check that protects everyone. *(added `paths/onboarding.md`, `author` on lessons.)* |
| **Overall code-quality score** | **62/100** | **65/100** | Earned by *adding* real tools + tests, not by deleting anything. *(`anyagent analyze .`)* |
| **The gate stays honest** | 104/104 green | **104/104 green** | We added a lot and **nothing broke**. *(`make check`.)* |

## The one-sentence version
**Before:** one helper, one phone line, checks-when-you-remember, tools only humans can use.
**After:** a cookie-cutter for new lessons, four phone lines, a robot that checks every change,
and tools other AIs can plug into — with the whole team's memory compounding behind it.

## How each was proven (so you can re-run it)
- **Module generator:** `python3 scripts/new-module.py M6-demo "Demo" --dir /tmp/x` then check every
  persona file has the 7 headings and the exercise `--selftest` exits 0.
- **Fallback chain:** `python3 -m pytest tests/test_fallback.py -q` (order + selection, no network).
- **MCP server:** pipe `initialize` / `tools/list` / `tools/call` JSON-RPC into
  `tools/spec-to-green/mcp_server.py` and read the replies.
- **Gate + CI:** `make check` locally; the same command runs in `.github/workflows/ci.yml` on push.
