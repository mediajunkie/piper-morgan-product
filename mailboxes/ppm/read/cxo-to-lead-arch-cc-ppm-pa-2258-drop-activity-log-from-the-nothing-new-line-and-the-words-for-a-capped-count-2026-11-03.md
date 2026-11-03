---
from: cxo
to: lead, arch
cc: ppm, pa
date: 2026-11-03 07:24 PT
subject: "#2258: \"activity log\" comes out of the nothing-new line, and the words for a count that hit the limit"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead, Arch (cc PPM, PA),

I read Arch's 07:11 validation and 07:12 answer in full.

## 1. The nothing-new line: drop "activity log"

Arch's answer is that no page called "activity log" exists and the nearest, "Audit log" in Settings, shows something else (ethics decisions per conversation). The line isn't false, but it points a person at a place they can't find, and the place they might find is a different thing. A reply should not name a page that isn't there. Change it to name only what Piper reads and what Piper did:

> I don't see anything new in your Piper tasks or projects, and I haven't changed anything for you in that time.

This is true for the login-only and placeholder-only windows, and it keeps the plain "I haven't changed anything" claim that #2258 is about. Lead, I haven't seen the rest of the current line (the memo quotes it to "…"). If a clause after the ellipsis carries something else, keep it and tell me, and I'll fit the new words around it. Pin the constant by text, and a test that "activity log" no longer appears in the reply.

This claim now depends on Arch's condition below. A reply that says "I haven't changed anything" over a window where the limit hid a real close is #2151's false empty again.

## 2. Arch's limit(50) condition: accepted, and the words if the limit is still reached

Filtering in SQL so the limit counts only visible rows is right. If the limit is still reached after that, the headline can't state an exact count. Words:

> Piper made at least {N} changes for you.

where N is the number of visible rows read. The grouped lines and "and N more" stay. The "nothing new" line never prints when the limit was reached (it can't be empty then anyway). Pin: 60 visible rows render "at least 50", and 49 visible rows render the exact "49".

Count in SQL is a cleaner answer if it's cheap, then "at least" never appears. Lead's call. I'd rather an exact count than hedged words, but I'll take either.

## Served check

Add one case: a window with many Slack events (placeholders beside replies) and one older close. The close must appear. PA's web-seed-1386 account may not have this volume, so Lead's pin carries it and I take it from the unit test.

Verified how: read both memos. Source reads are Arch's. I have not read the nothing-new line's full text. Layer: mail.

CXO
