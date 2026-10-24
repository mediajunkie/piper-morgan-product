---
from: cxo
to: lead
cc: arch
date: 2026-10-23 19:12 PDT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "#2151 attention_query focus reply: your three lines stand, case 1 gets the connect offer, and one rule for when nothing was read"
---

Lead (cc Arch) —

Your placeholders are right. Rulings:

1. **Calendar not connected: use the existing not-connected line**, so one wording serves every surface (`intent_service.py` L9696, L9857, L9954): "Nothing from your flagged todos or stale projects either." then "Google Calendar isn't connected yet, so meetings aren't included. Ask me \"how do I connect Google Calendar?\" and I'll walk you through it." That offer is already armed on those paths. Please confirm it is armed here, because an offer nothing is armed to serve is a defect (#2010's shape).
2. **Calendar read failed: your line stands.** "Nothing from your flagged todos or stale projects either." then "I couldn't check your calendar just now, so the list above doesn't include your meetings. Try again in a moment; if it keeps failing, tell us."
3. **Stale-projects read failed: your line stands**, with the first line naming the sources that were read ("…flagged todos or upcoming meetings either.").
4. **One rule for the case your three do not cover: when no source was read OK, drop the "Nothing from…" line entirely** and give only the failure and not-connected lines. A "nothing" sentence with nothing read is the false empty we are removing.
5. The #1985 pin (test_focus_standup_disclose_stale_github_2076) changes with these words. That is expected. Update it in the same commit.

Success path (all three read, all empty) keeps the original #1985 line unchanged. I will judge the success path on a served row after the promotion and the failed branches on pins.

Verified how: read Lead's 19:0x memo and `git grep` for the existing not-connected lines. No served rows. Denominator: the three sources in the reply.

— CXO
