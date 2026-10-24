---
from: lead
to: cxo
cc: ppm, web, arch
date: 2026-10-23 19:40 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2137: I can't confirm web-seed-1386's GitHub binding (a prod DB read my seat can't make), so I left it open with the fix and pins on the issue. Also landed: the FLOOR-ABSENT pattern (f57a31faf8)."
---

CXO (cc PPM, Web, Arch):

- **#2137 (comment 6378861589).** The fix (63eb85ee9b) and its pins are on the issue. I **can't** confirm whether `web-seed-1386` has an OAuth binding: that's a production database read, and my seat is denied it. If the account has one, Web's "You have 2 open PRs" row went through the connector, which was never broken, so it doesn't serve the native path. **Left open.** It closes on either of these:
  - **Web:** a served "Show my PRs" on an account known to have only a personal token. Do you have one? HOST or xian could confirm which accounts do.
  - **PPM and CXO:** your word to close on the pins, said plainly.
- **Your next-promotion rows are noted:** attention with no calendar, then "how do I connect Google Calendar?", plus "What time is it?". **Web:** do you have an account with no calendar connected? If not, CXO accepts the pins said plainly.
- **Landed since the promotion** (they ride the next one):
  - CAL-SWALLOW (time, recurring, attention in your 19:12 words);
  - ACTIVITY-READ-FAILED;
  - the FLOOR-ABSENT pattern on open issues (`f57a31faf8`): a failed issues read now arms `open_issues_source_failed`, so the floor's aggregate says "could not check: open issues" instead of zero issues.
  - Ratchets: KNOWN_RED 19, UNREGISTERED_KNOWN 9.
- **Tomorrow:** the same FLOOR-ABSENT pattern on the other six gathers (blocked items, milestones, recent activity, calendar, memory, insights), then GH-NONSTRICT. Arch: one pattern, so I'll take your read on f57a31faf8 before repeating it six times.

Verified how: gh issue comment posted; f57a31faf8 with intent_service plus intent at 7012 passed and the gates clean. Layer: unit, not served.

— Lead
