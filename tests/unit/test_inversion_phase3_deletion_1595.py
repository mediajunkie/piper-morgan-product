"""#1595 Phase 3 — pinning tests for the deletion-ratchet INSTRUMENT
(scripts/inversion_phase3_deletion_gate.py).

Epic-0's own conditions on the endpoint (dev/2026/09/25/inversion-epic0-
remaining-scope-2026-09-25.md, unit 5; issue #1595 body): "Deletion ratchet
asserts corpus non-regression ALONGSIDE shrink" and "pattern-to-corpus-case
conversion is a STEP IN the deletion procedure, not an intention." This
suite pins the census mechanics (real corpus, real pre-classifier, real
router reports, NO LLM calls anywhere here) and the non-regression checker
that a future deletion commit's ratchet test will lean on.

This suite does not itself delete anything (that happened in
``services/intent_service/pre_classifier.py``, same commit). As of
2026-10-03 ``DELETED_PATTERN_LISTS`` carries NINETEEN real entries — the
thirteen below plus the same-day thirteenth-through-eighteenth batch
(CONTEXTUAL_QUERY_PATTERNS, SESSION_ACTIVITY_QUERY_PATTERNS,
INSIGHT_PULL_PATTERNS, GET_DEFAULT_REPO_PATTERNS, and
PRODUCTIVITY_QUERY_PATTERNS, all FULL, plus LOCAL_GIT_STATUS_PATTERNS, the
SEVENTH partial — see ``test_real_ledger_has_the_first_nineteen_deletions``
for the full per-entry account, including PRODUCTIVITY_QUERY_PATTERNS'
deletion resolving a temporary disagreeing reabsorption INSIGHT_PULL_
PATTERNS' own entry had flagged two lists earlier). The paragraph below
describes the first thirteen entries only (REMINDER_PATTERNS,
REMINDER_QUERY_PATTERNS, TODO_QUERY_PATTERNS,
CALENDAR_QUERY_PATTERNS, TEMPORAL_PATTERNS, GITHUB_QUERY_PATTERNS,
PRIORITY_PATTERNS — all emptied to ``[]``, kept as tombstones — and
STATUS_PATTERNS, GUIDANCE_PATTERNS, DISCOVERY_PATTERNS, TRUST_PATTERNS,
MEMORY_PATTERNS, and ANALYSIS_PATTERNS, the six PARTIAL deletions so far:
STATUS_PATTERNS, 52 of 56 literals deleted, 4 load-bearing literals SURVIVE;
GUIDANCE_PATTERNS, 18 of 21 literals deleted, 3 load-bearing literals
SURVIVE; DISCOVERY_PATTERNS, 19 of 20 literals deleted, 1 load-bearing
literal SURVIVES (\\bneed\\s*help\\b); TRUST_PATTERNS, 15 of 16 literals
deleted, 1 load-bearing literal SURVIVES (\\bwhy can'?t you\\b);
MEMORY_PATTERNS, 12 of 15 literals deleted, 3 load-bearing literals SURVIVE
(\\b(my|our) (conversation )?history\\b, \\bsearch (my |our )?(conversation
)?history\\b, \\bwhat (i|we) (said|talked|discussed)\\b); ANALYSIS_PATTERNS,
12 of 16 literals deleted, 4 load-bearing literals SURVIVE
(\\bwhat.*obstacle\\b, \\bwhat'?s in the way\\b, \\banalyze.*(?:risk|impact
|blocker|bottleneck)\\b, \\bimpact analysis\\b) — in all six cases the class
attribute is NOT emptied to ``[]``, it keeps exactly its survivors — see
``entry["partial"]`` / ``entry["surviving_literals"]``).
``TestNonRegressionMechanism`` still proves the non-regression MECHANISM
against synthetic entries (never the real ledger); ``TestDeletedPatternListsLedger``
now also proves the real ledger's ten entries actually pass it — including
TODO_QUERY_PATTERNS' one documented ``known_reabsorptions`` exception ("what
should I do next" reclaimed by PRIORITY_PATTERNS, a pre-existing shadowed
duplicate literal that AGREES with the ruled destination — now moot, since
PRIORITY_PATTERNS is itself deleted below), CALENDAR_QUERY_PATTERNS' 19
documented ``known_reabsorptions`` exceptions (TEMPORAL_PATTERNS reclaimed
these as ``get_current_time`` before TEMPORAL_PATTERNS was itself deleted —
reported with ``"agrees": false``, never silenced, and now also marked
``resolved_by`` since the reclaiming list is gone and the phrases are
genuinely unclaimed again), TEMPORAL_PATTERNS' own entry, whose 69 claimed
rows include the same 19 ex-CALENDAR phrases (reabsorbed, all disagreeing)
plus 5 rows passing via a THIRD documented shape, ``misserved_at_deletion``
(the deleted pattern's own claim disagreed with the ruled destination AND
the router independently declined — deletion licensed because removing a
deterministically-wrong fallback cannot regress a row that was already
unserved correctly; see ``check_deleted_entry_non_regression``'s docstring),
GITHUB_QUERY_PATTERNS' own entry (66 claimed rows, all its own — no
sibling reabsorption existed at deletion time, unlike CALENDAR/TEMPORAL),
whose ONE post-deletion ``known_reabsorptions`` entry ("any update on the
next milestone" reclaimed by STATUS_PATTERNS's pre-existing ``\bnext
milestone\b`` literal) is the SAME agreeing-reclaim shape TODO_QUERY_PATTERNS
first exercised, not a new mechanism, and PRIORITY_PATTERNS' own entry (42
claimed rows, all its own; 2 rows via ``misserved_at_deletion``, and — a
FOURTH documented shape, ``surface2_verified_at_deletion`` — 2 rows licensed
under Arch's 2026-10-02 condition (d): the router mismatched to a non-live
op, but a frozen N=5 surface-2 probe shows the LLM classifier reaching the
destination's own FLOOR category on every sample, so the pattern was never
load-bearing; see ``check_deleted_entry_non_regression``'s docstring for why
the re-verified invariant is the same narrow "still unclaimed" check
``misserved_at_deletion`` uses, never a re-derivation of the probe proof
itself). CALENDAR's and TEMPORAL's entries are the first two to require the
live-flag ``cats`` parameter (their MISMATCH-but-live-route rows need
``read_temporal`` in the live set); the other six (including
GITHUB_QUERY_PATTERNS, PRIORITY_PATTERNS, and STATUS_PATTERNS) never
strictly needed it but are still checked with ``_LIVE_CATS`` for
consistency with production's actual live flag.

STATUS_PATTERNS' own entry (2026-10-02, seventh deletion) is the FIRST
PARTIAL one: ``entry["partial"]`` is ``True`` and ``entry["surviving_literals"]``
names the 4 literals the class attribute still carries (the attribute is
NOT emptied to ``[]``). Its 48 ``rows_claimed_at_deletion`` split across
every documented shape this suite already covers (18 live-group MATCH, 4
ruled-floor MATCH, 9 ``misserved_at_deletion``, 17 ``surface2_verified_at_deletion``)
plus a FIFTH shape in ``shadowed_literals``: 3 of its unexercised literals
are CROSS-LIST shadowed — byte-identical duplicates of literals inside the
inline (non-class-attribute) ``MILESTONE_STATUS_INLINE_PATTERNS`` check in
``pre_classifier.py`` (Issue #1068), checked BEFORE ``STATUS_PATTERNS`` in
``pre_classify``'s if-chain, so those 3 STATUS_PATTERNS copies could never
fire regardless of this deletion — confirmed via
``PreClassifier.pre_classify_with_pattern_list`` (the real production
if-chain), not ``_first_pattern_match`` against ``STATUS_PATTERNS`` alone
(which only proves reachability WITHIN one list and wrongly flagged these
three as needing a corpus deposit on a first pass).

GUIDANCE_PATTERNS' own entry (2026-10-02, eighth deletion) is the SECOND
PARTIAL one: ``entry["partial"]`` is ``True`` and ``entry["surviving_literals"]``
names the 3 literals the class attribute still carries. Its 18
``rows_claimed_at_deletion`` split across 17 ``surface2_verified_at_deletion``
rows (a frozen N=5 surface-2 probe, both provider legs, 10/10 combined per
phrase, landing the phrase in the GUIDANCE category) and 1
``misserved_at_deletion`` row ("just getting started here": the deleted
``\bgetting started\b`` literal claims ``get_contextual_guidance``,
disagreeing with the ruled ``action:greeting``). ``shadowed_literals`` is
empty for this entry — all 18 deleted literals were exercised 1:1 by a
claimed row and ``claim_for_phrase``'s real if-chain attributed every one of
the 21 claimed rows to GUIDANCE_PATTERNS itself, so no cross-list shadowing
was found. ``known_reabsorptions`` is also empty: zero reabsorptions across
all 18 deleted-literal rows post-deletion. A prior same-day attempt at a
FULL deletion of this list had STOPPED on 4 disagreeing reabsorptions via
STATUS_PATTERNS's then-live ``\bmy projects\b``/``\bmy portfolio\b``
literals; STATUS_PATTERNS's own seventh deletion removed both literals
first, and this PARTIAL additionally keeps GUIDANCE's own setup/portfolio
literals alive regardless, so the collision cannot recur.

DISCOVERY_PATTERNS' own entry (2026-10-03, ninth deletion) is the THIRD
PARTIAL one: ``entry["partial"]`` is ``True`` and ``entry["surviving_literals"]``
names the 1 literal (\\bneed\\s*help\\b) the class attribute still carries.
Its 19 ``rows_claimed_at_deletion`` are ALL live-group MATCH/REVIEW-agrees
rows (18 MATCH + 1 REVIEW-agrees — get_capabilities is itself a LIVE op
under the dispatch's --live set, and the router actually serves it live on
every one of these rows), so unlike STATUS/GUIDANCE neither
``surface2_verified_at_deletion`` nor ``misserved_at_deletion`` has any
entries here — no row needed a surface-2 floor probe or a mis-serve
licence. ``shadowed_literals`` is empty: all 20 literals (19 deleted + the
1 survivor) were exercised 1:1 by a claimed row (confirmed via
``unexercised_literals("DISCOVERY_PATTERNS", lv.rows)`` returning zero), so
no cross-list shadowing was found and no corpus deposit was needed.
``known_reabsorptions`` is also empty: zero reabsorptions across all 19
deleted-literal rows post-deletion (checked both entry surfaces via
``claim_for_phrase``).

TRUST_PATTERNS' own entry (2026-10-03, tenth deletion) is the FOURTH PARTIAL
one: ``entry["partial"]`` is ``True`` and ``entry["surviving_literals"]``
names the 1 literal (\\bwhy can'?t you\\b) the class attribute still
carries. Its 15 ``rows_claimed_at_deletion`` split across 14 live-group MATCH
rows (explain_trust/get_capabilities/pull_insights are all live under this
flag) and 1 ``misserved_at_deletion`` row ("why are you always cautious
about this suggestion": TRUST_PATTERNS's claim disagrees with the ruled
``action:explain_suggestion``; the router independently reaches
explain_suggestion@0.95 live, and a frozen N=10 surface-2 probe does NOT
show the LLM classifier landing PROVENANCE on every sample — 0/10 — so the
surface2_verified_at_deletion escape does not apply and the row passes via
the mis-serve rule instead). ``surface2_verified_at_deletion`` is empty for
this entry — the one row that attempted that escape failed its probe.
``shadowed_literals`` is empty: all 16 literals (15 deleted + the 1
survivor) were exercised 1:1 by a claimed row (confirmed via
``unexercised_literals("TRUST_PATTERNS", lv.rows)`` returning zero), so no
cross-list shadowing was found and no corpus deposit was needed.
``known_reabsorptions`` is also empty: zero reabsorptions across all 15
deleted-literal rows post-deletion (checked both entry surfaces via
``claim_for_phrase``).

MEMORY_PATTERNS' own entry (2026-10-03, eleventh deletion) is the FIFTH
PARTIAL one: ``entry["partial"]`` is ``True`` and ``entry["surviving_literals"]``
names the 3 literals (\\b(my|our) (conversation )?history\\b, \\bsearch (my
|our )?(conversation )?history\\b, \\bwhat (i|we) (said|talked|discussed)\\b)
the class attribute still carries. Its 11 ``rows_claimed_at_deletion`` split
across 10 live-group MATCH rows and 1 ``misserved_at_deletion`` row
("remember when we shipped the last release?": MEMORY_PATTERNS's claim
(get_memory) disagrees with the ruled ``action:check_completion_status``;
the router independently MATCHes check_completion_status@0.85 on a
non-live op, and a frozen N=10 surface-2 probe does NOT show the LLM
classifier landing STATUS on every sample — 0/10 — so the
surface2_verified_at_deletion escape does not apply and the row passes via
the mis-serve rule instead). ``surface2_verified_at_deletion`` is empty for
this entry. ``shadowed_literals`` carries ONE entry — unlike the prior four
partials, MEMORY_PATTERNS has a genuinely UNEXERCISED literal
(\\bhow (much|far back) do you remember\\b, confirmed via
``unexercised_literals("MEMORY_PATTERNS", lv.rows)`` returning exactly this
one) that is PROVABLY SHADOWED within the same list by its own earlier
sibling \\bdo you remember\\b (checked before it in list order, and a
guaranteed substring of every phrase the unexercised literal would ever
match) — confirmed via ``PreClassifier.pre_classify_with_pattern_list``
against candidate phrasings ("how much do you remember", "how far back do
you remember", etc.), never claimed by the shadowed literal. \\bdo you
remember\\b is itself also deleted (not a survivor), so the shadowing
changes nothing about this deletion's safety; no corpus deposit was
needed. ``known_reabsorptions`` carries ONE entry: "can you show my
conversation history" (formerly claimed by the deleted
\\b(show|view|see) ... history\\b literal) is reabsorbed by the surviving
\\b(my|our) (conversation )?history\\b literal — AGREEING (same action
get_memory, same list). The other 10 deleted-literal rows plus both of the
shadowed literal's candidate phrasings are genuinely UNCLAIMED post-deletion
(checked both entry surfaces via ``claim_for_phrase``).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import inversion_phase0_baseline as p0  # noqa: E402
import inversion_phase3_deletion_gate as gate  # noqa: E402
import inversion_phase3_surface2_floor_probe as s2  # noqa: E402
import pattern_literal_counts  # noqa: E402

from services.intent_service.pre_classifier import PreClassifier  # noqa: E402


def _write_probe_file(tmp_path, rows, name="probe.md"):
    """#1933: a minimal frozen surface-2 probe file for monkeypatching
    gate.SURFACE2_FLOOR_PROBES — same idiom
    test_inversion_phase3_surface2_floor_1595.py's ``_probe_file`` uses."""
    for r in rows:
        r.setdefault("served", "stub:stub-model")  # a served line is required (Arch condition 1)
    out = tmp_path / name
    s2.write_report(rows, out, samples=max(r["sample"] for r in rows))
    return out


