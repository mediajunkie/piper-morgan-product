#!/usr/bin/env python3
"""Build the Inversion Phase-0 corpus (#1595) from its cited sources.

Phase 0 (proposal §Migration): "corpus grows from PM's live failures — every
transcript sentence becomes a judged case; baseline the current architecture's
corpus score honestly." Arch's conditions carried here:
  - per-CATEGORY gate → every row carries a category bucket (the denominator)
  - every row cites its SOURCE (probe row / issue / transcript / corpus-1283)
    — "a narrowing without its probe row is not narrowing, it is guessing"
  - "what reminders do I have?" MUST be present (Arch's one demand)

The builder is deterministic and re-runnable: structured sources are PARSED
(routing_corpus_1283.yaml; the surface-1 counterfactual results table), and
only genuinely unstructured sources (PM transcript verbatims already pinned in
tests, corpus-tagged issue phrasings) are inlined by hand WITH their citation.

Output: tests/fixtures/inversion_corpus_phase0.yaml
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS_1283 = ROOT / "tests" / "fixtures" / "routing_corpus_1283.yaml"
PROBE_RESULTS = (
    ROOT
    / "docs"
    / "internal"
    / "architecture"
    / "current"
    / "surface1-counterfactual-results-2026-08-08.md"
)
OUT = ROOT / "tests" / "fixtures" / "inversion_corpus_phase0.yaml"

# Category bucket per expected-destination, for rows whose category isn't
# already explicit. Buckets follow IntentCategory values (upper-cased).
_ACTION_CATEGORY = {
    "show_standup": "STATUS",
    "meeting_time": "TEMPORAL",
    "get_identity": "IDENTITY",
    "manage_portfolio": "PORTFOLIO",
    "get_default_repo": "QUERY",
    "set_default_repo": "EXECUTION",
    "close_issue_query": "EXECUTION",
    "reopen_issue_query": "EXECUTION",
    "comment_issue_query": "EXECUTION",
    "update_document_query": "EXECUTION",
    "create_issue": "EXECUTION",
    "create_reminder": "TEMPORAL",
    "list_archived_projects": "PORTFOLIO",
    "update_issue": "EXECUTION",
    "list_reminders_query": "TEMPORAL",
    "stale_prs_query": "QUERY",
    "pull_insights": "MEMORY",
    "get_capabilities": "DISCOVERY",
    "explain_suggestion": "PROVENANCE",
    "explain_trust": "TRUST",
    "get_memory": "MEMORY",
    "write_stakeholder_update": "SYNTHESIS",
    "summarize_document": "SYNTHESIS",  # #1624: uploaded-document summarize rail entry
    "greeting": "CONVERSATION",
    "farewell": "CONVERSATION",
    "thanks": "CONVERSATION",
}

# ---------------------------------------------------------------------------
# Hand-inlined rows: PM live-failure verbatims + corpus-tagged issues. Each
# cites the artifact that carries the verbatim (test file that pins it, issue
# number, or transcript reference). REVIEW = expected destination is the
# Inversion's question to answer, not an assertion.
# ---------------------------------------------------------------------------
HAND_ROWS = [
    # 2026-10-06 (Lead) — Arch's (a), 2026-10-05: complete_todo consumes router-extracted
    # TARGETS. These rows assert the target set (expected_args), not just the action.
    # Mini-grammar: "1" ordinal · "1-3" range · "last" · "all" · "name:<text>"; exclude =
    # the same shape for carve-outs. PM's own 10-05 phrasings first (they failed live).
    {
        "phrase": "Mark the first three complete and leave the fourth one pending.",
        "category": "EXECUTION",
        "expected": "action:complete_todo",
        "expected_args": {"targets": ["1-3"]},
        "source": "phase3-args/complete_todo PM live 2026-10-05 test C",
        "notes": (
            "2026-10-06 first score: router gave targets 1-3 and NO exclude for 'leave the "
            "fourth one pending'. exclude is only load-bearing when targets is 'all' (the "
            "handler enumerates 'Leaving D' from candidates minus targets), so this row asserts "
            "targets only; the 'all … except' rows keep asserting exclude."
        ),
    },
    {
        "phrase": "Mark the first one complete and leave the second one pending.",
        "category": "EXECUTION",
        "expected": "action:complete_todo",
        "expected_args": {"targets": ["1"], "exclude": ["2"]},
        "source": "phase3-args/complete_todo PM live 2026-10-01 (#1914)",
    },
    {
        "phrase": "I want you to clear 'check the test card again,' and 'review the pr' — mark them done",
        "category": "EXECUTION",
        "expected": "action:complete_todo",
        "expected_args": {"targets": ["name:check the test card again", "name:review the pr"]},
        "source": "phase3-args/complete_todo PM live 2026-10-05 clear-family answer",
    },
    {
        "phrase": "mark all my reminders done except for 'revise the pr'",
        "category": "EXECUTION",
        "expected": "action:complete_todo",
        "expected_args": {"targets": ["all"], "exclude": ["name:revise the pr"]},
        "source": "phase3-args/complete_todo exception clause (#1605 shape, explicit verb)",
    },
    {
        "phrase": "mark the first two complete",
        "category": "EXECUTION",
        "expected": "action:complete_todo",
        "expected_args": {"targets": ["1-2"]},
        "source": "phase3-args/complete_todo range",
    },
    {
        "phrase": "complete the last one",
        "category": "EXECUTION",
        "expected": "action:complete_todo",
        "expected_args": {"targets": ["last"]},
        "source": "phase3-args/complete_todo last",
    },
    {
        "phrase": "mark #2 as done",
        "category": "EXECUTION",
        "expected": "action:complete_todo",
        "expected_args": {"targets": ["2"]},
        "source": "phase3-args/complete_todo hash ordinal",
    },
    {
        "phrase": "mark todo 3 as complete",
        "category": "EXECUTION",
        "expected": "action:complete_todo",
        "expected_args": {"targets": ["3"]},
        "source": "phase3-args/complete_todo numbered (#904 shape)",
    },
    {
        "phrase": "mark 1, 2 and 4 done",
        "category": "EXECUTION",
        "expected": "action:complete_todo",
        "expected_args": {"targets": ["1", "2", "4"]},
        "source": "phase3-args/complete_todo list of ordinals (the router prompt's own example)",
    },
    {
        "phrase": "complete 'review the pr'",
        "category": "EXECUTION",
        "expected": "action:complete_todo",
        "expected_args": {"targets": ["name:review the pr"]},
        "source": "phase3-args/complete_todo quoted name",
    },
    {
        "phrase": "finish the second one",
        "category": "EXECUTION",
        "expected": "REVIEW",
        "source": "phase3-args/complete_todo finish verb",
        "notes": (
            "2026-10-06 first score: CLARIFY @0.3 — without the turn before it ('second one' of "
            "WHAT?) the router honestly asks; the corpus is context-free (Phase-0 convention: "
            "context-dependent rows are informational). REVIEW, not asserted."
        ),
    },
    {
        "phrase": "I'm done with the first and the third",
        "category": "EXECUTION",
        "expected": "action:complete_todo",
        "expected_args": {"targets": ["1", "3"]},
        "source": "phase3-args/complete_todo two ordinals",
    },
    {
        "phrase": "mark the PR review todo as done",
        "category": "EXECUTION",
        "expected": "action:complete_todo",
        "expected_args": {"targets": ["name:pr review"]},
        "source": "phase3-args/complete_todo unquoted name (#904 fuzzy shape)",
    },
    {
        "phrase": "mark everything done except the last one",
        "category": "EXECUTION",
        "expected": "action:complete_todo",
        "expected_args": {"targets": ["all"], "exclude": ["last"]},
        "source": "phase3-args/complete_todo all-but-last",
    },
    # 2026-10-04 (Lead): PORTFOLIO_PATTERNS' update/edit-project literals have NO handler
    # branch (manage_portfolio inventory row 12: they land in the fallback). Arch ruled
    # 2026-10-04: dead claims, rows expect floor (an honest "I can't edit projects yet").
    {
        "phrase": "update my project name to Atlas",
        "category": "PORTFOLIO",
        "expected": "floor",
        "source": 'phase3-conversion/PORTFOLIO_PATTERNS literal r"\\bupdate\\s+(?:my\\s+)?(?:the\\s+)?project\\b"',
        "notes": "Arch 2026-10-04 ruling: no update-project handler exists; dead claim, floor is the honest destination",
    },
    {
        "phrase": "edit my project description",
        "category": "PORTFOLIO",
        "expected": "floor",
        "source": 'phase3-conversion/PORTFOLIO_PATTERNS literal r"\\bedit\\s+(?:my\\s+)?(?:the\\s+)?project\\b"',
        "notes": "Arch 2026-10-04 ruling: no edit-project handler exists; dead claim, floor is the honest destination",
    },
    # — Live-drift deposits, 2026-09-23 (supersession gate: failing phrasings
    #   become corpus rows, never local patches) —
    {
        "phrase": "show me all project plans",
        "category": "QUERY",
        "expected": "action:search_documents",
        "source": "#1841 (Arch ruled 2026-09-22: search_documents; manage_portfolio is the drift)",
        "notes": (
            "document-genre search — 'plans' names a document type in the same slot as "
            "'design docs'/'technical specifications'; gpt-4o pattern-matches the surface "
            "token 'project' toward manage_portfolio (whose canonical is 'List my projects', "
            "CRUD on tracked Project entities). Pinned live-failing in "
            "tests/intent/test_coverage_pm039.py until the slot-emission lane learns it."
        ),
    },
    {
        "phrase": "do a standup",
        "category": "STATUS",
        "expected": "action:show_standup",
        "source": "#1860 (PM live 2026-09-23: fell to the honest no-result fallback)",
        "notes": (
            "initiation VERB family — bare \\bstandup\\b was deliberately removed from the "
            "pre-classifier (temporal false-positive: 'what time is standup'), leaving "
            "do/run/start/let's-do phrasings to the LLM leg, which did not dispatch live. "
            "Destination is the report-or-offer entry the working phrasing "
            "('show my standup for today') reaches; the offer seam arms the interview."
        ),
    },
    {
        "phrase": "let's do a standup",
        "category": "STATUS",
        "expected": "action:show_standup",
        "source": "#1860 (PM live 2026-09-23: got a conversational floor reply instead)",
        "notes": "same initiation-verb family as 'do a standup'; see that row",
    },
    # — Exhibit A (PM T6 transcript 2026-08-08, log line 26; pinned in tests) —
    {
        "phrase": "Yes please",
        "category": "CONVERSATION",
        "expected": "REVIEW",
        "source": "exhibit-a/1529 (test_offer_binding_1529.py PM_YES_PLEASE)",
        "notes": "must bind to the pending contextual offer, never claimed by a suspended flow",
    },
    {
        "phrase": "end standup",
        "category": "CONVERSATION",
        "expected": "REVIEW",
        "source": "exhibit-a/1529 (test_offer_binding_1529.py PM_END_STANDUP)",
        "notes": "flow-exit against a suspended standup; historically misrouted to todo-complete",
    },
    {
        "phrase": "i am not doing the standup right now. restore CoVa",
        "category": "PORTFOLIO",
        "expected": "REVIEW",
        "source": "exhibit-a/1529 (test_flow_escape_1529.py PM_REFUSAL_WITH_COMMAND)",
        "notes": "refusal closes the flow; residual 'restore CoVa' proceeds as normal intent",
    },
    {
        "phrase": "restore CoVa",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "source": "exhibit-a/1529 (PM live 2026-08-08 13:22, v38 — bare restore command, issued TWICE during the standup hijack per the issue body's 'NINE attempts to execute one restore', both swallowed)",
        "notes": (
            "#1595 completeness audit deposit (2026-09-25): the issue's embedded-refusal "
            "sibling row above pins the compound 'i am not doing... restore CoVa' shape; "
            "this bare form was a separately-swallowed attempt in the same hijack sequence "
            "and had no row of its own"
        ),
    },
    {
        "phrase": "Please list my archived projects",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "source": (
            "exhibit-a/1529 (PM live 2026-08-08 13:22, v38 — issued during the standup "
            "hijack and composed into standup content instead of reaching the archived-list "
            "lane; cf. issue-1579's unprefixed 'list my archived projects' sibling row below "
            "for the non-hijack destination)"
        ),
        "notes": "#1595 completeness audit deposit (2026-09-25): the 'Please'-prefixed exact verbatim had no row",
    },
    {
        "phrase": "what projects do I have?",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "source": "exhibit-a/1530 (chat omitted active CoVa; wrong source + wrong denominator)",
    },
    {
        "phrase": "what are my projects?",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "source": (
            "exhibit-a/1530 (PM live 2026-08-08 13:19, v38 — the LITERAL Exhibit-A "
            "verbatim: chat answered 'two projects: Klatch and One Job', omitting active "
            "CoVa and volunteering a wrong denominator; closed 2026-08-09 PM live-verified)"
        ),
        "notes": (
            "#1595 completeness audit deposit (2026-09-25): the sibling row above "
            "('what projects do I have?') is a PARAPHRASE the builder mislabeled as this "
            "issue's exhibit — it is not PM's exact words. This row is the actual verbatim"
        ),
    },
    # — corpus-tagged issues (the moratorium's deposit box) —
    {
        "phrase": "remind me at 3pm tomorrow to review the PR",
        "category": "TEMPORAL",
        "expected": "action:create_reminder",
        "source": (
            "issue-1559 (turn-1 PM verbatim, #1517 T4 2026-08-08; pinned in "
            "test_reminder_time_binding_1490.py)"
        ),
        "notes": (
            "adjacency-gap twin of the 9:41 row — misses REMINDER_PATTERNS at "
            "surface 1 (re-verified 2026-09-12: pre_classify -> None); turn 1 "
            "executed live only because the LLM happened to emit create_reminder. "
            "Both PM verbatims are the issue's stated Inversion acceptance cases"
        ),
    },
    {
        "phrase": "remind me at 9:41 today to check in with the lead developer",
        "category": "TEMPORAL",
        "expected": "action:create_reminder",
        "source": "issue-1559 (adjacency gap: 'remind me at <time> <day> to X' misses the reminder pattern)",
    },
    {
        "phrase": "Remind me tomorrow at 3pm to review the PR",
        "category": "TEMPORAL",
        "expected": "action:create_reminder",
        "source": (
            "issue-1490 (PM 8/7 original verbatim: date-then-time-then-task ordering — "
            "'I didn't catch what you'd like to be reminded about'; the WHAT slot was lost "
            "when time preceded task. Distinct from the T4 time-first inversion "
            "'remind me at 3pm tomorrow...' already pinned above under issue-1559's row; "
            "closed 2026-08-09 PM live-verified)"
        ),
        "notes": (
            "#1595 completeness audit deposit (2026-09-25): the issue's own original "
            "exemplar phrase had no row — only its later T4 inverted-order retry did"
        ),
    },
    {
        "phrase": "show me my archived projects",
        "category": "PORTFOLIO",
        "expected": "action:list_archived_projects",
        "source": "issue-1579 (PORTFOLIO list pattern rejects the 'me' token; claimed by STATUS @1.0)",
    },
    {
        "phrase": "list my archived projects",
        "category": "PORTFOLIO",
        "expected": "action:list_archived_projects",
        "source": "issue-1579 (the working sibling phrasing — the 'me' token is the discriminator)",
    },
    {
        "phrase": "list my archive projects",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "source": (
            "issue-1579 comment 2026-09-09 (PM live v70: 'archive' for 'archived' -> "
            "I couldn't find a project called 'projects')"
        ),
        "notes": (
            "routing is CORRECT for this drift form (re-verified 2026-09-12: "
            "pre_classify -> portfolio/manage_portfolio @1.0) — the failure is the "
            "name-slot extractor taking the literal word 'projects' as a project "
            "name. Deposited as a routing regression pin with the extraction gap "
            "on record; one character of drift must not turn a list into a lookup"
        ),
    },
    {
        "phrase": "Archive my project Test.",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "source": "issue-1492 (trailing punctuation breaks extraction)",
    },
    {
        "phrase": 'Archive my project "Test"',
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "source": "issue-1492 (quoted name breaks extraction)",
    },
    {
        "phrase": "Archive the project called Test",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "source": "issue-1492 ('called X' phrasing breaks extraction)",
    },
    {
        "phrase": "Archive my Test project, please.",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "source": (
            "issue-1492 (PM 8/7 EXACT verbatim: adjective-position 'my Test project' plus "
            "trailing comma/politeness — extraction produced 'test project, please.'; "
            "closed 2026-09-09 PM live-verified as the Test1 instance)"
        ),
        "notes": (
            "#1595 completeness audit deposit (2026-09-25): the sibling row above "
            "('Archive my project Test.') is a DIFFERENT word order (noun-then-adjective, "
            "no politeness tail) — it does not cover the adjective-position bug this exact "
            "phrase named"
        ),
    },
    {
        "phrase": 'Archive my project called "Test" please',
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "source": (
            "issue-1492 (PM 8/7 EXACT verbatim: quoted 'called \"X\"' form — extraction "
            "produced 'called \"test\"'; closed 2026-09-09 PM live-verified as the Test2 "
            "instance)"
        ),
        "notes": (
            "#1595 completeness audit deposit (2026-09-25): the sibling row above "
            "('Archive the project called Test') drops the quote marks and the trailing "
            "'please' — it is a paraphrase, not this exact PM verbatim"
        ),
    },
    {
        "phrase": "archive CoVa",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "source": (
            "issue-1492 comment (PM live T6, 2026-08-08 13:19, v38 — Exhibit-A window: "
            "case-sensitivity bug — lowercase 'archive CoVa' NOT FOUND while 'Archive CoVa' "
            "(capital A) succeeded on the identical remaining words; closed 2026-09-09 "
            "PM live-verified)"
        ),
        "notes": "#1595 completeness audit deposit (2026-09-25): no prior row exercised the case-sensitivity failure mode",
    },
    {
        "phrase": "delete my reminders",
        "category": "TEMPORAL",
        "expected": "REVIEW",
        "source": "issue-1527 (greedy portfolio delete pattern claims non-portfolio deletes)",
        "notes": "verb decision (clear=complete/delete/dismiss) is #1605/#1569's product question",
    },
    {
        "phrase": "delete my hydrate reminder",
        "category": "TEMPORAL",
        "expected": "action:delete_todo",
        "source": (
            "issue-1527 (v70 live 2026-09-08: LLM emitted execution/delete_reminder — "
            "verb=delete source_type=reminder — which no registry surface recognized; "
            "fell to the generic unwired-write decline, a false capability denial)"
        ),
        "notes": "pinned: test_reminder_delete_live_emission_1527.py (real classifier path)",
    },
    {
        "phrase": "remind me",
        "category": "TEMPORAL",
        "expected": "action:create_reminder",
        "source": (
            "issue-1654 (v70 live 2026-09-08: bare 'remind me' drew unknown/"
            "clarification_needed -> floor composed a merged what-and-when question "
            "with NO carrier armed; the bare answer 'make coffee' orphaned into the "
            "routing chain as a literal request)"
        ),
        "notes": (
            "incomplete but lane-known: create_reminder's handler owns the clarify "
            "(no-task ask arms the 1654 task carrier; answer binds at the offer seam)"
        ),
    },
    {
        "phrase": "hi piper, connect my github",
        "category": "EXECUTION",
        "expected": "REVIEW",
        "source": "issue-1505 (multi-intent path drops the connect ask; resolves to greeting only)",
    },
    {
        "phrase": "what time is it? also connect my github",
        "category": "TEMPORAL",
        "expected": "REVIEW",
        "source": (
            "issue-1755 (found during the 1505 fix, 2026-09-12 repro probe: the "
            "multi-intent TEMPORAL-skip was group-level, not span-aware, so a "
            "connect claim anywhere in the message suppressed the WHOLE temporal "
            "group, dropping a genuinely disjoint second ask — resolved to "
            "guidance/get_contextual_guidance only)"
        ),
        "notes": (
            "REVIEW, not a single scored action, because the row is genuinely "
            "MULTI-INTENT (guidance/get_contextual_guidance + temporal/"
            "get_current_time) — the Phase-0 schema asserts one action per row, "
            "same shape as the 'hi piper, connect my github' sibling row above. "
            "Fixed in the deterministic pre-classifier by "
            "PreClassifier._temporal_disjoint_from_connect (span-overlap check, "
            "not group suppression); deposited so the Inversion router's own "
            "answer is on record for this shape too — "
            "test_multi_intent_temporal_span_1755.py pins the pre-classifier fix."
        ),
    },
    {
        "phrase": 'please clear the reminders except for "Review the PR" - also, are you able to set my default repo for me conversationally?',
        "category": "TEMPORAL",
        "expected": "REVIEW",
        "source": "issue-1606 (PM live 2026-08-12: request 1 dropped; request 2 — a question — parsed as a malformed set-command)",
    },
    {
        "phrase": "are you able to set my default repo for me conversationally?",
        "category": "DISCOVERY",
        "expected": "REVIEW",
        "source": "issue-1606 (interrogative parsed as imperative-with-garbage-args)",
    },
    # — issue-1606 comment thread: the deposit box's own deposits (08-13/15/18
    #   comments filed these verbatims "per the deposit discipline"; none had
    #   reached the corpus — deposited 2026-09-12). Elided fragments in the
    #   08-13 comment ('…the status field of Issue #108…', '…the state field…',
    #   the typo'd 'emind' retry) are NOT deposited: no full verbatim, nothing
    #   invented. Grammar templates ('remind me: X') likewise stay out — the
    #   corpus is live verbatims only.
    {
        "phrase": "use the interview from now on",
        "category": "STATUS",
        "expected": "REVIEW",
        "source": "issue-1606 comment 2026-08-13 (PM 3:27-3:32 session; floor false-denial, #1591 verdict)",
        "notes": (
            "#1591 built the standup-mode declaration store AFTER this failure, but "
            "deliberately excludes this tokenless form (pinned: "
            "test_standup_mode_declaration_1591.py — no standup token, not a "
            "declaration; surface 1 None re-verified 2026-09-12). What the turn "
            "SHOULD do without conversational context is the open question"
        ),
    },
    {
        "phrase": "use the standup interview format by default from now on",
        "category": "STATUS",
        "expected": "REVIEW",
        "source": "issue-1606 comment 2026-08-13 (floor improvised an unstored promise)",
        "notes": (
            "since HANDLED by #1591: detect_standup_mode_declaration stores the "
            "interview default and confirms (pinned: "
            "test_standup_mode_declaration_1591.py PM_DECLARATION). REVIEW because "
            "the handling seam is the standup declaration detector, not an "
            "action:/category: destination this schema can assert — regression "
            "coverage lives in the 1591 pins"
        ),
    },
    {
        "phrase": "change the status of issue #108 to Done",
        "category": "EXECUTION",
        "expected": "action:update_issue",
        "source": "issue-1606 comment 2026-08-13 (alternating-slot-loss family, #1411)",
        "notes": (
            "destination is the #1411 update lane (surface 1 None re-verified "
            "2026-09-12 — LLM-layer routing); the recorded failures are slot loss, "
            "not lane choice. Bare '#108' repo resolution is the B3/default-repo "
            "question downstream of routing"
        ),
    },
    {
        "phrase": "please mark issue #108 in the mediajunkie/test-piper-morgan repo complete",
        "category": "EXECUTION",
        "expected": "REVIEW",
        "source": "issue-1606 comment 2026-08-13 (cross-domain claim by the todo handler)",
        "notes": (
            "still claimed today: pre_classify -> execution/complete_todo @1.0 "
            "(re-verified 2026-09-12) — a GitHub issue captured by the todo domain. "
            "GH lane either way; REVIEW because close_issue_query vs update_issue "
            "is undecided"
        ),
    },
    {
        "phrase": "add a reminder: test the safe clarification",
        "category": "TEMPORAL",
        "expected": "action:create_reminder",
        "source": (
            "issue-1606 comment 2026-08-15 (v53 retest: colon-form not extracted — "
            "'I didn't catch what you'd like to be reminded about'; the taught "
            "rephrase worked)"
        ),
        "notes": (
            "surface 1 None (re-verified 2026-09-12): 'add a reminder' matches no "
            "REMINDER_PATTERNS form; per the 08-18 comment the colon-form is the "
            "highest-frequency reminder phrasing miss"
        ),
    },
    {
        "phrase": 'please remind me: ask Lead how to test "outwardness disclosure" today',
        "category": "TEMPORAL",
        "expected": "action:create_reminder",
        "source": "issue-1606 comment 2026-08-18 (corpus +2: colon-form unparsed, twice in one session)",
    },
    {
        "phrase": "please mark 1, 2, 4, and 5 done",
        "category": "EXECUTION",
        "expected": "REVIEW",
        "source": "PM live 2026-08-12 (#1603 session; multi-ordinal completion has no handler shape)",
    },
    {
        "phrase": "Create a doc from this conversation",
        "category": "SYNTHESIS",
        "expected": "REVIEW",
        "source": "issue-1674 (canonical Q36 mode-4 drift, Run 14 2026-08-21: rail key create_content reachable by NO deterministic surface)",
        "notes": "History: floored at Run 11 (then-expected floor); routed action Run 15 + 08-01 baseline -> 1395-rev flipped expectation to action on those 2 observations; Run 14 floors again (synthesis) — an oscillator like Q22, no intervening routing-code change explains the flip-back. No surface ever claimed it: pre-classifier None, no prompt example teaches create_content, no verb-shim CREATE cell, no rail aliases, normalize_action has no create_ prefix. Inversion router 2026-08-22: route NONE @0.85 (no catalog op handles it) — defensible, since _handle_generate_content requires content_type in {status_report, readme_section, issue_template} and the asked capability (conversation->document export) exists nowhere; the historic action-routing was name-similarity and ended in a content_type clarification. REVIEW = is NONE/clarify the right destination, or should a real conversation-export op exist?",
    },
    # — #1595 completeness audit deposit, 2026-09-25: the Exhibit-A catalog's
    #   8th entry (#1488-class) had NO corpus row at all. PM's literal beta-
    #   account phrase is redacted in the issue ("'create a todo: …' (bare AND
    #   'Please '-prefixed, greeting-primed)") — genuinely unrecoverable as an
    #   exact quote. #1677's investigation (2026-08-22) found the real
    #   mechanism with a MEASURED, non-fabricated phrase: real classifier,
    #   cache off, 3 samples — "add todo buy oat milk" drew create_ticket 2/3,
    #   the worst draw in the table. Using that measured phrase rather than
    #   inventing PM's redacted one.
    {
        "phrase": "add todo buy oat milk",
        "category": "EXECUTION",
        "expected": "action:create_todo",
        "source": (
            "issue-1488 (beta account misroute to GitHub-connect decline, 8/2 + 8/7 v30, "
            "class of the bare/greeting-primed 'create a todo: …' family whose exact PM "
            "wording is redacted in the issue) + issue-1677 (2026-08-22 real-classifier "
            "measurement, cache off, 3 samples/variant: this colonless phrasing drew "
            "create_ticket 2/3 — the worst draw of the probed table; pinned verbatim in "
            "test_inversion_write_allowlist_1677.py:101)"
        ),
        "notes": (
            "closed with #1677 on PM's live evidence 2026-08-29: create_todo now routes "
            "via the Inversion's allowlisted-write flip, 5/5 clean under the watched flip, "
            "zero create_ticket draws"
        ),
    },
    # phase3-conversion — #1595 epic-0 unit 5 Phase-3 deletion-gate deposits,
    # 2026-09-27. `scripts/inversion_phase3_deletion_gate.py --list <NAME>`
    # reported these regex literals as unexercised by any corpus row (the
    # gate's own pattern->corpus conversion check, `_first_pattern_match`
    # called read-only on the already-known claiming list — no new matching
    # logic). Each phrase below was verified against the REAL production
    # matcher before being deposited: `PreClassifier.pre_classify_with_pattern_list`
    # returns the named list (not a different one — no phrase here is
    # shadowed by an earlier-checked list), AND `PreClassifier._first_pattern_match`
    # against that list's own literals returns exactly the cited literal (not
    # an earlier sibling literal in the same list stealing the claim first).
    # `expected` names the REGISTRY CANONICAL action (list_completed_todos and
    # next_todo_query are aliases of list_todos_query per
    # `inversion_phase1_shadow_score.py --dry-run`'s grammar table — same
    # canonical `same_operation` would already resolve them to, stated
    # explicitly here per the deposit convention).
    #
    # — REMINDER_PATTERNS (4 literals; the 5th, `\bremind\s+me\s+(?:to|about)\b`,
    #   was already exercised by the existing "remind me to review the
    #   roadmap tomorrow" row) —
    {
        "phrase": "set a reminder for the dentist appointment",
        "category": "TEMPORAL",
        "expected": "action:create_reminder",
        "source": 'phase3-conversion/REMINDER_PATTERNS literal r"\\bset\\s+(?:a\\s+)?reminder\\b"',
    },
    {
        "phrase": "create a reminder to call the plumber",
        "category": "TEMPORAL",
        "expected": "action:create_reminder",
        "source": 'phase3-conversion/REMINDER_PATTERNS literal r"\\bcreate\\s+(?:a\\s+)?reminder\\b"',
    },
    {
        "phrase": "don't let me forget to submit the report",
        "category": "TEMPORAL",
        "expected": "action:create_reminder",
        "source": 'phase3-conversion/REMINDER_PATTERNS literal r"\\bdon\'?t\\s+let\\s+me\\s+forget\\b"',
    },
    {
        "phrase": "I need to remember to submit my timesheet",
        "category": "TEMPORAL",
        "expected": "action:create_reminder",
        "source": 'phase3-conversion/REMINDER_PATTERNS literal r"\\bneed\\s+to\\s+remember\\s+to\\b"',
    },
    # — REMINDER_QUERY_PATTERNS (3 literals; the 4th, `\bwhat reminders\b`, was
    #   already exercised by the existing "what reminders do I have?" row) —
    {
        "phrase": "what are my reminders",
        "category": "TEMPORAL",
        "expected": "action:list_reminders_query",
        "source": 'phase3-conversion/REMINDER_QUERY_PATTERNS literal r"\\bmy reminders\\b"',
    },
    {
        "phrase": "show reminders",
        "category": "TEMPORAL",
        "expected": "action:list_reminders_query",
        "source": (
            "phase3-conversion/REMINDER_QUERY_PATTERNS literal "
            'r"\\b(?:show|list|view|see|check)\\s+(?:me\\s+)?(?:all\\s+)?(?:my\\s+)?reminders\\b"'
        ),
    },
    {
        "phrase": "do I have any reminders",
        "category": "TEMPORAL",
        "expected": "action:list_reminders_query",
        "source": 'phase3-conversion/REMINDER_QUERY_PATTERNS literal r"\\bdo i have (?:any\\s+)?reminders\\b"',
    },
    # — TODO_QUERY_PATTERNS (8 literals; the 2 not deposited here,
    #   `\bshow.*completed\s+todos\b`'s and `\bshow\s+all\s+(?:my\s+)?todos\b`'s
    #   near neighbor `\bmy todos\b`, and `\bwhat'?s my next todo\b`, were
    #   already exercised by the existing "show me my todos" / "show all my
    #   todos" / "what's my next todo?" rows) —
    {
        "phrase": "show todos",
        "category": "QUERY",
        "expected": "action:list_todos_query",
        "source": 'phase3-conversion/TODO_QUERY_PATTERNS literal r"\\bshow\\s+(?:my\\s+)?todos\\b"',
    },
    {
        "phrase": "list my todos",
        "category": "QUERY",
        "expected": "action:list_todos_query",
        "source": 'phase3-conversion/TODO_QUERY_PATTERNS literal r"\\blist\\s+(?:my\\s+)?todos\\b"',
    },
    {
        "phrase": "what are my todos",
        "category": "QUERY",
        "expected": "action:list_todos_query",
        "source": 'phase3-conversion/TODO_QUERY_PATTERNS literal r"\\bwhat are my todos\\b"',
    },
    {
        "phrase": "show me completed todos",
        "category": "QUERY",
        "expected": "action:list_todos_query",
        "source": 'phase3-conversion/TODO_QUERY_PATTERNS literal r"\\bshow.*completed\\s+todos\\b"',
        "notes": "surface-1 claims list_completed_todos (alias of canonical list_todos_query)",
    },
    {
        "phrase": "show all todos",
        "category": "QUERY",
        "expected": "action:list_todos_query",
        "source": 'phase3-conversion/TODO_QUERY_PATTERNS literal r"\\bshow\\s+all\\s+(?:my\\s+)?todos\\b"',
        "notes": (
            "surface-1 claims list_completed_todos (alias of canonical list_todos_query); "
            "'my' deliberately omitted so `\\bmy todos\\b` (an earlier literal in the same "
            "list, already exercised) does not steal the claim first"
        ),
    },
    {
        "phrase": "next todo",
        "category": "QUERY",
        "expected": "action:list_todos_query",
        "source": 'phase3-conversion/TODO_QUERY_PATTERNS literal r"\\bnext todo\\b"',
        "notes": "surface-1 claims next_todo_query (alias of canonical list_todos_query)",
    },
    {
        "phrase": "what should I do next",
        "category": "QUERY",
        # RULED 2026-09-27 (CXO, PPM concurring): this asks Piper to DECIDE, not
        # to enumerate — get_top_priority ("What should I work on first?" in the
        # registry), never list_todos_query. Surface 1's next_todo_query claim
        # was the pattern's reading, not the product's. First scored MISMATCH
        # against the old expectation (deposits report 09-27); re-scored under
        # this one in inversion-phase3-todo-query-rescore-2026-09-27.md.
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/TODO_QUERY_PATTERNS literal r"\\bwhat should i do next\\b"',
        "notes": "surface-1 claims next_todo_query; product destination ruled get_top_priority (CXO/PPM 09-27)",
    },
    {
        "phrase": "what do I have next to do",
        "category": "QUERY",
        "expected": "action:get_top_priority",  # RE-EXPECTED 2026-10-01: Haiku (served model) routes get_top_priority — the decide-for-me "next" shape CXO ruled 09-27; flagged to CXO
        "source": 'phase3-conversion/TODO_QUERY_PATTERNS literal r"\\bwhat.*next.*do\\b"',
        "notes": (
            "surface-1 claims next_todo_query (alias of canonical list_todos_query); phrased "
            "so 'next' precedes 'do' in the text (the literal's own left-to-right order — "
            "'what do I do next' does NOT match this literal and falls through to "
            "PRIORITY_PATTERNS instead, an unreachable-at-surface-1 finding for that word "
            "order, not a deposit)"
        ),
    },
    # — GUIDANCE_PATTERNS (20 of 21 literals; `\bget started\b` was already
    #   exercised by the existing "how do I get started?" row, category
    #   GUIDANCE per that row's convention — matched here, not the QUERY
    #   category used by the separate INTEGRATION_CONNECT_PATTERNS-claimed
    #   rows that also expect get_contextual_guidance). `expected` is the
    #   REGISTRY CANONICAL action: get_contextual_guidance is itself
    #   canonical (ACTION_REGISTRY ActionDisposition.CANONICAL for
    #   ("GUIDANCE", "get_contextual_guidance")), not an alias — no
    #   per-row alias note needed. All 20 phrases verified against the REAL
    #   production matcher: `PreClassifier.pre_classify_with_pattern_list`
    #   returns GUIDANCE_PATTERNS (no earlier-checked sibling list steals the
    #   claim — GUIDANCE is checked well before ANALYSIS/STATUS/etc. in
    #   pre_classify order) AND `PreClassifier._first_pattern_match` against
    #   GUIDANCE_PATTERNS's own literals returns exactly the cited literal
    #   (not an earlier sibling literal in the same list stealing the claim
    #   first — one phrase needed rewording for this, noted below).
    {
        "phrase": "where should I focus this week",
        "category": "GUIDANCE",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/GUIDANCE_PATTERNS literal r"\\bwhere should i focus\\b"',
        "notes": "surface-1 claims GUIDANCE; RULED get_top_priority (CXO 09-28: decide-for-me shape, as 'what next')",
    },
    {
        "phrase": "I could use some guidance on this",
        "category": "GUIDANCE",
        "expected": "action:get_contextual_guidance",
        "source": 'phase3-conversion/GUIDANCE_PATTERNS literal r"\\bguidance\\b"',
    },
    {
        "phrase": "do you have a recommendation",
        "category": "GUIDANCE",
        "expected": "action:get_contextual_guidance",
        "source": 'phase3-conversion/GUIDANCE_PATTERNS literal r"\\brecommendation\\b"',
    },
    {
        "phrase": "what's your advice here",
        "category": "GUIDANCE",
        "expected": "action:get_contextual_guidance",
        "source": 'phase3-conversion/GUIDANCE_PATTERNS literal r"\\badvice\\b"',
    },
    {
        "phrase": "ok that's merged, what now?",
        "category": "GUIDANCE",
        "expected": "action:get_contextual_guidance",
        "source": 'phase3-conversion/GUIDANCE_PATTERNS literal r"\\bwhat now\\b"',
    },
    {
        "phrase": "what are the next steps",
        "category": "GUIDANCE",
        "expected": "action:get_contextual_guidance",
        "source": 'phase3-conversion/GUIDANCE_PATTERNS literal r"\\bnext steps\\b"',
    },
    {
        "phrase": "what should I do about this bug",
        "category": "GUIDANCE",
        "expected": "action:get_contextual_guidance",
        "source": (
            'phase3-conversion/GUIDANCE_PATTERNS literal r"\\bwhat should (i|we) do '
            '(about|with)\\b"'
        ),
    },
    {
        "phrase": "advise me on this decision",
        "category": "GUIDANCE",
        "expected": "action:get_contextual_guidance",
        "source": 'phase3-conversion/GUIDANCE_PATTERNS literal r"\\badvise (me|us) on\\b"',
    },
    {
        "phrase": "what's the process for filing a bug",
        "category": "GUIDANCE",
        "expected": "action:get_contextual_guidance",
        "source": (
            "phase3-conversion/GUIDANCE_PATTERNS literal " 'r"\\bwhat(\'?s| is) the process for\\b"'
        ),
    },
    {
        "phrase": "can you help me setup the integration",
        "category": "GUIDANCE",
        "expected": "action:get_contextual_guidance",
        "source": 'phase3-conversion/GUIDANCE_PATTERNS literal r"\\bhelp.*setup\\b"',
    },
    {
        "phrase": "can you help me configure the connector",
        "category": "GUIDANCE",
        "expected": "action:get_contextual_guidance",
        "source": 'phase3-conversion/GUIDANCE_PATTERNS literal r"\\bhelp.*configure\\b"',
    },
    {
        "phrase": "I need to setup my projects",
        "category": "GUIDANCE",
        "expected": "action:get_contextual_guidance",
        "source": 'phase3-conversion/GUIDANCE_PATTERNS literal r"\\bsetup.*projects?\\b"',
    },
    {
        "phrase": "how do I configure my projects",
        "category": "GUIDANCE",
        "expected": "action:get_contextual_guidance",
        "source": 'phase3-conversion/GUIDANCE_PATTERNS literal r"\\bconfigure.*projects?\\b"',
    },
    {
        "phrase": "how do I setup the connector",
        "category": "GUIDANCE",
        "expected": "action:get_contextual_guidance",
        "source": 'phase3-conversion/GUIDANCE_PATTERNS literal r"\\bhow do i.*setup\\b"',
    },
    {
        "phrase": "how do I configure the connector",
        "category": "GUIDANCE",
        "expected": "action:get_contextual_guidance",
        "source": 'phase3-conversion/GUIDANCE_PATTERNS literal r"\\bhow do i.*configure\\b"',
    },
    {
        "phrase": "just getting started here",
        "category": "GUIDANCE",
        "expected": "action:greeting",
        "source": 'phase3-conversion/GUIDANCE_PATTERNS literal r"\\bgetting started\\b"',
        "notes": "surface-1 claims GUIDANCE; RULED greeting is a reasonable landing (CXO 09-28)",
    },
    {
        "phrase": "can you help me set up the integration",
        "category": "GUIDANCE",
        "expected": "action:get_contextual_guidance",
        "source": 'phase3-conversion/GUIDANCE_PATTERNS literal r"\\bhelp.*set up\\b"',
    },
    {
        "phrase": "I want to set up my projects",
        "category": "GUIDANCE",
        "expected": "action:get_contextual_guidance",
        "source": 'phase3-conversion/GUIDANCE_PATTERNS literal r"\\bset up.*projects?\\b"',
    },
    {
        "phrase": "how do I set up the connector",
        "category": "GUIDANCE",
        "expected": "action:get_contextual_guidance",
        "source": 'phase3-conversion/GUIDANCE_PATTERNS literal r"\\bhow do i.*set up\\b"',
    },
    {
        "phrase": "I'd like to set up my portfolio",
        "category": "GUIDANCE",
        "expected": "action:get_contextual_guidance",
        "source": 'phase3-conversion/GUIDANCE_PATTERNS literal r"\\bset up.*portfolio\\b"',
        "notes": (
            "phrased without a leading 'how do I' so the earlier sibling literal "
            "r'\\bhow do i.*set up\\b' does not steal the claim first — 'how do I set up my "
            "portfolio' hits that literal instead, verified empirically before rewording"
        ),
    },
    # — PRIORITY_PATTERNS (38 of 43 unexercised literals; 4 of 47 were already
    #   exercised before this deposit — "my priorities" / "top priorities" /
    #   "what should i focus on" / "what should i do next", the last one
    #   reclaimed from TODO_QUERY_PATTERNS's second deletion — so this block
    #   covers the remaining 43 minus 5 structurally unreachable literals,
    #   named below). `expected` is `action:get_top_priority` throughout —
    #   PRIORITY_PATTERNS has exactly one destination in both
    #   `pre_classify`/`pre_classify_with_pattern_list` (single-intent) and the
    #   multi-intent pattern-group table, `("PRIORITY", "get_top_priority")`,
    #   confirmed `ActionDisposition.FLOOR` in `action_registry.py` (routes to
    #   the conversational floor, no WORKFLOW rail entry — same disposition as
    #   STATUS/get_project_status) and not an alias of any other canonical
    #   action; this exact action:get_top_priority expectation already scored
    #   MATCH once, in the TODO_QUERY_PATTERNS re-expected "what should I do
    #   next" row (CXO/PPM ruling, 2026-09-27). All 38 phrases verified
    #   against the REAL production matcher: `PreClassifier.
    #   pre_classify_with_pattern_list(phrase)` returns `"PRIORITY_PATTERNS"`
    #   (no earlier-checked list in `pre_classify`'s own if-chain —
    #   GREETING/FAREWELL/THANKS/DISCOVERY/PROVENANCE/TRUST/INSIGHT_PULL/
    #   MEMORY/…/GUIDANCE/ANALYSIS/STATUS all precede PRIORITY there — steals
    #   the claim) AND `PreClassifier._first_pattern_match` against
    #   PRIORITY_PATTERNS's own literals (in list order) returns exactly the
    #   cited literal, not an earlier sibling literal in the SAME list
    #   stealing the claim first (several needed rewording for this, noted
    #   per row below).
    #
    #   Five literals are UNREACHABLE at surface 1 and get no deposit here —
    #   every string satisfying the later literal necessarily also satisfies
    #   an earlier sibling literal in the same list (first-match-wins, so the
    #   earlier one always claims first; confirmed empirically with multiple
    #   phrasing attempts, not just inferred from the regex text):
    #     r"\bwhat are my priorities\b"      — always contains "my priorities",
    #       claimed first by r"\bmy priorities\b" (list position 0).
    #     r"\bmost important task\b"         — always contains "most important",
    #       claimed first by r"\bmost important\b" (earlier in the list).
    #     r"\bmost important work\b"         — same shadow as above.
    #     r"\bwhat'?s most important\b"      — same shadow as above.
    #     r"\bwhat.*work on next\b"          — always contains "work on next",
    #       which also satisfies the alternation in
    #       r"\bwhat.*(?:do|work on|tackle|handle)\s+next\b" (earlier in the
    #       list), so it is always claimed there first.
    {
        "phrase": "what's my top priority",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bwhat\'?s my top priority\\b"',
    },
    {
        "phrase": "this is top priority for the team",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\btop priority\\b"',
    },
    {
        "phrase": "this is the highest priority item",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bhighest priority\\b"',
    },
    {
        "phrase": "mark this as priority one",
        "category": "PRIORITY",
        "expected": "action:prioritize",  # RULED 2026-09-30/10-01 (CXO+PPM): was action:get_top_priority
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bpriority one\\b"',
    },
    {
        "phrase": "show priorities for this sprint",
        "category": "PRIORITY",
        "expected": "floor",  # RULED 2026-09-30/10-01 (CXO+PPM): was action:get_top_priority
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bshow.*priorities\\b"',
        "notes": (
            "phrased without 'my' so the earlier sibling literal r'\\bmy priorities\\b' "
            "does not steal the claim first — 'show me my priorities' hits that literal "
            "instead, verified empirically before rewording"
        ),
    },
    {
        "phrase": "list priorities for the team",
        "category": "PRIORITY",
        "expected": "floor",  # RULED 2026-09-30/10-01 (CXO+PPM): was action:get_top_priority
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\blist.*priorities\\b"',
        "notes": (
            "phrased without 'my' so the earlier sibling literal r'\\bmy priorities\\b' "
            "does not steal the claim first — 'list my priorities' hits that literal "
            "instead, verified empirically before rewording"
        ),
    },
    {
        "phrase": "what are my current priorities",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bcurrent priorities\\b"',
    },
    {
        "phrase": "what are the key priorities this quarter",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bkey priorities\\b"',
    },
    {
        "phrase": "what's most important right now",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bmost important\\b"',
    },
    {
        "phrase": "what matters most this week",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bwhat matters most\\b"',
    },
    {
        "phrase": "what are the key tasks for this sprint",
        "category": "PRIORITY",
        "expected": "floor",  # RULED 2026-09-30/10-01 (CXO+PPM): was action:get_top_priority
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bkey tasks\\b"',
    },
    {
        "phrase": "what are the key items on my plate",
        "category": "PRIORITY",
        "expected": "action:attention_query",  # RULED 2026-10-01 (CXO): was action:get_top_priority
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bkey items\\b"',
    },
    {
        "phrase": "should i focus on the bug first",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bshould i focus\\b"',
    },
    {
        "phrase": "what could I focus on",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bwhat.*focus on\\b"',
        "notes": (
            "phrased as 'what could I' rather than 'what should I' so the earlier "
            "sibling literal r'\\bwhat should i focus on\\b' does not steal the claim "
            "first — 'what should I focus on' hits that literal instead, verified "
            "empirically before rewording"
        ),
    },
    {
        "phrase": "where should my focus be today",
        "category": "PRIORITY",
        "expected": "action:attention_query",  # RULED 2026-10-01 (CXO): was action:get_top_priority
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bwhere.*focus\\b"',
    },
    {
        "phrase": "what are my focus areas this sprint",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bfocus areas\\b"',
    },
    {
        "phrase": "let's focus on today's priorities",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bfocus on today\\b"',
        "notes": (
            "phrased without a leading 'what should I' so the earlier sibling literal "
            "r'\\bwhat should i focus on\\b' does not steal the claim first — 'what "
            "should I focus on today' hits that literal instead, verified empirically "
            "before rewording"
        ),
    },
    {
        "phrase": "what's my focus this week",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bfocus this week\\b"',
    },
    {
        "phrase": "not sure what to focus next",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bwhat to focus\\b"',
        "notes": (
            "phrased without a trailing 'on' so the earlier sibling literal "
            "r'\\bwhat.*focus on\\b' does not steal the claim first — 'what to focus "
            "on next' hits that literal instead, verified empirically before rewording"
        ),
    },
    {
        "phrase": "what's urgent right now",
        "category": "PRIORITY",
        "expected": "action:attention_query",  # RULED 2026-09-30/10-01 (CXO+PPM): was action:get_top_priority
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bwhat\'?s urgent\\b"',
    },
    {
        "phrase": "what are my urgent tasks",
        "category": "PRIORITY",
        "expected": "action:attention_query",  # RULED 2026-09-30/10-01 (CXO+PPM): was action:get_top_priority
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\burgent tasks\\b"',
    },
    {
        "phrase": "what are my urgent items",
        "category": "PRIORITY",
        "expected": "action:attention_query",  # RULED 2026-09-30/10-01 (CXO+PPM): was action:get_top_priority
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\burgent items\\b"',
    },
    {
        "phrase": "what's my urgent work today",
        "category": "PRIORITY",
        "expected": "action:attention_query",  # RULED 2026-10-01 (CXO): was action:get_top_priority
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\burgent work\\b"',
    },
    {
        "phrase": "what's the most urgent thing",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bmost urgent\\b"',
    },
    {
        "phrase": "what needs my focus today",
        "category": "PRIORITY",
        "expected": "action:attention_query",  # RULED 2026-09-30/10-01 (CXO+PPM): was action:get_top_priority
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bneeds.*focus\\b"',
    },
    {
        "phrase": "what requires attention right now",
        "category": "PRIORITY",
        "expected": "action:attention_query",  # RULED 2026-09-30/10-01 (CXO+PPM): was action:get_top_priority
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\brequires attention\\b"',
    },
    {
        "phrase": "what's critical right now",
        "category": "PRIORITY",
        "expected": "action:attention_query",  # RULED 2026-10-01 (CXO): was action:get_top_priority
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bwhat\'?s critical\\b"',
    },
    {
        "phrase": "what are my critical tasks",
        "category": "PRIORITY",
        "expected": "action:attention_query",  # RULED 2026-10-01 (CXO): was action:get_top_priority
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bcritical tasks\\b"',
    },
    {
        "phrase": "what are my critical items",
        "category": "PRIORITY",
        "expected": "action:attention_query",  # RULED 2026-09-30/10-01 (CXO+PPM): was action:get_top_priority
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bcritical items\\b"',
    },
    {
        "phrase": "what's my critical work today",
        "category": "PRIORITY",
        "expected": "action:attention_query",  # RULED 2026-10-01 (CXO): was action:get_top_priority
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bcritical work\\b"',
    },
    {
        "phrase": "what's the most critical thing",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bmost critical\\b"',
    },
    {
        "phrase": "what should I do first",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bwhat should i do first\\b"',
    },
    {
        "phrase": "what should I tackle next",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": (
            "phase3-conversion/PRIORITY_PATTERNS literal "
            'r"\\bwhat.*(?:do|work on|tackle|handle)\\s+next\\b"'
        ),
    },
    {
        "phrase": "what's next for me",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bwhat(?:\'s| is) next\\b"',
    },
    {
        "phrase": "what should I review first",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bwhat.*first\\b"',
    },
    {
        "phrase": "which project should get my focus today",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bwhich project.*focus\\b"',
        "notes": (
            "phrased as 'should get my focus' rather than 'should I focus' so the "
            "earlier sibling literals r'\\bshould i focus\\b' and r'\\bneeds.*focus\\b' "
            "do not steal the claim first — 'which project should I focus on' hits "
            "r'\\bshould i focus\\b' instead, verified empirically before rewording"
        ),
    },
    {
        "phrase": "which task should get my focus next",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bwhich task.*focus\\b"',
        "notes": (
            "phrased as 'should get my focus' rather than 'should I focus' so the "
            "earlier sibling literal r'\\bshould i focus\\b' does not steal the claim "
            "first, same rewording as the 'which project' row above"
        ),
    },
    {
        "phrase": "not sure what to do about this",
        "category": "PRIORITY",
        "expected": "action:get_contextual_guidance",  # RULED 2026-09-30/10-01 (CXO+PPM): was action:get_top_priority
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bwhat to do\\b"',
    },
    # — CALENDAR_QUERY_PATTERNS (46 of 49 unexercised literals; 3 of 52 were
    #   already exercised before this deposit — "what's on my calendar
    #   today?", "show my recurring meetings", "what's my week look like?" —
    #   so this block covers the remaining 49 minus 3 structurally
    #   unreachable literals, named below). Unlike PRIORITY_PATTERNS,
    #   CALENDAR_QUERY_PATTERNS has THREE destinations
    #   (`meeting_time`/`recurring_meetings`/`week_calendar`), all
    #   `ActionDisposition.WORKFLOW` in `action_registry.py`, all dispatched
    #   via the `_CALENDAR_QUERY_COHORT` WORKFLOW rail entries in
    #   `workflow_entries.py` (read only — not modified by this unit), all in
    #   the SAME `_CALENDAR_QUERY_FLIP_GROUPS` flip group ("read_temporal") —
    #   so every row below is live-routable under the dispatch's `--live`
    #   set. `expected` is the specific `action:<name>` each row's exact
    #   PHRASE actually routes to — verified against the REAL production
    #   function, not inferred from the regex text: `PreClassifier.
    #   pre_classify_with_pattern_list(phrase)` returns `("CALENDAR_QUERY_
    #   PATTERNS", intent)` and `intent.action` is read directly (the
    #   `meeting_time`/`recurring_meetings`/`week_calendar` choice is made by
    #   a SEPARATE re-match of the message against two hardcoded sub-lists
    #   inside the branch, independent of which CALENDAR_QUERY_PATTERNS
    #   literal claimed first — several phrases below demonstrate this: e.g.
    #   "what's my agenda this week" is CLAIMED by the list literal
    #   r"\bagenda.*this week\b" but its action comes out meeting_time
    #   because the same string also contains "my agenda", which IS in the
    #   meeting_time sub-list; both facts are independently verified, not
    #   contradictory). `PreClassifier._first_pattern_match` against
    #   CALENDAR_QUERY_PATTERNS's own literals (in list order) confirms the
    #   cited literal claims first, not an earlier sibling in the SAME list
    #   (several needed rewording for this, noted per row below).
    #
    #   Three literals are UNREACHABLE at surface 1 and get no deposit here —
    #   every string satisfying the later literal necessarily also satisfies
    #   an earlier sibling literal in the same list (first-match-wins, so the
    #   earlier one always claims first; confirmed empirically with 2
    #   different phrasing attempts each, not just inferred from the regex
    #   text):
    #     r"\bon my agenda\b"                      — any match necessarily
    #       contains the word-bounded substring "my agenda" (the "on " is
    #       just a prefix), claimed first by r"\bmy agenda\b" (earlier in
    #       the list).
    #     r"\bwhat'?s on my calendar.*tomorrow\b"  — any match necessarily
    #       contains "what's on my calendar" (or "what is on my calendar")
    #       as a prefix, claimed first by r"\bwhat'?s on my calendar\b"
    #       (list position 0) / r"\bwhat is on my calendar\b".
    #     r"\bmy calendar tomorrow\b"               — any match necessarily
    #       contains "calendar" immediately followed (within .*) by
    #       "tomorrow", claimed first by r"\bcalendar.*tomorrow\b" (earlier
    #       in the list).
    {
        "phrase": "what is on my calendar",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bwhat is on my calendar\\b"',
    },
    {
        "phrase": "show me my calendar today",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bmy calendar today\\b"',
    },
    {
        "phrase": "calendar today please",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bcalendar today\\b"',
    },
    {
        "phrase": "what meetings today",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bmeetings today\\b"',
    },
    {
        "phrase": "do i have any meetings",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bdo i have any meetings\\b"',
    },
    {
        "phrase": "do i have meetings",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bdo i have meetings\\b"',
    },
    {
        "phrase": "what meetings do i have",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bwhat meetings do i have\\b"',
    },
    {
        "phrase": "what meetings are coming up",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bwhat meetings\\b"',
    },
    {
        "phrase": "what's my schedule today",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bmy schedule today\\b"',
    },
    {
        "phrase": "today's schedule please",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\btoday\'?s schedule\\b"',
    },
    {
        "phrase": "what's the schedule for today",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bschedule for today\\b"',
    },
    {
        "phrase": "what's my agenda today",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bagenda.*today\\b"',
    },
    {
        "phrase": "what's my agenda tomorrow",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bagenda.*tomorrow\\b"',
    },
    {
        "phrase": "what's my agenda this week",
        "category": "QUERY",
        "expected": "action:week_calendar",  # RULED 2026-09-30/10-01 (CXO+PPM): was action:meeting_time
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bagenda.*this week\\b"',
        "notes": (
            "claimed by r'\\bagenda.*this week\\b' (CALENDAR_QUERY_PATTERNS list order), "
            "but action=meeting_time because the SAME phrase also contains 'my agenda', "
            "which independently matches the meeting_time sub-list inside the action "
            "branch — the claiming match and the action-determining match are separate "
            "re-checks against the message, verified directly via intent.action, not "
            "inferred from which literal claims in CALENDAR_QUERY_PATTERNS"
        ),
    },
    {
        "phrase": "what's my agenda next week",
        "category": "QUERY",
        "expected": "action:week_calendar",  # RULED 2026-09-30/10-01 (CXO+PPM): was action:meeting_time
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bagenda.*next week\\b"',
        "notes": "same 'my agenda' collateral-match mechanism as the 'this week' row above",
    },
    {
        "phrase": "show me my agenda",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bmy agenda\\b"',
    },
    {
        "phrase": "show me calendar for tomorrow",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bcalendar.*tomorrow\\b"',
    },
    {
        "phrase": "tomorrow's calendar please",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\btomorrow\'?s calendar\\b"',
    },
    {
        "phrase": "how many meetings do I have tomorrow",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bmeetings.*tomorrow\\b"',
        "notes": (
            "phrased without 'what meetings' so the earlier sibling literal "
            "r'\\bwhat meetings do i have\\b' does not steal the claim first — 'what "
            "meetings do I have tomorrow' hits that literal instead, verified "
            "empirically before rewording"
        ),
    },
    {
        "phrase": "what's the schedule tomorrow",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bschedule.*tomorrow\\b"',
    },
    {
        "phrase": "tomorrow's schedule please",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\btomorrow\'?s schedule\\b"',
    },
    {
        "phrase": "what's happening tomorrow",
        "category": "QUERY",
        "expected": "action:meeting_time",  # RULED 2026-09-30/10-01 (CXO+PPM): was action:week_calendar
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bwhat\'?s.*tomorrow\\b"',
    },
    {
        "phrase": "show calendar this week",
        "category": "QUERY",
        "expected": "action:week_calendar",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bcalendar.*this week\\b"',
    },
    {
        "phrase": "show calendar next week",
        "category": "QUERY",
        "expected": "action:week_calendar",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bcalendar.*next week\\b"',
    },
    {
        "phrase": "what's the schedule this week",
        "category": "QUERY",
        "expected": "action:week_calendar",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bschedule.*this week\\b"',
    },
    {
        "phrase": "what's the schedule next week",
        "category": "QUERY",
        "expected": "action:week_calendar",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bschedule.*next week\\b"',
    },
    {
        "phrase": "how many meetings this week",
        "category": "QUERY",
        "expected": "action:week_calendar",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bmeetings.*this week\\b"',
    },
    {
        "phrase": "how many meetings next week",
        "category": "QUERY",
        "expected": "action:week_calendar",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bmeetings.*next week\\b"',
    },
    {
        "phrase": "how much time in meetings do I have",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bhow much time in meetings\\b"',
        "notes": (
            "phrased without a trailing 'today' so the earlier sibling literal "
            "r'\\bmeetings today\\b' does not steal the claim first — 'how much time in "
            "meetings today' hits that literal instead, verified empirically before "
            "rewording"
        ),
    },
    {
        "phrase": "how much time do I spend sitting in meetings",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bhow much time.*meetings\\b"',
    },
    {
        "phrase": "time spent in meetings is high lately",
        "category": "QUERY",
        "expected": "floor",  # RULED 2026-10-01 (CXO): was action:meeting_time
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\btime spent in meetings\\b"',
        "notes": (
            "phrased without a trailing 'this week' so the earlier sibling literal "
            "r'\\bmeetings.*this week\\b' does not steal the claim first — 'time spent in "
            "meetings this week' hits that literal instead, verified empirically "
            "before rewording"
        ),
    },
    {
        "phrase": "what's my meeting time today",
        "category": "QUERY",
        "expected": "action:meeting_time",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bmeeting time\\b"',
    },
    {
        "phrase": "let's review my recurring meetings",
        "category": "QUERY",
        "expected": "action:recurring_meetings",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\breview.*recurring meetings\\b"',
    },
    {
        "phrase": "audit my standing meetings",
        "category": "QUERY",
        "expected": "action:recurring_meetings",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\baudit.*standing meetings\\b"',
    },
    {
        "phrase": "recurring meetings keep piling up",
        "category": "QUERY",
        "expected": "floor",  # RULED-BY-ANALOGY 2026-10-01: was action:recurring_meetings — an observation, not a request (CXO: "time spent in meetings is high lately" -> floor); flagged to CXO
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\brecurring meetings\\b"',
        "notes": (
            "phrased without a leading 'show'/'review'/'audit' verb so the earlier "
            "sibling literal r'\\bshow.*recurring meetings\\b' does not steal the claim "
            "first — 'show me recurring meetings' hits that literal instead, verified "
            "empirically before rewording"
        ),
    },
    {
        "phrase": "show me my week",
        "category": "QUERY",
        "expected": "action:week_calendar",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bshow.*my week\\b"',
    },
    {
        "phrase": "what's the week ahead look like",
        "category": "QUERY",
        "expected": "action:week_calendar",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bweek ahead\\b"',
    },
    {
        "phrase": "show the week calendar",
        "category": "QUERY",
        "expected": "action:week_calendar",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bweek calendar\\b"',
    },
    {
        "phrase": "check my calendar for conflicts",
        "category": "QUERY",
        "expected": "floor",  # RULED 2026-10-01 (CXO): was action:week_calendar
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bcheck.{0,10}calendar\\b"',
    },
    {
        "phrase": "is my calendar showing any conflict",
        "category": "QUERY",
        "expected": "floor",  # RULED 2026-10-01 (CXO): was action:week_calendar
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bcalendar.*conflict\\b"',
        "notes": (
            "phrased without 'tomorrow' and without a leading 'check' so neither the "
            "earlier sibling literal r'\\bcalendar.*tomorrow\\b' nor the earlier "
            "sub-list match r'\\bcheck.{0,10}calendar\\b' steals the claim first — both "
            "alternatives were tried and failed empirically before this rewording"
        ),
    },
    {
        "phrase": "does my calendar overlap with hers",
        "category": "QUERY",
        "expected": "floor",  # RULED 2026-10-01 (CXO): was action:week_calendar
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bcalendar.*overlap\\b"',
    },
    {
        "phrase": "is there a conflict on my calendar",
        "category": "QUERY",
        "expected": "floor",  # RULED 2026-09-30/10-01 (CXO+PPM): was action:week_calendar  # RULED 2026-10-01 (CXO): was action:meeting_time
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bconflict.*calendar\\b"',
    },
    {
        "phrase": "find time for a 1:1 with sarah",
        "category": "QUERY",
        "expected": "floor",  # RULED 2026-09-30/10-01 (CXO+PPM): was action:week_calendar
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bfind time for\\b"',
    },
    {
        "phrase": "find some time for a sync",
        "category": "QUERY",
        "expected": "floor",  # RULED 2026-09-30/10-01 (CXO+PPM): was action:week_calendar
        "source": (
            "phase3-conversion/CALENDAR_QUERY_PATTERNS literal "
            'r"\\bfind.{0,10}time.{0,10}(?:meeting|1:1|1 on 1|sync|chat)\\b"'
        ),
    },
    {
        "phrase": "schedule a quick call",
        "category": "QUERY",
        "expected": "floor",  # RULED 2026-09-30/10-01 (CXO+PPM): was action:week_calendar
        "source": (
            "phase3-conversion/CALENDAR_QUERY_PATTERNS literal "
            'r"\\bschedule.{0,10}(?:1:1|1 on 1|meeting|sync|call)\\b"'
        ),
    },
    {
        "phrase": "book a slot with the team",
        "category": "QUERY",
        "expected": "floor",  # RULED 2026-09-30/10-01 (CXO+PPM): was action:week_calendar
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bbook.{0,10}(?:meeting|time|1:1|slot)\\b"',
    },
    # — TEMPORAL_PATTERNS (48 of 54 unexercised literals; 2 of 56 were already
    #   exercised before this deposit — "what time is it?" (literal r"\bwhat
    #   time is it\b") and "when is my next meeting?" (claimed by r"\bnext
    #   meeting\b", NOT r"\bwhen is my.{0,10}meeting\b" as its wording might
    #   suggest — confirmed via `PreClassifier._first_pattern_match`, which is
    #   why that longer literal is itself still unexercised and gets its own
    #   row below) — so this block covers the remaining 54 minus 6
    #   structurally unreachable literals, named below. `expected` is
    #   `action:get_current_time` throughout — TEMPORAL_PATTERNS has exactly
    #   one destination in `pre_classify`/`pre_classify_with_pattern_list`
    #   (single-intent path, ~line 1835: `return Intent(category=TEMPORAL,
    #   action="get_current_time", ...), "TEMPORAL_PATTERNS"` — no sub-list
    #   branch the way CALENDAR_QUERY_PATTERNS has one), confirmed
    #   `("TEMPORAL", "get_current_time")` is `ActionDisposition.CANONICAL` in
    #   `action_registry.py` (read only — not modified by this unit). All 48
    #   phrases verified against the REAL production matcher: `PreClassifier.
    #   pre_classify_with_pattern_list(phrase)` returns `("TEMPORAL_PATTERNS",
    #   intent)` with `intent.action == "get_current_time"` read directly (no
    #   action-determining sub-branch to independently verify here, unlike
    #   CALENDAR_QUERY_PATTERNS) AND `PreClassifier._first_pattern_match`
    #   against TEMPORAL_PATTERNS's own literals (in list order) returns
    #   exactly the cited literal, not an earlier sibling literal in the SAME
    #   list, nor an entirely different list checked earlier in the
    #   `pre_classify_with_pattern_list` if-chain (CALENDAR_QUERY_PATTERNS in
    #   particular — it is checked BEFORE TEMPORAL_PATTERNS and several of its
    #   52 literals duplicate or subsume a TEMPORAL_PATTERNS literal's text;
    #   several rows below needed rewording for either kind of shadow, noted
    #   per row).
    #
    #   Six literals are UNREACHABLE at surface 1 and get no deposit here —
    #   confirmed empirically with 2 independent phrasing attempts each (not
    #   just inferred from the regex text), four of them a NEW shadow shape
    #   not seen in the PRIORITY/CALENDAR_QUERY blocks: a TEMPORAL_PATTERNS
    #   literal permanently shadowed by a DIFFERENT, earlier-checked list
    #   (CALENDAR_QUERY_PATTERNS), not merely an earlier sibling in its own
    #   list:
    #     r"\bwhat'?s on my calendar\b"   — CALENDAR_QUERY_PATTERNS has the
    #       IDENTICAL literal and is checked first (pre_classify_with_
    #       pattern_list, ~line 1499 vs. ~line 1835); any match is claimed
    #       there, never reaching TEMPORAL_PATTERNS at all.
    #     r"\bwhat'?s.{0,10}tomorrow\b"   — CALENDAR_QUERY_PATTERNS has the
    #       broader, unbounded r"\bwhat'?s.*tomorrow\b", checked first; every
    #       string the bounded TEMPORAL literal can match (gap <= 10 chars)
    #       also satisfies the unbounded CALENDAR one.
    #     r"\btomorrow'?s schedule\b"     — CALENDAR_QUERY_PATTERNS has the
    #       IDENTICAL literal, checked first.
    #     r"\bmeetings this week\b"       — CALENDAR_QUERY_PATTERNS has the
    #       broader r"\bmeetings.*this week\b", checked first; any string
    #       satisfying the TEMPORAL literal ("meetings" immediately followed
    #       by " this week") trivially satisfies the CALENDAR one too.
    #   Two are the familiar within-list shadow (earlier sibling literal in
    #   TEMPORAL_PATTERNS itself always wins first):
    #     r"\bwhat'?s on my schedule\b"   — always contains "my schedule",
    #       claimed first by r"\bmy schedule\b" (earlier in the list).
    #     r"\bhow long.*been working\b"   — "been working" always contains
    #       "working", so any match also satisfies r"\bhow long.*working\b"
    #       (earlier in the list), which wins first.
    {
        "phrase": "what's the time",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bwhat\'?s the time\\b"',
    },
    {
        "phrase": "current time please",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bcurrent time\\b"',
    },
    {
        "phrase": "give me the time now",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\btime now\\b"',
    },
    {
        "phrase": "tell me the time",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\btell me the time\\b"',
    },
    {
        "phrase": "what day is it",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bwhat day is it\\b"',
    },
    {
        "phrase": "what's the date",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bwhat\'?s the date\\b"',
    },
    {
        "phrase": "current date please",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bcurrent date\\b"',
    },
    {
        "phrase": "today's date please",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\btoday\'?s date\\b"',
    },
    {
        "phrase": "what's today",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bwhat\'?s today\\b"',
    },
    {
        "phrase": "give me the date and time",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bdate and time\\b"',
    },
    {
        "phrase": "what day of the week is it",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bday of the week\\b"',
    },
    {
        "phrase": "tell me the date",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\btell me the date\\b"',
    },
    {
        "phrase": "what date is it",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bwhat date is it\\b"',
    },
    {
        "phrase": "remind me today's day",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\btoday\'?s day\\b"',
        "notes": (
            "reworded — \"what's today's day\" is stolen first by the earlier TEMPORAL_PATTERNS "
            "sibling r'\\bwhat'?s today\\b'; this phrasing avoids that prefix"
        ),
    },
    {
        "phrase": "pull up my calendar",
        "category": "TEMPORAL",
        "expected": "action:week_calendar",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bmy calendar\\b"',
        "notes": (
            "live router (2026-10-01) returned CLARIFY@0.6 for this bare phrase (no day "
            'word); the symmetric sibling row "pull up my schedule" (identical construction, '
            '"schedule" for "calendar") scored week_calendar@0.85 — aligned both to '
            "week_calendar (the higher-confidence verdict) rather than leave two parallel "
            "phrasings disagreeing on what looks like router noise at the low-confidence end"
        ),
    },
    {
        "phrase": "show the team calendar",
        "category": "TEMPORAL",
        "expected": "floor",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bshow.{0,10}calendar\\b"',
        "notes": (
            'reworded — "show my calendar" is stolen first by the earlier TEMPORAL_PATTERNS '
            "sibling r'\\bmy calendar\\b'; this phrasing keeps \"my\" out of the message. "
            "Arch's named example: no team-calendar feature exists; live router agrees "
            "(NONE@0.85, declined to name an operation)."
        ),
    },
    {
        "phrase": "pull up my schedule",
        "category": "TEMPORAL",
        "expected": "action:week_calendar",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bmy schedule\\b"',
    },
    {
        "phrase": "show the team schedule",
        "category": "TEMPORAL",
        "expected": "floor",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bshow.{0,10}schedule\\b"',
        "notes": (
            'reworded — "show my schedule" is stolen first by the earlier TEMPORAL_PATTERNS '
            "sibling r'\\bmy schedule\\b'; this phrasing keeps \"my\" out of the message. "
            "No team-calendar feature exists; live router agrees (NONE@0.85)."
        ),
    },
    {
        "phrase": "calendar check for today",
        "category": "TEMPORAL",
        "expected": "action:meeting_time",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bcalendar.*today\\b"',
    },
    {
        "phrase": "schedule check for today",
        "category": "TEMPORAL",
        "expected": "action:meeting_time",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bschedule.*today\\b"',
        "notes": (
            "live router returned CLARIFY@0.4 (low confidence) despite the phrase explicitly "
            'naming "today" — disagree: the symmetric sibling row "calendar check for today" '
            'scored meeting_time@0.95 for the identical construction with "calendar" for '
            '"schedule"; treating the CLARIFY as router noise at the low-confidence end, not '
            "a real distinction between the two phrasings"
        ),
    },
    {
        "phrase": "walk me through my appointments",
        "category": "TEMPORAL",
        "expected": "action:week_calendar",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bmy appointments\\b"',
    },
    {
        "phrase": "show all appointments",
        "category": "TEMPORAL",
        "expected": "action:week_calendar",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bshow.{0,10}appointments\\b"',
        "notes": (
            '"show the upcoming appointments" exceeds the literal\'s {0,10} gap (14 chars '
            'between "show" and "appointments") and matches no pattern at all; this '
            'phrasing fits the gap. Matches Arch\'s explicit "all appointments" week_calendar '
            "example; live router agrees (week_calendar@0.7)."
        ),
    },
    {
        "phrase": "walk me through my meetings",
        "category": "TEMPORAL",
        "expected": "action:week_calendar",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bmy meetings\\b"',
    },
    {
        "phrase": "what are the upcoming meetings",
        "category": "TEMPORAL",
        "expected": "action:week_calendar",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bupcoming meetings\\b"',
    },
    {
        "phrase": "when is my team meeting",
        "category": "TEMPORAL",
        "expected": "action:meeting_time",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bwhen is my.{0,10}meeting\\b"',
        "notes": (
            'the EXISTING corpus row "when is my next meeting?" claims via the earlier '
            "sibling r'\\bnext meeting\\b', not this literal (confirmed via "
            "_first_pattern_match) — this literal was still unexercised at gate time despite "
            'its wording resembling that row; this phrase avoids "next meeting" so it claims '
            "here instead. Arch named this exact phrase as the single-day meeting_time "
            "example; live router agrees (meeting_time@0.85)."
        ),
    },
    {
        "phrase": "when am i in a meeting",
        "category": "TEMPORAL",
        "expected": "action:meeting_time",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bwhen am i.{0,10}meeting\\b"',
    },
    {
        "phrase": "meeting check for today",
        "category": "TEMPORAL",
        "expected": "action:meeting_time",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bmeeting.*today\\b"',
    },
    {
        "phrase": "meeting check for tomorrow",
        "category": "TEMPORAL",
        "expected": "action:meeting_time",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bmeeting.*tomorrow\\b"',
    },
    {
        "phrase": "walk me through my events",
        "category": "TEMPORAL",
        "expected": "action:week_calendar",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bmy events\\b"',
    },
    {
        "phrase": "show all events",
        "category": "TEMPORAL",
        "expected": "action:week_calendar",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bshow.{0,10}events\\b"',
        "notes": (
            '"show the upcoming events" exceeds the literal\'s {0,10} gap (14 chars between '
            '"show" and "events"), so it does not match this literal at all and falls '
            "through to the later sibling r'\\bupcoming events\\b' instead (same shape as the "
            '"show all appointments" row above); this phrasing fits the gap and avoids '
            '"upcoming" so it claims here. Disagree with the live router (CLARIFY@0.6): the '
            'symmetric sibling row "show all appointments" scored week_calendar@0.7 for the '
            "identical construction — aligned for consistency, treating the CLARIFY as "
            "router noise."
        ),
    },
    {
        "phrase": "what are the upcoming events",
        "category": "TEMPORAL",
        "expected": "action:week_calendar",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bupcoming events\\b"',
    },
    {
        "phrase": "events check for today",
        "category": "TEMPORAL",
        "expected": "action:meeting_time",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bevents.*today\\b"',
    },
    {
        "phrase": "events check for tomorrow",
        "category": "TEMPORAL",
        "expected": "action:meeting_time",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bevents.*tomorrow\\b"',
    },
    {
        "phrase": "when's the next event",
        "category": "TEMPORAL",
        "expected": "action:meeting_time",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bnext event\\b"',
    },
    {
        "phrase": "what did I work on today",
        "category": "TEMPORAL",
        "expected": "action:session_activity_query",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bwork on today\\b"',
        "notes": (
            "beyond Arch's four named buckets (pure time / meeting_time / week_calendar / "
            "floor): this is a retrospective ask a REAL rail-registered operation serves "
            "(session_activity_query, WORKFLOW disposition, flip_group read_status, "
            "workflow_entries.py _query_cohort) — live router agrees "
            "(session_activity_query@0.92), so expected names that operation rather than the "
            "generic floor catch-all"
        ),
    },
    {
        "phrase": "what happened in the meeting yesterday",
        "category": "TEMPORAL",
        "expected": "floor",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bwhat.*yesterday\\b"',
        "notes": (
            "retrospective, no specific item named for check_completion_status to resolve — "
            "live router agrees (NONE@0.95, declined to name an operation)"
        ),
    },
    {
        "phrase": "did I finish the report yesterday",
        "category": "TEMPORAL",
        "expected": "action:check_completion_status",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bdid.*yesterday\\b"',
        "notes": (
            'reworded — "what did I do yesterday" is stolen first by the earlier sibling '
            'r\'\\bwhat.*yesterday\\b\'; this phrasing has no "what" before "yesterday". '
            "Beyond Arch's four named buckets: live router names check_completion_status@0.92 "
            "(STATUS/check_completion_status, ActionDisposition.FLOOR — a floor-routed "
            "canonical with no WorkflowEntry, same shape get_current_time had before this "
            "unit's rail entry — named explicitly rather than collapsed to bare floor since "
            "a real, specific operation serves this ask, it's just not yet rail-dispatchable)"
        ),
    },
    {
        "phrase": "a lot happened yesterday",
        "category": "TEMPORAL",
        "expected": "action:changes_query",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bhappened yesterday\\b"',
        "notes": (
            'reworded — "what happened yesterday" is stolen first by the earlier sibling '
            'r\'\\bwhat.*yesterday\\b\'; this phrasing has no "what" or "did" before '
            '"yesterday". Beyond Arch\'s four named buckets: live router names '
            "changes_query@0.92 (QUERY/changes_query, WORKFLOW disposition, flip_group "
            "read_temporal, workflow_entries.py run_changes_query_workflow) — already "
            "rail-registered and live"
        ),
    },
    {
        "phrase": "when was the last time I worked on this",
        "category": "TEMPORAL",
        "expected": "floor",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\blast time.*worked\\b"',
        "notes": "duration/retrospective ask; live router agrees (CLARIFY@0.4, declined)",
    },
    {
        "phrase": "how long have I been working on this",
        "category": "TEMPORAL",
        "expected": "floor",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bhow long.*working\\b"',
        "notes": (
            "Arch's explicit named example (\"retrospective 'how long have I been working' "
            'if any) -> floor"); live router agrees (CLARIFY@0.3, declined)'
        ),
    },
    {
        "phrase": "this week's priorities, remind me",
        "category": "TEMPORAL",
        "expected": "plan",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bthis week\'?s\\b"',
        "notes": (
            "a PRIORITY-shaped ask in temporal clothing, not a calendar/time query at all; "
            "live router proposes a compound PLAN (get_top_priority\u2192create_reminder), which "
            "this corpus's single `expected: action:X` format cannot represent — floor is the "
            "honest catch-all for a row no single TEMPORAL-family operation serves"
        ),
    },
    {
        "phrase": "next week's priorities, remind me",
        "category": "TEMPORAL",
        "expected": "plan",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bnext week\'?s\\b"',
        "notes": (
            'same shape as the "this week\'s priorities" row above — live router proposes '
            "PLAN[get_top_priority\u2192create_reminder], not representable as a single expected "
            "action"
        ),
    },
    {
        "phrase": "this month's numbers, remind me",
        "category": "TEMPORAL",
        "expected": "plan",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bthis month\'?s\\b"',
        "notes": (
            "live router proposes PLAN[generate_report\u2192create_reminder], not representable "
            "as a single expected action"
        ),
    },
    {
        "phrase": "when am i free",
        "category": "TEMPORAL",
        "expected": "action:week_calendar",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bwhen am i free\\b"',
    },
    {
        "phrase": "when's my next free slot",
        "category": "TEMPORAL",
        "expected": "action:meeting_time",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bwhen\'?s my next.{0,10}free\\b"',
    },
    {
        "phrase": "what's my available time",
        "category": "TEMPORAL",
        "expected": "action:week_calendar",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bavailable time\\b"',
    },
    {
        "phrase": "when do I have free time",
        "category": "TEMPORAL",
        "expected": "action:week_calendar",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bfree time\\b"',
    },
    {
        "phrase": "what are my open slots",
        "category": "TEMPORAL",
        "expected": "action:week_calendar",  # SORTED 2026-10-01 (Arch's ruling): was action:get_current_time
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bopen slots\\b"',
    },
    # — GITHUB_QUERY_PATTERNS (53 of 53 unexercised literals get a row; 11 of
    #   64 were already exercised before this deposit — "show my open
    #   issues", "show my open pull requests", "close issue 42", "comment on
    #   issue 42: looks good", "what did we ship this week?", "show stale
    #   prs", "close issue #123", "reopen issue #123", "comment on issue
    #   #123", "how many open issues do we have?", "show my prs" — plus 2
    #   PRE-EXISTING [FAIL] rows this unit did NOT touch ("show issue #123",
    #   "show milestones" — both REVIEW-disagreements between the
    #   pre-classifier's claim and the router's actual route; reported to the
    #   Lead, not re-expected here — correcting an existing row's `expected`
    #   is a ruling, not a deposit). Unlike CALENDAR/TEMPORAL, ALL 53 literals
    #   are reachable — no structurally-unreachable literal found (none
    #   needed more than one reword; the 5 that needed rewording are noted
    #   per row below).
    #
    #   `expected` is `action:<name>`, the action `PreClassifier.
    #   pre_classify_with_pattern_list(phrase).action` actually returns for
    #   that exact phrase — verified directly, not hand-traced from the
    #   branch's if/elif (the branch's action-determination re-checks the
    #   message against several HARDCODED SUB-LISTS, independent of which
    #   GITHUB_QUERY_PATTERNS literal claimed the row — see finding below).
    #   `PreClassifier._first_pattern_match` against GITHUB_QUERY_PATTERNS's
    #   own literals (list order) confirms the cited literal claims first,
    #   not an earlier sibling.
    #
    #   **Significant finding, reported not fixed**: the milestones/
    #   releases/labels/branches literals (23 of the 53 rows below — every
    #   literal from `\blist.*milestones?\b` through `\bwhat branches?\b`)
    #   all claim via GITHUB_QUERY_PATTERNS but get action=review_issue_query
    #   — the SAME action as "show me issue #42" — because the branch's
    #   action-determination if/elif chain in `pre_classify_with_pattern_list`
    #   (services/intent_service/pre_classifier.py ~1532-1620) has NO case for
    #   milestones/releases/labels/branches; every literal that isn't
    #   shipped/stale/close/reopen/comment/list_issues/list_prs falls into the
    #   trailing `else: action = review_issue_query`. This is despite
    #   `list_milestones_query` / `list_releases_query` / `list_labels_query`
    #   / `list_branches_query` being fully registered WORKFLOW actions with
    #   their own handlers and `read_status` flip groups in
    #   `workflow_entries.py` (`_handle_list_milestones_query` etc., lines
    #   ~1216-1219/1256-1261) — those four handlers are structurally
    #   unreachable from this branch's action-determination logic, confirmed
    #   empirically (not inferred) for all 23 literals. The pre-existing
    #   "show milestones" FAIL row already shows this exact disagreement at
    #   one data point (claim=review_issue_query, router=list_milestones@1.0)
    #   — this deposit shows the disagreement's full scope. Not corrected
    #   here (a ruling, not a deposit); flagged for the Lead/Arch.
    #
    #   Flip groups (workflow_entries.py `_READ_QUERY_FLIP_GROUPS`, read
    #   only): shipped_query/stale_prs_query/list_issues_query/list_prs_query
    #   -> read_status; review_issue_query -> read_referent — both live under
    #   the dispatch's `--live` set, so all 45 QUERY-category rows below mark
    #   [OK] "expected action live via group" once re-gated. close_issue_query
    #   / reopen_issue_query / comment_issue_query (8 EXECUTION-category rows,
    #   matching the pre-existing close/reopen/comment rows' own category
    #   convention) carry NO flip_group and NO flip_write_allowlist_key —
    #   confirmed via `grep` on workflow_entries.py — so unlike the five QUERY
    #   actions above, these 8 rows are NOT live under any `--live` token
    #   today; expected to UNSCORED/not-live until the Lead's own write-rail
    #   ruling, not a deposit defect.
    #
    #   5 of the 53 phrases needed a reword after a first attempt was claimed
    #   by an earlier sibling literal or a DIFFERENT, earlier-checked list:
    #     "show me what shipped" -> claimed by \bwhat shipped\b (earlier
    #       sibling); reworded "can you show what has shipped".
    #     "what shipped this week" -> claimed by \bwhat shipped\b (earlier
    #       sibling); reworded "what has shipped this past week".
    #     "what's the next milestone" -> claimed by
    #       MILESTONE_STATUS_INLINE_PATTERNS (a DIFFERENT, earlier-checked
    #       list — STATUS category, action=get_project_status, per the #1068
    #       ordering comment), not GITHUB_QUERY_PATTERNS at all; reworded
    #       "any update on the next milestone".
    #     "what prs are assigned to me" / "which pull requests are assigned
    #       to me" -> matched NO literal at all (the literals
    #       `\bprs assigned to me\b` / `\bpull requests assigned to me\b`
    #       require that exact adjacency, no "are" in between); reworded "any
    #       prs assigned to me" / "any pull requests assigned to me".
    {
        "phrase": "what shipped recently",
        "category": "QUERY",
        "expected": "action:shipped_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bwhat shipped\\b"',
    },
    {
        "phrase": "can you show what has shipped",
        "category": "QUERY",
        "expected": "action:shipped_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bshow.*what.*shipped\\b"',
    },
    {
        "phrase": "what has shipped this past week",
        "category": "QUERY",
        "expected": "action:shipped_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bwhat.*shipped.*week\\b"',
    },
    {
        "phrase": "show our stale pull requests",
        "category": "QUERY",
        "expected": "action:stale_prs_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bstale pull requests\\b"',
    },
    {
        "phrase": "any old prs lying around",
        "category": "QUERY",
        "expected": "action:stale_prs_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bold prs\\b"',
    },
    {
        "phrase": "prs needing review",
        "category": "QUERY",
        "expected": "action:stale_prs_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bprs.*needing review\\b"',
    },
    {
        "phrase": "close the completed issue",
        "category": "EXECUTION",
        "expected": "action:close_issue_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bclose.*completed.*issue\\b"',
    },
    {
        "phrase": "please close this issue",
        "category": "EXECUTION",
        "expected": "action:close_issue_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bclose.*issue\\b"',
    },
    {
        "phrase": "re-open issue 88",
        "category": "EXECUTION",
        "expected": "action:reopen_issue_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bre-open\\s+issue\\s*#?\\d+\\b"',
    },
    {
        "phrase": "reopen the old issue",
        "category": "EXECUTION",
        "expected": "action:reopen_issue_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\breopen\\s+.*issue\\b"',
    },
    {
        "phrase": "re-open the old issue",
        "category": "EXECUTION",
        "expected": "action:reopen_issue_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bre-open\\s+.*issue\\b"',
    },
    {
        "phrase": "add comment to issue 99",
        "category": "EXECUTION",
        "expected": "action:comment_issue_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\badd comment to issue\\s*#?\\d+\\b"',
    },
    {
        "phrase": "reply to issue 99",
        "category": "EXECUTION",
        "expected": "action:comment_issue_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\breply to issue\\s*#?\\d+\\b"',
    },
    {
        "phrase": "comment on 99",
        "category": "EXECUTION",
        "expected": "action:comment_issue_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bcomment\\s+on\\s+#?\\d+\\b"',
    },
    {
        "phrase": "review issue 101",
        "category": "QUERY",
        "expected": "action:review_issue_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\breview issue\\s*#?\\d+\\b"',
    },
    {
        "phrase": "issue 101 details",
        "category": "QUERY",
        "expected": "action:review_issue_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bissue\\s*#?\\d+\\s*details\\b"',
    },
    {
        "phrase": "get issue 101",
        "category": "QUERY",
        "expected": "action:review_issue_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bget issue\\s*#?\\d+\\b"',
    },
    {
        "phrase": "what are my issues",
        "category": "QUERY",
        "expected": "action:list_issues_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bmy issues\\b"',
    },
    {
        "phrase": "list the issues please",
        "category": "QUERY",
        "expected": "action:list_issues_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\blist.*issues\\b"',
    },
    {
        "phrase": "show the issues",
        "category": "QUERY",
        "expected": "action:list_issues_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bshow.*issues\\b"',
    },
    {
        "phrase": "what's the issue count",
        "category": "QUERY",
        "expected": "action:list_issues_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bissue count\\b"',
    },
    {
        "phrase": "which issues are assigned to engineering",
        "category": "QUERY",
        "expected": "action:list_issues_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bissues.*assigned\\b"',
    },
    {
        "phrase": "show my pull requests",
        "category": "QUERY",
        "expected": "action:list_prs_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bshow my pull requests\\b"',
    },
    {
        "phrase": "what are my prs looking like",
        "category": "QUERY",
        "expected": "action:list_prs_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bmy prs\\b"',
    },
    {
        "phrase": "where are my pull requests",
        "category": "QUERY",
        "expected": "action:list_prs_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bmy pull requests\\b"',
    },
    {
        "phrase": "list the prs",
        "category": "QUERY",
        "expected": "action:list_prs_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\blist.*prs\\b"',
    },
    {
        "phrase": "list all pull requests from this sprint",
        "category": "QUERY",
        "expected": "action:list_prs_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\blist.*pull requests\\b"',
    },
    {
        "phrase": "any open prs waiting on me",
        "category": "QUERY",
        "expected": "action:list_prs_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bopen prs\\b"',
    },
    {
        "phrase": "any prs assigned to me",
        "category": "QUERY",
        "expected": "action:list_prs_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bprs assigned to me\\b"',
    },
    {
        "phrase": "any pull requests assigned to me",
        "category": "QUERY",
        "expected": "action:list_prs_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bpull requests assigned to me\\b"',
    },
    {
        "phrase": "list the milestones for this quarter",
        "category": "QUERY",
        "expected": "action:list_milestones_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\blist.*milestones?\\b"',
    },
    {
        "phrase": "any update on the next milestone",
        "category": "QUERY",
        "expected": "action:review_issue_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bnext milestone\\b"',
    },
    {
        "phrase": "what milestones do we have",
        "category": "QUERY",
        "expected": "action:list_milestones_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bwhat milestones?\\b"',
    },
    {
        "phrase": "milestones due this month",
        "category": "QUERY",
        "expected": "action:list_milestones_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bmilestones?\\s+(?:status|count|list|due)\\b"',
    },
    {
        "phrase": "when's the milestone deadline",
        "category": "QUERY",
        "expected": "action:list_milestones_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bwhen.*milestone\\b"',
    },
    {
        "phrase": "any recent releases",
        "category": "QUERY",
        "expected": "action:list_releases_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\brecent releases?\\b"',
    },
    {
        "phrase": "show me the releases",
        "category": "QUERY",
        "expected": "action:list_releases_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bshow.*releases?\\b"',
    },
    {
        "phrase": "list our releases",
        "category": "QUERY",
        "expected": "action:list_releases_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\blist.*releases?\\b"',
    },
    {
        "phrase": "what version are we on",
        "category": "QUERY",
        "expected": "action:review_issue_query",
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bwhat version (?:are we on|is current)\\b"',
    },
    {
        "phrase": "what's the current release",
        "category": "QUERY",
        "expected": "action:list_releases_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bcurrent (?:release|version)\\b"',
    },
    {
        "phrase": "what's our latest release",
        "category": "QUERY",
        "expected": "action:list_releases_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\blatest release\\b"',
    },
    {
        "phrase": "what labels do we use",
        "category": "QUERY",
        "expected": "action:list_labels_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bwhat labels?\\b"',
    },
    {
        "phrase": "show me the labels",
        "category": "QUERY",
        "expected": "action:list_labels_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bshow.*labels?\\b"',
    },
    {
        "phrase": "list the labels",
        "category": "QUERY",
        "expected": "action:list_labels_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\blist.*labels?\\b"',
    },
    {
        "phrase": "what are the issue labels",
        "category": "QUERY",
        "expected": "action:list_labels_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bissue labels?\\b"',
    },
    {
        "phrase": "labels count please",
        "category": "QUERY",
        "expected": "action:list_labels_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\blabels?\\s+(?:list|count)\\b"',
    },
    {
        "phrase": "all labels please",
        "category": "QUERY",
        "expected": "action:list_labels_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\b(?:available|all)\\s+labels?\\b"',
    },
    {
        "phrase": "show me the active branches",
        "category": "QUERY",
        "expected": "action:list_branches_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bactive branches?\\b"',
    },
    {
        "phrase": "show which branches exist",
        "category": "QUERY",
        "expected": "action:list_branches_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bshow.*branches?\\b"',
    },
    {
        "phrase": "list the branches",
        "category": "QUERY",
        "expected": "action:list_branches_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\blist.*branches?\\b"',
    },
    {
        "phrase": "what feature branches do we have",
        "category": "QUERY",
        "expected": "action:list_branches_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bfeature branches?\\b"',
    },
    {
        "phrase": "what are the current branches",
        "category": "QUERY",
        "expected": "action:list_branches_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bcurrent branches?\\b"',
    },
    {
        "phrase": "what branches do we have",
        "category": "QUERY",
        "expected": "action:list_branches_query",  # CORRECTED 2026-10-01: was action:review_issue_query — the branch has no case for this literal family (lane finding); the router names the real op
        "source": 'phase3-conversion/GITHUB_QUERY_PATTERNS literal r"\\bwhat branches?\\b"',
    },
    # — PRIORITY_PATTERNS, the three literals no corpus row ever exercised
    #   (found at the sixth deletion, 2026-10-02 — deposited by the Lead the
    #   same hour so the ledger's "every literal exercised" claim holds; the
    #   destination is the floor, so these are scored under the FLOOR rule).
    {
        "phrase": "what's my most important task right now",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bmost important task\\b"',
    },
    {
        "phrase": "what is my most important work today",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bmost important work\\b"',
    },
    {
        "phrase": "what should I work on next",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bwhat.*work on next\\b"',
    },
    # — STATUS_PATTERNS (46 of 51 unexercised literals get a row; 5 of 56 were
    #   already exercised before this deposit — "what am I working on?",
    #   "show me my archived projects", "what are my projects?", "give me my
    #   standup", "give me a project status report" — plus 2 PRE-EXISTING
    #   [FAIL] rows this unit did NOT touch ("what am I working on?" —
    #   expected=category:STATUS, router=get_top_priority, MISMATCH; "show me
    #   my archived projects" — expected=REVIEW, router=list_archived_projects,
    #   REVIEW-disagrees). Reported to the Lead, not re-expected here —
    #   correcting an existing row's `expected` is a ruling, not a deposit.
    #
    #   5 of the 51 unexercised literals are structurally UNREACHABLE — more
    #   severe than GITHUB's shadow finding, because these are BYTE-IDENTICAL
    #   regex duplicates of literals in OTHER lists checked earlier in the
    #   `pre_classify_with_pattern_list` if-chain (services/intent_service/
    #   pre_classifier.py), not just an earlier sibling in the same list:
    #     `\bnext milestone\b` — AT DEPOSIT TIME, byte-identical to
    #       GITHUB_QUERY_PATTERNS' own `\bnext milestone\b` (line ~448),
    #       checked at ~1532, before STATUS_PATTERNS at ~1810; ANY phrase
    #       matching this regex matched GITHUB's identical copy first
    #       (confirmed then: "next milestone details" ->
    #       GITHUB_QUERY_PATTERNS, action=review_issue_query).
    #       CORRECTED 2026-10-02 (seventh-deletion gate run, STATUS_PATTERNS):
    #       GITHUB_QUERY_PATTERNS was itself emptied by the fifth deletion
    #       (2026-10-02, same day, after this deposit) — its shadowing copy
    #       of `\bnext milestone\b` no longer exists, so STATUS_PATTERNS'
    #       own `\bnext milestone\b` is REACHABLE again for any phrase that
    #       does not ALSO match MILESTONE_STATUS_INLINE_PATTERNS' "what's the
    #       next/upcoming milestone" shape (e.g. "any update on the next
    #       milestone" — confirmed via `pre_classify_with_pattern_list`,
    #       which now returns STATUS_PATTERNS for it). This is exactly the
    #       seventh deletion gate's finding: `\bnext milestone\b` is one of
    #       the 4 load-bearing SURVIVORS, not one of the unreachable four —
    #       the claim below was accurate when written, not after GITHUB's
    #       own deletion landed. See scripts/inversion_phase3_deleted_patterns.json's
    #       STATUS_PATTERNS entry for the current, re-verified account.
    #     `\bwhat'?s the (?:next|upcoming) milestone\b`, `\bmilestone
    #       status\b`, `\bmilestone progress\b` — byte-identical to the
    #       INLINE (non-class-attribute) `MILESTONE_STATUS_INLINE_PATTERNS`
    #       list (pre_classifier.py ~1502-1515, issue #1068), checked before
    #       even GITHUB_QUERY_PATTERNS. Same mathematical-unreachability
    #       argument (confirmed: "milestone status please" / "milestone
    #       progress report" -> MILESTONE_STATUS_INLINE_PATTERNS). Net: this
    #       destination is IDENTICAL either way (STATUS/get_project_status),
    #       so the shadow is behaviorally inert, but the STATUS_PATTERNS
    #       literal itself is dead code.
    #     `\bmy current work\b` — shadowed WITHIN this same list by its own
    #       earlier, shorter sibling `\bcurrent work\b` (STATUS_PATTERNS
    #       line ~269, checked before line ~280's `\bmy current work\b` in
    #       list-iteration order). "current work" is a guaranteed substring
    #       of "my current work" (preceded by a space => a `\b` boundary is
    #       always present), so the shorter pattern provably claims first for
    #       every possible phrase — not a phrasing-dependent shadow like
    #       CALENDAR/TEMPORAL's, a structural one. Confirmed empirically with
    #       two independent phrasings, both claimed by `\bcurrent work\b`.
    #   AT DEPOSIT TIME: only `\bupcoming milestones?\b` (no duplicate
    #   anywhere else in the file — grep-confirmed) survived reachable from
    #   the milestone subfamily. CORRECTED 2026-10-02 (seventh-deletion gate
    #   run): post-GITHUB-deletion, TWO of the 5-literal subfamily are
    #   reachable — `\bupcoming milestones?\b` (this row) AND `\bnext
    #   milestone\b` (see the correction on that bullet above) — both are
    #   seventh-deletion load-bearing survivors. The other 3
    #   (`\bwhat'?s the (?:next|upcoming) milestone\b`, `\bmilestone
    #   status\b`, `\bmilestone progress\b`) remain cross-list shadowed by
    #   MILESTONE_STATUS_INLINE_PATTERNS exactly as documented above — that
    #   part of this block comment was never stale.
    #
    #   `expected` is `action:<name>`, the action `PreClassifier.
    #   pre_classify_with_pattern_list(phrase).action` actually returns for
    #   that exact phrase — verified directly. Unlike GITHUB_QUERY_PATTERNS'
    #   partial if/elif branching, STATUS_PATTERNS' claim branch
    #   (pre_classifier.py ~1807-1816) has NO branching at all: every one of
    #   its 56 literals returns the single hardcoded action
    #   `get_project_status` — the "no case for this family" shape
    #   (dispatch's framing) applies to the ENTIRE list here, not a subset.
    #
    #   **Significant finding #1, reported not fixed**: `get_project_status`
    #   itself has NO WorkflowEntry / flip_group in workflow_entries.py
    #   (grep-confirmed: zero hits) and STATUS is not a canonical-handler
    #   category either — `canonical_handlers.py:141-156`'s own docstring
    #   states "STATUS/PRIORITY removed Apr 13 (#925) — floor-routed via
    #   Action Gate," i.e. EVERY STATUS claim, regardless of which literal
    #   fired, is floor-routed in production (services/intent_service/
    #   canonical_handlers.py, `canonical_categories` set — STATUS absent;
    #   confirmed by direct read, not inferred). `action:get_project_status`
    #   is therefore a classification label, not a live dispatch destination
    #   — the Lead's Haiku scoring pass will need to decide whether the
    #   gate's live-match mechanism (keyed on registered flip_groups) can
    #   ever read these rows as [OK] short of a `floor`-shaped expected, or
    #   whether MATCH/REVIEW-agreement against the router's own classified
    #   category is the right bar. Flagged for the Lead/Arch, not resolved
    #   here (a ruling, not a deposit).
    #
    #   **Significant finding #2 / corrections applied** (mirroring GITHUB's
    #   milestone/release/label/branch correction): 8 of the 46 rows below
    #   have their `expected` CORRECTED away from the uniformly-emitted
    #   `action:get_project_status`, where the literal's own words plainly
    #   name a different, already-registered destination with DIRECT
    #   evidence in THIS corpus (not speculation):
    #     - 6 standup literals -> `action:show_standup`. Direct anchor: the
    #       pre-existing, already-MATCH-scored row "give me my standup"
    #       (claim=get_project_status, expected=action:show_standup,
    #       router=show_standup@0.95, verdict=MATCH) already establishes
    #       this correction for the same literal family in this same corpus
    #       — `show_standup` IS workflow-registered (`["show_standup",
    #       "get_standup"]`, flip_group `read_status`, workflow_entries.py
    #       ~2505), unlike get_project_status.
    #     - `\bmy portfolio\b` and `\blist.*projects\b` -> `action:
    #       manage_portfolio`. Direct anchor: the pre-existing,
    #       already-MATCH-scored row "what are my projects?"
    #       (claim=get_project_status, expected=action:manage_portfolio,
    #       router=manage_portfolio@0.95, verdict=MATCH) for the sibling
    #       `\bmy projects\b` literal in this same list, corroborated by
    #       in-code documentation of the SAME collision for these two exact
    #       literals (pre_classifier.py ~2515-2538, #1738/#1884: "my
    #       portfolio"/"my projects" wording and the
    #       `r"\blist.*projects\b"` broad literal are both named as
    #       colliding with PORTFOLIO's own claim, "STATUS is the
    #       false-positive overlap"). `manage_portfolio` is
    #       canonical-handler-dispatched (PORTFOLIO is in
    #       `canonical_handlers.py`'s `canonical_categories` set) — a real,
    #       live destination, unlike floor-routed get_project_status.
    #   The remaining 38 rows (including the one reachable milestone
    #   survivor) keep `action:get_project_status` uncorrected: the
    #   milestone case is DELIBERATE design per the Issue #898 Q25 comment
    #   ("Milestone queries are project status, not priority," line ~324),
    #   and the other 37 (status/progress/tasks/assignments/work vocabulary)
    #   have no comparably direct in-corpus or in-code anchor pointing to a
    #   more specific destination — correcting them without evidence would
    #   be guessing, which this deposit does not do (contrast: GITHUB's
    #   milestone/release/label/branch correction came from a POST-DEPOSIT
    #   Haiku-scoring pass finding REVIEW-agreement with specific ops, not
    #   from the depositing agent's own judgment).
    #
    #   All 46 phrases verified empirically: `pre_classify_with_pattern_list`
    #   returns `STATUS_PATTERNS` as the claiming list AND
    #   `PreClassifier._first_pattern_match` against STATUS_PATTERNS' own
    #   literals (list order) confirms the cited literal claims first, not
    #   an earlier sibling. 12 of the 46 needed a reword after a first
    #   attempt was claimed by an earlier sibling literal (the "my X" short
    #   literal shadowing a later "show/list/how's/what's.*X" broad one) or
    #   by a different, earlier-checked list (PORTFOLIO_PATTERNS):
    #     "what am I working on now" -> claimed by \bwhat am i working on\b
    #       (earlier sibling, already-exercised literal); reworded "quick
    #       check, working on now?".
    #     "show me my status"/"show me my standup"/"show me my progress"/
    #       "show me my tasks"/"show me my assignments" -> each claimed by
    #       the corresponding earlier "my X" sibling; reworded to "show
    #       {the current|today's} X" (no "my").
    #     "how's my progress going" / "what's my progress looking like" ->
    #       claimed by \bmy progress\b (earlier sibling); reworded "how's
    #       the progress going" / "what's the progress looking like".
    #     "list my tasks" / "what tasks am I working on" -> "list my tasks"
    #       claimed by \bmy tasks\b; "what tasks am I working on" claimed by
    #       the much-earlier \bwhat.*working on\b (not a same-list sibling —
    #       checked at list position ~11 vs `\btasks.*working\b`'s ~40);
    #       reworded "list today's tasks" / "tasks I'm actively working on".
    #     "list my projects" -> claimed by PORTFOLIO_PATTERNS (a DIFFERENT,
    #       much-earlier-checked list — PORTFOLIO_PATTERNS is checked at
    #       ~1366, before even MILESTONE_STATUS_INLINE_PATTERNS at ~1502 —
    #       via the named `PORTFOLIO_LIST_PATTERN` constant, which matches
    #       "list my projects" exactly); reworded "list my active projects
    #       for this quarter" (inserting a word between "my" and "projects"
    #       defeats PORTFOLIO_LIST_PATTERN's adjacency requirement while
    #       `\blist.*projects\b`'s `.*` still spans it).
    #
    #   Flip groups (workflow_entries.py, read only): `show_standup` ->
    #   `read_status` (live under the dispatch's `--live` set). `manage_
    #   portfolio` and `get_project_status` carry NO flip_group (neither is
    #   WORKFLOW-rail-registered; PORTFOLIO is canonical-handler-dispatched,
    #   STATUS is floor-routed) — confirmed via grep, not assumed.
    {
        "phrase": "time for my stand-up",
        "category": "STATUS",
        "expected": "action:show_standup",  # CORRECTED: was action:get_project_status — literal names standup; anchor row "give me my standup" (same list, same corpus) already MATCH-scores this correction
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bstand-up\\b"',
    },
    {
        "phrase": "give me my stand up",
        "category": "STATUS",
        "expected": "action:show_standup",  # CORRECTED: was action:get_project_status — see "time for my stand-up" above
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bstand up\\b"',
    },
    {
        "phrase": "give me a standup update",
        "category": "STATUS",
        "expected": "action:show_standup",  # CORRECTED: was action:get_project_status — see "time for my stand-up" above
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bstandup update\\b"',
    },
    {
        "phrase": "give me a standup report",
        "category": "STATUS",
        "expected": "action:show_standup",  # CORRECTED: was action:get_project_status — see "time for my stand-up" above
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bstandup report\\b"',
    },
    {
        "phrase": "what's my daily standup",
        "category": "STATUS",
        "expected": "action:show_standup",  # CORRECTED: was action:get_project_status — see "time for my stand-up" above
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bdaily standup\\b"',
    },
    {
        "phrase": "show today's standup",
        "category": "STATUS",
        "expected": "action:show_standup",  # CORRECTED: was action:get_project_status — see "time for my stand-up" above
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bshow.*standup\\b"',
    },
    {
        "phrase": "show me my portfolio",
        "category": "STATUS",
        "expected": "action:manage_portfolio",  # CORRECTED: was action:get_project_status — literal names "portfolio"; anchor row "what are my projects?" (sibling literal, same list, same corpus) already MATCH-scores manage_portfolio; corroborated by pre_classifier.py ~2515-2538 (#1738/#1884) naming this exact literal as a documented PORTFOLIO collision
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bmy portfolio\\b"',
    },
    {
        "phrase": "list my active projects for this quarter",
        "category": "STATUS",
        "expected": "action:manage_portfolio",  # CORRECTED: was action:get_project_status — pre_classifier.py ~2515-2538 (#1738/#1884) names this exact literal (r"\blist.*projects\b") as a documented PORTFOLIO collision; see "show me my portfolio" above
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\blist.*projects\\b"',
        "notes": "reworded from the natural 'list my projects' — that exact phrase is claimed by PORTFOLIO_PATTERNS first (PORTFOLIO_LIST_PATTERN, pre_classifier.py ~1011, checked ~1366, before STATUS_PATTERNS ~1810); inserting a word between 'my' and 'projects' defeats PORTFOLIO_LIST_PATTERN's strict adjacency while STATUS's own broader `.*` still spans it",
    },
    {
        "phrase": "any upcoming milestones for this project",
        "category": "STATUS",
        "expected": "action:list_milestones",  # CORRECTED 2026-10-01 (Lead): was action:get_project_status — upcoming milestones → the milestones list op, same ruling as the 2026-10-01 GITHUB_QUERY milestone correction (#898 Q25 predates list_milestones)
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bupcoming milestones?\\b"',
        "notes": "AT DEPOSIT TIME, the one reachable survivor of STATUS_PATTERNS' 5-literal milestone subfamily (the other 4 structurally unreachable — see block comment above). CORRECTED 2026-10-02 (seventh-deletion gate run): post-GITHUB-deletion, `\\bnext milestone\\b` is ALSO reachable (GITHUB_QUERY_PATTERNS' own shadowing copy was emptied by the fifth deletion) — it is the seventh deletion's other milestone-family survivor, claimed via \"any update on the next milestone\"; the remaining 3 (`\\bwhat'?s the (?:next|upcoming) milestone\\b`, `\\bmilestone status\\b`, `\\bmilestone progress\\b`) stay cross-list shadowed by MILESTONE_STATUS_INLINE_PATTERNS as originally documented. The STATUS category (vs. PRIORITY) for this milestone subfamily is DELIBERATE design per Issue #898 Q25 ('Milestone queries are project status, not priority', pre_classifier.py line ~324); this row's own `expected` was separately corrected 2026-10-01 to action:list_milestones (see this row's own comment), so the 'get_project_status' destination named in the ORIGINAL version of this note applied to the family's category rationale, not to this row's final expected action",
    },
    {
        "phrase": "what's my current project",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bwhat\'?s my current project\\b"',
    },
    {
        "phrase": "can you summarize my current work",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bcurrent work\\b"',
    },
    {
        "phrase": "what are my current projects",
        "category": "STATUS",
        "expected": "action:manage_portfolio",  # CORRECTED 2026-10-01 (Lead): was action:get_project_status — a projects listing — same anchor as the lane's \bmy portfolio\b / \blist.*projects\b corrections ('what are my projects?' MATCH, #1738/#1884)
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bcurrent projects\\b"',
    },
    {
        "phrase": "give me a project overview",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bproject overview\\b"',
    },
    {
        "phrase": "what's the project landscape",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bproject landscape\\b"',
    },
    {
        "phrase": "what projects am I working on",
        "category": "STATUS",
        "expected": "action:manage_portfolio",  # CORRECTED 2026-10-01 (Lead): was action:get_project_status — a projects listing — same anchor as the lane's \bmy portfolio\b / \blist.*projects\b corrections ('what are my projects?' MATCH, #1738/#1884)
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bprojects.*working on\\b"',
    },
    {
        "phrase": "tell me what I'm working on",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bwhat.*working on\\b"',
    },
    {
        "phrase": "quick check, working on now?",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bworking on now\\b"',
        "notes": "reworded from 'what am I working on now' — claimed by the earlier, already-exercised sibling \\bwhat am i working on\\b instead",
    },
    {
        "phrase": "what are my active projects",
        "category": "STATUS",
        "expected": "action:manage_portfolio",  # CORRECTED 2026-10-01 (Lead): was action:get_project_status — a projects listing — same anchor as the lane's \bmy portfolio\b / \blist.*projects\b corrections ('what are my projects?' MATCH, #1738/#1884)
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bactive projects\\b"',
    },
    {
        "phrase": "show my active work",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bactive work\\b"',
    },
    {
        "phrase": "what's my status",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bwhat\'?s my status\\b"',
    },
    {
        "phrase": "give me a status update",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bstatus update\\b"',
    },
    {
        "phrase": "what is my status",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bmy status\\b"',
    },
    {
        "phrase": "what's my work status",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bwork status\\b"',
    },
    {
        "phrase": "show the current status",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bshow.*status\\b"',
        "notes": "reworded from 'show me my status' — claimed by the earlier sibling \\bmy status\\b instead",
    },
    {
        "phrase": "what's the current status",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bcurrent status\\b"',
    },
    {
        "phrase": "I need a status report",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bstatus report\\b"',
    },
    {
        "phrase": "what's my progress",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bmy progress\\b"',
    },
    {
        "phrase": "give me a progress update",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bprogress update\\b"',
    },
    {
        "phrase": "I need a progress report",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bprogress report\\b"',
    },
    {
        "phrase": "what's the progress on this",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bprogress on\\b"',
    },
    {
        "phrase": "show today's progress",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bshow.*progress\\b"',
        "notes": "reworded from 'show me my progress' — claimed by the earlier sibling \\bmy progress\\b instead",
    },
    {
        "phrase": "what's the current progress",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bcurrent progress\\b"',
    },
    {
        "phrase": "how's the progress going",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bhow\'?s.*progress\\b"',
        "notes": "reworded from 'how's my progress going' — claimed by the earlier sibling \\bmy progress\\b instead",
    },
    {
        "phrase": "what's the progress looking like",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bwhat\'?s.*progress\\b"',
        "notes": "reworded from 'what's my progress looking like' — claimed by the earlier sibling \\bmy progress\\b instead",
    },
    {
        "phrase": "what are my tasks",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bmy tasks\\b"',
    },
    {
        "phrase": "show me my current tasks",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bcurrent tasks\\b"',
    },
    {
        "phrase": "what are my active tasks",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bactive tasks\\b"',
    },
    {
        "phrase": "show today's tasks",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bshow.*tasks\\b"',
        "notes": "reworded from 'show me my tasks' — claimed by the earlier sibling \\bmy tasks\\b instead",
    },
    {
        "phrase": "list today's tasks",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\blist.*tasks\\b"',
        "notes": "reworded from 'list my tasks' — claimed by the earlier sibling \\bmy tasks\\b instead",
    },
    {
        "phrase": "tasks I'm actively working on",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\btasks.*working\\b"',
        "notes": "reworded from 'what tasks am I working on' — claimed by the much-earlier (list position ~11, not a same-list sibling of this literal's ~40) \\bwhat.*working on\\b instead",
    },
    {
        "phrase": "what tasks do I have",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bwhat tasks\\b"',
    },
    {
        "phrase": "what's the task status",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\btask status\\b"',
    },
    {
        "phrase": "what are my assignments",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bmy assignments\\b"',
    },
    {
        "phrase": "show me my current assignments",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bcurrent assignments\\b"',
    },
    {
        "phrase": "what's assigned to me",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bwhat\'?s assigned\\b"',
    },
    {
        "phrase": "show today's assignments",
        "category": "STATUS",
        "expected": "action:get_project_status",
        "source": 'phase3-conversion/STATUS_PATTERNS literal r"\\bshow.*assignments\\b"',
        "notes": "reworded from 'show me my assignments' — claimed by the earlier sibling \\bmy assignments\\b instead",
    },
    # — DISCOVERY_PATTERNS / ANALYSIS_PATTERNS / TRUST_PATTERNS / MEMORY_PATTERNS
    #   (#1595 epic-0 unit 5, 2026-10-02): all four lists are single-action,
    #   no per-literal branching (`pre_classify_with_pattern_list` returns
    #   one hardcoded action for every literal in the list, same "no case
    #   for this family" shape as STATUS_PATTERNS above) — DISCOVERY ->
    #   get_capabilities, ANALYSIS -> analyze_blockers, TRUST ->
    #   explain_trust, MEMORY -> get_memory. All four actions are
    #   ActionDisposition.FLOOR in action_registry.py AND have zero
    #   WorkflowEntry/flip_group registrations in workflow_entries.py
    #   (grep-confirmed) — this is the DOCUMENTED, already-known disposition
    #   for these four (unlike STATUS's undocumented gap finding above), so
    #   it is noted here, not re-raised as a new finding.
    #
    #   61 of 66 unexercised literals (20+16+16+15 total literals, 4
    #   pre-existing claimed rows, 65 unexercised) get a row; 1 is
    #   structurally unreachable (see below). All phrases verified directly:
    #   `pre_classify_with_pattern_list(phrase)` returns the named list AND
    #   `PreClassifier._first_pattern_match(cleaned, PreClassifier.<LIST>)`
    #   cites the exact literal below (not an earlier sibling). No reword
    #   was needed — all 62 drafted phrases passed first try (checked
    #   same-list earlier-sibling shadowing and cross-list earlier-checked-list
    #   shadowing by hand before drafting, then confirmed empirically).
    #
    #   DISCOVERY_PATTERNS: 20 literals, 1 pre-existing claimed row
    #   ("are you able to set my default repo for me conversationally?" ->
    #   action:get_capabilities, via `\bwhat can you do\b`). 19 unexercised,
    #   all 19 reachable, all 19 get a row below.
    #
    #   ANALYSIS_PATTERNS: 16 literals, 1 pre-existing claimed row ("what's
    #   blocking the milestone?" -> action:analyze_blockers, via
    #   `\bwhat'?s blocking\b`). 15 unexercised, all 15 reachable, all 15 get
    #   a row below.
    #
    #   TRUST_PATTERNS: 16 literals, 1 pre-existing claimed row ("why can't
    #   you create issues?" -> action:explain_trust, via `\bwhy can'?t
    #   you\b`). 15 unexercised, all 15 reachable, all 15 get a row below.
    #
    #   MEMORY_PATTERNS: 15 literals, 1 pre-existing claimed row ("what do
    #   you remember about me?" -> action:get_memory, via `\bwhat do you
    #   remember\b`). 14 unexercised, 13 reachable (rows below), 1
    #   UNREACHABLE:
    #     `\bhow (much|far back) do you remember\b` — mathematically
    #       shadowed by its own earlier, shorter sibling `\bdo you
    #       remember\b` (list position 2, vs this literal's position 13):
    #       both of this literal's two alternatives ("how much do you
    #       remember" / "how far back do you remember") contain "do you
    #       remember" as a direct substring with intact word boundaries, so
    #       the shorter earlier pattern always claims first — the same
    #       structural shape as STATUS_PATTERNS' "my current work" vs
    #       "current work" above, not a phrasing-dependent shadow. Confirmed
    #       empirically with two independent phrasings ("how far back do you
    #       remember our chats", "how much do you remember about my
    #       preferences"), both claimed by `\bdo you remember\b`.
    #
    #   No `expected` corrections applied: none of these four lists carries
    #   in-corpus or in-code evidence (an already-MATCH-scored sibling row,
    #   or a documented-collision comment) pointing a specific literal at a
    #   different registered destination the way STATUS_PATTERNS' standup/
    #   portfolio literals did — correcting without such an anchor would be
    #   guessing. `expected` is `action:<name>` for every row below, the
    #   single hardcoded action the claim branch actually returns.
    #
    #   The gate reads these as UNSCORED (no router call has been made —
    #   this unit makes NO LLM calls per its dispatch) — NO-GO for all four
    #   lists is expected and correct after this deposit; the Lead's scoring
    #   pass resolves MATCH/REVIEW/MISMATCH.
    {
        "phrase": "what are your capabilities?",
        "category": "DISCOVERY",
        "expected": "action:get_capabilities",
        "source": 'phase3-conversion/DISCOVERY_PATTERNS literal r"\\bwhat are your capabilities\\b"',
    },
    {
        "phrase": "what services can you provide?",
        "category": "DISCOVERY",
        "expected": "action:get_capabilities",
        "source": 'phase3-conversion/DISCOVERY_PATTERNS literal r"\\bwhat services\\b"',
    },
    {
        "phrase": "what do you offer as an assistant?",
        "category": "DISCOVERY",
        "expected": "action:get_capabilities",
        "source": 'phase3-conversion/DISCOVERY_PATTERNS literal r"\\bwhat do you offer\\b"',
    },
    {
        "phrase": "what features does piper have?",
        "category": "DISCOVERY",
        "expected": "action:get_capabilities",
        "source": 'phase3-conversion/DISCOVERY_PATTERNS literal r"\\bwhat features\\b"',
    },
    {
        "phrase": "what can you help me do today?",
        "category": "DISCOVERY",
        "expected": "action:get_capabilities",
        "source": 'phase3-conversion/DISCOVERY_PATTERNS literal r"\\bwhat can you help\\b"',
    },
    {
        "phrase": "show me your capabilities",
        "category": "DISCOVERY",
        "expected": "action:get_capabilities",
        "source": 'phase3-conversion/DISCOVERY_PATTERNS literal r"\\bshow me your capabilities\\b"',
    },
    {
        "phrase": "give me a menu of services",
        "category": "DISCOVERY",
        "expected": "action:get_capabilities",
        "source": 'phase3-conversion/DISCOVERY_PATTERNS literal r"\\bmenu of services\\b"',
    },
    {
        "phrase": "can you list your capabilities",
        "category": "DISCOVERY",
        "expected": "action:get_capabilities",
        "source": 'phase3-conversion/DISCOVERY_PATTERNS literal r"\\blist.*capabilities\\b"',
    },
    {
        "phrase": "I want to understand your capabilities better",
        "category": "DISCOVERY",
        "expected": "action:get_capabilities",
        "source": 'phase3-conversion/DISCOVERY_PATTERNS literal r"\\byour capabilities\\b"',
    },
    {
        "phrase": "pull up the capability menu",
        "category": "DISCOVERY",
        "expected": "action:get_capabilities",
        "source": 'phase3-conversion/DISCOVERY_PATTERNS literal r"\\bcapability menu\\b"',
    },
    {
        "phrase": "open the capabilities menu",
        "category": "DISCOVERY",
        "expected": "action:get_capabilities",
        "source": 'phase3-conversion/DISCOVERY_PATTERNS literal r"\\bcapabilities menu\\b"',
    },
    {
        "phrase": "show me the menu",
        "category": "DISCOVERY",
        "expected": "action:get_capabilities",
        "source": 'phase3-conversion/DISCOVERY_PATTERNS literal r"\\bshow.*menu\\b"',
    },
    {
        "phrase": "what are you able to do for my project",
        "category": "DISCOVERY",
        "expected": "action:get_capabilities",
        "source": 'phase3-conversion/DISCOVERY_PATTERNS literal r"\\bwhat.*able to do\\b"',
    },
    {
        "phrase": "show me the features you offer",
        "category": "DISCOVERY",
        "expected": "action:get_capabilities",
        "source": 'phase3-conversion/DISCOVERY_PATTERNS literal r"\\bshow.*features\\b"',
    },
    {
        "phrase": "what's available in terms of features",
        "category": "DISCOVERY",
        "expected": "action:get_capabilities",
        "source": 'phase3-conversion/DISCOVERY_PATTERNS literal r"\\bavailable.*features\\b"',
    },
    {
        "phrase": "help",
        "category": "DISCOVERY",
        "expected": "action:get_capabilities",
        "source": 'phase3-conversion/DISCOVERY_PATTERNS literal r"^help$"',
    },
    {
        "phrase": "open the help menu",
        "category": "DISCOVERY",
        "expected": "action:get_capabilities",
        "source": 'phase3-conversion/DISCOVERY_PATTERNS literal r"\\bhelp\\s*menu\\b"',
    },
    {
        "phrase": "can you show help topics",
        "category": "DISCOVERY",
        "expected": "action:get_capabilities",
        "source": 'phase3-conversion/DISCOVERY_PATTERNS literal r"\\bshow\\s*help\\b"',
    },
    {
        "phrase": "I need help understanding something",
        "category": "DISCOVERY",
        "expected": "action:get_capabilities",
        "source": 'phase3-conversion/DISCOVERY_PATTERNS literal r"\\bneed\\s*help\\b"',
    },
    {
        "phrase": "what is blocking this release",
        "category": "ANALYSIS",
        "expected": "action:analyze_blockers",
        "source": 'phase3-conversion/ANALYSIS_PATTERNS literal r"\\bwhat is blocking\\b"',
    },
    {
        "phrase": "what tasks are blocking our sprint",
        "category": "ANALYSIS",
        "expected": "action:analyze_blockers",
        "source": 'phase3-conversion/ANALYSIS_PATTERNS literal r"\\bwhat.*block(?:s|ing|ed)\\s+(?:the|my|our)\\b"',
    },
    {
        "phrase": "blockers for the release",
        "category": "ANALYSIS",
        "expected": "action:analyze_blockers",
        "source": 'phase3-conversion/ANALYSIS_PATTERNS literal r"\\bblockers?\\s+(?:for|on|in)\\b"',
    },
    {
        "phrase": "what's the main obstacle here",
        "category": "ANALYSIS",
        "expected": "action:analyze_blockers",
        "source": 'phase3-conversion/ANALYSIS_PATTERNS literal r"\\bwhat.*obstacle\\b"',
    },
    {
        "phrase": "what's in the way of finishing this",
        "category": "ANALYSIS",
        "expected": "action:analyze_blockers",
        "source": 'phase3-conversion/ANALYSIS_PATTERNS literal r"\\bwhat\'?s in the way\\b"',
    },
    {
        "phrase": "let's analyze the risk here",
        "category": "ANALYSIS",
        "expected": "action:analyze_blockers",
        "source": 'phase3-conversion/ANALYSIS_PATTERNS literal r"\\banalyze.*(?:risk|impact|blocker|bottleneck)\\b"',
    },
    {
        "phrase": "I'd like a risk assessment for this project",
        "category": "ANALYSIS",
        "expected": "action:analyze_blockers",
        "source": 'phase3-conversion/ANALYSIS_PATTERNS literal r"\\brisk assessment\\b"',
    },
    {
        "phrase": "can you run an impact analysis on this change",
        "category": "ANALYSIS",
        "expected": "action:analyze_blockers",
        "source": 'phase3-conversion/ANALYSIS_PATTERNS literal r"\\bimpact analysis\\b"',
    },
    {
        "phrase": "is there a bottleneck analysis available",
        "category": "ANALYSIS",
        "expected": "action:analyze_blockers",
        "source": 'phase3-conversion/ANALYSIS_PATTERNS literal r"\\bbottleneck.*(?:analysis|report)\\b"',
    },
    {
        "phrase": "what risks does this project have",
        "category": "ANALYSIS",
        "expected": "action:analyze_blockers",
        "source": 'phase3-conversion/ANALYSIS_PATTERNS literal r"\\bwhat risks\\b"',
    },
    {
        "phrase": "what risk do we have in this plan",
        "category": "ANALYSIS",
        "expected": "action:analyze_blockers",
        "source": 'phase3-conversion/ANALYSIS_PATTERNS literal r"\\bwhat.*risk(?:s)?\\s+(?:should|do|are)\\b"',
    },
    {
        "phrase": "please identify the risks in this plan",
        "category": "ANALYSIS",
        "expected": "action:analyze_blockers",
        "source": 'phase3-conversion/ANALYSIS_PATTERNS literal r"\\bidentify.*risks?\\b"',
    },
    {
        "phrase": "risks we should flag before launch",
        "category": "ANALYSIS",
        "expected": "action:analyze_blockers",
        "source": 'phase3-conversion/ANALYSIS_PATTERNS literal r"\\brisk(?:s)?\\s+(?:i|we)\\s+should\\b"',
    },
    {
        "phrase": "threats to our timeline this week",
        "category": "ANALYSIS",
        "expected": "action:analyze_blockers",
        "source": 'phase3-conversion/ANALYSIS_PATTERNS literal r"\\bthreats?\\s+(?:to|should|i)\\b"',
    },
    {
        "phrase": "what could threaten this deadline",
        "category": "ANALYSIS",
        "expected": "action:analyze_blockers",
        "source": 'phase3-conversion/ANALYSIS_PATTERNS literal r"\\bwhat.*threaten\\b"',
    },
    {
        "phrase": "why won't you create issues for me",
        "category": "TRUST",
        "expected": "action:explain_trust",
        "source": 'phase3-conversion/TRUST_PATTERNS literal r"\\bwhy won\'?t you\\b"',
    },
    {
        "phrase": "why don't you just do it yourself",
        "category": "TRUST",
        "expected": "action:explain_trust",
        "source": 'phase3-conversion/TRUST_PATTERNS literal r"\\bwhy don\'?t you\\b"',
    },
    {
        "phrase": "why are you always cautious about this suggestion",
        "category": "TRUST",
        "expected": "action:explain_trust",
        "source": 'phase3-conversion/TRUST_PATTERNS literal r"\\bwhy (are|do) you (so|being so|always) (cautious|careful|conservative)\\b"',
    },
    {
        "phrase": "what can't you do here",
        "category": "TRUST",
        "expected": "action:explain_trust",
        "source": 'phase3-conversion/TRUST_PATTERNS literal r"\\bwhat can\'?t you do\\b"',
    },
    {
        "phrase": "what are your limits as an assistant",
        "category": "TRUST",
        "expected": "action:explain_trust",
        "source": 'phase3-conversion/TRUST_PATTERNS literal r"\\bwhat are your limits\\b"',
    },
    {
        "phrase": "what's the capability boundary here",
        "category": "TRUST",
        "expected": "action:explain_trust",
        "source": 'phase3-conversion/TRUST_PATTERNS literal r"\\bcapability (boundary|boundaries|limits)\\b"',
    },
    {
        "phrase": "how well do you know me by now",
        "category": "TRUST",
        "expected": "action:explain_trust",
        "source": 'phase3-conversion/TRUST_PATTERNS literal r"\\bhow (well )?do you know me\\b"',
    },
    {
        "phrase": "do you trust me with this decision",
        "category": "TRUST",
        "expected": "action:explain_trust",
        "source": 'phase3-conversion/TRUST_PATTERNS literal r"\\bdo you trust me\\b"',
    },
    {
        "phrase": "how much do you trust my judgment",
        "category": "TRUST",
        "expected": "action:explain_trust",
        "source": 'phase3-conversion/TRUST_PATTERNS literal r"\\bhow much do you trust\\b"',
    },
    {
        "phrase": "what's our relationship like these days",
        "category": "TRUST",
        "expected": "action:explain_trust",
        "source": 'phase3-conversion/TRUST_PATTERNS literal r"\\bwhat\'?s our relationship\\b"',
    },
    {
        "phrase": "how do you see our relationship evolving",
        "category": "TRUST",
        "expected": "action:explain_trust",
        "source": 'phase3-conversion/TRUST_PATTERNS literal r"\\bhow do you see our relationship\\b"',
    },
    {
        "phrase": "how do we work together on this project",
        "category": "TRUST",
        "expected": "action:explain_trust",
        "source": 'phase3-conversion/TRUST_PATTERNS literal r"\\bhow do (we|you and i) work together\\b"',
    },
    {
        "phrase": "why did you go ahead without asking",
        "category": "TRUST",
        "expected": "action:explain_trust",
        "source": 'phase3-conversion/TRUST_PATTERNS literal r"\\bwhy did you (do|just|go ahead)\\b"',
    },
    {
        "phrase": "why do you always ask me the same thing",
        "category": "TRUST",
        "expected": "action:explain_trust",
        "source": 'phase3-conversion/TRUST_PATTERNS literal r"\\bwhy do you (always|keep)\\b"',
    },
    {
        "phrase": "i didn't ask you to do that",
        "category": "TRUST",
        "expected": "action:explain_trust",
        "source": 'phase3-conversion/TRUST_PATTERNS literal r"\\bi didn\'?t (ask|tell) you to\\b"',
    },
    {
        "phrase": "what can you remember about our last conversation",
        "category": "MEMORY",
        "expected": "action:get_memory",
        "source": 'phase3-conversion/MEMORY_PATTERNS literal r"\\bwhat can you remember\\b"',
    },
    {
        "phrase": "do you remember my last project update",
        "category": "MEMORY",
        "expected": "action:get_memory",
        "source": 'phase3-conversion/MEMORY_PATTERNS literal r"\\bdo you remember\\b"',
    },
    {
        "phrase": "remember when we shipped the last release?",
        "category": "MEMORY",
        "expected": "action:get_memory",
        "source": 'phase3-conversion/MEMORY_PATTERNS literal r"\\bremember (when|that|our|my)\\b"',
    },
    {
        "phrase": "can you show my conversation history",
        "category": "MEMORY",
        "expected": "action:get_memory",
        "source": 'phase3-conversion/MEMORY_PATTERNS literal r"\\b(show|view|see) (my |our )?(conversation )?history\\b"',
    },
    {
        "phrase": "our history together has been good",
        "category": "MEMORY",
        "expected": "action:get_memory",
        "source": 'phase3-conversion/MEMORY_PATTERNS literal r"\\b(my|our) (conversation )?history\\b"',
    },
    {
        "phrase": "let's look at past conversations we've had",
        "category": "MEMORY",
        "expected": "action:get_memory",
        "source": 'phase3-conversion/MEMORY_PATTERNS literal r"\\bpast conversations?\\b"',
    },
    {
        "phrase": "pull up my previous messages please",
        "category": "MEMORY",
        "expected": "action:get_memory",
        "source": 'phase3-conversion/MEMORY_PATTERNS literal r"\\bprevious (conversations?|chats?|messages?)\\b"',
    },
    {
        "phrase": "can I see the conversation log",
        "category": "MEMORY",
        "expected": "action:get_memory",
        "source": 'phase3-conversion/MEMORY_PATTERNS literal r"\\bconversation log\\b"',
    },
    {
        "phrase": "find when I mentioned this bug before",
        "category": "MEMORY",
        "expected": "action:get_memory",
        "source": 'phase3-conversion/MEMORY_PATTERNS literal r"\\bfind (when|where) (i|we)\\b"',
    },
    {
        "phrase": "search history for that conversation topic",
        "category": "MEMORY",
        "expected": "action:get_memory",
        "source": 'phase3-conversion/MEMORY_PATTERNS literal r"\\bsearch (my |our )?(conversation )?history\\b"',
    },
    {
        "phrase": "what did we discuss in our last session",
        "category": "MEMORY",
        "expected": "action:get_memory",
        "source": 'phase3-conversion/MEMORY_PATTERNS literal r"\\bwhat (did|have) (i|we) (talk|discuss|say)\\b"',
    },
    {
        "phrase": "what we discussed yesterday was helpful",
        "category": "MEMORY",
        "expected": "action:get_memory",
        "source": 'phase3-conversion/MEMORY_PATTERNS literal r"\\bwhat (i|we) (said|talked|discussed)\\b"',
    },
    {
        "phrase": "how long is your memory exactly",
        "category": "MEMORY",
        "expected": "action:get_memory",
        "source": 'phase3-conversion/MEMORY_PATTERNS literal r"\\bhow long (is|do) (your|my) memory\\b"',
    },
    # REPO_MANAGEMENT_PATTERNS (#1595 Phase 3, 2026-10-03): 10 of 12 literals were
    # unexercised (2 already claimed: "link mediajunkie/test-piper-morgan to the
    # project" -> MATCH, "add a repo to my portfolio" -> REVIEW). All 10 new rows
    # get expected: action:manage_repos — the single hardcoded action for the
    # whole list (pre_classifier.py:1420-1427, checked before PORTFOLIO/GUIDANCE/
    # INTEGRATION_CONNECT). Investigated the dispatcher's named ambiguity
    # ("connect my repo to X": manage_repos vs an INTEGRATION_CONNECT/github
    # connect flow) directly in code and found it RESOLVED, not ambiguous:
    # INTEGRATION_CONNECT_BLOCKERS (pre_classifier.py:862-868) explicitly names
    # the repo-word/owner-repo-slug guard ("the repo-link lane (#862 handles it
    # earlier in the pass) — never integration setup", Arch-ratified #1417), and
    # on the single-intent path REPO_MANAGEMENT_PATTERNS is checked at line 1420,
    # well before INTEGRATION_CONNECT_PATTERNS at line 1835 — so a repo-bearing
    # phrase never reaches the integration-connect branch at all. The existing
    # REVIEW anchor ("add a repo to my portfolio", probe-row-7) traces to a
    # DIFFERENT disagreement (the live router once proposed a non-canonical
    # `execution/add_repo_to_portfolio`, not GUIDANCE/get_contextual_guidance —
    # see surface1-counterfactual-results-2026-08-08.md row 7) and recent
    # re-probes (2026-09-25 through 2026-10-02) all show the router AGREEING at
    # manage_repos@0.9-0.95 for that same phrase — so generalizing that anchor's
    # REVIEW to these 10 literals would not be evidence-backed. No row deposited
    # with expected: REVIEW; all 10 use the confident action.
    {
        "phrase": "link my repository to the project",
        "category": "PORTFOLIO",
        "expected": "action:manage_repos",
        "source": 'phase3-conversion/REPO_MANAGEMENT_PATTERNS literal r"\\blink\\s+(?:(?:my|the|a)\\s+)?(?:repo(?:sitory)?)\\s+(?:to\\s+)"',
    },
    {
        "phrase": "connect my repository to the project",
        "category": "PORTFOLIO",
        "expected": "action:manage_repos",
        "source": 'phase3-conversion/REPO_MANAGEMENT_PATTERNS literal r"\\bconnect\\s+(?:(?:my|the|a)\\s+)?(?:repo(?:sitory)?)\\s+(?:to\\s+)"',
        "notes": (
            "dispatcher-named ambiguity check (manage_repos vs INTEGRATION_CONNECT) "
            "investigated and resolved NOT ambiguous: INTEGRATION_CONNECT_BLOCKERS "
            "(pre_classifier.py:862-868) blocks repo-word phrases from the "
            "integration-connect lane, and REPO_MANAGEMENT_PATTERNS is checked "
            "earlier (line 1420) than INTEGRATION_CONNECT_PATTERNS (line 1835) on "
            "the single-intent path regardless."
        ),
    },
    {
        "phrase": "connect octocat/hello-world to the project",
        "category": "PORTFOLIO",
        "expected": "action:manage_repos",
        "source": 'phase3-conversion/REPO_MANAGEMENT_PATTERNS literal r"\\bconnect\\s+[\\w.-]+/[\\w.-]+"',
    },
    {
        "phrase": "add octocat/hello-world to the project",
        "category": "PORTFOLIO",
        "expected": "action:manage_repos",
        "source": 'phase3-conversion/REPO_MANAGEMENT_PATTERNS literal r"\\badd\\s+[\\w.-]+/[\\w.-]+\\s+to\\s+"',
    },
    {
        "phrase": "please unlink my repository from this project",
        "category": "PORTFOLIO",
        "expected": "action:unlink_repo",
        "source": 'phase3-conversion/REPO_UNLINK_PATTERNS literal r"\\bunlink\\s+(?:(?:my|the|a)\\s+)?(?:repo(?:sitory)?)"',
        "notes": (
            "RE-POINTED 2026-10-04 (Arch's ruling §1, applied by Lead's "
            "dispatched unit): was action:manage_repos. This literal moved "
            "out of REPO_MANAGEMENT_PATTERNS into its own REPO_UNLINK_PATTERNS "
            "list, claimed as unlink_repo (PORTFOLIO) and checked before "
            "REPO_MANAGEMENT_PATTERNS in both claim tables — a pure claim "
            "re-point, not a new pattern. The turn now reaches "
            "_dispatch_action_rail's DESTRUCTIVE block (the unlink_repo rail "
            "entry, already #1190-gated via "
            "destructive_confirm.build_unlink_repo_confirmation) instead of "
            "the manage_repos canonical branch, which executed unconfirmed. "
            "WRITE/DESTRUCTIVE op (removes a project<->repo link)."
        ),
    },
    {
        "phrase": "please remove my repository from this project",
        "category": "PORTFOLIO",
        "expected": "action:unlink_repo",
        "source": 'phase3-conversion/REPO_UNLINK_PATTERNS literal r"\\bremove\\s+(?:(?:my|the|a)\\s+)?(?:repo(?:sitory)?)\\s+from\\s+"',
        "notes": "RE-POINTED 2026-10-04 (Arch's ruling §1): was action:manage_repos — see the sibling 'unlink' row's note for the full rationale.",
    },
    {
        "phrase": "please disconnect my repository from this project",
        "category": "PORTFOLIO",
        "expected": "action:unlink_repo",
        "source": 'phase3-conversion/REPO_UNLINK_PATTERNS literal r"\\bdisconnect\\s+(?:(?:my|the|a)\\s+)?(?:repo(?:sitory)?)"',
        "notes": "RE-POINTED 2026-10-04 (Arch's ruling §1): was action:manage_repos — see the sibling 'unlink' row's note for the full rationale.",
    },
    {
        "phrase": "please show my linked repos",
        "category": "PORTFOLIO",
        "expected": "action:manage_repos",
        "source": 'phase3-conversion/REPO_MANAGEMENT_PATTERNS literal r"\\b(?:show|list|view|which)\\s+(?:(?:my|the)\\s+)?(?:linked\\s+)?repos\\b"',
    },
    {
        "phrase": "which repo connected to this project should i check",
        "category": "PORTFOLIO",
        "expected": "action:manage_repos",
        "source": 'phase3-conversion/REPO_MANAGEMENT_PATTERNS literal r"\\bwhich\\s+repos?\\s+(?:are\\s+)?(?:linked|connected)\\b"',
        "notes": (
            "singular 'repo' with direct 'connected' adjacency (no 'is'/'are') — "
            "the only reachable phrasing: plural 'which repos ... linked/connected' "
            "is always shadowed by the earlier list-literal "
            'r"\\b(?:show|list|view|which)\\s+(?:(?:my|the)\\s+)?(?:linked\\s+)?repos\\b" '
            "(which also accepts the 'which' verb), and 'which repo is "
            "linked/connected' does not match this literal's regex at all "
            "('is' is not in its (?:are\\s+)? alternation)."
        ),
    },
    {
        "phrase": "can you show project repositories for this account",
        "category": "PORTFOLIO",
        "expected": "action:manage_repos",
        "source": 'phase3-conversion/REPO_MANAGEMENT_PATTERNS literal r"\\bshow\\s+(?:project\\s+)?repositories\\b"',
    },
    # 2026-10-05 (Lead, per CXO's rule-cxo-to-lead-cc-arch-list-repos-not-found-
    # keeps-the-lookup-answer-with-all-your-repos-corpus-rows-too memo §1a):
    # the two phrasings that triggered the list_repos not-found misread
    # ("github"/"repos" read as a project name). expected: action:list_repos
    # is the GROUND-TRUTH resolved action (the canonical handler's LIST
    # branch — and the new read_portfolio rail entry calling it directly —
    # both return intent.action "list_repos"; "manage_repos" is only
    # surface-1's legacy unsplit literal-claim name, per
    # _handle_list_repos's own docstring and the REPO_UNLINK_PATTERNS
    # precedent above, which already claims its split action directly).
    {
        "phrase": "list my repos on github",
        "category": "PORTFOLIO",
        "expected": "action:list_repos",
        "source": (
            'phase3-conversion/REPO_MANAGEMENT_PATTERNS literal r"\\b(?:show|list|view|which)'
            '\\s+(?:(?:my|the)\\s+)?(?:linked\\s+)?repos\\b" — verified via '
            "PreClassifier.pre_classify_with_pattern_list('list my repos on github') "
            "-> (manage_repos, REPO_MANAGEMENT_PATTERNS); the trailing 'on github' is "
            "unanchored and misread as a project-name clause downstream, which is the "
            "bug this row exists to pin against (see #list-repos-notfound memo)."
        ),
    },
    {
        "phrase": "show all of my repos",
        "category": "PORTFOLIO",
        "expected": "action:list_repos",
        "source": (
            "phase3-conversion/REPO_MANAGEMENT_PATTERNS — NOT claimed by surface 1: "
            "PreClassifier.pre_classify_with_pattern_list('show all of my repos') "
            "-> (None, None). No REPO_MANAGEMENT_PATTERNS literal matches ('show' is not "
            "immediately followed by 'repos'/'my repos'/'the repos' — 'all of' breaks the "
            "adjacency the list literal requires), so this phrase currently falls through "
            "to the floor rather than reaching the list handler at all. Deposited anyway "
            "(ground-truth expectation is list_repos) per CXO's §1a instruction; closing "
            "this gap is future narrowing work, not this row's job."
        ),
    },
    # #1595 Phase 3 (2026-10-03): six more GO-but-unexercised *_PATTERNS lists.
    # CONTEXTUAL_QUERY_PATTERNS (13 literals / 2 rows), GET_DEFAULT_REPO_PATTERNS
    # (5/2), INSIGHT_PULL_PATTERNS (7/2), LOCAL_GIT_STATUS_PATTERNS (12/1),
    # PRODUCTIVITY_QUERY_PATTERNS (4/1), SESSION_ACTIVITY_QUERY_PATTERNS (6/1).
    # Every list is single-action (or, for CONTEXTUAL_QUERY, a two-way split
    # resolved by the SAME explicit if/any() sub-check `pre_classify_with_
    # pattern_list` runs at the claim site, lines ~1465-1479) — no per-literal
    # branching beyond that. All five QUERY-category actions (changes_query,
    # attention_query, get_default_repo, local_git_status_query,
    # productivity_query, session_activity_query) are WORKFLOW-disposition,
    # rail-registered WorkflowEntry's with a flip_group inside the dispatched
    # --live set (read_temporal / read_status / read_referent) — LIVE rail ops.
    # pull_insights (INSIGHT_PULL_PATTERNS, category MEMORY) is FLOOR
    # disposition with NO WorkflowEntry at all (grep-confirmed against
    # workflow_entries.py) — the one NON-LIVE op in this unit, same shape as
    # the 10-02 DISCOVERY/ANALYSIS/TRUST/MEMORY lane's four floor lists.
    # Investigated (not generalized from) the existing REVIEW anchors for
    # LOCAL_GIT_STATUS/PRODUCTIVITY/SESSION_ACTIVITY ("what branch are we
    # on?" / "what's my productivity?" / "what did we create this session?"):
    # each carries a historical DISAGREE probe-row tag in the corpus, but the
    # CURRENT gate run (quoted in the lane log) reads REVIEW-agrees for all
    # three at router confidence 1.0 — the same "anchor's own later evidence
    # leans AGREE" shape the REPO_MANAGEMENT lane found for its own REVIEW
    # anchor, and the corpus already carries separately-ruled action: rows
    # for changes_query/session_activity_query elsewhere (CXO/PPM rulings,
    # "beyond Arch's four named buckets") confirming the live-agreement
    # reasoning generalizes. No REVIEW rows deposited; all 40 new rows use
    # the list's own confident action, each independently verified via
    # PreClassifier.pre_classify_with_pattern_list + _first_pattern_match
    # against the real production matcher.
    {
        "phrase": "what's changed since last week",
        "category": "QUERY",
        "expected": "action:changes_query",
        "source": 'phase3-conversion/CONTEXTUAL_QUERY_PATTERNS literal r"\\bwhat\'?s changed since\\b"',
    },
    {
        "phrase": "show me the changes since last monday",
        "category": "QUERY",
        "expected": "action:changes_query",
        "source": 'phase3-conversion/CONTEXTUAL_QUERY_PATTERNS literal r"\\bshow.*changes since\\b"',
    },
    {
        "phrase": "show me everything that's changed",
        "category": "QUERY",
        "expected": "action:changes_query",
        "source": 'phase3-conversion/CONTEXTUAL_QUERY_PATTERNS literal r"\\bshow me.*changed\\b"',
    },
    {
        "phrase": "any changes since the last deploy",
        "category": "QUERY",
        "expected": "action:changes_query",
        "source": 'phase3-conversion/CONTEXTUAL_QUERY_PATTERNS literal r"\\bchanges since\\b"',
    },
    {
        "phrase": "give me the activity since yesterday's standup",
        "category": "QUERY",
        "expected": "action:changes_query",
        "source": 'phase3-conversion/CONTEXTUAL_QUERY_PATTERNS literal r"\\bactivity since\\b"',
    },
    {
        "phrase": "any updates since this morning",
        "category": "QUERY",
        "expected": "action:changes_query",
        "source": 'phase3-conversion/CONTEXTUAL_QUERY_PATTERNS literal r"\\bupdates since\\b"',
    },
    {
        "phrase": "what needs attention right now",
        "category": "QUERY",
        "expected": "action:attention_query",
        "source": 'phase3-conversion/CONTEXTUAL_QUERY_PATTERNS literal r"\\bwhat needs attention\\b"',
    },
    {
        "phrase": "this project needs my attention today",
        "category": "QUERY",
        "expected": "action:attention_query",
        "source": 'phase3-conversion/CONTEXTUAL_QUERY_PATTERNS literal r"\\bneeds my attention\\b"',
    },
    {
        "phrase": "show me what needs the most attention",
        "category": "QUERY",
        "expected": "action:attention_query",
        "source": 'phase3-conversion/CONTEXTUAL_QUERY_PATTERNS literal r"\\bshow.*needs.*attention\\b"',
    },
    {
        "phrase": "the items that need attention haven't been touched",
        "category": "QUERY",
        "expected": "action:attention_query",
        "source": 'phase3-conversion/CONTEXTUAL_QUERY_PATTERNS literal r"\\bitems.*need.*attention\\b"',
    },
    {
        "phrase": "please list the attention items for review",
        "category": "QUERY",
        "expected": "action:attention_query",
        "source": 'phase3-conversion/CONTEXTUAL_QUERY_PATTERNS literal r"\\battention items\\b"',
    },
    # GET_DEFAULT_REPO_PATTERNS: literal r"\bwhat\s+default\s+repo(?:sitory)?\b"
    # is MATHEMATICALLY SHADOWED by its own earlier sibling
    # r"\bwhat(?:'s|\s+is)?\s+(?:my\s+)?default\s+repo(?:sitory)?\b" (the
    # claimed literal) for EVERY possible phrase: that earlier pattern's
    # "'s"/"is"/"my" groups are all optional, so "what" + whitespace +
    # "default" + whitespace + "repo(sitory)?" with nothing else in between
    # — exactly what the later literal requires — already satisfies the
    # earlier one. Confirmed empirically with three independent phrasings
    # ("what default repo do you have on file", "what default repo should i
    # use", "what default repository is configured", "what default repo"
    # bare) — all four claimed by the earlier sibling, never this literal.
    # No row deposited for this literal; same structural shape as MEMORY_
    # PATTERNS' "how (much|far back) do you remember" self-shadow (10-02 lane).
    {
        "phrase": "which repository is my default",
        "category": "QUERY",
        "expected": "action:get_default_repo",
        "source": (
            'phase3-conversion/GET_DEFAULT_REPO_PATTERNS literal r"\\bwhich\\s+'
            '(?:repo(?:sitory)?\\s+)?is\\s+(?:my\\s+)?default(?:\\s+repo(?:sitory)?)?\\b"'
        ),
    },
    {
        "phrase": "please show my default repository",
        "category": "QUERY",
        "expected": "action:get_default_repo",
        "source": (
            'phase3-conversion/GET_DEFAULT_REPO_PATTERNS literal r"\\b(?:show|see|'
            'tell\\s+me|get)\\s+(?:my\\s+)?default\\s+repo(?:sitory)?\\b"'
        ),
    },
    {
        "phrase": "my default repository",
        "category": "QUERY",
        "expected": "action:get_default_repo",
        "source": (
            "phase3-conversion/GET_DEFAULT_REPO_PATTERNS literal "
            'r"^(?:my\\s+)?default\\s+repo(?:sitory)?\\??$"'
        ),
    },
    {
        "phrase": "what do you know about my work habits",
        "category": "MEMORY",
        "expected": "action:pull_insights",
        "source": 'phase3-conversion/INSIGHT_PULL_PATTERNS literal r"\\bwhat do you know about (me|my |our |the )"',
        "notes": "NON-LIVE op — pull_insights is FLOOR disposition, no WorkflowEntry (grep-confirmed)",
    },
    {
        "phrase": "tell me what you've learned about my habits",
        "category": "MEMORY",
        "expected": "action:pull_insights",
        "source": 'phase3-conversion/INSIGHT_PULL_PATTERNS literal r"\\btell me what you(\'ve| have) learned\\b"',
        "notes": "NON-LIVE op — pull_insights is FLOOR disposition, no WorkflowEntry (grep-confirmed)",
    },
    {
        "phrase": "what insights do you have about my productivity",
        "category": "MEMORY",
        "expected": "action:pull_insights",
        "source": 'phase3-conversion/INSIGHT_PULL_PATTERNS literal r"\\bwhat insights do you have\\b"',
        "notes": "NON-LIVE op — pull_insights is FLOOR disposition, no WorkflowEntry (grep-confirmed)",
    },
    {
        "phrase": "show me what you've learned about my preferences",
        "category": "MEMORY",
        "expected": "action:pull_insights",
        "source": 'phase3-conversion/INSIGHT_PULL_PATTERNS literal r"\\bshow me what you(\'ve| have) learned\\b"',
        "notes": "NON-LIVE op — pull_insights is FLOOR disposition, no WorkflowEntry (grep-confirmed)",
    },
    {
        "phrase": "what patterns have you noticed in my work",
        "category": "MEMORY",
        "expected": "action:pull_insights",
        "source": (
            'phase3-conversion/INSIGHT_PULL_PATTERNS literal r"\\bwhat patterns have you '
            '(noticed|observed|found|seen)\\b"'
        ),
        "notes": "NON-LIVE op — pull_insights is FLOOR disposition, no WorkflowEntry (grep-confirmed)",
    },
    {
        "phrase": "what have you noticed about my habits lately",
        "category": "MEMORY",
        "expected": "action:pull_insights",
        "source": 'phase3-conversion/INSIGHT_PULL_PATTERNS literal r"\\bwhat have you noticed about (me|my |our |the )"',
        "notes": "NON-LIVE op — pull_insights is FLOOR disposition, no WorkflowEntry (grep-confirmed)",
    },
    {
        "phrase": "what branch am i on right now",
        "category": "QUERY",
        "expected": "action:local_git_status_query",
        "source": 'phase3-conversion/LOCAL_GIT_STATUS_PATTERNS literal r"\\bwhat branch am i on\\b"',
    },
    {
        "phrase": "which branch are we on at the moment",
        "category": "QUERY",
        "expected": "action:local_git_status_query",
        "source": 'phase3-conversion/LOCAL_GIT_STATUS_PATTERNS literal r"\\bwhich branch are we on\\b"',
    },
    {
        "phrase": "can you tell me the current branch",
        "category": "QUERY",
        "expected": "action:local_git_status_query",
        "source": 'phase3-conversion/LOCAL_GIT_STATUS_PATTERNS literal r"\\bcurrent branch\\b"',
    },
    {
        "phrase": "what's the working tree status",
        "category": "QUERY",
        "expected": "action:local_git_status_query",
        "source": 'phase3-conversion/LOCAL_GIT_STATUS_PATTERNS literal r"\\bworking tree (?:clean|dirty|status)\\b"',
    },
    {
        "phrase": "are there any uncommitted changes",
        "category": "QUERY",
        "expected": "action:local_git_status_query",
        "source": 'phase3-conversion/LOCAL_GIT_STATUS_PATTERNS literal r"\\buncommitted changes?\\b"',
    },
    {
        "phrase": "do we have a dirty working tree",
        "category": "QUERY",
        "expected": "action:local_git_status_query",
        "source": 'phase3-conversion/LOCAL_GIT_STATUS_PATTERNS literal r"\\bdirty (?:working )?tree\\b"',
    },
    {
        "phrase": "are we ahead of origin right now",
        "category": "QUERY",
        "expected": "action:local_git_status_query",
        "source": (
            'phase3-conversion/LOCAL_GIT_STATUS_PATTERNS literal r"\\bahead of '
            '(?:main|origin|upstream|master)\\b"'
        ),
    },
    {
        "phrase": "are we behind upstream at all",
        "category": "QUERY",
        "expected": "action:local_git_status_query",
        "source": (
            'phase3-conversion/LOCAL_GIT_STATUS_PATTERNS literal r"\\bbehind '
            '(?:main|origin|upstream|master)\\b"'
        ),
    },
    {
        "phrase": "do we have any unpushed commits",
        "category": "QUERY",
        "expected": "action:local_git_status_query",
        "source": 'phase3-conversion/LOCAL_GIT_STATUS_PATTERNS literal r"\\bunpushed commits?\\b"',
    },
    {
        "phrase": "can you show the local git status",
        "category": "QUERY",
        "expected": "action:local_git_status_query",
        "source": 'phase3-conversion/LOCAL_GIT_STATUS_PATTERNS literal r"\\blocal git status\\b"',
        "notes": (
            "checked before its own sibling literal r'\\bgit status\\b': 'local git "
            "status' contains 'git status' as a substring, but this literal is earlier "
            "in the list so it claims first — _first_pattern_match confirmed"
        ),
    },
    {
        "phrase": "please run git status for me",
        "category": "QUERY",
        "expected": "action:local_git_status_query",
        "source": 'phase3-conversion/LOCAL_GIT_STATUS_PATTERNS literal r"\\bgit status\\b"',
        "notes": "phrased without 'local' preceding 'git status' so the earlier sibling literal doesn't claim it first",
    },
    {
        "phrase": "show me my productivity report",
        "category": "QUERY",
        "expected": "action:productivity_query",
        "source": 'phase3-conversion/PRODUCTIVITY_QUERY_PATTERNS literal r"\\bshow.*productivity\\b"',
    },
    {
        "phrase": "can you share my productivity metrics",
        "category": "QUERY",
        "expected": "action:productivity_query",
        "source": 'phase3-conversion/PRODUCTIVITY_QUERY_PATTERNS literal r"\\bproductivity metrics\\b"',
    },
    {
        "phrase": "i'd like to check my productivity this week",
        "category": "QUERY",
        "expected": "action:productivity_query",
        "source": 'phase3-conversion/PRODUCTIVITY_QUERY_PATTERNS literal r"\\bmy productivity\\b"',
    },
    {
        "phrase": "what have we created so far",
        "category": "QUERY",
        "expected": "action:session_activity_query",
        "source": 'phase3-conversion/SESSION_ACTIVITY_QUERY_PATTERNS literal r"\\bwhat have we created\\b"',
    },
    {
        "phrase": "what did we make earlier",
        "category": "QUERY",
        "expected": "action:session_activity_query",
        "source": 'phase3-conversion/SESSION_ACTIVITY_QUERY_PATTERNS literal r"\\bwhat did we make\\b"',
    },
    {
        "phrase": "what did i create this session",
        "category": "QUERY",
        "expected": "action:session_activity_query",
        "source": (
            'phase3-conversion/SESSION_ACTIVITY_QUERY_PATTERNS literal r"\\bwhat did '
            '(?:we|i) create this session\\b"'
        ),
        "notes": (
            "the only reachable phrasing for this literal: the 'we' variant ('what did "
            "we create this session') is always claimed first by the earlier sibling "
            'r"\\bwhat did we create\\b" (a strict prefix match, confirmed via '
            "_first_pattern_match); the 'i' variant has no such earlier-sibling prefix "
            "and reaches this literal cleanly"
        ),
    },
    {
        "phrase": "what did we do this session",
        "category": "QUERY",
        "expected": "action:session_activity_query",
        "source": 'phase3-conversion/SESSION_ACTIVITY_QUERY_PATTERNS literal r"\\bwhat did we do this session\\b"',
    },
    {
        "phrase": "what issues did we open during the call",
        "category": "QUERY",
        "expected": "action:session_activity_query",
        "source": (
            'phase3-conversion/SESSION_ACTIVITY_QUERY_PATTERNS literal r"\\bwhat '
            '(?:issues|items) did we (?:create|make|open)\\b"'
        ),
    },
]


def parse_1283() -> list:
    """Rows from routing_corpus_1283.yaml (phrase, expected, optional seam)."""
    rows, cur = [], {}
    for raw in CORPUS_1283.read_text().splitlines():
        line = raw.split("#", 1)[0].rstrip()
        m = re.match(r'\s*- phrase: "(.*)"', line)
        if m:
            if cur.get("phrase"):
                rows.append(cur)
            cur = {"phrase": m.group(1)}
            continue
        m = re.match(r"\s*expected: (\S+)", line)
        if m and cur is not None:
            cur["expected"] = m.group(1)
    if cur.get("phrase"):
        rows.append(cur)
    return rows


def parse_probe() -> list:
    """Rows from the surface-1 counterfactual results table."""
    rows = []
    for line in PROBE_RESULTS.read_text().splitlines():
        m = re.match(
            r"\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*`([^`]+)`\s*\|.*\|\s*(AGREE|DISAGREE|VARIANT)",
            line,
        )
        if not m:
            continue
        idx, phrase, claim, verdict = m.groups()
        cat, action = claim.split("/", 1)
        rows.append(
            {
                "phrase": phrase,
                "surface1_claim": claim,
                "probe_verdict": verdict,
                "probe_row": int(idx),
                "claim_category": cat.upper(),
                "claim_action": action,
            }
        )
    return rows


def bucket(expected: str, fallback: str = "QUERY") -> str:
    if expected.startswith("category:"):
        return expected.split(":", 1)[1].upper()
    if expected.startswith("action:"):
        return _ACTION_CATEGORY.get(expected.split(":", 1)[1], fallback)
    return fallback


# Destination rulings that apply to rows carried in from a STRUCTURED source
# (corpus-1283 / probe rows), whose expectation is not editable in place (the
# fixture file is shared with its own tests). Applied in main() after the merge,
# with the ruling cited; the original source citation is kept on the row.
RULED_EXPECTATIONS: dict = {
    "threats to our timeline this week": (
        "action:analyze_blockers",
        "RULED 2026-10-03 (CXO reversing C1 after the router's 3/3): a PROJECT-level risk question is analyze_blockers; attention_query is the PERSONAL aggregate",
    ),
    # PPM 2026-10-02 (evening) — 7 of 13 four-small-list disagreements concur with the router; 6 dissent and stay.
    "what can't you do here": (
        "action:get_capabilities",
        "RULED 2026-10-02 (PPM): was action:explain_trust — a limits/boundary question is the negative framing of 'what can you do'",
    ),
    "what are your limits as an assistant": (
        "action:get_capabilities",
        "RULED 2026-10-02 (PPM): was action:explain_trust — capability question",
    ),
    "what's the capability boundary here": (
        "action:get_capabilities",
        "RULED 2026-10-02 (PPM): was action:explain_trust — capability question",
    ),
    "why are you always cautious about this suggestion": (
        "action:explain_suggestion",
        "RULED 2026-10-02 (PPM): was action:explain_trust — PROVENANCE's own 'explain why the assistant made a prior suggestion'",
    ),
    "how well do you know me by now": (
        "action:pull_insights",
        "RULED 2026-10-02 (PPM): was action:explain_trust — what-have-you-learned is pull_insights",
    ),
    "is there a bottleneck analysis available": (
        "action:get_capabilities",
        "RULED 2026-10-02 (PPM): was action:analyze_blockers — 'is there X available' is the DISCOVERY existence question",
    ),
    "remember when we shipped the last release?": (
        "action:check_completion_status",
        "RULED 2026-10-02 (PPM): was action:get_memory — a completion-date question, not interaction recall",
    ),
    # CXO/PPM 2026-10-01 (evening) — STATUS_PATTERNS three families + GITHUB's last three rows.
    "what are my tasks": (
        "action:list_todos_query",
        "RULED 2026-10-01 (CXO+PPM): was action:get_project_status — 'my tasks' is the todo list; concrete beats composed",
    ),
    "show me my current tasks": (
        "action:list_todos_query",
        "RULED 2026-10-01 (CXO+PPM): was action:get_project_status — 'my tasks' is the todo list; concrete beats composed",
    ),
    "what are my active tasks": (
        "action:list_todos_query",
        "RULED 2026-10-01 (CXO+PPM): was action:get_project_status — 'my tasks' is the todo list; concrete beats composed",
    ),
    "show today's tasks": (
        "action:list_todos_query",
        "RULED 2026-10-01 (CXO+PPM): was action:get_project_status — 'my tasks' is the todo list; concrete beats composed",
    ),
    "list today's tasks": (
        "action:list_todos_query",
        "RULED 2026-10-01 (CXO+PPM): was action:get_project_status — 'my tasks' is the todo list; concrete beats composed",
    ),
    "tasks I'm actively working on": (
        "action:list_todos_query",
        "RULED 2026-10-01 (CXO+PPM): was action:get_project_status — 'my tasks' is the todo list; concrete beats composed",
    ),
    "what tasks do I have": (
        "action:list_todos_query",
        "RULED 2026-10-01 (CXO+PPM): was action:get_project_status — 'my tasks' is the todo list; concrete beats composed",
    ),
    "what are my assignments": (
        "floor",
        "RULED 2026-10-01 (CXO; PPM conceded): was action:get_project_status — an OWNERSHIP question; attention_query is an urgency aggregate and no assigned-to-me op exists",
    ),
    "show me my current assignments": (
        "floor",
        "RULED 2026-10-01 (CXO; PPM conceded): was action:get_project_status — an OWNERSHIP question; attention_query is an urgency aggregate and no assigned-to-me op exists",
    ),
    "what's assigned to me": (
        "floor",
        "RULED 2026-10-01 (CXO; PPM conceded): was action:get_project_status — an OWNERSHIP question; attention_query is an urgency aggregate and no assigned-to-me op exists",
    ),
    "tell me what I'm working on": (
        "floor",
        "RULED 2026-10-01 (CXO; PPM conceded): was action:get_project_status — an OWNERSHIP question; attention_query is an urgency aggregate and no assigned-to-me op exists",
    ),
    "show my active work": (
        "floor",
        "RULED 2026-10-01 (CXO; PPM conceded): was action:get_project_status — an OWNERSHIP question; attention_query is an urgency aggregate and no assigned-to-me op exists",
    ),
    "what am I working on?": (
        "floor",
        "RULED 2026-10-01 (CXO; PPM conceded): was action:get_project_status — an OWNERSHIP question; attention_query is an urgency aggregate and no assigned-to-me op exists",
    ),
    "I need a status report": (
        "action:generate_report",
        "RULED 2026-10-01 (CXO+PPM): the ask names a report; generate_report is a real wired handler",
    ),
    "I need a progress report": (
        "action:generate_report",
        "RULED 2026-10-01 (CXO+PPM): the ask names a report; generate_report is a real wired handler",
    ),
    "give me a project status report": (
        "action:generate_report",
        "RULED 2026-10-01 (CXO+PPM): the ask names a report; generate_report is a real wired handler",
    ),
    "prs needing review": (
        "floor",
        "RULED 2026-10-01 (CXO): neither list_prs (author-scoped) nor stale_prs (age-based) computes reviewer-requested status — capability gap, tracked",
    ),
    "when's the milestone deadline": (
        "floor",
        "RULED 2026-10-01 (CXO): no named milestone and no current-milestone default — CLARIFY is honest",
    ),
    "what version are we on": (
        "action:list_releases_query",
        "RULED 2026-10-01 (CXO): _handle_list_releases_query's own docstring disposes this exact phrase (#1039 Q5); the pattern's review_issue_query was stale",
    ),
    # CXO 2026-10-01 (PPM concurred, Arch cc) — rulings on the Phase 3 day bundle.
    # #1606: "are you able to X" is a capability QUESTION, not a disguised request.
    "are you able to set my default repo for me conversationally?": (
        "action:get_capabilities",
        "RULED 2026-10-01 (CXO, PPM concurs): was REVIEW — a capability question, not a set-command (#1606)",
    ),
    'please clear the reminders except for "Review the PR" - also, are you able to set my default repo for me conversationally?': (
        "plan",
        "RULED 2026-10-01 (CXO): was REVIEW — a two-op plan [delete_todo -> get_capabilities]; the second half is a capability question (#1606)",
    ),
    # GITHUB_QUERY: a numbered issue is a single-issue lookup; plural milestones is a listing;
    # a descriptor with no referent is honestly a clarification (floor); a milestone *update*
    # is the floor-synthesized status destination.
    "show issue #123": (
        "action:review_issue_query",
        "RULED 2026-10-01 (CXO/PPM): was REVIEW — a numbered issue is review_issue; the router's list_issues is a miss",
    ),
    "show milestones": (
        "action:list_milestones",
        "RULED 2026-10-01 (CXO/PPM): was REVIEW — plural, unnamed: a listing",
    ),
    "close the completed issue": (
        "floor",
        "RULED 2026-10-01 (CXO/PPM): was action:close_issue_query — 'the completed issue' is no referent; asking is right",
    ),
    "reopen the old issue": (
        "floor",
        "RULED 2026-10-01 (CXO/PPM): was action:reopen_issue_query — 'the old issue' is no referent; asking is right",
    ),
    "re-open the old issue": (
        "floor",
        "RULED 2026-10-01 (CXO/PPM): was action:reopen_issue_query — 'the old issue' is no referent; asking is right",
    ),
    "any update on the next milestone": (
        "action:get_project_status",
        "RULED 2026-10-01 (CXO/PPM): was action:review_issue_query — a milestone update is the floor-synthesized status destination",
    ),
    # TEMPORAL: a specific availability question is answered BETTER by the floor (it already has
    # next_free_block / time_available_minutes in context) than by a week dump.
    "when's my next free slot": (
        "floor",
        "RULED 2026-10-01 (CXO/PPM): was action:meeting_time — availability is the floor's own context field, not a calendar view",
    ),
    "what's my available time": (
        "floor",
        "RULED 2026-10-01 (CXO/PPM): was action:week_calendar — availability is the floor's own context field, not a calendar view",
    ),
    # Lead 2026-10-01 (STATUS_PATTERNS gate read): "archived projects" has its
    # own WorkflowEntry (list_archived_projects, workflow_entries.py) and the
    # served router names it @0.99 on all three phrasings; REVIEW (the
    # corpus-1283 structured source predates the entry) and manage_portfolio
    # (the active-projects listing) were both stale. Same anchor rule as the
    # GITHUB/STATUS literal-family corrections: the user names the op.
    "show me my archived projects": (
        "action:list_archived_projects",
        "RULED 2026-10-01 (Lead): was REVIEW — dedicated list_archived_projects entry exists",
    ),
    "list my archived projects": (
        "action:list_archived_projects",
        "RULED 2026-10-01 (Lead): was action:manage_portfolio — dedicated list_archived_projects entry exists",
    ),
    "Please list my archived projects": (
        "action:list_archived_projects",
        "RULED 2026-10-01 (Lead): was action:manage_portfolio — dedicated list_archived_projects entry exists",
    ),
    # CXO 2026-10-01 (extending the 09-30 PRIORITY ruling): focus-today asks
    # are attention_query's cross-domain aggregate, not a single top item.
    "what should I focus on today?": (
        "action:attention_query",
        "RULED 2026-10-01 (CXO): was category:PRIORITY — urgent/critical/focus family -> attention_query",
    ),
}


def main() -> None:
    seen = {}
    out_rows = []

    def add(row):
        key = row["phrase"].strip().lower()
        if key in seen:
            # merge citations rather than duplicating the phrase
            prev = seen[key]
            prev["source"] = f"{prev['source']} + {row['source']}"
            for k in ("probe_row", "probe_verdict", "surface1_claim", "notes"):
                if row.get(k) is not None and prev.get(k) is None:
                    prev[k] = row[k]
            return
        seen[key] = row
        out_rows.append(row)

    for r in parse_1283():
        add(
            {
                "phrase": r["phrase"],
                "category": bucket(r.get("expected", "REVIEW")),
                "expected": r.get("expected", "REVIEW"),
                "source": "corpus-1283",
            }
        )

    for r in parse_probe():
        # The probe's surface-1 claim is a CLAIM, not ground truth; expected
        # stays REVIEW unless corpus-1283 already asserted it (merge above
        # keeps 1283's expected). DISAGREE rows are precisely the Inversion's
        # open questions.
        add(
            {
                "phrase": r["phrase"],
                "category": r["claim_category"]
                if r["claim_category"] != "QUERY"
                else bucket(f"action:{r['claim_action']}", "QUERY"),
                "expected": "REVIEW",
                "source": f"probe-row-{r['probe_row']}",
                "surface1_claim": r["surface1_claim"],
                "probe_verdict": r["probe_verdict"],
            }
        )

    for r in HAND_ROWS:
        add(dict(r))

    # Arch's one demand, asserted at build time — the build FAILS without it.
    assert any(
        "what reminders do i have" in p for p in seen
    ), "Arch's demanded row ('what reminders do I have?') is missing"

    lines = [
        "# Inversion Phase-0 corpus (#1595) — GENERATED by scripts/build_inversion_corpus_phase0.py",
        "# Do not hand-edit rows that carry a structured source (corpus-1283 / probe-row-N);",
        "# edit the source or the builder. Hand rows live in the builder's HAND_ROWS with citations.",
        "#",
        "# expected:  action:<registry-canonical> | category:<NAME> | REVIEW",
        "#   REVIEW = the row is a QUESTION the Inversion answers, not an assertion —",
        "#   36 DISAGREE probe rows are open questions by construction.",
        "# category:  the PER-CATEGORY gate's denominator bucket (Arch condition 1, amended).",
        "# source:    the citation that keeps every later narrowing falsifiable.",
        "corpus:",
    ]
    for r in out_rows:
        ruled = RULED_EXPECTATIONS.get(r["phrase"])
        if ruled is not None:
            r["expected"] = ruled[0]
            r["category"] = bucket(ruled[0], r.get("category", "REVIEW"))
            r["notes"] = (r.get("notes") + " | " if r.get("notes") else "") + ruled[1]
    for r in out_rows:
        phrase = r["phrase"].replace('"', '\\"')
        lines.append(f'  - phrase: "{phrase}"')
        lines.append(f"    category: {r['category']}")
        lines.append(f"    expected: {r['expected']}")
        lines.append(f"    source: \"{r['source']}\"")
        if r.get("expected_args"):
            # Arch's (a), 2026-10-06: the asserted TARGET SET for a row whose
            # action alone is not the test. JSON is valid YAML flow syntax.
            lines.append(f"    expected_args: {json.dumps(r['expected_args'], ensure_ascii=False)}")
        for k in ("surface1_claim", "probe_verdict", "notes"):
            if r.get(k):
                lines.append(f'    {k}: "{r[k]}"')
    OUT.write_text("\n".join(lines) + "\n")

    cats = {}
    for r in out_rows:
        cats[r["category"]] = cats.get(r["category"], 0) + 1
    total = len(out_rows)
    review = sum(1 for r in out_rows if r["expected"] == "REVIEW")
    print(f"wrote {OUT.relative_to(ROOT)}: {total} rows ({review} REVIEW)")
    print("per-category denominators (m-44):")
    for c, n in sorted(cats.items(), key=lambda kv: -kv[1]):
        print(f"  {c:14s} {n}")


if __name__ == "__main__":
    main()
