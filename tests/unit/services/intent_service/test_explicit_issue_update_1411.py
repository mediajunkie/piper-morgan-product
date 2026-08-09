"""#1411 update-reachability gap — explicit-#N update shape resolves at B3 Stage 0.

PM's live retest (2026-08-09): "change the title of issue #108 to test new
regressions" never reached the fully-implemented, rail-registered update_issue
handler. Two deterministic-layer mechanisms, both live-reproduced before the fix:

- WITHOUT '#' ("… of issue 108 to …"): surface 1's DOCUMENT_QUERY_PATTERNS
  (``change … to``) claims it → ``update_document_query`` @ confidence 1.0 —
  a hard misroute to the document handler.
- WITH '#': the '#' happens to break the doc pattern's ``[\\w\\s]+`` span, so
  surface 1 passes — and B3 Stage 0 deliberately falls through on explicit
  ``#N`` (the ``_EXPLICIT_ISSUE_RE`` guard: "nothing to resolve"). Every
  deterministic surface passed, so reachability of update_issue depended
  entirely on the LLM emission ("rail fine, reachability = corpus").

Fix at the B3 SEAM (the stack doc's sanctioned deterministic Stage 0), NOT a
new pre-classifier pattern: ``_detect_explicit_issue_update`` +
``_resolve_issue_referent``'s explicit path emit ``update_issue`` with the
issue number bound by construction, before ``detect_multiple_intents`` at both
classifier entries. All prior N-guards stay intact (the ledgered-referent
detection is untouched; see test_b3_referent_resolution_1394.py).
"""

import contextlib

import pytest
import pytest_asyncio

from services.intent_service.classifier import (
    IntentClassifier,
    _detect_explicit_issue_update,
    _detect_issue_referent,
)

# PM's verbatim retest phrasing (2026-08-09).
PM_MSG = "change the title of issue #108 to test new regressions"
PM_MSG_NO_HASH = "change the title of issue 108 to test new regressions"

_CONV = "conv-1411-1"
_USER = "owner-1411"


class TestDetection:
    """Deterministic explicit-#N detection. Guards mirror the referent path:
    update verb AND issue-field word required (the N2 analog); a document noun
    anywhere declines (a stray '#4' in a doc-edit message is not an issue)."""

    @pytest.mark.parametrize("msg,num", [
        (PM_MSG, 108),
        (PM_MSG_NO_HASH, 108),
        ("update the labels on issue #77", 77),
        ("set the state of #42 to closed", 42),
        ("In acme/widgets, change the title of issue #107 to something new", 107),
    ])
    def test_explicit_updates_detected_with_number(self, msg, num):
        assert _detect_explicit_issue_update(msg) == num

    @pytest.mark.parametrize("msg", [
        "change the title of the design doc to #4",   # doc noun → doc edit, not issue
        "change the title to Foo",                    # no explicit N → ledgered-referent path
        "close issue #9",                             # not an update-field shape
        "what does issue #12 say",                    # read, not update
        "update the roadmap document with #12 items", # doc noun
        "",
    ])
    def test_non_matches_pass_through(self, msg):
        assert _detect_explicit_issue_update(msg) is None

    def test_ledgered_referent_guard_unchanged(self):
        """The pre-existing guard is untouched: explicit #N is still NOT an
        unresolved referent (the two detectors are disjoint by construction)."""
        assert _detect_issue_referent(PM_MSG) is False
        assert _detect_issue_referent("change the title to Foo") is True


@pytest_asyncio.fixture
async def sm(monkeypatch):
    # Ledger-backed tests only — the fixture (not the module) requires aiosqlite,
    # so the detection/no-ledger tests above still RUN on seats without it (the
    # module-level importorskip in the 1394 suite silently skips everything there).
    pytest.importorskip("aiosqlite")
    from sqlalchemy.ext.asyncio import (
        AsyncSession,
        async_sessionmaker,
        create_async_engine,
    )

    from services.database.models import SessionActivityDB

    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: SessionActivityDB.__table__.create(c, checkfirst=True))
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with maker() as s:
            yield s

    import services.database.session_factory as sf

    monkeypatch.setattr(sf.AsyncSessionFactory, "session_scope", staticmethod(_scope))
    yield maker
    await engine.dispose()


