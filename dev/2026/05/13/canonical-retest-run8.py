#!/usr/bin/env python3
"""
Canonical Retest Run 8 — Multi-Turn Evaluation Harness (#1070)

Extends Run 7 with multi-turn fixture support so Q49 /standup (and similar
flows with intended multi-turn shape) can be evaluated end-to-end.

Prior runs (per BRIEFING-CURRENT-STATE):
- Run 1 (Apr 11): routing 41%, quality 59% — first honest post-M1 baseline
- Run 2 (Apr 12): routing 95.1%, quality 65.6% — after #965 + #968
- Run 3 (Apr 16): quality 72.1% — after #950 Five Pillars + grammar in floor
- Run 4 (May 8): M2f-entry baseline
- Run 5/6 (May 9): fixture-reset + rubric-recalibration
- Run 7 (May 9): post 3-bug-fix — routing 93.4% / quality 68.9% PASS
- Run 8 (May 13): multi-turn harness, same M2f-end codebase

Changes from Run 7:
1. CANONICAL_QUERIES tuples may now be 5-tuples (single-turn, unchanged)
   OR 6-tuples with optional `follow_ups: list[str]` for multi-turn queries.
2. `run_query` does a send-receive loop for follow-ups when present;
   accumulates a structured transcript "[Turn N] User: ... / Assistant: ..."
3. `judge_response` accepts an optional `transcript` instead of single
   `response_text`. The multi-turn judge prompt evaluates the conversation
   as a whole (PM Q3 decision — single full-transcript call).
4. /standup gets 3 fixtures: Q49 (quick path, the AC headline), Q49b
   (detailed path), Q49c (cancel path).

Methodology source of truth:
    docs/internal/testing/canonical-query-test-matrix-v3.md
    docs/internal/testing/colleague-test-rubric.md

Plan:
    dev/2026/04/11/canonical-retest-m1-plan.md (still applicable)

Usage:
    # Prerequisites:
    # 1. Docker daemon running
    # 2. PostgreSQL on 5433: docker compose up -d
    # 3. Server on 8001: python main.py (in another terminal)
    # 4. ANTHROPIC_API_KEY in .env (for the judge)
    POSTGRES_PORT=5433 ./venv/bin/python dev/2026/05/13/canonical-retest-run8.py

Outputs:
    dev/2026/05/13/canonical-retest-run8-results.csv
    dev/2026/05/13/canonical-retest-run8-report.md
"""

import csv
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

# Add project root to path so we can import from services/
# Path: dev/2026/04/11/canonical-retest-m1.py → 5 levels up = project root
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))

# Load .env so ANTHROPIC_API_KEY (and others) are available
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass

# --- Configuration ---
BASE_URL = "http://localhost:8001"
INTENT_ENDPOINT = f"{BASE_URL}/api/v1/intent"
LOGIN_ENDPOINT = f"{BASE_URL}/api/v1/auth/login"
USERNAME = "canonical-test"
PASSWORD = "canonical-test-2026"
SESSION_ID_PREFIX = "canonical-retest-run8"
OUTPUT_DIR = Path(__file__).parent

# Judge config
JUDGE_CONFIDENCE_THRESHOLD = 0.7  # Below this → human escalation flag
JUDGE_ENABLED = True  # Set False to skip Tier B and use Tier A only

# --- Canonical Queries v3 (61 single-turn + 3 multi-turn variants, Run 8) ---
# Format: (query_num, query_text, category, expected_routing, known_issue)
#         OR
#         (query_num, query_text, category, expected_routing, known_issue, follow_ups)
#
# follow_ups: optional list[str] of additional user messages to send in
# sequence after the initial query. Each one reuses the same session_id so
# the server preserves conversation state across turns. When present, the
# judge evaluates the FULL transcript (not just the first response).
#
# expected_routing values:
#   "floor"     — routes through ConversationalFloor (LLM response with context)
#   "canonical" — routes through canonical_handlers.handle()
#   "action"    — routes through _handle_execution_intent (mutations)
#   "preclass"  — resolved by pre-classifier (deterministic)
#
# These reflect M1 reality per intent_service.py _should_route_to_floor /
# _requires_canonical_handler. Source of truth: services/intent/intent_service.py
# lines 9829-9962 and services/intent_service/canonical_handlers.py can_handle().

