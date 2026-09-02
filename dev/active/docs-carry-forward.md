# Docs Carry-Forward

**Updated**: 2026-09-02 ~12:1x PDT (Ship #058 published + title-case fixed; Ongoing-milestone
audit backlog triaged and delegated; FLYWHEEL backlog assessed, 4 issues closed, 7 delegated to CIO)
**Session log**: `dev/2026/09/02/2026-09-02-0727-docs-code-log.md` (open).
**Cron**: `b6541910`, `57 6,9,12,15,18,21 * * *`, healthy, next fire 12:57.

## Ongoing-milestone backlog work (PM-directed) — 3 closed, 1 open-with-real-remainder, 5 still queued

**Closed this session**: #1259/#1275/#1162/#465 (stale, evidence on each), **#1584** (both
Parts A+B — Part A was already done 08-10, Part B fixed today: 4 real fixes + 4 dead-link
annotations, ~28 remaining hits are all already-dispositioned low-priority/historical/false-
positive, not actionable). **#1682**: item 1 closed by Lead (verify-first — deleted a leftover
duplicate, not moved), item 2 already fixed 08-30 — **only item 3 (CITATIONS.md) remains, mine.**

⚠️ **Caught a real mistake mid-fire**: mailed CIO asking them to fix #1584 Part C, which turned
out already done 2026-08-12 (and *I'd verified it myself* at the time) — my carry-forward carried
it as still-open without re-checking the issue's own comment thread. Sent CIO a direct correction
owning the cause. **Lesson for future backlog triage: read an issue's comment history, not just
its original filing, before routing it to someone.**

**#1644** left open (not closeable) — its 56 broken-link residual is resolved (same #1584 pass),
but PPM's own 08-24 fix explicitly flagged the full v19 roadmap.md historical fold as separately,
genuinely still owed. Not mine; don't touch without PPM.

**Closed since**: #1682 (all 3 items — item 3 CITATIONS.md real targeted review, fixed a genuinely
wrong MCP platform claim, verified spatial-intelligence claim still accurate). **#1683 partially
resolved** (143/144 rows reconciled with a data-verified completion rule after the issue's own
day-of-week theory failed a spot-check; left open for 2 new inverse-case residuals — "Building for
Learning" and "Drained on Paper," need real Medium verification, not guessing).

**#1392 mostly resolved this session**: 5 of 6 items done (2 already fixed independently before I
checked, 2 more already fixed, 1 new instance found+fixed). Left open for PM's call on
`thirteen-mailboxes` — the body figure now references a genuinely *different* image than the hero
(not the literal duplicate the issue described), real editorial question, not mine to guess.

**#1585 CLOSED** — all 6 items resolved. 2 of 3 duplicate-file calls turned out mischaracterized
in the original filing (checked directly, not trusted) — canonical-queries pair aren't duplicates;
INDEX.md's real problem was staleness, not discoverability.

**#1611 CLOSED** — confirmed the architecture (single-process, not two), full rewrite of the doc
(scripts + framing), kept in the visitor-facing KEEP set.

**5 issues closed this fire total**: #1584, #1682, #1585, #1611, plus the earlier
#1259/#1275/#1162/#465 batch. **2 substantially resolved, appropriately left open**: #1683
(143/144 rows, 2 genuine residuals need Medium verification), #1392 (5/6 items, 1 real editorial
question for PM).

**Still genuinely queued, mine**:
- **#1486** — Monthly Housekeeping Audit, 33 items, not due to auto-regen until ~09-07 but already
  open and actionable now that B3/#1712 are both closed

Sent CIO a 7-issue delegation list (cc Lead Dev) for the current-stage-relevant FLYWHEEL backlog
that shouldn't sit on Lead. Full reasoning in today's session log.

## Weekly Ship #058 published — https://pipermorgan.ai/shipping-news/weekly-ship-058-what-we-actually-had

PM-engaged (not a cron fire). Independent mechanical audit + 4 load-bearing fact-checks against
primary sources (issues-closed count, connector-investigation numbers, heading-defect count,
learning-pattern callback) — zero discrepancies. hashId `201e33efbf5c`. **Syndication leg owed**:
LinkedIn only (`theme=ship`), owed to Dispatch-PM — memo sent to Comms/Exec/PM naming it.

⚠️ **Real self-caught bug worth remembering**: a `git add` with 4 paths, one of them already
stale post-`git mv`, aborted the *whole* add silently (matches CLAUDE.md's documented 08-30/31
failure class) — the calendar status update never landed in the first "archive" commit despite
looking committed. Caught by re-verifying content on `origin/main`, not by trusting `git status`'s
leading-space staged/unstaged distinction at a glance. Fixed same-fire (`be7c56524`). **Lesson**:
after any multi-path `git add`, check `git diff --cached --name-only` lists every intended file —
don't infer from `git status --short`'s single-line summary alone.

## Doc-currency escalation is working — CIO broadcast it, roles are self-correcting for real

CIO broadcast my 8/31 escalation to the 6 role owners on the 6/19 bulk stamp, using my own
`BRIEFING-ESSENTIAL-DOCS.md` re-verification as the worked example. PA already found a real stale
claim in their own briefing ("you are not autonomous," 2 months post-Amber-migration) rather than
blind-bump — the mechanism this escalation was for is visibly working. Nothing further needed from
me; watch periodically, don't chase.

## Owed by Web: publish Step 9 automation, target path corrected

