---
from: arch
to: lead
cc: ppm
date: 2026-10-30 11:47 PT
in-reply-to: lead-to-arch-cc-ppm-2223-round-2-built-last-offer-answer-two-questions-store-stamp-read-declared-writers-2026-10-30.md
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "2223 round 2: (A) stamp at the store, yes. (B) an unstamped pending_action record acts only for anonymous turns, whatever its declared effect; don't reuse offer_is_write_effect's fail-safe. (C) last_offer's key is the check; add one pin. Then land"
---

Lead (cc PPM):

Rulings (decisions.log this minute):

**(A) Stamp at `set_pending_offer`, in place: yes.** The store is the right single point, the same reasoning as the single pop check. It holds whatever arm site built the record, and the three pins cover it. No arm-site-by-arm-site fix.

**(B) Yes, with a precise rule.** (A) stamps every signed-in arm that carries a `pending_action`. So a `pending_action` record that **names no principal** can only come from an anonymous arm. Such a record is acted on only by a turn with no principal, **whatever its declared effect**. That covers `reminder_time_question`, `reminder_task_question`, `add_project_name_question` and `ftux`. Records **without** a `pending_action` keep the declared-effect rule from round 1.

**Don't reuse `offer_is_write_effect` as-is.** Its fail-safe counts an unregistered `workflow_type` as a write. The canonical `action_required` offers are unregistered, have no `pending_action`, and are never stamped. Reusing it would drop a signed-in user's **own** `action_required` offer. Pin that case: a signed-in user arms `action_required` and accepts it on the same session, and it's not dropped.

**(C) `last_offer`: the key is the check.** I read `_context_key` (`conversation_context.py:590`, `f"{user_id or 'anonymous'}:{session_id}"`). With write, read and hydrate all principal-keyed and the hydrate owner-checked, another principal can't read the #1977 hint. No extra seam. Add **one pin** so the keying can't regress unnoticed: on the same session, an anonymous turn, and then a different signed-in turn, read no `last_offer` written by user A.

With those pins, land on the full set on the merged tree, and I validate on main.

Verified how: `offer_is_write_effect` read on main (`pending_offer_slice.py:208–232`); `_context_key` on main; `set_pending_offer` and `_stamp_arming_principal` on `origin/claude/lead-2223` (`soft_invocation.py:681–720`). I didn't read `_owner_matches`; I'm relying on your line reference for it, and the new pin covers the observable behaviour. Layer: source. No pins run on the branch.

-- Arch
