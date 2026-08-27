---
from: docs
to: exec
date: 2026-08-21
subject: "Ship #057 contributor workstream report — Docs — window Aug 14-20"
---

# Ship #057 Contributor Workstream Report — Documentation Management (Docs)

**Window**: Friday, August 14 – Thursday, August 20, 2026.

## Progress

**Two real recurring-cadence gaps found and closed same-week, both self-found**: a 3-day omnibus
gap (08-14/15/16, closed 08-17) and a 2-day omnibus gap (08-17/18, closed 08-19). Neither was
flagged by anyone else — both surfaced during routine carry-forward review and were closed the
same fire they were found, via sequential subagent dispatch to avoid a CSV-write race. By 08-21
the chain was continuous 07-27 through 08-20 with zero remaining gaps.

**Weekly Docs Audit #1643 (08-17)**: the first fully comprehensive run of the audit — 7 real
fixes committed (broken-link repairs, a genuinely-wrong ADR catalog entry corrected rather than
guessed at, missing NAVIGATION.md entries, a duplicate-content cluster flagged), 2 systemic
findings surfaced rather than swept under the rug (a stale bulk `last_verified` stamp cluster
87% unrefreshed 3 weeks after being flagged; BRIEFING-CURRENT-STATE 22 days stale under a
5-day-old banner). #1644 filed for the 56 residual broken links, correctly left to a future pass
rather than force-closed.

**A 9-day duty-cycle-heartbeat gap in my own practice was found by Exec and fixed same-fire
(08-18)** — I'd never actually been running Step 5b, which explained two prior false freeze-alarms
that week. Verified independently at every hop (Exec → HOST → me → CIO closing the loop) before
anyone acted on it. Adopted as a standing per-fire practice since; held clean the rest of the week.

**Weekly Ship #056 published (08-19) with 2 real defects caught and fixed** (a bare GitHub issue
number breaking an established Ship-prose convention; one "cohort") and **5 load-bearing factual
claims fact-checked against primary session logs**, all confirmed accurate. Same day, found and
fixed a live-404 blocking PM's LinkedIn cross-post — then, rather than stop at the one reported
instance, scanned the whole corpus for the same defect class and caught a second, older casualty:
**Ship #054 had been broken the identical way since 2026-08-05, 14 days uncaught.** Filed
`piper-morgan-website#33` for a systemic guard.

**"The Dead Code That Wasn't" published (08-20)**, 14/14 template checks clean, 4 technical claims
fact-checked verbatim against the primary Lead Dev logs the drafting notes cited. Same day, what
looked like a spreading "3rd instance" of the hero-image bug turned out to be a 100%-structural
pattern (81 of 81 published posts share the same frontmatter-name-never-matches-deployed-asset
shape, by design) with exactly one real misuse site — a wrong instruction in the `draft-weekly-ship`
skill telling drafters to copy that value verbatim into a public URL. **Fixed at that instruction**
(not just the two symptom posts), and reframed `website#33`'s scope so a future guard gets built
against the right shape rather than an 81-file frontmatter chase that would have broken the
field's actual job.

**Caught 3 confidently-wrong or stale claims this window before acting on them** — a same-day
report claiming CLAUDE.md's checkout path was broken (verified false via `git worktree list` +
live dry-run), an incoming report's "3rd instance" framing on the hero-image bug (verified false
for that specific post before accepting the framing), and — found this morning, outside this
window but worth naming since it's the same pattern — my own carried-forward "MIT license badge"
item, which Exec caught as stale 10 minutes after I wrote it (the repo shipped an Apache 2.0
LICENSE on 08-15 and I hadn't independently re-verified before carrying the note forward).

**docs-standing-items.md fully refreshed (08-19)** — had gone stale since 2026-05-27; 6 of its
cited GitHub issues were already closed, verified live before rewriting rather than assumed.
**docs-carry-forward.md fully pruned (08-21, this window's edge)** — 440 lines of ~6-week
accumulated history down to ~65, with the old content fully preserved in git log and session/
omnibus logs; deferred twice before finally doing it.

## Setbacks

**The MIT-badge miss above is the real one worth naming honestly**: I pruned the carry-forward
this morning specifically to make stale content easier to catch, then in the same pass carried
forward an item without applying the same live-verification discipline I'd just used on the
issue-tracked items. Caught within the hour by Exec, not by me. The fix going forward is
mechanical, not just "be more careful": any carried-forward item without a GitHub issue behind it
needs the same live-check as the ones that do, every time it's carried, not just when it's first
written.

**No sprint-completeness or milestone claim made in this report** — per Exec's instruction, only
running `sprint-truth.py` if this report made one, and it doesn't; Docs's portfolio doesn't carry
sprint-denominator claims.

## Blockers

None. Two items remain genuinely awaiting PM (docs-tree flattening plan go/no-go, filed 08-11;
no other genuine blockers) — not chasing, both are correct to hold per standing discipline.

— Docs
