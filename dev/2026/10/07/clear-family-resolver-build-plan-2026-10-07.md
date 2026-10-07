# Clear family under router args — build plan (Lead, 2026-10-07)

**Rulings this implements**: Arch 10-06 (`clear_todos` is a RESOLVER rail entry: mutates nothing, resolves the verb, re-enters the
rail as `complete_todo` or `delete_todo` with the same args; may resolve only to live-eligible ops; no `flip_group`, own token;
flips after both concrete ops are live) · CXO 10-06 (five strings, below) · ADR-080 D1–D6 · procedure rules 5 and 7.
**Landing gate**: rule 7 — adding the `clear_todos` rail entry is a catalog change → full-corpus run in the same lane. That run is
live spend, **parked on PM's API-cost ruling (Exec's Decision F)**. Code can be built and unit-tested on a side branch first.

## What exists today (read 10-07)
- `reminder_clear.py` (#1605): handler-internal REGEX detection (`detect_clear_family_ask`: verb + noun + no explicit verb), the
  three ratified variants, the stored verb default via `verified_inference` (`inference_key(verb)`, store-on-verify), the
  correction window, and regex target binders (22 surfaces under `reminder-clear-binding`, ceiling 17 literals).
- `complete_todo` consumes router targets (`handle_complete_todo_targets`, #1943): resolves names/ordinals (ordinals only against
  the numbered list last shown), 1 item → completes, 2+ or any exclusion → enumerating #1190 confirm, unresolved → CXO string 4.
- **`delete_todo` does NOT consume router targets.** `handle_delete_todo` resolves its own target (#1666 rail-confirmed single delete).
- Rail re-entry precedent: `run_confirm_pending_action_workflow` → `dispatch_workflow(workflow_type=action, context={"intent": …})`.

## Pieces, in build order (each one reviewed unit)
1. **`delete_todo` consumes router targets** (`handle_delete_todo_targets`, mirror of 1943): same resolver
   (`resolve_router_targets`, numbered-list scope), same unresolved reply (CXO string 4 with "delete"), and **always** the
   enumerating #1190 confirm (DESTRUCTIVE → CONFIRM in every consent cell, even for one item). Confirm copy for a plain delete:
   needs a CXO string (draft: `Delete 3 reminders: "A" (2 items) and "B"? Leaving "D" as is. (yes/no)`). Live-eligible only
   once PM's `delete_todo` token is on (it is allowlisted; flag state is PM's).
2. **`clear_todos` resolver entry** (`run_clear_todos_workflow`, `effect=READ`, no `flip_group`): reads `inversion_args`; resolves
   the SET first via the shared resolver (so every reply can enumerate it); then the verb:
   - **stored = done**, 1 target and no carve-out → re-enter as `complete_todo` (auto-apply) and append CXO variant-2 disclosure
     ("That's what 'clear' has meant for you. Say so if you meant delete this time." — the existing `CORRECTION_WINDOW_ASK`).
   - **stored = done**, 2+ or any carve-out → re-enter as `complete_todo`; its own gate arms the enumerating confirm (CXO 2: no
     extra clause); on "yes", the summary plus the disclosure line (needs the re-entered intent to carry a `via_clear_verb` marker).
   - **stored = delete** → re-enter as `delete_todo` (piece 1) with CXO variant-3 copy: `You've set 'clear' to mean delete —
     delete 3 reminders: "…" (2 items) and "…"? Leaving "…" as is. (yes/no)`.
   - **no stored default** → CXO variant-1-with-set: `You want to clear 3 reminders: "…" (2 items) and "…". Leaving "…" as is.
     Before I touch them — when you say 'clear' on a reminder, do you want me to mark it done, or delete it? I'll remember for next time.`
     Arm the existing verb-question carrier with the RESOLVED ids bound; the answer turn stores the verb (unchanged #1605 mechanics)
     and re-enters as the concrete op with those ids; if the answer carries its own list ("delete them, but not the PR one"), refine
     the set and RE-RENDER it before acting (CXO 4).
   - **any target unresolved** → complete_todo string 4 with NO verb clause (CXO 5); ask the verb only once the set resolves.
   - **live-eligibility guard**: if the concrete op is not live (flag), fall through to the legacy #1605 path — never a back door.
3. **Description + corpus**: `clear_todos` description (the router decides family membership: "clear/handle/take care of/reset
   applied to reminders or todos, where done-vs-delete is ambiguous"); corpus rows with `expected_args` (PM's 08-15 transcript,
   "please clear the reminders except for 'Review the PR'", which today scores `PLAN[delete_todo→get_capabilities]`) → **full-corpus
   run (rule 7) — parked on Decision F**; ×6 controls on moved rows.
4. **Served-answer probe** (rule 8): PM's own transcript, in-process app + Postgres, local flag with `clear_todos` +
   `complete_todo` + `delete_todo`.
5. **Retire** `detect_clear_family_ask`, `_EXPLICIT_VERB_RE`, and the target binders under `reminder-clear-binding`, lowering the
   ratchet in the same commit — only after 3 and 4 pass and PM's token is on.

## Open questions before piece 1
- CXO: the plain-delete enumerated confirm string (piece 1) — not yet ruled.
- Arch: piece 1 makes `delete_todo` a second `inversion_args` consumer; same strict-parser constant as complete_todo (his condition).
