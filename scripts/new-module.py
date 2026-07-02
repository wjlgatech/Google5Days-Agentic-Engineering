#!/usr/bin/env python3
"""
new-module.py — the course GRAMMAR made executable (the "Heighten" 10X move).

A module in this hub is a grammar: 7 parts × 5 personas × {runnable + --selftest}.
`schemas/module.schema.json` *names* that grammar; this script *generates* from it, so a new
module is DECLARED, not hand-authored across 9 files. The output passes objective O4 (the 7
part headings) and O10 (the exercise self-test) by construction.

    python3 scripts/new-module.py M6-give-your-agent-goals "Give Your Agent Goals" \\
        --stage Plan --day 1 [--dir modules]

It scaffolds; you then fill the prose and wire it into index.html (O12) + LEARNING-PATHS (O13).
That's the point: the machine guarantees the *structure*; a human supplies the *teaching*.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

PERSONAS = ["15-explorer", "20-junior", "30-senior", "40-director", "50-executive"]
# The 7 part headings the gate (O4) greps for — the schema's `parts`, as Markdown headings.
PARTS = [
    "Plain explanation", "Concrete example", "Hands-on exercise", "Real-world use case",
    "Failure mode", "Measurable output", "Next step",
]
PERSONA_LENS = {
    "15-explorer": "build something real today; plain words, a fun win",
    "20-junior": "workflows, debugging, shipping",
    "30-senior": "architecture, reliability, reuse",
    "40-director": "operating model, evaluation, risk",
    "50-executive": "strategy, governance, ROI",
}


def persona_md(mod_id: str, title: str, persona: str, script: str) -> str:
    parts = "\n\n".join(f"## {p}\n\n_TODO ({persona}): {p.lower()} — {PERSONA_LENS[persona]}._" for p in PARTS)
    run = f"cd modules/{mod_id}/exercise\npython3 {script} --selftest"
    return (
        f"# {title} — for the {persona} learner\n\n"
        f"*Same idea, framed for you: {PERSONA_LENS[persona]}.*\n\n"
        f"```bash\n{run}\n```\n\n{parts}\n"
    )


def exercise_py(mod_id: str, title: str) -> str:
    return (
        '#!/usr/bin/env python3\n'
        f'"""{title} — runnable exercise (scaffold). Fill in the real mechanism.\n\n'
        f'Zero-dep. `python3 {mod_id}.py --selftest` prints ✓/✗ and exits 0 when green;\n'
        'scripts/check.sh O10 runs this, and O14 enforces any lesson guard you add."""\n'
        'import sys\n\n\n'
        'def core(x: str) -> str:\n'
        '    """The one mechanism this module teaches. TODO: implement for real."""\n'
        '    return x.strip().lower()\n\n\n'
        'def selftest() -> int:\n'
        '    checks = {\n'
        '        "core runs":       core("  Hello ") == "hello",\n'
        '        "core is total":   isinstance(core(""), str),\n'
        '    }\n'
        '    print("--- self-test ---")\n'
        '    for name, ok in checks.items():\n'
        "        print(f\"  {'✓' if ok else '✗'} {name}\")\n"
        '    return 0 if all(checks.values()) else 1\n\n\n'
        'if __name__ == "__main__":\n'
        '    sys.exit(selftest() if "--selftest" in sys.argv else (print(core(" ".join(sys.argv[1:]))) or 0))\n'
    )


def readme_md(mod_id: str, title: str, stage: str, day: int) -> str:
    return (
        f"# {title}\n\n"
        f"> Conforms to [`schemas/module.schema.json`](../../schemas/module.schema.json); "
        f"structural completeness enforced by [`scripts/check.sh`](../../scripts/check.sh) (O4).\n\n"
        f"**Loop stage owned:** {stage} · **Source:** Day {day}.\n\n"
        "## Plug in at your level\n\n"
        + "\n".join(f"- [{p}](./{p}.md)" for p in PERSONAS) + "\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a schema-conformant learning module skeleton.")
    ap.add_argument("id", help="module id, e.g. M6-give-your-agent-goals")
    ap.add_argument("title", help="human title, e.g. 'Give Your Agent Goals'")
    ap.add_argument("--stage", default="Plan", help="loop stage owned (Intent/Plan/…/Decide)")
    ap.add_argument("--day", type=int, default=1, help="source whitepaper day (1-5)")
    ap.add_argument("--dir", default="modules", help="output parent dir (default: modules)")
    a = ap.parse_args()

    if not re.match(r"^M[0-9]+(-[a-z0-9-]+)?$", a.id):
        print(f"ERROR: id '{a.id}' must match ^M[0-9]+(-[a-z0-9-]+)?$ (e.g. M6-give-your-agent-goals)", file=sys.stderr)
        return 2
    root = pathlib.Path(a.dir) / a.id
    if root.exists():
        print(f"ERROR: {root} already exists — refusing to overwrite.", file=sys.stderr)
        return 2
    script = f"{a.id}.py"
    (root / "exercise").mkdir(parents=True)
    for p in PERSONAS:
        (root / f"{p}.md").write_text(persona_md(a.id, a.title, p, script))
    (root / "README.md").write_text(readme_md(a.id, a.title, a.stage, a.day))
    (root / "exercise" / script).write_text(exercise_py(a.id, a.title))

    n = len(list(root.rglob("*")))
    print(f"✓ generated {root}/ — {len(PERSONAS)} persona files + README + runnable exercise ({n} paths)")
    print(f"  next: fill the TODOs, then advertise it in index.html (O12) and personas/LEARNING-PATHS.md (O13).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
