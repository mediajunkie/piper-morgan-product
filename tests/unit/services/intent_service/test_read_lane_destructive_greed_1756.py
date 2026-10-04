"""1756 — the READ lanes decline destructive asks at surface 1.

The 2026-09-13 census ran 100 destructive shapes through the REAL
pre-classifier on BOTH entry paths (``pre_classify_with_pattern_list`` and
``detect_multiple_intents``). Four read lanes claimed them:

    STATUS_PATTERNS .......... 30/30  ("get rid of my tasks" -> status/get_project_status)
    TEMPORAL_PATTERNS ........ 24/24  ("delete the meeting tomorrow" -> temporal/get_current_time)
    MEMORY_PATTERNS .......... 15/15  ("delete our conversation history" -> memory/get_memory)
    CALENDAR_QUERY_PATTERNS ... 5/6   ("delete my meetings this week" -> query/week_calendar)

(The issue named the first three; CALENDAR_QUERY is the same failure class on
the same vocabulary — "delete my meetings this week" is a sibling of the
issue's own "delete the meeting tomorrow" — and was found by this census.
INSIGHT_PULL_PATTERNS was probed too and claimed 0/5: no work needed there.)

Why this is the higher-stakes member of the #1527 family: a surface-1 claim
SHORT-CIRCUITS the LLM lane (``classifier.py`` returns on the ``pre_classify``
branch before the LLM call, and ``classify_multiple`` returns on any non-empty
detection). The destructive ask therefore never becomes a DESTRUCTIVE rail
action, and the #1190 confirm gate — which only ever inspects rail actions —
never gets a turn on it. The user asks for a deletion and is handed a status
report, the current time, or their own memory contents.

The fix is the blocker idiom (REMINDER_QUERY_BLOCKERS #1521 /
INTEGRATION_CONNECT_BLOCKERS #1471) narrowed by POSITION rather than by
vocabulary: ``DESTRUCTIVE_ASK_BLOCKERS`` fires only when the destructive verb
heads the turn or sits under an explicit request frame. #1527's positive
evidence has no analogue here — a read lane's legitimate claim space is not
marked by any one noun. NARROWING ONLY: a blocked lane falls through, never
reroutes, and no new claim is created.

Layer honesty (m-43): every assertion below calls ``PreClassifier`` directly —
surface 1, the layer that can wrongly claim. ``TestGateSeesTheFallThrough``
checks the rail layer (registry effect declarations); it does NOT run the LLM
classifier, which needs credentials no unit test has. What is verified is the
two links this change owns: surface 1 declines, and the rail family a
destructive ask lands in is declared DESTRUCTIVE so the gate fires on it.

Denominator (m-44): 100 destructive shapes (30 STATUS / 24 TEMPORAL /
15 MEMORY / 5 INSIGHT_PULL / 6 CALENDAR / 20 misc) plus 50 read controls;
the sets below are that census verbatim, minus the 6 GITHUB_QUERY shapes,
which are a DIFFERENT lane and filed as separate discovered work.
"""

import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory

# ── Destructive asks, by the lane that wrongly claimed them ────────────────

STATUS_LANE_DESTRUCTIVE = (
    "get rid of my tasks",  # the issue's own probe phrase
    "delete my tasks",
    "remove my tasks",
    "clear my tasks",
    "cancel my tasks",
    "erase my tasks",
    "wipe my tasks",
    "delete my current tasks",
    "delete all active tasks",
    "remove that task status",
    "delete my assignments",
    "get rid of my assignments",
    "remove my current assignments",
    "get rid of my portfolio",
    "delete my portfolio",
    "wipe my portfolio",
    "get rid of my current work",
    "delete my current work",
    "remove my active work",
    "delete my status",
    "clear my status",
    "erase my progress",
    "delete my progress",
    "remove my progress report",
    "delete my standup",
    "cancel my standup",
    "remove the upcoming milestone",
    "delete my work status",
)

TEMPORAL_LANE_DESTRUCTIVE = (
    "delete the meeting tomorrow",  # the issue's own probe phrase
    "cancel the meeting tomorrow",
    "delete my meetings",
    "cancel my meetings",
    "remove my next meeting",
    "cancel my next meeting",
    "delete my upcoming meetings",
    "cancel the meeting today",
    "clear my calendar",
    "delete my calendar",
    "wipe my calendar",
    "clear my schedule",
    "delete my schedule",
    "erase my schedule",
    "delete my appointments",
    "cancel my appointments",
    "delete my events",
    "cancel my events",
    "remove my upcoming events",
    "delete the next event",
    "clear my free time",
    "delete my open slots",
)