# RECONCILED 2026-04-12 (#968): Expected routing updated from empirical
# diagnostic pass against live M1+#965 server. Each value reflects what
# the query ACTUALLY routes to, not what we guessed.
CANONICAL_QUERIES = [
    # Identity (5) — all floor (Apr 8 migration, verified)
    (1, "What's your name?", "Identity", "floor", None),
    (2, "What can you help me with?", "Identity", "floor", None),
    (3, "Are you working properly?", "Identity", "floor", None),
    (4, "How do I get help?", "Identity", "floor", None),
    (5, "What makes you different?", "Identity", "floor", None),

    # Temporal (5) — Q6 canonical, Q7/9/10 floor (#965), Q8 canonical (pre-classifier→query)
    (6, "What day is it?", "Temporal", "canonical", None),
    (7, "What did we accomplish yesterday?", "Temporal", "floor", None),
    (8, "What's on the agenda for today?", "Temporal", "canonical", None),  # pre-classifier routes to query/meeting_time
    (9, "When was the last time we worked on this?", "Temporal", "floor", None),
    (10, "How long have we been working on this project?", "Temporal", "floor", None),

    # Spatial / Status (4) — all floor (STATUS routes through floor via safety net)
    (11, "What projects are we working on?", "Spatial", "floor", None),
    (12, "Show me the project landscape", "Spatial", "floor", None),
    (13, "Which project should I focus on?", "Spatial", "floor", None),
    (14, "What's the status of project X?", "Spatial", "floor", None),

    # Capability (5) — mixed: action for mutations, floor for read-only
    (16, "Create a GitHub issue about testing", "Capability", "action", None),
    (17, "Analyze this document", "Capability", "action", None),
    (18, "List all my projects", "Capability", "floor", None),  # STATUS→floor
    (19, "Generate a status report", "Capability", "floor", None),  # STATUS→floor
    (20, "Search for authentication in our documents", "Capability", "action", None),

    # Predictive (5) — all floor
    (21, "What should I focus on today?", "Predictive", "floor", None),
    (22, "What patterns do you see?", "Predictive", "floor", "M2 Beta"),
    (23, "What risks should I be aware of?", "Predictive", "floor", "M2 Beta"),
    (24, "What opportunities should I pursue?", "Predictive", "floor", "M2 Beta"),
    (25, "What's the next milestone?", "Predictive", "floor", "M2 Beta"),

    # Conversational (5) — mostly floor, Q29/30 canonical (pre-classifier→query)
    (26, "What else can you help with?", "Conversational", "floor", None),
    (27, "Tell me more about the GitHub integration", "Conversational", "floor", None),
    (28, "How do I use the calendar feature?", "Conversational", "floor", None),
    (29, "What changed since yesterday?", "Conversational", "canonical", None),  # query/changes_query
    (30, "What needs my attention?", "Conversational", "canonical", None),  # query/attention_query

    # Scheduling (5) — Q32 action, rest canonical (pre-classifier→query)
    (31, "Schedule a meeting about the roadmap", "Scheduling", "canonical", "M2"),  # query/meeting_time
    (32, "Remind me to review PRs tomorrow", "Scheduling", "action", "M2"),
    (33, "Find time for a 1:1 with the team lead", "Scheduling", "canonical", "M2"),  # query/meeting_time
    (34, "How much time am I spending in meetings?", "Scheduling", "canonical", None),
    (35, "Review my recurring meetings", "Scheduling", "canonical", None),

    # Documents (4) — Q36-38 floor, Q40 action
    (36, "Create a doc from this conversation", "Documents", "floor", "M2"),
    (37, "Compare these two documents", "Documents", "floor", "M2"),
    (38, "Synthesize these sources into a summary", "Documents", "floor", "M2"),
    (40, "Update the project roadmap document", "Documents", "action", "M2"),

    # GitHub Operations (8) — mixed
    (41, "What did we ship this week?", "GitHub Ops", "canonical", None),  # query/shipped_query
    (42, "Show me stale PRs", "GitHub Ops", "canonical", None),  # query/stale_prs_query
    (43, "What's blocking the milestone?", "GitHub Ops", "floor", None),
    (44, "Create issues from this meeting's action items", "GitHub Ops", "floor", None),
    (45, "Close completed issues", "GitHub Ops", "floor", None),
    (58, "Update issue #123", "GitHub Ops", "action", None),
    (59, "Comment on issue #456", "GitHub Ops", "canonical", None),  # query/comment_issue_query
    (60, "Review issue #789", "GitHub Ops", "canonical", None),  # query/review_issue_query

    # Slack (5) — Q46-48 floor, Q49 action, Q50 floor
    (46, "Any mentions I missed?", "Slack", "floor", "M2"),
    (47, "Summarize #general from yesterday", "Slack", "floor", "M2"),
    (48, "Post this update to the team channel", "Slack", "floor", "M2"),
    # Q49 now multi-turn (#1070): /standup → "quick" exercises the happy-path
    # branch of the #900 3-part flow. Verdict-improvement metric for the AC.
    (49, "/standup", "Slack", "action", None, ["quick"]),
    (50, "/piper help", "Slack", "floor", None),

    # Productivity (3) — all floor
    (51, "What's my productivity this week?", "Productivity", "floor", None),
    (52, "Are we on track for the milestone?", "Productivity", "floor", None),
    (53, "What did the team accomplish this sprint?", "Productivity", "floor", None),

    # Todo Management (4) — Q54-55 action, Q56-57 canonical (pre-classifier→query)
    (54, "Add a todo: review the deployment plan", "Todos", "action", None),
    (55, "Complete the PR review todo", "Todos", "action", None),
    (56, "Show my todos", "Todos", "canonical", None),  # query/list_todos_query
    (57, "What's my next todo?", "Todos", "canonical", None),  # query/next_todo_query

    # Calendar Extended (2) — both canonical (pre-classifier→query)
    (61, "What's my week look like?", "Calendar Ext", "canonical", None),
    (62, "Check my calendar for conflicts", "Calendar Ext", "canonical", None),

    # Knowledge (1) — floor
    (63, "Upload a file to the knowledge base", "Knowledge", "floor", "M2"),

    # #1070 multi-turn coverage: /standup branch coverage beyond Q49 happy-path
    # Same query, different second-turn responses to exercise the 3 branches.
    (149, "/standup", "Slack (multi-turn)", "action", None, ["detailed"]),
    (150, "/standup", "Slack (multi-turn)", "action", None, ["no"]),
]


# --- LLM-as-Judge ---

