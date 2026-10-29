"""Shared fixtures for the intent_service unit suite.

#1821 (fixes the #1819 containment): nine files here (37 tests) drive the REAL
conversational floor for turns that — correctly, by design — fall through to it
(CONVERSATION/STATUS/UNKNOWN category routing, off-intent pops, state-question
survival re-arms). The floor's default `_get_llm_client()` lazily builds a REAL
`LLMClient()` singleton when no `llm_client` was injected at construction, and
every `ConversationalFloor()` call site inside `services/intent/intent_service.py`
(`_handle_floor_with_context`, `_handle_unknown_intent`, and two further
fallthrough sites) constructs it bare — none accept an injectable client. So on
any keyed machine (including `run-sweep.sh unit`, which strips only ANTHROPIC_*
env vars) these 37 tests were making a LIVE OpenAI completion, billed to
whatever key the machine's keychain/env held, on every sweep.

#1819 contained this by binding the designated-operator form (the diff this
docstring replaces), which made the spend *legal* rather than removing the
need for it — the suites still depended on the spend machinery, just with an
explicit opt-in instead of an accidental one.

THE FIX (#1821, this file): none of the 37 tests assert on the floor's actual
composed prose — every one pins offer/pending-state/routing mechanics (last_offer,
pending_offer, category, dispatch) that are upstream of, or independent from,
whatever the floor says. That is #1821's Class B: "didn't know they were reaching
an LLM at all — assert on things upstream of the call." The fix cuts the path at
the floor's LLM boundary itself: `LLMClient.complete` is stubbed with a benign,
deterministic canned string for exactly these nine files, so a turn that falls
through to the floor completes for free and for real (all the surrounding
routing/offer/context-assembly logic still runs) — it just never reaches a
vendor SDK or the network. Scoped by filename (not directory-autouse) so the
OTHER files in this directory that test the floor directly are untouched: they
already inject their own fake `llm_client` at `ConversationalFloor(...)`
construction (test_conversational_floor.py et al. — the correct, pre-existing
idiom for tests that DO care about floor composition).

No key, no keychain read, no network path — the suite needs none of the three.
If a stray call reaches an UNPATCHED LLM boundary anyway (a new call site, or a
file added to this directory without equivalent coverage), #1809's inversion is
the backstop: an unbound context raises `UnboundLLMKeyError` instead of silently
spending — loud failure, not a bill.
"""

import pytest

# The nine files named in #1821's census, verified against the tree by running
# each with the LLM boundary UNSTUBBED and a real (keychain-loaded) key present:
# exactly 37 failures, all `UnboundLLMKeyError` at the `_openai_complete` chokepoint.
_FLOOR_STUBBED_FILES = frozenset(
    {
        "test_contextual_offer_continuation.py",
        "test_reminder_clear_verb_anchor_1653.py",
        "test_offer_accept_decline.py",
        "test_standup_offer_flag_1652.py",
        "test_soft_offer_survival_clobber_1753.py",
        "test_soft_offer_last_offer_clobber_1770.py",
        "test_standup_todo_offer_1651.py",
        "test_offer_binding_1529.py",
        "test_soft_invocation_integration.py",
    }
)

_CANNED_FLOOR_MESSAGE = "(#1821 test double: floor LLM boundary stubbed — no key, no network)"


@pytest.fixture(autouse=True)
def _stub_floor_llm_boundary_1821(request, monkeypatch):
    """Cut the LLM boundary for the nine #1821 files — see module docstring.

    A no-op for every other file in this directory (including the dedicated
    floor-composition suites, which inject their own fake ``llm_client`` and
    never reach the real ``LLMClient`` class this patches).
    """
    if request.node.fspath.basename not in _FLOOR_STUBBED_FILES:
        yield
        return

    from services.llm.clients import LLMClient

    async def _canned_complete(self, *args, **kwargs):
        return _CANNED_FLOOR_MESSAGE

    monkeypatch.setattr(LLMClient, "complete", _canned_complete)
    yield


# #2205 (Arch 2026-10-29 13:48): a GitHub WRITE now uses only a default the USER
# designated (source "user"); an auto-picked or source-less default asks first. These
# files were written before the default carried a source: each sets up its default (or
# its absence) through ``get_user_default_repo`` or a mocked router, and tests what a
# write does GIVEN that default. For them, whatever default the test configured counts
# as user-designated, so they keep testing what they test. The gate itself (auto,
# legacy, user, the ask and its persisted answer) is pinned in
# test_write_target_designated_2205.py, which is NOT in this set.
_LEGACY_DESIGNATED_DEFAULT_FILES = frozenset(
    {
        "test_acceptance_contract_1739.py",
        "test_action_fabrication_1648.py",
        "test_comment_issue_graceful_1159.py",
        "test_comment_issue_slotfill_1124.py",
        "test_confirm_crisp_accept_1650.py",
        "test_consent_gate_1509.py",
        "test_create_issue_title_1543.py",
        "test_destructive_confirm_1190.py",
        "test_drafted_issue_1571.py",
        "test_drafted_issue_body_steal_1627.py",
        "test_drafted_issue_explicit_slots_1649.py",
        "test_drafted_issue_subjectless_1630.py",
        "test_github_query_handlers.py",
        "test_issue_close_reopen.py",
        "test_repo_clarification_1567.py",
        "test_repo_wiring_1641.py",
        "test_update_issue_clarify_first_1411.py",
    }
)


@pytest.fixture(autouse=True)
def _legacy_default_is_user_designated_2205(request, monkeypatch):
    """See ``_LEGACY_DESIGNATED_DEFAULT_FILES``. The configured default (possibly
    patched by the test) is returned as the write target; with none configured, a
    write in these files reaches the router's own resolution as before (the router
    is mocked there), so the target reads as designated."""
    if request.node.fspath.basename not in _LEGACY_DESIGNATED_DEFAULT_FILES:
        yield
        return

    from services.integrations.github import repo_resolver

    async def _designated(user_id):
        if user_id is None:
            return "legacy-test/designated-default"
        from uuid import UUID

        configured = await repo_resolver.get_user_default_repo(UUID(str(user_id)))
        return configured or "legacy-test/designated-default"

    monkeypatch.setattr(repo_resolver, "get_user_write_target", _designated)
    yield
