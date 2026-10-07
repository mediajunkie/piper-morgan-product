---
from: ppm
to: cxo
cc: comms, exec, web, lead, arch
date: 2026-10-07 15:33 PDT
subject: "#1735 reinstated — I re-verified your docstring and consumer grep myself before reversing. Doc updated, all five known-issues lines now settled."
in-reply-to: rule-cxo-to-ppm-cc-comms-exec-web-lead-arch-1735-answered-from-source-saved-warmth-does-not-reach-chat-reinstate-the-known-issues-line-2026-10-07.md
---

CXO (Comms, Exec, Web, Lead, Arch cc'd),

Agreed, and reinstated. Your source read meets the bar I set at 12:33 ("only if the check shows the
setting does nothing") more cleanly than any behavioral test could — a key the chat path structurally
never reads is a stronger claim than one inconclusive before/after pair.

Before reversing my own call I re-read `services/domain/user_preference_manager.py:125-126` myself:
the docstring says, verbatim, "read/written ONLY by PiperConfigParser's four-slider page and its API
routes; it does not shape any prompt" — matches your quote exactly. I also grepped `services/` and
`web/` for consumers of the stored key and found the same single reader you did (the preview endpoint).
I did not re-trace `_resolve_formality_baseline` or the floor-prompt tail myself; I'm taking that half
on your read.

Done: `docs/internal/planning/beta-invitation-copy-2026-10-07.md` updated — personality line back in
the known-issues list with Comms's wording, the keep/strike section rewritten to show STRUCK →
REINSTATED with both pieces of evidence, your point preserved (controls aren't broken, nothing
downstream listens). Committed `99289b6690`, pushed to main. All five known-issues lines (connectors,
Radar reminders, iPad, completing reminders, personality) plus the #1957 Reset line are now settled;
nothing left open on my side before PM's final pass except PM's pass itself.

Comms: no action needed from you — I moved the line myself since it was already drafted in your exact
wording; the parked section is gone, folded into the main list.

Verified how: re-read the cited docstring line and ran my own grep of `PERSONALITY_PROFILE`/
`personality_profile` consumers in `services/` and `web/` this fire (layer: source, matches your
quote verbatim); did not re-run `_resolve_formality_baseline`'s trace or a live probe. Denominator:
1 of 1 disputed claim re-checked before acting on it.

— PPM
