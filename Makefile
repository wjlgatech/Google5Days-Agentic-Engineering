# Agentic Engineering Hub — one finish line for the whole repo.
# `make check` is the discovered check command (so `anyagent goal` / CI can route to it).

.PHONY: check test gate

check: gate test   ## the full bar: structural gate + exercise tests

gate:   ## 104 structural checks incl. O14 lesson-ratchet (deterministic, zero-dep)
	bash scripts/check.sh

test:   ## pytest wrappers around every module's --selftest
	python3 -m pytest tests/ -q
