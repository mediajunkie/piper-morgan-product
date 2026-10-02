"""
CHAT_POINTERS — the product-surface chat-reachability ledger (#1433) and the
single source for the user-facing capability answer (#1428).

This module is imported by BOTH:

- ``tests/test_architecture_enforcement.py::TestChatPointersReachabilityRatchet``
  — the Arch-ratified (2026-08-02) product-inward reachability ratchet
  (docs/internal/architecture/current/chat-pointers-reachability-ratchet-design-1433.md).
  It derives the must-be-covered surface set at collection time and requires a
  ledger row per surface, so a POINTER here is a VERIFIED claim: its utterance
  resolves deterministically (no LLM) to its expected destination, or the
  build fails.
- ``services/intent_service/context_assembler.py`` — the DISCOVERY/IDENTITY
  ("what can you do?") answer path derives its capability list from the
  POINTER rows here via :func:`capability_answer_lines` (#1428, design §6
  step 3). A new capability joins the answer by getting a ledger row —
  membership by existing; no hand-maintained list can drift, and
  CHAT_INVISIBLE surfaces are never claimed.

Keep this module dependency-free (pure data + pure functions): the ratchet
runs keyless in gating CI, and the product import happens inside the intent
hot path.
"""

# ---------------------------------------------------------------------------
# Row types
# ---------------------------------------------------------------------------


class POINTER:
    """A canonical chat utterance that must route DETERMINISTICALLY to the
    surface's capability. `expects` is the (category, action) destination,
    lowercase category (IntentCategory.value)."""

    __slots__ = ("utterance", "expects")

    def __init__(self, utterance: str, expects: tuple):
        self.utterance = utterance
        self.expects = expects


class CHAT_INVISIBLE:
    """A surface deliberately or currently not reachable from chat.

    STRUCTURED citation required (Arch refinement 2, the ADR-079 `# global-ok:`
    shape): exactly one of
      - issue=N       — the tracked issue (the reachability gap's tracker, or
                        the surface-defining issue for by-design entries)
      - ref="ADR-NNN" — a ratified ADR/PDR that makes the surface web-only
      - untracked=True — BASELINE-ONLY escape hatch: the census found the gap
                        but no tracker exists yet. Valid ONLY for surfaces in
                        UNTRACKED_BASELINE below (frozen 2026-08-02, shrinks
                        only). A NEW chat-invisible surface must cite a real
                        issue or ADR — never add to the baseline.
    `note` is optional human context; it is NOT a citation and never
    satisfies the requirement (free-text reason = fail).
    """

    __slots__ = ("issue", "ref", "untracked", "note")

    def __init__(self, issue=None, ref=None, untracked=False, note=""):
        self.issue = issue
        self.ref = ref
        self.untracked = untracked
        self.note = note


# Surfaces the 2026-08-02 baseline found chat-invisible with NO tracked issue
# and no covering ADR/PDR (reported to Lead/PM in the #1433 build report).
# FROZEN: only remove entries (when a tracker is filed, swap the row to
# issue=N and delete the entry here). NEVER add.
UNTRACKED_BASELINE = frozenset(
    {
        "page:/personality-preferences",
        "page:/learning",
        "page:/settings",
        "page:/account",
        "page:/settings/llm-keys",
        "page:/lists",
        "page:/work-items",
        "page:/settings/privacy",
        "page:/settings/advanced",
        "capability:create_document",
        "capability:batch_create_issues",
    }
)


