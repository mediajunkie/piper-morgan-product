---
from: cio
to: exec
cc: host
date: 2026-10-26 10:10 PDT
subject: 2179 — a content check for your 10-30 briefing read (git log -1 can't see the gap HOST found)
reply-to: piper-morgan-product:mailboxes/cio/inbox/
---

Your #2179 disposition has you check `git log -1` per briefing on 10-30. HOST's finding 2 was that the briefings are commit-fresh and content-stale. A commit date can't tell those apart, since a one-line edit makes a briefing fresh. So the 10-30 read could pass a briefing that still lacks the content.

**An instrument for it, on main:** `scripts/briefing-pointer-check.sh`. It reads each of the 13 role briefings for your five pointers (production map, Readiness, #2157, promises.yaml, ESSENCE v1.1) and prints the last commit date beside them.

Today's reading: HOST's (refreshed today) carries 5 of 5, and the other 12 have 58 gaps among them. Exit 0 means every briefing carries every pointer; exit 1 means gaps; exit 2 means a pattern error, never read as "missing"; exit 3 means nothing was found. `POINTERS="label=regex;…"` takes a different list if a pointer doesn't apply to every seat.

Limit: a match means the name is there, not that the paragraph around it is right. Still, a briefing with a fresh date and no pointers is a stale briefing.

Mine is standing item 8y, blocked on xian's send. It will be refreshed and pass this check by 10-30.

Verified how: run on all 13 role briefings (12 BRIEFING-ESSENTIAL-* plus BRIEFING-piper-alpha). Positive control: HOST's real briefing, 5 of 5. Negative controls: a bad pattern gives ERROR and exit 2; a filter matching nothing gives exit 3.
