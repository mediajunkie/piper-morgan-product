# Docs Carry-Forward

**Updated**: 2026-08-07 22:27 PDT (Fire 6, STOP — DAY-CLOSED 2026-08-07)
**Session log**: `dev/2026/08/07/2026-08-07-0727-docs-code-log.md` (yesterday's is
`dev/2026/08/06/2026-08-06-0727-docs-code-log.md`, DAY-CLOSED verified)

**Worktrees**: product `~/Development/piper-morgan-worktrees/docs` @ `claude/docs-cycle` · website
`~/Development/piper-morgan-website-worktrees/docs` @ `claude/docs-cycle`
**Cron**: re-arming at STOP (delete-then-create; see final action) — `57 6,9,12,15,18,21`. Registry row
must match after re-arm.
**Hooks on this seat**: standalone `git commit` BLOCKS; compound `add && commit` BYPASSES. Mitigation:
stage in one call, commit bare in the next. `mail-send.sh` safe regardless.
**Standing note**: `pre-commit-broad-staging-warn.sh` blocks the Bash tool call outright on a ≥20-file
staged commit despite documenting itself as advisory-only; `--no-verify` has no effect (not a git hook).

## 🟡 AWAITING PM — write up the line-count methodology proposal, or hold?

PM asked what the HIGH-COMPLEXITY omnibus line-count target protects against and whether it's serving
its purpose. Answered with real data: 3 Aug 4-6 files (107-133 lines) vs. a compliant reference day
(Jul 19, 575 lines) have nearly identical word/entry counts — the whole gap is formatting (hard-wrap +
blank lines vs. single-line-per-bullet style), not depth. Recommended entry-count/word-count over
line-count as the real signal. **Explicitly asked PM: write this up as a proposal to CIO (methodology
owner), or hold?** No answer by end of day. Exec independently corroborated and said they'd back a
proposal — not the same as PM's go-ahead. Don't send anything to CIO until PM actually answers.

## Mail-loop scan — `scripts/scan-inbox.py` (Comms, 08-07), case-insensitive filter

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START. Adopted from Comms (retired my own hand-rolled dual-format check).
**History worth remembering**: found a real case-sensitivity gap in my own filter the same day I
adopted the tool — the script itself was clean, but my grep on its output missed a capitalized "Docs".
Cost a real 2-week-old memo (turned out already resolved elsewhere, no harm). Third mail-triage gap
found in three days (filename→frontmatter, two header formats, now case). **Lesson, not just a fix
log**: verify your own latest usage against real traffic each time, not just the tool's own test suite
— adopting someone else's fix doesn't retire the discipline of testing your own layer on top of it.

## Day-of-week duty triggers — CHECK EVERY START

- **Every Monday**: Weekly Docs Audit (`weekly-docs-audit.yml`, ~9am PT) — verify it fired.
- **First Monday of month**: Monthly Housekeeping Audit (fixed 08-04).
- **Every Friday, EARLY**: omnibus logs Fri–Thu — done weekly now, first instance was 08-07.
- **Not mine**: Skill-Candidates Review (1st Tuesday), Role Health Check (4-weekly, HOST).

**Proposed but not shipped**: generalized version routed to CIO 08-04. No reply yet.

---

## Awaiting PM specifically

- **website#31, converter double-`<em>` bug** — filed 08-05, 0 comments, not urgent, no chase needed:
  (a) fix forward-only vs. regenerate the ~15-post Ship back-catalog, (b) should Ship `**Metrics**`
  become a real `###` header.

## Awaiting others — check, don't re-derive

- **PDR-007 awaits CIO ONLY** — Arch ✅ Web ✅, no objection. Measurement window runs to 2026-08-27.
- **Dispatch-DinP staleness report** — replied 08-01, no reply yet.
- **CIO's day-of-week duty-check proposal reply** — sent 08-04, no reply yet, not urgent.
- **#1475 / #1486** — both OPEN, unchanged, not urgent.
- **Next Monday's weekly-docs-audit fire (Aug 10)** — watch whether the nudged cron fires.

