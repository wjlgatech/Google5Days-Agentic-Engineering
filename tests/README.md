# tests/

Developer-facing `pytest` view of the modules' runnable self-tests.

```bash
pip install pytest
pytest tests/ -q
```

Each exercise (`modules/M*/exercise/*.py`) ships its own `--selftest` — that is the
authoritative check, run by `bash scripts/check.sh` (objective **O10**). These tests are
the same selftests surfaced as real test *files* so standard tooling (CI, coverage,
`anyagent analyze`) can see them, **without** moving the proof out of the teaching code
where a learner reads it.

If you add a module, no change is needed here: `test_exercises.py` auto-discovers every
`modules/M*/exercise/*.py` and asserts its `selftest()` returns 0.
