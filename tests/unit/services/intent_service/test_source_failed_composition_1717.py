"""1717/1772 — source-failed honest-degrade directives compose via ONE
registry site, and (since #1772) via ONE composition shape for every N >= 1.

History (the seam this file was built to be): through 2026-09-12 the renderer
had five independent source-failed directive sites that composed ADDITIVELY —
a turn with N failed sources got N separate "check FAILED" directives, each
with its own honesty guard (CXO's voice-watch finding, 2026-09-01). The
previous revision of this file pinned that pile deliberately, with the
all-five and two-of-five tests docstring-marked as "the ones that MUST start
failing when an aggregated-directive fix lands." **That seam fired
2026-09-12**: the #1717 composition fix (epic 5 / GatherOutcome opener)
replaced the five hand sites with a single composition site derived from
``SOURCE_FAILED_FLAGS`` — but kept a special case: N == 1 rendered a
registered per-source directive verbatim, N >= 2 rendered the aggregate.

**#1772 (2026-09-25) removed that special case.** Two nights of measurement
(``dev/2026/09/15/1772-scope-leak-measurement.md``,
``dev/2026/09/24/1772-candidate-measurement-2026-09-24.md``) found the
verbatim N == 1 copy leaking an unarmed source at 5/10 then 2/10 on
anthropic, while the aggregate shape scored 0/25 across both providers.
Arch ruled the mechanism (fold N == 1 into the same aggregate branch,
removing the ``len(_failed_sources) == 1`` special case); CXO ruled the copy
(the aggregate wording itself had to become N-agnostic — the pre-#1772
aggregate template presupposed a plural set in four phrases, which read as
meaningless rather than merely awkward at N == 1). This file now pins the
UNIFIED shape: every N >= 1 renders exactly one aggregate directive, using
CXO's N-agnostic wording, naming exactly the armed checks.

The composed contract (CXO's GatherOutcome user-facing contract §4,
docs/internal/design/gather-outcome-user-facing-contract-2026-09-09.md,
updated 2026-09-25 by #1772):

- **ANY N >= 1**: ONE aggregate directive naming exactly the failed checks
  (in registry order), instructing one sentence covering what wasn't
  checked — never one caveat per item — with one unified honesty guard
  (never claim it's empty or fine, never invent details). There is no more
  per-source verbatim directive; ``SourceFailedDirective`` carries no
  ``directive`` field.
- The wrinkle-1 SCOPE directive (CXO verbatim, binding copy) rides exactly
  once whenever >= 1 flag is armed, never at zero. Byte-identical to the
  pre-#1772 text — #1772 changed the aggregate line only.
- Wrinkle 2 (anti-reassurance) is unchanged in the floor addendum's
  never-fabricate block.

Layer honesty (m-43): this pins the deterministic CONTEXT-RENDERER and the
composed PROMPT — not what a live model does with the directive (that
evidence lives in the #1772 measurement docs; contract §6 is explicit that
its acceptance cases need delivered turns to score).

Registry round (2026-09-09) still holds: everything here DERIVES from
``SOURCE_FAILED_FLAGS`` — the renderer's own registry — so a sixth flag
registered there is automatically in every denominator (no bare 5s). The
registry<->renderer association is AST-enforced by
test_source_failed_registry_1717.py.
"""

from unittest.mock import MagicMock

import pytest

from services.intent_service.conversational_floor import (
    FLOOR_SYSTEM_PROMPT_ADDENDUM,
    SOURCE_FAILED_FLAGS,
    ConversationalFloor,
    FloorContext,
)

# flag key -> short check name (appears in the aggregate clause at any N >= 1).
NAMES = {entry.flag: entry.check_name for entry in SOURCE_FAILED_FLAGS}

ALL_FLAGS = {entry.flag: True for entry in SOURCE_FAILED_FLAGS}

# Stable prefix of the aggregate directive — the ONE failure-report line any
# N >= 1 turn gets. Pinned as a literal (8/21 lesson: pin NEW copy).
AGGREGATE_PREFIX = "- DATA CHECKS FAILED this turn — could not check: "

