#!/usr/bin/env python3
"""
M4 — Is Your Agent Any Good?  ·  trajectory evaluation in ~150 lines, zero deps.

M1 ran a loop, M2 gave it hands, M3 gave it memory. M4 asks the only question that matters in
production: is it any GOOD? Day 4's answer: "An agent can pass 100 unit tests and still fail
catastrophically — its failure is a flaw in judgment, not a bug in the code." So we evaluate
the TRAJECTORY (plan -> tool choice -> args -> observations -> answer), not just the final line.

Evaluate OUTSIDE-IN:
  1. Black-Box  — did the final answer meet the objective? (task success)
  2. Glass-Box  — open the trajectory: right tools? valid args? redundant/missing steps?
                  did it terminate? did it stay safe?
Score the FOUR PILLARS (Effectiveness, Efficiency, Robustness, Safety) -> overall -> verdict.

What stays human (Day 4: "a human writes the rubric"): whether the answer is well-judged/clear.
This evaluator NEVER self-certifies that — it returns a NEEDS_HUMAN gate. That's the hub rule:
deterministic where we can be, human where judgment is required.

The rule-based scorer here stands in for an LLM-as-a-Judge; swap one in at `# GO REAL` below.
It also does PAIRWISE judging (Day 4: pairwise beats single-scoring for cutting judge bias).

Run it:
    python3 trajectory_eval.py             # evaluate a good run and a bad run
    python3 trajectory_eval.py --selftest  # deterministic check used by scripts/check.sh
"""
from __future__ import annotations
import sys, json

def evaluate(run: dict, expected: dict | None = None, allowed_tools: list | None = None,
             max_steps: int = 8) -> dict:
    """Score one agent run across the Four Pillars. `run` = {mission, trajectory:[{tool,args,
    observation}], final_answer, ...}. Deterministic; returns pillars + verdict + findings."""
    traj = run.get("trajectory", [])
    steps = len(traj)
    final = run.get("final_answer", "")
    exp = expected or run.get("expected") or {}
    must = [m.lower() for m in exp.get("contains", [])]

    # ---- Black-Box: task success ----
    hits = [m for m in must if m in final.lower()]
    effectiveness = (len(hits) / len(must)) if must else (1.0 if final and not final.startswith("ERROR") else 0.0)
    task_success = (len(hits) == len(must)) if must else effectiveness == 1.0

    # ---- Glass-Box: open the trajectory ----
    tools = [s.get("tool") for s in traj]
    seen, redundant = set(), 0
    for s in traj:
        key = (s.get("tool"), json.dumps(s.get("args", {}), sort_keys=True))
        if key in seen:
            redundant += 1
        seen.add(key)
    errors = sum(1 for s in traj if str(s.get("observation", "")).startswith("ERROR"))
    disallowed = sorted({t for t in tools if allowed_tools is not None and t not in allowed_tools})
    terminated = steps <= max_steps
    nonidem = run.get("non_idempotent_tools", [])
    nonidem_repeat = sorted({t for t in nonidem if tools.count(t) > 1})
    distinct_useful = len({t for t, s in zip(tools, traj) if not str(s.get("observation", "")).startswith("ERROR")})

    # ---- Four Pillars (0..1) ----
    efficiency = round(distinct_useful / steps, 3) if steps else 0.0          # every step a distinct useful action -> 1.0
    robustness = round(max(0.0, 1.0 - errors / steps), 3) if steps else 0.0   # unrecovered errors hurt
    safety = 0.0 if (disallowed or nonidem_repeat) else 1.0
    pillars = {"effectiveness": round(effectiveness, 3), "efficiency": efficiency,
               "robustness": robustness, "safety": safety}
    overall = round(sum(pillars.values()) / 4, 3)

    findings = []
    if not task_success: findings.append(f"task NOT met (matched {len(hits)}/{len(must)} expected)")
    if redundant:        findings.append(f"{redundant} redundant tool call(s)")
    if disallowed:       findings.append(f"disallowed tool(s): {disallowed}")
    if not terminated:   findings.append(f"did not terminate within {max_steps} steps")
    if errors:           findings.append(f"{errors} error observation(s) in trajectory")
    if nonidem_repeat:   findings.append(f"non-idempotent tool repeated (unsafe retry): {nonidem_repeat}")

    # Verdict: deterministic gate. PASS needs task success + safe + terminated + decent overall.
    verdict = "pass" if (task_success and safety == 1.0 and terminated and overall >= 0.6) else "fail"
    return {
        "pillars": pillars, "overall": overall, "task_success": task_success,
        "terminated": terminated, "verdict": verdict, "findings": findings,
        # NEVER auto-answered — Day 4: a human writes the rubric for subjective quality.
        "human_gate": "NEEDS_HUMAN: is the final answer well-judged, clear, and appropriate in tone?",
    }

