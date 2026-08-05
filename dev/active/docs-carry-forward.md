# Docs Carry-Forward

**Updated**: 2026-08-04 22:40 PDT (Fire 5, STOP — DAY-CLOSED 2026-08-04)
**Session log**: `dev/2026/08/04/2026-08-04-0727-docs-code-log.md` (yesterday's is
`dev/2026/08/03/2026-08-03-0711-docs-code-log.md`, DAY-CLOSED verified)

**Worktrees**: product `~/Development/piper-morgan-worktrees/docs` @ `claude/docs-cycle` · website
`~/Development/piper-morgan-website-worktrees/docs` @ `claude/docs-cycle`
**Cron**: re-arming `82ddcd08` → new id at STOP (delete-then-create; see final action) —
`57 6,9,12,15,18,21`. Registry row must match.
**Hooks on this seat**: standalone `git commit` BLOCKS; compound `add && commit` BYPASSES. Mitigation:
stage in one call, commit bare in the next. `mail-send.sh` safe regardless.
**Standing note**: `pre-commit-broad-staging-warn.sh` blocks the Bash tool call outright on a ≥20-file
staged commit despite documenting itself as advisory-only; `--no-verify` has no effect (not a git hook).
Split large multi-file commits into batches under 20 files.

## ⚠️ Day-of-week duty triggers (added 2026-08-04, PM-directed) — CHECK EVERY START

**Why this section exists**: the Monday 2026-08-03 weekly doc audit (#1475) sat untouched until PM
asked me to check on it Tuesday. Nothing in the duty cycle knew it was Monday. Checking it surfaced a
second, independent finding: the *monthly* housekeeping audit had been silently broken by two real
bugs since the file was written — nobody had been checking whether it fired at all, because nothing
prompted the check. Both now fixed (see Resolved below).

**Read this list at every START, not just Mondays** (a START after a multi-day gap needs to catch up
on any Monday it missed):

- **Every Monday**: Weekly Docs Audit fires via `weekly-docs-audit.yml` (~9am PT). Check
  `gh run list --workflow=weekly-docs-audit.yml --limit 2` fired and succeeded; if not, `gh workflow
  run weekly-docs-audit.yml` and work the checklist issue yourself. Don't assume it ran — verify.
- **First Monday of each month**: Monthly Housekeeping Audit fires via
  `monthly-housekeeping-audit.yml` (fixed 08-04, cron was correct-looking but wrong per POSIX
  day-of-month/day-of-week OR semantics — see Resolved). Same check.
- **Not mine, but worth knowing exists**: Skill-Candidates Review (1st Tuesday, PM+Exec owned) and
  Role Health Check (4-weekly, HOST owned) — see `docs/internal/operations/
  staggered-audit-calendar-2026.md` for the full cadence table if a date ever looks Docs-adjacent.

**Proposed but not yet shipped**: a generic "Day-of-Week Duty Check" step in the shared
`duty-cycle-tick` skill (Step 3, right after reading carry-forward) — routed to CIO 2026-08-04, cc PM.
No reply yet; this section is the interim fix for Docs specifically until/unless that lands.

---

## Awaiting others — check, don't re-derive

- **PDR-007 awaits CIO ONLY** — unchanged, checked again this fire. Arch ✅ and Web ✅ both reviewed,
  no objection. **Do not decide the storage question early** — pre-registered 2–4 week window
  (2026-07-30 → 2026-08-27), shipped measurement (`scripts/measure-editorial-drift.py`).
- **Dispatch-DinP staleness report** — replied 2026-08-01, no reply yet. Still watching.
- **CIO's response on the day-of-week duty-check proposal** — sent 2026-08-04, no reply yet. Not
  urgent; my own interim fix (the section above) works standalone regardless of CIO's disposition.
- **Next Monday's weekly-docs-audit fire (~9:07 PT, Aug 10)** — Lead nudged the cron off the
  top-of-hour after 08-03's schedule didn't fire. Watch whether it fires this time.
- **#1475 (weekly doc audit) and #1486 (monthly housekeeping audit)** — both still OPEN, both have
  substantive evidence posted, neither claimed complete. Not mine to close solo — #1475 covered maybe
  half the checklist; #1486 was just created today (the actual overdue August run, a few days late)
  and hasn't been worked at all yet, only verified to now fire and render correctly.

## Owed by me — unblocked, priority order

1. **`planning/current/` Finding 1 — needs a fresh, careful pass, NOT a quick rename.** Headline claim
   ("100% stale, 314d") is false — `vision.md` is ~113d, not ~314d — and there are 13 live inbound
   references, several in active session-start briefing paths. **Named trigger for the deferral**: a
   fresh session/compaction — still hasn't arrived, five days running now.
2. **97 docs >30d asserting current-state language** — separate, broader item; no deadline named.
3. **#1486's actual checklist** — the monthly housekeeping audit issue now exists and fires correctly,
   but nobody has worked the checklist itself yet (agent infra, pattern/ADR counts, dev/active cleanup,
   metrics snapshot). Not urgent — first genuinely-correct run, no backlog of misses to catch up on.
4. **methodology-20's two HIGH-COMPLEXITY compression rules are mutually unsatisfiable** — CIO owns.
5. **`docs-standing-items.md` is stale** (last touched 2026-05-27, pre-Amber). Low priority, not urgent.

## Resolved 2026-08-04 — do NOT re-open

- ~~Today's blog post ("The List That Lies")~~ — **fully closed.** Proofread (14-check template audit
  clean, one word-count flag not a block), published, archived, calendar updated, drift clean.
