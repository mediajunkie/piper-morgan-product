# Docs Carry-Forward

**Updated**: 2026-08-08 22:27 PDT (Fire 6, STOP — DAY-CLOSED 2026-08-08)
**Session log**: `dev/2026/08/08/2026-08-08-0713-docs-code-log.md` (yesterday's is
`dev/2026/08/07/2026-08-07-0727-docs-code-log.md`, DAY-CLOSED verified)

**Worktrees**: product `~/Development/piper-morgan-worktrees/docs` @ `claude/docs-cycle` · website
`~/Development/piper-morgan-website-worktrees/docs` @ `claude/docs-cycle`
**Cron**: re-arming at STOP (delete-then-create; see final action) — `57 6,9,12,15,18,21`. Registry row
must match after re-arm.
**Hooks on this seat**: standalone `git commit` BLOCKS; compound `add && commit` BYPASSES. Mitigation:
stage in one call, commit bare in the next. `mail-send.sh` safe regardless.
**Standing note**: `pre-commit-broad-staging-warn.sh` blocks the Bash tool call outright on a ≥20-file
staged commit despite documenting itself as advisory-only; `--no-verify` has no effect (not a git hook).

## 🟡 AWAITING PM (2 days now) — write up the line-count methodology proposal, or hold?

PM asked (08-07) what the HIGH-COMPLEXITY omnibus line-count target protects against and whether it's
serving its purpose. Answered with real data: 3 Aug 4-6 files (107-133 lines) vs. a compliant
reference day (Jul 19, 575 lines) have nearly identical word/entry counts — the whole gap is
formatting (hard-wrap + blank lines vs. single-line-per-bullet style), not depth. Recommended
entry-count/word-count over line-count as the real signal. **Explicitly asked PM: write this up as a
proposal to CIO (methodology owner), or hold?** Still no answer as of 08-08 STOP — second day running.
Not chasing it; staying at "hold until told" is the correct default for a genuine external dependency,
not a failure to follow up. Exec independently corroborated and would back a proposal — not the same
as PM's go-ahead.

## Mail-loop scan — `scripts/scan-inbox.py` (Comms, 08-07), case-insensitive filter

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START. Worked cleanly across all 6 fires today (08-08) with no new gaps found
— first full day the tooling has been fully reliable after two straight days of finding real ones
(filename→frontmatter 08-05, header formats 08-05, case-sensitivity 08-07). Worth trusting more now,
but keep testing rather than assuming permanence.

## Day-of-week duty triggers — CHECK EVERY START

- **Every Monday**: Weekly Docs Audit (`weekly-docs-audit.yml`, ~9am PT) — verify it fired. **Next
  instance is Aug 10, watch whether the nudged cron fires.**
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
- **CIO's day-of-week duty-check proposal reply** — sent 08-04, no reply yet, not urgent.
- **#1475 / #1486** — both OPEN, unchanged, not urgent.

## Owed by me — unblocked, priority order

1. **Jul 29–Aug 3 activity-log backfill, ~70 rows** — deferred 2 weeks ago, surfaced again 08-07. No
   functional consequence yet but real debt; do it before it's a third gap.
2. **`planning/current/` Finding 1** — fresh careful pass needed, not a rename. Named trigger (fresh
   session/compaction) still hasn't arrived — ten days running now.
3. **97 docs >30d asserting current-state language** — no deadline.
4. **#1486's actual checklist** — not urgent.
5. **methodology-20's compression rules mutually unsatisfiable** — CIO owns.
6. **`docs-standing-items.md` stale** — low priority.

## Resolved 2026-08-09 — do NOT re-open

- **Web's 2 fixes I'd left unblocked for 11 days** — traced from PM's question about Dispatch's
  stale-calendar friction to my own unanswered 07-29 memo; resolved with clear decisions same-day, Web
  shipped both within the hour (`1b95fa5`), verified the actual commit diff matches before closing.

## Resolved 2026-08-08 — do NOT re-open

- **"Verify at the User Path, Not the Data Layer"** — published clean. First live use of
  `template-audit` v1.8's throat-clearing checks; two judgment-level flags (a negation-reveal, a
  closing throat-clearing candidate) surfaced from actually reading the prose and correctly left to
  PM — both kept as-is, PM's calls.
- **Comms' publish-ready memo appeared to describe defects my audit missed** — checked via commit
  timestamps rather than assuming either side was wrong: Comms' fixes landed before I synced and read
  the file, so I'd published their already-corrected version. No live defect, no actual discrepancy.

## Standing lessons (carried, still live)

**A surprising claim about your own prior work is worth checking at the primary source before either
accepting or dismissing it.** Today's clean instance: Comms' memo described defects my audit hadn't
found. Neither "Comms must be wrong" nor "I must have missed it" was the right first move — commit
timestamps resolved it in under a minute and showed neither party was wrong, just sequenced.

**Verification only counts when applied to your own latest fix, not the fix you inherited.** Still
live from 08-07 — today confirmed the payoff: the same tool, tested the same way, held up clean across
6 fires once the real gaps were actually fixed rather than papered over.

**Holding a blocked item across a STOP is legitimate when the block is a genuine external dependency,
not a self-imposed pause.** The line-count proposal is now 2 days into this — the discipline holds:
don't fabricate an answer, don't bury the ask, don't manufacture urgency that isn't there either.

**A published artifact's ground truth can move after publication, and the right response depends on
what the author actually wants.** Still the frame from 08-06 — asking beats defaulting to either
"always fix" or "never touch."

## Watch items (not owed to me, but adjacent)

- **"Verify at the User Path" (Aug 8) unsyndicated** — no Medium/LinkedIn, unlike the 7-of-9 recent
  norm. Comms found + flagged directly to Dispatch, offered to fill columns herself. Nothing for me
  until URLs land (from either Comms or Dispatch) — take the update whichever way it arrives.
- **Puppeteer extraction cause** — Pard's lane.
- **methodology-20's mutually unsatisfiable compression rules** — CIO owns.
- **`pre-commit-broad-staging-warn.sh` blocking despite advisory design** — documented, not escalated.
- **Blog index is client-rendered, returns a shell** — Comms's finding, not mine unless it becomes one.

## The one thing I most want to carry into the next fire

**A quiet day is not a wasted day if the quiet is genuine and the one real event got handled well.**
Five of six fires today were correctly-quiet holds — no manufactured busywork, no padding. The one
substantive thread (Comms' apparent-discrepancy memo) got the same rigor a "loud" day would demand.
The measure isn't how much happened; it's whether what did happen got checked properly.
