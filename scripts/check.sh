#!/usr/bin/env bash
# check.sh — the deterministic verification harness for the Agentic Engineering Hub.
# Implements docs/OBJECTIVES.md O1..O10. Exits non-zero on any failure.
# Zero dependencies beyond bash + python3 (JSON validation) + standard coreutils.
#
# This file IS the "evaluation-gated deployment" of Day 5, applied to a docs hub:
# nothing is "green" until it passes here. Turn future failures into new checks below.

set -uo pipefail
cd "$(dirname "$0")/.." || exit 2

VERBOSE=0; [[ "${1:-}" == "-v" || "${1:-}" == "--verbose" ]] && VERBOSE=1
PASS=0; FAIL=0
ok()   { PASS=$((PASS+1)); [[ $VERBOSE -eq 1 ]] && printf '  \033[32m✓\033[0m %s\n' "$1"; return 0; }
bad()  { FAIL=$((FAIL+1)); printf '  \033[31m✗\033[0m %s\n' "$1"; return 0; }
hdr()  { printf '\n\033[1m%s\033[0m\n' "$1"; }

exists() { [[ -f "$1" ]] && ok "$1 exists" || bad "$1 MISSING"; }
# grep -q wrapper: contains PATTERN in FILE
has() { if [[ -f "$1" ]] && grep -qiE "$2" "$1"; then ok "$3"; else bad "$3"; fi; }

PERSONAS=(15-explorer 20-junior 30-senior 40-director 50-executive)
# The 7 mission-required module parts, as the headings used in the persona files.
PARTS=("Plain" "Concrete example" "Hands-on" "Real-world" "Failure mode" "Measurable output" "Next step")

hdr "O1  Repo skeleton"
for f in README.md index.html CHANGELOG.md AGENTS.md docs/PRINCIPLES.md docs/OBJECTIVES.md; do exists "$f"; done

hdr "O2  Schemas are valid JSON"
shopt -s nullglob
for s in schemas/*.schema.json; do
  if python3 -c "import json,sys; json.load(open('$s'))" 2>/dev/null; then ok "$s valid"; else bad "$s INVALID JSON"; fi
done
[[ -f schemas/module.schema.json ]] || bad "schemas/module.schema.json missing"
[[ -f schemas/tool.schema.json ]]   || bad "schemas/tool.schema.json missing"

hdr "O3  Personas (5) exist & route to a module"
for p in "${PERSONAS[@]}"; do
  f="personas/$p.md"
  exists "$f"
  has "$f" "modules/M1" "$p links module M1"
done

hdr "O4  Modules complete — 7 parts × 5 personas (matched on HEADING lines, not prose)"
mods=(modules/*/)
[[ -d "${mods[0]:-}" ]] || bad "no modules found under modules/"
for d in "${mods[@]}"; do
  [[ -d "$d" ]] || continue
  mod=$(basename "$d")
  for p in "${PERSONAS[@]}"; do
    f="$d$p.md"
    if [[ ! -f "$f" ]]; then bad "$mod/$p.md MISSING"; continue; fi
    missing=""
    for part in "${PARTS[@]}"; do
      # Require the part as a Markdown heading (^#+ ...), so a stray phrase in prose can't fake it.
      grep -qiE "^#+ .*${part}" "$f" || missing="$missing[$part]"
    done
    [[ -z "$missing" ]] && ok "$mod/$p has all 7 part headings" || bad "$mod/$p missing part HEADINGS: $missing"
  done
done

hdr "O5  Reusable tool 'spec-to-green' complete (8-field contract)"
TOOLDIR=tools/spec-to-green
exists "$TOOLDIR/README.md"
exists "$TOOLDIR/contract.json"
if [[ -f "$TOOLDIR/contract.json" ]]; then
  python3 - "$TOOLDIR/contract.json" schemas/tool.schema.json <<'PY' && ok "contract.json present & has all 8 fields" || bad "contract.json incomplete"
import json,sys
c=json.load(open(sys.argv[1]))
req=["purpose","inputs","outputs","when_to_use","when_not_to_use","workflow","validation","failure_handling"]
missing=[k for k in req if not c.get(k)]
sys.exit(1 if missing else 0)
PY
fi

