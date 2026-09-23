# Design record — the conversational-lens surface (deleted 2026-09-23, #1863)

**Why this record exists**: delete-module-safely's extract-before-delete rule (PM-033d precedent) —
git history holds code; it doesn't surface ideas. Retrieve the pre-cut source from the commit
immediately before this rip lands on `claude/lead-cycle` (check `git log --oneline -- services/
intent_service/conversation_context.py` around 2026-09-23), or from `origin/main` prior to that
merge.

**Ruling**: Arch GO, 2026-09-23 (`mailboxes/lead/read/rule-arch-to-lead-cc-pm-1863-1499-both-GO-
verified-2026-09-23.md`), on the Lead's reader census (`mailboxes/lead/…` / GitHub issue #1863
comments). Split out of #1774 per Arch's 2026-09-22 ruling: **rip it, don't complete it** —
completing would mean re-ruling the #763 lens vocabulary that was already deleted with
`lens_inference.py`, and no product case exists for it. Filed as its own Rule-0 item (not a rider
on #1774) because it is schema-touching on both ends.

## What the lens surface was meant to do

**Issue #763 (GLUE-FOLLOWUP)**, part of the grammar-conscious / ADR-049 "Conversational State and
Hierarchical Intent Architecture" effort: track *what aspect of the user's world the conversation
is currently focused on* — calendar, issues, projects, people, or general — so that:

1. **Follow-ups could inherit context implicitly.** "What about Thursday?" after a calendar-lens
   turn should resolve against calendar semantics without the user having to restate "meeting."
   This was the `classify_conscious` pipeline's job (push/pop/reset a `lens_stack`, derive
   `current_lens` from the most recent turn that set one). `classify_conscious` and its follow-up
   detectors (`FollowUpType`, `FOLLOW_UP_PATTERNS`, `detect_follow_up`, `resolve_follow_up`,
   `extract_temporal_reference`, `extract_topic`) were deleted as zero-caller dead code in #1768
   (2026-09-12) — `classify()` was, and had been, the live classification path. That deletion took
   the lens-stack push/pop/reset **trio** with it but left the **fields** (`ConversationTurn.lens`,
   `ConversationContext.lens_stack`, `.current_lens`) in place, because two still-live call sites
   read them:

2. **Issue #820**: the soft-invocation seam (`services/intent/intent_service.py`) read
   `conv_context.current_lens` and threaded it into `SoftInvocationDetector.detect()` as
   `active_lens`, and stored it on the `pending_offer` dict for later replay when a soft offer was
   accepted.

3. **Issue #822**: `SoftInvocationDetector.detect()` used `active_lens` to **boost confidence**
   when the active lens matched the soft-offer's workflow type (`_LENS_WORKFLOW_AFFINITY` — e.g.
   calendar lens + "meeting" pattern → +0.15 confidence, capped at 0.95). The idea: if the user is
   already visibly thinking about calendar topics, a meeting offer is more likely welcome.

4. **Issue #953**: `lens_stack` was folded into the Layer-4 persisted context slice
   (`ConversationContext.to_persistable_state()` / `apply_persisted_state()`, stored under the
   `layer4_state` key inside `ConversationDB.context` JSONB) so it would survive a session
   restart/refresh alongside `last_offer` and the floor-continuation flags.