MEMORY_LANE_DESTRUCTIVE = (
    "delete our conversation history",  # the issue's own probe phrase
    "delete my conversation history",
    "delete my history",
    "erase our conversation history",
    "wipe my history",
    "clear my conversation history",
    "remove my conversation history",
    "delete our past conversations",
    "erase past conversations",
    "delete previous messages",
    "remove previous conversations",
    "clear my conversation log",
    "delete the conversation log",
    "get rid of my history",
    "get rid of our conversation history",
)

CALENDAR_LANE_DESTRUCTIVE = (
    "delete my meetings this week",
    "cancel tomorrow's schedule",
    "cancel my agenda for today",
    "clear my agenda",
    "delete what's on my calendar",
)

ALL_DESTRUCTIVE = (
    STATUS_LANE_DESTRUCTIVE
    + TEMPORAL_LANE_DESTRUCTIVE
    + MEMORY_LANE_DESTRUCTIVE
    + CALENDAR_LANE_DESTRUCTIVE
)

# Categories a read lane claims into. A destructive ask reaching ANY of these
# at surface 1 is the bug — asserting on the category set (not one action)
# keeps the pin honest if a lane's action string is ever renamed.
READ_LANE_CATEGORIES = frozenset(
    {
        IntentCategory.STATUS,
        IntentCategory.TEMPORAL,
        IntentCategory.MEMORY,
        IntentCategory.QUERY,
    }
)

# ── Legitimate reads that must KEEP their claim (no over-narrowing) ────────

