"""The collection floor holds regardless of invocation flags (#1671).

WHY THIS PIN EXISTS: pytest.ini's `addopts` carries the --ignore lines for the
archived tree, but `-o addopts=...` REPLACES that value wholesale. Every one-off
run that overrides addopts — including our own scripts/run-sweep.sh in unit and
full modes — silently re-collected tests/archive and reported ~24 failures that
read as a regression. A FALSE RED in the instrument we verify everything else
with, which is worse than a broken test: it makes a good tree look bad and
trains people to discount the suite.

The cure is conftest-level `collect_ignore_glob`, which conftest collection
honors irrespective of addopts. This file pins that the floor still exists —
deletion is the realistic rot, and deletion is silent (the symptom only shows
up under an addopts override, which CI never uses).
"""

import tests.conftest as root_conftest


def test_conftest_declares_a_collection_floor_for_archive():
    """The floor exists and names the archived tree, in both shapes."""
    patterns = getattr(root_conftest, "collect_ignore_glob", None)
    assert patterns, (
        "tests/conftest.py must declare collect_ignore_glob — without it, any "
        "`-o addopts=...` invocation re-collects tests/archive and reports a "
        "false red (#1671)."
    )
    assert "archive/*" in patterns
    assert "*/archive/*" in patterns


def test_pytest_ini_still_carries_the_fast_path():
    """The addopts ignores stay: belt kept, suspenders added — not replaced.

    The conftest floor is a backstop, not a substitute; addopts short-circuits
    collection earlier and faster on normal runs.
    """
    from pathlib import Path

    ini = Path(__file__).resolve().parent.parent / "pytest.ini"
    text = ini.read_text(encoding="utf-8")
    assert "--ignore=tests/archive" in text
