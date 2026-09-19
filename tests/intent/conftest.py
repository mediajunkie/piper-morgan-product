"""tests/intent conftest — pin the unmarked tier to the DETERMINISTIC classifier (#1831).

The defect this fixes (2026-09-19, epic 1): the unmarked tests in this directory were
written against the deterministic classification tier, and in keyless CI that is exactly
what they exercise — `LLMClient.complete` raises the no-providers `RuntimeError`, the
classifier catches it and degrades onto the deterministic path, and the tests have passed
that way for months. But nothing PINNED that tier. On a dev seat whose keychain holds real
keys, provider selection succeeds, the leg reaches `request_spend_key`, and — post-#1809 —
raises `UnboundLLMKeyError`, which the stack deliberately does NOT catch (a refusal must
surface, never degrade — the #1809/#1815-Gap-2 ruling). Result: 26 tests local-red /
CI-green, and pre-#1809 the same 26 were silently LIVE-BILLING the developer's keys on
every local run (#1821's disease, this directory's cohort).

The stub below reproduces CI's boundary VERBATIM for unmarked tests: `complete` raises the
same no-providers RuntimeError keyless CI produces, so the deterministic degradation path
— the thing these tests actually assert on — runs identically everywhere, key or no key.

**`llm`-marked tests are exempt** (checked per-node): those are this directory's
deliberate live tier (e.g. the marked halves of the contracts files), and they keep the
real boundary — including #1819's operator binding via the root conftest when live keys
are present.

If you add a test here that needs a CANNED LLM ANSWER (not the deterministic tier), don't
widen this stub — inject a fake llm_client at construction like
`test_conversational_floor.py` does, or mark it `llm` for the live tier.
"""

import pytest


@pytest.fixture(autouse=True)
def _deterministic_tier_no_llm_1831(request, monkeypatch):
    """Unmarked tests get keyless-CI's exact LLM boundary; `llm`-marked tests don't."""
    if request.node.get_closest_marker("llm"):
        yield
        return

    async def _no_providers(self, *args, **kwargs):
        # The same terminal state keyless CI reaches (clients.py's no-provider raise),
        # so the classifier's catch-and-degrade behaves identically to CI. NOT an
        # UnboundLLMKeyError: a refusal is a correct ANSWER that must surface (#1809),
        # and faking one here would assert the wrong contract.
        raise RuntimeError(
            "No LLM providers configured. (#1831 deterministic-tier stub — "
            "tests/intent unmarked tests pin the deterministic classifier)"
        )

    monkeypatch.setattr("services.llm.clients.LLMClient.complete", _no_providers)
    yield
