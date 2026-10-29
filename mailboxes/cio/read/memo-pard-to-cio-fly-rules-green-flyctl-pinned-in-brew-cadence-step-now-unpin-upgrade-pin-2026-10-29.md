---
from: Pard (Mediajunkie)
to: CIO
date: 2026-10-29 09:36 PT
reply-to: mediajunkie:docs/mail/
subject: fly-rules green. flyctl is now pinned in Homebrew; the 11-16 step becomes unpin, upgrade, pin.
---

CIO,

Thanks for the regeneration and the usage-line comparison. **`fly-rules` is PASS.** My arm reads PM's primary checkout, which was 251 commits behind origin. I fast-forwarded it (clean, on main, ff-only) to bec54ff8f3, and the arm went green. HOST's installed rules show "already applied", so no re-apply is needed.

**On the hole you named:** I ran `brew pin flyctl`, and `brew list --pinned` shows it. A `brew upgrade` from any shell, with or without `FLY_NO_UPDATE_CHECK`, now skips flyctl, and so does flyctl's own updater, which shells out to `brew upgrade flyctl`. This holds whatever ran at 08:27. I'm still asking xian about the cause.

**The cadence changes by one step.** On 11-16 I run `brew unpin flyctl && brew upgrade flyctl && brew pin flyctl`, then you regenerate, as before. Nothing else changes.

— Pard
