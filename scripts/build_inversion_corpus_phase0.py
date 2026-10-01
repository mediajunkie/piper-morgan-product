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
        "expected": "action:list_todos_query",
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
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bpriority one\\b"',
    },
    {
        "phrase": "show priorities for this sprint",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
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
        "expected": "action:get_top_priority",
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
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bkey tasks\\b"',
    },
    {
        "phrase": "what are the key items on my plate",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
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
        "expected": "action:get_top_priority",
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
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bwhat\'?s urgent\\b"',
    },
    {
        "phrase": "what are my urgent tasks",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\burgent tasks\\b"',
    },
    {
        "phrase": "what are my urgent items",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\burgent items\\b"',
    },
    {
        "phrase": "what's my urgent work today",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
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
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bneeds.*focus\\b"',
    },
    {
        "phrase": "what requires attention right now",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\brequires attention\\b"',
    },
    {
        "phrase": "what's critical right now",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bwhat\'?s critical\\b"',
    },
    {
        "phrase": "what are my critical tasks",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bcritical tasks\\b"',
    },
    {
        "phrase": "what are my critical items",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
        "source": 'phase3-conversion/PRIORITY_PATTERNS literal r"\\bcritical items\\b"',
    },
    {
        "phrase": "what's my critical work today",
        "category": "PRIORITY",
        "expected": "action:get_top_priority",
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
        "expected": "action:get_top_priority",
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
        "expected": "action:meeting_time",
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
        "expected": "action:meeting_time",
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
        "expected": "action:week_calendar",
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
        "expected": "action:meeting_time",
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
        "expected": "action:recurring_meetings",
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
        "expected": "action:week_calendar",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bcheck.{0,10}calendar\\b"',
    },
    {
        "phrase": "is my calendar showing any conflict",
        "category": "QUERY",
        "expected": "action:week_calendar",
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
        "expected": "action:week_calendar",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bcalendar.*overlap\\b"',
    },
    {
        "phrase": "is there a conflict on my calendar",
        "category": "QUERY",
        "expected": "action:week_calendar",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bconflict.*calendar\\b"',
    },
    {
        "phrase": "find time for a 1:1 with sarah",
        "category": "QUERY",
        "expected": "action:week_calendar",
        "source": 'phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"\\bfind time for\\b"',
    },
    {
        "phrase": "find some time for a sync",
        "category": "QUERY",
        "expected": "action:week_calendar",
        "source": (
            "phase3-conversion/CALENDAR_QUERY_PATTERNS literal "
            'r"\\bfind.{0,10}time.{0,10}(?:meeting|1:1|1 on 1|sync|chat)\\b"'
        ),
    },
    {
        "phrase": "schedule a quick call",
        "category": "QUERY",
        "expected": "action:week_calendar",
        "source": (
            "phase3-conversion/CALENDAR_QUERY_PATTERNS literal "
            'r"\\bschedule.{0,10}(?:1:1|1 on 1|meeting|sync|call)\\b"'
        ),
    },
    {
        "phrase": "book a slot with the team",
        "category": "QUERY",
        "expected": "action:week_calendar",
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
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bmy calendar\\b"',
    },
    {
        "phrase": "show the team calendar",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bshow.{0,10}calendar\\b"',
        "notes": (
            'reworded — "show my calendar" is stolen first by the earlier TEMPORAL_PATTERNS '
            "sibling r'\\bmy calendar\\b'; this phrasing keeps \"my\" out of the message"
        ),
    },
    {
        "phrase": "pull up my schedule",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bmy schedule\\b"',
    },
    {
        "phrase": "show the team schedule",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bshow.{0,10}schedule\\b"',
        "notes": (
            'reworded — "show my schedule" is stolen first by the earlier TEMPORAL_PATTERNS '
            "sibling r'\\bmy schedule\\b'; this phrasing keeps \"my\" out of the message"
        ),
    },
    {
        "phrase": "calendar check for today",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bcalendar.*today\\b"',
    },
    {
        "phrase": "schedule check for today",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bschedule.*today\\b"',
    },
    {
        "phrase": "walk me through my appointments",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bmy appointments\\b"',
    },
    {
        "phrase": "show all appointments",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bshow.{0,10}appointments\\b"',
        "notes": (
            '"show the upcoming appointments" exceeds the literal\'s {0,10} gap (14 chars '
            'between "show" and "appointments") and matches no pattern at all; this '
            "phrasing fits the gap"
        ),
    },
    {
        "phrase": "walk me through my meetings",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bmy meetings\\b"',
    },
    {
        "phrase": "what are the upcoming meetings",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bupcoming meetings\\b"',
    },
    {
        "phrase": "when is my team meeting",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bwhen is my.{0,10}meeting\\b"',
        "notes": (
            'the EXISTING corpus row "when is my next meeting?" claims via the earlier '
            "sibling r'\\bnext meeting\\b', not this literal (confirmed via "
            "_first_pattern_match) — this literal was still unexercised at gate time despite "
            'its wording resembling that row; this phrase avoids "next meeting" so it claims '
            "here instead"
        ),
    },
    {
        "phrase": "when am i in a meeting",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bwhen am i.{0,10}meeting\\b"',
    },
    {
        "phrase": "meeting check for today",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bmeeting.*today\\b"',
    },
    {
        "phrase": "meeting check for tomorrow",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bmeeting.*tomorrow\\b"',
    },
    {
        "phrase": "walk me through my events",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bmy events\\b"',
    },
    {
        "phrase": "show all events",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bshow.{0,10}events\\b"',
        "notes": (
            '"show the upcoming events" exceeds the literal\'s {0,10} gap (14 chars between '
            '"show" and "events"), so it does not match this literal at all and falls '
            "through to the later sibling r'\\bupcoming events\\b' instead (same shape as the "
            '"show all appointments" row above); this phrasing fits the gap and avoids '
            '"upcoming" so it claims here'
        ),
    },
    {
        "phrase": "what are the upcoming events",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bupcoming events\\b"',
    },
    {
        "phrase": "events check for today",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bevents.*today\\b"',
    },
    {
        "phrase": "events check for tomorrow",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bevents.*tomorrow\\b"',
    },
    {
        "phrase": "when's the next event",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bnext event\\b"',
    },
    {
        "phrase": "what did I work on today",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bwork on today\\b"',
    },
    {
        "phrase": "what happened in the meeting yesterday",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bwhat.*yesterday\\b"',
    },
    {
        "phrase": "did I finish the report yesterday",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bdid.*yesterday\\b"',
        "notes": (
            'reworded — "what did I do yesterday" is stolen first by the earlier sibling '
            'r\'\\bwhat.*yesterday\\b\'; this phrasing has no "what" before "yesterday"'
        ),
    },
    {
        "phrase": "a lot happened yesterday",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bhappened yesterday\\b"',
        "notes": (
            'reworded — "what happened yesterday" is stolen first by the earlier sibling '
            'r\'\\bwhat.*yesterday\\b\'; this phrasing has no "what" or "did" before '
            '"yesterday"'
        ),
    },
    {
        "phrase": "when was the last time I worked on this",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\blast time.*worked\\b"',
    },
    {
        "phrase": "how long have I been working on this",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bhow long.*working\\b"',
    },
    {
        "phrase": "this week's priorities, remind me",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bthis week\'?s\\b"',
    },
    {
        "phrase": "next week's priorities, remind me",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bnext week\'?s\\b"',
    },
    {
        "phrase": "this month's numbers, remind me",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bthis month\'?s\\b"',
    },
    {
        "phrase": "when am i free",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bwhen am i free\\b"',
    },
    {
        "phrase": "when's my next free slot",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bwhen\'?s my next.{0,10}free\\b"',
    },
    {
        "phrase": "what's my available time",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bavailable time\\b"',
    },
    {
        "phrase": "when do I have free time",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bfree time\\b"',
    },
    {
        "phrase": "what are my open slots",
        "category": "TEMPORAL",
        "expected": "action:get_current_time",
        "source": 'phase3-conversion/TEMPORAL_PATTERNS literal r"\\bopen slots\\b"',
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
        phrase = r["phrase"].replace('"', '\\"')
        lines.append(f'  - phrase: "{phrase}"')
        lines.append(f"    category: {r['category']}")
        lines.append(f"    expected: {r['expected']}")
        lines.append(f"    source: \"{r['source']}\"")
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
