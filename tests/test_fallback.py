"""Unit tests for the webapp guide's free-LLM fallback chain (no network)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "webapp"))
import guide  # noqa: E402


def names(env):
    return [p["name"] for p in guide.active_providers(env)]


def test_no_key_means_no_provider():
    assert guide.active_providers({}) == []


def test_single_provider_selected():
    assert names({"OPENROUTER_API_KEY": "x"}) == ["openrouter"]


def test_chain_order_is_preserved_not_env_order():
    # Even if only GROQ+GEMINI keys exist, Gemini (higher in the chain) comes first.
    assert names({"GROQ_API_KEY": "x", "GEMINI_API_KEY": "y"}) == ["gemini", "groq"]


def test_all_four_in_declared_order():
    env = {p["key_env"]: "x" for p in guide.PROVIDERS}
    assert names(env) == ["gemini", "groq", "nvidia", "openrouter"]
