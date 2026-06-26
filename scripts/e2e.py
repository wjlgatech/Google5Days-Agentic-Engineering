#!/usr/bin/env python3
"""
e2e.py — prove the hub's modules COMPOSE on a LIVE run (objective O11).

M5 imports M4, but until now the M1 -> M4 link was only exercised on a hand-written sample.
This runs the real chain end-to-end:

    M1 (run an actual agent loop)  ->  M4 (evaluate its live trajectory)  ->  M5 (gate the release)

If this is green, the hub's central claim — "it all fits together into one loop" — is
machine-verified, not just asserted. scripts/check.sh runs this as O11.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
for _m in ("M1-your-first-agent-loop", "M4-is-your-agent-any-good", "M5-ship-it-without-breaking-it"):
    sys.path.insert(0, os.path.join(ROOT, "modules", _m, "exercise"))

from agent_loop import run as run_agent       # M1: the loop
from trajectory_eval import evaluate          # M4: trajectory evaluation
from deploy_gate import deploy                # M5: evaluation-gated deployment

ALLOW = ["calculator", "sunset"]
EXPECTED = {"contains": ["42", "8:15pm"]}

def m1_to_eval_shape(result: dict) -> dict:
    """Adapt M1's (thought, action, observation) trajectory into M4's {tool, args, observation}."""
    traj = [{"tool": action.split("(")[0], "args": {}, "observation": obs}
            for _thought, action, obs in result["trajectory"]]
    return {"mission": result["mission"], "trajectory": traj,
            "final_answer": result["answer"], "expected": EXPECTED}

def main() -> int:
    result = run_agent("What is 6 * 7, and what time is sunset roughly?")   # M1, live
    live_run = m1_to_eval_shape(result)
    ev = evaluate(live_run, allowed_tools=ALLOW)                            # M4, on the live run
    candidate = {"version": "e2e-v1", "suite": [live_run], "canary": live_run}
    promoted = deploy(candidate, human_signoff=True, allowed_tools=ALLOW)   # M5, gated
    held     = deploy(candidate, human_signoff=False, allowed_tools=ALLOW)

    checks = {
        "M1 produced a multi-step trajectory":   len(result["trajectory"]) >= 2,
        "M4 scored the LIVE run as pass":         ev["verdict"] == "pass",
        "M4 confirmed task success":              ev["task_success"] is True,
        "M5 PROMOTED the gated live release":     promoted["status"] == "PROMOTED",
        "M5 held it without human sign-off":      held["status"] == "HELD_FOR_SIGNOFF",
    }
    print("--- e2e: M1 -> M4 -> M5 on a LIVE agent run ---")
    for name, ok in checks.items():
        print(f"  {'✓' if ok else '✗'} {name}")
    return 0 if all(checks.values()) else 1

if __name__ == "__main__":
    sys.exit(main())