`piper-morgan-website#37` — Exec found Step 9 (image archival) is documented but has no code, real
near-miss on PM's laptop. I confirmed the shape but corrected the target: checked git history
(not memory) and found my own last 2 publishes drifted from the documented `images-archive/` split
to co-locating image+`.md` in `drafts/published/`. Told Exec/Web to build against the actual
current practice, not the stale doc. **I owe**: update `docs-notify.js:88`'s text once Web's
automation lands, so doc and mechanism agree. Not urgent — wait for Web's issue to move.

## 2026-09-01, fully closed — see that day's session log for full detail

B3 corpus-disposition CLOSED (81/81 patterns, Arch's cross-corpus synthesis ruling executed
same-day including a real P-059→m-22 judgment call — full trace in
`docs/internal/architecture/reviews/2026-08-architectural-review/b3-patterns-disposition.md`).
"A Sender-Impersonation Bug" published + fully syndicated, nothing owed. **New standing practice
adopted**: publish-confirmation memos now name which syndication legs are owed and to whom, per
theme routing — carries forward indefinitely, not a 09-01-only item. Weekly Docs Audit #1712
driven to substantive completion (~10 sections, real evidence, left open for other-role items).
`.md` frontmatter is authoritative for editorial calendar data; calendar CSV is derived/convenience.

## Watch: CIO's response on the doc-currency escalation

Mailed 2026-09-01 (`c98ca3d65`) — 31/38 operating docs stale, 20 on an identical 6/19 bulk stamp,
crossed the 75% threshold. Cohort-wide staleness mechanism, not mine to fix beyond my own two
docs. Don't re-chase before next Monday's audit.

## Monthly Housekeeping Audit (#1486) — not due yet

33 unchecked items, zero progress since 2026-08-05. September's audit won't auto-generate until
~09-07 (may need another manual dispatch given the 08-31 scheduled-workflow defect — watch for
it, #1713 has the evidence if it recurs). No time pressure.

## New standing responsibility: the glossary is a living-core-doc

Per Arch's B2 workstream: `knowledge/piper-morgan-glossary-v1.1.md` is now one of six "current law"
docs (60-day staleness contract). Needs CXO's tracked-state frontmatter at first substantive touch
— not urgent, current header is prose-only.

## ⚠️ PM's local main checkout has a genuine history divergence — PARKED

4 local-only commits (`dc943cabb`, `e5f024bf8`, `ca460a4b8`, `87d068f8a`) blocking
`git pull --ff-only` in PM's own checkout. A `diff origin/main..HEAD --stat` was pulled (touches
~20+ files, not obviously safe-to-discard) but never reviewed. **Do not act on this without PM
present** — resume only if PM re-engages.

## Awaiting others (check periodically, don't re-derive)

- **#1584** (broken links, ~34 residual) — CIO's Part C (methodology-19 numbering drift), his lane.
- **#1585** (6 genuinely-remaining low-priority items) — none urgent.
- **#1682** (item 1 Lead Dev's lane, item 3 explicitly no-urgency) — item 2 fixed 08-30.

## Owed by me — unblocked

- **PreCompact hook locality differentiation** (added 08-23) — real design work, scope
  deliberately before implementing. Full detail in `docs-standing-items.md`.
- **Critical-docs YAML-frontmatter upgrade** — 95 days old per CIO's dating audit, own deferral
  condition is "flag at next PM engagement" — hasn't found its moment yet, surface when it does.

## ✅ pmorgan.tech scrub — CORRECTED 2026-09-02, this was actually DONE, not "remaining queue"

The prior line here (carried since ~08-14) said "remaining queue, batched over fires" without
re-verification. Checked directly today: all 3 Phase-3 guard rails from
`docs/internal/operations/docs-site-scoping-proposal-2026-08-12.md`'s sequencing are complete —
**#1593** (link-checker gate) is CLOSED, `docs/CONTRIBUTING.md` carries the two-surfaces scoping
note, `docs/_config.yml` carries the owner/review-trigger comment. Phase-2 staleness/link pass was
already logged COMPLETE in that doc's own 2026-08-14 status update. **Live-verified** just now:
`https://pmorgan.tech/` (kept surface) → 200; excluded surfaces (`internal/...`, `NAVIGATION.html`)
→ 404, exactly as designed. Nothing left on this item — nothing further owed.

## Day-of-week duty triggers — CHECK EVERY START

- **Every Monday**: Weekly Docs Audit.
- **First Monday of month**: Monthly Housekeeping Audit (#1486).
- **Every Friday, EARLY**: omnibus logs Fri–Thu.
- **First Tuesday**: Skill-Candidates Review — not mine (PM+Exec+CIO).
- **Not mine otherwise**: Role Health Check (4-weekly, HOST).

## Standing practices (apply at every fire, not just START)

- A duty-cycle sync from earlier in the session is a timestamped fact, not a durable one — `git
  fetch` + fast-forward before reading state, if meaningful time has passed.
- **"Last scheduled fire of today" is arithmetic on the cron expression** (does the *next* slot
  fall on a different date), not a feel-based judgment on how much of the day seems done. Verify
  before STOPping — this bit once (2026-08-30), corrected, held on 2026-08-31.

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.

---

*Full history: prior versions of this file are in git log
(`git log -p -- dev/active/docs-carry-forward.md`) if ever needed verbatim; the durable record
lives in dated session logs and `docs/omnibus-logs/`.*
