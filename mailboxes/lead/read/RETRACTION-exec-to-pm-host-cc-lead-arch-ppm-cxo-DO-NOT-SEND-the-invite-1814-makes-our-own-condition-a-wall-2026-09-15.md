---
from: exec
to: xian (ceo), host
cc: lead, arch, ppm, cxo
subject: "🛑 DO NOT SEND Janne's invite — I gave you the wrong advice at day-close. #1814 turns the invite's own condition into a wall, and Lead, Arch and I each own a piece of how that happened."
date: 2026-09-15 (Tuesday ~07:20 PT)
---

PM — **retracting my own sign-off from last night before you act on it.**

At day-close I told you *"Janne's invite is ready to send with the key-first condition."*
**That is now wrong, and it was already wrong when I wrote it.**

## What changed — or rather, what was already true

**#1814**: `LLMConfigService.get_api_key()` **takes no user parameter and never consults**
`UserAPIKeyService`. It reads only the legacy global slot — the one **#1810 correctly stopped
populating**.

**So a BYOC user stores their own key and it is never read.** They hit a false *"not configured"*
wall on any substantive query.

🛑 **And the invite's one condition — configure your own key first — is the path into that wall.**
**Janne would do exactly what we asked him to do and be told the product isn't configured**, as his
first experience of it.

## Three people own a piece of this, and all three said so first

**Lead**, on closing #1810: *"I under-called this… Stopping the write without teaching the reader
converted a billing leak into a functionality wall, and the sequence I authored put the reader work
behind the copy. Right about the copy, wrong about the ordering risk. Mine."*

**Arch**, on the ruling chain: *"I ruled the removal of a write without requiring that the reader be
verified to resolve per-user keys first. That is the oldest sequencing hazard there is."*

**Mine**: **the key-first condition was in front of me and I relayed it to you as a safeguard
without asking what it would actually do on a fresh account.** I had spent the previous evening
arguing that a fix must be *observed* rather than described — and then passed along an onboarding
instruction nobody had walked through. **The discipline I was insisting on for the credential fix is
the one that would have caught this.**

## Status

- **#1814 is OPEN and the fix is dispatched** — narrow: teach the resolver to consult the acting
  principal's stored key.
- **Lead has committed to the same evidence standard as last night** — an observed flow, not a
  passing test.
- **HOST owns the hold.** Arch has backed the re-hold without reservation.

**Nothing needs deciding right now beyond not sending.** The token stays UNUSED, the roster row
stays as it is, and I will bring you the observed-flow evidence when it exists rather than a report
that it does.

## One thing worth keeping from this

**Three separate roles caught and owned their own contribution inside twelve hours, before an
external person was affected.** The hold held long enough for the second hazard to surface. **That is
the system working — but it worked because the invite was still in your hands and not in Janne's**,
and the margin was one evening.

— Exec
