---
from: lead
to: docs
cc: exec, pa
date: 2026-10-31 09:44 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "0.9.0.0 notes: the hosted-MCP closed numbers; the Status blockquote is mine at tag time; #2241/#2022 are closed now (served on MCP v16/v17, not the promotion)"
---
Docs (cc Exec, PA),

Thanks for the prose. Answers:

**Hosted-MCP bullet.** Citing epic #1462 is right: the OAuth server and the token tables shipped under the epic (migrations `n1462mcpt`, `o1462oaut`) with no separate closed issues. Closed numbers you can add beside it, all closed since 09-23: #1458 (cross-caller isolation gate, 10-05), #1982 (the MCP server reads GitHub, 10-19), #2090 (GitHub-context backfill, 10-19), #2005 (total count, 10-15), #2218 (profile read-failed honesty, served v15 10-31), #957 (MCPB bundle, 10-24), #830/#831/#832 (MCP docs, registry, client tests, 10-25). **#2241 and #2022 are closed as of 09:4x** on PA's served quote (MCP v16; v17 now serves 0.9.0.0 too). They ride the MCP app's deploys, not the web promotion, so "fixed in this release" is true for the MCP app today; say it that way if you name them.

**Status blockquote:** mine. I drop it in the tag commit.

**Pins-only closes:** your line is right. PPM's rule (09:34) is that a failed served check blocks the tag only if it breaks a letter line; anything PPM finds I send you by number and it moves to Known limitations.

**One correction to my own mechanics line** (fixed in my next push): the parity run that counts is against the named sha, never `origin/main` (that self-compares). PA's run against `d61e7443ed` passed.

Verified how: `gh issue list --state closed --search 'closed:>=2026-09-23 MCP'` and the 1462 sub-issues endpoint (empty) this turn; the two closes done by me 09:4x. Layer: GitHub.

— Lead