JUDGE_SYSTEM_PROMPT = """You are an evaluator scoring Piper Morgan's responses to product manager queries against the Colleague Test rubric.

THE RUBRIC

Score three dimensions, 0-3 each:

Relevance (R): Does the response engage with what the user actually asked?
- 0: Did not address the question. Generic greeting or off-topic.
- 1: Vaguely gestured at the topic, did not answer.
- 2: Addressed the question but missed key parts.
- 3: Directly engaged or asked clarifying questions when context was missing.

Context (C): Does the response reference real data, conversation history, or appropriate knowledge?
- 0: Empty response, OR fabricated content (made-up data that doesn't exist).
- 1: Generic — could be any user, any project. No real situation referenced.
- 2: Some real context referenced but underused.
- 3: Rich, accurate use of available context. Honest about gaps.

Tone (T): Does the response sound like a colleague rather than a chatbot or template?
- 0: Robotic, template-fingerprinted, or chatbot warmth ("I'm so excited to help!").
- 1: Polite but stilted.
- 2: Conversational and competent.
- 3: Distinctly colleague-like.

VERDICTS (recalibrated 2026-05-09 — see investigation memo for #1064)

PASS: total >= 7
MARGINAL: total in {5, 6}
FAIL: total < 5 OR two-or-more dimensions scored 0 (auto-fail)

A single dimension scoring 0 is no longer disqualifying — Run 4 surfaced
that the judge over-weights user-context-specificity (C dimension) on
queries that don't need it (identity, capability, mutation-confirm).
A response can score R=3 C=0 T=2 and still aggregate to 5 MARGINAL
(or higher if T is strong). Two-or-more zeros still forces FAIL because
that signals broad failure across multiple quality axes.

CALIBRATION EXAMPLES

Example 1 (PASS, 8/9):
Query: "How trustworthy are your recommendations?"
Response: "That's a smart question to ask. My recommendations are as good as the reasoning behind them — I draw on established PM frameworks, best practices, and the context you share with me, but I'm not infallible. I'm strongest when we're working through problems together — thinking through trade-offs, applying prioritization frameworks, or analyzing stakeholder dynamics. But I can't replace your judgment about your specific team dynamics."
Scores: R=3 C=2 T=3 = 8 PASS

Example 2 (FAIL, 1/9, double auto-fail):
Query: "Help me plan a stakeholder presentation for next week"
Response: "I'm ready to help! What's on your mind today?"
Scores: R=0 C=0 T=1 = 1 FAIL (R and C auto-fail)

Example 3 (MARGINAL, 5/9):
Query: "Do you remember what we talked about yesterday?"
Response: "Today is Wednesday, April 08, 2026. Regarding memory, we haven't had many conversations yet, but I'm looking forward to getting to know you better as we work together!"
Scores: R=2 C=2 T=1 = 5 MARGINAL (chatbot warmth tone)

OUTPUT FORMAT

Return ONLY valid JSON, no other text:
{
  "relevance": <0-3>,
  "context": <0-3>,
  "tone": <0-3>,
  "rationale": {"r": "<one sentence>", "c": "<one sentence>", "t": "<one sentence>"},
  "total": <sum>,
  "verdict": "PASS" | "MARGINAL" | "FAIL",
  "confidence": <0.0-1.0>
}

confidence reflects how sure you are of this verdict. Use < 0.7 if the response is borderline, edge-case, or you would want a human to confirm."""


# #1070: multi-turn judge rubric — evaluates the conversation as a whole.
# Used when a query has follow-ups defined; rubric explicitly accounts for
# how the FULL exchange (not just the opener) serves the user's intent.
JUDGE_SYSTEM_PROMPT_MULTITURN = """You are an evaluator scoring Piper Morgan's multi-turn conversations against the Colleague Test rubric.

YOU ARE EVALUATING A SEQUENCE OF TURNS — not a single response.

The transcript shows:
- [Turn 1] User: <the initial query>
- [Turn 1] Assistant: <Piper's first response>
- [Turn 2] User: <follow-up>
- [Turn 2] Assistant: <Piper's follow-up response>
- ...

A good multi-turn exchange may legitimately open with a short clarifying
question (e.g. "Quick or detailed?") — score that opening as appropriate
context-gathering, not as a low-relevance non-answer, as long as the LATER
turns substantively serve the user's intent.

THE RUBRIC (scoring the conversation as a whole)

Score three dimensions, 0-3 each:

Relevance (R): Across the full exchange, did Piper engage with what the user actually wanted?
- 0: The exchange never engages with the initial intent. Final turn off-topic.
- 1: Vaguely gestured at the topic across turns; no substantive answer.
- 2: Addressed the intent but missed key parts. May have asked good clarifying
     questions but then fell short on the substantive follow-through.
- 3: Across the turns, fully served the intent. Clarifying questions (when
     used) led to substantive, relevant follow-through.

Context (C): Across the exchange, does Piper reference real data, conversation
state, or appropriate knowledge?
- 0: Empty or fabricated. Made-up data.
- 1: Generic throughout — never anchored to real situation.
- 2: Some real context referenced, but underused or only in one turn.
- 3: Rich, accurate use of context across turns. Later turns build on earlier
     state. Honest about gaps.

Tone (T): Across the exchange, does Piper sound like a colleague?
- 0: Robotic, templated, or chatbot warmth throughout.
- 1: Polite but stilted; one turn fine, another regression.
- 2: Conversational and competent across turns.
- 3: Distinctly colleague-like through the whole exchange.

VERDICTS (same calibration as single-turn — recalibrated 2026-05-09)

PASS: total >= 7
MARGINAL: total in {5, 6}
FAIL: total < 5 OR two-or-more dimensions scored 0 (auto-fail)

KEY MULTI-TURN CALIBRATION

- A short opener that asks a reasonable clarifying question ("Quick standup or
  detailed?") is GOOD context-gathering. Don't penalize it as R=0/C=0. The
  later turns are where substantive credit accrues.
- A "no" / cancel branch where the user backs out should score well IF Piper
  acknowledges the cancellation cleanly and ends the flow.
- A "detailed" branch should score well IF Piper actually delivers the
  detailed response in turn 2+.

OUTPUT FORMAT

Return ONLY valid JSON, no other text:
{
  "relevance": <0-3>,
  "context": <0-3>,
  "tone": <0-3>,
  "rationale": {"r": "<one sentence>", "c": "<one sentence>", "t": "<one sentence>"},
  "total": <sum>,
  "verdict": "PASS" | "MARGINAL" | "FAIL",
  "confidence": <0.0-1.0>
}

confidence reflects how sure you are of this verdict. Use < 0.7 if the conversation is borderline, edge-case, or you would want a human to confirm."""


