"""#1567 — the repository clarification carrier + natural repo-name extraction.

PM's live transcript (2026-08-10, the #1411 retest): after the honest refusal
"Cannot update issue: repository not specified. Please specify which
repository." PM answered with "change the title of issue 108 in the
test-Piper-Morgan repository" — and got the SAME refusal. Two gaps, both
fixed here:

1. **The clarification never BOUND** — the refusal was a dead-end, not a
   slot-filling continuation. The update/close handlers now ARM a pending
   action in the #846 session-scoped offer store (kind ``issue_repo_question``,
   the action-agnostic #1190 carrier shape — the same idiom as
   ``unmapped_field_value_clarification``, ``reminder_clear_verb_question``
   and ``drafted_issue``) carrying the ORIGINAL classified Intent. The next
   turn's answer binds the repository into that Intent's context and
   re-dispatches it through ``run_confirm_pending_action_workflow`` (the
   #1190 acceptance mirror) — the answer is never re-classified, and the
   operation proceeds with the ORIGINAL parameters (title, issue number).

2. **Natural repo phrasing was never extracted** — only the compressed
   ``owner/name`` pair parsed. ``extract_natural_repo_name`` now reads
   "in the test-Piper-Morgan repository", "the repo called X", quoted names,
   case-insensitively; a bare name resolves against the user's actual repos
   (default-repo name match first — no network — then the #1327
   ``search_user_repositories`` rail). Extraction runs on the ORIGINAL ask
   too, so a fully-phrased request never sees the question at all.

Safety properties (the fail-safe DIRECTION, same as ``resolve_repo``'s
callers): a bare name only ACTS when it resolves to exactly one of the
user's real repositories — no match / ambiguous / repos-unreadable each
re-arm the question with honest, distinct copy (m-43: the "couldn't check"
copy never claims a search that didn't run). A user-NAMED repo is never
silently second-guessed by the default repo — naming a repo we can't find
asks, it does not fall through to the default (the wrong-repo write is the
worse failure). When a default repo exists, the failed-name ask offers it
as a closed question ("say 'yes' to use your default, owner/name") per the
#1411 default-repo integration.

Turn discrimination at the pop seam (inherits #1631 via the generic seam):

- declines / bare exits fall through to the generic decline path (honest
  drop via ``decline_message``);
- a bare "yes" against the OPEN question falls to the generic accept path,
  whose ``CONFIRM_PENDING_ACTION_WORKFLOW`` dispatch re-runs the ORIGINAL
  handler — which finds the repository still missing and re-asks (the
  self-re-arming property; no separate re-ask workflow needed);
- an unrelated command mid-ask (different issue number, or an anchored
  imperative outside the pending operation's own verb family) returns None
  → off-intent abandons per the carrier's rules and the turn routes
  normally through the 4-surface chain;
- a RE-STATEMENT of the same operation ("change the title of issue 108 in
  the test-Piper-Morgan repository" — PM's literal turn) binds: same issue
  number, same verb family, repo extracted; any title/body the restatement
  carries is merged via the same ``_slotfill_issue_request`` extraction the
  original ask used (newer values win).

Known limits, stated honestly: a single bare token that is not a repo
("banana") re-arms with the honest not-found copy rather than routing —
with a repo question armed, a one-word turn is far more likely a repo
answer than a new intent, and the miss is recoverable (nothing writes).

#1641 (2026-08-18): the carrier now also serves the reopen/comment handlers
and the three ANALYSIS repository dead-ends (analyze_commits /
generate_report / analyze_data), plus natural-phrasing extraction on the
create path. The ANALYSIS/create asks have no issue number — the offer's
``issue_number=None`` + ``operation`` form carries the copy, and the pop
seam's different-issue-number guard is skipped for them.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

import structlog

from services.intent_service.destructive_confirm import (
    CONFIRM_PENDING_ACTION_WORKFLOW,
)

logger = structlog.get_logger(__name__)

REPO_QUESTION_KIND = "issue_repo_question"

# ── Extraction patterns ──────────────────────────────────────────────────────

# owner/name — URL form first, then the domain-guarded bare pair (both are
# the proven shapes from IntentService._slotfill_issue_request).
_URL_REPO_RE = re.compile(r"github\.com/([A-Za-z0-9._-]+/[A-Za-z0-9._-]+)")
_OWNER_REPO_RE = re.compile(
    r"(?<![./\w])((?=[A-Za-z0-9-]*[A-Za-z])[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?"
    r"/[A-Za-z0-9._-]+)\b"
)

# Natural phrasing: `in the test-Piper-Morgan repository`, `on the X repo`.
# The captured token must survive the stoplist below ("in my default
# repository" is the DEFAULT-repo phrase, not a name — #1411's resolver
# handles it).
_NATURAL_IN_RE = re.compile(
    r"\b(?:in|into|inside|on|for|from|to)\s+(?:the\s+|my\s+|our\s+)?"
    r"[\"'‘“]?([A-Za-z0-9][A-Za-z0-9._-]{0,99})[\"'’”]?"
    r"\s+(?:repository|repo)\b",
    re.IGNORECASE,
)
# `the repository called/named X`
_NATURAL_CALLED_RE = re.compile(
    r"\b(?:repository|repo)\s+(?:called|named)\s+"
    r"[\"'‘“]?([A-Za-z0-9][A-Za-z0-9._/-]{0,99})[\"'’”]?",
    re.IGNORECASE,
)
# Answer-only anchored forms: `the X repository`, `use X`, `it's (in) X`,
# a quoted name alone, a bare token alone.
_ANSWER_THE_X_REPO_RE = re.compile(
    r"^(?:it'?s\s+)?(?:the\s+)?"
    r"[\"'‘“]?([A-Za-z0-9][A-Za-z0-9._-]{0,99})[\"'’”]?"
    r"\s+(?:repository|repo)\s*[.!?]*$",
    re.IGNORECASE,
)
_ANSWER_LEAD_IN_RE = re.compile(
    r"^(?:use|try|it'?s(?:\s+in)?|in)\s+(?:the\s+|my\s+)?"
    r"[\"'‘“]?([A-Za-z0-9][A-Za-z0-9._/-]{0,99})[\"'’”]?"
    r"\s*[.!?]*$",
    re.IGNORECASE,
)
_ANSWER_QUOTED_RE = re.compile(r"^[\"'‘“]([A-Za-z0-9][A-Za-z0-9._/-]{0,99})[\"'’”]\s*[.!?]*$")
_ANSWER_BARE_TOKEN_RE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]{1,99})\s*[.!?]*$")

# Words that can occupy the name slot without naming a repo. "default" is
# load-bearing: "in my default repository" must fall to the #1411 resolver,
# never read as a repo literally named "default".
_STOP_NAMES = frozenset(
    {
        "default",
        "same",
        "that",
        "this",
        "it",
        "current",
        "usual",
        "my",
        "your",
        "our",
        "the",
        "a",
        "an",
        "any",
        "some",
        "which",
        "what",
        "one",
        "right",
        "wrong",
        "other",
        "another",
        "new",
        "github",
        "git",
        "main",
        "first",
        "last",
        "own",
        "correct",
        # bare-token non-answers that must fall to the generic seam
        "yes",
        "yeah",
        "yep",
        "no",
        "nope",
        "ok",
        "okay",
        "sure",
        "thanks",
        "thank",
        "hmm",
        "hi",
        "hello",
        "help",
        "why",
        "how",
        "huh",
        "please",
        "cancel",
        "stop",
        "nevermind",
    }
)

# Issue-number mentions, guarded so `repo2`'s digits don't read as one.
_ISSUE_NUM_RE = re.compile(r"(?<![\w/-])#?(\d{1,7})\b")

# Anchored-imperative lead verb (prefix structure mirrors
# collaboration_gate._EXECUTE_RE / drafted_issue._COMMAND_SUPPLEMENT_RE).
_LEAD_VERB_RE = re.compile(
    r"^\s*"
    r"(?:(?:please|hey|hi|ok(?:ay)?|piper)[,!\s]+)*"
    r"(?:go\s+ahead\s+and\s+)?"
    r"(?:(?:can|could|would|will)\s+you\s+(?:please\s+)?)?"
    r"([a-zA-Z]+)\b"
)
_IMPERATIVE_VERBS = frozenset(
    {
        "close",
        "reopen",
        "delete",
        "remove",
        "archive",
        "restore",
        "cancel",
        "stop",
        "list",
        "show",
        "search",
        "find",
        "fetch",
        "get",
        "check",
        "tell",
        "give",
        "create",
        "file",
        "open",
        "add",
        "update",
        "change",
        "rename",
        "edit",
        "modify",
        "set",
        "make",
        "write",
        "draft",
        "comment",
        "assign",
        "label",
        "remind",
        "summarize",
    }
)

# The pending operation's OWN verb family — a re-statement leading with one
# of these is an answer, not a new command.
_UPDATE_FAMILY = frozenset({"change", "update", "rename", "edit", "modify", "set"})
_CLOSE_FAMILY = frozenset({"close"})
_REOPEN_FAMILY = frozenset({"reopen"})
# #1641: the newly-wired carriers' families. Comment restatements lead with
# "comment"/"add"; report/create restatements lead with make-verbs; the
# analyze verbs aren't in _IMPERATIVE_VERBS at all (they can't be blocked),
# listed for documentation/symmetry.
_COMMENT_FAMILY = frozenset({"comment", "add", "reply"})
_REPORT_FAMILY = frozenset({"generate", "create", "make", "write"})
_ANALYZE_FAMILY = frozenset({"analyze", "analyse", "evaluate"})
_CREATE_FAMILY = frozenset({"create", "file", "open", "make", "write", "draft", "add"})

# Trailing repo-routing clause a slot-filled TITLE must never swallow:
# `... to Testing in the test-piper-morgan repository` / `... in owner/repo`.
# Requires the owner/name slash OR the repository/repo noun — a plain
# `... in Chrome` tail is title content, not routing.
_TRAILING_REPO_CLAUSE_RE = re.compile(
    r"\s+in\s+(?:the\s+|my\s+|our\s+)?"
    r"(?:"
    r"(?:(?:https?://)?github\.com/)?[A-Za-z0-9._-]+/[A-Za-z0-9._-]+(?:\.git)?"
    r"|[\"'‘“]?[A-Za-z0-9][A-Za-z0-9._-]{0,99}[\"'’”]?\s+(?:repository|repo)"
    r")\s*$",
    re.IGNORECASE,
)


def restatement_verbs_for(action: Optional[str]) -> Tuple[str, ...]:
    """The pending operation's own verb family (re-statements bind).

    #1641 ordering notes: "close"/"reopen" first (unambiguous); "comment"
    before the create family ("add_comment" must read as comment, not add);
    "report" before "create" ("create_report" is the report cohort's alias,
    not an issue-create)."""
    a = (action or "").lower()
    if "close" in a:
        return tuple(_CLOSE_FAMILY)
    if "reopen" in a:
        return tuple(_REOPEN_FAMILY)
    if "comment" in a:
        return tuple(_COMMENT_FAMILY)
    if "report" in a:
        return tuple(_REPORT_FAMILY)
    if "analyze" in a or "analyse" in a or "metrics" in a or "evaluate" in a:
        return tuple(_ANALYZE_FAMILY)
    if "create" in a or "ticket" in a:
        return tuple(_CREATE_FAMILY)
    return tuple(_UPDATE_FAMILY)


def strip_trailing_repo_clause(title: str) -> str:
    """Remove a trailing `in [the] X repository` / `in owner/repo` routing
    clause from an unquoted slot-filled title — it is repo routing, not
    subject (#1567; the about-form already stripped the owner/name shape)."""
    return _TRAILING_REPO_CLAUSE_RE.sub("", title).strip()


def strip_repo_phrase_for(title: str, repository: Optional[str]) -> str:
    """#1543 REWORK (PM live 2026-08-29, v64): remove a trailing routing
    phrase that NAMES the repo the write actually targets — `…the login
    timeout in test-piper-morgan` when the issue is being created in
    mediajunkie/test-piper-morgan.

    ``strip_trailing_repo_clause`` handles the shapes that are
    self-evidently repos at extraction time (owner/name, `… the X
    repository`). A BARE name is only knowable as routing once the target
    repo is resolved, so this runs at the handler AFTER resolution (named
    or default — PM's live case was the default repo coinciding with the
    named one). Pure function; phrases naming anything else are left alone
    (never guess), and a title that is nothing but the phrase is returned
    unchanged rather than emptied."""
    if not title or not repository or "/" not in repository:
        return title
    name = repository.split("/", 1)[1]
    for target in (repository, name):
        pat = re.compile(
            r"[\s,]+(?:in|into|inside|on|for|to)\s+(?:the\s+|my\s+|our\s+)?"
            r"[\"'‘“]?" + re.escape(target) + r"[\"'’”]?"
            r"(?:\s+(?:repository|repo))?\s*$",
            re.IGNORECASE,
        )
        stripped = pat.sub("", title).strip().rstrip(" .!?,;:")
        if stripped and stripped != title:
            return stripped
    return title


def _clean_name(candidate: str) -> Optional[str]:
    name = candidate.strip().strip("\"'‘’“”").rstrip(" .!?,;:")
    if not name or not re.search(r"[A-Za-z]", name):
        return None
    if name.lower() in _STOP_NAMES:
        return None
    return name


def extract_natural_repo_name(message: Optional[str]) -> Optional[str]:
    """Natural repo phrasing in an ORIGINAL ask (or an answer): returns a
    bare repo name ("test-Piper-Morgan") or an owner-qualified full name
    when the phrase carried one. None when nothing repo-shaped is phrased.

    Does NOT scan for a free-standing ``owner/name`` pair — the callers'
    existing ``_slotfill_issue_request`` already owns that shape."""
    text = (message or "").strip()
    if not text:
        return None
    for pattern in (_NATURAL_IN_RE, _NATURAL_CALLED_RE):
        m = pattern.search(text)
        if m:
            name = _clean_name(m.group(1))
            if name:
                return name
    return None


def extract_repo_answer(message: str, *, allow_bare_token: bool = True) -> Optional[str]:
    """Extract the repo reference from an ANSWER turn to the repo question.

    Accepts owner/name (bare or URL), the natural phrasings, quoted names,
    `use X` / `it's X` lead-ins, and (when ``allow_bare_token``) a single
    bare token. Returns the reference (full name when owner-qualified, else
    bare name), or None when the turn carries nothing repo-shaped."""
    text = (message or "").strip()
    if not text:
        return None
    m = _URL_REPO_RE.search(text)
    if m:
        return m.group(1).removesuffix(".git")
    m = _OWNER_REPO_RE.search(text)
    if m:
        return m.group(1).removesuffix(".git")
    natural = extract_natural_repo_name(text)
    if natural:
        return natural
    for pattern in (_ANSWER_THE_X_REPO_RE, _ANSWER_LEAD_IN_RE, _ANSWER_QUOTED_RE):
        m = pattern.match(text)
        if m:
            name = _clean_name(m.group(1))
            if name:
                return name
    if allow_bare_token:
        m = _ANSWER_BARE_TOKEN_RE.match(text)
        if m:
            return _clean_name(m.group(1))
    return None


# ── Bare-name resolution against the user's actual repos ─────────────────────


@dataclass
class RepoNameResolution:
    """Outcome of resolving a bare repo name against the user's repos.

    status: "resolved" | "ambiguous" | "not_found" | "unavailable".
    ``unavailable`` means the repos could NOT be read (no principal, degrade,
    or error) — m-43: distinct from ``not_found`` (searched, absent), and its
    copy must never claim a search that didn't run."""

    status: str
    full_name: Optional[str] = None
    candidates: List[str] = field(default_factory=list)


async def resolve_repo_name(user_id: Optional[str], name: str) -> RepoNameResolution:
    """Resolve a bare repo name ("test-Piper-Morgan") to ``owner/name``.

    Case-insensitive. Default-repo name match first (no network — the #1042
    rail's store), then the user's own repos via the #1327
    ``search_user_repositories`` rail. Never raises; failure directions all
    land on honest non-acting statuses."""
    if "/" in name:
        return RepoNameResolution(status="resolved", full_name=name)
    wanted = name.lower()

    uid: Optional[UUID] = None
    try:
        uid = UUID(str(user_id)) if user_id else None
    except (ValueError, TypeError):
        uid = None

    if uid is not None:
        try:
            from services.integrations.github.repo_resolver import (
                get_user_default_repo,
            )

            default = await get_user_default_repo(uid)
            if default and default.split("/", 1)[1].lower() == wanted:
                return RepoNameResolution(status="resolved", full_name=default)
        except Exception as e:  # silent-ok: default-name match is an optimization; the repo search below is the real lookup
            logger.debug("repo_name_default_match_failed", error=str(e))

    if uid is None:
        return RepoNameResolution(status="unavailable")

    try:
        from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

        result = await GitHubMCPSpatialAdapter().search_user_repositories(str(uid))
        if result.degradation is not None:
            return RepoNameResolution(status="unavailable")
        matches = sorted(
            {
                str(full_name)
                for r in (result.repositories or [])
                if (r.get("name") or "").lower() == wanted and (full_name := r.get("full_name"))
            }
        )
    except Exception as e:  # silent-ok: fail-safe DIRECTION — an unreadable repo list must degrade to the honest ask, never guess a WRITE target
        logger.warning("repo_name_resolution_search_failed", error=str(e))
        return RepoNameResolution(status="unavailable")

    if len(matches) == 1:
        return RepoNameResolution(status="resolved", full_name=matches[0])
    if matches:
        return RepoNameResolution(status="ambiguous", candidates=matches)
    return RepoNameResolution(status="not_found")


# ── Question copy (one home; the honest per-status variants) ─────────────────


def open_repo_question(issue_number: Optional[int], operation: Optional[str] = None) -> str:
    """#1641: ``issue_number=None`` is the non-issue-anchored form (the
    ANALYSIS/create carriers have no issue to name); ``operation`` is the
    human phrase for what's pending ("analyze commits")."""
    if issue_number is not None:
        head = f"Which repository is issue #{issue_number} in?"
    elif operation:
        head = f"Which repository should I use to {operation}?"
    else:
        head = "Which repository should I use?"
    return (
        f"{head} Give me the "
        f"owner/name (like octocat/hello-world) — or just the repo name "
        f"and I'll find it among your repositories."
    )


def repo_resolution_question(
    name: str, resolution: RepoNameResolution, default_repo: Optional[str] = None
) -> str:
    """The ask copy after a bare name failed to resolve — per-status, honest
    about what was actually checked (m-43/m-44)."""
    if resolution.status == "ambiguous":
        listed = ", ".join(resolution.candidates[:5])
        return (
            f"'{name}' matches more than one of your repositories: {listed}. "
            f"Which owner/name should I use?"
        )
    if resolution.status == "unavailable":
        return (
            f"I couldn't check your repositories just now, so I can't look "
            f"up '{name}' by name alone. Give me the owner/name and I'll "
            f"proceed."
        )
    base = (
        f"I looked through your repositories and couldn't find one called "
        f"'{name}'. Give me the owner/name and I'll take it from there."
    )
    if default_repo:
        base += f" Or say 'yes' to use your default, {default_repo}."
    return base


def repo_question_decline_message(
    issue_number: Optional[int], operation: Optional[str] = None
) -> str:
    if issue_number is not None:
        return (
            f"Okay — I haven't touched issue #{issue_number}. Name the "
            f"repository (owner/name) if you want to pick this back up."
        )
    if operation:
        return (
            f"Okay — I've left that alone. Name the repository (owner/name) "
            f"if you want me to {operation} later."
        )
    return (
        "Okay — I've left that alone. Name the repository (owner/name) "
        "if you want to pick this back up."
    )


# ── Offer builder (the #1190 action-agnostic carrier shape) ──────────────────


def build_repo_question_offer(
    intent: Any,
    issue_number: Optional[int],
    principal: Optional[str],
    *,
    asked_name: Optional[str] = None,
    default_repo: Optional[str] = None,
    operation: Optional[str] = None,
    question: Optional[str] = None,
) -> Dict[str, Any]:
    """The #846 pending-offer record binding the ORIGINAL Intent while the
    repository slot fills. workflow_type is the #1190 confirm carrier, so a
    bare "yes" against the open question re-dispatches the original handler
    — which re-asks (self-re-arming; no separate re-ask workflow).

    #1641: ``issue_number=None`` + ``operation`` is the non-issue-anchored
    form (ANALYSIS/create) — the pop seam's different-issue-number guard is
    skipped for it, and the copy names the operation instead of an issue.

    ``question`` (#1665): the ALREADY-RENDERED ask the caller returns this
    turn (open_repo_question / repo_resolution_question output — the caller
    picked which form). Stored verbatim so the SessionSnapshot never drifts
    from what the user saw; the re-arm seams update it when the re-ask copy
    changes."""
    if issue_number is not None:
        summary = f"{intent.action} for issue #{issue_number}"
    else:
        summary = operation or intent.action
    return {
        "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
        "question": question,
        "pending_action": {
            "kind": REPO_QUESTION_KIND,
            "action": intent.action,
            "intent": intent,
            "summary": summary,
            "user_id": principal,
            "issue_number": issue_number,
            "asked_name": asked_name,
            "default_repo": default_repo,
            "operation": operation,
            "restatement_verbs": list(restatement_verbs_for(intent.action)),
        },
        "decline_message": repo_question_decline_message(issue_number, operation),
    }


# ── Pop-seam turn handling (kind-specific, BEFORE generic accept/decline) ────


def _principal_mismatch(payload: Dict[str, Any], user_id: Optional[str]) -> bool:
    """#1532: if the turn's principal differs from the offer's, nothing may
    bind or act."""
    offer_user = payload.get("user_id")
    principal = str(user_id) if user_id else None
    return bool(offer_user and principal and offer_user != principal)


def _pending_intent_data(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "category": "execution",
        "action": payload.get("action") or "update_issue",
        "issue_repo_question_pending": True,  # _apply_soft_offer clobber guard
    }


def _rearm(
    intent_service: Any,
    session_id: Optional[str],
    user_id: Optional[str],
    pending_offer: Dict[str, Any],
) -> bool:
    try:
        intent_service.workflow_offer_service.set_pending_offer(
            session_id, pending_offer, user_id=user_id
        )
        return True
    except Exception as e:  # silent-ok: a store failure must not crash the turn; logged ERROR and the copy stays honest (no false "ask again" claim)
        logger.error("repo_question_rearm_failed", error=str(e))
        return False


async def _bind_and_dispatch(
    pending_offer: Dict[str, Any],
    payload: Dict[str, Any],
    full_name: str,
    answer_text: Optional[str],
    *,
    session_id: Optional[str],
    user_id: Optional[str],
    intent_service: Any,
) -> Dict[str, Any]:
    """Bind the resolved repository into the ORIGINAL Intent and re-dispatch
    it through the #1190 acceptance mirror. A restatement's newer title/body
    slot-fills win. Failure re-arms the question — retry never loses the
    pending operation."""
    intent = payload.get("intent")
    if intent is None:
        logger.error("repo_question_missing_intent", session_id=session_id)
        return {
            "message": (
                "Something went sideways on my end and I lost track of the "
                "operation — nothing has been changed. Please give me the "
                "full request again."
            ),
            "intent_data": _pending_intent_data(payload),
        }
    intent.context = dict(intent.context or {})
    intent.context["repository"] = full_name
    if answer_text:
        try:
            slots = intent_service._slotfill_issue_request(answer_text)
        except (
            Exception
        ):  # silent-ok: slot merge is best-effort sugar; the bound repo is the load-bearing part
            slots = {}
        for key in ("title", "body"):
            if slots.get(key):
                intent.context[key] = slots[key]

    from services.intent_service.workflow_entries import (
        run_confirm_pending_action_workflow,
    )

    result: Optional[Dict[str, Any]] = None
    if session_id is None:
        # Structurally unreachable — an armed repo question is session-keyed
        # by construction (#846 store), so the answer turn always carries the
        # session. Narrowed explicitly (mypy); falls to the honest retry path.
        logger.error("repo_question_dispatch_no_session")
    else:
        try:
            result = await run_confirm_pending_action_workflow(
                session_id=session_id,
                user_id=user_id,
                context={"pending_action": payload, "intent_service": intent_service},
            )
        except Exception as e:  # silent-ok: a raised dispatch must not crash the answer turn; logged ERROR + traceback, honest retained copy below
            logger.error("repo_question_dispatch_raised", error=str(e), exc_info=True)
            result = None

    if result is None:
        # #1665: the re-armed record's open question is this turn's retry ask
        # (set BEFORE the store so what's stored is what's said).
        retry_ask = "Say the repository again (or 'no' to drop it) and I'll retry."
        pending_offer["question"] = retry_ask
        rearmed = _rearm(intent_service, session_id, user_id, pending_offer)
        tail = retry_ask if rearmed else "Please give me the full request again."
        logger.info(
            "repo_question_dispatch_failed",
            session_id=session_id,
            rearmed=rearmed,
        )
        return {
            "message": (
                f"I couldn't complete that against {full_name} just now — "
                f"nothing has been changed. {tail}"
            ),
            "intent_data": _pending_intent_data(payload),
        }

    logger.info(
        "repo_question_answer_bound",
        repository=full_name,
        action=payload.get("action"),
        session_id=session_id,
    )
    return result


async def handle_repo_question_turn(
    pending_offer: Dict[str, Any],
    message: str,
    *,
    session_id: Optional[str],
    user_id: Optional[str],
    intent_service: Any,
) -> Optional[Dict[str, Any]]:
    """Kind-specific turn handling for a pending repo question, run BEFORE
    generic accept/decline (the #1510/#1605/#1571 sanctioned seam — the pop
    already happened).

    Returns the acceptance-seam dict shape when this turn was consumed;
    None falls through to the generic offer flow (bare "yes" → the confirm
    workflow's re-dispatch re-asks; "no"/bare exit → honest decline copy;
    anything else — including unrelated commands, which keep routing — is
    abandoned via the pop, inheriting the #1631 prose/command discrimination
    ``detect_offer_response`` applies at the generic seam)."""
    payload = pending_offer.get("pending_action") or {}
    if payload.get("kind") != REPO_QUESTION_KIND:
        return None
    text = (message or "").strip()
    if not text:
        return None

    from services.intent_service.destructive_confirm import detect_bare_exit

    if detect_bare_exit(text):
        return None  # "cancel" / "forget it" → generic decline path

    if _principal_mismatch(payload, user_id):
        logger.warning(
            "repo_question_principal_mismatch",
            offer_user=payload.get("user_id"),
            turn_user=user_id,
        )
        return {
            "message": ("Let's hold off on that — nothing has been changed or stored."),
            "intent_data": {
                "category": "execution",
                "action": payload.get("action") or "update_issue",
                "principal_mismatch": True,
            },
        }

    from services.intent_service.soft_invocation import detect_offer_response

    resp = detect_offer_response(text)
    if resp == "decline":
        return None  # generic decline drops honestly via decline_message

    default_repo = payload.get("default_repo")

    # Unrelated command guards — BEFORE extraction, so "close issue #200 in
    # a/b" routes as a command instead of stealing the update's repo slot.
    nums = {int(n) for n in _ISSUE_NUM_RE.findall(text)}
    pending_number = payload.get("issue_number")
    if pending_number is not None and any(n != pending_number for n in nums):
        return None  # names a different issue → off-intent, routes normally
    m = _LEAD_VERB_RE.match(text)
    lead = m.group(1).lower() if m else None
    allowed = set(payload.get("restatement_verbs") or ())
    if lead and lead in _IMPERATIVE_VERBS and lead not in allowed:
        return None  # anchored imperative outside the pending family

    ref = extract_repo_answer(text, allow_bare_token=resp is None)
    if ref is None:
        # "yes" against the closed default question binds the default; the
        # open question's "yes" falls to the generic accept (self-re-ask).
        # #1650: binding the default FIRES the held update — a CONFIRM — so
        # only a crisp, full-message affirmative binds it. A greedy-row
        # pseudo-accept ("please note that…" under the #1631 floor) falls
        # through to None → the generic seam's off-intent rule (the pop
        # drops the question; the new turn routes normally).
        from services.intent_service.soft_invocation import (
            detect_confirm_response,
        )

        if detect_confirm_response(text) == "accept" and default_repo:
            return await _bind_and_dispatch(
                pending_offer,
                payload,
                default_repo,
                None,
                session_id=session_id,
                user_id=user_id,
                intent_service=intent_service,
            )
        # "use the default" without a bare "yes"
        if default_repo and re.search(r"\bdefault\b", text, re.IGNORECASE):
            return await _bind_and_dispatch(
                pending_offer,
                payload,
                default_repo,
                None,
                session_id=session_id,
                user_id=user_id,
                intent_service=intent_service,
            )
        return None  # not an answer → generic accept / off-intent flow

    if "/" in ref:
        return await _bind_and_dispatch(
            pending_offer,
            payload,
            ref,
            text,
            session_id=session_id,
            user_id=user_id,
            intent_service=intent_service,
        )

    principal = str(user_id) if user_id else payload.get("user_id")
    resolution = await resolve_repo_name(principal, ref)
    # ``and full_name``: a "resolved" status always carries one (see
    # resolve_repo_name) — the narrow is for mypy; the impossible
    # resolved-without-a-name shape re-arms honestly below.
    if resolution.status == "resolved" and resolution.full_name:
        return await _bind_and_dispatch(
            pending_offer,
            payload,
            resolution.full_name,
            text,
            session_id=session_id,
            user_id=user_id,
            intent_service=intent_service,
        )

    # Honest non-acting statuses: re-arm the SAME offer and say exactly what
    # was (and wasn't) checked. #1665: the re-ask copy is computed FIRST and
    # stored on the record as its open question — store what is said.
    copy = repo_resolution_question(ref, resolution, default_repo)
    pending_offer["question"] = copy
    rearmed = _rearm(intent_service, session_id, user_id, pending_offer)
    if not rearmed:
        copy += " (I couldn't keep the question pending — please give me the full request again.)"
    logger.info(
        "repo_question_name_unresolved",
        name=ref,
        status=resolution.status,
        session_id=session_id,
    )
    return {
        "message": copy,
        "intent_data": {
            **_pending_intent_data(payload),
            "requested_repo_name": ref,
            "repo_name_resolution": resolution.status,
        },
        "requires_clarification": True,
    }
