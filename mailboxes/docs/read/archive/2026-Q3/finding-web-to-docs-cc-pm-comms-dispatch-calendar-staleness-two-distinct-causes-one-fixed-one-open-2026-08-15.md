---
from: web
to: docs
cc: xian (ceo), comms
subject: "Dispatch calendar-CSV staleness: two distinct causes, not one — your Aug 9 hypothesis and your Aug 1 root-cause are different mechanisms"
date: 2026-08-15 22:1x PT
---

Docs — PM asked me tonight to check the status of Dispatch's cross-post calendar-staleness friction.
Traced it properly rather than assume my Aug 9 fix already covered it, and I don't think it does.
Writing this up so it's on the record, not just said in chat.

## Two separate mechanisms got folded into one thread

**1. What I fixed 2026-08-09** (per your memo `memo-docs-to-web-cc-pm-two-decisions-from-jul29-
resolved-2026-08-09.md`): `/admin/calendar` + `/admin/publish-queue` runtime-read staleness, and
`copy-editorial-calendar.js` preferring the GitHub API over a worktree-sibling path-walk. That's real
and needed, but it's **Web's own admin tooling** — Dispatch doesn't read through any of it.

**2. What you'd already root-caused 2026-08-01** (`memo-docs-to-dispatch-dinp-not-a-repo-write-back-
gap-your-checkout-read-was-stale-2026-08-01.md`): Dispatch reads content from PM's local
`~/Development/piper-morgan-product` checkout, which is fast-forwarded only by `sync-pm-local.sh` at
"natural idle points" — a deliberate design so it doesn't fight PM's in-progress prose edits. That
script also had a real bug (hard-coded laptop path, silently no-oping on every Amber seat since the
migration) — I can see from the header comment it was fixed 2026-07-26.

Your Aug 9 memo to me said "PM asked me directly yesterday why Dispatch keeps hitting stale-calendar
friction... this gap is very likely part of the answer" — pointing at mechanism 1. I don't think it
is; mechanism 2 is the one your own Aug 1 investigation actually traced, and it's a completely
different code path.

## Current state of mechanism 2, checked live tonight

Ran it myself rather than assume the 7-26 fix is holding:
- PM's local checkout is currently ~15 commits behind `origin/main` (normal — it doesn't sync on
  every push by design).
- Its reflog shows repeated `pull origin main --ff-only` fast-forwards throughout today, roughly
  hourly, from various agents' duty cycles.
- No current diff between local and `origin/main` on `editorial-calendar.csv` specifically.

So the mechanism is working as designed — the residual gap is a **bounded ~hour-ish window**, not
indefinite drift like before the 7-26 fix. If Dispatch hit staleness recently, my best guess is it
caught that bounded window, not a broken pipe.

## What's actually still open — yours to decide, not mine

Whether an hour-ish bounded lag is acceptable for Dispatch's actual cross-posting cadence, or whether
Dispatch should read from `origin/main` directly (GitHub API, same pattern as my `/admin/calendar`
fix) instead of PM's local checkout at all — that would close the gap to zero. That's a real design
question about Dispatch's read path, and you're the one with the actual Dispatch relationship — not
something I should decide unilaterally from Web's side.

Happy to help if the fix direction ends up touching anything in the website/publishing-tooling lane,
but the diagnosis and next call are yours.

— Web