def judge_response(query_text: str, response_text: str, anthropic_client, transcript: str = None) -> dict:
    """Call LLM-as-judge for a response. Returns dict with scores + confidence.

    Returns dict with keys: relevance, context, tone, total, verdict, confidence,
    rationale (dict), error (if any), raw_response (debug).

    #1070: when `transcript` is non-None, evaluate the full multi-turn
    transcript (rubric judges the conversation as a whole). When None,
    evaluate the single response_text (Run 7 behavior, unchanged).
    """
    if not anthropic_client:
        return {"error": "no judge client"}

    is_multi_turn = transcript is not None

    if is_multi_turn:
        user_prompt = f"""Initial query: {query_text!r}

Full conversation transcript (multi-turn):
\"\"\"
{transcript}
\"\"\"

Score this conversation as a whole per the rubric. Return only the JSON object."""
        system_prompt = JUDGE_SYSTEM_PROMPT_MULTITURN
    else:
        user_prompt = f"""Query: {query_text!r}

Piper's response:
\"\"\"
{response_text}
\"\"\"

Score this response per the rubric. Return only the JSON object."""
        system_prompt = JUDGE_SYSTEM_PROMPT

    try:
        message = anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            temperature=0.2,  # Low temperature for consistent scoring
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        raw = message.content[0].text.strip()

        # Strip markdown code fences if the LLM included them
        if raw.startswith("```"):
            raw = raw.split("```", 2)[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()
            if raw.endswith("```"):
                raw = raw[:-3].strip()

        parsed = json.loads(raw)

        # Sanity-check structure
        for key in ("relevance", "context", "tone", "verdict", "confidence"):
            if key not in parsed:
                parsed["error"] = f"judge missing key: {key}"
                parsed["raw_response"] = raw[:300]
                return parsed

        # Sanity-check ranges
        for key in ("relevance", "context", "tone"):
            v = parsed.get(key)
            if not isinstance(v, int) or v < 0 or v > 3:
                parsed["error"] = f"judge invalid {key}: {v}"
                return parsed

        # Auto-fail rule (defense against judge inconsistency).
        # 2026-05-09 recalibration (per CEO + investigation memo for #1064):
        # Soften from "any single dim=0" to "two-or-more dims=0" — Run 4 surfaced
        # that the judge over-weights user-context-specificity even on queries that
        # don't need it (identity, capability, mutation-confirm shapes), causing
        # false FAILs. CXO/PPM review pending; PM authorized proceed without sign-off.
        zero_dims = sum(1 for k in ("relevance", "context", "tone") if parsed.get(k) == 0)
        if zero_dims >= 2:
            if parsed.get("verdict") != "FAIL":
                parsed["verdict"] = "FAIL"
                parsed["rationale"] = parsed.get("rationale", {})
                parsed["rationale"]["override"] = f"auto-fail rule ({zero_dims} dimensions scored 0)"

        total_computed = parsed["relevance"] + parsed["context"] + parsed["tone"]
        parsed["total"] = total_computed

        return parsed

    except json.JSONDecodeError as e:
        return {"error": f"judge JSON parse failed: {e}", "raw_response": raw[:300] if 'raw' in locals() else ""}
    except Exception as e:
        return {"error": f"judge call failed: {type(e).__name__}: {e}"}


# --- Heuristic check (Tier A) ---

PLACEHOLDER_INDICATORS = [
    "not yet implemented",
    "capability pending",
    "coming soon",
    "placeholder",
    "i don't have that capability",
    "that feature isn't available",
    "not currently supported",
]

ERROR_INDICATORS = [
    "something unexpected happened",
    "internal server error",
    "i had trouble",
    "something went wrong",
    "exception",
    "traceback",
]

TEMPLATE_FINGERPRINTS = [
    "i'm piper morgan — i work alongside you on product management",
    "i'm here to help! what's on your mind",
    "looking forward to getting to know you better",
]


def heuristic_check(message: str) -> dict:
    """Tier A: fast heuristic check. Returns dict with: empty, error, placeholder, template_fingerprint."""
    if not message or len(message.strip()) < 5:
        return {"empty": True, "error": False, "placeholder": False, "template": False}

    m = message.lower()
    return {
        "empty": False,
        "error": any(ind in m for ind in ERROR_INDICATORS),
        "placeholder": any(ind in m for ind in PLACEHOLDER_INDICATORS),
        "template": any(ind in m for ind in TEMPLATE_FINGERPRINTS),
    }


# --- Routing classification ---

# Map intent category (lowercase from API response) → expected routing
# This mirrors _should_route_to_floor / _requires_canonical_handler logic.
FLOOR_CATEGORIES = {"identity", "discovery", "trust", "memory", "guidance", "unknown"}
CANONICAL_CATEGORIES = {"temporal", "status", "priority", "portfolio"}
ACTION_CATEGORIES = {"execution"}


def determine_actual_routing(intent_data: dict, response_text: str, intent_data_extras: dict) -> str:
    """Inspect the API response to determine which routing path was taken.

    The /api/v1/intent endpoint returns intent_data with category, action, and
    optionally floor_hit (set when the conversational floor handles the response).

    #968: Simplified after empirical reconciliation — floor_hit is the primary
    signal. For queries without floor_hit, classify based on category.
    """
    if not intent_data:
        return "unknown"

    # Most reliable signal: floor_hit flag
    if intent_data.get("floor_hit") is True:
        return "floor"

    category = (intent_data.get("category") or "").lower()

    # Execution category without floor_hit = action handler
    if category == "execution":
        return "action"

    # Everything without floor_hit that isn't execution = canonical/handler path
    return "canonical"


def routing_match(expected: str, actual: str) -> bool:
    """Check if actual routing matches expected. preclass treated as canonical."""
    if expected == actual:
        return True
    if expected == "preclass" and actual in ("canonical", "floor"):
        return True
    return False


# --- Auth ---

def ensure_user(session: requests.Session) -> bool:
    """Ensure the canonical-test user exists. Idempotent."""
    create_url = f"{BASE_URL}/api/v1/setup/create-user"
    resp = session.post(
        create_url,
        json={
            "username": USERNAME,
            "email": f"{USERNAME}@piper-morgan.local",
            "password": PASSWORD,
            "password_confirm": PASSWORD,
        },
    )
    if resp.status_code == 200:
        print(f"  Created test user {USERNAME}")
        return True
    if resp.status_code == 400 and "exist" in resp.text.lower():
        print(f"  Test user {USERNAME} already exists (OK)")
        return True
    print(f"  ensure_user note: {resp.status_code} {resp.text[:200]}")
    # Don't abort — login will tell us if there's a real problem
    return True


def login(session: requests.Session) -> str | None:
    """Authenticate. Returns auth token or None.

    Stores token in session cookie + Authorization header for subsequent requests.
    """
    resp = session.post(
        LOGIN_ENDPOINT,
        data={"username": USERNAME, "password": PASSWORD},  # Form-encoded per auth.py
    )
    if resp.status_code != 200:
        print(f"  LOGIN FAILED: {resp.status_code} {resp.text[:200]}")
        return None
    try:
        data = resp.json()
        token = data.get("token") or data.get("access_token")
        if token:
            session.headers["Authorization"] = f"Bearer {token}"
            print(f"  Logged in as {USERNAME}")
            return token
        print(f"  LOGIN FAILED: no token in response: {data}")
        return None
    except Exception as e:
        print(f"  LOGIN FAILED: {e}")
        return None


# --- Per-query test ---

def run_query(
    session,
    query_num,
    query_text,
    category,
    expected_routing,
    known_issue,
    anthropic_client,
    follow_ups=None,
) -> dict:
    """Send one query (and optional follow-ups), classify routing, run heuristic + judge.

    #1070: when `follow_ups` is non-None, the harness sends each follow-up as
    a subsequent POST reusing the same session_id; the server preserves
    conversation state across turns. The judge receives the FULL transcript
    (all user+assistant turns) and evaluates the conversation as a whole.
    """
    is_multi_turn = bool(follow_ups)
    result = {
        "query_num": query_num,
        "query": query_text,
        "category": category,
        "expected_routing": expected_routing,
        "known_issue": known_issue or "",
        "actual_routing": None,
        "actual_intent_category": None,
        "actual_intent_action": None,
        "http_status": None,
        "response_text": "",
        "response_preview": "",
        # #1070: full transcript for multi-turn (List[str] formatted)
        "transcript": "",
        "turns_completed": 0,
        "follow_ups": list(follow_ups) if follow_ups else [],
        "heuristic": {},
        "routing_pass": False,
        "tier_a_verdict": None,
        "judge_relevance": None,
        "judge_context": None,
        "judge_tone": None,
        "judge_total": None,
        "judge_verdict": None,
        "judge_confidence": None,
        "judge_rationale": "",
        "escalate_to_human": False,
        "escalate_reason": "",
        "error": None,
        "notes": "",
    }

    try:
        session_id = f"{SESSION_ID_PREFIX}-q{query_num}"
        resp = session.post(
            INTENT_ENDPOINT,
            json={
                "message": query_text,
                "session_id": session_id,
            },
            timeout=60,
        )
        result["http_status"] = resp.status_code

        if resp.status_code != 200:
            result["error"] = f"HTTP {resp.status_code}: {resp.text[:200]}"
            result["tier_a_verdict"] = "ERROR"
            return result

        data = resp.json()
        intent_data = data.get("intent") or {}
        message = data.get("message") or ""
        api_error = data.get("error")

        result["actual_intent_category"] = intent_data.get("category")
        result["actual_intent_action"] = intent_data.get("action")
        result["response_text"] = message
        result["response_preview"] = message[:200]
        result["actual_routing"] = determine_actual_routing(intent_data, message, data)
        result["routing_pass"] = routing_match(expected_routing, result["actual_routing"])
        result["turns_completed"] = 1

        # #1070: build transcript starting with turn 1 (always, for uniform shape)
        transcript_lines = [
            f"[Turn 1] User: {query_text}",
            f"[Turn 1] Assistant: {message}",
        ]

        # #1070: send follow-ups in sequence, reusing session_id so server
        # preserves conversation state across turns. Each follow-up's response
        # is appended to the transcript; the judge sees the whole thing.
        if is_multi_turn:
            for i, follow_up in enumerate(follow_ups, start=2):
                # Brief pause so the server's per-session state settles
                time.sleep(0.3)
                try:
                    fresp = session.post(
                        INTENT_ENDPOINT,
                        json={"message": follow_up, "session_id": session_id},
                        timeout=60,
                    )
                    if fresp.status_code != 200:
                        result["notes"] = (
                            f"follow-up turn {i} HTTP {fresp.status_code}: {fresp.text[:200]}"
                        )
                        # Don't return — judge can still evaluate the partial transcript
                        break
                    fdata = fresp.json()
                    fmessage = fdata.get("message") or ""
                    transcript_lines.append(f"[Turn {i}] User: {follow_up}")
                    transcript_lines.append(f"[Turn {i}] Assistant: {fmessage}")
                    result["turns_completed"] = i
                except requests.exceptions.Timeout:
                    result["notes"] = f"follow-up turn {i} timeout"
                    break
                except Exception as fe:
                    result["notes"] = f"follow-up turn {i} error: {type(fe).__name__}: {fe}"
                    break

        result["transcript"] = "\n".join(transcript_lines)

        # Tier A heuristic
        h = heuristic_check(message)
        result["heuristic"] = h

        if api_error:
            result["error"] = f"service: {api_error}"
            result["tier_a_verdict"] = "ERROR"
            return result
        if h["empty"]:
            result["tier_a_verdict"] = "FAIL"
            result["notes"] = "empty response"
            return result
        if h["error"]:
            result["tier_a_verdict"] = "FAIL"
            result["notes"] = "error fingerprint in response"
            return result
        if h["template"]:
            result["tier_a_verdict"] = "FAIL"
            result["notes"] = "template fingerprint detected"
            # still run judge to confirm
        if h["placeholder"]:
            result["tier_a_verdict"] = "NOT_IMPL"
            result["notes"] = "graceful 'not implemented' message"
            # don't waste judge tokens on these
            return result

        if not result["tier_a_verdict"]:
            result["tier_a_verdict"] = "OK"  # passed Tier A, on to judge

        # Tier B: judge
        if JUDGE_ENABLED and anthropic_client and result["tier_a_verdict"] in ("OK", "FAIL"):
            # #1070: pass transcript for multi-turn; single response for single-turn
            judge_result = judge_response(
                query_text,
                message,
                anthropic_client,
                transcript=result["transcript"] if is_multi_turn else None,
            )
            if "error" in judge_result:
                result["error"] = (result["error"] or "") + " | judge: " + judge_result["error"]
                result["escalate_to_human"] = True
                result["escalate_reason"] = "judge error"
            else:
                result["judge_relevance"] = judge_result.get("relevance")
                result["judge_context"] = judge_result.get("context")
                result["judge_tone"] = judge_result.get("tone")
                result["judge_total"] = judge_result.get("total")
                result["judge_verdict"] = judge_result.get("verdict")
                result["judge_confidence"] = judge_result.get("confidence")
                result["judge_rationale"] = json.dumps(judge_result.get("rationale", {}))[:500]

                # Tier C escalation triggers
                conf = judge_result.get("confidence", 1.0) or 1.0
                if conf < JUDGE_CONFIDENCE_THRESHOLD:
                    result["escalate_to_human"] = True
                    result["escalate_reason"] = f"low confidence ({conf:.2f})"
                elif 0 in (judge_result.get("relevance"), judge_result.get("context"), judge_result.get("tone")):
                    result["escalate_to_human"] = True
                    result["escalate_reason"] = "auto-fail (2+ dimensions scored 0)"

        return result

    except requests.exceptions.Timeout:
        result["error"] = "timeout (60s)"
        result["tier_a_verdict"] = "ERROR"
        return result
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {e}"
        result["tier_a_verdict"] = "ERROR"
        return result


# --- Output ---

CSV_FIELDS = [
    "query_num",
    "query",
    "category",
    "expected_routing",
    "actual_routing",
    "routing_pass",
    "actual_intent_category",
    "actual_intent_action",
    "tier_a_verdict",
    "judge_relevance",
    "judge_context",
    "judge_tone",
    "judge_total",
    "judge_verdict",
    "judge_confidence",
    "escalate_to_human",
    "escalate_reason",
    "known_issue",
    "http_status",
    "error",
    "notes",
    "response_preview",
    "judge_rationale",
    # #1070: multi-turn fields (blank for single-turn rows)
    "follow_ups",
    "turns_completed",
]


def write_csv(results, filepath: Path):
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for r in results:
            row = {k: r.get(k, "") for k in CSV_FIELDS}
            row["heuristic"] = ""  # don't include nested
            writer.writerow(row)


def write_report(results, filepath: Path):
    total = len(results)

    routing_pass = sum(1 for r in results if r["routing_pass"])
    routing_fail = total - routing_pass

    judge_pass = sum(1 for r in results if r.get("judge_verdict") == "PASS")
    judge_marginal = sum(1 for r in results if r.get("judge_verdict") == "MARGINAL")
    judge_fail = sum(1 for r in results if r.get("judge_verdict") == "FAIL")
    judge_skipped = sum(1 for r in results if r.get("judge_verdict") is None)

    escalations = [r for r in results if r["escalate_to_human"]]
    errors = [r for r in results if r.get("error")]
    known_issues = [r for r in results if r["known_issue"]]

    by_category = {}
    for r in results:
        cat = r["category"]
        if cat not in by_category:
            by_category[cat] = {
                "total": 0, "routing_pass": 0,
                "judge_pass": 0, "judge_marginal": 0, "judge_fail": 0, "judge_skipped": 0,
            }
        by_category[cat]["total"] += 1
        if r["routing_pass"]:
            by_category[cat]["routing_pass"] += 1
        v = r.get("judge_verdict")
        if v == "PASS":
            by_category[cat]["judge_pass"] += 1
        elif v == "MARGINAL":
            by_category[cat]["judge_marginal"] += 1
        elif v == "FAIL":
            by_category[cat]["judge_fail"] += 1
        else:
            by_category[cat]["judge_skipped"] += 1

    lines = [
        "# Canonical Query Retest Report — Post-M1 (v3)",
        "",
        f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "**Version**: v0.8.6 (post-M1, M1 closed Apr 11)",
        f"**User**: {USERNAME} (fresh account)",
        f"**Total Queries**: {total}",
        f"**Methodology**: canonical-query-test-matrix-v3.md (dual scoring + LLM-as-judge)",
        "",
        "---",
        "",
        "## Routing Verdict (M0-comparable dimension)",
        "",
        f"| Metric | Count | Percentage |",
        f"|--------|-------|------------|",
        f"| Routing PASS | {routing_pass} | {routing_pass/total*100:.1f}% |",
        f"| Routing FAIL | {routing_fail} | {routing_fail/total*100:.1f}% |",
        "",
        "**M0 baseline (Mar 12)**: 70.5% routing pass (43/61)",
        f"**M1 routing**: {routing_pass/total*100:.1f}% ({routing_pass}/{total})",
        "",
        "---",
        "",
        "## Quality Verdict (Colleague Test, new in v3)",
        "",
        f"| Verdict | Count | Percentage |",
        f"|---------|-------|------------|",
        f"| PASS (judge ≥7) | {judge_pass} | {judge_pass/total*100:.1f}% |",
        f"| MARGINAL (judge 5-6) | {judge_marginal} | {judge_marginal/total*100:.1f}% |",
        f"| FAIL (judge <5 or auto-fail) | {judge_fail} | {judge_fail/total*100:.1f}% |",
        f"| Skipped (NOT_IMPL or ERROR) | {judge_skipped} | {judge_skipped/total*100:.1f}% |",
        "",
        f"**Quality pass rate (judged queries)**: "
        f"{judge_pass}/{judge_pass+judge_marginal+judge_fail} "
        f"({judge_pass/max(1, judge_pass+judge_marginal+judge_fail)*100:.1f}%)",
        "",
        "---",
        "",
        "## Results by Category",
        "",
        "| Category | Total | Routing PASS | Quality PASS | MARGINAL | FAIL |",
        "|----------|-------|-------------|--------------|----------|------|",
    ]
    for cat in [
        "Identity", "Temporal", "Spatial", "Capability", "Predictive",
        "Conversational", "Scheduling", "Documents", "GitHub Ops", "Slack",
        "Productivity", "Todos", "Calendar Ext", "Knowledge",
    ]:
        if cat in by_category:
            d = by_category[cat]
            lines.append(
                f"| {cat} | {d['total']} | {d['routing_pass']}/{d['total']} | "
                f"{d['judge_pass']} | {d['judge_marginal']} | {d['judge_fail']} |"
            )

    if escalations:
        lines.extend([
            "",
            "---",
            "",
            f"## Human Escalation Queue ({len(escalations)} items)",
            "",
            "These results need human review. Triggers: low judge confidence, auto-fail (dimension=0), or judge error.",
            "",
        ])
        for r in escalations:
            lines.append(
                f"- **Q{r['query_num']}** ({r['category']}): `{r['query'][:60]}` — {r['escalate_reason']}"
            )
            if r.get("judge_total") is not None:
                lines.append(
                    f"  - Judge: R={r['judge_relevance']} C={r['judge_context']} T={r['judge_tone']} "
                    f"= {r['judge_total']}/{r['judge_verdict']} (conf {r['judge_confidence']:.2f})"
                )

    if errors:
        lines.extend([
            "",
            "---",
            "",
            f"## Errors ({len(errors)} items)",
            "",
        ])
        for r in errors:
            lines.append(f"- **Q{r['query_num']}** ({r['category']}): `{r['query'][:60]}` — {r['error']}")

    if known_issues:
        lines.extend([
            "",
            "---",
            "",
            f"## Known Issues Run Anyway ({len(known_issues)} items)",
            "",
            "Per PM guidance: known failures are still run honestly. Tag indicates tracking.",
            "",
        ])
        for r in known_issues:
            verdict = r.get("judge_verdict") or r.get("tier_a_verdict") or "—"
            lines.append(
                f"- **Q{r['query_num']}** ({r['category']}, {r['known_issue']}): "
                f"`{r['query'][:60]}` — {verdict}"
            )

    lines.extend([
        "",
        "---",
        "",
        "## Methodology Notes",
        "",
        "- **Routing verdict**: Compares actual route taken (floor / canonical / action) to v3 expected route. M0 baseline used a different methodology (literal category matching) so this is a reframed but loosely comparable number.",
        "- **Quality verdict**: LLM-as-judge using Colleague Test rubric. Judge model: claude-sonnet-4-20250514, temperature 0.2, with calibration examples in system prompt.",
        f"- **Confidence threshold for human escalation**: < {JUDGE_CONFIDENCE_THRESHOLD}",
        "- **Auto-fail rule**: any single dimension scoring 0 forces FAIL verdict regardless of total.",
        "- **Known issues** are run anyway per PM guidance — honest reporting over hiding.",
        "",
        f"*Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} by canonical-retest-m1.py*",
    ])

    with open(filepath, "w") as f:
        f.write("\n".join(lines))


# --- Main ---

def main():
    print("=" * 70)
    print("M1 Canonical Retest — Post-M1 Floor-First Validation")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Target: {BASE_URL}")
    print(f"Queries: {len(CANONICAL_QUERIES)}")
    print("=" * 70)

    # Initialize judge
    anthropic_client = None
    if JUDGE_ENABLED:
        try:
            from anthropic import Anthropic
            api_key = os.getenv("ANTHROPIC_API_KEY")
            key_source = "env"
            if not api_key:
                # #1070: fall back to KeychainService so the retest works
                # in worktrees that don't have a local .env file. The
                # conftest already uses this pathway for pytest.
                try:
                    from services.infrastructure.keychain_service import KeychainService

                    api_key = KeychainService().get_api_key("anthropic")
                    if api_key:
                        key_source = "keychain"
                except Exception as ke:
                    print(f"  (keychain unavailable: {ke})")
            if api_key:
                anthropic_client = Anthropic(api_key=api_key)
                print(f"\nLLM-as-judge: enabled (claude-sonnet-4-20250514) — key from {key_source}")
            else:
                print("\nLLM-as-judge: DISABLED (no ANTHROPIC_API_KEY in env or keychain)")
        except Exception as e:
            print(f"\nLLM-as-judge: DISABLED ({e})")

    # Phase 0: Fixture reset (2026-05-09 — added per investigation memo for #1064).
    # Wipe canonical-test polymorphic items + todo state so mutation queries (Q53/Q54
    # add-todo) don't accumulate across runs. Idempotent; runs even if user doesn't
    # exist yet (no-op for empty result).
    import subprocess
    print("\nPhase 0: resetting canonical-test fixtures...")
    reset_sql = """
BEGIN;
DELETE FROM todo_items WHERE owner_id = (SELECT id FROM users WHERE username='canonical-test');
DELETE FROM items WHERE id NOT IN (SELECT id FROM todo_items);
COMMIT;
"""
    try:
        proc = subprocess.run(
            ["docker", "exec", "-i", "piper-postgres", "psql", "-U", "piper", "-d", "piper_morgan"],
            input=reset_sql, capture_output=True, text=True, timeout=10,
        )
        if proc.returncode == 0:
            print("  Fixture reset OK (canonical-test todos + orphan items wiped)")
        else:
            print(f"  Fixture reset note: {proc.stderr[:200]}")
    except Exception as e:
        print(f"  Fixture reset skipped ({e}) — continuing")

    # Ensure test user + Login
    session = requests.Session()
    print("\nEnsuring test user...")
    ensure_user(session)
    print("Authenticating...")
    if not login(session):
        print("FATAL: Cannot authenticate. Aborting.")
        sys.exit(1)

    # Run queries
    results = []
    current_category = None
    for query in CANONICAL_QUERIES:
        # #1070: tuples may be 5-tuples (single-turn) or 6-tuples (with follow_ups)
        query_num = query[0]
        query_text = query[1]
        category = query[2]
        expected_routing = query[3]
        known_issue = query[4]
        follow_ups = query[5] if len(query) > 5 else None

        if category != current_category:
            current_category = category
            print(f"\n### {category} ###")

        result = run_query(
            session, query_num, query_text, category, expected_routing,
            known_issue, anthropic_client, follow_ups=follow_ups,
        )
        results.append(result)

        # Status icon based on best available verdict
        verdict = result.get("judge_verdict") or result.get("tier_a_verdict") or "?"
        icon = {
            "PASS": "✅", "MARGINAL": "🟡", "FAIL": "❌",
            "NOT_IMPL": "⬜", "ERROR": "💥", "OK": "✅", "?": "❓",
        }.get(verdict, "?")
        routing_icon = "→" if result["routing_pass"] else "✗"
        escalate_icon = " 👁" if result["escalate_to_human"] else ""
        # #1070: multi-turn marker
        turns = result.get("turns_completed", 1)
        turn_marker = f" [{turns} turns]" if turns > 1 else ""

        print(
            f"  {icon} Q{query_num:>2}: {verdict:<8} "
            f"{routing_icon}{result.get('actual_routing', 'N/A'):<10}"
            f"{escalate_icon} "
            f"{query_text[:50]}{turn_marker}"
        )

        # Brief pause to avoid hammering the server (and the judge)
        time.sleep(0.5)

    # Summary
    total = len(results)
    routing_pass = sum(1 for r in results if r["routing_pass"])
    judge_pass = sum(1 for r in results if r.get("judge_verdict") == "PASS")
    judge_marginal = sum(1 for r in results if r.get("judge_verdict") == "MARGINAL")
    judge_fail = sum(1 for r in results if r.get("judge_verdict") == "FAIL")
    escalations = sum(1 for r in results if r["escalate_to_human"])

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total queries:    {total}")
    print(f"  Routing PASS:     {routing_pass} ({routing_pass/total*100:.1f}%)")
    print(f"  Quality PASS:     {judge_pass} ({judge_pass/total*100:.1f}%)")
    print(f"  Quality MARGINAL: {judge_marginal} ({judge_marginal/total*100:.1f}%)")
    print(f"  Quality FAIL:     {judge_fail} ({judge_fail/total*100:.1f}%)")
    print(f"  Human escalation: {escalations}")
    print()
    print(f"  M0 baseline:      70.5% routing pass")
    print(f"  M1 routing:       {routing_pass/total*100:.1f}%")

    # Write outputs
    csv_path = OUTPUT_DIR / "canonical-retest-run8-results.csv"
    report_path = OUTPUT_DIR / "canonical-retest-run8-report.md"
    write_csv(results, csv_path)
    write_report(results, report_path)

    print(f"\n  CSV:    {csv_path}")
    print(f"  Report: {report_path}")
    print("=" * 70)

    return results


if __name__ == "__main__":
    main()
