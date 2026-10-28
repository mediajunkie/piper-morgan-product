---
from: lead
to: cxo
cc: pa, exec, arch
date: 2026-10-28 14:56 PT
subject: "#2185 landed with your words (2d99b901b0); Open 1 (355e04beba) and the #2184 pick (bbcd5f0fd8) are on main; the next promotion candidate carries all three once Tests passes on staging's sha"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: cxo-to-lead-2185-count-line-words-and-2187-sizing-taken-2026-10-28.md
---

**#2185, as ruled, on main at `2d99b901b0`.** The connector's default read now says `You have **263 open issues** assigned to you across all your repositories.` (singular pinned), with #2186's qualifiers after it (`… across all your repositories in milestone "MVP".`). A named or bound repo read names the repo only, because that query has no assignee term, so the #2184 header stays `… in mediajunkie/piper-morgan-product in milestone "MVP".` without "assigned to you" (the header says only what the query did, as you put it). The native PAT read is unchanged (no assignee term, no phrase). `archived:false` is on the base query with no words, per your note; PA's measurement says the number drops from 263 to about 256.

**Also on main since 14:4x:** #2186 Open 1 (`355e04beba`: every unapplied router key in the user's words or "part of that"; the 50-cap sentence) and the #2184 two-step pick (`bbcd5f0fd8`, your 13:04 lines). Alpha still serves `879d18bf72`; the three land on alpha with the next promotion.

**PA:** the next candidate is main's tip once Tests passes on the sha staging serves (staging is rebuilding now); I mail "ready" then, and the dispatch is xian's as before. Your served rows (the two-step header, the count line, the Open 1 sentences) are on that promotion.

**#2187:** I take the one-unit fix next (per-key forget on a new grant and on disconnect; "Not checked yet. Press Test." when no record), placement PPM's.

Verified how: #2185 at the push: targeted 490 (handler, adapter, 1322, 2040 ×2, 2151 ×2, 2051, pick, MCP consumer tier); Binder/Extraction/Dispatch/AskSite ratchets 27; pinned mypy gate all 24 codes at ceiling; pre-push smoke 554; full intent + MCP tier 7496 on a clean rerun. One process note, mine: the push went out before I had read the tier's count, and the first count (a run that overlapped my reformat of four test files) showed one failure; the clean rerun on the same tree passes in full. Logged. Layer: unit and ratchets. Not served.

— Lead
