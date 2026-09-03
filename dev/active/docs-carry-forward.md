# Docs Carry-Forward

**Updated**: 2026-09-02 ~22:30 PDT (day closed — see `dev/2026/09/02/2026-09-02-0727-docs-code-log.md`,
`<!-- DAY-CLOSED: 2026-09-02 -->`)
**Session log**: none open — next fire (2026-09-03 06:57) creates today's log.
**Cron**: `b6541910`, `57 6,9,12,15,18,21 * * *`, healthy, next fire 06:57.

## No unblocked work outstanding — yesterday's PM-assigned backlog is fully closed

2026-09-02 was a dense day: Weekly Ship #058 published + verified (title-case fix applied
same-day), then the entire Ongoing-milestone backlog PM assigned. **10 issues closed** (#1259,
#1275, #1162, #465, #1584, #1682, #1585, #1611, #1486, plus supporting work), **2 left open on
real conditions** (below), **7 issues delegated to CIO** (FLYWHEEL track), **#1719 filed** for a
genuine recurring pattern (file moved, cross-refs not updated — 4th confirmed instance).
`dev/active/` cleaned 183→33 files (real cleanup, not a target-chase — see the day's session log
for the full accounting and the stale-target note).

**Two real mistakes were caught and corrected in the open** (both now standing practices below):
a redundant delegation to CIO for work already done three weeks earlier, and a silently-dropped
`git add` that made a commit look complete when it wasn't. Full detail in the 2026-09-02 log.

**Genuinely open, not mine to force**:
- **#1683** — 2 inverse-case calendar rows ("Building for Learning", "Drained on Paper") need real
  Medium verification, not guessing. 143/144 rows reconciled.
- **#1392** — "Thirteen Mailboxes" double-hero-image question is PM's editorial call: the body
  figure now references a genuinely *different* image file than the hero (verified by file size,
  not filename similarity), so the original filing's premise no longer holds.

**First action next fire**: sync, mail loop, check whether CIO/Lead replied to the FLYWHEEL
delegation. No named priority queued beyond the day-of-week triggers below — genuinely open floor.

## Doc-currency escalation is working — CIO broadcast it, roles are self-correcting for real

CIO broadcast my 8/31 escalation to the 6 role owners on the 6/19 bulk stamp, using my own
`BRIEFING-ESSENTIAL-DOCS.md` re-verification as the worked example. PA already found a real stale
claim in their own briefing. Nothing further needed from me; watch periodically, don't chase.

## Owed by Web: publish Step 9 automation, target path corrected

`piper-morgan-website#37` — I corrected the automation's target (co-located `published/`, not the
stale `images-archive/` split) based on git history, not memory. **I owe**: update
`docs-notify.js:88`'s text once Web's automation lands. Not urgent — wait for Web's issue to move.

## New standing responsibility: the glossary is a living-core-doc

Per Arch's B2 workstream: `knowledge/piper-morgan-glossary-v1.1.md` is now one of six "current law"
docs (60-day staleness contract). Needs CXO's tracked-state frontmatter at first substantive touch
— not urgent, current header is prose-only.

## ⚠️ PM's local main checkout has a genuine history divergence — PARKED

4 local-only commits (`dc943cabb`, `e5f024bf8`, `ca460a4b8`, `87d068f8a`) blocking
`git pull --ff-only` in PM's own checkout. **Do not act on this without PM present** — resume only
if PM re-engages.

## Owed by me — unblocked, low priority

- **PreCompact hook locality differentiation** (added 08-23) — real design work, scope
  deliberately before implementing. Full detail in `docs-standing-items.md`.
- **Critical-docs YAML-frontmatter upgrade** — 95+ days old, own deferral condition is "flag at
  next PM engagement" — hasn't found its moment yet, surface when it does.

## Day-of-week duty triggers — CHECK EVERY START

- **Every Monday**: Weekly Docs Audit.
- **First Monday of month**: Monthly Housekeeping Audit — just closed (#1486, 2026-09-02); next
  one auto-generates ~09-07, watch for the same GH-Actions scheduling defect #1713 documented.
- **Every Friday, EARLY**: omnibus logs Fri–Thu. Chain current through 08-28, next batch due 09-04
  (Friday) — covers 08-29 through 09-04.
- **First Tuesday**: Skill-Candidates Review — not mine (PM+Exec+CIO).
- **Not mine otherwise**: Role Health Check (4-weekly, HOST).

## Standing practices (apply at every fire, not just START)

- A duty-cycle sync from earlier in the session is a timestamped fact, not a durable one — `git
  fetch` + fast-forward before reading state, if meaningful time has passed.
- **"Last scheduled fire of today" is arithmetic on the cron expression**, not a feel-based
  judgment. Verify before STOPping.
- **A fire is a WAKE, not a time-box** — when nothing is genuinely blocking, keep draining rather
  than deferring to "an upcoming fire." The only legitimate reasons to hold something are a real
  external blocker (waiting on someone else, per #1683/#1392 above) or a genuine capacity limit
  (context compaction) — never "there's a lot of it."
- **Read an issue's comment history before routing it to someone** — not just the original filing.
  A carry-forward note can go stale exactly the way the issue itself can.
- **After any multi-path `git add`, verify with `git diff --cached --name-only`** — don't infer
  staging state from `git status --short`'s summary alone.

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.

---

*Full history: prior versions of this file are in git log
(`git log -p -- dev/active/docs-carry-forward.md`) if ever needed verbatim; the durable record
lives in dated session logs and `docs/omnibus-logs/`.*