hdr "O6  Closed loop documented — 9 stages in order"
LOOP=loop/README.md
exists "$LOOP"
for stage in Intent Plan Specification Execute Validate Evaluate Diagnose Learn Decide; do
  has "$LOOP" "$stage" "loop names stage: $stage"
done

hdr "O7  Provenance — all 5 days cited"
for d in 1 2 3 4 5; do has docs/PRINCIPLES.md "Day $d" "PRINCIPLES cites Day $d"; done

hdr "O8  HTML hub real & wired"
if [[ -f index.html ]]; then
  bytes=$(wc -c < index.html)
  [[ "$bytes" -gt 2000 ]] && ok "index.html non-trivial ($bytes bytes)" || bad "index.html too small ($bytes bytes)"
fi
has index.html "M1-your-first-agent-loop|Your First Agent Loop" "index.html references module M1"
has index.html "spec-to-green" "index.html references the tool"

hdr "O9  Org memory seeded & schema-valid"
dcount=$(ls memory/decisions/*.json 2>/dev/null | wc -l | tr -d ' ')
lcount=$(ls memory/lessons/*.json 2>/dev/null | wc -l | tr -d ' ')
[[ "$dcount" -ge 1 ]] && ok "$dcount decision(s) present" || bad "no decisions in memory/decisions/"
[[ "$lcount" -ge 1 ]] && ok "$lcount lesson(s) present" || bad "no lessons in memory/lessons/"
for j in memory/decisions/*.json memory/lessons/*.json; do
  [[ -f "$j" ]] || continue
  python3 -c "import json;json.load(open('$j'))" 2>/dev/null && ok "$(basename "$j") valid JSON" || bad "$(basename "$j") INVALID"
done

hdr "O10  Runnable exercises self-test green (every module that ships one)"
found=0
for py in modules/*/exercise/*.py; do
  [[ -f "$py" ]] || continue
  grep -q "selftest" "$py" || continue
  found=$((found+1))
  label="$(basename "$(dirname "$(dirname "$py")")")/$(basename "$py")"
  if python3 "$py" --selftest >/dev/null 2>&1; then ok "$label --selftest passed"; else bad "$label --selftest FAILED"; fi
done
[[ $found -ge 1 ]] && ok "$found self-testing exercise(s) found" || bad "no runnable self-testing exercise found"

hdr "O11  End-to-end: modules compose on a LIVE run (M1 → M4 → M5)"
exists "scripts/e2e.py"
if [[ -f scripts/e2e.py ]]; then
  if python3 scripts/e2e.py >/dev/null 2>&1; then ok "e2e.py passed (live M1 run evaluated by M4, gated by M5)"; else bad "e2e.py FAILED — modules do not compose on a live run"; fi
fi

hdr "O12  No broken promises — advertised modules exist, on-disk modules are advertised"
# (a) every module the hub advertises in index.html must exist on disk (catches a deleted module)
adv=$(grep -oE 'modules/M[0-9][^"/]*' index.html 2>/dev/null | sort -u)
[[ -n "$adv" ]] || bad "no module cards found in index.html"
while IFS= read -r m; do
  [[ -z "$m" ]] && continue
  [[ -d "$m" ]] && ok "advertised $m exists" || bad "index.html advertises a MISSING module: $m"
done <<< "$adv"
# (b) every module on disk must be advertised (catches an orphan/unlinked module)
for d in modules/*/; do
  [[ -d "$d" ]] || continue
  mod="modules/$(basename "$d")"
  grep -q "$mod" index.html && ok "$mod is advertised in index.html" || bad "$mod exists but is NOT advertised in index.html"
done

# ---- summary ----
printf '\n\033[1m──────────────────────────────\033[0m\n'
TOTAL=$((PASS+FAIL))
if [[ $FAIL -eq 0 ]]; then
  printf '\033[32m✓ GREEN\033[0m  %d/%d checks passed.\n' "$PASS" "$TOTAL"
  printf 'Structural completeness confirmed. Human gates HJ1–HJ3 (see OBJECTIVES.md) remain yours.\n'
  exit 0
else
  printf '\033[31m✗ RED\033[0m  %d/%d passed, %d failed.\n' "$PASS" "$TOTAL" "$FAIL"
  exit 1
fi