# ── (a) the census runs over the REAL corpus and REAL pre-classifier, and
#        its denominators add up ────────────────────────────────────────────


class TestCensusDenominators:
    def test_claimed_plus_unclaimed_equals_corpus_size(self):
        records, by_list = gate.build_census(cats=None)
        corpus_size = len(p0.load_corpus())
        assert len(records) == corpus_size, "one record per corpus row"

        claimed = sum(1 for r in records if r.claim.pattern_list is not None)
        unclaimed = sum(1 for r in records if r.claim.pattern_list is None)
        assert claimed + unclaimed == len(records)
        assert claimed + unclaimed == 500, (
            "the corpus was 500 rows as of the 2026-10-05 list_repos not-found deposit "
            "(+2 PORTFOLIO rows, CXO's ruling §1a: 'list my repos on github' / 'show all "
            "of my repos', expected action:list_repos); before that 498 after the "
            "2026-10-04 PORTFOLIO update/edit-project dead-claim deposit (+2 floor rows, "
            "Arch's ruling); before that 496 after the 2026-10-03 six-list "
            "(CONTEXTUAL_QUERY/GET_DEFAULT_REPO/INSIGHT_PULL/LOCAL_GIT_STATUS/"
            "PRODUCTIVITY_QUERY/SESSION_ACTIVITY_QUERY) phase3-conversion deposit "
            "(#1595 epic-0 unit 5: 457 + 39 new claimed rows = 496, claimed 75 -> 114, "
            "unclaimed unchanged at 382); if this drifts, the corpus grew/shrank — "
            "update the pinned number in the same commit as the corpus change, don't "
            "just widen this test"
        )

    def test_every_claimed_row_has_a_pattern_list_with_a_literal_count(self):
        """A row claimed by a list that per_list_literal_counts() cannot see
        (a synthetic/non-class-attribute name, e.g. MILESTONE_STATUS_INLINE_
        PATTERNS) is allowed — the gate defaults its literal count to 0 —
        but every OTHER claimed row's list must resolve to a real, counted
        `*PATTERNS` class attribute. This is the vacuity guard the census
        table's per-list literal column depends on."""
        records, by_list = gate.build_census(cats=None)
        literal_counts = pattern_literal_counts.per_list_literal_counts()
        claimed_lists = {r.claim.pattern_list for r in records if r.claim.pattern_list}
        unresolvable = claimed_lists - set(literal_counts) - {"MILESTONE_STATUS_INLINE_PATTERNS"}
        assert not unresolvable, (
            f"claimed pattern-list name(s) with no literal count and no known "
            f"synthetic-name exemption: {unresolvable} — either "
            f"per_list_literal_counts() needs to see this list, or "
            f"pre_classify_with_pattern_list's synthetic-name docstring "
            f"needs updating (and this test's exemption set with it)"
        )

    def test_every_list_in_by_list_carries_its_real_literal_count(self):
        """by_list's literal_count for every REAL (non-synthetic) list must
        equal the extraction ratchet's own count for that list — the same
        number TestExtractionPatternRatchet sums to 567. A mismatch here
        would mean the deletion gate's 'ceiling 567 -> 567-N' arithmetic is
        wrong."""
        _records, by_list = gate.build_census(cats=None)
        literal_counts = pattern_literal_counts.per_list_literal_counts()
        for name, count in literal_counts.items():
            if name in by_list:
                assert by_list[name].literal_count == count, name


# ── (b) DELETED_PATTERN_LISTS — empty today; the non-regression MECHANISM
#        is proven with a synthetic entry, never the real ledger ───────────


