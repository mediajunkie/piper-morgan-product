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

## 🟠 ACTIVE — Weekly Docs Audit #1583, 6 of 8 sections done, 2 remain — pick up next fire

**All 3 background subagents landed and were consolidated this fire** (verified each factual claim before
acting — caught nothing wrong this time, but the discipline is what makes that trustworthy). Real fixes
shipped: CITATIONS.md Serena attribution (`32d6cba9b`), NAVIGATION.md/INDEX.md methodology-43-47 gap
(`34457f82f`), duplicate draft removed (`06209210d`). Two tracking issues filed for what's too large for
one sitting: **#1584** (~240 broken links, 2 methodology cross-ref drifts) and **#1585** (11 stale
current-state docs, 6 duplicate-file clusters).

**Completion Matrix state** (posted to #1583, both progress comments):
- ✅ Briefing Freshness, Link Integrity, Omnibus Coverage, GitHub Issues Sync, Quality Checks (both READMEs)
- ⏳ **Sprint & Roadmap Alignment** — checked, roadmap.md is PPM's actively-maintained artifact (4 days
  old), marked verified-current rather than edited (not my lane) — arguably done, but worth a final look
  next fire before checking the box.
- ⏳ **Pattern & Knowledge Capture** — pattern-count sub-check done (no real discrepancy). Session-log
  pattern-mining sub-item NOT started — this is the one genuinely open piece of audit work.
- ⏳ **Staggered-audit-calendar update** — final closing step, blocked on everything else finishing.

**Next fire, in order**: (1) do the session-log pattern-mining pass, (2) confirm Sprint/Roadmap can be
checked off, (3) update `docs/internal/operations/staggered-audit-calendar-2026.md`, (4) fill the final
Completion Matrix and close #1583 via `close-issue-properly`. Do NOT close early — Pattern-046 (no silent
skipping) applies to the checklist's own gate.

**New PM item, not urgent**: root README.md's MIT license badge has **no LICENSE file anywhere in repo
history** (verified via `find` + `git log --all`) — needs PM's call (add LICENSE vs. adjust badge), added
below in "Awaiting PM specifically."

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
- **MIT license badge, no LICENSE file** (found 08-10, weekly-docs-audit #1583) — root README.md
  displays an MIT badge; `find . -iname "LICENSE*"` and `git log --all -- LICENSE*` both return zero
  hits, repo-wide, all of history. Needs PM's call: add a real LICENSE file, or adjust/remove the badge.
  Not urgent, not blocking, flagged in #1583's progress comment.

## Awaiting others — check, don't re-derive

- **PDR-007 awaits CIO ONLY** — Arch ✅ Web ✅, no objection. Measurement window runs to 2026-08-27.
  Checked 08-09 22:27: still no matching PR.
- **CIO's day-of-week duty-check proposal reply** — sent 08-04, no reply yet, not urgent.
- **#1475 / #1486** — both OPEN, unchanged, not urgent.

## Owed by me — unblocked, priority order

1. **`planning/current/` Finding 1** — fresh careful pass needed, not a rename. Named trigger (fresh
   session/compaction) still hasn't arrived — twelve days running now. This session was compacted
   08-09; still hasn't found a natural opening since.
2. **97 docs >30d asserting current-state language** — no deadline.
3. **#1486's actual checklist** — not urgent.
4. **methodology-20's compression rules mutually unsatisfiable** — CIO owns.
5. **`docs-standing-items.md` stale** — low priority.

## Resolved 2026-08-10 — do NOT re-open

- **Jul 29–Aug 3 activity-log backfill, 77 rows** — deferred since 08-04 (that day's own omnibus
  catch-up explicitly deferred its Step 10.5). Delegated to a background subagent, verified
  independently (row counts, field-count parse, convention spot-check, diff scope), committed
  `98b569e3c`, pushed clean.

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

- **Syndication gap, now 3 posts not 1 (updated 08-10 07:27)** — Comms' 08-09 report was scoped to 2
  rows she happened to compare; a proper sweep this morning (08-10) found 3 genuinely unsyndicated
  (*The Package and the First Bite* Jul 9, *Drained on Paper* Aug 7, *Verify at the User Path* Aug 8)
  and 1 partial (*The Team Catches the Cycle*, Medium only). 2 more were bookkeeping-only and Comms
  fixed those herself (commit `46782a55e`, verified real). All filed with Dispatch already. Nothing for
  me until URLs land.
- **Puppeteer extraction cause** — Pard's lane.
- **methodology-20's mutually unsatisfiable compression rules** — CIO owns.
- **`pre-commit-broad-staging-warn.sh` blocking despite advisory design** — documented, not escalated.
- **Blog index is client-rendered, returns a shell** — Comms's finding, not mine unless it becomes one.

## The one thing I most want to carry into the next fire

**Monday's weekly-docs-audit check is the first real test of the nudged cron** — treat a no-fire as a
process gap worth same-day attention, not a "watch and see" item to defer again. Everything else today
was applying disciplines that already existed; tomorrow's first move is a genuine unknown.
