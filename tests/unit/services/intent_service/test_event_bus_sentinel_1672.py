"""Sentinel: nobody attaches an event bus to IntentClassifier (#1672).

THE LATENT HAZARD THIS GUARDS: ``IntentClassifier.classify`` emits
``intent.classified`` when ``self.event_bus`` is attached. Today no production
construction site passes one (verified 2026-08-21: classifier.py:1770,
intent_service/__init__.py, the two Slack sites, and container/initialization.py
all construct without ``event_bus=``), so the emission is inert — which is
exactly why the #1668 legacy-counterfactual leg may safely call ``classify``
unscoped/uncached as an observer.

The day someone attaches a subscriber, that safety assumption breaks SILENTLY:
the subscriber would start receiving shadow classifications from the
counterfactual, indistinguishable from real user turns, and the symptom would
surface in whatever the subscriber feeds — far from the cause.

This test converts that silent future hazard into a build-time conversation
(#1672's option (c), the cheap cure). If you are here because it failed: you
just attached an event bus to a production classifier. Before making this test
pass, EITHER give classify() an observer/suppress flag the #1668 counterfactual
sets, OR emit with a provenance field your subscriber honors — then update this
sentinel to assert the mitigation instead. Deleting the test is the one wrong
move; #1672 has the full analysis.
"""

import re
from pathlib import Path

SERVICES = Path(__file__).resolve().parents[4] / "services"

# Production construction sites, enumerated (not globbed) so a NEW site is
# also caught by the sweep below, and these named ones document the 2026-08-21
# baseline.
KNOWN_SITES = [
    "intent_service/classifier.py",
    "intent_service/__init__.py",
    "integrations/slack/response_handler.py",
    "integrations/slack/webhook_router.py",
    "container/initialization.py",
]

_CONSTRUCT_RE = re.compile(r"IntentClassifier\s*\(([^)]*)\)", re.DOTALL)


def _production_py_files():
    for p in SERVICES.rglob("*.py"):
        if "__pycache__" in p.parts or "tests" in p.parts:
            continue
        yield p


def test_no_production_site_attaches_an_event_bus_to_the_classifier():
    offenders = []
    for p in _production_py_files():
        text = p.read_text(encoding="utf-8", errors="ignore")
        for m in _CONSTRUCT_RE.finditer(text):
            if "event_bus" in m.group(1):
                offenders.append(f"{p.relative_to(SERVICES.parent)}: {m.group(0)[:90]}")
    assert not offenders, (
        "An event bus is now attached to IntentClassifier at a production "
        "site — the #1668 counterfactual's observer-safety assumption just "
        "broke. Read this file's docstring and #1672 BEFORE making this "
        f"pass. Sites: {offenders}"
    )


def test_known_sites_still_exist_so_the_sweep_is_not_vacuous():
    """m-44: if the construction sites moved, the sweep above might be
    scanning for a shape that no longer exists. At least the known ones must
    still construct an IntentClassifier at all."""
    found = 0
    for rel in KNOWN_SITES:
        p = SERVICES / rel
        if p.exists() and "IntentClassifier(" in p.read_text(encoding="utf-8", errors="ignore"):
            found += 1
    assert found >= 3, (
        f"Only {found} of the documented construction sites still exist — the "
        "sentinel's sweep may be vacuous; re-verify the classifier's "
        "construction surface and update KNOWN_SITES (#1672)."
    )
