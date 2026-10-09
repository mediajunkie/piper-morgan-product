"""DRAFT — #1595 Epic 0 Phase 3, rule-10 corpus rows for HELD literals.

Dispatched by Lead, 2026-10-09 (prog, Sonnet, DRAFTING TASK — no code/corpus/test
changes, no commits). Context: the 2026-10-09 "19-plus" batch
(dev/2026/10/09/2026-10-09-1023-prog-code-log-1595-phase3-deletions-19-plus.md)
attempted a 9-list partial-deletion batch, broke 95 pre-existing unit tests, and
reverted. Root cause (filed as #1969, ratified as rule 10 in
dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md): "Zero corpus rows
is absence of evidence, per literal ... A non-survivor with zero rows is held,
the same as a zero-row list, until it has rows ... A unit test that fails on a
deletion is a phrasing the corpus is missing. Add its phrasing as a corpus row."

This file is NOT the corpus. It is a draft for the Lead to review, correct, and
merge into `scripts/build_inversion_corpus_phase0.py`'s HAND_ROWS before anyone
re-attempts the 9-list batch (or scores these rows).

## Method

1. Ran `venv/bin/python scripts/inversion_phase3_deletion_gate.py --list <NAME>`
   for all 9 lists named in the dispatch. Collected every line printed as
   "HELD (rule 10, needs its own corpus row before deletion): r"..."".

2. For each HELD literal, searched the test files the 10-09 log named as broken
   by the (reverted) deletion, for a phrase the literal's own regex claims. Where
   found, used the test's own phrase verbatim ("origin": "test") and cited the
   test by file::class::test (or file::test). Where no test exercises a literal,
   wrote a natural phrasing and marked it ("origin": "synthesized").

3. Verified EVERY phrase below two ways, both run this session
   (scripts under /tmp, not committed):
   - `PreClassifier.pre_classify(phrase)` returns the list's own uniform claim
     action/category (confirms the phrase is claimed by *some* list, matching
     the list's known claim branch — not a different list's claim).
   - A manual scan of the list's own literals in source order confirms the
     FIRST one that matches `phrase.lower()` is the exact literal this row is
     for (not an earlier sibling literal in the same list stealing the claim).
   All 47 rows below passed both checks — `claimed_ok: True` throughout, no
   exceptions, no shadowed literals found in this batch (contrast with several
   prior Phase-3 deposit lanes that found a few structurally-unreachable
   literals; none turned up here).

## Totals

- 47 rows drafted, covering 47 of the 48 literals the dispatch estimated as
  held. The gate's own `--list` output for all 9 named lists sums to exactly
  47 HELD literals (7 PROVENANCE + 12 PORTFOLIO + 5 IDENTITY + 9 DOCUMENT_QUERY
  + 5 FEATURE_INFO + 3 STAKEHOLDER_UPDATE + 3 TODO_COMPLETE + 3
  SET_DEFAULT_REPO + 0 REPO_MANAGEMENT). REPO_MANAGEMENT_PATTERNS contributes
  ZERO literals to this list — see the note at the bottom of this file. The
  dispatch's "48" was evidently a close estimate, not measured against today's
  `--list` output; flagged for the Lead rather than silently reconciled.
- 38 of 47 rows are test-derived ("origin": "test"); 9 are synthesized.
- 1 row (DOCUMENT_QUERY_PATTERNS' "change ... to" literal) is "expected":
  "REVIEW" with a lead_question — see below.
- All other 46 rows have a confident "expected": "action:<name>" assertion.

## REPO_MANAGEMENT_PATTERNS — explicitly OUT of this draft, and why

`--list REPO_MANAGEMENT_PATTERNS` reports "verdict: GO (partial) ... 0 HELD
(rule 10: no claiming row)" — every one of its 4 non-survivor literals
(the two bare "link owner/repo" / "connect owner/repo" forms, "add owner/repo
to ...", and "show project repositories") already has >=1 claiming corpus row.
Rule 10 (zero-row literals are held) therefore finds NOTHING to hold here —
this list is not in scope for "deposit a row" work.

But the 10-09 log shows its deletion broke `test_repo_management.py` (5),
`test_integration_connect_preclassifier_1417.py`, and
`test_spend_free_canonical_ratchet_1818.py` (2) anyway. Looking at the gate's
own per-row output for this list (re-run this session), several of its
CLAIMED rows score [FAIL] — MISMATCH, non-live REVIEW, or UNSCORED — yet the
list still reads "GO (partial)" because the gate's partial-deletion GO/NO-GO
logic only checks "does >=1 row exist", not "does every claimed row pass".
That is a DIFFERENT gap than #1969's "zero rows" gap — it's the one #1969's
own proposal (3) flagged for audit ("an audit of the six already-landed
partial deletions ... for the same blind spot"), now shown to apply to a
*seventh* list that hasn't even landed yet. I'm reporting this rather than
drafting rows for it, since rule 10 as currently written doesn't ask for rows
here and inventing a fix to the gate's GO logic is out of this drafting
task's scope.

## The REVIEW row

DOCUMENT_QUERY_PATTERNS' `r"\\bchange\\s+(?:the\\s+)?[\\w\\s]+\\s+to\\b"` literal
is exercised, verbatim, by an EXISTING pinned test
(`test_explicit_issue_update_1411.py::TestOrderingAndWiring::
test_surface1_still_claims_no_hash_form`), which asserts
`PreClassifier.pre_classify("change the title of issue 108 to test new
regressions").action == "update_document_query"`. That is a real, passing,
test-derived claim.

But the SAME file's docstring and `TestOrderingAndWiring::
test_classify_multiple_resolves_before_document_claim` establish that this
exact phrase's RULED, full-pipeline destination is `update_issue` (B3 Stage 0
intercepts it before the document claim can act, in the `classify_multiple`
entry) — the surface-1 claim this literal produces is the #1411 BUG shape,
not the correct answer. I don't know which of the two entry points the
deletion gate's "surface 1" reads for this specific literal/row combination
with enough confidence to assert either `action:update_document_query`
(restates the known bug as "expected") or `action:update_issue` (asserts a
destination this exact literal's claim never produces at its own entry
point). Flagged REVIEW rather than guessed — see `lead_question` on the row.

## Verified how

Every `claimed_ok` below is from `PreClassifier.pre_classify(...)` plus a
manual list-order scan, both run this session against this worktree's HEAD
(`services/intent_service/pre_classifier.py` — no diff, confirmed via
`git status --short` before and after this task; this is a drafting task,
nothing in the working tree changed). Layer: deterministic/surface-1 only,
zero LLM calls. Denominator: all 47 rows this file claims to have verified,
individually, by index match against each list's own literal order — not a
sample.
"""

