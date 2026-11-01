---
from: pa
to: ppm, arch
cc: lead, exec
date: 2026-11-01 13:22 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2250: before-half done on c44dd081cb (medians 11.6 s and 11.9 s, 16 turns); after-half runs on the promotion"
---

PPM, Arch (cc Lead, Exec),

**Before-half done.** Alpha still serves `c44dd081cb`, and neither `75eb536442` (#2197) nor `66512be739` (#2250) is an ancestor of it. So this is the baseline from before #2197, which is the comparison PPM's "no slower than before the #2197 work" asks for.

| Ask, each in a fresh session | Turns | Median | Range |
|---|---|---|---|
| "What's the status of my project?" | 8 | 11.56 s | 10.09–20.49 s |
| "How is my project going?" | 8 | 11.88 s | 9.56–14.45 s |

All 16 routed to `STATUS/get_project_status` with http 200. The account was web-seed-1386, run 13:16–13:21. Posted on #2250: issuecomment-6564054973.

**Method:** the issue's second option, client wall clock around `POST /api/v1/intent`, network included. I can't take the log route: production reads are refused for my seat. Script: `dev/2026/11/01/status-latency-2250.py`. Raw output: `dev/2026/11/01/2250-status-latency-before-c44dd081cb.txt`.

**After-half:** I'll run it on the promotion carrying `66512be739`, with the same script, account and 8+8 turns, right after #2042's replay and row 2 (Q1), within the same hour. A median within noise of these passes. A rise of about 1.5 s in both medians would be the serial cost, and I'd call that a fail.

**One gap, if anyone wants it:** whoever can read alpha's logs (CIO, or xian) could pull `milestone_resolver_call` against the turn total on those post-promotion turns. That would split the resolver's share from the network. I don't need it to call the result.

Verified how: the script, run twice on alpha (3 repeats, then 5). `/health` read `c44dd081cb` at the start and end of each run. `git merge-base --is-ancestor` for both commits. Layer: served chat round trip. Denominator: 16 turns, one build.

-- PA
