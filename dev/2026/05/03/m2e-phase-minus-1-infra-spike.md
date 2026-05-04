# M2e Phase -1 Infrastructure Spike — 2026-05-03

**Author**: Lead Developer (Claude Code Opus)
**Purpose**: Pre-gameplan infrastructure verification across the 4 M2e implementation issues (#790, #864, #900, #869). Per gameplan-template v9.3 Phase -1 — done once across the cohort.

---

## Summary of findings

| Issue | Surface | Existence | Risk | Notable |
|---|---|---|---|---|
| **#790** Trust-gated calendar | calendar_connected flag, TrustComputationService, UserPreferenceManager | ✅ All present | Low | Mostly state-tracking + decision logic atop existing infra |
| **#864** Pre-classifier patterns for milestones/labels/releases/branches | PreClassifier + GITHUB_QUERY_PATTERNS exist; **GitHub MCP adapter LACKS the 4 entity-type methods** | ⚠️ MCP gap | Medium | Issue body explicitly anticipates this: "GitHub API support should be verified — some may require new MCP adapter methods" |
| **#900** Standup 3-part collection | State machine + conversation_manager exist; #889 dep CLOSED | ✅ Deps met | Medium | **PM-triage caveat in body**: "may be polish sprint, may not be MVP" — surface during audit walkthrough |
| **#869** Project Detail config IA | project_detail.html + projects.html exist; #861 CLOSED | ✅ Partial | Medium | Front-end-heavy + cross-page IA work; URL-structure + nav decisions needed |

---

## Per-issue infrastructure inventory

### #790 — Trust-gated calendar integration behavior

**GREEN — proceed cleanly**:

- `services/mcp/consumer/google_calendar_adapter.py:81` — `calendar_connected: bool = True` field on adapter (added by #789); used at `services/intent_service/canonical_handlers.py:279` and propagated through `temporal_summary.calendar_connected`
- `services/trust/trust_computation_service.py:49` — `TrustComputationService.get_trust_stage(user_id) → TrustStage` (used heavily across M2d insight work)
- `services/domain/user_preference_manager.py` — `UserPreferenceManager` exists; `calendar_setup_offered: bool` flag is a straightforward extension of existing preference patterns
- Issue #789 (alpha fix: silent when calendar not connected) is closed — current behavior is "silent default"; #790 layers on top to add the trust-gated offer

**Implementation shape (gameplan preview)**:
- Detect "calendar not connected" via existing `temporal_summary.calendar_connected == False`
- Read trust stage + user preference flag
- Branch decision: New user → offer help; Returning user (declined) → silent; Returning user (interested) → guidance
- Store user response in preference flag

**No scope-shape gaps**. Risk: low.

---

### #864 — Pre-classifier patterns for milestones/labels/releases/branches

**⚠️ MCP adapter gap**:

- `services/intent_service/pre_classifier.py:380` — `GITHUB_QUERY_PATTERNS` exists (issue + PR coverage)
- `services/intent_service/pre_classifier.py:1512` — `_get_github_action()` exists (issue + PR action mapping)
- `services/mcp/consumer/github_adapter.py` exists with methods for: `create_issue`, `update_issue`, `add_comment`, `list_github_issues_direct`, `get_closed_issues`, `get_github_issue_direct`
- **MISSING from adapter**: methods to fetch milestones, labels, releases, branches

The issue body anticipates this gap explicitly: *"GitHub API support should be verified before building handlers — some may require new MCP adapter methods"*. So the gameplan must scope **per-entity-type adapter additions** + handlers + patterns + tests.

**Implementation shape (gameplan preview)**:
- 4 new adapter methods: `list_milestones`, `list_labels`, `list_releases`, `list_branches`
- 4 corresponding handlers in `canonical_handlers.py` or `intent_service.py`
- Per-entity pre-classifier patterns + action detection
- Tests for each
- Issue body suggests priority order: **Milestones > Releases > Labels > Branches**. Could be staged: ship Milestones first, then Releases, etc.

**Scope shape consideration**: this is meaningfully larger than "add patterns." Worth flagging as Q1 in audit walkthrough — does PM want this as one issue or split into 4 sub-issues per entity type (per the split-related-issues feedback memory)?

---

### #900 — Standup 3-part structural collection

**✅ Deps met; PM-triage caveat noted**:

- `services/shared_types.py:215+` — `StandupConversationState` enum: `GATHERING_PREFERENCES / GENERATING / REFINING / FINALIZING` (current freeform state machine)
- `services/standup/conversation_manager.py:47` — `StandupConversationManager` consumes the states
- **#889** (escape/timeout/suspend bug fixes) — CLOSED (verified via `gh issue view`); the dependency is met
- **#888** (escape commands, suspend protocol) — referenced as "already complete" in #900 body

**🚩 PM-triage caveat in issue body** (worth surfacing during audit walkthrough):

> "PM to triage: may be polish sprint, may not be MVP. Per PM: 'We also don't want to overbuild features before knowing if a user wants it!'"

This is a Q1-shape question: should #900 be in M2e MVP, or deferred to M2-tail / Fast Follow / polish? Per gameplan-template Phase -1 PM verification, this is a "should we do this at all" question that deserves explicit disposition before drafting full Phase 1+ implementation.

**Implementation shape (gameplan preview, if PM keeps in MVP)**:
- 3-part state machine extension: GATHERING_YESTERDAY → GATHERING_TODAY → GATHERING_BLOCKERS → GENERATING
- Per-part prompting in conversation_manager
- "Done" recognition expanded with NL patterns ("that's all", "nothing else")
- Partial standup persistence on escape/timeout/suspend
- Tests across all flows

---

### #869 — Project configuration IA

**✅ Partial frontend infrastructure**:

- `templates/project_detail.html` exists (10K+ template; has tab plumbing per `tabindex` markers at lines 323, 394)
- `templates/projects.html` exists (list view)
- **#861** (Settings → Projects) — CLOSED; per #869 body: "current Settings → Projects implementation is fine as a stepping stone. When Project Detail gets its config tab, Settings → Projects should evolve to link there rather than duplicate the interface"
- URL structure proposed: `/projects/{id}?tab=settings` and `/settings/projects`

**Implementation shape (gameplan preview)**:
- Add Config tab to project_detail.html (existing tab plumbing should support it)
- Migrate config UI logic FROM Settings → Projects TO Project Detail Config tab
- Update Settings → Projects to LINK to Project Detail rather than duplicate UI
- URL routing for `?tab=settings` query param
- Front-end-heavy work; mostly template + JS

**Risk note**: #869 was relocated from M2d on May 2 with rationale "substance is IA, not MUX-lifecycle." That relocation was correct — this issue is purely about navigation/IA structure, no MUX semantics involved.

---

## Cross-cutting observations

### 1. WIRE-* triage backlog

`docs/internal/planning/m2-structure.md:161` flags: *"Several WIRE-* issues from the original M2 list (#690-695) may be partially superseded by floor migration. Needs triage."*

This triage hasn't happened. Not blocking the 4 named M2e issues, but the M2e gate ("Integration smoke tests pass for configured integrations") may depend on knowing whether these WIRE-* issues are in or out. Worth surfacing to PM during audit walkthrough as a separate question.

### 2. M2e is more heterogeneous than M2d

M2d was tightly themed around MUX surfaces (lifecycle indicator + insight-surfacing + composting). M2e is **integrations + IA + UX polish** — more diverse work shapes:
- #790 = backend logic + state tracking (small)
- #864 = MCP adapter extension + pattern coverage (medium-large)
- #900 = conversation flow + state machine (medium, gated by PM-triage)
- #869 = front-end IA + cross-page nav (medium, FE-heavy)

The audit walkthrough should expect more divergent question shapes per gameplan than M2d's tightly-related questions.

### 3. PM-triage flags

Two issues have explicit PM-disposition flags:
- **#900**: "may be polish, may not be MVP"
- **#864**: scope shape (one issue vs split per entity)

Both deserve explicit dispositions before Phase 0 of those gameplans starts.

---

## Questions for PM (before drafting gameplans)

1. **#900 PM-triage**: keep in M2e MVP, defer to polish/Fast-Follow, or further scope-trim? My lean: **keep in M2e MVP** since the dependency (#889) is closed and the partial-persistence + 3-part guidance is genuine UX value, but I want explicit confirmation given the body's "may not be MVP" caveat.

2. **#864 scope shape**: one issue covering all 4 entity types, OR split into 4 sub-issues per entity (Milestones / Releases / Labels / Branches) per the split-related-issues principle? My lean: **split into 2 issues** — Milestones+Releases together (similar shape, both list-with-detail), Labels+Branches separately (also similar pair). Halves the issue count without forcing artificial subdivision.

3. **WIRE-* triage**: separate concern; surface as a sibling task or fold into one of the 4 gameplans? My lean: **separate concern; not part of these 4 gameplans**. File a follow-up tracking issue for the WIRE-* triage; M2e gate language can specify "configured integrations" to dodge the ambiguity for now.

4. **#1037 still post-MVP confirmation**: per yesterday's audit, the topic-mapping issue stays post-MVP. Confirming it doesn't move into M2e scope. (This is a sanity-check, not a real question.)

If PM disposes Q1-Q3, I can draft 4 (or 5, if #864 splits) gameplans next.

---

## Files referenced in this spike

**#790**:
- `services/mcp/consumer/google_calendar_adapter.py:81`
- `services/intent_service/canonical_handlers.py:279`
- `services/trust/trust_computation_service.py:49`
- `services/domain/user_preference_manager.py`

**#864**:
- `services/intent_service/pre_classifier.py:380, 1512`
- `services/mcp/consumer/github_adapter.py` (methods inventory)

**#900**:
- `services/shared_types.py:215+` (StandupConversationState enum)
- `services/standup/conversation_manager.py:47`
- `gh issue view 889` → state: CLOSED

**#869**:
- `templates/project_detail.html`
- `templates/projects.html`
- `gh issue view 861` → state: CLOSED

**Cross-cutting**:
- `docs/internal/planning/m2-structure.md:149-165` (M2e composition + WIRE-* triage flag)

---

## Standing observations

- M2e isn't a single-theme sub-epic the way M2d was. Expect each gameplan to surface its own scoping questions rather than a tightly-grouped family.
- The Q1 pattern from M2d (each gameplan has audit-cascade ⚠️ items) will probably show up again, but with more variance in shape.
- One gameplan (#864) has a meaningful scope question that may bifurcate the issue. The split-related-issues feedback memory applies.
