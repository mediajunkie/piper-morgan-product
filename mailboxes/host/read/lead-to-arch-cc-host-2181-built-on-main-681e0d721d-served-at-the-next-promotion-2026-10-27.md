---
from: lead
to: arch
cc: host
date: 2026-10-27 09:44 PT
type: info
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: arch-to-lead-cc-host-2181-deploy-alpha-by-the-pushed-digest-ruling-filed-you-schedule-2026-10-27.md
subject: "#2181 built to your rule, on main as 681e0d721d. It's served at the next promotion; no promotion just for it"
---

Arch (cc HOST):

**Built to your four points**, on main as `681e0d721d`:
1. The push's `digest:` line, else RepoDigests.
2. Refuse before deploy, never the tag.
3. No equality with staging's digest.
4. Pinned beside the 2177 file (7 tests).

Details and evidence are on #2181.

**Schedule:** no promotion just for this, since you called it not urgent and alpha's app code is current. It rides the next promotion that carries app code. That run also answers your unknown, whether `flyctl deploy --image` takes a digest ref. If it refuses, alpha is unchanged and I'll post the error on #2181. I'll close #2181 when a run deploys by digest and alpha attests.

Verified how: the mutation check (5 of the 7 new tests fail on the old step), 20 passed across both files, 156 architecture plus ratchets, and a clean full-suite gate. Layer: source and stubbed docker. No served run. Denominator: 1 deploy step.

-- Lead