# #1595 Phase 3 seventh deletion (2026-10-02, PARTIAL): every one of the 13
# original phrases below matched a STATUS_PATTERNS literal now among the 52
# deleted (STATUS_PATTERNS keeps only 4: \bcurrent work\b, \bproject
# overview\b, \bproject landscape\b, \bnext milestone\b) — none of the
# originals claim anything at surface 1 any more. Swapped for 13 phrases
# confirmed claiming deterministically at confidence 1.0, this session,
# drawn from STATUS_PATTERNS' 4 survivors, STATUS's COMPLETION_HISTORY_
# PATTERNS sibling, and LOCAL_GIT_STATUS_PATTERNS (#1044, QUERY category,
# a member of READ_LANE_CATEGORIES, untouched by any Phase 3 deletion so
# far) — same point: legitimate reads that must keep their claim.
#
# #1595 Phase 3 eighteenth deletion (2026-10-03, PARTIAL): 7 of the 13
# phrases below matched now-deleted LOCAL_GIT_STATUS_PATTERNS literals
# (`\bwhat branch are we on\b`, `\bwhat branch am i on\b`, `\bcurrent
# branch\b`, `\bworking tree (?:clean|dirty|status)\b`, `\buncommitted
# changes?\b`, `\bahead of (?:main|origin|upstream|master)\b`,
# `\bunpushed commits?\b`, `\blocal git status\b`) and no surviving literal
# covers them — moved OUT of this set (see
# LOCAL_GIT_STATUS_READS_NOW_UNCLAIMED and
# TestLocalGitStatusReadsNowDeclineAtSurfaceOne below), same treatment as
# TEMPORAL_READS/MEMORY_READS_NOW_UNCLAIMED. The remaining 5 are genuine
# STATUS_PATTERNS/COMPLETION_HISTORY_PATTERNS reads, unaffected.
STATUS_READS = (
    "can you summarize my current work",
    "any update on the next milestone",
    "give me a project overview",
    "what's the project landscape",
    "when did I complete the onboarding project?",
)
LOCAL_GIT_STATUS_READS_NOW_UNCLAIMED = (
    "what branch are we on",
    "what branch am i on",
    "current branch",
    "working tree clean",
    "uncommitted changes",
    "ahead of main",
    "unpushed commits",
    "local git status",
)
# #1595 Phase 3 fourth deletion (2026-10-01): TEMPORAL_PATTERNS is now `[]`
# (tombstoned) — these phrases no longer claim at surface 1 AT ALL, whether
# or not a destructive verb is present. The positional-vs-vocabulary
# narrowing property this file pins has nothing left to narrow for this
# category: there is no surface-1 claim space to over- or under-narrow.
# Kept as a named historical record (not deleted — the phrases themselves
# are still real, legitimate temporal reads), but moved OUT of
# KEEP_CLAIMING; see TestTemporalReadsNowDeclineAtSurfaceOne below, which
# pins the new reality directly instead of silently dropping the coverage.
TEMPORAL_READS = (
    "what time is it",
    "what's the date",
    "my calendar",
    "show my calendar",
    "my schedule",
    "my meetings",
    "next meeting",
    "upcoming meetings",
    "my appointments",
    "my events",
    "upcoming events",
    "when am i free",
    "free time",
    "what happened yesterday",
)
# #1595 Phase 3 eleventh deletion (2026-10-03, PARTIAL): 8 of the original
# 11 phrases below matched now-deleted MEMORY_PATTERNS literals (\bwhat do
# you remember\b, \bdo you remember\b, \bpast conversations?\b, \bprevious
# (conversations?|chats?|messages?)\b, \bconversation log\b, \bwhat (did|
# have) (i|we) (talk|discuss|say)\b, \bhow (much|far back) do you
# remember\b, \bremember (when|that|our|my)\b) and no surviving literal
# covers them — moved OUT of this set (see MEMORY_READS_NOW_UNCLAIMED and
# TestMemoryReadsNowDeclineAtSurfaceOne below). The remaining 3 are still
# claimed: "show my history" and "my conversation history" via the
# surviving \b(my|our) (conversation )?history\b literal (reabsorption —
# "show my history" was formerly claimed by the deleted \b(show|view|see)
# ... history\b literal), "search my history" via the surviving \bsearch
# (my |our )?(conversation )?history\b literal (unaffected by this
# deletion).
MEMORY_READS = (
    "show my history",
    "my conversation history",
    "search my history",
)
MEMORY_READS_NOW_UNCLAIMED = (
    "what do you remember",
    "do you remember",
    "past conversations",
    "previous conversations",
    "conversation log",
    "what did we talk about",
    "how much do you remember",
    "remember when we discussed the api",
)
# #1595 Phase 3 third+fourth deletions: CALENDAR_QUERY_PATTERNS (2026-10-01
# third deletion) and TEMPORAL_PATTERNS (fourth, same day — which had been
# reabsorbing these phrases after CALENDAR's own deletion, per the third
# deletion's documented known_reabsorptions) are BOTH now `[]`. Same
# treatment as TEMPORAL_READS above — moved out of KEEP_CLAIMING, pinned
# declining instead in TestTemporalReadsNowDeclineAtSurfaceOne.
CALENDAR_READS = (
    "what's on my calendar",
    "meetings this week",
    "tomorrow's schedule",
)

