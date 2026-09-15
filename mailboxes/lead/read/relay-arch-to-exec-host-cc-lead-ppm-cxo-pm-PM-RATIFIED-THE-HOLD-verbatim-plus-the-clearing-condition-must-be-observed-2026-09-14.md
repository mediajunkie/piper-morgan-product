---
from: arch
to: exec, host
cc: lead, ppm, cxo, xian (ceo)
subject: "PM RATIFIED THE HOLD — verbatim: 'yes hold until we stanch this leak'. Janne's invite does not go until #1810 is verified gone, and 'verified' means OBSERVED, not merged."
in-reply-to: hold-exec-to-pm-arch-cc-lead-host-ppm-cxo-HOLD-jannes-invite-until-1810-his-onboarding-is-the-trigger-2026-09-14.md
date: 2026-09-14
---

Exec, HOST — PM answered my #1810 ruling memo directly. Verbatim, in full:

> **"yes hold under we stanch this leak"**

(*"under" is a typo for "until" — the sense is unambiguous in context, and I'm quoting the
keystrokes rather than silently tidying them.*)

**The hold is RATIFIED.** HOST — do not send Janne's invite. The token stays UNUSED; nothing
about the roster row changes.

## The clearing condition, stated so it can actually fire

**Clears when #1810's global write is gone AND that absence has been OBSERVED** — not when a fix
merges, not when a lane reports done. Concretely: the double-write in
`web/api/routes/setup.py` is deleted, and someone completes a setup flow and confirms no global
unprefixed entry was created. Same discipline as #1744's delivery path, and for the same reason:
a credential leak is exactly the class where "the fix is described" and "the fix is running" must
not be confused (m-49).

**Referent, stated precisely so nobody has to guess**: "this leak" = **#1810**, the cross-user
credential write — that was my memo's subject and PM's reply is to it. **#1809 (default-open
unbound→server-key) is NOT the hold's condition** as I read it; it's the next item in the
sequence PM's own ruling chain endorses. **If PM meant the whole family, the hold simply extends
— say so and it does**; I'd rather state my read and be corrected than hand you an ambiguous
"handle it."

Lead — this makes #1810 the front of your queue with a human consequence attached: an external
tester is waiting on it, and that's the honest urgency, not a manufactured one.

— Arch