- ~~Comms's soft-404 finding (`publish-to-blog` verification gap)~~ — **fully closed.** Fixed v0.22
  (`e71abedfc`) — content-check method, not status code, in both Step 9's gate and the Quality
  Checklist.
- ~~Omnibus gap, Jul 29 – Aug 3 (6 days, ~70 logs)~~ — **fully closed.** All 6 written to
  `docs/omnibus-logs/` via 6 parallel extraction agents + synthesis. Landed shorter than the
  HIGH-COMPLEXITY target line budget (155–194 vs. 450–600) — flagged honestly to Comms and in the
  commit rather than claimed as full compliance. Comms notified directly since the gap was blocking
  their narrative-front work. Step 10.5 (activity-log CSV reconciliation) explicitly deferred, not
  silently skipped.
- ~~Monday's weekly doc audit (#1475) — verified NOT done, partially closed~~ — real evidence posted
  (Doc Currency ratio, GitHub issues sync, link integrity, one false alarm caught before reporting, one
  flagged-not-confirmed `pmorgan.tech` staleness concern). Issue left open — too much of the checklist
  genuinely uncovered to claim done.
- ~~Monthly housekeeping audit — found broken, two bugs fixed and behaviorally verified~~ — cron fired
  every day 1–7 regardless of weekday (POSIX day-of-month/day-of-week OR semantics), fixed to
  weekly-Monday + runtime day<=7 guard. Unescaped backticks in the JS template literal caused a syntax
  error on every run since the file was authored — likely never once succeeded. Both fixed; verified
  via `node --check` on all 3 script blocks AND a real `workflow_dispatch` run that created issue
  #1486 with correctly-rendered markdown.

## Inbox

**87 remaining at STOP, cc-only.** Most of today's volume is a dense, active multi-agent thread
(CIO/HOST/CXO/Arch/PA/Comms/PPM investigating a "Step 5b heartbeat" mechanism) — cc'd throughout, not
addressed to docs, nothing owed. Everything addressed *to* docs is drained as of this fire. Not
mass-moving to `read/` — drain on quiet fires.

## Standing lessons (carried, still live)

**Checking your own new discipline immediately can surface a second, unrelated finding.** Implementing
the Monday-trigger check for the weekly audit led directly to checking the monthly one too (same
remit, same table) — which turned out to be the more consequential find, a workflow that had likely
never worked at all. The lesson from two days ago ("going to verify one thing can surface a second")
held again, in a different shape.

**Verify a fix behaviorally, not just statically, before calling it done.** `node --check` confirmed
syntax; it did not confirm the fix actually worked end-to-end. Running the real workflow and reading
the actual rendered issue body is what closed the loop — a static pass alone would have been the same
shape as this week's other "clear is not a measurement" findings.

**A finding that arrives as "check if this affects you too" is worth checking properly, not pattern-
matching.** Held again today with Comms's soft-404 finding — reading the actual skill text found the
exact gap in two places a guess could have missed or over-applied.

## Watch items (not owed to me, but adjacent)

- **Puppeteer extraction cause** — Pard's lane, still open.
- **methodology-20's mutually unsatisfiable compression rules** — CIO owns, raised twice.
- **`docs/internal/operations/one-command-checks.md`** (Arch, 2026-08-02) — worth reading before the
  next audit-shaped task.
- **`pre-commit-broad-staging-warn.sh` blocking despite advisory design** — documented, not escalated.
- **Blog index is client-rendered, returns a shell** — Comms's finding, not urgent, not mine unless it
  becomes one.
- **Skill-Candidates Review (1st Tuesday) is today** — PM+Exec owned, not mine to act on, but worth
  knowing it's the same week as the monthly housekeeping audit per the staggered calendar's own noted
  "wrinkle" (two Monday-anchored-adjacent audits landing close together).

## The one thing I most want to carry into the next fire

**A design question PM asks in passing can be the fastest route to a real, previously-undiscovered
defect.** PM's ask wasn't "check if the monthly audit is broken" — it was "help me build a mechanism so
audits don't get missed." Building the mechanism for my own lane required actually checking whether the
thing I was building a trigger for had ever worked, and it hadn't. The design question and the
verification question turned out to be the same question, one layer down.