# The load-bearing distinction: a destructive VERB in a read turn is a read
# ABOUT deletion, not a deletion. Position, not vocabulary — this is the set a
# naive `\bdelete\b` blocklist would have broken.
READS_MENTIONING_DESTRUCTIVE_VERBS = (
    # #1595 Phase 3 fourth deletion (2026-10-01): the original two phrases
    # here ("what did i delete yesterday", "what meetings did i cancel
    # yesterday") matched TEMPORAL_PATTERNS' generic `\bdid.*yesterday\b` /
    # `\bwhat.*yesterday\b` patterns — now tombstoned, so surface 1 no
    # longer claims either. Swapped for STATUS-lane equivalents (confirmed
    # claiming at confidence 1.0, live, this session) that exercise the
    # SAME property — a destructive verb mentioned mid-sentence, not heading
    # the ask — via a surviving lane. Not deleted: STATUS_PATTERNS still has
    # no "yesterday"-specific vocabulary, so this is a genuinely different
    # (but equally valid) member of the same shape, not a weaker stand-in.
    # #1595 Phase 3 seventh deletion (2026-10-02, PARTIAL): all three phrases
    # below matched now-deleted STATUS_PATTERNS literals (`\bmy tasks\b` /
    # `\bshow.*tasks\b` / `\bwhat tasks\b`) and no longer claim anything.
    # Swapped for 3 phrases confirmed claiming deterministically at
    # confidence 1.0 AND confirmed NOT an ask position
    # (`PreClassifier._is_destructive_ask` returns False for each, this
    # session) — a destructive verb mentioned mid-sentence, not heading the
    # ask, via STATUS_PATTERNS' surviving \bcurrent work\b literal and
    # LOCAL_GIT_STATUS_PATTERNS (untouched by any Phase 3 deletion so far).
    "can you summarize my current work before i delete the test branch",
    # #1595 Phase 3 eighteenth deletion (2026-10-03, PARTIAL): the original
    # two phrases below ("what branch are we on, i think i deleted the
    # wrong one", "git status before i delete my branch") matched now-
    # deleted LOCAL_GIT_STATUS_PATTERNS literals (`\bwhat branch are we on
    # \b`, `\blocal git status\b`) and no longer claim anything. Swapped
    # for 2 phrases confirmed claiming deterministically at confidence 1.0
    # AND confirmed NOT an ask position (`PreClassifier._is_destructive_
    # ask` returns False for each, this session) via LOCAL_GIT_STATUS_
    # PATTERNS' own surviving \bbehind (?:main|origin|upstream|master)\b
    # literal — same destructive-verb-mid-sentence shape, same list,
    # different literal.
    "we're behind upstream, i think i deleted the wrong branch",
    "check if we're behind upstream before i delete this branch",
    # #1595 Phase 3 eleventh deletion (2026-10-03, PARTIAL): the original
    # two phrases here ("do you remember what i deleted", "what did we
    # discuss about deleting projects") matched now-deleted MEMORY_PATTERNS
    # literals (\bdo you remember\b, \bwhat (did|have) (i|we) (talk|
    # discuss|say)\b) and no longer claim anything. Swapped for 2 phrases
    # confirmed claiming deterministically at confidence 1.0 AND confirmed
    # NOT an ask position (`PreClassifier._is_destructive_ask` returns
    # False for each, this session) — a destructive verb mentioned
    # mid-sentence, not heading the ask, via MEMORY_PATTERNS' surviving
    # \b(my|our) (conversation )?history\b and \bsearch (my |our )?
    # (conversation )?history\b literals.
    "can you show my history before i delete these old notes",
    "search my history before i cancel this project",
)
# Deliberately NOT in the keep set: "show me my cancelled meetings" and
# "what's the status of the delete feature" claim nothing at surface 1 BEFORE
# this change either (census baseline, 2026-09-13). Pinning them as keeps
# would assert a claim that never existed — they belong to the pre-existing
# surface-1 coverage gap, not to this narrowing. They ARE pinned below in
# TestBlockerIsPositionalNotVocabulary, where the claim under test is the
# guard's own verdict rather than a lane's.

# #1595 Phase 3 fourth deletion: TEMPORAL_READS and CALENDAR_READS excluded
# — neither TEMPORAL_PATTERNS nor CALENDAR_QUERY_PATTERNS claims anything at
# surface 1 any more (both tombstoned), so there is no claim left for this
# set to "keep". See TestTemporalReadsNowDeclineAtSurfaceOne below.
KEEP_CLAIMING = (STATUS_READS + MEMORY_READS) + READS_MENTIONING_DESTRUCTIVE_VERBS


def _single(phrase):
    return PreClassifier.pre_classify(phrase)


def _multi(phrase):
    return PreClassifier.detect_multiple_intents(phrase).intents


class TestDestructiveAsksFallThroughSingleIntentPath:
    """RED pre-fix: each phrase was claimed by a read lane at confidence 1.0.
    GREEN: no read-lane claim — the turn falls through surface 1."""

    @pytest.mark.parametrize("phrase", ALL_DESTRUCTIVE)
    def test_no_read_lane_claim(self, phrase):
        intent = _single(phrase)
        assert intent is None or intent.category not in READ_LANE_CATEGORIES, (
            f"read lane still claims the destructive ask {phrase!r} -> "
            f"{intent.category.value}/{intent.action}"
        )


class TestDestructiveAsksFallThroughMultiIntentPath:
    """The multi path is a live claim surface too — classify_multiple returns
    on any non-empty detection, so a claim here short-circuits the LLM lane
    exactly as the single path does."""

    @pytest.mark.parametrize("phrase", ALL_DESTRUCTIVE)
    def test_no_read_lane_claim(self, phrase):
        claimed = [i for i in _multi(phrase) if i.category in READ_LANE_CATEGORIES]
        assert claimed == [], (
            f"read lane still claims the destructive ask {phrase!r} on the "
            f"multi path -> {[f'{i.category.value}/{i.action}' for i in claimed]}"
        )