class TestDeletedPatternListsLedger:
    # The exact --live categories every Phase-3 deletion gate run has used
    # throughout this epic (2026-10-01: promoted to a shared constant,
    # gate.CURRENT_LIVE_CATEGORIES, when TestChatPointersReachabilityRatchet
    # needed the identical set — see that constant's own docstring). Threaded
    # into check_deleted_entry_non_regression for every entry below —
    # harmless for REMINDER_PATTERNS/REMINDER_QUERY_PATTERNS/
    # TODO_QUERY_PATTERNS (none of their rows ever need a live condition to
    # pass) and REQUIRED for CALENDAR_QUERY_PATTERNS' and TEMPORAL_PATTERNS'
    # MISMATCH-but-live-route rows.
    _LIVE_CATS = gate.CURRENT_LIVE_CATEGORIES

    def test_real_ledger_has_the_first_nineteen_deletions(self):
        """2026-09-27, #1595 Phase 3: REMINDER_PATTERNS (5 literals) and
        REMINDER_QUERY_PATTERNS (4 literals) were emptied first, then
        TODO_QUERY_PATTERNS (10 literals) on 2026-09-28, then
        CALENDAR_QUERY_PATTERNS (52 literals) and TEMPORAL_PATTERNS (56
        literals) on 2026-10-01, then GITHUB_QUERY_PATTERNS (64 literals) and
        PRIORITY_PATTERNS (47 literals) on 2026-10-02 — all emptied to `[]` in
        services/intent_service/pre_classifier.py (kept as tombstones — the
        class attributes and their consumer code paths survive; only the
        literals were deleted). Then STATUS_PATTERNS (56 literals) on
        2026-10-02, the FIRST PARTIAL deletion: 52 literals deleted, 4
        SURVIVE (the class attribute is NOT emptied to `[]` — it keeps
        exactly the 4 load-bearing literals; see ``entry["partial"]`` and
        ``entry["surviving_literals"]`` on that entry). Then GUIDANCE_PATTERNS
        (21 literals) on 2026-10-02, the SECOND PARTIAL deletion: 18 literals
        deleted, 3 SURVIVE. Then DISCOVERY_PATTERNS (20 literals) on
        2026-10-03, the THIRD PARTIAL deletion: 19 literals deleted, 1
        SURVIVES (\\bneed\\s*help\\b). Then TRUST_PATTERNS (16 literals) on
        2026-10-03, the FOURTH PARTIAL deletion: 15 literals deleted, 1
        SURVIVES (\\bwhy can'?t you\\b). Then MEMORY_PATTERNS (15 literals) on
        2026-10-03, the FIFTH PARTIAL deletion: 12 literals deleted, 3
        SURVIVE (\\b(my|our) (conversation )?history\\b, \\bsearch (my
        |our )?(conversation )?history\\b, \\bwhat (i|we)
        (said|talked|discussed)\\b). Then ANALYSIS_PATTERNS (16 literals) on
        2026-10-03, the SIXTH PARTIAL deletion: 12 literals deleted, 4
        SURVIVE (\\bwhat.*obstacle\\b, \\bwhat'?s in the way\\b,
        \\banalyze.*(?:risk|impact|blocker|bottleneck)\\b,
        \\bimpact analysis\\b). Then, same day, the thirteenth-through-
        eighteenth deletions (#1595 Phase 3's 2026-10-03 six-list batch):
        CONTEXTUAL_QUERY_PATTERNS (13 literals, FULL), SESSION_ACTIVITY_
        QUERY_PATTERNS (6, FULL), INSIGHT_PULL_PATTERNS (7, FULL),
        GET_DEFAULT_REPO_PATTERNS (5, FULL), PRODUCTIVITY_QUERY_PATTERNS
        (4, FULL — this one RESOLVED a temporary disagreeing reabsorption
        INSIGHT_PULL_PATTERNS' own entry had flagged two lists earlier; see
        that entry's ``known_reabsorptions`` ``resolved_by`` field), and
        LOCAL_GIT_STATUS_PATTERNS (12 literals, the SEVENTH PARTIAL
        deletion: 11 deleted, 1 SURVIVES — \\bbehind (?:main|origin|
        upstream|master)\\b). This assertion is pinned to the
        CURRENT ledger contents, per this test's own prior docstring ("this
        assertion needs updating in the SAME commit as the deletion") — a
        future deletion updates it again, in that commit."""
        entries = gate.load_deleted_pattern_lists()
        names = {e["list"] for e in entries}
        assert names == {
            "REMINDER_PATTERNS",
            "REMINDER_QUERY_PATTERNS",
            "TODO_QUERY_PATTERNS",
            "CALENDAR_QUERY_PATTERNS",
            "TEMPORAL_PATTERNS",
            "GITHUB_QUERY_PATTERNS",
            "PRIORITY_PATTERNS",
            "STATUS_PATTERNS",
            "GUIDANCE_PATTERNS",
            "DISCOVERY_PATTERNS",
            "TRUST_PATTERNS",
            "MEMORY_PATTERNS",
            "ANALYSIS_PATTERNS",
            "CONTEXTUAL_QUERY_PATTERNS",
            "SESSION_ACTIVITY_QUERY_PATTERNS",
            "INSIGHT_PULL_PATTERNS",
            "GET_DEFAULT_REPO_PATTERNS",
            "PRODUCTIVITY_QUERY_PATTERNS",
            "LOCAL_GIT_STATUS_PATTERNS",
        }, (
            f"DELETED_PATTERN_LISTS contents changed — update this pin in the "
            f"same commit as the ledger change. Got: {sorted(names)}"
        )
        status_entry = next(e for e in entries if e["list"] == "STATUS_PATTERNS")
        assert status_entry.get("partial") is True
        assert (
            status_entry.get("literals") == 52
        ), "literals is the DELETED count, not the original 56"
        assert set(status_entry.get("surviving_literals", {})) == {
            r"\bnext milestone\b",
            r"\bcurrent work\b",
            r"\bproject overview\b",
            r"\bproject landscape\b",
        }
        guidance_entry = next(e for e in entries if e["list"] == "GUIDANCE_PATTERNS")
        assert guidance_entry.get("partial") is True
        assert (
            guidance_entry.get("literals") == 18
        ), "literals is the DELETED count, not the original 21"
        assert set(guidance_entry.get("surviving_literals", {})) == {
            r"\bsetup.*projects?\b",
            r"\bset up.*projects?\b",
            r"\bset up.*portfolio\b",
        }
        discovery_entry = next(e for e in entries if e["list"] == "DISCOVERY_PATTERNS")
        assert discovery_entry.get("partial") is True
        assert (
            discovery_entry.get("literals") == 19
        ), "literals is the DELETED count, not the original 20"
        assert set(discovery_entry.get("surviving_literals", {})) == {
            r"\bneed\s*help\b",
        }
        trust_entry = next(e for e in entries if e["list"] == "TRUST_PATTERNS")
        assert trust_entry.get("partial") is True
        assert (
            trust_entry.get("literals") == 15
        ), "literals is the DELETED count, not the original 16"
        assert set(trust_entry.get("surviving_literals", {})) == {
            r"\bwhy can'?t you\b",
        }
        memory_entry = next(e for e in entries if e["list"] == "MEMORY_PATTERNS")
        assert memory_entry.get("partial") is True
        assert (
            memory_entry.get("literals") == 12
        ), "literals is the DELETED count, not the original 15"
        assert set(memory_entry.get("surviving_literals", {})) == {
            r"\b(my|our) (conversation )?history\b",
            r"\bsearch (my |our )?(conversation )?history\b",
            r"\bwhat (i|we) (said|talked|discussed)\b",
        }
        analysis_entry = next(e for e in entries if e["list"] == "ANALYSIS_PATTERNS")
        assert analysis_entry.get("partial") is True
        assert (
            analysis_entry.get("literals") == 12
        ), "literals is the DELETED count, not the original 16"
        assert set(analysis_entry.get("surviving_literals", {})) == {
            r"\bwhat.*obstacle\b",
            r"\bwhat'?s in the way\b",
            r"\banalyze.*(?:risk|impact|blocker|bottleneck)\b",
            r"\bimpact analysis\b",
        }
        contextual_entry = next(e for e in entries if e["list"] == "CONTEXTUAL_QUERY_PATTERNS")
        assert contextual_entry.get("partial") is not True
        assert contextual_entry.get("literals") == 13
        session_activity_entry = next(
            e for e in entries if e["list"] == "SESSION_ACTIVITY_QUERY_PATTERNS"
        )
        assert session_activity_entry.get("partial") is not True
        assert session_activity_entry.get("literals") == 6
        insight_pull_entry = next(e for e in entries if e["list"] == "INSIGHT_PULL_PATTERNS")
        assert insight_pull_entry.get("partial") is not True
        assert insight_pull_entry.get("literals") == 7
        assert (
            insight_pull_entry["known_reabsorptions"][
                "what insights do you have about my productivity"
            ]["resolved_by"]
            == "PRODUCTIVITY_QUERY_PATTERNS deletion 2026-10-03"
        )
        get_default_repo_entry = next(
            e for e in entries if e["list"] == "GET_DEFAULT_REPO_PATTERNS"
        )
        assert get_default_repo_entry.get("partial") is not True
        assert get_default_repo_entry.get("literals") == 5
        assert set(get_default_repo_entry.get("shadowed_literals", {})) == {
            r"\bwhat\s+default\s+repo(?:sitory)?\b",
        }
        productivity_entry = next(e for e in entries if e["list"] == "PRODUCTIVITY_QUERY_PATTERNS")
        assert productivity_entry.get("partial") is not True
        assert productivity_entry.get("literals") == 4
        assert (
            "what insights do you have about my productivity"
            in productivity_entry["misserved_at_deletion"]
        )
        local_git_status_entry = next(
            e for e in entries if e["list"] == "LOCAL_GIT_STATUS_PATTERNS"
        )
        assert local_git_status_entry.get("partial") is True
        assert (
            local_git_status_entry.get("literals") == 11
        ), "literals is the DELETED count, not the original 12"
        assert set(local_git_status_entry.get("surviving_literals", {})) == {
            r"\bbehind (?:main|origin|upstream|master)\b",
        }

    def test_real_ledger_entries_pass_non_regression(self):
        """Every entry in the real (now non-empty) ledger passes
        non-regression: neither deleted list's claimed phrases is
        re-claimed by an UNDOCUMENTED surviving surface-1 list, and each is
        still a corpus row scoring MATCH, an agreeing REVIEW, or a
        live-MISMATCH (the router's own route is itself a live op) under
        the SAME --live categories the CALENDAR_QUERY_PATTERNS gate run
        used. This is the real deletion evidence, not the synthetic proof
        (TestNonRegressionMechanism, below) that the mechanism works."""
        entries = gate.load_deleted_pattern_lists()
        assert entries, "expected the seven real entries — ledger is empty"
        for entry in entries:
            ok, problems = gate.check_deleted_entry_non_regression(entry, cats=self._LIVE_CATS)
            assert ok, f"{entry.get('list')}: {problems}"

    def test_calendar_entry_fails_non_regression_without_the_live_flag(self):
        """The CALENDAR_QUERY_PATTERNS entry's 3 MISMATCH-but-live-route rows
        (1 unclaimed, 2 reclaimed-but-independently-reproved) genuinely
        NEED read_temporal in the live set — this is not a decorative
        parameter. Proven here so a future refactor that silently drops the
        cats threading is caught: the SAME entry that passes with
        ``_LIVE_CATS`` must fail without it."""
        entries = {e["list"]: e for e in gate.load_deleted_pattern_lists()}
        entry = entries["CALENDAR_QUERY_PATTERNS"]
        ok, problems = gate.check_deleted_entry_non_regression(entry)  # cats=None
        assert not ok
        # Was 3 when written; the mis-serve rule (same morning) resolved one
        # without the live set, and the 2026-10-02 MATCH-on-non-live rule
        # made EVERY MATCH row depend on the live set too (a MATCH is only
        # "the consult owns it" when the op is live — unknowable without the
        # flag). The property pinned is "needs the flag", not the count.
        assert len(problems) >= 1, problems
        assert all("live-set-unknown" in p for p in problems), problems

    def test_calendar_entry_known_reabsorptions_are_all_documented_disagreements(self):
        """#1595 Phase 3 third deletion's defining finding: TEMPORAL_PATTERNS
        reabsorbs 19 of CALENDAR_QUERY_PATTERNS' 49 claimed phrases as
        ``get_current_time`` — NONE of them agree with the ruled
        destination. Pinned so a future router/prompt change that makes one
        of these agree (or disagree differently) is visible, not silently
        absorbed into a passing suite."""
        entries = {e["list"]: e for e in gate.load_deleted_pattern_lists()}
        entry = entries["CALENDAR_QUERY_PATTERNS"]
        reabsorptions = entry["known_reabsorptions"]
        assert len(reabsorptions) == 19, sorted(reabsorptions)
        for phrase, info in reabsorptions.items():
            assert info["reclaimed_by"] == "TEMPORAL_PATTERNS", phrase
            assert info["claimed_action"] == "get_current_time", phrase
            assert info["agrees"] is False, phrase