# #1772 CXO's N-agnostic aggregate wording, verbatim, the FULL sentence that
# follows the failed-checks list — pinned once as a literal per the 8/21
# lesson (pin NEW copy, not just key phrases).
AGGREGATE_TAIL = (
    ". If this becomes relevant, name what wasn't checked in ONE sentence — "
    "never one caveat per item. Don't claim it's empty or fine, and never "
    "invent details to fill the gap."
)

# #1717 wrinkle 1 — CXO's scope directive, verbatim (the rendered line, whole).
# Binding copy: a paraphrase is a regression even if it "means the same thing".
# Unchanged by #1772 — only the aggregate line's own wording changed.
SCOPE_DIRECTIVE = (
    "- Name ONLY the checks explicitly listed as FAILED above. Do not mention "
    "any other data source. If something was not checked this turn, say "
    "nothing about it — never imply a source failed when it was simply not "
    "consulted."
)


def _floor() -> ConversationalFloor:
    return ConversationalFloor(llm_client=MagicMock())


def _aggregate_lines(text: str) -> list:
    return [ln for ln in text.splitlines() if ln.strip().startswith(AGGREGATE_PREFIX.strip())]


class TestAggregateComposition:
    """N >= 2: one aggregate directive, no per-source pile, no bleed."""

    def test_all_five_flags_render_one_aggregate_not_five(self):
        out = _floor()._format_domain_context(dict(ALL_FLAGS))
        aggs = _aggregate_lines(out)
        assert len(aggs) == 1, f"expected exactly one aggregate line, got {len(aggs)}:\n{out}"
        assert out.count("check FAILED:") == 0
        assert out.count(SCOPE_DIRECTIVE) == 1

    def test_aggregate_names_all_failed_checks_in_registry_order(self):
        out = _floor()._format_domain_context(dict(ALL_FLAGS))
        (line,) = _aggregate_lines(out)
        positions = []
        for entry in SOURCE_FAILED_FLAGS:
            assert entry.check_name in line, f"{entry.check_name!r} missing from aggregate"
            positions.append(line.index(entry.check_name))
        assert positions == sorted(positions), "check names not in registry order"

    def test_two_of_five_aggregate_names_exactly_those_two(self):
        armed = {"source_failed": True, "projects_source_failed": True}
        out = _floor()._format_domain_context(dict(armed))
        (line,) = _aggregate_lines(out)
        assert NAMES["source_failed"] in line
        assert NAMES["projects_source_failed"] in line
        for flag in NAMES.keys() - armed.keys():
            assert NAMES[flag] not in line, f"{flag} named in aggregate while unarmed"
        assert out.count("check FAILED:") == 0
        assert out.count(SCOPE_DIRECTIVE) == 1

    def test_three_of_five_contract_acceptance_shape(self):
        # Contract §6.1: >= 3 armed flags produce ONE failure directive, not
        # three (the unit-testable half; the delivered-reply half is the
        # Colleague-Test check the contract says no unit test substitutes for).
        armed = {
            "source_failed": True,
            "pending_todos_source_failed": True,
            "completed_todos_source_failed": True,
        }
        out = _floor()._format_domain_context(dict(armed))
        assert len(_aggregate_lines(out)) == 1
        assert out.count("check FAILED:") == 0
        assert out.count(SCOPE_DIRECTIVE) == 1

    def test_composed_prompt_carries_single_aggregate(self):
        # One level up (m-43): the PROMPT the floor would hand the LLM —
        # not just the domain block in isolation.
        ctx = FloorContext(
            user_message="good morning, what's my status?",
            session_id="pin-1717",
            domain_context=dict(ALL_FLAGS),
        )
        prompt = _floor()._build_prompt(ctx)
        assert len(_aggregate_lines(prompt)) == 1
        assert prompt.count("check FAILED:") == 0
        assert prompt.count(SCOPE_DIRECTIVE) == 1


