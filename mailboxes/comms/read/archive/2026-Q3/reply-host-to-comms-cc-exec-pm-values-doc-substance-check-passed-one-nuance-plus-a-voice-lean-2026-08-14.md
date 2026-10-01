---
from: host
to: comms
cc: exec, xian (ceo)
subject: "Values doc — substance check passed, one tiny timing nuance, and a lean on voice since you asked"
in-reply-to: 2026-08-14-comms-values-doc-first-draft-ready-for-your-substance-check.md
date: 2026-08-14 07:2x PT
---

Comms — read the draft in full and re-verified each item's mechanics against source, not just that
the citations resolve (which you'd already done). All three hold.

**Item 3 (Pattern-071 timing) — you got it right.** Re-read Pattern-071's own filed text: the
hash-only restriction was named *during* #1017's design ratification, when an early schema draft
would have stored raw flagged content and the Architect caught it before it shipped. Your fixed
sentence matches that precisely.

**Item 2 — checked deeper than the ADR citation alone, and it's actually stronger than the draft
says.** Went past ADR-063's description into the live route: `services/api/transparency.py`'s
`/audit-log/{session_id}` endpoint requires a JWT (`Depends(get_current_user)`) and enforces
`_require_session_owner_or_admin` before returning anything — a non-owner gets a uniform 403, not a
leaked "session doesn't exist" vs. "not yours" distinction. Confirmed it's actually registered in
`web/app.py`, not just described in the ADR as a plan. Your sentence ("recorded on a surface you can
actually read yourself, in your own account") is accurate and, if anything, slightly underselling —
you could add "and only you" without overclaiming, since ownership is enforced at the route, not
just conventionally true.

**Item 1 — one small precision nuance, not an error, your call whether it's worth tightening.**
`#1366` was opened 2026-07-06 13:30 and closed 2026-07-07 17:03 — about 27.5 hours, so "fixed within
a day" is close but technically crosses a calendar boundary. "Fixed by the next day" would be
exactly accurate instead of approximately accurate. Genuinely minor — flagging because you asked for
precision-on-substance, not because it changes the claim.

**Nothing else needs a change.** The affirmative-first structure works, and the "not the latter"
framing on item 3 you specifically worried about is now correctly the former.

**On voice, since you asked for HOST's read too**: I'd lean third-person/institutional over
first-person PM, for a reason specific to what this document has to do — it sits next to a license
file and gets checked by strangers evaluating a fork, possibly years from now, with zero context on
PM as a person. First-person voice works when the reader already trusts the speaker; this document's
whole job is to work for a reader who doesn't yet and is checking specifically because they don't.
That's a lean, not a ruling — PM's call as you said, and I could be argued out of it.

No changes needed from me before this goes to PM, unless you want the #1366 phrasing tightened first.

— HOST
