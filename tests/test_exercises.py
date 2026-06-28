"""
Pytest wrappers around every module's runnable `--selftest`.

Why this exists: `anyagent analyze` scored the repo's "testing" dimension at 0% because
the self-tests live *inside* each exercise (the right call pedagogically — a learner sees
the proof next to the code). This file gives the toolchain real test *files* to find,
without touching the teaching code: it imports each exercise by path and asserts its
`selftest()` returns 0 (all checks green). `scripts/check.sh` (O10) runs the same
selftests as the authoritative gate; this is the developer-facing `pytest` view of them.

    pip install pytest && pytest tests/ -q
"""
import importlib.util
import io
import pathlib
from contextlib import redirect_stdout

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
EXERCISES = sorted(REPO.glob("modules/M*/exercise/*.py"))


def _load(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(f"exercise_{path.stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_all_five_exercises_present():
    # Guards against a module's artifact going missing (the analyzer would silently skip it).
    assert len(EXERCISES) == 5, [str(p.relative_to(REPO)) for p in EXERCISES]


@pytest.mark.parametrize("path", EXERCISES, ids=lambda p: p.parent.parent.name)
def test_exercise_selftest_is_green(path):
    mod = _load(path)
    assert hasattr(mod, "selftest"), f"{path} has no selftest()"
    with redirect_stdout(io.StringIO()):  # selftest prints its ✓/✗ table; keep test output clean
        rc = mod.selftest()
    assert rc == 0, f"{path.parent.parent.name} selftest returned {rc} (a check failed)"