# ---------------------------------------------------------------------------
# THE LEDGER — every derived product surface gets exactly one row.
# POINTER utterances below are all VERIFIED against the live pre-classifier
# (2026-08-02); if one stops resolving, the ratchet harness fails loudly with
# the recorded resolution path.
#
# POINTER utterances are USER-FACING (#1428): they are surfaced verbatim as
# example asks in the "what can you do?" answer. Write them in user register —
# no issue numbers, no rail keys, no internal vocabulary.
# ---------------------------------------------------------------------------
CHAT_POINTERS = {
    # ---- pages (web/api/routes/ui.py GET page routes, derived) ----
    # Home hosts the inline chat itself (#1266 F2) — chat cannot "point to"
    # its own host surface.
    "page:/": CHAT_INVISIBLE(issue=1266, note="home hosts the inline chat"),
    "page:/login": CHAT_INVISIBLE(issue=393, note="pre-auth by definition"),
    "page:/reset-password": CHAT_INVISIBLE(issue=1261, note="pre-auth by definition"),
    "page:/setup": CHAT_INVISIBLE(issue=390, note="pre-auth setup wizard"),
    # #1595 Phase 3 seventh deletion (2026-10-02): STATUS_PATTERNS' standup
    # literal is gone, so this utterance no longer resolves at surface 1 — it
    # resolves through the deletion LEDGER (the ratchet's _phase3_ledger_resolve),
    # whose verified destination for "give me my standup" is show_standup: the
    # live read_status rail key the served router names @0.95 (ruled 10-01),
    # dispatched under QUERY (a rail key with no registry row takes the
    # grammar's category, else QUERY — inversion_live's own rule). The
    # utterance stays — it is what a user would actually type for this page —
    # and the expectation now says where it really goes.
    "page:/standup": POINTER("give me my standup", expects=("query", "show_standup")),
    "page:/personality-preferences": CHAT_INVISIBLE(untracked=True),
    "page:/learning": CHAT_INVISIBLE(untracked=True, note="dashboard-only today"),
    "page:/settings": CHAT_INVISIBLE(untracked=True, note="settings nav index"),
    "page:/account": CHAT_INVISIBLE(untracked=True, note="Coming Soon page"),
    "page:/transparency": CHAT_INVISIBLE(
        ref="ADR-063", note="user-facing audit-envelope READ surface (web-only)"
    ),
    "page:/files": CHAT_INVISIBLE(
        issue=1426,
        note="upload lives on /files; chat-side attachments unwired (census F5)",
    ),
    "page:/documents": CHAT_INVISIBLE(issue=1270, note="redirects to /files"),
    "page:/insights": POINTER(
        "what have you learned about my work style?", expects=("memory", "pull_insights")
    ),
    "page:/settings/integrations": POINTER(
        "connect my github", expects=("guidance", "get_contextual_guidance")
    ),
    "page:/settings/llm-keys": CHAT_INVISIBLE(
        untracked=True, note="api-keys census gap; page shipped in #1380"
    ),
    # #1876: reached deterministically through the time face — while the user
    # is on the DEFAULT zone the reply names it and points here. The chat
    # action ("set my timezone to <city>") also exists (set_timezone_entry)
    # but is LLM-classifier-resolved, so it is not the pointer's utterance.
    #
    # #1595 Phase 3 fourth deletion (2026-10-01): the pointer's utterance was
    # "what time is it for me?" — TEMPORAL_PATTERNS claimed it via a
    # substring match (r"\bwhat time is it\b") before that list was
    # tombstoned. The exact phrase was never itself a corpus row, so
    # TestChatPointersReachabilityRatchet's phase3-deletion-ledger resolver
    # (which requires an EXACT, already-scored corpus-row match — see
    # scripts/inversion_phase3_deletion_gate.py::_phase3_ledger_resolve) has
    # no evidence for it; depositing it as a brand-new corpus row would add
    # an UNSCORED row (no frozen router report has ever seen it, and scoring
    # one costs a live LLM call this unit's dispatch forbids), which would
    # fail check_deleted_entry_non_regression for the WHOLE TEMPORAL_PATTERNS
    # ledger entry, not just this phrase. Swapped to "what time is it?" —
    # already one of the ledger's 69 verified rows_claimed_at_deletion
    # (pre-existing, MATCH@0.99) — same destination, same pure-time-ask
    # shape, zero new corpus/scoring needed. The "for me" framing was
    # flavor text for this one example utterance, not load-bearing for the
    # page or the default-zone-copy behavior it demonstrates (see
    # tests/unit/services/intent_service/test_agenda_render_faces_1576.py::
    # TestDefaultZoneIsNamedNotAssumed, which constructs its own Intent
    # directly and is unaffected by this swap).
    "page:/settings/preferences": POINTER(
        "what time is it?", expects=("temporal", "get_current_time")
    ),
    "page:/settings/integrations/notion": POINTER(
        "connect my notion", expects=("guidance", "get_contextual_guidance")
    ),
    "page:/settings/integrations/github": POINTER(
        "connect my github", expects=("guidance", "get_contextual_guidance")
    ),
    "page:/settings/integrations/slack": POINTER(
        "connect my slack", expects=("guidance", "get_contextual_guidance")
    ),
    "page:/settings/integrations/calendar": POINTER(
        "link my google calendar", expects=("guidance", "get_contextual_guidance")
    ),
    "page:/settings/projects": POINTER(
        "add a repo to my portfolio", expects=("portfolio", "manage_repos")
    ),
    "page:/lists": CHAT_INVISIBLE(untracked=True, note="census direction-1 gap"),
    "page:/todos": POINTER("show me my todos", expects=("query", "list_todos_query")),
    "page:/projects": POINTER("list my projects", expects=("portfolio", "manage_portfolio")),
    "page:/projects/{project_id}": CHAT_INVISIBLE(
        issue=711, note="detail deep-link surface; list reachable via /projects pointer"
    ),
    "page:/work-items": CHAT_INVISIBLE(untracked=True, note="census direction-1 gap"),
    "page:/settings/privacy": CHAT_INVISIBLE(untracked=True, note="Coming Soon page"),
    "page:/settings/advanced": CHAT_INVISIBLE(untracked=True, note="Coming Soon page"),
    "page:/settings/connected-apps": CHAT_INVISIBLE(
        issue=1918, note="settings-only MCP-connection revoke surface; no chat utterance maps here"
    ),
    # ---- connectable integrations (settings_integrations.py, derived) ----
    "integration:github": POINTER(
        "connect my github", expects=("guidance", "get_contextual_guidance")
    ),
    "integration:slack": POINTER(
        "connect my slack", expects=("guidance", "get_contextual_guidance")
    ),
    # #1471: the NATURAL phrasing — pre-#1471 it collided with the temporal
    # calendar pattern (→ current time) and the ledger had to use the "link"
    # phrasing. Both phrasings are now pinned as POINTERs (this row + the
    # page:/settings/integrations/calendar row above) per the #1471 regression
    # requirement.
    "integration:calendar": POINTER(
        "connect my calendar", expects=("guidance", "get_contextual_guidance")
    ),
    "integration:notion": POINTER(
        "connect my notion", expects=("guidance", "get_contextual_guidance")
    ),
    # ---- capabilities named in decline copy (derived; unreachable BY
    #      DEFINITION — if one ships, its decline copy must be removed, which
    #      removes the surface from the derived set AND this row in the same
    #      commit, lowering the chat_invisible ceiling) ----
    # Real connector-backed chat writes ride the RECONNECT R2 epic (#1440;
    # #1322 Q3 is listed cross-cutting there).
    "capability:create_milestone": CHAT_INVISIBLE(issue=1440),
    "capability:create_release": CHAT_INVISIBLE(issue=1440),
    "capability:create_label": CHAT_INVISIBLE(issue=1440),
    "capability:create_branch": CHAT_INVISIBLE(issue=1440),
    "capability:create_pull_request": CHAT_INVISIBLE(issue=1440),
    "capability:update_status": CHAT_INVISIBLE(issue=1440),
    "capability:create_calendar_event": CHAT_INVISIBLE(
        issue=1440, note="calendar connector port rides the R2 epic"
    ),
    "capability:post_to_slack": CHAT_INVISIBLE(
        issue=1364, note="Slack #1232-contract port (rides #1440)"
    ),
    "capability:create_document": CHAT_INVISIBLE(untracked=True),
    "capability:batch_create_issues": CHAT_INVISIBLE(untracked=True),
    # ---- regression pins ----
    # A "pin:" row is NOT a derived product surface: it exists purely so the
    # #1433 ratchet re-verifies, on every build, that a once-misrouted natural
    # phrasing still resolves deterministically to its capability (the #1471
    # calendar precedent, generalized — that fix could ride existing surface
    # rows; reminders have no page/integration surface of their own, they live
    # on todo_items.reminder_date). The ratchet's stale check exempts the pin:
    # namespace; test_every_pointer_resolves_deterministically enforces pins
    # exactly like surface rows, and pins MUST be POINTERs (asserted there).
    # Being POINTERs, pins also join the "what can you do?" answer (#1428).
    #
    # #1521: signed-in "what reminders do I have?" fell past the pre-classifier
    # to the LLM, which misrouted it to the temporal lane — answered with
    # today's date and "(No meetings – great day for deep work!)" while the
    # stored reminder was never consulted (PM live, 2026-08-08).
    "pin:reminder-query": POINTER(
        "what reminders do I have?", expects=("query", "list_reminders_query")
    ),
}


