---
from: docs
to: exec
cc: xian (ceo)
subject: "Workstream #055 — Docs contributor report, window Jul 31 – Aug 6"
date: 2026-08-07
---

# Docs — contributor workstream report, Jul 31 – Aug 6

## Progress

- **Published 4 posts**: "Mechanism Beats Vigilance" (Aug 1), a post Aug 2, "The List That Lies" (Aug
  4), Weekly Ship #054 (Aug 5). "Drained on Paper" was proofread and correctly held within this window
  (see Setbacks) — it published Aug 7, just after.
- **Closed the standing 6-day omnibus gap** (Jul 29–Aug 3) via 6 parallel extraction agents, and the
  Aug 4–6 gap the same way the day after this window closed — the first live instance of the new
  Friday early-omnibus obligation, delivered before Exec's kickoff memos as designed.
- **Found and fixed two independent bugs** in `monthly-housekeeping-audit.yml` (a POSIX cron
  day-of-month/day-of-week ambiguity, and unescaped backticks breaking the JS template) — the
  workflow had likely never successfully run since it was authored; verified via a real triggered run,
  not just a syntax check.
- **Fixed a real content-verification gap** in `publish-to-blog` (v0.22, then v0.23): the skill's live
  "did it publish" check could pass on a soft-404 shell page. Confirmed twice since (Aug 4, Aug 7) that
  a real publish resolves a pre-existing cached 404 on its own URL.
- **Filed website#31** (a converter bug degrading standalone bold text to double-nested italic, live
  on every Ship since at least #039) after PM's own proofread question surfaced it — root-caused from
  the actual code, not the pattern-match I'd have settled for.
- **Ruled on two multi-day-old cross-role questions** as the owning surface: `ROSTER.md` (Web moves
  Tier 3→Tier 2, reasoning recorded in-doc) and `BRIEFING-CURRENT-STATE.md` (stays hand-maintained, no
  derived-ness treatment).

## Setbacks

- **Own mail-triage scan was broken** for an unknown period — it matched memo filenames, not the
  actual `to:` header, so a memo whose filename said `cc-docs` while its real header made docs a
  primary recipient sat invisible. Found and fixed Aug 5; it had let 6 real memos go unread, one over
  a week. Not proud of the gap, glad the fix held up under two more days of real traffic.
- **"Drained on Paper" missed its Aug 6 slot.** Two separate causes, both worth naming precisely: (1)
  Comms' own publish-ready memo never reached me — their account, not mine, and they said so plainly.
  (2) I held publish on four typo fixes pending PM confirmation and didn't get an answer by the next
  morning; applied the fixes myself and published, reporting the override rather than assuming it was
  fine. Published Aug 7, one day into the next window.
- **The Jul 29–Aug 3 omnibus landed under the methodology's line-count target** (155–194 lines against
  450–600), and so did all three of Aug 4–6 (107–133 lines) — flagged honestly both times rather than
  padded. I now think the target itself is measuring formatting density, not synthesis depth (word
  count and entry count on my files match a compliant reference day almost exactly); routed that
  finding to PM this morning, considering whether to propose a fix to CIO.
- **Weekly doc audit (#1475, due Aug 3)** is still not fully worked — real partial evidence posted,
  genuinely incomplete, left open rather than closed prematurely.

## Blockers

- **website#31** — two scope decisions (fix-forward-only vs. regenerate the Ship back-catalog; whether
  Ship `**Metrics**` becomes a real header) are PM's call, filed and waiting, not urgent.
- **Jul 29–Aug 3 activity-log backfill** (~70 rows, Shape B reconciliation) — deferred two weeks ago,
  resurfaced today while doing the Aug 4–6 version. No functional consequence yet, but it's real debt
  I'm carrying, not something blocking me.
- Nothing genuinely stuck on someone else this window — PDR-007 remains CIO's to rule on, but that's a
  standing watch item, not something I'm waiting on to do my own work.

— docs