class TestReadsKeepTheirClaim:
    """No over-narrowing. Includes the reads that MENTION a destructive verb
    without being one — the shapes a vocabulary blocklist would have eaten."""

    @pytest.mark.parametrize("phrase", KEEP_CLAIMING)
    def test_single_intent_path_still_claims(self, phrase):
        intent = _single(phrase)
        assert intent is not None, f"read lost its claim: {phrase!r}"
        assert intent.category in READ_LANE_CATEGORIES
        assert intent.confidence == 1.0

    @pytest.mark.parametrize("phrase", KEEP_CLAIMING)
    def test_multi_intent_path_still_claims(self, phrase):
        claimed = [i for i in _multi(phrase) if i.category in READ_LANE_CATEGORIES]
        assert claimed, f"read lost its multi-path claim: {phrase!r}"


class TestTemporalReadsNowDeclineAtSurfaceOne:
    """#1595 Phase 3 fourth deletion (2026-10-01): pins the new reality for
    TEMPORAL_READS + CALENDAR_READS directly, rather than silently dropping
    their coverage when they left KEEP_CLAIMING above. Both
    TEMPORAL_PATTERNS and CALENDAR_QUERY_PATTERNS are tombstoned (`[]`) —
    these phrases decline at surface 1 UNCONDITIONALLY now (not because the
    destructive-ask blocker narrows them; there is no claim left to narrow).
    Correctness for these asks at runtime now lives at the Inversion layer
    (`consult_inversion_live`, flip_group `read_temporal`) when that group
    is live, or the LLM classifier as fallback — see
    docs/internal/architecture/current/intent-routing-stack.md's Phase 3
    "Fourth deletion" subsection."""

    _PHRASES = TEMPORAL_READS + CALENDAR_READS

    @pytest.mark.parametrize("phrase", _PHRASES)
    def test_single_intent_path_declines(self, phrase):
        assert _single(phrase) is None, f"{phrase!r} unexpectedly still claims at surface 1"

    @pytest.mark.parametrize("phrase", _PHRASES)
    def test_multi_intent_path_declines(self, phrase):
        claimed = [i for i in _multi(phrase) if i.category in READ_LANE_CATEGORIES]
        assert claimed == [], f"{phrase!r} unexpectedly still claims on the multi path: {claimed}"

    async def test_what_time_is_it_still_served_live_via_inversion(self, monkeypatch):
        """Plumbing attestation (never a live LLM call — the router is
        stubbed): "what time is it" declines at surface 1 above, and the
        Inversion still dispatches it when read_temporal is live, via the
        get_current_time_entry rail entry #1595 registered the same day."""
        from tests.unit.services.intent_service._inversion_pin_helper import (
            assert_inversion_routes,
        )

        await assert_inversion_routes(
            monkeypatch,
            "what time is it",
            live_categories="read_temporal",
            expected_action="get_current_time",
        )


class TestMemoryReadsNowDeclineAtSurfaceOne:
    """#1595 Phase 3 eleventh deletion (2026-10-03, PARTIAL): pins the new
    reality for the 8 MEMORY_READS phrases that left KEEP_CLAIMING above,
    rather than silently dropping their coverage. Unlike
    TestTemporalReadsNowDeclineAtSurfaceOne's full tombstone,
    MEMORY_PATTERNS is only PARTIALLY emptied — 3 literals survive — but
    none of these 8 phrases is covered by a surviving literal, so they
    decline at surface 1 unconditionally now too."""

    _PHRASES = MEMORY_READS_NOW_UNCLAIMED

    @pytest.mark.parametrize("phrase", _PHRASES)
    def test_single_intent_path_declines(self, phrase):
        assert _single(phrase) is None, f"{phrase!r} unexpectedly still claims at surface 1"

    @pytest.mark.parametrize("phrase", _PHRASES)
    def test_multi_intent_path_declines(self, phrase):
        claimed = [i for i in _multi(phrase) if i.category in READ_LANE_CATEGORIES]
        assert claimed == [], f"{phrase!r} unexpectedly still claims on the multi path: {claimed}"