# ---------------------------------------------------------------------------
# #1428 — the capability answer derivation
# ---------------------------------------------------------------------------

# Conversational capabilities that are true of the floor itself and have no
# product surface to point at. Deliberately tiny; everything surface-backed
# comes from POINTER rows. User register only (guarded by
# tests/unit/services/intent_service/test_capability_answer_1428.py).
CORE_CAPABILITIES = (
    "conversational PM guidance",
    "strategic thinking and prioritization frameworks",
)


def pointer_utterances(ledger=None):
    """Deduped canonical utterances from the ledger's POINTER rows, in ledger
    (insertion) order — deterministic, so the answer is stable across calls."""
    if ledger is None:
        ledger = CHAT_POINTERS
    seen = []
    for row in ledger.values():
        if isinstance(row, POINTER) and row.utterance not in seen:
            seen.append(row.utterance)
    return seen


def capability_answer_lines(ledger=None):
    """User-register capability lines for the 'what can you do?' answer.

    Derived from the ledger: one example-ask line per unique POINTER
    utterance, plus the CORE_CAPABILITIES conversational lines. CHAT_INVISIBLE
    surfaces contribute nothing — the answer never claims a capability chat
    cannot reach (honesty per capability state, #1428 AC).
    """
    lines = list(CORE_CAPABILITIES)
    lines.extend(f'you can ask me: "{utterance}"' for utterance in pointer_utterances(ledger))
    return lines
