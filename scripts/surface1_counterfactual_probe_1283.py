"""Surface-1 counterfactual probe — what would the LLM classifier (surface 2)
have done with the utterances the deterministic pre-classifier (surface 1)
currently CLAIMS?

Arch ruling 2026-08-08 (mailboxes/arch/sent/ruling-arch-to-lead-…-narrowing-
surface-1-…-2026-08-08.md): "Do not narrow surface 1 yet. Make its claims
observable first." Surface 1's claims are unfalsifiable in production — when it
claims an utterance, the LLM never sees the phrase, so "the LLM would have
gotten it right/wrong" is unmeasurable. This probe measures it, one-off,
out-of-CI (Arch-ratified for this purpose, scoped to surface-1-claimed
utterances).

Per-utterance verdict:
- AGREE    — LLM emits the same action surface 1 claims (category noted if it
             drifts).
- VARIANT  — same semantic target, paraphrase-drift action name (mode-4 data).
             Mechanical test: same rail handler (alias equivalence via
             get_action_workflows(), the routing_probe_1283 _same_handler
             precedent) OR same category + content-token stem match.
- DISAGREE — different destination.
- ERROR    — the LLM call failed; never a faked verdict.

Denominator (stated, per the ruling's "say the denominator" instruction):
(a) every POINTER row in services/intent_service/chat_pointers.py whose
    utterance surface 1 claims (pre_classify returns non-None) — includes the
    pin: namespace rows; POINTER rows that resolve via surfaces 3/4 instead
    are excluded and counted.
(b) ONE hand-written canonical representative per pre-classifier pattern
    group/sub-action not already covered by (a), asserted at build time to be
    claimed by pre_classify with the expected (category, action). We probe ONE
    representative per group, NOT the infinite pattern space — a group verdict
    generalizes only as far as its representative does.

The counterfactual seam: IntentClassifier.classify() runs Stage 0 (B3) → cache
→ Stage 1 (PreClassifier.pre_classify) → Stage 2 (LLM via
_classify_with_reasoning + action normalization + verb-shim + vague-check). We
obtain the LLM-ONLY result by calling classify() with
PreClassifier.pre_classify monkeypatched to return None — so the FULL
production Stage-2 path runs (normalization map, #1124 verb shim, low-
confidence clarification), which a direct _classify_with_reasoning() call
would skip. B3 self-bypasses (user_id/session_id are None → D1a early return,
classifier.py:203); the cache is bypassed with use_cache=False. The patch is
verified live: a counter asserts the patched pre_classify was consulted on
every classify() call, and every probed utterance is one surface 1 claims —
so any non-ERROR answer is, by construction, the LLM's.

m-43 layer note: this measures the LLM classifier with EMPTY conversation
context (no context/session/spatial_context). That is D4's real shape — the
production classifier never sees history either (intent-routing-stack.md,
surface 0 note) — so the counterfactual matches the classifier's actual
production input shape, not an impoverished lab version of it.

Run (env-stripped per CLAUDE.md — inherited empty ANTHROPIC_API_KEY shadows
the env fallback; keychain resolves first):

    env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN \
      -u ANTHROPIC_CUSTOM_HEADERS POSTGRES_PORT=5433 \
      venv/bin/python scripts/surface1_counterfactual_probe_1283.py \
      [--dry-run] [--out report.md]

--dry-run builds + asserts the claimed-utterance set (no LLM calls, keyless).
Cost: exactly one LLM call per utterance (count printed in the report header).
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DEFAULT_OUT = (
    PROJECT_ROOT
    / "docs"
    / "internal"
    / "architecture"
    / "current"
    / "surface1-counterfactual-results-2026-08-08.md"
)

# ---------------------------------------------------------------------------
# (b) group representatives — ONE canonical utterance per pre-classifier
# pattern group / sub-action. Each row: (group, utterance, expected_category
# IntentCategory.value, expected_action). Asserted against the live
# pre_classify at build time; a mismatch fails the run BEFORE any LLM call.
# Groups already covered by a ledger POINTER utterance in (a) are marked so in
# the comment and carry no row here (dedup happens by utterance anyway).
# ---------------------------------------------------------------------------
GROUP_REPRESENTATIVES = [
    ("greeting", "hello", "conversation", "greeting"),
    ("farewell", "goodbye", "conversation", "farewell"),
    ("thanks", "thank you!", "conversation", "thanks"),
    ("discovery", "what can you do?", "discovery", "get_capabilities"),
    ("provenance", "why did you suggest that?", "provenance", "explain_suggestion"),
    ("trust", "why can't you create issues?", "trust", "explain_trust"),
    # insight-pull: covered by (a) "what have you learned about my work style?"
    ("memory", "what do you remember about me?", "memory", "get_memory"),
    ("get-default-repo", "what's my default repo?", "query", "get_default_repo"),
    (
        "set-default-repo",
        "set my default repo to mediajunkie/piper-morgan-product",
        "query",
        "set_default_repo",
    ),
    (
        "stakeholder-update",
        "write a short update for the CEO on the beta",
        "query",
        "write_stakeholder_update",
    ),
    (
        "document-query",
        "update the roadmap doc with the new dates",
        "query",
        "update_document_query",
    ),
    # repo-management: covered by (a) "add a repo to my portfolio"
    # portfolio: covered by (a) "list my projects"
    (
        "feature-info",
        "tell me more about the github integration",
        "query",
        "get_feature_info",
    ),
    ("identity", "who are you?", "identity", "get_identity"),
    ("contextual/changes", "what changed since yesterday?", "query", "changes_query"),
    ("contextual/attention", "what needs my attention?", "query", "attention_query"),
    ("calendar/meeting_time", "what's on my calendar today?", "query", "meeting_time"),
    (
        "calendar/recurring",
        "show my recurring meetings",
        "query",
        "recurring_meetings",
    ),
    ("calendar/week", "what's my week look like?", "query", "week_calendar"),
    (
        "milestone-status (#1068)",
        "what's the next milestone?",
        "status",
        "get_project_status",
    ),
    ("local-git (#1044)", "what branch are we on?", "query", "local_git_status_query"),
    ("github/shipped", "what did we ship this week?", "query", "shipped_query"),
    ("github/stale-prs", "show stale prs", "query", "stale_prs_query"),
    ("github/close-issue", "close issue #123", "query", "close_issue_query"),
    ("github/reopen-issue", "reopen issue #123", "query", "reopen_issue_query"),
    ("github/comment-issue", "comment on issue #123", "query", "comment_issue_query"),
    (
        "github/list-issues",
        "how many open issues do we have?",
        "query",
        "list_issues_query",
    ),
    ("github/list-prs", "show my prs", "query", "list_prs_query"),
    ("github/review-issue", "show issue #123", "query", "review_issue_query"),
    # NOTE: on the single-intent path the milestone/release/label/branch
    # listing patterns fall through pre_classify's elif chain to
    # review_issue_query; only detect_multiple_intents' _get_github_action
    # emits list_milestones_query etc. The claim recorded is the real
    # single-intent claim; the multi-path column shows the divergence.
    ("github/milestones", "show milestones", "query", "review_issue_query"),
    (
        "session-activity (#1394)",
        "what did we create this session?",
        "query",
        "session_activity_query",
    ),
    ("productivity", "what's my productivity?", "query", "productivity_query"),
    # reminder-query (#1521): covered by (a) pin "what reminders do I have?"
    (
        "reminder-create (#903)",
        "remind me to review the roadmap tomorrow",
        "execution",
        "create_reminder",
    ),
    ("todo-complete (#904)", "complete todo 3", "execution", "complete_todo"),
    # todo-query/list: covered by (a) "show me my todos"
    ("todo-query/completed", "show all my todos", "query", "list_completed_todos"),
    ("todo-query/next", "what's my next todo?", "query", "next_todo_query"),
    (
        "completion-history (#1117)",
        "when did I complete the onboarding project?",
        "status",
        "check_completion_status",
    ),
    # integration-connect (#1417/#1471): covered by (a) connect rows
    ("temporal", "what time is it?", "temporal", "get_current_time"),
    ("guidance", "how do I get started?", "guidance", "get_contextual_guidance"),
    ("analysis", "what's blocking the milestone?", "analysis", "analyze_blockers"),
    ("status", "what am I working on?", "status", "get_project_status"),
    ("priority", "what are my priorities?", "priority", "get_top_priority"),
]

# Tokens carrying no semantic target in an action name — stripped before the
# stem comparison the VARIANT test uses.
_STOP_TOKENS = {"get", "show", "list", "view", "query", "my", "me", "check", "fetch", "display"}


def _stems(action: str) -> frozenset:
    toks = set()
    for t in (action or "").lower().split("_"):
        if not t or t in _STOP_TOKENS:
            continue
        toks.add(t[:-1] if t.endswith("s") and len(t) > 3 else t)
    return frozenset(toks)


def build_utterance_set():
    """Build the claimed-utterance set. Returns (rows, excluded_pointers) where
    rows = list of dicts with utterance/source/claim (asserted), and
    excluded_pointers = POINTER rows surface 1 does NOT claim (resolve via
    surfaces 3/4)."""
    from services.intent_service.chat_pointers import CHAT_POINTERS, POINTER
    from services.intent_service.pre_classifier import PreClassifier

    rows = []
    seen = {}
    excluded = []

    # (a) ledger POINTER rows (incl. pin: namespace)
    for key, row in CHAT_POINTERS.items():
        if not isinstance(row, POINTER):
            continue
        u = row.utterance
        claim = PreClassifier.pre_classify(u)
        if claim is None:
            excluded.append((key, u))
            continue
        if u in seen:
            seen[u]["source"] += f", {key}"
            continue
        exp_cat, exp_act = row.expects
        got = (claim.category.value, claim.action)
        assert got == (exp_cat, exp_act), (
            f"POINTER {key!r} utterance {u!r}: pre_classify claims {got}, "
            f"ledger expects {(exp_cat, exp_act)}"
        )
        entry = {
            "utterance": u,
            "source": f"(a) {key}",
            "claim_cat": claim.category.value,
            "claim_action": claim.action,
        }
        seen[u] = entry
        rows.append(entry)

    # (b) group representatives (dedup against (a) by utterance)
    for group, u, exp_cat, exp_act in GROUP_REPRESENTATIVES:
        if u in seen:
            seen[u]["source"] += f", (b) {group}"
            continue
        claim = PreClassifier.pre_classify(u)
        assert claim is not None, f"group {group!r}: pre_classify does NOT claim {u!r}"
        got = (claim.category.value, claim.action)
        assert got == (exp_cat, exp_act), (
            f"group {group!r} utterance {u!r}: pre_classify claims {got}, "
            f"expected {(exp_cat, exp_act)}"
        )
        entry = {
            "utterance": u,
            "source": f"(b) {group}",
            "claim_cat": exp_cat,
            "claim_action": exp_act,
        }
        seen[u] = entry
        rows.append(entry)

    # surface-1's OTHER entry point: detect_multiple_intents primary claim
    for entry in rows:
        multi = PreClassifier.detect_multiple_intents(entry["utterance"])
        primary = multi.primary_intent
        if primary is None:
            entry["multi"] = "—"
        else:
            m = (primary.category.value, primary.action)
            entry["multi"] = (
                "same"
                if m == (entry["claim_cat"], entry["claim_action"])
                else f"{m[0]}/{m[1]}"
            )
    return rows, excluded


def judge(claim_cat, claim_action, llm_cat, llm_action, workflows) -> str:
    if llm_action == claim_action:
        return "AGREE" if llm_cat == claim_cat else f"AGREE(action; category {llm_cat})"
    # alias equivalence: both names dispatch to the same rail handler
    ha, hb = workflows.get(claim_action), workflows.get(llm_action)
    if ha is not None and ha is hb:
        return "VARIANT(rail-alias: same handler)"
    if llm_cat == claim_cat:
        sa, sb = _stems(claim_action), _stems(llm_action)
        if sa and sb and (sa <= sb or sb <= sa):
            return "VARIANT(stem-match)"
    return "DISAGREE"


async def run(dry_run: bool, out_path: Path) -> int:
    rows, excluded = build_utterance_set()
    n_a = sum(1 for r in rows if r["source"].startswith("(a)"))
    n_b = len(rows) - n_a
    print(
        f"claimed-utterance set: {len(rows)} unique utterances "
        f"({n_a} from ledger POINTERs, {n_b} group representatives; "
        f"{len(excluded)} POINTER rows excluded as not surface-1-claimed)"
    )
    for key, u in excluded:
        print(f"  excluded (not claimed by surface 1): {key} -> {u!r}")
    if dry_run:
        for r in rows:
            print(
                f"  {r['claim_cat']}/{r['claim_action']:<28} multi={r['multi']:<28}"
                f" {r['utterance']!r}  [{r['source']}]"
            )
        print("dry-run complete: all claims asserted, no LLM calls made.")
        return 0

    from services.intent_service.classifier import IntentClassifier
    from services.intent_service.pre_classifier import PreClassifier
    from services.intent_service.workflow_dispatcher import get_action_workflows
    from services.intent_service.workflow_entries import register_default_workflows
    from services.llm.clients import LLMClient

    register_default_workflows()
    workflows = get_action_workflows()
    classifier = IntentClassifier(llm_service=LLMClient())

    # --- the bypass: surface 1 answers None for every message ---------------
    bypass_calls = {"n": 0}
    real_pre_classify = PreClassifier.pre_classify

    def _bypassed_pre_classify(message):
        bypass_calls["n"] += 1
        return None

    llm_calls = 0
    try:
        PreClassifier.pre_classify = staticmethod(_bypassed_pre_classify)
        for i, r in enumerate(rows, 1):
            expected_consultations = bypass_calls["n"] + 1
            try:
                llm_calls += 1
                intent = await classifier.classify(
                    r["utterance"], use_cache=False, user_id=None, session_id=None
                )
                # bypass verification: the patched surface 1 was consulted and
                # declined, so this answer is the LLM's (B3 self-bypassed with
                # no session; cache off). Every utterance here is one surface 1
                # claims — an answer at all proves the bypass is real.
                assert bypass_calls["n"] == expected_consultations, (
                    "bypass not consulted — classify() answered without passing "
                    "the patched pre_classify; result is NOT the LLM counterfactual"
                )
                r["llm_cat"] = intent.category.value
                r["llm_action"] = intent.action or ""
                r["llm_conf"] = round(float(intent.confidence or 0.0), 2)
                r["verdict"] = judge(
                    r["claim_cat"], r["claim_action"], r["llm_cat"], r["llm_action"], workflows
                )
            except AssertionError:
                raise
            except Exception as e:
                r["llm_cat"] = "—"
                r["llm_action"] = "—"
                r["llm_conf"] = ""
                r["verdict"] = f"ERROR: {type(e).__name__}: {e}"
            print(
                f"[{i}/{len(rows)}] {r['verdict']:<34} {r['utterance']!r} "
                f"claim={r['claim_cat']}/{r['claim_action']} "
                f"llm={r['llm_cat']}/{r['llm_action']}"
            )
    finally:
        PreClassifier.pre_classify = real_pre_classify

    agree = sum(1 for r in rows if r["verdict"].startswith("AGREE"))
    variant = sum(1 for r in rows if r["verdict"].startswith("VARIANT"))
    disagree = sum(1 for r in rows if r["verdict"] == "DISAGREE")
    errors = sum(1 for r in rows if r["verdict"].startswith("ERROR"))
    print(
        f"\n== {agree} AGREE / {disagree} DISAGREE / {variant} VARIANT / "
        f"{errors} ERROR of {len(rows)} ({llm_calls} LLM calls) =="
    )

    variants = [r for r in rows if r["verdict"].startswith("VARIANT")]
    lines = [
        "# Surface-1 counterfactual — what the LLM classifier would have done "
        "with surface 1's claims",
        "",
        f"Run: {datetime.now():%Y-%m-%d %H:%M} PT · "
        f"`scripts/surface1_counterfactual_probe_1283.py` · "
        f"Arch ruling 2026-08-08 (make surface 1's claims observable before narrowing).",
        "",
        "## Method",
        "",
        "- **Claim**: `PreClassifier.pre_classify(utterance)` (surface 1's "
        "single-intent entry); the multi-intent entry "
        "(`detect_multiple_intents` primary) is recorded in its own column "
        "where it diverges.",
        "- **Counterfactual**: `IntentClassifier.classify(utterance, "
        "use_cache=False)` with `PreClassifier.pre_classify` monkeypatched to "
        "return `None` — the full production Stage-2 LLM path runs "
        "(normalization map, #1124 verb shim, low-confidence clarification). "
        "B3/Stage-0 self-bypasses (no user/session → D1a early return); cache "
        "off. Bypass verified per call (patched surface 1 consulted, "
        "declined).",
        "- **m-43 layer note**: the LLM ran with EMPTY conversation context. "
        "That is D4's production shape — the classifier never sees history — "
        "so this is the classifier's real input shape, not a lab "
        "impoverishment.",
        "- **Verdicts**: AGREE = same action (category drift annotated). "
        "VARIANT = same semantic target under a paraphrase-drift name "
        "(mode-4): same rail handler via alias equivalence, or same category "
        "+ content-stem match. DISAGREE = different destination. ERROR = the "
        "call failed (never a faked verdict).",
        "",
        "## Denominator",
        "",
        f"- **{len(rows)} unique utterances probed**: {n_a} from "
        "`chat_pointers.py` POINTER rows surface 1 claims (incl. `pin:` "
        f"rows; duplicates deduped, ledger keys listed per row), plus {n_b} "
        "hand-written group representatives asserted at build time to be "
        "claimed with the expected (category, action).",
        f"- **{len(excluded)} POINTER rows excluded** (utterance resolves via "
        "surfaces 3/4, not surface 1)."
        + (
            " Excluded: " + "; ".join(f"`{k}` ({u!r})" for k, u in excluded)
            if excluded
            else ""
        ),
        "- **Scope caveat**: ONE representative per pre-classifier pattern "
        "group/sub-action — not the infinite pattern space. A group's verdict "
        "generalizes only as far as its representative does.",
        "",
        f"## Result: **{agree} AGREE / {disagree} DISAGREE / {variant} "
        f"VARIANT / {errors} ERROR** of {len(rows)}",
        "",
        f"Cost: {llm_calls} LLM classification calls (one per utterance, no "
        "retries).",
        "",
        "| # | utterance | surface-1 claim | multi-path claim | LLM verdict "
        "(cat/action @conf) | verdict |",
        "|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        llm_cell = (
            f"`{r['llm_cat']}/{r['llm_action']}` @{r['llm_conf']}"
            if not r["verdict"].startswith("ERROR")
            else "—"
        )
        lines.append(
            f"| {i} | {r['utterance']} | `{r['claim_cat']}/{r['claim_action']}` "
            f"| {r['multi']} | {llm_cell} | {r['verdict']} |"
        )
    lines += [
        "",
        "## Mode-4 variant list (paraphrase-drift emissions)",
        "",
    ]
    if variants:
        for r in variants:
            lines.append(
                f"- {r['utterance']!r}: claim `{r['claim_action']}` vs LLM "
                f"`{r['llm_action']}` ({r['verdict']})"
            )
    else:
        lines.append("- none observed in this run")
    lines += [
        "",
        "## Row sources",
        "",
    ]
    for r in rows:
        lines.append(f"- {r['utterance']!r} — {r['source']}")
    out_path.write_text("\n".join(lines) + "\n")
    print(f"report -> {out_path}")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    sys.exit(asyncio.run(run(args.dry_run, args.out)))
