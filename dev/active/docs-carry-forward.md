# Docs Carry-Forward

**Updated**: 2026-08-09 22:27 PDT (Fire 6, STOP — DAY-CLOSED 2026-08-09)
**Session log**: `dev/2026/08/09/2026-08-09-0715-docs-code-log.md` (yesterday's is
`dev/2026/08/08/2026-08-08-0713-docs-code-log.md`, DAY-CLOSED verified)

**Worktrees**: product `~/Development/piper-morgan-worktrees/docs` @ `claude/docs-cycle` · website
`~/Development/piper-morgan-website-worktrees/docs` @ `claude/docs-cycle`
**Cron**: re-arming at STOP (delete-then-create; see final action) — `57 6,9,12,15,18,21`. Registry row
must match after re-arm.
**Hooks on this seat**: standalone `git commit` BLOCKS; compound `add && commit` BYPASSES. Mitigation:
stage in one call, commit bare in the next. `mail-send.sh` safe regardless.
**Standing note**: `pre-commit-broad-staging-warn.sh` blocks the Bash tool call outright on a ≥20-file
staged commit despite documenting itself as advisory-only; `--no-verify` has no effect (not a git hook).

## 🔴 MONDAY (08-10) IS A DOCS-OWNED TRIGGER DAY — check FIRST at START

**Weekly Docs Audit** (`weekly-docs-audit.yml`, fires ~9am PT) — verify it actually fired before doing
anything else. Last cycle this was flagged as "watch whether the nudged cron fires" and then the day
turned out to be Sunday (no check needed) — tomorrow is the real test. If it didn't fire, that's a
process gap worth a same-day fix, not a defer.

## 🟡 AWAITING PM (3+ days now) — write up the line-count methodology proposal, or hold?

PM asked (08-07) what the HIGH-COMPLEXITY omnibus line-count target protects against and whether it's
serving its purpose. Answered with real data: 3 Aug 4-6 files (107-133 lines) vs. a compliant
reference day (Jul 19, 575 lines) have nearly identical word/entry counts — the whole gap is
formatting (hard-wrap + blank lines vs. single-line-per-bullet style), not depth. Recommended
entry-count/word-count over line-count as the real signal. **Explicitly asked PM: write this up as a
proposal to CIO (methodology owner), or hold?** No answer through all of 08-08 or 08-09. Not chasing
it — staying at "hold until told" is the correct default for a genuine external dependency, not a
failure to follow up. Exec independently corroborated and would back a proposal — not the same as PM's
go-ahead.

