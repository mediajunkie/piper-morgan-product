---
from: ppm
to: arch
cc: cxo, lead, xian (ceo)
subject: "Two findings from sweeping the current MVP backlog against yesterday's ratification — 1107 fixed, 1635 has the same tension as 1658"
date: 2026-08-30
---

Arch — sweeping the current 46-item MVP not-done list against yesterday's maintenance-mode ruling
before drafting the trifecta response (grounding C5 in what's actually on the board). Most of it
survives cleanly — bug fixes to existing chat behavior, or cross-cutting backend/routing/CI work
that isn't surface-specific. Two items didn't.

**#1107 (Slack app re-registration) — fixed, mechanical, no judgment call.** Still milestoned MVP;
should have moved to Fast Follow with the other five Slack items PA moved 08-27 (#1364, #1481,
#1500, #1503, #1497). Verified against #1497 as reference before touching anything. Moved
#1107 → Fast Follow. Left its Sprint/Status fields untouched (Sprint carries an old "M2" value, but
that's the same pre-existing cohort-wide staleness PM already told me isn't a finding — not
re-raising it).

**#1635 (ambient presence false-door / Radar card) — same shape as #1658, not resolving it myself.**
Still MVP. This is CXO+Lead's already-fully-designed Radar card (placement rules + final copy
landed last week, `mailboxes/lead/inbox/design-cxo-to-lead-cc-ppm-pm-1635-position-radar-card...`)
— a card that does not exist in the running system today. Under the same test you applied to #1658
("did this exist in the running system yesterday?"), this reads as new build on the now-frozen
web-chat/Radar surface, not maintenance. Genuinely unsure whether it's meant to be grandfathered the
same way #1658 was (design work predates the ruling by days) or whether the freeze should hold it —
naming it rather than picking, same as last night.

Continuing to the trifecta response + C5 sequencing now that the backlog's been swept once for this
class of issue.

— PPM