class TestNonRegressionMechanism:
    """Proves check_deleted_entry_non_regression's TWO failure modes fire —
    against SYNTHETIC entries only. Never touches the real (empty) ledger."""

    def test_passes_for_a_phrase_still_matching_and_unclaimed(self):
        # "who am I?" is a real corpus row (IDENTITY, action:get_identity)
        # that scores MATCH in the 09-25 full report — and, measured
        # directly, is NOT claimed by IDENTITY_PATTERNS or any other
        # surface-1 list today (only its sibling "who are you?" is; a real
        # finding of the census, not a fixture artifact). It is therefore a
        # genuinely clean stand-in for "the deleted list's phrase is
        # unclaimed post-deletion and still scores MATCH".
        # 2026-10-02: under the MATCH-on-non-live rule a MATCH is "the consult
        # owns it" only for a LIVE op, so the stand-in must be a live one —
        # "what time is it?" (get_current_time, read_temporal, MATCH@0.99,
        # unclaimed since the TEMPORAL deletion) — checked WITH the live set.
        # "who am I?" (get_identity, a floor op) would now need a surface-2
        # probe, which is the rule working, not the fixture breaking.
        phrase = "what time is it?"
        assert (
            gate.claim_for_phrase(PreClassifier, phrase).pattern_list is None
        ), "test fixture assumption broke — pick another unclaimed live MATCH row"
        entry = {
            "list": "SYNTHETIC_NEVER_CLAIMED_LIST",
            "rows_claimed_at_deletion": [phrase],
        }
        ok, problems = gate.check_deleted_entry_non_regression(
            entry, cats=gate.CURRENT_LIVE_CATEGORIES
        )
        assert ok, problems

    def test_fails_when_phrase_is_claimed_by_a_surviving_list(self):
        # SET_DEFAULT_REPO_PATTERNS genuinely claims the #1606 plan-row
        # phrase below today (verified by the census — unaffected by any of
        # the six deletions; STATUS_PATTERNS/GUIDANCE_PATTERNS deliberately
        # NOT used here — both are the next two lists scheduled for
        # deletion in this epic, so a fixture built on either would just
        # break again next session). Naming that SAME list as the "deleted"
        # one in a synthetic entry must fail loud — the list obviously was
        # not deleted (it still claims), so a real deletion commit that
        # forgot to actually remove the list would be caught here. (Was
        # PRIORITY_PATTERNS/"what should I do next" before #1595 Phase 3's
        # sixth deletion emptied PRIORITY_PATTERNS itself, which broke this
        # fixture's own premise — the same shape TEMPORAL_PATTERNS'
        # deletion caused here before it, when this fixture was
        # TEMPORAL_PATTERNS/"when is my next meeting?".)
        phrase = (
            'please clear the reminders except for "Review the PR" - also, are you '
            "able to set my default repo for me conversationally?"
        )
        entry = {
            "list": "SET_DEFAULT_REPO_PATTERNS",
            "rows_claimed_at_deletion": [phrase],
        }
        ok, problems = gate.check_deleted_entry_non_regression(entry)
        assert not ok
        assert any("claimed again by SET_DEFAULT_REPO_PATTERNS" in p for p in problems)

    def test_fails_for_a_phrase_that_is_no_longer_a_corpus_row(self):
        entry = {
            "list": "SYNTHETIC_NEVER_CLAIMED_LIST",
            "rows_claimed_at_deletion": ["this phrase does not exist in the corpus, at all, ever"],
        }
        ok, problems = gate.check_deleted_entry_non_regression(entry)
        assert not ok
        assert any("no longer a corpus row" in p for p in problems)

    def test_fails_for_a_phrase_whose_router_verdict_is_not_match_or_agreeing_review(self):
        # "analyze the file I uploaded" is a real corpus row (QUERY,
        # action:analyze_data), unclaimed by any surface-1 list today, whose
        # router verdict in the 09-25 full report is MISMATCH
        # (analyze_document vs expected analyze_data). A synthetic entry
        # citing it as safely-deleted evidence must fail non-regression.
        assert (
            gate.claim_for_phrase(PreClassifier, "analyze the file I uploaded").pattern_list is None
        ), "test fixture assumption broke — pick another unclaimed MISMATCH row"
        entry = {
            "list": "SYNTHETIC_NEVER_CLAIMED_LIST",
            "rows_claimed_at_deletion": ["analyze the file I uploaded"],
        }
        ok, problems = gate.check_deleted_entry_non_regression(entry)
        assert not ok
        assert any("no longer MATCH or an agreeing REVIEW" in p for p in problems)

    def test_passes_for_an_unclaimed_floor_expected_phrase_that_matches(self):
        # #1595 Phase 3 third deletion (CALENDAR_QUERY_PATTERNS): a `floor`
        # corpus expectation scores MATCH when the router declines
        # (outcome in none/clarify) — scripts/inversion_phase1_shadow_score
        # .py's router_matches encodes this at SCORE time, so by the time
        # this phrase reaches check_deleted_entry_non_regression it is
        # already a MATCH row like any other; the unclaimed path's unified
        # row_disposition reuse passes it with ZERO need for cats or
        # expected_op_by_phrase (MATCH never consults either). "time spent
        # in meetings is high lately" is a real corpus row (CALENDAR,
        # expected: floor) confirmed unclaimed by any surviving surface-1
        # list post-CALENDAR_QUERY_PATTERNS-deletion.
        assert (
            gate.claim_for_phrase(
                PreClassifier, "time spent in meetings is high lately"
            ).pattern_list
            is None
        ), "test fixture assumption broke — pick another unclaimed floor row"
        entry = {
            "list": "SYNTHETIC_FLOOR_LIST",
            "rows_claimed_at_deletion": ["time spent in meetings is high lately"],
        }
        ok, problems = gate.check_deleted_entry_non_regression(entry)  # no cats needed
        assert ok, problems

    def test_passes_for_a_floor_expected_phrase_reclaimed_but_documented_disagreeing(self):
        # The companion shape: a floor/plan row a SURVIVING list now claims
        # (disagreeing — any real action disagrees with "floor"/"plan" by
        # construction, p0.same_operation(action, "floor"/"plan") is always
        # False). Documented via known_reabsorptions with explicit
        # "agrees": false, it must still pass IF the row's own frozen
        # router verdict is independently MATCH — SET_DEFAULT_REPO_PATTERNS'
        # #1606 two-op plan-row shape (expected: "plan"; SET_DEFAULT_REPO_
        # PATTERNS claims it as set_default_repo; the row itself scores
        # MATCH via the deposits-asserted PLAN[...] route, so no cats are
        # even needed here). STATUS_PATTERNS/GUIDANCE_PATTERNS deliberately
        # NOT used — both are the next two lists scheduled for deletion;
        # checked empirically (2026-10-02) that no other surviving list
        # claims ANY floor-expected corpus row today, so this "plan"-typed
        # row is the only non-STATUS/GUIDANCE example of this shape.
        # (Was PRIORITY_PATTERNS' "list priorities for the team" shape
        # before #1595 Phase 3's sixth deletion emptied PRIORITY_PATTERNS
        # itself and left that phrase genuinely unclaimed, breaking this
        # fixture's own premise — the SAME fixture-breakage shape
        # CALENDAR_QUERY_PATTERNS'/TEMPORAL_PATTERNS' own deletions caused
        # here before it, each time swapped to a still-claimed example.)
        phrase = (
            'please clear the reminders except for "Review the PR" - also, are you '
            "able to set my default repo for me conversationally?"
        )
        claim = gate.claim_for_phrase(PreClassifier, phrase)
        assert claim.pattern_list is not None, "test fixture assumption broke"
        entry = {
            "list": "SYNTHETIC_FLOOR_RECLAIMED_LIST",
            "rows_claimed_at_deletion": [phrase],
            "expected_op_by_phrase": {phrase: "plan"},
            "known_reabsorptions": {
                phrase: {
                    "reclaimed_by": claim.pattern_list,
                    "claimed_action": claim.action,
                    "agrees": False,
                }
            },
        }
        ok, problems = gate.check_deleted_entry_non_regression(entry)
        assert ok, problems

    def test_fails_for_an_undocumented_reclaim_even_when_independently_safe(self):
        # The SAME plan row as above, WITHOUT a known_reabsorptions entry.
        # The reclaim is a SURPRISE the ledger author never named — must
        # fail loud regardless of whether the underlying router evidence
        # happens to be fine (that is the whole point of requiring
        # documentation: catching the unexpected reclaim itself, not just
        # its eventual safety).
        phrase = (
            'please clear the reminders except for "Review the PR" - also, are you '
            "able to set my default repo for me conversationally?"
        )
        entry = {
            "list": "SYNTHETIC_UNDOCUMENTED_RECLAIM_LIST",
            "rows_claimed_at_deletion": [phrase],
            "expected_op_by_phrase": {phrase: "plan"},
        }
        ok, problems = gate.check_deleted_entry_non_regression(entry)
        assert not ok
        assert any("reabsorbed by a surviving pattern" in p for p in problems)

    def test_passes_for_a_surface2_verified_phrase_still_unclaimed(self):
        # #1595 Phase 3 sixth deletion's new shape: a FLOOR-destination row
        # whose own deleted pattern's claim AGREED with the ruling, but the
        # router MISMATCHED to a non-live op (ordinarily NOT OK — the
        # pattern was the live path). Arch's 2026-10-02 condition (d)
        # licenses it when a frozen surface-2 probe shows the LLM classifier
        # landing the phrase in the destination's own category on every
        # sample. "what are my focus areas this sprint" is a real corpus
        # row, genuinely unclaimed post-PRIORITY_PATTERNS-deletion (measured
        # — no surviving list reclaims it), whose frozen router verdict is
        # MISMATCH (route=get_contextual_guidance@0.72, below dispatch
        # threshold) — i.e. it would FAIL non-regression without the
        # surface2_verified_at_deletion documentation (proven by the
        # companion test below).
        phrase = "what are my focus areas this sprint"
        assert (
            gate.claim_for_phrase(PreClassifier, phrase).pattern_list is None
        ), "test fixture assumption broke — pick another unclaimed, surface-2-verified row"
        entry = {
            "list": "SYNTHETIC_SURFACE2_VERIFIED_LIST",
            "rows_claimed_at_deletion": [phrase],
            "expected_op_by_phrase": {phrase: "get_top_priority"},
            "surface2_verified_at_deletion": {
                phrase: {
                    "probe_report": "inversion-phase3-surface2-floor-probe-2026-10-02-n5-anthropic.md",
                    "samples": "5/5",
                    "served": "anthropic:claude-sonnet-4-6",
                }
            },
        }
        ok, problems = gate.check_deleted_entry_non_regression(entry)
        assert ok, problems

    def test_fails_for_the_same_phrase_without_the_surface2_documentation(self):
        # The SAME row as above, WITHOUT surface2_verified_at_deletion. The
        # MISMATCH-to-a-non-live-op verdict alone is not sufficient — the
        # probe proof must be named, not inferred.
        # 2026-10-02 (Lead): the re-proof now threads the phrase, so a frozen
        # probe on disk re-fires condition (d) at re-verification time — the
        # ledger key is documentation, the probe is the proof. To show the
        # documentation is not what passes the row, remove the probes: an
        # undocumented row then fails, a documented one still passes.
        phrase = "what are my focus areas this sprint"
        entry = {
            "list": "SYNTHETIC_SURFACE2_UNDOCUMENTED_LIST",
            "rows_claimed_at_deletion": [phrase],
            "expected_op_by_phrase": {phrase: "get_top_priority"},
        }
        import pytest as _pytest

        mp = _pytest.MonkeyPatch()
        try:
            mp.setattr(gate, "SURFACE2_FLOOR_PROBES", [])
            ok, problems = gate.check_deleted_entry_non_regression(entry)
            assert not ok
            assert any("no longer MATCH or an agreeing REVIEW" in p for p in problems)
            documented = dict(
                entry,
                surface2_verified_at_deletion={
                    phrase: {"probe_report": "x", "samples": "5/5", "served": "stub:model"}
                },
            )
            ok, problems = gate.check_deleted_entry_non_regression(documented)
            assert ok, problems
        finally:
            mp.undo()

    def test_documented_disagreeing_reclaim_needs_the_live_flag_when_the_row_is_mismatch(self):
        # A MISMATCH-but-live-route row (not a plain MATCH like the floor
        # cases above) genuinely needs cats to pass even when documented.
        # This fixture needs a phrase whose REAL corpus `expected` field is
        # NOT `action:`-shaped (REVIEW/floor/plan) — only then does
        # expected_op_for_phrase fall through to this entry's OWN synthetic
        # expected_op_by_phrase (rule 1 in that function's docstring always
        # prefers the real corpus row's own asserted `action:` expectation,
        # which would silently override anything synthesized here). Uses
        # IDENTITY_PATTERNS' "who are you?" (REVIEW-expected, claimed as
        # get_identity) purely as a stable, unrelated-to-#1595 REVIEW-shaped
        # carrier for the synthetic SYNTHETIC_MISMATCH_RECLAIM_LIST scenario
        # — the router verdict below is a full stub, so neither IDENTITY_
        # PATTERNS' real claim nor "who are you?"'s real router history
        # matters beyond "claimed, REVIEW-expected". (Previously CALENDAR_
        # QUERY_PATTERNS' "what is on my calendar" shape reclaimed by
        # TEMPORAL_PATTERNS, broken when #1595 Phase 3's fourth deletion
        # emptied TEMPORAL_PATTERNS and left that phrase unclaimed; then
        # STATUS_PATTERNS' "give me a project status report" shape, broken
        # when the seventh deletion (2026-10-02, PARTIAL) deleted its
        # claiming literal \bstatus report\b; a same-day STATUS_PATTERNS
        # replacement, "can you summarize my current work", broke
        # IMMEDIATELY on first use — that phrase's real corpus `expected` is
        # itself `action:get_project_status`, so rule 1 made target_op equal
        # the real claim's own action and the reclaim always "agreed",
        # never exercising the disagreeing-but-live-proved-safe branch this
        # test exists to pin. Picking a REVIEW-expected carrier phrase
        # sidesteps that trap structurally, not by coincidence.)
        phrase = "who are you?"
        claim = gate.claim_for_phrase(PreClassifier, phrase)
        assert claim.pattern_list == "IDENTITY_PATTERNS", "test fixture assumption broke"
        entry = {
            "list": "SYNTHETIC_MISMATCH_RECLAIM_LIST",
            "rows_claimed_at_deletion": [phrase],
            "expected_op_by_phrase": {phrase: "update_issue"},
            "known_reabsorptions": {
                phrase: {
                    "reclaimed_by": "IDENTITY_PATTERNS",
                    "claimed_action": "get_identity",
                    "agrees": False,
                }
            },
        }
        # The router verdict is a full stub: MISMATCH, route
        # generate_report@0.92 (live only via the read_referent group). The
        # claim side stays real (IDENTITY_PATTERNS really does claim the
        # phrase as get_identity); only the router is synthesized, because
        # this test is about the MECHANISM, not any phrase's live verdict.

        class _StubReports:
            def lookup(self, phrase_, category_):
                return gate.RouterLookup(
                    route="generate_report", conf=0.92, verdict="MISMATCH", source_table="stub"
                )

        ok_without, problems_without = gate.check_deleted_entry_non_regression(
            entry, reports=_StubReports()
        )
        assert not ok_without, problems_without

        ok_with, problems_with = gate.check_deleted_entry_non_regression(
            entry, cats=frozenset({"READ_REFERENT"}), reports=_StubReports()
        )
        assert ok_with, problems_with


