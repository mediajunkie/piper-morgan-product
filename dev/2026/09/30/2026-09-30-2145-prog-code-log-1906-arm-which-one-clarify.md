# Session Log — Coding Agent (prog), 2026-09-30 21:45 PDT

**Role**: Coding Agent (prog)
**Model**: Sonnet (Claude Sonnet 5)
**Dispatched by**: Lead Developer
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
**Task**: #1906 — arm the "which one do you mean?" clarify (`services/intent_service/reminder_clear.py`'s `named_target_unmatched` branch, the one unarmed offer-site in that module)
**Constraints honored**: no git add/commit/index operations (per dispatch instructions); no live LLM calls in any test; no flag/env changes.

## What shipped

1. **Fix** — `maybe_handle_clear_family`'s `named_target_unmatched` branch (zero or several candidates for a named target, e.g. PM's "clear the overdue reminder" where no candidate literally says "overdue") now calls `set_pending_offer` when at least one candidate exists. New carrier: workflow type `reminder_clear_pick_target` (kind `CLEAR_PICK_TARGET_KIND`), registered in `workflow_entries.py` as `READ` effect (PRIVATE, offer-seam only, `action_triggered=False` — no rail/dispatch-site growth).
2. **Binding** (`_resolve_pick_target` + helpers) — the next turn's answer binds to exactly ONE candidate via, in priority order: an ordinal/positional reference (`_ordinal_index`: "the first one" / "second" / "#2" / "1" / "last" — bounds-checked, so an unrelated command's number like "close issue #108" never misreads as a position); an unambiguous status word (`_overdue_status`: "the overdue one", judged off each candidate's due-ish timestamp bound at OFFER time, ISO string, no fresh DB read — skips honestly to "none" when zero or multiple qualify, never guesses); a name/substring match (`_name_index`: literal substring first, then significant-word overlap, ties → "ambiguous").
3. **Continuation, not re-classification** — extracted the three-variant post-resolution decision tree (lines that used to live inline at the end of `maybe_handle_clear_family`) into a new shared function `_act_on_resolved_targets(intent_service, session_id, user_id, principal, todo_user_id, todo_service, verb, noun, ids, texts, candidate_effect, original_message, base_intent_data)`. Both the original named-target-matched path AND the new pick-target turn handler call it — one source of truth, not a parallel copy. A bound pick re-enters this with `[ids[idx]], [texts[idx]]` — exactly the flow a single matched name would have reached (variant 1's either/or, variant 2's auto-apply+disclosure, or variant 3's REAL #1190 destructive confirm).
4. **Turn handler** (`_handle_pick_target_turn`) — principal-mismatch check first; then `acceptance.evaluate_acceptance` at the carrier's declared READ×PRIVATE→LOW_CEREMONY axes: STATE_QUESTION and DECLINE both return `None` (fall through to the generic seam, which silently re-arms / answers the decline honestly — same idiom as `_handle_verb_answer_turn`); a bare ACCEPT ("yes", names nothing) also returns `None` so the generic seam's ACCEPT path dispatches the registered `run_reminder_clear_pick_target_workflow` (re-ask + re-arm — the `clarify_reminder_clear_verb` idiom, never a blind bind). Otherwise: attempt the bind. Bound → continue into `_act_on_resolved_targets`. Unresolved (no match or ambiguous) → check for an unrelated command via the SAME #1899 reads-only discriminator the reminder-task carrier uses (`PreClassifier.pre_classify` surface 1 first — free, deterministic; `inversion_live.read_op_claims_turn` second, only on a live-flagged READ verdict) → release (`None`) if claimed. Otherwise re-ask once (`pick_target_reasked=True` stamped on the re-armed payload); a SECOND consecutive unresolved turn releases (`None`) rather than looping forever.
5. Wired the new kind into `handle_reminder_clear_turn`'s dispatch and into `services/intent/intent_service.py`'s pending-offer kind-check tuple (the same `elif _vi_payload.get("kind") in (...)` the other two reminder-clear kinds already use — NOT a new `elif intent.action` dispatch-site, so `MAX_DISPATCH_SITES` is untouched).
6. `candidate_effect` (the classifier's WRITE/DESTRUCTIVE guess from the ORIGINAL arming turn) is threaded into the pick-target offer payload (`clear_candidate_effect`, stored as the `EffectClass` member's `.name`, e.g. `"WRITE"` — not `.value`, which is an `int` since `EffectClass` is an `IntEnum`; this was the first of two transient mypy `arg-type` regressions, fixed by switching `.value`→`.name` and the reconstruction from `EffectClass(...)`→`EffectClass[...]`) so the no-stored-default branch's effect-weighted gate (`decide_verb_interpretation`) has the SAME input a fresh turn would have had — no live classification needed on the answer turn.
7. Docs: one paragraph in `docs/internal/architecture/current/intent-routing-stack.md`'s armed-offers narrative (after the #1696 bulk-delete paragraph, before #1769) naming the new carrier, its binding rules, and the continuation. One `decisions.log` entry (2026-09-30 22:0x PDT).

## Tests

New file: `tests/unit/services/intent_service/test_reminder_clear_pick_target_1906.py` — 28 tests, all pass, 0 live LLM calls.

- `TestResolvePickTargetOrdinal` (8) — every ordinal form binds; an out-of-range number (unrelated command's issue #) does NOT bind.
- `TestResolvePickTargetName` (4) — literal substring, partial word-overlap, tied overlap → ambiguous, no overlap → none.
- `TestResolvePickTargetStatus` (3) — unambiguous overdue binds; multiple overdue → ambiguous; no due data → none (skipped honestly, never guessed).
- `TestRegistryEntry` (2) — `reminder_clear_pick_target` registered READ×PRIVATE→LOW_CEREMONY; not rail-reachable.
- `TestArmingRegression` (2) — **THE pin**: `_arm_pick_target` asserts the named-target-unmatched turn now arms (`kind == CLEAR_PICK_TARGET_KIND`, full candidate ids/texts/due stored); the zero-candidate case ("you don't have any right now") correctly stays unarmed.
- `TestBindingContinuesTheFlow` (4) — ordinal pick + stored COMPLETE default → variant 2 auto-applies to ONLY the bound item (not the whole set); name pick + stored DELETE default → variant 3's singular-grammar confirm, then a real `#1190` yes deletes exactly 1; overdue pick binds the single overdue candidate; no stored default → variant 1's exact `variant_one_question()` (byte-identical to what a matched name would have produced), and a follow-up "mark it done" actually executes (PM's "Yes" now has something to run — the regression's fix, proven end-to-end).
- `TestBareAcceptReasks` (1) — "yes" alone re-asks, re-arms, nothing mutates.
- `TestDeclineReleases` (1) — "no" declines honestly, offer cleared.
- `TestOffIntentReleases` (1) — unit-level call to `handle_reminder_clear_turn` directly (the #1654 idiom — avoids a live turn through `process_intent`'s downstream GitHub/LLM-backed floor routing, which is NOT what this carrier's behavior is about): "close issue #108" (pinned as a deterministic `PreClassifier.pre_classify` surface-1 claim) returns `None` and arms nothing.
- `TestSecondAmbiguousReleases` (1) — same unit-level idiom: first ambiguous answer re-asks + re-arms (`pick_target_reasked=True`); feeding the SAME ambiguous answer into the re-armed offer releases (`None`, nothing re-armed).
- `TestPrincipalMismatch` (1) — a different principal's turn cannot bind; nothing mutates.

Early iteration note: my first draft of `TestOffIntentReleases`/`TestSecondAmbiguousReleases` ran through the full `process_intent` e2e path and hit the REAL conversational floor's LLM call (because "close issue #108" is a genuine, fully-dispatchable command — pre-classified and routed for real, not just claimed-and-discarded) — caught by the explosive-LLM fixture, which is exactly what it's for. Rewrote both to call `handle_reminder_clear_turn` directly against a fake `intent_service` (`SimpleNamespace` + a real `WorkflowOfferService`), the same "turn-handler seam" idiom `test_task_clarify_1654.py::TestTaskTurnHandlerSeam` uses — deterministic, no live turn, proves exactly the carrier behavior under test.

## Gate results (run this session, in this worktree)

- `ruff format` + `ruff check --fix` over all touched files: clean, no findings after two format passes.
- `tests/unit/services/intent_service/test_reminder_clear_pick_target_1906.py`: **28 passed**.
- `tests/unit/services/intent_service/ tests/unit/services/intent/` (full): **5012 passed**, 0 failed (first run, before the mypy fix — behavior unaffected by the subsequent typing-only fix).
- `tests/test_architecture_enforcement.py`: **63 passed, 1 xfailed** (expected xfail, pre-existing).
- Combined re-run after the mypy fix (`tests/unit/services/intent_service/ tests/unit/services/intent/ tests/test_architecture_enforcement.py`): **5075 passed, 1 xfailed**, exit code 0.
- `scripts/run-sweep.sh ratchets` (completion ratchets + architecture enforcement + the #1436 mypy per-code gate, read in full before running): **73 passed, 1 xfailed**; mypy gate **all 24 ratcheted codes at ceiling** (arg-type=364, held — see below).

### Mypy gate: two transient regressions found and fixed in this session

First `ratchets` run reported `mypy_arg_type: 366 > ceiling 364` (2 new). Isolated both to `reminder_clear.py` via a direct `mypy --show-error-codes` run filtered to the touched files:
1. `_pick_target_offer`'s `candidate_effect` param is typed `Optional[str]`; I was passing `candidate_effect.value` — `EffectClass` is an `IntEnum`, so `.value` is `int`, not `str`. Fixed: pass `.name` (e.g. `"WRITE"`), and reconstruct via `EffectClass[name]` (lookup by member name) instead of `EffectClass(value)` (lookup by int value), with the `except KeyError` (not `ValueError`) to match.
2. `_act_on_resolved_targets`'s `principal` param was typed `str`, but `_handle_pick_target_turn` computes `principal = str(user_id) if user_id else payload.get("user_id")` — a `dict.get` return, `Any | None`. Retyped the param `Optional[str]` (matches what `get_verified_inference`/`get_meta_mode`/`store_verified_inference` already accept — no behavior change, just an honest signature).

Re-measured clean: arg-type held at 364 (ceiling), all 24 codes at ceiling, gate green.

**Verified how**: method = `scripts/run-sweep.sh ratchets` (completion ratchets + architecture enforcement + the pinned `venv-mypy-gate/bin/python` mypy per-code gate against `scripts/ratchet_ceilings.json`) plus direct `pytest` runs of the touched test directories, all executed this turn, output read in full and quoted above — not a check run earlier and assumed still valid. Layer = unit/integration tests against the REAL `IntentService.process_intent` dispatch chain and the REAL registered-workflow/acceptance-contract machinery (mocked only at the LLM boundary — explosive, raises on any attribute touch — the TodoManagementService boundary, and the users.preferences JSONB boundary), plus the REAL mypy type-checker over the full `services/`+`web/` tree; this is NOT a render test, NOT a curl-200, and NOT a config-presence check. Denominator = the full `tests/unit/services/intent_service/` + `tests/unit/services/intent/` directories (5075 of however many collected — all collected, 0 skipped, 0 deselected in that combined run) plus the full architecture-enforcement + completion-ratchet + mypy-gate suite (`scripts/run-sweep.sh ratchets`'s own scope, read in full before running) — not a hand-picked subset.

## Discovered work

None filed. (One pre-existing observation, not mine to act on: this shared worktree already carried substantial uncommitted changes to `scripts/build_inversion_corpus_phase0.py`, `tests/fixtures/inversion_corpus_phase0.yaml`, and `tests/unit/test_inversion_phase3_deletion_1595.py` — 589 lines, matching the #1595 Phase 3 corpus-deposit work referenced in this worktree's recent commit history — present before I touched anything and untouched by me throughout. Flagging for Lead's awareness only; per dispatch instructions I did not stage, commit, or otherwise touch the git index.)

## Files touched (all uncommitted — dispatch instructions: no git add/commit/index operations)

- `services/intent_service/reminder_clear.py` — the fix (+619/-38 lines: new constants, `_due_iso`, `_pick_target_offer`, the `_ordinal_index`/`_overdue_status`/`_name_index`/`_resolve_pick_target` binding predicate, `_handle_pick_target_turn`, `_act_on_resolved_targets` (extracted), `run_reminder_clear_pick_target_workflow`, arming call site in `maybe_handle_clear_family`, dispatch wiring in `handle_reminder_clear_turn`)
- `services/intent_service/workflow_entries.py` — import + `WorkflowEntry` registration for `reminder_clear_pick_target`
- `services/intent/intent_service.py` — added the new kind to the existing pending-offer kind-check tuple (comment updated to match)
- `tests/unit/services/intent_service/test_reminder_clear_pick_target_1906.py` — new, 28 tests
- `docs/internal/architecture/current/intent-routing-stack.md` — one paragraph, armed-offers narrative
- `docs/internal/architecture/decisions/decisions.log` — one entry, 2026-09-30 22:0x PDT

## Memory & briefing surfaces referenced this session

- **Referenced**: GH issue #1906 full body (PM's transcript + mechanism — the task spec); `services/intent_service/reminder_clear.py` read in full (module docstring, every existing arming branch, the `#1762`/`#1665`/`#1899` precedent comments inline); `services/intent_service/acceptance.py` full (`evaluate_acceptance`, `AcceptanceVerdict`, `acceptance_tier`); `services/intent_service/todo_handlers.py`'s `#1899` discriminator (`handle_reminder_task_turn`'s command-release block, lines ~1710-1747) — direct model for the pick-target carrier's off-intent release; `docs/internal/architecture/current/intent-routing-stack.md` — read the #1605/#1696/#1769 paragraphs to match voice/structure for the new entry; `tests/unit/services/intent_service/test_reminder_clear_verb_1605.py` and `test_reminder_clear_verb_anchor_1653.py` — full test idiom (explosive-LLM fixture, `todo_boundary`, `pref_store`, `_stub_classification`) and the turn-handler-seam unit-test idiom (`test_task_clarify_1654.py::TestTaskTurnHandlerSeam`, `_fake_service`/`_offer`).
- **Loaded but not referenced**: CLAUDE.md's full worktree/mailbox/sign-off discipline sections (not applicable — this is a prog dispatch with explicit no-git-index instructions, not a session with mailbox or merge-to-main responsibilities); MEMORY.md index.
- **Wanted but not found**: nothing — the issue body + the named files were sufficient; no gap.

## Sign-off

Per dispatch instructions: no commit, no stage, no git-index operation performed. Work remains on disk in this shared worktree for the Lead to review/commit. Reporting back via SubagentHandback.
