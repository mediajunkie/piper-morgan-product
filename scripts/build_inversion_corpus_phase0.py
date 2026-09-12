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
        "phrase": "what projects do I have?",
        "category": "PORTFOLIO",
        "expected": "action:manage_portfolio",
        "source": "exhibit-a/1530 (chat omitted active CoVa; wrong source + wrong denominator)",
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