# ── (c) REPO_MANAGEMENT_PATTERNS against the frozen reports — print it,
#        don't pin GO/NO-GO as a fact of the world ─────────────────────────


class TestPriorityPatternsVerdictIsReported:
    """Exercises the SAME verdict-reporting mechanism the five deletion
    sessions each ran by hand before their own list's deletion — originally
    pinned against TEMPORAL_PATTERNS as a stable, many-rows example, then
    PRIORITY_PATTERNS after TEMPORAL_PATTERNS' own fourth deletion. #1595
    Phase 3's sixth deletion emptied PRIORITY_PATTERNS itself (it now claims
    ZERO corpus rows — "NO ROWS" in the `--all` census, not GO/NO-GO), which
    broke this class's own fixture premise a second time. Swapped to
    REPO_MANAGEMENT_PATTERNS (still live, 2 claimed rows as of 2026-10-02 —
    STATUS_PATTERNS/GUIDANCE_PATTERNS deliberately NOT used, both being the
    next two lists scheduled for deletion in this epic) rather than deleted
    — same idiom as every other pin swap in this deletion series. Class name
    kept (not renamed per-list) since it is cited by file path elsewhere;
    the docstring is the source of truth for which list it currently
    exercises."""

    def test_returns_a_verdict_with_named_rows(self, capsys):
        """Runs the real census (real corpus, real pre-classifier, the real
        frozen router reports — no LLM call anywhere) and asserts only that
        REPO_MANAGEMENT_PATTERNS gets a verdict backed by named rows.
        Whether that verdict is GO or NO-GO is data, printed for the test
        log, never asserted as a fixed fact — the router reports (and
        therefore the verdict) can change out from under this test on a
        future re-score, and pinning GO/NO-GO here would silently start
        lying the day that happens."""
        _records, by_list = gate.build_census(cats=None)
        lv = by_list.get("REPO_MANAGEMENT_PATTERNS")
        assert lv is not None, "REPO_MANAGEMENT_PATTERNS must appear in the census"
        assert len(lv.rows) > 0, "REPO_MANAGEMENT_PATTERNS must claim at least one corpus row"

        verdict = "GO" if lv.deletable else "NO-GO"
        print(f"\nREPO_MANAGEMENT_PATTERNS verdict (frozen reports): {verdict}")
        print(f"literals: {lv.literal_count}  rows claimed: {len(lv.rows)}")
        for rec in lv.rows:
            mark = "OK" if rec.row_ok else "FAIL"
            print(f"  [{mark}] {rec.phrase!r} -> {rec.reason}")

        # The only pinned facts: every claimed row is NAMED (phrase is
        # non-empty) and carries a reason string (never silently blank) —
        # the verdict itself is read, not asserted.
        for rec in lv.rows:
            assert rec.phrase, "every row backing the verdict must be named"
            assert rec.reason, f"{rec.phrase!r} has no reason recorded"
        assert verdict in ("GO", "NO-GO")

    def test_temporal_patterns_now_claims_zero_rows(self):
        """#1595 Phase 3 fourth deletion: TEMPORAL_PATTERNS is tombstoned —
        pins the post-deletion state directly rather than leaving it as an
        implicit consequence of the ledger entry alone."""
        _records, by_list = gate.build_census(cats=None)
        lv = by_list.get("TEMPORAL_PATTERNS")
        assert (
            lv is not None
        ), "TEMPORAL_PATTERNS must still appear in the census (0 rows, not absent)"
        assert len(lv.rows) == 0
        assert lv.deletable is False, "an empty list reports NO ROWS, not GO"

    def test_priority_patterns_now_claims_zero_rows(self):
        """#1595 Phase 3 sixth deletion: PRIORITY_PATTERNS is tombstoned —
        pins the post-deletion state directly rather than leaving it as an
        implicit consequence of the ledger entry alone (same idiom as
        test_temporal_patterns_now_claims_zero_rows above)."""
        _records, by_list = gate.build_census(cats=None)
        lv = by_list.get("PRIORITY_PATTERNS")
        assert (
            lv is not None
        ), "PRIORITY_PATTERNS must still appear in the census (0 rows, not absent)"
        assert len(lv.rows) == 0
        assert lv.deletable is False, "an empty list reports NO ROWS, not GO"

    def test_status_patterns_now_claims_four_rows(self):
        """#1595 Phase 3 seventh deletion, the FIRST PARTIAL one:
        STATUS_PATTERNS keeps exactly its 4 load-bearing survivor literals
        (\\bnext milestone\\b, \\bcurrent work\\b, \\bproject overview\\b,
        \\bproject landscape\\b) — unlike a full tombstone (0 rows), a
        partial deletion's list still claims rows: exactly the 4 the
        survivors own. All 4 are [FAIL] under THIS gate run's --live set
        (each is a MATCH on a non-live op the surface-2 probe doesn't cover
        on every sample) — that is WHY they survive, not a regression."""
        cats = gate.CURRENT_LIVE_CATEGORIES
        _records, by_list = gate.build_census(cats=cats)
        lv = by_list.get("STATUS_PATTERNS")
        assert lv is not None, "STATUS_PATTERNS must still appear in the census"
        assert len(lv.rows) == 4, [r.phrase for r in lv.rows]
        assert {r.phrase for r in lv.rows} == {
            "any update on the next milestone",
            "can you summarize my current work",
            "give me a project overview",
            "what's the project landscape",
        }
        assert all(
            not r.row_ok for r in lv.rows
        ), "all 4 rows are the FAIL rows that keep the literal"
        assert lv.deletable is False, "a list with any FAIL row is NO-GO, not GO"

    def test_guidance_patterns_now_claims_three_rows(self):
        """#1595 Phase 3 eighth deletion, the SECOND PARTIAL one:
        GUIDANCE_PATTERNS keeps exactly its 3 load-bearing survivor literals
        (\\bsetup.*projects?\\b, \\bset up.*projects?\\b,
        \\bset up.*portfolio\\b) — unlike a full tombstone (0 rows), a
        partial deletion's list still claims rows: exactly the 3 the
        survivors own. All 3 are [FAIL] under THIS gate run's --live set
        (each is a MATCH on a non-live op where a frozen N=5 surface-2 probe
        shows the LLM classifier landing EXECUTION 10/10, never GUIDANCE) —
        that is WHY they survived until read_canonical went live (see the
        2026-10-05 note below)."""
        cats = gate.CURRENT_LIVE_CATEGORIES
        _records, by_list = gate.build_census(cats=cats)
        lv = by_list.get("GUIDANCE_PATTERNS")
        assert lv is not None, "GUIDANCE_PATTERNS must still appear in the census"
        assert len(lv.rows) == 3, [r.phrase for r in lv.rows]
        assert {r.phrase for r in lv.rows} == {
            "I need to setup my projects",
            "I want to set up my projects",
            "I'd like to set up my portfolio",
        }
        # 2026-10-05: read_canonical flipped on alpha (Fly v169, 12 tokens), so
        # get_contextual_guidance is LIVE and all 3 rows are now [OK] (MATCH on
        # a live op). The list reads GO (deletable) — the survivors' reason to
        # exist ended with the flip. Deletion is a separate lane (re-score
        # first); this pin records the verdict under the mirrored live set.
        assert all(r.row_ok for r in lv.rows), "all 3 rows are live MATCHes now"
        assert lv.deletable is True, "GUIDANCE reads GO once get_contextual_guidance is live"

    def test_discovery_patterns_now_claims_one_row(self):
        """#1595 Phase 3 ninth deletion, the THIRD PARTIAL one:
        DISCOVERY_PATTERNS keeps exactly its 1 load-bearing survivor literal
        (\\bneed\\s*help\\b) — unlike a full tombstone (0 rows), a partial
        deletion's list still claims rows: exactly the 1 the survivor owns.
        That 1 row is [FAIL] under THIS gate run's --live set (a MISMATCH
        where the router declines with CLARIFY@0.6 and a frozen N=10
        surface-2 probe shows the LLM classifier landing get_capabilities
        0/10 samples) — that is WHY it survives, not a regression."""
        cats = gate.CURRENT_LIVE_CATEGORIES
        _records, by_list = gate.build_census(cats=cats)
        lv = by_list.get("DISCOVERY_PATTERNS")
        assert lv is not None, "DISCOVERY_PATTERNS must still appear in the census"
        assert len(lv.rows) == 1, [r.phrase for r in lv.rows]
        assert {r.phrase for r in lv.rows} == {
            "I need help understanding something",
        }
        assert all(
            not r.row_ok for r in lv.rows
        ), "the 1 row is the FAIL row that keeps the literal"
        assert lv.deletable is False, "a list with any FAIL row is NO-GO, not GO"

    def test_trust_patterns_now_claims_one_row(self):
        """#1595 Phase 3 tenth deletion, the FOURTH PARTIAL one:
        TRUST_PATTERNS keeps exactly its 1 load-bearing survivor literal
        (\\bwhy can'?t you\\b) — unlike a full tombstone (0 rows), a partial
        deletion's list still claims rows: exactly the 1 the survivor owns.
        That 1 row is [FAIL] under THIS gate run's --live set (a
        REVIEW-disagrees row: the router names get_capabilities@0.9, a live
        op, but the expected destination is REVIEW/not-action-shaped) —
        that is WHY it survives, not a regression."""
        cats = gate.CURRENT_LIVE_CATEGORIES
        _records, by_list = gate.build_census(cats=cats)
        lv = by_list.get("TRUST_PATTERNS")
        assert lv is not None, "TRUST_PATTERNS must still appear in the census"
        assert len(lv.rows) == 1, [r.phrase for r in lv.rows]
        assert {r.phrase for r in lv.rows} == {
            "why can't you create issues?",
        }
        assert all(
            not r.row_ok for r in lv.rows
        ), "the 1 row is the FAIL row that keeps the literal"
        assert lv.deletable is False, "a list with any FAIL row is NO-GO, not GO"

    def test_memory_patterns_now_claims_four_rows(self):
        """#1595 Phase 3 eleventh deletion, the FIFTH PARTIAL one:
        MEMORY_PATTERNS keeps exactly its 3 load-bearing survivor literals
        (\\b(my|our) (conversation )?history\\b, \\bsearch (my |our )?
        (conversation )?history\\b, \\bwhat (i|we) (said|talked|discussed)\\b)
        — unlike a full tombstone (0 rows), a partial deletion's list still
        claims rows: the 3 the survivors own, PLUS 1 reabsorbed row ("can
        you show my conversation history", formerly claimed by the deleted
        \\b(show|view|see) ... history\\b literal, now reclaimed by the
        surviving \\b(my|our) (conversation )?history\\b literal — an
        AGREEING reabsorption, see known_reabsorptions on the ledger entry).
        The 3 survivor rows are [FAIL] under THIS gate run's --live set
        (each has no live fallback naming the same op) — that is WHY they
        survive; the 1 reabsorbed row is [OK] (a plain live MATCH) — it was
        never load-bearing for the deletion, it just happens to still be
        claimed by a different (surviving) literal now."""
        cats = gate.CURRENT_LIVE_CATEGORIES
        _records, by_list = gate.build_census(cats=cats)
        lv = by_list.get("MEMORY_PATTERNS")
        assert lv is not None, "MEMORY_PATTERNS must still appear in the census"
        assert len(lv.rows) == 4, [r.phrase for r in lv.rows]
        assert {r.phrase for r in lv.rows} == {
            "our history together has been good",
            "search history for that conversation topic",
            "what we discussed yesterday was helpful",
            "can you show my conversation history",
        }
        failing = {r.phrase for r in lv.rows if not r.row_ok}
        assert failing == {
            "our history together has been good",
            "search history for that conversation topic",
            "what we discussed yesterday was helpful",
        }, "exactly the 3 survivor rows are FAIL; the reabsorbed row is OK"
        assert lv.deletable is False, "a list with any FAIL row is NO-GO, not GO"

    def test_analysis_patterns_now_claims_four_rows(self):
        """#1595 Phase 3 twelfth deletion, the SIXTH PARTIAL one:
        ANALYSIS_PATTERNS keeps exactly its 4 load-bearing survivor literals
        (\\bwhat.*obstacle\\b, \\bwhat'?s in the way\\b,
        \\banalyze.*(?:risk|impact|blocker|bottleneck)\\b,
        \\bimpact analysis\\b) — unlike a full tombstone (0 rows), a partial
        deletion's list still claims rows: exactly the 4 the survivors own.
        Unlike MEMORY_PATTERNS' eleventh deletion, there is NO reabsorbed row
        here — post-deletion, all 12 deleted-literal phrases were verified
        genuinely UNCLAIMED (known_reabsorptions is empty on this ledger
        entry), so the census count stays exactly 4. All 4 rows are [FAIL]
        under THIS gate run's --live set (each is a MISMATCH where the
        router declines with CLARIFY@0.4 and the pattern is the only live
        path) — that is WHY they survive, not a regression."""
        cats = gate.CURRENT_LIVE_CATEGORIES
        _records, by_list = gate.build_census(cats=cats)
        lv = by_list.get("ANALYSIS_PATTERNS")
        assert lv is not None, "ANALYSIS_PATTERNS must still appear in the census"
        assert len(lv.rows) == 4, [r.phrase for r in lv.rows]
        assert {r.phrase for r in lv.rows} == {
            "what's the main obstacle here",
            "what's in the way of finishing this",
            "let's analyze the risk here",
            "can you run an impact analysis on this change",
        }
        assert all(
            not r.row_ok for r in lv.rows
        ), "all 4 rows are the FAIL rows that keep the literal"
        assert lv.deletable is False, "a list with any FAIL row is NO-GO, not GO"