class TestLocalGitStatusReadsNowDeclineAtSurfaceOne:
    """#1595 Phase 3 eighteenth deletion (2026-10-03, PARTIAL): pins the new
    reality for the 8 LOCAL_GIT_STATUS_READS_NOW_UNCLAIMED phrases that left
    KEEP_CLAIMING above, rather than silently dropping their coverage. Like
    MEMORY_PATTERNS' eleventh deletion, LOCAL_GIT_STATUS_PATTERNS is only
    PARTIALLY emptied — 1 literal survives (`\bbehind (?:main|origin|
    upstream|master)\b`) — but none of these 8 phrases is covered by the
    surviving literal, so they decline at surface 1 unconditionally now
    too. Correctness for these asks at runtime now lives at the Inversion
    layer (`consult_inversion_live`, flip_group `read_status`) when that
    group is live, or the LLM classifier as fallback."""

    _PHRASES = LOCAL_GIT_STATUS_READS_NOW_UNCLAIMED

    @pytest.mark.parametrize("phrase", _PHRASES)
    def test_single_intent_path_declines(self, phrase):
        assert _single(phrase) is None, f"{phrase!r} unexpectedly still claims at surface 1"

    @pytest.mark.parametrize("phrase", _PHRASES)
    def test_multi_intent_path_declines(self, phrase):
        claimed = [i for i in _multi(phrase) if i.category in READ_LANE_CATEGORIES]
        assert claimed == [], f"{phrase!r} unexpectedly still claims on the multi path: {claimed}"

    @pytest.mark.asyncio
    async def test_what_branch_still_served_live_via_inversion(self, monkeypatch):
        """Plumbing attestation (never a live LLM call — the router is
        stubbed): "what branch are we on" declines at surface 1 above, and
        the Inversion still dispatches it when read_status is live, via the
        local_git_status_query rail entry (unaffected by this deletion)."""
        from tests.unit.services.intent_service._inversion_pin_helper import (
            assert_inversion_routes,
        )

        await assert_inversion_routes(
            monkeypatch,
            "what branch are we on",
            live_categories="read_status",
            expected_action="local_git_status_query",
        )


class TestBlockerIsPositionalNotVocabulary:
    """The guard's contract, pinned directly: ASK position blocks, mention
    does not. This is what keeps the narrowing from becoming the blocklist
    #1527 proved cannot contain an open claim space."""

    @pytest.mark.parametrize(
        "phrase",
        [
            "delete my tasks",
            "please delete my tasks",
            "just clear my calendar",
            "can you delete my tasks",
            "could you please cancel my meetings",
            "i want to delete my tasks",
            "i need you to wipe my history",
            "let's clear my calendar",
            "help me delete my tasks",
            "get rid of my tasks",
        ],
    )
    def test_ask_position_blocks(self, phrase):
        assert PreClassifier._is_destructive_ask(phrase) is True

    @pytest.mark.parametrize(
        "phrase",
        [
            "what did i delete yesterday",
            "show me my cancelled tasks",
            "show me my cancelled meetings",
            "what meetings did i cancel yesterday",
            "do you remember what i deleted",
            "what did we discuss about deleting projects",
            "what's the status of the delete feature",
            "my tasks",
            "what time is it",
        ],
    )
    def test_mention_does_not_block(self, phrase):
        assert PreClassifier._is_destructive_ask(phrase) is False


class TestGateSeesTheFallThrough:
    """The point of the narrowing, at the rail layer.

    With surface 1 declining, a destructive ask reaches the LLM lane, whose
    emission dispatches the action rail — and every member of the delete-todo
    family (the rail family "delete my tasks" / "get rid of my tasks" lands
    in) is declared DESTRUCTIVE, which is exactly what derives the #1190
    ``needs_confirm`` verdict. m-43: this asserts the registry's declarations,
    not a live LLM round-trip.
    """

    def test_delete_todo_family_is_confirm_gated(self):
        from services.intent_service.destructive_confirm import _DELETE_TODO_FAMILY
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()  # idempotent; the registry is import-empty
        rail = get_action_workflows()
        missing = [a for a in _DELETE_TODO_FAMILY if a not in rail]
        assert not missing, f"delete-todo rail keys unregistered: {missing}"
        ungated = [a for a in _DELETE_TODO_FAMILY if not rail[a].needs_confirm]
        assert not ungated, (
            f"rail keys reachable after the #1756 fall-through are NOT #1190 "
            f"confirm-gated: {ungated}"
        )

    @pytest.mark.parametrize("phrase", ["delete my tasks", "get rid of my tasks"])
    def test_surface_one_leaves_the_turn_for_the_gate(self, phrase):
        """Both entry paths must be silent — a claim on EITHER one returns
        before the LLM call, so the gate never sees the action."""
        assert _single(phrase) is None
        assert _multi(phrase) == []