async def _seed_issue(maker, owner, conv, ref="mediajunkie/test-piper-morgan#108", title="T"):
    from services.database.repositories import SessionActivityRepository

    async with maker() as s:
        await SessionActivityRepository(s).record(
            owner_id=owner, conversation_id=conv,
            action_type="issue_created", target_ref=ref, target_title=title,
        )


class TestResolverEmit:
    pytestmark = pytest.mark.asyncio

    async def test_explicit_resolves_without_session(self):
        """The user already named the issue — no ledger read required, so the
        explicit path resolves even with no principal/session (D1a scopes
        LEDGER reads; this path reads none here)."""
        intent = await IntentClassifier._resolve_issue_referent(PM_MSG, None, None)
        assert intent is not None
        assert intent.action == "update_issue"
        assert intent.context["issue_number"] == 108
        assert "repository" not in intent.context  # unbound → handler slot-fills or asks
        assert intent.original_message == PM_MSG   # raw preserved (#1332)

    async def test_ledger_binds_repository_when_this_session_created_it(self, sm):
        await _seed_issue(sm, _USER, _CONV, ref="mediajunkie/test-piper-morgan#108")
        intent = await IntentClassifier._resolve_issue_referent(PM_MSG, _USER, _CONV)
        assert intent is not None
        assert intent.action == "update_issue"
        assert intent.context["issue_number"] == 108
        assert intent.context["repository"] == "mediajunkie/test-piper-morgan"

    async def test_ledger_with_different_number_does_not_cross_bind(self, sm):
        await _seed_issue(sm, _USER, _CONV, ref="mediajunkie/test-piper-morgan#107")
        intent = await IntentClassifier._resolve_issue_referent(PM_MSG, _USER, _CONV)
        assert intent is not None
        assert intent.context["issue_number"] == 108
        assert "repository" not in intent.context

    async def test_never_create_issue(self):
        intent = await IntentClassifier._resolve_issue_referent(PM_MSG, None, None)
        assert intent.action != "create_issue"
        assert intent.action == "update_issue"


class TestOrderingAndWiring:
    """B3 must keep running BEFORE detect_multiple_intents at both entries —
    the doc-pattern claim on the no-hash form is still live at surface 1
    (pinned below), so Stage-0 ordering is what makes the fix hold."""

    pytestmark = pytest.mark.asyncio

    async def test_surface1_still_claims_no_hash_form(self):
        """Pin the mechanism: the pre-classifier's document pattern DOES claim
        the no-hash phrasing. If this ever changes, the ordering rationale in
        this file (and the stack doc) needs revisiting — not deleting."""
        from services.intent_service.pre_classifier import PreClassifier

        res = PreClassifier.pre_classify(PM_MSG_NO_HASH)
        assert res is not None and res.action == "update_document_query"

    async def test_classify_multiple_resolves_before_document_claim(self, sm):
        """PM's no-hash form through the real classify_multiple entry: B3's
        explicit path must win over the surface-1 document claim."""
        await _seed_issue(sm, _USER, _CONV, ref="mediajunkie/test-piper-morgan#108")
        clf = IntentClassifier()
        result = await clf.classify_multiple(
            PM_MSG_NO_HASH, user_id=_USER, session_id=_CONV
        )
        assert result.intents, "B3 must emit — not fall to the document handler"
        assert result.intents[0].action == "update_issue"
        assert result.intents[0].action != "update_document_query"
        assert result.intents[0].context["issue_number"] == 108

    async def test_classify_resolves_hash_form_without_llm(self):
        """PM's verbatim hash form through classify(): deterministic emit —
        the LLM must never be consulted (reachability no longer = corpus)."""

        class _Explosive:
            def __getattr__(self, name):
                raise AssertionError("LLM must not be consulted for explicit-#N updates")

        clf = IntentClassifier(llm_service=_Explosive())
        intent = await clf.classify(PM_MSG, use_cache=False)
        assert intent.action == "update_issue"
        assert intent.context["issue_number"] == 108