class TestSingleFailureUsesAggregate:
    """N == 1 (#1772): the SAME aggregate directive renders as N >= 2 — the
    former verbatim per-source line is gone. Pins the single check_name +
    CXO's new N-agnostic wording as a LITERAL, and that no OTHER check_name
    leaks into the line."""

    @pytest.mark.parametrize("flag", sorted(NAMES))
    def test_one_flag_renders_the_aggregate_with_only_its_own_check_name(self, flag):
        out = _floor()._format_domain_context({flag: True})
        aggs = _aggregate_lines(out)
        assert (
            len(aggs) == 1
        ), f"expected exactly one aggregate line at N==1, got {len(aggs)}:\n{out}"
        (line,) = aggs
        assert NAMES[flag] in line
        for other_flag, other_name in NAMES.items():
            if other_flag == flag:
                continue
            assert other_name not in line, f"{other_name!r} (unarmed) leaked into N==1 aggregate"
        assert line == AGGREGATE_PREFIX + NAMES[flag] + AGGREGATE_TAIL
        assert out.count("check FAILED:") == 0
        # The 1-flag case is where wrinkle 1 actually bit — the scope
        # directive must ride with a lone flag too.
        assert out.count(SCOPE_DIRECTIVE) == 1

    def test_zero_flags_render_no_failure_lines(self):
        out = _floor()._format_domain_context({"current_time": "now-ish"})
        assert "check FAILED:" not in out
        assert not _aggregate_lines(out)
        assert SCOPE_DIRECTIVE not in out


class TestDirectiveCopyPins1717:
    """Directive copy pinned as literals (8/21 lesson: pin NEW copy fragments,
    so drift is a test failure rather than a live regression)."""

    def test_renderer_emits_cxo_scope_copy_verbatim(self):
        out = _floor()._format_domain_context({"source_failed": True})
        assert SCOPE_DIRECTIVE in out
        # Key phrase pinned independently of the wrapping constant, so a
        # drifted renderer AND a drifted constant can't pass together by
        # agreeing with each other.
        assert "never imply a source failed when it was simply not consulted" in out

    def test_aggregate_copy_key_phrases(self):
        # The aggregate's load-bearing clauses (#1772 N-agnostic wording):
        # one-sentence composition and the unified honesty guard.
        armed = {"source_failed": True, "projects_source_failed": True}
        out = _floor()._format_domain_context(dict(armed))
        assert "name what wasn't checked in ONE sentence" in out
        assert "never one caveat per item" in out
        assert "Don't claim it's empty or fine" in out
        assert "never invent details to fill the gap" in out

    def test_aggregate_copy_present_at_single_failure(self):
        # #1772 inverts the pre-unification pin: the aggregate copy now
        # renders at N == 1 too — there is no separate single-failure copy
        # for it to be "absent" in favor of.
        out = _floor()._format_domain_context({"source_failed": True})
        assert "never one caveat per item" in out
        assert "name what wasn't checked in ONE sentence" in out

    def test_full_aggregate_sentence_verbatim_at_n_equals_one(self):
        # #1772: pin the FULL new sentence verbatim, not just key phrases.
        out = _floor()._format_domain_context({"source_failed": True})
        expected = AGGREGATE_PREFIX + NAMES["source_failed"] + AGGREGATE_TAIL
        assert expected in out

    def test_anti_reassurance_directive_in_fabrication_block(self):
        # #1717 wrinkle 2: lives in the never-fabricate section of the floor
        # addendum, because comfort about unread state is a fabrication, not
        # a tone slip (CXO memo, 2026-09-01). Unchanged by the composition fix.
        start = FLOOR_SYSTEM_PROMPT_ADDENDUM.index("CRITICAL — Never fabricate user data")
        end = FLOOR_SYSTEM_PROMPT_ADDENDUM.index("CRITICAL", start + 10)
        section = FLOOR_SYSTEM_PROMPT_ADDENDUM[start:end]
        assert "Do not reassure the user about data you could not read" in section
        assert "you may NOT say their data is safe, intact, unaffected" in section
        assert "Comfort about unread state is a claim about that state." in section

    def test_anti_reassurance_directive_appears_once(self):
        assert (
            FLOOR_SYSTEM_PROMPT_ADDENDUM.count(
                "Do not reassure the user about data you could not read"
            )
            == 1
        )