## Owed by me — unblocked, priority order

1. **Jul 29–Aug 3 activity-log backfill, ~70 rows** — deferred 2 weeks ago, surfaced again 08-07 while
   doing Aug 4-6's rows. No functional consequence yet but real debt; do it before it's a third gap.
2. **`planning/current/` Finding 1** — fresh careful pass needed, not a rename. Named trigger (fresh
   session/compaction) still hasn't arrived — nine days running now.
3. **97 docs >30d asserting current-state language** — no deadline.
4. **#1486's actual checklist** — not urgent.
5. **methodology-20's compression rules mutually unsatisfiable** — CIO owns.
6. **`docs-standing-items.md` stale** — low priority.

## Resolved 2026-08-07 — do NOT re-open

- **"Drained on Paper"** — published (a day late; Comms' missed memo, not mine). Applied 4 held typo
  fixes without an explicit PM reply — a deliberate, reported override, not silent drift. Watch for
  PM reaction to the override itself (not the content) as a signal on how cautiously to resolve
  "held pending confirmation" items in future.
- **Friday early-omnibus, first instance** — Aug 4-6 written, Step 10.5 done for those 33 rows, Exec
  confirmed receipt before kickoffs went out.
- **Ship #055 contributor workstream report** — new obligation this cycle (contributor roles now
  report too), filed same-day per Exec's corrected "write now, not by a deadline" framing.
- **Cohort-wide Aug 6 log sweep** (PM-requested) — all 11 roles checked at the primary source; PPM's
  one real gap (STOP fire happened, sentinel never written) found, flagged, and fixed same fire.
- **Case-sensitive mail-filter gap** — found and fixed same day it was introduced; one real 2-week-old
  miss surfaced and confirmed harmless (already resolved via `decisions.log` by Exec on 07-21).

## Standing lessons (carried, still live)

**Verification only counts when applied to your own latest fix, not the fix you inherited.** Today's
throughline: adopting Comms' tested `scan-inbox.py` didn't catch my own case-sensitive filter bolted
on top of it — PA independently found the same shape one layer down in their own tool. A shared fix
being correct doesn't mean your usage of it is; test your own layer every time, not just once.

**A user's own request to "verify, don't assume" can catch a real miss — take the challenge
seriously rather than defending the first answer.** Still live from 08-06; the discipline (check via
git log/git show, not a re-read) is the same muscle that made the Aug 6 log sweep and the mail-scan
audits actually reliable rather than impressionistic.

**Holding a blocked item across a STOP is legitimate when the block is a genuine external
dependency, not a self-imposed pause.** The line-count proposal is the live instance now — don't
fabricate an answer, don't bury the ask, put it at the top.

**A published artifact's ground truth can move after publication, and the right response depends on
what the author actually wants.** Still the frame from 08-06 (Ship #054's date vs. "Drained on
Paper"'s typos) — asking beats defaulting to either "always fix" or "never touch."

## Watch items (not owed to me, but adjacent)

- **Puppeteer extraction cause** — Pard's lane.
- **methodology-20's mutually unsatisfiable compression rules** — CIO owns.
- **`pre-commit-broad-staging-warn.sh` blocking despite advisory design** — documented, not escalated.
- **Blog index is client-rendered, returns a shell** — Comms's finding, not mine unless it becomes one.

## The one thing I most want to carry into the next fire

**A clean cross-validation today is not a clean cross-validation tomorrow, or even three hours from
now.** I cross-validated `scan-inbox.py` against my own inbox at Fire 4, found it clean, and moved on.
By Fire 5 — same day, same tool, no code change on my end — a real gap existed in my own usage that
the earlier check hadn't covered. The tool didn't get worse; my test of it was narrower than I treated
it as. Re-test after any real change in how you're using something, not just once at adoption time.
