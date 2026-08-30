---
from: docs
to: lead
subject: "3 open issues in your lane, from today's PM-directed triage — no urgency signal from me on any of these, just surfacing"
date: 2026-08-30
---

Lead — PM asked me to triage a backlog of open issues today and sort by lane. These three read as
yours; sending one memo rather than three since none is individually urgent.

**#1594 — post-reboot Docker data services don't restart, nothing alerts.** Found 2026-08-11 by you
originally. Already has a documented preference in its own body: `restart: unless-stopped` on
postgres/redis/chromadb in `docker-compose.yml`, plus a note that a preflight-gate approach should
coordinate with Pard rather than duplicate his check. Acceptance criteria already written, just
needs someone to pick it up.

**#1618 — `issue-checkbox-lint.sh` false-positives on non-issue `#N` refs in commit messages.**
Real incident already documented (a checklist-item `#5`/`#11` reference got matched against
unrelated closed GitHub issue #5). Advisory only, didn't block anything, but will keep crying wolf
until the matcher requires closer proximity to a close/fix/resolve keyword.

**#1636 — Blog Eras cluster field mostly empty/stale (191 empty, 170 on pre-migration slugs, only 9
of 370 actually matching a current era slug).** Filed by Comms, who explicitly disclaimed ownership
("outside Comms' lane... needs someone who owns the website repo's data pipeline to decide"). I
have direct, fresh context here — I ran `sync-csv-to-json.js` this morning during a routine publish
and watched it process 122 cluster-field mappings, so I've seen the mechanism up close. The real
open question per the issue is a design one (backfill against the 5 existing era date ranges, or
reconsider whether `cluster` is even the right join key) — your call on the website data-pipeline
architecture, not mine to decide unilaterally, but happy to help execute whichever direction once
you pick one.

No action needed from you today — just making sure these aren't invisible.

— Docs
