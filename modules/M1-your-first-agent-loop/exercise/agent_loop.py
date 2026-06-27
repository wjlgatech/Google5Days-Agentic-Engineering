#!/usr/bin/env python3
"""
M1 — Your First Agent Loop  ·  the smallest complete agent, in ~80 lines, zero deps.

This is the hands-on artifact for Module M1. It implements Day 1's 5-step loop literally:

    Get the Mission -> Scan the Scene -> Think It Through -> Take Action -> Observe & Iterate

There is no LLM here on purpose: an agent is "a system in a loop with tools to accomplish an
objective" (Day 1). The *loop and the tools* are the engineering; the model is swappable. We
stub the "Think" step with a tiny rule-based planner so you can run it offline, see the
trajectory, and THEN swap in a real model (see `think_with_llm` at the bottom).

Run it:
    python3 agent_loop.py "What is 6 * 7, and what time is sunset roughly?"
    python3 agent_loop.py --selftest      # deterministic check used by scripts/check.sh

The agent keeps a SHORT-TERM MEMORY (the trajectory: a list of (thought, action, observation)
— Day 3 "session") and prints it at the end, because **the trajectory is the truth** (Day 4).
"""
from __future__ import annotations
import sys, re, ast, operator

# ---- TOOLS: the agent's "hands" (Day 2). Each is task-shaped, with a clear contract. ----

def tool_calculator(expr: str) -> str:
    """Evaluate a basic arithmetic expression. Input: '6 * 7'. Output: the number, or an
    error string that tells the agent how to recover (Day 2: errors must teach recovery)."""
    ops = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
           ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg}
    def ev(node):
        if isinstance(node, ast.Constant): return node.value
        if isinstance(node, ast.BinOp):  return ops[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp): return ops[type(node.op)](ev(node.operand))
        raise ValueError("unsupported")
    try:
        return str(ev(ast.parse(expr, mode="eval").body))
    except Exception:
        return "ERROR: calculator needs a plain arithmetic expression like '6 * 7'. Retry with digits and + - * / only."

def tool_sunset(_: str) -> str:
    """A stand-in 'world' tool: returns a fixed fact. In a real agent this calls an API."""
    return "Sunset is roughly 8:15pm local in summer."

# TOOLS is a *dict* (name -> function), not a list. To add your own tool you do TWO things:
#   (1) register it here with a key:   TOOLS = {..., "shout": tool_shout}
#   (2) teach the planner to pick it — add a rule in think() below (a tool nobody calls is dead).
TOOLS = {"calculator": tool_calculator, "sunset": tool_sunset}

# ---- ORCHESTRATION: the loop itself (Day 1 "nervous system"). ----

def think(mission: str, scratch: list) -> tuple[str, str, str] | None:
    """The planner. Returns (thought, tool_name, tool_input) or None when done.
    This rule-based stub is deliberately simple — swap `think_with_llm` in to go real."""
    done_calc = any(a.startswith("calculator") for _, a, _ in scratch)
    done_sun  = any(a.startswith("sunset")     for _, a, _ in scratch)
    m = mission.lower().replace("x", "*")
    arith = re.search(r"\d+\s*[\*\+\-/]\s*\d+", m)
    if not done_calc and arith:
        return ("The mission contains arithmetic; I'll use the calculator.", "calculator", arith.group().strip())
    if not done_sun and "sunset" in m:
        return ("The mission asks about sunset; I'll use the sunset tool.", "sunset", "")
    # YOUR TURN (exercise): add a rule for your new tool here, e.g.
    #   done_shout = any(a.startswith("shout") for _, a, _ in scratch)
    #   if not done_shout and "shout" in m:
    #       return ("The mission says shout; I'll use the shout tool.", "shout", mission)
    return None  # nothing left to do -> exit the loop

def run(mission: str, think_fn=think, max_steps: int = 6) -> dict:
    """The 5-step loop. Returns the final answer + the full trajectory (short-term memory)."""
    print(f"① MISSION: {mission}\n")
    scratch: list[tuple[str, str, str]] = []        # (thought, action, observation) — the session
    for step in range(1, max_steps + 1):
        plan = think_fn(mission, scratch)            # ②③ Scan + Think
        if plan is None:
            break
        thought, tool, tool_in = plan
        if tool not in TOOLS:                        # robustness (Day 4 pillar)
            obs = f"ERROR: no tool named '{tool}'. Available: {list(TOOLS)}."
        else:
            obs = TOOLS[tool](tool_in)               # ④ Take Action
        scratch.append((thought, f"{tool}({tool_in!r})", obs))   # ⑤ Observe & remember
        print(f"  step {step}: 🧠 {thought}\n           🔧 {tool}({tool_in!r}) -> {obs}")
    answer = " ".join(obs for _, _, obs in scratch) or "Nothing to do."
    print(f"\n⑤ ANSWER: {answer}")
    return {"mission": mission, "answer": answer, "trajectory": scratch, "steps": len(scratch)}

# ---- SELF-TEST: the measurable output (Day 4). Deterministic; scripts/check.sh runs this. ----

def selftest() -> int:
    r = run("What is 6 * 7, and what time is sunset roughly?")
    checks = {
        "calculator used":   any(a.startswith("calculator") for _, a, _ in r["trajectory"]),
        "sunset used":       any(a.startswith("sunset") for _, a, _ in r["trajectory"]),
        "answer has 42":     "42" in r["answer"],
        "answer has sunset": "8:15pm" in r["answer"],
        "terminated":        r["steps"] <= 6,
        "bad tool handled":  tool_calculator("not math").startswith("ERROR"),
    }
    print("\n--- self-test ---")
    for name, passed in checks.items():
        print(f"  {'✓' if passed else '✗'} {name}")
    return 0 if all(checks.values()) else 1

# ---- GO REAL (read this after you've run the stub): swap the planner for an LLM. ----
# def think_with_llm(mission, scratch):
#     """Give the model the mission + trajectory + the TOOLS contracts, ask for the next
#     (thought, tool, input) as JSON. That is ALL a real agent changes — the loop is the same.
#     This is where you'd plug Claude/Gemini/etc. Keep the tool contracts identical."""
#     ...

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    mission = " ".join(args) or "What is 6 * 7, and what time is sunset roughly?"
    run(mission)
