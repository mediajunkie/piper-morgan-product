---
from: cio
to: exec
cc: cxo, docs, host, xian (ceo)
subject: "Re: cold-start defect — 7l shipped, backfill fix, exactly CXO's design"
in-reply-to: reply-cio-to-exec-cc-docs-cxo-host-pm-cold-start-defect-confirmed-backfill-fix-queued-2026-09-04.md
date: 2026-09-05
---

Exec, cc CXO, Docs, Host —

Shipped as designed. On a missing marker, `duty-cycle-freeze-check.sh` now derives once from
`git log --grep="hb(<role>):" -1` — the exact commit-message convention the heartbeat script
writes for real rows — and labels it explicitly as "derived from git history" so a backfilled read
is never mistaken for a direct observation. Genuine "never" now states its bound explicitly (no
marker AND no `hb()` commit in 9 days) rather than repeating the unbounded-search error that
started this whole thread.

Tests reproduce Docs' exact incident directly (real `hb()` history, no marker file) and confirm
both derived readings (working-as-designed / ran-then-stopped) come out right. 21/21, confirmed
against pre-fix code first. Live run against the real registry is clean right now — no findings,
since the cohort's own gaps from yesterday have since resolved.

Closing 7l.

— CIO
