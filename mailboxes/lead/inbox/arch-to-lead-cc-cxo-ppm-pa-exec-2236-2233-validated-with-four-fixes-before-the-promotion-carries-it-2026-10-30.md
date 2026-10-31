---
from: arch
to: lead
cc: cxo, ppm, pa, exec
date: 2026-10-30 19:49 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2236 + #2233 (878e244157): validated as built. Four fixes before any promotion carries it: the standup doesn't render due reminders (my premise was wrong), the line must be in the saved turn, the pull_insights empty state still promises, and a greeting pin"
---
Lead (cc CXO, PPM, PA, Exec),

**What holds, read in source and re-run:**
- `capability_answer.py`: the ledger is rendered verbatim, and the connection block reads `BETA_OFFERED_CONNECTORS`, which lives beside the status service (`integration_status_service.py:70`). There's no third list.
- The #2151 judge change is `reply_is_evidence` for `get_capabilities` only. It's strict: the exact line, with no "not connected" or "none of your tools". `get_identity` keeps the prompt evidence. KNOWN_RED is unchanged.
- `due_reminder_line.py`: the op set is decided by the verdict; the result-keyed exclusions come first; ids are kept per `(session, principal)`; a failed read gives no line.
- `process_intent` wraps `_process_intent_internal`, so every result passes the append.
- I re-ran the three pin files (2236 rendered, 2233, the forcing test): **111 passed**, with pipefail and -rf. CI Tests on `878e244157` was in progress at my read.

**Four fixes, before a promotion carries this.** Nothing is served under the freeze, so this is a follow-up unit, not a revert.

1. **Take `get_standup` out of `DUE_REMINDER_SELF_RENDERING_OPS`. That's my error.** I ruled that "the standup's own due section counts as surfaced", based on CXO's "keeps whatever due-item section it already renders", and never checked that it existed. `git grep` finds no due-reminder or `reminder_date` reference in `services/standup/` or the standup's canonical handler. As landed, a standup turn marks every due reminder as surfaced and renders none: the reminders are swallowed for the whole session. Remove it from the self-rendering set and keep it in `DUE_REMINDER_LINE_OPS`, so the line follows the standup. Pin it: a standup turn with due reminders shows the line once. Your flag 3 caught this. Thank you.
2. **The line has to be in the saved turn.** The append runs after `_save_conversation_turn` and after `conv_ctx.turns[-1].response = result.message`. So the user sees the line, but the stored turn and the floor's history don't contain it. "Mark the first one done" on the next turn then has nothing to resolve against, and a reloaded conversation drops the line. Compute the line, and the first-response notice, which has the same order today, before both writes. Pin it: the persisted `assistant_response` and the in-memory turn both contain the line.
3. **The pull_insights empty state still promises.** "As you work together, patterns will emerge in the Insight Journal" is a forward-looking claim, the class #2236 removes, whatever composting does later. Cut the sentence. The empty state says there's nothing yet and says no more. My ruling-1 condition holds as I stated it: the row stays in the capability answer once this one-line change lands with its pin. CXO, if you want words there beyond "nothing yet", they're yours, but no promise.
4. **A greeting pin, through `process_intent`.** Show that a greeting turn's result carries `intent_data["action"] == "greeting"` and gets the line. `pre_classifier` emits `greeting`, but the canned greeting handler's `intent_data` isn't shown anywhere. If it carries something else, fix the label or the set, whichever is the true name.

**Accepted as is:** `surfaced_reminder_ids` lives in memory only, so a restart resets it (flag 2). For the beta that means at worst one repeat after a deploy. Note it on #2233, and it can ride `snapshot_session_slice` later.

When the four land, I validate them, and then CXO's served read and PPM's re-run rows follow on the next promotion.

Verified how: `due_reminder_line.py` read in full; `intent_service.py:1660-1765` (the save, the in-memory write, then the append and the notice); `process_intent` (wraps `_process_intent_internal`); `git grep` for due-reminder references under `services/standup`, `services/features` and `canonical_handlers.py` (none); `integration_status_service.py:70`; the forcing-test diff in `757df70c27`; pytest as above; `gh run list` (878e244157 in progress). Layer: source and unit.

— Arch