5. **Issue #821** (a *separate, independent* mechanism — **not** part of this cut): slot-filling's
   own `active_lens: Optional[str]` parameter on `SlotFillingSession`, used to select lens-aware
   prompt phrasing (`slot_prompts.py`, `slot_template.py`'s `lens_prompts`/`lens_group_priority`).
   This was fed, at exactly one call site (`workflow_entries.py::start_meeting_workflow`), by the
   same `ctx.get("active_lens")` value that traced back to `current_lens` — so it was *also*
   always None in production, by the same transitive chain. It fails closed identically (`if lens
   and self.lens_prompts` short-circuits on None). **This #821 mechanism itself — the
   `SlotFillingSession.active_lens` field, `slot_prompts.py`, `slot_template.py`'s lens-prompt
   dicts, `slot_extractor.py`'s lens-aware group ordering — was left in place.** It is a general,
   independently-testable capability that nothing currently feeds, not a writer-less field; ripping
   it was outside this issue's GO and is flagged below as a discovered follow-on.

## Why it never got a writer

The only code that ever *wrote* `ConversationTurn.lens` (and therefore ever made `current_lens` or
`lens_stack` non-empty) was `classify_conscious`'s lens-inference step. `classify_conscious` had
**zero production callers** from the day the live `classify()` path shipped, and was deleted
outright in #1768. From that point on:

- `ConversationTurn.lens` was set by exactly one call site, `ConversationContext.add_turn(...,
  lens=...)` — and grep across every `add_turn(` call site in `services/` + `web/` found zero
  callers passing `lens=`.
- `current_lens` therefore always returned `None`.
- The #822 affinity boost's guard, `if active_lens and workflow_type in
  _LENS_WORKFLOW_AFFINITY.get(active_lens, [])`, fails closed on `None` — so the boost branch could
  never fire. Confidence was always the 0.7 baseline in production.
- `lens_stack` was declared, cleared on prune, and (de)serialized through the #953 slice, but
  nothing ever pushed onto it (the push/pop/reset trio died with `classify_conscious` in #1768) —
  so it was always `[]`, persisted and rehydrated as an empty list forever.

Small-fry riding the same shape: `ConversationTurn.temporal_reference` / `.topic` /
`.entity_references` and `ConversationContext.last_temporal_reference` — populated by the same
deleted `extract_temporal_reference`/`extract_topic` annotators, stored-never-populated since
#1768, zero readers outside `conversation_context.py` itself (confirmed by the same census sweep).
`ConversationContext.last_topic` (reads `turn.topic`) was not separately named in the census but
is a direct, necessary consequence of removing the `topic` field.

Also removed: the `ConversationalLens` enum in `services/shared_types.py`. It was never actually
wired as a type — `ConversationTurn.lens` was always typed `Optional[str]`, not
`Optional[ConversationalLens]` — so it had zero production readers of its own; its only uses were
decorative docstring references (this module, `slot_template.py`) and test literals. Once those
test literals were removed with the rest of this cut, it became fully orphaned, so it rode along.

## What was removed (2026-09-23, #1863)

- `services/intent_service/conversation_context.py`: `ConversationTurn.lens`,
  `ConversationTurn.temporal_reference`, `ConversationTurn.entity_references`,
  `ConversationTurn.topic`; `ConversationContext.lens_stack`,
  `ConversationContext.current_lens` (property), `ConversationContext.last_temporal_reference`
  (property), `ConversationContext.last_topic` (property); the lens-stack clear in
  `_prune_old_turns`; `add_turn`'s `lens=`/`temporal_reference=`/`entity_references=`/`topic=`
  kwargs; `lens_stack`'s read/write in `to_persistable_state()`/`apply_persisted_state()`.
- `services/intent/intent_service.py`: the `current_lens` read (#820 seam), its threading into
  `soft_invocation_detector.detect(active_lens=...)`, its storage on `pending_offer["active_lens"]`,
  its replay into `dispatch_context["active_lens"]` at offer-acceptance.
- `services/intent_service/soft_invocation.py`: `detect()`'s `active_lens` parameter,
  `_LENS_WORKFLOW_AFFINITY`, `_LENS_AFFINITY_BOOST`, the boost branch (#822), the `lens_boosted`
  debug-log field.
- `services/intent_service/workflow_entries.py`: `start_meeting_workflow`'s
  `ctx.get("active_lens")` read and its thread-through to `slot_filling_adapter.manager.
  start_filling(active_lens=...)` and the returned `intent_data.context["active_lens"]`. (The
  `start_filling(active_lens=...)` *parameter* itself, and everything downstream of it in
  `services/slot_filling/`, is #821's and was NOT touched — see above.)
- `services/shared_types.py`: the `ConversationalLens` enum.
- No `ConversationDB` schema change, no alembic migration: `lens_stack` was a key inside the
  `ConversationDB.context` JSONB column (namespaced under `layer4_state`), not a column. The
  repository layer (`services/database/repositories.py`) is opaque to what keys the persisted dict
  contains and required no changes.

## Legacy-row handling (no migration)

Existing DB rows may still carry a `layer4_state` blob with a `lens_stack` key (and, in principle,
a hand-edited or very old `current_lens` key, though nothing ever wrote one).
`ConversationContext.apply_persisted_state()` already ignores unknown/absent keys by construction
(each field is guarded by an explicit `if "<key>" in state` / `isinstance(...)` check before
assignment) — removing the `lens_stack` read means an old row's `lens_stack` key is now simply
never looked at, same as any other unrecognized key. Pinned behaviorally (Arch's condition) in
`tests/unit/services/intent_service/test_layer4_hydration_ignores_legacy_lens_keys_1863.py`:
hydrating a `layer4_state` dict containing legacy `lens_stack`/`current_lens` keys succeeds without
raising, and every other key in the same blob still hydrates correctly.

## What a future implementation would need to re-add

If "lens" (implicit topic-of-conversation inheritance) becomes a real product feature again, a
future implementation needs, at minimum:

1. **A writer.** The core reason this rip was safe is that nothing ever set `ConversationTurn.lens`
   after #1768. Any re-add starts with: what actually infers the lens from a turn, and where does
   it hook into the live `classify()` path (not a dead `classify_conscious`-style side pipeline)?
   LLM-based intent classification is the obvious candidate signal source now, where #763-era
   design assumed a rule-based `classify_conscious` annotator.
2. **A decision on whether lens state belongs on `ConversationTurn` at all**, versus a separate,
   explicitly-scoped piece of session state — the #763 design coupled it to turns (`current_lens`
   scans turns in reverse for the most recent non-None `.lens`), which meant every reader had to
   re-derive "current" by scanning, rather than reading a single source of truth.
3. **Re-litigating the #822 affinity boost's product case** on its own merits — Arch's 2026-09-22
   ruling on #1774 was explicit that completing/reviving the #763 lens vocabulary is a re-ruling,
   not a resume; the boost table (`calendar → meeting/standup`, etc.) encoded a hypothesis that was
   never actually tested in production (always-None input).
4. **Re-wiring to #821's slot-filling lens-aware prompts** if desired — that machinery
   (`SlotFillingSession.active_lens`, `slot_prompts.py`, `slot_template.py`'s
   `lens_prompts`/`lens_group_priority`) is intact and independently testable
   (`tests/unit/services/slot_filling/test_lens_aware_prompts.py`); it just currently has no feed.
5. **The enum**, if a typed vocabulary is wanted again: `ConversationalLens(str, Enum)` — CALENDAR,
   ISSUES, PROJECTS, PEOPLE, GENERAL — is recoverable from history (see the retrieval note above)
   and was a reasonable shape; it was removed here because it was decorative, not because the
   vocabulary was wrong.

## Discovered work (report only, not actioned here)

- `services/slot_filling/`'s #821 lens-aware-prompt machinery is now **permanently unfed** — the
  one call site that ever populated `SlotFillingSession.active_lens` with a real value (transitively,
  via the #820/#763 chain) is gone. It was already always-None in production before this cut
  (same transitive chain), so behavior is unchanged; flagging because it is now a second,
  structurally-similar writer-less-field candidate for a future Rule-0 pass, distinct from this
  issue's scope and not GO'd here.