HELD_LITERAL_ROWS_DRAFT = [
    # ============================================================
    # PROVENANCE_PATTERNS — 7/7 HELD literals covered, all test-derived.
    # Test: tests/unit/services/test_pre_classifier.py::TestPreClassifier::
    #       test_provenance_routes_before_trust (Issue #1030 R4). The test
    #       asserts both category==PROVENANCE and action=="explain_suggestion"
    #       for every phrase in its list — a direct, strict assertion.
    # ============================================================
    {
        "phrase": "Where did you get that from?",
        "category": "PROVENANCE",
        "expected": "action:explain_suggestion",
        "literal": r"\bwhere did (you get|that come from|you find)\b",
        "list": "PROVENANCE_PATTERNS",
        "test_ref": "tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_provenance_routes_before_trust",
        "origin": "test",
        "source": 'phase3-conversion/PROVENANCE_PATTERNS literal r"\\bwhere did (you get|that come from|you find)\\b"',
        "claimed_ok": True,
    },
    {
        "phrase": "How did you know about that?",
        "category": "PROVENANCE",
        "expected": "action:explain_suggestion",
        "literal": r"\bhow did you know( about| that)?\b",
        "list": "PROVENANCE_PATTERNS",
        "test_ref": "tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_provenance_routes_before_trust",
        "origin": "test",
        "source": 'phase3-conversion/PROVENANCE_PATTERNS literal r"\\bhow did you know( about| that)?\\b"',
        "claimed_ok": True,
    },
    {
        "phrase": "What made you mention the priority?",
        "category": "PROVENANCE",
        "expected": "action:explain_suggestion",
        "literal": r"\bwhat made you (mention|think|suggest|bring)\b",
        "list": "PROVENANCE_PATTERNS",
        "test_ref": "tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_provenance_routes_before_trust",
        "origin": "test",
        "source": 'phase3-conversion/PROVENANCE_PATTERNS literal r"\\bwhat made you (mention|think|suggest|bring)\\b"',
        "claimed_ok": True,
    },
    {
        "phrase": "How do you know about my schedule?",
        "category": "PROVENANCE",
        "expected": "action:explain_suggestion",
        "literal": r"\bhow do you know (about|that)\b",
        "list": "PROVENANCE_PATTERNS",
        "test_ref": "tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_provenance_routes_before_trust",
        "origin": "test",
        "source": 'phase3-conversion/PROVENANCE_PATTERNS literal r"\\bhow do you know (about|that)\\b"',
        "claimed_ok": True,
    },
    {
        "phrase": "Why is that on your list?",
        "category": "PROVENANCE",
        "expected": "action:explain_suggestion",
        "literal": r"\bwhy.* on (my|your|the) (list|radar|mind)\b",
        "list": "PROVENANCE_PATTERNS",
        "test_ref": "tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_provenance_routes_before_trust",
        "origin": "test",
        "source": 'phase3-conversion/PROVENANCE_PATTERNS literal r"\\bwhy.* on (my|your|the) (list|radar|mind)\\b"',
        "claimed_ok": True,
    },
    {
        "phrase": "Based on what?",
        "category": "PROVENANCE",
        "expected": "action:explain_suggestion",
        "literal": r"\bbased on what\b",
        "list": "PROVENANCE_PATTERNS",
        "test_ref": "tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_provenance_routes_before_trust",
        "origin": "test",
        "source": 'phase3-conversion/PROVENANCE_PATTERNS literal r"\\bbased on what\\b"',
        "claimed_ok": True,
    },
    {
        "phrase": "What's that based on?",
        "category": "PROVENANCE",
        "expected": "action:explain_suggestion",
        "literal": r"\bwhat'?s that based on\b",
        "list": "PROVENANCE_PATTERNS",
        "test_ref": "tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_provenance_routes_before_trust",
        "origin": "test",
        "source": 'phase3-conversion/PROVENANCE_PATTERNS literal r"\\bwhat\'?s that based on\\b"',
        "claimed_ok": True,
    },
    # ============================================================
    # PORTFOLIO_PATTERNS — 12/12 HELD literals covered. 11 test-derived from
    # the SAME test (Issue #675's canonical list), 1 synthesized (bare "new
    # project", which no existing test exercises without an add/create verb).
    # Test: tests/unit/services/test_pre_classifier.py::TestPreClassifier::
    #       test_portfolio_patterns — asserts category==PORTFOLIO,
    #       action=="manage_portfolio", confidence==1.0 for every phrase.
    # Rule 4 (effect-aware): hide/delete/remove/get-rid-of are destructive
    # (remove a project from view or permanently); restore/unarchive/
    # bring-back are the WRITE-but-restorative inverse; add/create and bare
    # "new project" are WRITE (create). None of these should be deleted on
    # a bare GO without surface-2 (N=5, agreeing) confirming no sample lands
    # somewhere worse than "ask which project" / "I can't find that project".
    # ============================================================
    {
        "phrase": "hide the project Beta",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "literal": r"\bhide\s+(?=.*\bprojects?\b)(?:my\s+)?(?:the\s+)?(?:project\s+)?(.+)",
        "list": "PORTFOLIO_PATTERNS",
        "test_ref": "tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_portfolio_patterns",
        "origin": "test",
        "source": 'phase3-conversion/PORTFOLIO_PATTERNS literal r"\\bhide\\s+(?=.*\\bprojects?\\b)(?:my\\s+)?(?:the\\s+)?(?:project\\s+)?(.+)"',
        "notes": "rule 4 (effect-aware): hide is destructive-shaped (removes the project from the visible list); surface-2 N=5 agreement should be required before deletion.",
        "claimed_ok": True,
    },
    {
        "phrase": "put the old project away",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "literal": r"\bput\s+(?=.*\bprojects?\b)(.+)\s+(?:away|aside)",
        "list": "PORTFOLIO_PATTERNS",
        "test_ref": "tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_portfolio_patterns",
        "origin": "test",
        "source": 'phase3-conversion/PORTFOLIO_PATTERNS literal r"\\bput\\s+(?=.*\\bprojects?\\b)(.+)\\s+(?:away|aside)"',
        "notes": "rule 4: same destructive shape as hide/archive — put-away is this codebase's archive synonym.",
        "claimed_ok": True,
    },
    {
        "phrase": "delete my project Gamma",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "literal": r"\bdelete\s+(?!.*\b(?:reminders?|to-?dos?|tasks?)\b)(?=.*\bprojects?\b)(?:my\s+)?(?:the\s+)?(?:project\s+)?(.+)",
        "list": "PORTFOLIO_PATTERNS",
        "test_ref": "tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_portfolio_patterns",
        "origin": "test",
        "source": 'phase3-conversion/PORTFOLIO_PATTERNS literal r"\\bdelete\\s+(?!.*\\b(?:reminders?|to-?dos?|tasks?)\\b)(?=.*\\bprojects?\\b)(?:my\\s+)?(?:the\\s+)?(?:project\\s+)?(.+)"',
        "notes": "rule 4: genuinely destructive (deletes a project). Also pinned by test_portfolio_delete_greed_audit_1527.py's PROJECT_DELETES tuple — the #1527 audit's own positive-evidence narrowing guard. Do not delete without surface-2 confirming no sample routes to a non-WRITE/non-DESTRUCTIVE op.",
        "claimed_ok": True,
    },
    {
        "phrase": "remove the project Delta",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "literal": r"\bremove\s+(?!.*\b(?:reminders?|to-?dos?|tasks?)\b)(?=.*\bprojects?\b)(?:my\s+)?(?:the\s+)?(?:project\s+)?(.+)",
        "list": "PORTFOLIO_PATTERNS",
        "test_ref": "tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_portfolio_patterns",
        "origin": "test",
        "source": 'phase3-conversion/PORTFOLIO_PATTERNS literal r"\\bremove\\s+(?!.*\\b(?:reminders?|to-?dos?|tasks?)\\b)(?=.*\\bprojects?\\b)(?:my\\s+)?(?:the\\s+)?(?:project\\s+)?(.+)"',
        "notes": "rule 4: destructive, same family as delete. Also pinned by test_portfolio_delete_greed_audit_1527.py's PROJECT_DELETES tuple.",
        "claimed_ok": True,
    },
    {
        "phrase": "get rid of my test project",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "literal": r"\bget rid of\s+(?!.*\b(?:reminders?|to-?dos?|tasks?)\b)(?=.*\bprojects?\b)(?:my\s+)?(?:the\s+)?(?:project\s+)?(.+)",
        "list": "PORTFOLIO_PATTERNS",
        "test_ref": "tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_portfolio_patterns",
        "origin": "test",
        "source": 'phase3-conversion/PORTFOLIO_PATTERNS literal r"\\bget rid of\\s+(?!.*\\b(?:reminders?|to-?dos?|tasks?)\\b)(?=.*\\bprojects?\\b)(?:my\\s+)?(?:the\\s+)?(?:project\\s+)?(.+)"',
        "notes": "rule 4: destructive, same family as delete/remove. Also pinned by test_portfolio_delete_greed_audit_1527.py's PROJECT_DELETES tuple.",
        "claimed_ok": True,
    },
    {
        "phrase": "restore project Epsilon",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "literal": r"\brestore\s+(?=.*\bprojects?\b)(?:my\s+)?(?:the\s+)?(?:project\s+)?(.+)",
        "list": "PORTFOLIO_PATTERNS",
        "test_ref": "tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_portfolio_patterns",
        "origin": "test",
        "source": 'phase3-conversion/PORTFOLIO_PATTERNS literal r"\\brestore\\s+(?=.*\\bprojects?\\b)(?:my\\s+)?(?:the\\s+)?(?:project\\s+)?(.+)"',
        "notes": "WRITE (un-deletes/restores); not itself destructive, but mutates state — also pinned by test_portfolio_archive_greed_1757.py.",
        "claimed_ok": True,
    },
    {
        "phrase": "unarchive the old project",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "literal": r"\bunarchive\s+(?=.*\bprojects?\b)(?:my\s+)?(?:the\s+)?(.+)",
        "list": "PORTFOLIO_PATTERNS",
        "test_ref": "tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_portfolio_patterns",
        "origin": "test",
        "source": 'phase3-conversion/PORTFOLIO_PATTERNS literal r"\\bunarchive\\s+(?=.*\\bprojects?\\b)(?:my\\s+)?(?:the\\s+)?(.+)"',
        "notes": "WRITE (restorative); also pinned by test_portfolio_archive_greed_1757.py as the issue's own named edge case.",
        "claimed_ok": True,
    },
    {
        "phrase": "bring back my archived project",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "literal": r"\bbring back\s+(?=.*\bprojects?\b)(?:my\s+)?(?:the\s+)?(?:project\s+)?(.+)",
        "list": "PORTFOLIO_PATTERNS",
        "test_ref": "tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_portfolio_patterns",
        "origin": "test",
        "source": 'phase3-conversion/PORTFOLIO_PATTERNS literal r"\\bbring back\\s+(?=.*\\bprojects?\\b)(?:my\\s+)?(?:the\\s+)?(?:project\\s+)?(.+)"',
        "notes": "WRITE (restorative); also pinned by test_portfolio_archive_greed_1757.py.",
        "claimed_ok": True,
    },
    {
        "phrase": "search projects for budget",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "literal": r"\bsearch\s+(?:my\s+)?projects?\s+(?:for\s+)?(.+)",
        "list": "PORTFOLIO_PATTERNS",
        "test_ref": "tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_portfolio_patterns",
        "origin": "test",
        "source": 'phase3-conversion/PORTFOLIO_PATTERNS literal r"\\bsearch\\s+(?:my\\s+)?projects?\\s+(?:for\\s+)?(.+)"',
        "notes": "READ, not WRITE — rule 4 N/A. Also present in test_subsumption_portfolio_write_family_1884.py::test_search_projects_read_verb_single_intent_no_status_to_begin_with as the read-verb control case for that file's write-family subsumption tests.",
        "claimed_ok": True,
    },
    {
        "phrase": "find project deadline",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "literal": r"\bfind\s+(?:my\s+)?project\s+(.+)",
        "list": "PORTFOLIO_PATTERNS",
        "test_ref": "tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_portfolio_patterns",
        "origin": "test",
        "source": 'phase3-conversion/PORTFOLIO_PATTERNS literal r"\\bfind\\s+(?:my\\s+)?project\\s+(.+)"',
        "notes": "READ, not WRITE — rule 4 N/A.",
        "claimed_ok": True,
    },
    {
        "phrase": "add a new project",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "literal": r"\b(?:add|create)\s+(?:a\s+)?(?:new\s+)?project\b",
        "list": "PORTFOLIO_PATTERNS",
        "test_ref": "tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_portfolio_patterns",
        "origin": "test",
        "source": 'phase3-conversion/PORTFOLIO_PATTERNS literal r"\\b(?:add|create)\\s+(?:a\\s+)?(?:new\\s+)?project\\b"',
        "notes": "WRITE (creates a project); not destructive.",
        "claimed_ok": True,
    },
    {
        "phrase": "I'd like to start a new project",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "literal": r"\bnew project\b",
        "list": "PORTFOLIO_PATTERNS",
        "test_ref": None,
        "origin": "synthesized",
        "source": 'phase3-conversion/PORTFOLIO_PATTERNS literal r"\\bnew project\\b"',
        "notes": (
            "No existing test exercises bare 'new project' without an add/create verb — "
            "test_portfolio_patterns' own phrases ('add a new project', 'create a project') "
            'are claimed by the PRECEDING survivor literal r"\\b(?:add|create)...\\bproject\\b", '
            "confirmed by this session's literal-index check. WRITE (creates a project); not destructive."
        ),
        "claimed_ok": True,
    },
    # ============================================================
    # IDENTITY_PATTERNS — 5/5 HELD literals covered, all test-derived, all
    # from the SAME parametrized test.
    # Test: tests/unit/services/intent_service/test_discovery_intent.py::
    #       test_identity_patterns_still_work — asserts category==IDENTITY,
    #       action=="get_identity" for each parametrized phrase.
    # No rule-4 concern — pure READ (identity disclosure), no mutation.
    # ============================================================
    {
        "phrase": "what's your name",
        "category": "IDENTITY",
        "expected": "action:get_identity",
        "literal": r"\bwhat'?s your name\b",
        "list": "IDENTITY_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_discovery_intent.py::test_identity_patterns_still_work",
        "origin": "test",
        "source": 'phase3-conversion/IDENTITY_PATTERNS literal r"\\bwhat\'?s your name\\b"',
        "claimed_ok": True,
    },
    {
        "phrase": "your role",
        "category": "IDENTITY",
        "expected": "action:get_identity",
        "literal": r"\byour role\b",
        "list": "IDENTITY_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_discovery_intent.py::test_identity_patterns_still_work",
        "origin": "test",
        "source": 'phase3-conversion/IDENTITY_PATTERNS literal r"\\byour role\\b"',
        "claimed_ok": True,
    },
    {
        "phrase": "what do you do",
        "category": "IDENTITY",
        "expected": "action:get_identity",
        "literal": r"\bwhat do you do\b",
        "list": "IDENTITY_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_discovery_intent.py::test_identity_patterns_still_work",
        "origin": "test",
        "source": 'phase3-conversion/IDENTITY_PATTERNS literal r"\\bwhat do you do\\b"',
        "notes": "test's own comment: 'This is ambiguous but kept in IDENTITY' — a deliberate, not accidental, claim.",
        "claimed_ok": True,
    },
    {
        "phrase": "tell me about yourself",
        "category": "IDENTITY",
        "expected": "action:get_identity",
        "literal": r"\btell me about yourself\b",
        "list": "IDENTITY_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_discovery_intent.py::test_identity_patterns_still_work",
        "origin": "test",
        "source": 'phase3-conversion/IDENTITY_PATTERNS literal r"\\btell me about yourself\\b"',
        "notes": "Also directly pinned in test_keyword_disambiguation_901.py::test_tell_me_about_yourself_still_identity as the #901 FEATURE_INFO/IDENTITY disambiguation regression guard.",
        "claimed_ok": True,
    },
    {
        "phrase": "introduce yourself",
        "category": "IDENTITY",
        "expected": "action:get_identity",
        "literal": r"\bintroduce yourself\b",
        "list": "IDENTITY_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_discovery_intent.py::test_identity_patterns_still_work",
        "origin": "test",
        "source": 'phase3-conversion/IDENTITY_PATTERNS literal r"\\bintroduce yourself\\b"',
        "claimed_ok": True,
    },
    # ============================================================
    # DOCUMENT_QUERY_PATTERNS — 9/9 HELD literals covered: 7 test-derived
    # (6 from one file, 1 from a second), 1 synthesized, 1 REVIEW.
    # Primary test: tests/unit/services/intent_service/test_document_query_
    #       handlers.py::TestPreClassifierDocumentRouting (Issue #522)
    # Category per corpus convention (confirmed against existing corpus rows,
    # NOT the surface-1 Intent.category, which reads QUERY for this action —
    # the corpus's own category bucket for update_document_query is EXECUTION,
    # per scripts/build_inversion_corpus_phase0.py's _ACTION_CATEGORY map and
    # multiple existing corpus rows, e.g. "update the project plan doc with
    # the new dates" / "update the roadmap doc with the new dates").
    # ============================================================
    {
        "phrase": "edit the meeting notes document",
        "category": "EXECUTION",
        "expected": "action:update_document_query",
        "literal": r"\bedit\s+(?:the\s+)?[\w\s]+\s+doc(?:ument)?\b",
        "list": "DOCUMENT_QUERY_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_document_query_handlers.py::TestPreClassifierDocumentRouting::test_document_update_queries_route_to_update_action",
        "origin": "test",
        "source": 'phase3-conversion/DOCUMENT_QUERY_PATTERNS literal r"\\bedit\\s+(?:the\\s+)?[\\w\\s]+\\s+doc(?:ument)?\\b"',
        "claimed_ok": True,
    },
    {
        "phrase": "modify the status document",
        "category": "EXECUTION",
        "expected": "action:update_document_query",
        "literal": r"\bmodify\s+(?:the\s+)?[\w\s]+\s+doc(?:ument)?\b",
        "list": "DOCUMENT_QUERY_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_document_query_handlers.py::TestPreClassifierDocumentRouting::test_document_update_queries_route_to_update_action",
        "origin": "test",
        "source": 'phase3-conversion/DOCUMENT_QUERY_PATTERNS literal r"\\bmodify\\s+(?:the\\s+)?[\\w\\s]+\\s+doc(?:ument)?\\b"',
        "claimed_ok": True,
    },
    {
        "phrase": "change the spec doc",
        "category": "EXECUTION",
        "expected": "action:update_document_query",
        "literal": r"\bchange\s+(?:the\s+)?[\w\s]+\s+doc(?:ument)?\b",
        "list": "DOCUMENT_QUERY_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_document_query_handlers.py::TestPreClassifierDocumentRouting::test_document_update_queries_route_to_update_action",
        "origin": "test",
        "source": 'phase3-conversion/DOCUMENT_QUERY_PATTERNS literal r"\\bchange\\s+(?:the\\s+)?[\\w\\s]+\\s+doc(?:ument)?\\b"',
        "claimed_ok": True,
    },
    {
        "phrase": "add to the notes document new items",
        "category": "EXECUTION",
        "expected": "action:update_document_query",
        "literal": r"\badd\s+(?:to\s+)?(?:the\s+)?[\w\s]+\s+doc(?:ument)?\b",
        "list": "DOCUMENT_QUERY_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_document_query_handlers.py::TestPreClassifierDocumentRouting::test_document_add_queries_route_correctly",
        "origin": "test",
        "source": 'phase3-conversion/DOCUMENT_QUERY_PATTERNS literal r"\\badd\\s+(?:to\\s+)?(?:the\\s+)?[\\w\\s]+\\s+doc(?:ument)?\\b"',
        "claimed_ok": True,
    },
    {
        "phrase": "append to the log doc",
        "category": "EXECUTION",
        "expected": "action:update_document_query",
        "literal": r"\bappend\s+(?:to\s+)?(?:the\s+)?[\w\s]+\s+doc(?:ument)?\b",
        "list": "DOCUMENT_QUERY_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_document_query_handlers.py::TestPreClassifierDocumentRouting::test_document_add_queries_route_correctly",
        "origin": "test",
        "source": 'phase3-conversion/DOCUMENT_QUERY_PATTERNS literal r"\\bappend\\s+(?:to\\s+)?(?:the\\s+)?[\\w\\s]+\\s+doc(?:ument)?\\b"',
        "claimed_ok": True,
    },
    {
        "phrase": "update project plan with new deadline",
        "category": "EXECUTION",
        "expected": "action:update_document_query",
        "literal": r"\bupdate\s+(?:the\s+)?[\w\s]+\s+with\b",
        "list": "DOCUMENT_QUERY_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_document_query_handlers.py::TestPreClassifierDocumentRouting::test_document_update_with_content_routes_correctly",
        "origin": "test",
        "source": 'phase3-conversion/DOCUMENT_QUERY_PATTERNS literal r"\\bupdate\\s+(?:the\\s+)?[\\w\\s]+\\s+with\\b"',
        "notes": "the identical shape ('update the roadmap with the new dates') is also directly pinned by test_pre_classifier_stakeholder_update_1256.py::TestDocumentUpdateNonRegression::test_update_x_with_y_still_routes_to_document_query.",
        "claimed_ok": True,
    },
    {
        "phrase": "edit the report with corrections",
        "category": "EXECUTION",
        "expected": "action:update_document_query",
        "literal": r"\bedit\s+(?:the\s+)?[\w\s]+\s+with\b",
        "list": "DOCUMENT_QUERY_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_document_query_handlers.py::TestPreClassifierDocumentRouting::test_document_update_with_content_routes_correctly",
        "origin": "test",
        "source": 'phase3-conversion/DOCUMENT_QUERY_PATTERNS literal r"\\bedit\\s+(?:the\\s+)?[\\w\\s]+\\s+with\\b"',
        "claimed_ok": True,
    },
    {
        "phrase": "modify the onboarding checklist with the new steps",
        "category": "EXECUTION",
        "expected": "action:update_document_query",
        "literal": r"\bmodify\s+(?:the\s+)?[\w\s]+\s+with\b",
        "list": "DOCUMENT_QUERY_PATTERNS",
        "test_ref": None,
        "origin": "synthesized",
        "source": 'phase3-conversion/DOCUMENT_QUERY_PATTERNS literal r"\\bmodify\\s+(?:the\\s+)?[\\w\\s]+\\s+with\\b"',
        "notes": (
            "No existing test exercises 'modify ... with' specifically. 'expected' is read "
            "directly off PreClassifier's uniform DOCUMENT_QUERY_PATTERNS claim branch "
            "(code-read, not test-asserted) — deliberately avoided the word 'doc'/'document' "
            "anywhere in the phrase so it can't be shadowed by the earlier modify...doc literal "
            "(confirmed by this session's literal-index check: winner_idx==target_idx)."
        ),
        "claimed_ok": True,
    },
    {
        "phrase": "change the title of issue 108 to test new regressions",
        "category": "EXECUTION",
        "expected": "REVIEW",
        "literal": r"\bchange\s+(?:the\s+)?[\w\s]+\s+to\b",
        "list": "DOCUMENT_QUERY_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_explicit_issue_update_1411.py::TestOrderingAndWiring::test_surface1_still_claims_no_hash_form",
        "origin": "test",
        "source": 'phase3-conversion/DOCUMENT_QUERY_PATTERNS literal r"\\bchange\\s+(?:the\\s+)?[\\w\\s]+\\s+to\\b"',
        "lead_question": (
            "The cited test strictly asserts PreClassifier.pre_classify(this exact phrase)."
            "action == 'update_document_query' — that IS this literal's claim, test-derived "
            "and currently passing. But the SAME file's "
            "test_classify_multiple_resolves_before_document_claim (and its own docstring) "
            "establish the phrase's RULED, full-pipeline destination is 'update_issue' — B3 "
            "Stage 0 intercepts it in the classify_multiple entry BEFORE this literal's claim "
            "can act; the literal's claim at the bare pre_classify entry is the #1411 BUG "
            "shape, not the correct answer. I don't know whether the deletion gate's 'surface "
            "1' reading for this literal/row combination models the bare pre_classify entry "
            "(where this literal is live and claims update_document_query) or something closer "
            "to the full pipeline (where B3 wins and the answer is update_issue) with enough "
            "confidence to assert either as 'expected' here. Rule 4 is relevant either way: "
            "update_issue is a WRITE. Marking REVIEW rather than guessing which destination "
            "the gate should score this row against — this is a decision for the Lead/Arch, "
            "not something a drafting pass should resolve by picking one."
        ),
        "claimed_ok": True,
    },
    # ============================================================
    # FEATURE_INFO_PATTERNS — 5/5 HELD literals covered: 1 test-derived,
    # 4 synthesized (no test exercises "how does X work" / "what is the X
    # integration" / "learn about X" / "information about X" specifically —
    # only the "tell me about <vocab word>" literal has test coverage).
    # Category QUERY per surface-1's own claim branch AND the test's direct
    # assertion (not EXECUTION — no write effect; pure information lookup).
    # No rule-4 concern — pure READ.
    # ============================================================
    {
        "phrase": "Tell me about Notion",
        "category": "QUERY",
        "expected": "action:get_feature_info",
        "literal": r"\btell me (?:more )?about\s+(?:github|slack|notion|calendar|mcp)\b",
        "list": "FEATURE_INFO_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_keyword_disambiguation_901.py::TestKeywordDisambiguationQ27::test_notion_integration_routes_to_query",
        "origin": "test",
        "source": 'phase3-conversion/FEATURE_INFO_PATTERNS literal r"\\btell me (?:more )?about\\s+(?:github|slack|notion|calendar|mcp)\\b"',
        "notes": (
            "The test asserts category==QUERY only (no explicit action assert); 'expected' "
            "action:get_feature_info is read directly off the uniform FEATURE_INFO_PATTERNS "
            "claim branch in pre_classifier.py, which this exact test file's sibling test "
            "(test_github_integration_routes_to_query) DOES assert explicitly for the survivor "
            "literal ('tell me more about the GitHub integration' -> action=='get_feature_info')."
        ),
        "claimed_ok": True,
    },
    {
        "phrase": "How does the Slack integration work?",
        "category": "QUERY",
        "expected": "action:get_feature_info",
        "literal": r"\bhow does the\s+\w+\s+(?:integration|feature|plugin|tool)\s+work\b",
        "list": "FEATURE_INFO_PATTERNS",
        "test_ref": None,
        "origin": "synthesized",
        "source": 'phase3-conversion/FEATURE_INFO_PATTERNS literal r"\\bhow does the\\s+\\w+\\s+(?:integration|feature|plugin|tool)\\s+work\\b"',
        "notes": "No existing test exercises this literal. expected is code-read (uniform claim branch), not test-asserted.",
        "claimed_ok": True,
    },
    {
        "phrase": "What is the Notion integration?",
        "category": "QUERY",
        "expected": "action:get_feature_info",
        "literal": r"\bwhat is the\s+\w+\s+(?:integration|feature|plugin)\b",
        "list": "FEATURE_INFO_PATTERNS",
        "test_ref": None,
        "origin": "synthesized",
        "source": 'phase3-conversion/FEATURE_INFO_PATTERNS literal r"\\bwhat is the\\s+\\w+\\s+(?:integration|feature|plugin)\\b"',
        "notes": "No existing test exercises this literal. expected is code-read (uniform claim branch), not test-asserted.",
        "claimed_ok": True,
    },
    {
        "phrase": "I'd like to learn more about the GitHub integration.",
        "category": "QUERY",
        "expected": "action:get_feature_info",
        "literal": r"\blearn (?:more )?about the\s+\w+\s+(?:integration|feature)\b",
        "list": "FEATURE_INFO_PATTERNS",
        "test_ref": None,
        "origin": "synthesized",
        "source": 'phase3-conversion/FEATURE_INFO_PATTERNS literal r"\\blearn (?:more )?about the\\s+\\w+\\s+(?:integration|feature)\\b"',
        "notes": "No existing test exercises this literal. expected is code-read (uniform claim branch), not test-asserted.",
        "claimed_ok": True,
    },
    {
        "phrase": "Can you give me information about the Slack integration?",
        "category": "QUERY",
        "expected": "action:get_feature_info",
        "literal": r"\binformation about the\s+\w+\s+(?:integration|feature)\b",
        "list": "FEATURE_INFO_PATTERNS",
        "test_ref": None,
        "origin": "synthesized",
        "source": 'phase3-conversion/FEATURE_INFO_PATTERNS literal r"\\binformation about the\\s+\\w+\\s+(?:integration|feature)\\b"',
        "notes": "No existing test exercises this literal. expected is code-read (uniform claim branch), not test-asserted.",
        "claimed_ok": True,
    },
    # ============================================================
    # STAKEHOLDER_UPDATE_PATTERNS — 3/3 HELD literals covered, all
    # test-derived from the same file (Issue #1256's own regression suite).
    # Test: tests/unit/services/intent_service/
    #       test_pre_classifier_stakeholder_update_1256.py::
    #       TestStakeholderUpdateRouting
    # Category SYNTHESIS per corpus convention (confirmed in both
    # _ACTION_CATEGORY and an existing corpus row: "write a short update for
    # the CEO on where we are" -> category SYNTHESIS, expected
    # action:write_stakeholder_update) — NOT surface-1's raw QUERY category.
    # No rule-4 concern — drafts prose, no destructive/write-to-system-state
    # effect in the sense rule 4 cares about.
    # ============================================================
    {
        "phrase": "Draft a status update for the board",
        "category": "SYNTHESIS",
        "expected": "action:write_stakeholder_update",
        "literal": r"\bdraft\s+(?:me\s+)?(?:a|an)?\s*(?:\w+\s+){0,3}update\s+for\b",
        "list": "STAKEHOLDER_UPDATE_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_pre_classifier_stakeholder_update_1256.py::TestStakeholderUpdateRouting::test_draft_status_update_for_routes_to_stakeholder_update",
        "origin": "test",
        "source": 'phase3-conversion/STAKEHOLDER_UPDATE_PATTERNS literal r"\\bdraft\\s+(?:me\\s+)?(?:a|an)?\\s*(?:\\w+\\s+){0,3}update\\s+for\\b"',
        "claimed_ok": True,
    },
    {
        "phrase": "Write something to send to Jake about the beta timeline",
        "category": "SYNTHESIS",
        "expected": "action:write_stakeholder_update",
        "literal": r"\bwrite\s+something\s+to\s+send\s+to\b",
        "list": "STAKEHOLDER_UPDATE_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_pre_classifier_stakeholder_update_1256.py::TestStakeholderUpdateRouting::test_write_something_to_send_to_routes_to_stakeholder_update",
        "origin": "test",
        "source": 'phase3-conversion/STAKEHOLDER_UPDATE_PATTERNS literal r"\\bwrite\\s+something\\s+to\\s+send\\s+to\\b"',
        "claimed_ok": True,
    },
    {
        "phrase": "I need a stakeholder update on the alpha program",
        "category": "SYNTHESIS",
        "expected": "action:write_stakeholder_update",
        "literal": r"\bstakeholder\s+update\b",
        "list": "STAKEHOLDER_UPDATE_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_pre_classifier_stakeholder_update_1256.py::TestStakeholderUpdateRouting::test_explicit_stakeholder_update_phrase_routes",
        "origin": "test",
        "source": 'phase3-conversion/STAKEHOLDER_UPDATE_PATTERNS literal r"\\bstakeholder\\s+update\\b"',
        "claimed_ok": True,
    },
    # ============================================================
    # TODO_COMPLETE_PATTERNS — 3/3 HELD literals covered: 1 test-derived,
    # 2 synthesized with a FINDING (the obvious test phrase for each is
    # actually claimed by a DIFFERENT, SURVIVING literal in the same list).
    # Category EXECUTION per existing corpus rows (many complete_todo rows
    # already present, all category EXECUTION).
    # These are WRITE ops (complete a todo) — not "delete/archive/remove/
    # hide" in rule 4's literal framing, but the same effect-aware caution
    # applies: don't delete without surface-2 confirming no sample lands on
    # a worse WRITE/DESTRUCTIVE op than the honest "which todo?" ask.
    # ============================================================
    {
        "phrase": "finish todo about deployment",
        "category": "EXECUTION",
        "expected": "action:complete_todo",
        "literal": r"\bfinish\s+todo\b",
        "list": "TODO_COMPLETE_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_todo_completion_lifecycle.py::test_finish_todo_pattern",
        "origin": "test",
        "source": 'phase3-conversion/TODO_COMPLETE_PATTERNS literal r"\\bfinish\\s+todo\\b"',
        "notes": "WRITE op (completes a todo); same effect-aware caution as rule 4.",
        "claimed_ok": True,
    },
    {
        "phrase": "Can we just mark done here?",
        "category": "EXECUTION",
        "expected": "action:complete_todo",
        "literal": r"\bmark\s+done\b",
        "list": "TODO_COMPLETE_PATTERNS",
        "test_ref": None,
        "origin": "synthesized",
        "source": 'phase3-conversion/TODO_COMPLETE_PATTERNS literal r"\\bmark\\s+done\\b"',
        "notes": (
            "FINDING: test_todo_completion_lifecycle.py::test_mark_done_pattern's own phrase "
            "('mark done the review docs todo') is NOT claimed by this literal — it's claimed "
            'by the earlier, SURVIVING literal r"\\b(?:mark|complete|finish)\\s+(?:the\\s+)?.+?'
            "\\s+(?:todo|task)\\b\" (the trailing 'todo' token wins the lazy-quantifier race "
            "before the bare 'mark done' literal is ever reached), confirmed by this session's "
            "literal-index check. Wrote a phrase with no trailing todo/task/done-family second "
            "token so this specific literal — not its survivor sibling — is the one that fires. "
            "WRITE op; same effect-aware caution as rule 4."
        ),
        "claimed_ok": True,
    },
    {
        "phrase": "Let's complete todo and move to the next one.",
        "category": "EXECUTION",
        "expected": "action:complete_todo",
        "literal": r"\bcomplete\s+todo\b",
        "list": "TODO_COMPLETE_PATTERNS",
        "test_ref": None,
        "origin": "synthesized",
        "source": 'phase3-conversion/TODO_COMPLETE_PATTERNS literal r"\\bcomplete\\s+todo\\b"',
        "notes": (
            "No existing test phrase isolates this literal the way test_finish_todo_pattern "
            "does for 'finish todo' — the obvious analogous phrasing ('complete todo about X') "
            "would risk the same survivor-literal shadowing test_mark_done_pattern's phrase hit "
            "(if X ever contains a later todo/task token). Wrote a phrase with no trailing "
            "todo/task/done-family second token so this literal fires, confirmed by this "
            "session's literal-index check. WRITE op; same effect-aware caution as rule 4."
        ),
        "claimed_ok": True,
    },
    # ============================================================
    # SET_DEFAULT_REPO_PATTERNS — 3/3 HELD literals covered: 2 test-derived
    # from the same parametrized test, 1 synthesized (no test exercises the
    # bare declarative "default repo is/should be/= X" form).
    # Category EXECUTION per existing corpus rows and _ACTION_CATEGORY
    # (NOT surface-1's raw QUERY category — same EXECUTION-vs-QUERY split as
    # DOCUMENT_QUERY_PATTERNS above; confirmed against an existing corpus row:
    # "set my default repo to acme/widgets" -> category EXECUTION, expected
    # action:set_default_repo).
    # WRITE (sets a config value); not destructive, but still a config
    # mutation — surface-2 agreement before deletion is still the safe move.
    # ============================================================
    {
        "phrase": "use mediajunkie/piper-morgan-product as my default repo",
        "category": "EXECUTION",
        "expected": "action:set_default_repo",
        "literal": r"\buse\s+[\w.-]+/[\w.-]+\s+as\s+(?:my\s+)?default\s+repo(?:sitory)?\b",
        "list": "SET_DEFAULT_REPO_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_set_default_repo_1327.py::TestPreClassifierSetDefaultRepoPatterns::test_set_default_repo_patterns_classify",
        "origin": "test",
        "source": 'phase3-conversion/SET_DEFAULT_REPO_PATTERNS literal r"\\buse\\s+[\\w.-]+/[\\w.-]+\\s+as\\s+(?:my\\s+)?default\\s+repo(?:sitory)?\\b"',
        "notes": "Test asserts category==QUERY (surface-1's raw category) and action=='set_default_repo'; this row's category follows the corpus's own EXECUTION bucket convention, not the surface-1 QUERY label — same distinction as the DOCUMENT_QUERY_PATTERNS rows above.",
        "claimed_ok": True,
    },
    {
        "phrase": "make mediajunkie/piper-morgan-product my default repo",
        "category": "EXECUTION",
        "expected": "action:set_default_repo",
        "literal": r"\bmake\s+[\w.-]+/[\w.-]+\s+(?:my\s+)?default\s+repo(?:sitory)?\b",
        "list": "SET_DEFAULT_REPO_PATTERNS",
        "test_ref": "tests/unit/services/intent_service/test_set_default_repo_1327.py::TestPreClassifierSetDefaultRepoPatterns::test_set_default_repo_patterns_classify",
        "origin": "test",
        "source": 'phase3-conversion/SET_DEFAULT_REPO_PATTERNS literal r"\\bmake\\s+[\\w.-]+/[\\w.-]+\\s+(?:my\\s+)?default\\s+repo(?:sitory)?\\b"',
        "notes": "Same EXECUTION-vs-surface-1-QUERY note as the row above.",
        "claimed_ok": True,
    },
    {
        "phrase": "My default repo should be mediajunkie/piper-morgan-product.",
        "category": "EXECUTION",
        "expected": "action:set_default_repo",
        "literal": r"\b(?:my\s+)?default\s+repo(?:sitory)?\s+(?:is|should be|=)\s+[\w.-]+/[\w.-]+",
        "list": "SET_DEFAULT_REPO_PATTERNS",
        "test_ref": None,
        "origin": "synthesized",
        "source": 'phase3-conversion/SET_DEFAULT_REPO_PATTERNS literal r"\\b(?:my\\s+)?default\\s+repo(?:sitory)?\\s+(?:is|should be|=)\\s+[\\w.-]+/[\\w.-]+"',
        "notes": (
            "No existing test exercises the bare declarative form ('default repo is/should "
            "be/= X'), only the imperative 'use X as'/'make X my' forms. expected is code-read "
            "(uniform SET_DEFAULT_REPO_PATTERNS claim branch), not test-asserted."
        ),
        "claimed_ok": True,
    },
]

assert len(HELD_LITERAL_ROWS_DRAFT) == 47, (
    f"expected 47 drafted rows, got {len(HELD_LITERAL_ROWS_DRAFT)} — "
    "recount against the 9 lists' --list output before trusting this file"
)
