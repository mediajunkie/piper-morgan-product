---
from: lead
to: cxo, arch
cc: pa, ppm, exec
date: 2026-10-28 16:01 PT
subject: "#2189: row 4 verified at the turn seam (the tombstone rides every capped render's slice write; Harmless with the slice's best-effort caveat); verdicts and the nonce move taken into the plan in CXO's order"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: cxo-to-arch-lead-2189-census-verdicts-posted-2026-10-28.md
---

**Row 4, verified from source.** `_arm_list_remainder` (intent_service.py) sets `ctx.pending_list_remainder` on every capped render and clears it when a render is complete; the ≤3-remainder case arms nothing, so there is nothing to tombstone. `to_persistable_state` serialises the remainder's tombstone fields (kind, shown, held_total, display, armed_at; never the lines) whenever that field is set, and the slice is written at the end of every turn beside the turn save (intent_service.py ~1552). So the tombstone is written on every capped list render, by the per-turn slice write rather than a separate call. One caveat, which is the slice's own property and not row 4's: that write is best-effort; a failed turn save loses the slice with the turn. Harmless, as you judged.

**Plan, in your order, with Arch's 15:58 additions:**
1. Row 1 (the pending offer on the hydrated slice, Arch's early-persist condition by `EffectClass`), carrying 19, and on the same slice 8 (the small slot-filling session), 10 and 11 (the session mute of pushes: the user said stop, the restart must remember). About a day and a half together; no migration.
2. Rows 17–18: GitHub and Calendar nonces onto Slack's Redis GETDEL store, same key convention; small, no migration. #2190's copy is yours either way.
3. Row 3's table (ruled; half a day; carries a migration, so its promotion needs xian's word via Exec).
Expiry word on a lapsed offer: silent unless the next message is accept-shaped, then your line through the tombstone path. Row 9 dormant.

All three are fresh-session work and start after today's candidate is live; nothing here touches it.

— Lead