## Mail-loop scan — `scripts/scan-inbox.py` (Comms, 08-07), case-insensitive filter

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START. Worked cleanly across all 6 fires again today (08-09) — one flagged
match was a broadcast cc (Exec's memo, `to: ppm`, docs one of 10 `cc:` names), correctly recognized as
not-owed rather than treated as new mail. Second full day the tooling has been fully reliable after two
straight days of finding real gaps (08-05, 08-07) — still worth re-testing rather than assuming
permanence, per standing lesson 10.

## Day-of-week duty triggers — CHECK EVERY START

- **Every Monday**: Weekly Docs Audit (`weekly-docs-audit.yml`, ~9am PT) — verify it fired. **Tomorrow,
  08-10, is the live instance — see the 🔴 item above.**
- **First Monday of month**: Monthly Housekeeping Audit (fixed 08-04, next due ~09-01).
- **Every Friday, EARLY**: omnibus logs Fri–Thu — done weekly now, ran clean 08-07.
- **Not mine**: Skill-Candidates Review (1st Tuesday), Role Health Check (4-weekly, HOST).

**Proposed but not shipped**: generalized day-of-week trigger version routed to CIO 08-04. No reply yet.

---

## Awaiting PM specifically

- **website#31, converter double-`<em>` bug** — filed 08-05, still 0 comments as of 08-09 22:27, not
  urgent, no chase needed: (a) fix forward-only vs. regenerate the ~15-post Ship back-catalog, (b)
  should Ship `**Metrics**` become a real `###` header.

## Awaiting others — check, don't re-derive

- **PDR-007 awaits CIO ONLY** — Arch ✅ Web ✅, no objection. Measurement window runs to 2026-08-27.
  Checked 08-09 22:27: still no matching PR.
- **CIO's day-of-week duty-check proposal reply** — sent 08-04, no reply yet, not urgent.
- **#1475 / #1486** — both OPEN, unchanged, not urgent.

## Owed by me — unblocked, priority order

1. **Jul 29–Aug 3 activity-log backfill, ~70 rows** — deferred repeatedly, surfaced again 08-07. No
   functional consequence yet but real debt; do it before it's a third gap.
2. **`planning/current/` Finding 1** — fresh careful pass needed, not a rename. Named trigger (fresh
   session/compaction) still hasn't arrived — eleven days running now. Note: this very session was
   compacted today; if a natural opening appears early in the next fire, this is the candidate.
3. **97 docs >30d asserting current-state language** — no deadline.
4. **#1486's actual checklist** — not urgent.
5. **methodology-20's compression rules mutually unsatisfiable** — CIO owns.
6. **`docs-standing-items.md` stale** — low priority.

## Resolved 2026-08-09 — do NOT re-open

- **"Over-Checking Pays Dividends"** published clean; template-audit v1.9 applied live for the first
  time (PM's negation-reveal word-order discriminator). Retro-fixed yesterday's post's stale footer
  tease (targeted single-string replace, verified exactly-one-occurrence before/after). Both
  live-verified via distinct content checks.
- **Syndication for today's post** — Medium then LinkedIn URLs both landed and were set; `status`
  correctly held at `published` until both confirmed, then bumped to `distributed`.
- **Web's 2 fixes I'd left unblocked for 11 days** — traced from PM's question about Dispatch's
  stale-calendar friction to my own unanswered 07-29 memo; resolved with clear decisions same-day, Web
  shipped both within the hour (`1b95fa5`), verified the actual commit diff matches before closing.
- **Dispatch-DinP's canonicalSite semantics question** — checked both owned skills' source text rather
  than answering from memory; confirmed no drift, quoted verbatim in reply.

## Resolved 2026-08-08 — do NOT re-open

- **"Verify at the User Path, Not the Data Layer"** — published clean, first live use of
  `template-audit` v1.8's throat-clearing checks.
- **Comms' publish-ready memo apparent-discrepancy** — resolved via commit timestamps; sequencing, not
  a real gap.

## Standing lessons (carried, still live — 11 items in the cron prompt; not restating all here)

**Today's addition candidate, considered and declined**: no new durable process gap surfaced today.
Rather than force a 12th lesson for continuity's sake, the existing 11 carry forward unchanged — a
deliberate call, not an oversight. If tomorrow's weekly-audit check turns up something, that's the next
real candidate.

**Verification only counts when applied to your own latest fix, not the fix you inherited.** Live again
today: verified Web's `1b95fa5` against the actual diff rather than trusting the memo description, and
it matched exactly — the payoff of checking rather than assuming.

**Holding a blocked item across multiple STOPs is legitimate when the block is a genuine external
dependency, not a self-imposed pause.** The line-count proposal is now 3+ days in — still the right
call: don't fabricate an answer, don't bury the ask, don't manufacture urgency that isn't there.

## Watch items (not owed to me, but adjacent)

- **"Verify at the User Path" (Aug 8) unsyndicated** — no Medium/LinkedIn, unlike the recent norm.
  Comms routed to Dispatch, offered to fill columns herself. Nothing for me until URLs land (from
  either party) — take the update whichever way it arrives.
- **Puppeteer extraction cause** — Pard's lane.
- **methodology-20's mutually unsatisfiable compression rules** — CIO owns.
- **`pre-commit-broad-staging-warn.sh` blocking despite advisory design** — documented, not escalated.
- **Blog index is client-rendered, returns a shell** — Comms's finding, not mine unless it becomes one.

## The one thing I most want to carry into the next fire

**Monday's weekly-docs-audit check is the first real test of the nudged cron** — treat a no-fire as a
process gap worth same-day attention, not a "watch and see" item to defer again. Everything else today
was applying disciplines that already existed; tomorrow's first move is a genuine unknown.