def pairwise(run_a: dict, run_b: dict, **kw) -> dict:
    """Compare two runs and pick a winner (Day 4: pairwise > single-scoring to cut judge bias)."""
    a, b = evaluate(run_a, **kw), evaluate(run_b, **kw)
    winner = "A" if a["overall"] > b["overall"] else "B" if b["overall"] > a["overall"] else "tie"
    return {"winner": winner, "a_overall": a["overall"], "b_overall": b["overall"],
            "rationale": f"A={a['overall']} vs B={b['overall']}; A findings={a['findings']}, B findings={b['findings']}"}

# GO REAL: replace the rule-based scorer with an LLM-as-a-Judge — pass the trajectory + a
# human-written rubric to a model and ask for per-pillar scores as JSON. Keep the human_gate.

# ---- sample runs (a clean M1-style success, and a broken run) ----

GOOD = {"mission": "What is 6 * 7, and what time is sunset?",
        "trajectory": [{"tool": "calculator", "args": {"expr": "6 * 7"}, "observation": "42"},
                       {"tool": "sunset", "args": {}, "observation": "Sunset is roughly 8:15pm local in summer."}],
        "final_answer": "42 Sunset is roughly 8:15pm local in summer.",
        "expected": {"contains": ["42", "8:15pm"]}}
BAD = {"mission": "What is 6 * 7, and what time is sunset?",
       "trajectory": [{"tool": "calculator", "args": {}, "observation": "ERROR: needs an expression"},
                      {"tool": "calculator", "args": {}, "observation": "ERROR: needs an expression"},
                      {"tool": "weather", "args": {}, "observation": "sunny"}],
       "final_answer": "ERROR ... sunny",
       "expected": {"contains": ["42", "8:15pm"]}}
ALLOW = ["calculator", "sunset"]

# ---- self-test = the measurable output (Day 4). scripts/check.sh runs this. ----

def selftest() -> int:
    g = evaluate(GOOD, allowed_tools=ALLOW)
    b = evaluate(BAD, allowed_tools=ALLOW)
    pw = pairwise(GOOD, BAD, allowed_tools=ALLOW)
    checks = {
        "good run PASSES":              g["verdict"] == "pass",
        "good overall is high":         g["overall"] >= 0.9,
        "black-box: good task success": g["task_success"] is True,
        "bad run FAILS":                b["verdict"] == "fail",
        "black-box: bad task fail":     b["task_success"] is False,
        "glass-box catches redundancy": any("redundant" in f for f in b["findings"]),
        "glass-box catches disallowed": any("disallowed" in f for f in b["findings"]),
        "safety pillar flags disallowed": b["pillars"]["safety"] == 0.0,
        "pairwise: good beats bad":     pw["winner"] == "A",
        "human gate NOT auto-answered": g["human_gate"].startswith("NEEDS_HUMAN"),
        "efficiency rewards clean run": g["pillars"]["efficiency"] > b["pillars"]["efficiency"],
    }
    print("--- self-test ---")
    for name, ok in checks.items():
        print(f"  {'✓' if ok else '✗'} {name}")
    return 0 if all(checks.values()) else 1

def _demo():
    for label, run in [("GOOD", GOOD), ("BAD", BAD)]:
        r = evaluate(run, allowed_tools=ALLOW)
        print(f"{label}: verdict={r['verdict']} overall={r['overall']} pillars={r['pillars']}")
        print(f"      findings={r['findings']}\n      {r['human_gate']}")
    print("\npairwise:", pairwise(GOOD, BAD, allowed_tools=ALLOW)["winner"], "wins")

if __name__ == "__main__":
    sys.exit(selftest()) if "--selftest" in sys.argv else _demo()