class TestGithubLaneDestructiveGreed1794:
    """#1794 — the fifth read lane, fixed with PER-CLAIM discrimination.

    #1756's blanket read-lane guard deliberately skipped GITHUB_QUERY because
    some of its claims are legitimately gated: `close_issue_query` /
    `reopen_issue_query` are registered DESTRUCTIVE rail keys, so their claims
    put the turn IN FRONT of the #1190 confirm gate rather than past it. The
    guard therefore discriminates by resolved ACTION: a destructive ask never
    rides out on a READ action; the gated rail claims pass unchanged.

    #1595 Phase 3 fifth deletion (2026-10-02): `GITHUB_QUERY_PATTERNS` is now
    `[]` (tombstoned) — `_github_read_claim_blocked` and this class's own
    per-claim discrimination are dead code (there is no claim left to
    discriminate). `test_gated_rail_claims_keep_their_lane` and
    `test_plain_reads_unchanged` below are converted to pin the new reality
    (decline on BOTH surfaces); `test_destructive_asks_fall_through_on_both_
    surfaces` is unaffected (these phrases already declined independently,
    as destructive asks). See `TestGithubPatternsNowDeclineAtSurfaceOne`
    below for the live-routes pins proving the plain-read destinations
    survive through the Inversion."""

    @pytest.mark.parametrize(
        "phrase",
        ["delete the next milestone", "delete my open issues"],
    )
    def test_destructive_asks_fall_through_on_both_surfaces(self, phrase):
        """THE #1794 pins — the issue's own probe table, inverted: the user who
        asks to delete their issues must never be answered with a listing."""
        assert _single(phrase) is None
        assert _multi(phrase) == []

    @pytest.mark.parametrize(
        "phrase,action",
        [("close issue 42", "close_issue_query"), ("reopen issue 42", "reopen_issue_query")],
    )
    def test_gated_rail_claims_keep_their_lane(self, phrase, action):
        """#1595 Phase 3 fifth deletion: GITHUB_QUERY_PATTERNS is tombstoned
        — close/reopen no longer claim at surface 1 on EITHER path (and
        neither has a registered flip_group, so there is no zero-LLM path
        for them either — the discovered gap this deletion's #1739 arm-step
        conversion also found, see test_acceptance_contract_1739.py)."""
        assert _single(phrase) is None
        assert _multi(phrase) == []

    @pytest.mark.parametrize(
        "phrase,action",
        [
            ("how many open issues do we have", "list_issues_query"),
            ("show me stale prs", "stale_prs_query"),
        ],
    )
    def test_plain_reads_unchanged(self, phrase, action):
        """#1595 Phase 3 fifth deletion: these reads no longer claim at
        surface 1 either — the whole list is tombstoned, not just the
        destructive-greed-adjacent vocabulary this test originally guarded."""
        assert _single(phrase) is None
        assert _multi(phrase) == []

    def test_close_family_is_actually_gated_not_assumed(self):
        """The discrimination is only safe because these rail keys really are
        confirm-gated — assert the registry, not the comment (m-43)."""
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()
        rail = get_action_workflows()
        from services.intent_service.pre_classifier import PreClassifier

        for action in PreClassifier._GITHUB_GATED_RAIL_ACTIONS:
            assert action in rail, f"{action} not a registered rail key"
            assert rail[action].needs_confirm, f"{action} is not #1190 confirm-gated"


class TestGithubPatternsNowDeclineAtSurfaceOne:
    """#1595 Phase 3 fifth deletion (2026-10-02): the plain-read destinations
    `TestGithubLaneDestructiveGreed1794.test_plain_reads_unchanged` used to
    pin still route correctly through the Inversion's live consult (stubbed
    router — no LLM call, ever), proving list_issues_query/stale_prs_query
    didn't just vanish when GITHUB_QUERY_PATTERNS emptied."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "phrase,action",
        [
            ("how many open issues do we have", "list_issues_query"),
            ("show me stale prs", "stale_prs_query"),
        ],
    )
    async def test_routes_live(self, monkeypatch, phrase, action):
        from tests.unit.services.intent_service._inversion_pin_helper import (
            assert_inversion_routes,
        )

        await assert_inversion_routes(
            monkeypatch,
            phrase,
            live_categories="read_status",
            expected_action=action,
        )