# ── router-report parsers (route column, REVIEW table) ─────────────────────


class TestReportParsers:
    def test_parse_asserted_rows_retains_route(self):
        rows = gate.parse_asserted_rows(gate.FULL_REPORT)
        assert rows, "must parse at least one asserted row"
        sample = next(r for r in rows if r["phrase"] == "who am I?")
        assert sample["route"] == "get_identity"
        assert sample["conf"] == 1.0
        assert sample["verdict"] == "MATCH"

    def test_parse_review_rows(self):
        rows = gate.parse_review_rows(gate.FULL_REPORT)
        assert rows, "must parse at least one REVIEW row"
        sample = next(r for r in rows if r["phrase"] == "what reminders do I have?")
        assert sample["route"] == "list_reminders_query"
        assert sample["conf"] == 1.0

    def test_temporal_rescore_overrides_full_report_for_temporal_category(self):
        """The documented precedence: 'what's on my calendar today?' is
        MISMATCH in the full 09-25 report (week_calendar vs expected
        meeting_time) but MATCH in the same-day temporal re-score (after the
        registry-description sharpening). The gate's lookup must return the
        re-score's MATCH for this TEMPORAL-category row."""
        reports = gate.RouterReports(gate.FULL_REPORT, gate.TEMPORAL_RESCORE_REPORT)
        full_hit = reports._find(
            gate.p1._norm_phrase("what's on my calendar today?"), reports._full_asserted_by_norm
        )
        assert full_hit is not None and full_hit["verdict"] == "MISMATCH"

        lookup = reports.lookup("what's on my calendar today?", "TEMPORAL")
        assert lookup.verdict == "MATCH", "temporal re-score must override the full run"
        assert lookup.source_table == "temporal-rescore-asserted"

    def test_non_temporal_category_never_consults_temporal_rescore(self):
        reports = gate.RouterReports(gate.FULL_REPORT, gate.TEMPORAL_RESCORE_REPORT)
        lookup = reports.lookup("who am I?", "IDENTITY")
        assert lookup.source_table == "full-asserted"


