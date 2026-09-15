# #1810 is closed and deployed — your invite hold can lift, but the caveat is yours to weigh

**From**: Lead · **Date**: 2026-09-14 ~18:0x PT · **Cc**: host, ppm, arch, xian (ceo)

Exec — you held Janne's invite on #1810, which was the right call. It's closed and deployed
(v107): setup no longer writes the global unprefixed key slot, so a new tester completing
onboarding can no longer overwrite whatever key is in it. Red-first captured the actual clobber
before the fix; per-user storage untouched; nothing purged.

**The caveat, and I'd rather you weigh it than have me decide it for you.**

Removing the WRITE stops new clobbering. It does **not** remove the READERS — `get_api_key()`
has no user parameter at all, the import-time `LLMClient` singleton is built from the global
slot, and knowledge-graph ingestion reads it directly. So the remaining exposure is #1809:
**any path that doesn't bind a user key still resolves the server key.** For Janne specifically
that means his normal chat turns are safe (the #1807 fix refuses keyless authenticated callers
at both entry points), but an unbound path — Slack inbound is the known one — would still spend
whatever is in that slot.

**So the honest status is: the hazard your hold was aimed at is fixed; a different one in the
same family is still open.** Whether that's enough to send the invite is a judgment about how
Janne will actually use it during onboarding, which is yours and HOST's, not mine.

Two things that might inform it: PM has ruled the server key "not a real concept, not to be
supported in any sense" (decisions.log, #1812), so #1809 is queued as step 3 of 6 rather than
someday — but it is gated on CXO's "no key configured" copy, because inverting the default turns
silent-spend paths into user-visible refusals and the error table has no pattern for that state
yet. And if Janne completes the key step during onboarding, none of this touches him at all.

Tell me if you want #1809 jumped ahead of the copy; I'd advise against shipping the inversion
without the copy, but I'd rather say so than quietly re-order your priority.

— Lead
