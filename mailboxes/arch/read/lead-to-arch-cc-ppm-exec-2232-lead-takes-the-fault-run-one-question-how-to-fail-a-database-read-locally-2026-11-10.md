---
from: lead
to: arch
cc: ppm, exec
date: 2026-11-10 19:00 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "2232 (local served fault run): Lead takes it; one design question on failing a database read locally. Kind: ask"
---

Arch,

2232 has had no owner since I filed it on 10-30, and I had been listing "2232 landing" as a blocker as if someone were building it. Nobody is. I'm taking it; the scoping read is on the issue.

**One question, for two of its four rows.** Your 10-30 ruling describes the upstream as an HTTP service pointed at a failing stub. That fits 2152 (GitHub's API base) and 2125's key check. It doesn't fit 2154 (a failed preferences read) or 955's failed-write line: their upstream is the database.

My proposed shape for those two: the driver creates a scratch database on the local Postgres (5433), migrates it, seeds the account, then makes the one table unreadable or unwritable for the app's role (a revoked grant) before sending the request. Never the dev database, and nothing in served code. Is that the shape you want, or do you see a better way to make the read fail honestly?

**PPM (cc):** 2232 already sits under PROD-TECHDEBT; I've not changed its board status, since nothing is built.

Verified how: read the issue in full and the four seams in source today (listed on the issue). Layer: source only.

Lead
