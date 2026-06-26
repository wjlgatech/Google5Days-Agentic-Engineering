#!/usr/bin/env python3
"""
M5 — Ship It Without Breaking It  ·  evaluation-gated deployment in ~120 lines, zero deps.

The whole hub points here. Day 5: "Building an agent is easy. Trusting it is hard." ~80% of the
work is the LAST MILE — the infrastructure, security, and validation that make an agent safe to
release. The core rule is EVALUATION-GATED DEPLOYMENT: no version reaches users without first
passing a comprehensive evaluation.

So this module literally wires in M4's evaluator and makes it the gate. A release candidate is
BLOCKED unless every eval case passes; then a CANARY must stay healthy; then a HUMAN signs off
(Day 5: a Product Owner approves prod). And the loop closes — Observe -> Act -> EVOLVE turns a
production failure into a new permanent eval case, so the same break can never ship twice.

This is the hub's own philosophy at the deployment layer: deterministic gate where correctness
is objective (does it pass eval?), human gate where the stakes are high (promote to prod?).

Run it:
    python3 deploy_gate.py             # walk a good release, a blocked release, a rollback
    python3 deploy_gate.py --selftest  # deterministic check used by scripts/check.sh
"""
from __future__ import annotations
import os, sys

# Reuse M4's evaluator — "version everything" + don't reimplement the gate (Day 5). This import
# IS the lesson: deployment is built ON TOP of evaluation.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "M4-is-your-agent-any-good", "exercise"))
from trajectory_eval import evaluate, GOOD, BAD, ALLOW   # noqa: E402

def gate(suite: list[dict], **kw) -> dict:
    """Phase 1/2 of the CI/CD funnel: every eval case must pass, or the version is blocked.
    suite = [{trajectory, final_answer, expected}, ...]."""
    results = [{"verdict": evaluate(run, **kw)["verdict"]} for run in suite]
    passed = sum(r["verdict"] == "pass" for r in results)
    return {"approved": passed == len(suite) and len(suite) > 0,
            "pass_rate": round(passed / len(suite), 3) if suite else 0.0,
            "results": results}

def canary(run: dict, **kw) -> dict:
    """Safe-rollout phase: route a sliver of traffic to the new version and watch it. Healthy
    only if the canary run still passes evaluation."""
    healthy = evaluate(run, **kw)["verdict"] == "pass"
    return {"healthy": healthy}

def evolve(failure_run: dict, expected: dict) -> dict:
    """Observe -> Act -> EVOLVE: turn a production failure into a new golden eval case. Returning
    a suite entry so the caller can append it — the same break can never ship again."""
    return {**failure_run, "expected": expected, "origin": "prod-failure"}

def deploy(candidate: dict, human_signoff: bool = False, **kw) -> dict:
    """The full gated pipeline. candidate = {version, suite, canary}.
    Order: evaluation gate -> canary -> human sign-off -> promote. Any stage can stop it."""
    g = gate(candidate["suite"], **kw)
    if not g["approved"]:
        # Day 5: a version that fails eval NEVER reaches users.
        return {"status": "BLOCKED_AT_GATE", "version": candidate["version"], "gate": g}
    c = canary(candidate["canary"], **kw)
    if not c["healthy"]:
        return {"status": "ROLLED_BACK", "version": candidate["version"], "gate": g, "canary": c}
    if not human_signoff:
        # Humans own the high-stakes call (Day 5: Product Owner sign-off before prod).
        return {"status": "HELD_FOR_SIGNOFF", "version": candidate["version"], "gate": g, "canary": c,
                "human_gate": "NEEDS_HUMAN: approve promotion to production?"}
    # The deploy record = your production "undo button": version + per-case verdicts.
    return {"status": "PROMOTED", "version": candidate["version"],
            "record": {"version": candidate["version"], "gate": g, "canary": c,
                       "rollout": "canary 1% -> 100%", "idempotent_tools_only": True}}

# ---- self-test = the measurable output (Day 4/5). scripts/check.sh runs this. ----

EXP = {"contains": ["42", "8:15pm"]}

def selftest() -> int:
    good = {"version": "v1.0", "suite": [GOOD], "canary": GOOD}
    bad  = {"version": "v1.1", "suite": [GOOD, BAD], "canary": GOOD}   # one case fails eval
    flaky = {"version": "v1.2", "suite": [GOOD], "canary": BAD}        # passes gate, fails canary

    promoted = deploy(good, human_signoff=True, allowed_tools=ALLOW)
    held     = deploy(good, human_signoff=False, allowed_tools=ALLOW)
    blocked  = deploy(bad,  human_signoff=True, allowed_tools=ALLOW)
    rolled   = deploy(flaky, human_signoff=True, allowed_tools=ALLOW)

    # Observe -> Act -> Evolve: the prod failure (BAD) becomes a golden case; the grown suite
    # now catches it, so the previously-shippable version is correctly blocked.
    grown = [GOOD, evolve(BAD, EXP)]
    gate_after_evolve = gate(grown, allowed_tools=ALLOW)

    checks = {
        "good + signoff -> PROMOTED":         promoted["status"] == "PROMOTED",
        "good - signoff -> HELD_FOR_SIGNOFF": held["status"] == "HELD_FOR_SIGNOFF",
        "human gate not auto-answered":       held["human_gate"].startswith("NEEDS_HUMAN"),
        "failing eval -> BLOCKED_AT_GATE":    blocked["status"] == "BLOCKED_AT_GATE",
        "blocked never reaches prod":         blocked.get("record") is None,
        "canary fail -> ROLLED_BACK":         rolled["status"] == "ROLLED_BACK",
        "deploy record has version (undo)":   promoted["record"]["version"] == "v1.0",
        "rollout strategy recorded":          "canary" in promoted["record"]["rollout"],
        "evolve grows the suite":             len(grown) == 2,
        "evolved suite catches the failure":  gate_after_evolve["approved"] is False,
    }
    print("--- self-test ---")
    for name, ok in checks.items():
        print(f"  {'✓' if ok else '✗'} {name}")
    return 0 if all(checks.values()) else 1

def _demo():
    for label, cand, signoff in [("good release", {"version": "v1.0", "suite": [GOOD], "canary": GOOD}, True),
                                 ("bad release", {"version": "v1.1", "suite": [GOOD, BAD], "canary": GOOD}, True),
                                 ("flaky canary", {"version": "v1.2", "suite": [GOOD], "canary": BAD}, True)]:
        r = deploy(cand, human_signoff=signoff, allowed_tools=ALLOW)
        print(f"{label:14s} -> {r['status']}")
    print("\nObserve->Act->Evolve: a prod failure becomes eval case; grown suite now blocks it:",
          "BLOCKED" if not gate([GOOD, evolve(BAD, EXP)], allowed_tools=ALLOW)["approved"] else "??")

if __name__ == "__main__":
    sys.exit(selftest()) if "--selftest" in sys.argv else _demo()
