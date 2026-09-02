# Docs Carry-Forward

**Updated**: 2026-09-02 ~17:0x PDT (Ongoing-milestone backlog PM assigned this session is fully
worked — 6 issues closed, 2 substantially resolved and left open, #1719 filed, Ship #058 published)
**Session log**: `dev/2026/09/02/2026-09-02-0727-docs-code-log.md` (open).
**Cron**: `b6541910`, `57 6,9,12,15,18,21 * * *`, healthy, next fire 18:57.

## No unblocked work outstanding — the whole PM-assigned backlog is closed

PM asked (in-conversation, this session) to work my own portfolio of Ongoing-milestone issues and
delegate the rest. **Fully done**:

- **Closed**: #1259, #1275, #1162, #465 (all stale, evidence on each) · #1584 (broken links, both
  parts — Part A already done 08-10, Part B fixed this session) · #1682 (all 3 items — item 1 by
  Lead, item 3 CITATIONS.md by me) · #1585 (6 items, 2 of 3 "duplicate" calls turned out
  mischaracterized on direct check, corrected rather than forced) · #1611 (mac-dock-integration.md,
  full rewrite against the confirmed single-process architecture) · #1486 (Monthly Housekeeping,
  all 7 sections, real dev/active/ cleanup 183→33 files).
- **Substantially resolved, left open on purpose** (real remaining work, not mine to force):
  #1683 (143/144 calendar rows reconciled, 2 genuine inverse-case residuals need Medium
  verification) · #1392 (5/6 items, 1 real editorial question for PM — does a second, genuinely
  *different* mailbox image belong in the post).
- **Delegated**: 7-issue FLYWHEEL list to CIO (cc Lead Dev) · #1584 Part C and #1682 item 1 routed
  (though Part C turned out already done — see below) · **#1719 filed** for a real recurring
  pattern (file moved, cross-refs not updated — 4th confirmed instance, caught from my own
  dev/active/ cleanup today).

**Two real self-caught mistakes this session, both corrected rather than left standing**:
1. Mailed CIO asking them to redo #1584 Part C — it was already done 2026-08-12, and I'd verified
   it myself at the time. My carry-forward carried it as open without re-checking the issue's own
   comment thread. **Lesson**: read an issue's comment history, not just its original filing,
   before routing it to someone.
2. A `git add` with a stale post-`git mv` path silently aborted the whole add (matches CLAUDE.md's
   documented failure class) — a calendar update looked committed but wasn't. Caught by
   re-verifying content on `origin/main`, not by trusting `git status`'s output at a glance.
   **Lesson**: after any multi-path `git add`, check `git diff --cached --name-only` lists every
   intended file.

**First action next fire**: sync, mail loop, check whether CIO/Lead replied to anything delegated.
Otherwise genuinely open floor — no named priority queued beyond the day-of-week triggers below.

## Weekly Ship #058 published — https://pipermorgan.ai/shipping-news/weekly-ship-058-what-we-actually-had

Independent mechanical audit + 4 load-bearing fact-checks against primary sources, zero
discrepancies. Title-case fix applied same-day (PM caught it) across both repos, live-verified.
hashId `201e33efbf5c`. LinkedIn leg confirmed live by Dispatch-PM, title-case now matches on both
copies. Nothing further owed.

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
- **First Monday of month**: Monthly Housekeeping Audit — just closed (#1486); next one auto-
  generates ~09-07, watch for the same GH-Actions scheduling defect #1713 documented.
- **Every Friday, EARLY**: omnibus logs Fri–Thu. Chain current through 08-28, next batch due 09-04.
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