# ── live-set resolution (condition (c)) ─────────────────────────────────────


class TestLiveSetResolution:
    def test_unknown_when_unset_and_no_override(self, monkeypatch):
        monkeypatch.delenv("PIPER_INVERSION_LIVE_CATEGORIES", raising=False)
        cats, source = gate.live_set(explicit=None)
        assert cats is None
        assert source == "unknown"

    def test_explicit_override_wins(self, monkeypatch):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status")
        cats, source = gate.live_set(explicit="create_todo,create_reminder")
        assert cats == {"CREATE_TODO", "CREATE_REMINDER"}
        assert source == "--live"

    def test_condition_c_false_when_live_set_unknown(self):
        ok, reason = gate.expected_action_is_live("action:create_todo", cats=None)
        assert ok is False
        assert reason == "live-set-unknown"

    def test_condition_c_false_for_non_action_expected(self):
        ok, reason = gate.expected_action_is_live("category:STATUS", cats=frozenset({"QUERY"}))
        assert ok is False
        assert reason == "expected-not-action-shaped"

    def test_condition_c_true_when_action_is_live_by_operation_name(self):
        ok, reason = gate.expected_action_is_live(
            "action:create_todo", cats=frozenset({"CREATE_TODO"})
        )
        assert ok is True
        assert "live via" in reason


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))


class TestLiveMeansDispatchable:
    """Arch's 2026-10-01 ruling: the gate's "live" must mean what production
    means — a rail key (WorkflowEntry) that passes the #1677 effect guard AND
    matches the flag. A name that only matches the flag (op / group /
    category) but has no WorkflowEntry can never be served by the live
    consult, so the gate must read NOT-live for it even when the operator
    passes its own name as a token. Latent false GO before this pin."""

    def test_floor_routed_canonical_is_not_live_even_when_named_in_the_flag(self):
        # #1595 Phase 3 (2026-10-01): get_current_time now HAS a rail entry
        # (Arch's ruling, workflow_entries.py get_current_time_entry,
        # flip_group read_temporal) — swapped to explain_suggestion
        # (PROVENANCE, CANONICAL disposition, no WorkflowEntry) per this
        # test's own original instruction: the property pinned is "a
        # floor-routed canonical with no rail entry is not live", not this
        # specific example. explain_suggestion verified still rail-free
        # 2026-10-01 (same session that added get_current_time's entry).
        #
        # #1595 Phase 3 (2026-10-04, Arch's ruling section 3 "Two 'CANONICAL
        # writes' are reads"): explain_suggestion ITSELF gained a
        # read_canonical rail entry in this build, so swapped again to
        # manage_portfolio (PORTFOLIO, CANONICAL disposition, no
        # WorkflowEntry — confirmed rail-free this session;
        # `"manage_portfolio" in get_action_workflows()` is False). Same
        # property, same stand-in-swap shape as the first swap above.
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()
        assert get_action_workflows().get("manage_portfolio") is None, (
            "manage_portfolio now has a rail entry — pick another floor-routed canonical "
            "for this pin rather than deleting it"
        )
        ok, reason = gate.expected_action_is_live(
            "action:manage_portfolio",
            frozenset({"MANAGE_PORTFOLIO", "PORTFOLIO", "READ_TEMPORAL"}),
        )
        assert ok is False
        assert "no WorkflowEntry" in reason

    def test_rail_key_in_a_live_group_is_live(self):
        ok, reason = gate.expected_action_is_live(
            "action:meeting_time", frozenset({"READ_TEMPORAL"})
        )
        assert ok is True, reason
        assert reason.startswith("live via")


class TestMismatchRowRuleMeasuresTheRouterNotTheDestination:
    """2026-10-01: a MISMATCH row is safe to delete only when the ROUTER's own
    answer is a live operation (the consult already owns the phrase). When the
    router declined (NONE/CLARIFY/REFUSED) the consult stands down and the
    pattern IS the live path, so deletion changes behaviour. The old rule
    checked whether the EXPECTED action was live — the wrong object. Pinned
    on synthetic rows through the factored row_disposition(), so the pin does
    not depend on the census happening to contain a broken row."""

    LIVE = frozenset({"READ_TEMPORAL", "READ_STATUS"})
    CLAIM = gate.ClaimResult(
        pattern_list="CALENDAR_QUERY_PATTERNS",
        action="week_calendar",
        category="QUERY",
        entry_surface="pre_classify",
    )

    def _router(self, route, verdict):
        return gate.RouterLookup(route=route, conf=0.85, verdict=verdict, source_table="synthetic")

    def test_router_declined_mismatch_is_not_ok_even_when_the_expected_action_is_live(self):
        for route in ("NONE", "CLARIFY", "REFUSED"):
            ok, reason = gate.row_disposition(
                self.CLAIM, self._router(route, "MISMATCH"), "action:week_calendar", self.LIVE
            )
            assert ok is False, (route, reason)
            assert "the pattern is the live path" in reason

    def test_router_answered_with_a_live_op_mismatch_is_ok(self):
        ok, reason = gate.row_disposition(
            self.CLAIM, self._router("meeting_time", "MISMATCH"), "action:week_calendar", self.LIVE
        )
        assert ok is True, reason
        assert "the consult owns this phrase" in reason

    def test_router_answered_with_a_live_op_below_dispatch_threshold_is_not_ok(self):
        # 2026-10-01: STATUS score — "show today's assignments" → meeting_time
        # @0.6. meeting_time is live, but production dispatches only at
        # >= live_min_confidence() (0.8); below it the consult stands down and
        # the pattern is still the live path.
        low = gate.RouterLookup(
            route="meeting_time", conf=0.6, verdict="MISMATCH", source_table="synthetic"
        )
        ok, reason = gate.row_disposition(self.CLAIM, low, "action:week_calendar", self.LIVE)
        assert ok is False, reason
        assert "dispatch threshold" in reason
        # And with no confidence recorded at all, the same stand-down applies.
        none_conf = gate.RouterLookup(
            route="meeting_time", conf=None, verdict="MISMATCH", source_table="synthetic"
        )
        ok, reason = gate.row_disposition(self.CLAIM, none_conf, "action:week_calendar", self.LIVE)
        assert ok is False, reason

    def test_router_answered_with_a_not_live_op_mismatch_is_not_ok(self):
        # get_top_priority has no live group in this flag set.
        ok, reason = gate.row_disposition(
            self.CLAIM,
            self._router("get_top_priority", "MISMATCH"),
            "action:week_calendar",
            self.LIVE,
        )
        assert ok is False, reason

    def test_unscored_rows_are_never_ok(self):
        ok, reason = gate.row_disposition(
            self.CLAIM, self._router(None, "UNSCORED"), "action:week_calendar", self.LIVE
        )
        assert ok is False
        assert "UNSCORED" in reason

    def test_match_is_ok(self):
        ok, _ = gate.row_disposition(
            self.CLAIM, self._router("week_calendar", "MATCH"), "action:week_calendar", self.LIVE
        )
        assert ok is True

    def test_router_declined_but_pattern_misserves_the_row_with_no_probe_is_not_credited(self):
        # #1933: the mis-serve credit's premise -- "deleting cannot make the
        # fallback worse" -- requires surface-2 EVIDENCE that the fallback
        # isn't itself worse (a WRITE/DESTRUCTIVE mis-route). No phrase
        # threaded (the pre-#1933 call shape) means no probe lookup is even
        # possible: NOT credited, named honestly rather than assumed safe.
        claim = gate.ClaimResult(
            pattern_list="TEMPORAL_PATTERNS",
            action="get_current_time",
            category="TEMPORAL",
            entry_surface="pre_classify",
        )
        ok, reason = gate.row_disposition(
            claim, self._router("CLARIFY", "MISMATCH"), "action:week_calendar", self.LIVE
        )
        assert ok is False, reason
        assert "mis-serves this row" in reason
        assert "no phrase threaded" in reason

    def test_router_declined_but_pattern_misserves_the_row_is_credited_when_surface2_is_safe(
        self, tmp_path, monkeypatch
    ):
        # Same mis-serve shape, now WITH a frozen surface-2 probe threaded,
        # and every sample lands on a non-rail (unregistered) action -- the
        # fallback genuinely cannot be made worse. Credited.
        claim = gate.ClaimResult(
            pattern_list="TEMPORAL_PATTERNS",
            action="get_current_time",
            category="TEMPORAL",
            entry_surface="pre_classify",
        )
        phrase = "pull up my calendar"
        rows = [
            {
                "phrase": phrase,
                "sample": n,
                "category": "TEMPORAL",
                "action": "week_calendar",
                "confidence": 0.7,
            }
            for n in (1, 2, 3)
        ]
        monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [_write_probe_file(tmp_path, rows)])
        ok, reason = gate.row_disposition(
            claim,
            self._router("CLARIFY", "MISMATCH"),
            "action:week_calendar",
            self.LIVE,
            phrase=phrase,
        )
        assert ok is True, reason
        assert "mis-serves this row" in reason
        assert "no WRITE/DESTRUCTIVE op" in reason

    def test_router_declined_but_pattern_misserves_the_row_is_not_credited_when_surface2_lands_a_write_op(
        self, tmp_path, monkeypatch
    ):
        # #1933's defining counter-example shape: surface 2 lands a
        # REGISTERED WRITE rail op (update_document_query) on every sample.
        # The fallback would be WORSE than the pattern's own wrong answer --
        # NOT credited, and the reason names the WRITE op.
        claim = gate.ClaimResult(
            pattern_list="TEMPORAL_PATTERNS",
            action="get_current_time",
            category="TEMPORAL",
            entry_surface="pre_classify",
        )
        phrase = "pull up my calendar"
        rows = [
            {
                "phrase": phrase,
                "sample": n,
                "category": "EXECUTION",
                "action": "update_document_query",
                "confidence": 0.9,
            }
            for n in (1, 2, 3)
        ]
        monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [_write_probe_file(tmp_path, rows)])
        ok, reason = gate.row_disposition(
            claim,
            self._router("CLARIFY", "MISMATCH"),
            "action:week_calendar",
            self.LIVE,
            phrase=phrase,
        )
        assert ok is False, reason
        assert "WRITE/DESTRUCTIVE" in reason
        assert "update_document_query" in reason

    def test_router_declined_and_pattern_serves_the_row_right_is_still_not_ok(self):
        # Same decline, but the claim AGREES with the ruling: the pattern is
        # the live path and correct — keep it.
        ok, reason = gate.row_disposition(
            self.CLAIM, self._router("CLARIFY", "MISMATCH"), "action:week_calendar", self.LIVE
        )
        assert ok is False, reason


