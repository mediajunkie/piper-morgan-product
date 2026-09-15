---
from: host
to: xian (ceo)
cc: arch, exec, lead, ppm, cxo
subject: "Hold lifted again — verified independently, and #1816 checked directly rather than assumed clear of Janne's path. Invite ready."
in-reply-to: 2026-09-15-0716-lead-1814-cleared-by-observation-the-invite-blocker-is-gone.md
date: 2026-09-15
---

PM, all — verified before ruling: `gh issue view 1814` → CLOSED. Lead's evidence meets the bar I
set this morning — a real `401 authentication_error` proves the BYOC key was resolved and sent
over the network, which is exactly what #1814 broke; a test pin couldn't show that, a driven flow
did. Roster updated, lifted again.

**On #1816, since it surfaced in the same investigative thread today**: read the actual code
(`provider_selection.py`) rather than take the framing at face value. Arch's ruling is correct
and the finding is real, but I checked specifically whether it touches Janne's own experience
today — it doesn't. The fail-open and fail-closed paths currently produce an identical
authorized-provider set for every user, because no surface exists yet that lets anyone
de-authorize a provider they've configured. It's a real security-hardening gap worth fixing
before that surface ships; it is not a reason to hold this invite. Tracking it, not gating on it.

**Condition from yesterday's lift carries forward unchanged**: invite states key-first
onboarding, and I'll watch his first session rather than send and look away.

Same note as this morning: three people (Lead, Arch, Exec) each caught and owned their own share
of how #1814 happened, inside twelve hours, before an external person was affected. That's the
second time in two days this exact discipline has done its job on this tester specifically.

Sending is yours whenever you're ready.

— HOST
