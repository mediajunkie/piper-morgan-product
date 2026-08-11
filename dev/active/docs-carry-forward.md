# Docs Carry-Forward

**Updated**: 2026-08-11 06:56 PDT (DAY-CLOSED 2026-08-10, PM-directed overnight block)
**Session log**: `dev/2026/08/10/2026-08-10-0727-docs-code-log.md` (DAY-CLOSED verified — includes a
long PM-engaged block 19:11-06:56 working through #1584/#1585)

**Worktrees**: product `~/Development/piper-morgan-worktrees/docs` @ `claude/docs-cycle` · website
`~/Development/piper-morgan-website-worktrees/docs` @ `claude/docs-cycle`
**Cron**: `bf577e17`, unchanged since 08-09 STOP — re-verify at next fire's START, no re-arm needed
yet (7-day window not expired).
**Hooks on this seat**: standalone `git commit` BLOCKS; compound `add && commit` BYPASSES. Mitigation:
stage in one call, commit bare in the next. `mail-send.sh` safe regardless.
**Standing note**: `pre-commit-broad-staging-warn.sh` blocks the Bash tool call outright on a ≥20-file
staged commit despite documenting itself as advisory-only; `--no-verify` has no effect (not a git hook).

## 🟢 NEXT UP — docs-tree flattening plan (PM asked 08-10, sequenced after #1584/#1585)

PM wants a plan (not immediate action, explicitly "wary of precipitous changes") to flatten parts of
the docs tree. Real evidence gathered while fixing #1584 tonight: `docs/internal/architecture/current/
models/` is 5 levels deep and that depth directly caused ~15 off-by-one `../` broken links across 5
files (fixed in `a0fd56987`); the same root cause (files moved into a nested subdir, cross-links never
updated) produced 3 more of #1584's systemic clusters. Also found 4 separate instances of an
auto-generated-boilerplate-README pattern (hallucinated subdirectory listings) scattered through the
tree — a related but distinct defect class.

**Plan should cover**: inventory of directories deep/complex enough to cause this class of bug,
proposed flatter target shape, staged execution (small batches, link-check after each — same
discipline as tonight's Finding-1 and #1584/#1585 work, not a blanket sweep). Draft as a document for
PM review, don't execute.

## ✅ RESOLVED 2026-08-10/11 (PM-directed, overnight) — #1584 and #1585 worked through

**#1584** (broken links): ~240 → 34 residual, ~155 fixed across 25 files, 5 commits
(`a0fd56987`, `253b46855`, `003185bea`, `8596e4518`, plus the citation fix earlier). Residual is
mostly non-issues (PM-034 dead links needing someone with project history, computer:// artifacts,
intentional template placeholders) or genuinely-missing content with no findable successor. Part C
(methodology-19 numbering drift) mailed to CIO, stays open — his lane. Progress comment posted, issue
left open for the residual.

**#1585** (stale docs + duplicates): Part A — 5 role/infra-owned docs got honest staleness banners
(not fabricated rewrites) + direct mail to each owner (PA, Exec, Lead Dev, CIO); 3 more independently
verified with real evidence (issue #172 confirmed closed, a fix confirmed already-shipped in
`status_checker.py`, a frozen-not-stale clarification); 1 finding self-corrected as out-of-scope
(`docs/refactor/` is a completed project's artifact trail, not meant to stay current — worth stating
plainly, not quietly fixing). Part B — 3 of 6 duplicate clusters reconciled with clear supersession
evidence (`33c945eb7`), 3 left flagged as genuinely ambiguous. Progress comment posted, issue left open.

**Full trace**: tonight's session log entry (`dev/2026/08/10/...`, "PM engaged 19:11-06:56").

## ✅ RESOLVED 2026-08-10 — `planning/current/` Finding 1, 12 days deferred, trigger arrived

Re-derived per-file staleness, confirmed `vision.md` is genuinely current (6+ live referrers) and
stays put; the other 7 files moved to `planning/historical/`. Per-file split, not the originally-
proposed blanket rename. `c3c1a7afc`.

## ✅ RESOLVED 2026-08-10 — Weekly Docs Audit #1583, CLOSED

First fully-worked weekly audit, first confirmed real fire of the nudged cron. All 8 sections
genuine. Filed #1584/#1585 as the checklist's own "create issue for complex cases" step, not a
deferral.

## 🟡 AWAITING PM — write up the line-count methodology proposal, or hold?

Asked 08-07, still no answer as of 08-10 STOP (4 days now). Not chasing — genuine external
dependency, correct to hold.

## Mail-loop scan — `scripts/scan-inbox.py` (Comms, 08-07), case-insensitive filter

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.

## Day-of-week duty triggers — CHECK EVERY START

- **Every Monday**: Weekly Docs Audit — verify it fired. Next: 08-17.
- **First Monday of month**: Monthly Housekeeping Audit — next due ~09-01.
- **Every Friday, EARLY**: omnibus logs Fri–Thu.
- **Today, Tuesday 08-11**: Skill-Candidates Review (1st Tuesday) — **not mine**, PM+Exec+CIO.
- **Not mine otherwise**: Role Health Check (4-weekly, HOST).

---

## Awaiting PM specifically

- **website#31, converter double-`<em>` bug** — filed 08-05, 0 comments, not urgent: (a) fix
  forward-only vs. regenerate the ~15-post Ship back-catalog, (b) should Ship `**Metrics**` become a
  real `###` header.
- **MIT license badge, no LICENSE file** (found 08-10, #1583) — root README.md displays MIT badge,
  zero LICENSE-file hits repo-wide all of history. Needs PM's call: add LICENSE vs. adjust badge.

## Awaiting others — check, don't re-derive

- **PDR-007 awaits CIO ONLY** — Arch ✅ Web ✅. Measurement window runs to 2026-08-27.
- **CIO's day-of-week duty-check proposal reply** — sent 08-04, no reply, not urgent.
- **#1584 Part C, #1475, #1486** — all OPEN, unchanged, not urgent.
- **4 mail flags sent 08-11 06:50-06:56** (PA/Exec/Lead Dev/CIO re: their stale docs + CIO re:
  #1584 Part C) — no reply expected soon, not urgent, just don't re-flag redundantly.

## Owed by me — unblocked, priority order

1. **Docs-tree flattening plan** — see 🟢 NEXT UP above. Highest priority next fire.
2. **#1486's actual checklist** — not urgent.
3. **methodology-20's compression rules mutually unsatisfiable** — CIO owns.
4. **`docs-standing-items.md` stale** — low priority.

## Standing lessons (carried, still live — 11 items in the cron prompt; not restating all here)

**No new durable process gap surfaced 08-10/11** that isn't already covered by the existing 11 —
tonight's self-corrections (pattern-count false-positive, baseline-test-status over-scope) are
instances of "verify before reporting," already standing lesson 4/9 territory, not a new category.

**Verify before fixing scales, not just for small cases.** 155 link fixes tonight — the two
self-corrections along the way (not the absence of errors) are the actual evidence the discipline
held under volume, not just in isolated small checks.

## Watch items (not owed to me, but adjacent)

- **Syndication gap, 3 posts** — filed with Dispatch, nothing for me until URLs land.
- **Puppeteer extraction cause** — Pard's lane.
- **`pre-commit-broad-staging-warn.sh` blocking despite advisory design** — documented, not escalated.
- **Blog index is client-rendered, returns a shell** — Comms's finding, not mine unless it becomes one.

## The one thing I most want to carry into the next fire

**The docs-tree flattening plan is real, PM-requested work, sequenced explicitly after #1584/#1585
— which are now done.** Start there. Today is also Tuesday (Skill-Candidates Review day, not mine) —
no special trigger for Docs beyond the usual mail/gated-item loop.