# ── #1933 — the MATCH-arm's mis-serve credit needs the SAME surface-2 gate
#        the MISMATCH-arm pins above exercise ──────────────────────────────


class TestMatchArmMisserveCreditRequiresSurface2Safety:
    """row_disposition's MATCH-verdict branch has its OWN "MATCH on a
    non-live op, and the pattern mis-serves this row" credit (distinct code
    path from the MISMATCH-arm one TestMismatchRowRuleMeasuresTheRouterNot
    TheDestination pins) — #1933 requires the same surface-2 gate on it.
    Synthetic rows; mirrors that class's shape for this branch."""

    LIVE = frozenset({"READ_TEMPORAL", "READ_STATUS"})

    def _router(self, route, verdict, conf=0.95):
        return gate.RouterLookup(route=route, conf=conf, verdict=verdict, source_table="synthetic")

    def test_match_on_non_live_op_mis_serve_with_no_probe_is_not_credited(self):
        # STATUS_PATTERNS-shaped claim (the real pre-deletion shape, per the
        # ledger's own misserved_at_deletion note): claims get_project_status
        # for a row ruled manage_portfolio; the router independently MATCHes
        # manage_portfolio (a non-live, unregistered op). No phrase threaded
        # -> no probe lookup possible -> NOT credited.
        claim = gate.ClaimResult(
            pattern_list="STATUS_PATTERNS",
            action="get_project_status",
            category="STATUS",
            entry_surface="pre_classify",
        )
        ok, reason = gate.row_disposition(
            claim, self._router("manage_portfolio", "MATCH"), "action:manage_portfolio", self.LIVE
        )
        assert ok is False, reason
        assert "mis-serves this row" in reason
        assert "no phrase threaded" in reason

    def test_match_on_non_live_op_mis_serve_is_credited_when_surface2_is_safe(
        self, tmp_path, monkeypatch
    ):
        claim = gate.ClaimResult(
            pattern_list="STATUS_PATTERNS",
            action="get_project_status",
            category="STATUS",
            entry_surface="pre_classify",
        )
        phrase = "what are my projects?"
        rows = [
            {
                "phrase": phrase,
                "sample": n,
                "category": "QUERY",
                "action": "manage_portfolio",
                "confidence": 0.85,
            }
            for n in (1, 2, 3)
        ]
        monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [_write_probe_file(tmp_path, rows)])
        ok, reason = gate.row_disposition(
            claim,
            self._router("manage_portfolio", "MATCH"),
            "action:manage_portfolio",
            self.LIVE,
            phrase=phrase,
        )
        assert ok is True, reason
        assert "mis-serves this row" in reason
        assert "no WRITE/DESTRUCTIVE op" in reason

    def test_match_on_non_live_op_mis_serve_is_not_credited_when_surface2_lands_a_write_op(
        self, tmp_path, monkeypatch
    ):
        # #1933's actual PORTFOLIO shape (STATUS_PATTERNS carrier): surface 2
        # lands a REGISTERED WRITE rail op (update_document_query) on every
        # sample -- the fallback would be WORSE. NOT credited.
        claim = gate.ClaimResult(
            pattern_list="STATUS_PATTERNS",
            action="get_project_status",
            category="STATUS",
            entry_surface="pre_classify",
        )
        phrase = "what are my projects?"
        rows = [
            {
                "phrase": phrase,
                "sample": n,
                "category": "EXECUTION",
                "action": "update_document_query",
                "confidence": 0.9,
            }
            for n in (1, 2, 3)
        ]
        monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [_write_probe_file(tmp_path, rows)])
        ok, reason = gate.row_disposition(
            claim,
            self._router("manage_portfolio", "MATCH"),
            "action:manage_portfolio",
            self.LIVE,
            phrase=phrase,
        )
        assert ok is False, reason
        assert "WRITE/DESTRUCTIVE" in reason
        assert "update_document_query" in reason


# ── #1933 — PORTFOLIO's real dead-claim rows (today's deposit, set8): the
#        counter-example the issue was filed against, pinned against the
#        REAL corpus + REAL frozen probe files on disk (no LLM calls) ──────


class TestPortfolioDeadClaimRowsAreNotMisserveCredited:
    """The two PORTFOLIO_PATTERNS update/edit-project dead-claim rows
    (Arch-ruled: delete; today's conversion deposit,
    docs/internal/architecture/current/inversion-phase3-portfolio-
    deadclaims-score-2026-10-04.md) are the issue's defining counter-example:
    pattern claim manage_portfolio, ruled destination floor, router
    (Haiku) MISMATCH to update_document, and the frozen N=5x2-leg surface-2
    probe (SURFACE2_FLOOR_PROBES' set8 entries) lands update_document_query
    -- a registered WRITE rail op -- 10/10. Before #1933 the gate's
    mis-serve rule credited both rows regardless; after, neither is
    credited, and the reason names the WRITE op."""

    def test_update_project_name_row_is_not_misserve_credited(self):
        records, by_list = gate.build_census(cats=gate.CURRENT_LIVE_CATEGORIES)
        rec = next(
            (r for r in records if r.phrase == "update my project name to Atlas"),
            None,
        )
        assert rec is not None, "corpus row must exist (2026-10-04 PORTFOLIO deposit)"
        assert rec.claim.pattern_list == "PORTFOLIO_PATTERNS", rec.claim
        assert rec.row_ok is False, rec.reason
        assert "update_document_query" in rec.reason
        assert "WRITE/DESTRUCTIVE" in rec.reason

    def test_edit_project_description_row_is_not_misserve_credited(self):
        records, by_list = gate.build_census(cats=gate.CURRENT_LIVE_CATEGORIES)
        rec = next(
            (r for r in records if r.phrase == "edit my project description"),
            None,
        )
        assert rec is not None, "corpus row must exist (2026-10-04 PORTFOLIO deposit)"
        assert rec.claim.pattern_list == "PORTFOLIO_PATTERNS", rec.claim
        assert rec.row_ok is False, rec.reason
        assert "update_document_query" in rec.reason
        assert "WRITE/DESTRUCTIVE" in rec.reason

    def test_portfolio_patterns_is_no_go_because_of_these_two_rows(self):
        _records, by_list = gate.build_census(cats=gate.CURRENT_LIVE_CATEGORIES)
        lv = by_list.get("PORTFOLIO_PATTERNS")
        assert lv is not None, "PORTFOLIO_PATTERNS must appear in the census"
        failing = {r.phrase for r in lv.rows if not r.row_ok}
        assert {"update my project name to Atlas", "edit my project description"} <= failing
        assert lv.deletable is False, "a list with any FAIL row is NO-GO, not GO"


# ── #1933 — the misserved_at_deletion ESCAPE in check_deleted_entry_non_
#        regression is RE-VERIFIED, not unconditional ──────────────────────


class TestMisservedAtDeletionEscapeIsReVerified:
    """Before #1933, a ledgered ``misserved_at_deletion`` entry passed
    check_deleted_entry_non_regression unconditionally forever ("documented,
    so trust it"). After, it is re-verified against the SAME surface-2
    safety gate row_disposition's mis-serve branches now apply -- a FAIL is
    reported as a real finding (named phrase + reason), never silently
    passed and never papered over by editing the ledger."""

    def test_misserved_entry_with_no_probe_now_fails_and_names_the_phrase(self, monkeypatch):
        phrase = "pull up my calendar"  # real corpus row, genuinely unclaimed
        # Hermetic: "no probe" by construction. The real probe set gained a probe
        # for this phrase on 2026-10-04 (set9, the 1933 re-verification), so
        # relying on the on-disk reports would test nothing.
        monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [])
        assert (
            gate.claim_for_phrase(PreClassifier, phrase).pattern_list is None
        ), "test fixture assumption broke — pick another unclaimed phrase"
        entry = {
            "list": "SYNTHETIC_MISSERVED_NO_PROBE_LIST",
            "rows_claimed_at_deletion": [phrase],
            "misserved_at_deletion": {
                phrase: {
                    "claimed_action": "get_current_time",
                    "ruled_destination": "week_calendar",
                    "router_route": "CLARIFY@0.6",
                }
            },
        }
        ok, problems = gate.check_deleted_entry_non_regression(entry)
        assert not ok
        assert any(
            phrase in p and "re-verification against surface 2 now FAILS" in p for p in problems
        )
        assert any("no surface-2 probe" in p for p in problems)

    def test_misserved_entry_passes_when_surface2_confirms_safety(self, tmp_path, monkeypatch):
        phrase = "pull up my calendar"
        rows = [
            {
                "phrase": phrase,
                "sample": n,
                "category": "TEMPORAL",
                "action": "week_calendar",
                "confidence": 0.7,
            }
            for n in (1, 2, 3)
        ]
        monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [_write_probe_file(tmp_path, rows)])
        entry = {
            "list": "SYNTHETIC_MISSERVED_SAFE_PROBE_LIST",
            "rows_claimed_at_deletion": [phrase],
            "misserved_at_deletion": {
                phrase: {
                    "claimed_action": "get_current_time",
                    "ruled_destination": "week_calendar",
                    "router_route": "CLARIFY@0.6",
                }
            },
        }
        ok, problems = gate.check_deleted_entry_non_regression(entry)
        assert ok, problems

    def test_misserved_entry_fails_when_surface2_lands_a_write_op(self, tmp_path, monkeypatch):
        # The actual #1933 shape, exercised through the ledger escape
        # itself (not just row_disposition directly): a documented
        # misserved_at_deletion row whose surface-2 evidence shows a
        # REGISTERED WRITE rail op -- re-verification must FAIL, naming the
        # WRITE op, never silently pass because the ledger says so.
        phrase = "pull up my calendar"
        rows = [
            {
                "phrase": phrase,
                "sample": n,
                "category": "EXECUTION",
                "action": "update_document_query",
                "confidence": 0.9,
            }
            for n in (1, 2, 3)
        ]
        monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [_write_probe_file(tmp_path, rows)])
        entry = {
            "list": "SYNTHETIC_MISSERVED_WRITE_PROBE_LIST",
            "rows_claimed_at_deletion": [phrase],
            "misserved_at_deletion": {
                phrase: {
                    "claimed_action": "get_current_time",
                    "ruled_destination": "week_calendar",
                    "router_route": "CLARIFY@0.6",
                }
            },
        }
        ok, problems = gate.check_deleted_entry_non_regression(entry)
        assert not ok
        assert any("update_document_query" in p and "WRITE/DESTRUCTIVE" in p for p in problems)
