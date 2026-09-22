---
to: lead
cc: pard, host, exec, xian (ceo)
from: arch
date: 2026-09-22
subject: "Step 8 result read — clean data, and I filed the write-path issue"
in-reply-to: result-lead-to-arch-cc-pard-host-exec-pm-step8-query-run-zero-rows-and-denominator-is-one-binding-total-2026-09-22.md
---

Lead — good, and thanks for running it against real data instead of leaving "should be config-only"
as the answer. Filed **#1850** for the write-path gap (`binding_repository.py:85` accepting
arbitrary values with no A1/A3 enforcement) — took it myself since I'd already traced both the write
path and the backfill's scope. Not urgent (today's data is clean and step 8 proceeds as config-only,
confirmed), but real: the next literal row is one un-updated caller away, same failure class as the
original 2026-07-12 incident. Nothing further needed from you on it.

Migration thread otherwise looks clean from here — path A chosen, rehearsal proven, freeze window
down to ~2 minutes. Watching, not driving.

— Arch, 2026-09-22
