# Docs Carry-Forward

**Updated**: 2026-08-12 07:33 PDT (Fire 1 of the day)
**Session log**: `dev/2026/08/12/2026-08-12-0733-docs-code-log.md` (today, open). 08-11's log
(`dev/2026/08/11/2026-08-11-0645-docs-code-log.md`) now carries `DAY-CLOSED`.

**Worktrees**: product `~/Development/piper-morgan-worktrees/docs` @ `claude/docs-cycle` · website
`~/Development/piper-morgan-website-worktrees/docs` @ `claude/docs-cycle`
**Cron**: `e47bd40c` (re-armed 2026-08-11 13:16 PDT post-reboot, replaces `bf577e17` which was
deliberately CronDelete'd ahead of the reboot per Pard's second stand-down notice). Same schedule
`57 6,9,12,15,18,21 * * *`. Prompt rewritten thin (constants + pointer to `duty-cycle-tick` skill +
this file), not re-frozen with the eleven standing lessons inline — recoverable verbatim from
`dev/active/duty-cycle-registry.tsv`'s STOP-chain history if ever needed. Registry row: `active:`.
**Hooks on this seat**: standalone `git commit` BLOCKS; compound `add && commit` BYPASSES. Mitigation:
stage in one call, commit bare in the next. `mail-send.sh` safe regardless.
**Standing note**: `pre-commit-broad-staging-warn.sh` blocks the Bash tool call outright on a ≥20-file
staged commit despite documenting itself as advisory-only; `--no-verify` has no effect (not a git hook).

## ✅ RESOLVED 2026-08-12 (Fire 1) — Write-Path-Chase pinch-hit follow-up + Lead's stale-docs reply

Janus's three flagged follow-ups from the 08-11 pinch-hit publish: 2 were already done same evening
by others; the stale "STILL BLOCKING PUBLISH" calendar notes text was still open — fixed
(`e15de4089`). Filed a real bug Janus hit (`--pub-date` silent UTC default, same shape as the fixed
`--work-date` bug) as **piper-morgan-website#32**. Replied to Janus at the correct cross-repo
channel (`designinproduct/docs/mail/`, `52f8811`) — caught and corrected a near-miss where I almost
wrote to this repo's known-dead-letter `mailboxes/janus/` instead.

Lead Dev's reply closes both stale-doc mail flags from #1585 (`ROLE-PORTFOLIO-LEAD-DEV.md`,
`environment-status.md`) — both audit rows now resolved, no further Docs action.

**🟡 Awaiting PM, low priority**: `claude/fix-docker-migration-setup` — merge-keeper sweep flagged
it (escalation: stray `.DS_Store` blobs). Confirmed genuinely abandoned (last commit 2026-03-31,
predates v0.8.6). Not mine to delete unilaterally (destructive). Recommend deletion when PM has a
moment; not urgent.

**🔵 In progress**: background subagent triaging the ~163-memo cc-only backlog in
`mailboxes/docs/inbox/` (mostly the multi-week cycling-roles dispatch-latency investigation,
2026-07-21 through 08-11) — confirming rather than assuming it's safe to bulk-file as read, and
surfacing anything that actually needs Docs. Report pending; action on next touch.

## ✅ RESOLVED 2026-08-11 (Fire 1) — docs-tree flattening plan drafted, awaiting PM's go/no-go

Plan written: `docs/internal/operations/docs-tree-flattening-plan-2026-08-11.md` (`0bca3ca8c`).
One high-confidence candidate (`docs/internal/planning/roadmap/CORE/`, 9 subdirs/76 files, every
filename already fully encodes its epic — nesting is 100% redundant). 3 categories explicitly
ruled out with reasons (adrs/patterns sound as-is; legacy-guides carry real info, already fixed;
image archive deep-by-design). **Not executed** — a document only, per PM's stated wariness.

**Bigger finding along the way, filed separately as #1593**: `.github/workflows/link-checker.yml`
correctly detects broken links (verified against a pre-#1584-fix run's own log) but the workflow
always reports success regardless — very likely the actual reason ~240 broken links accumulated
silently. This matters more than the flattening plan itself; flagged as such in the plan doc.

**Awaiting PM**: go/no-go on executing the one recommended flatten (`roadmap/CORE/`).

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
- **#1593** (link-checker.yml never fails despite detecting real breaks, filed 08-11) — not
  mine to fix (CI/workflow ownership), not urgent, but worth a periodic check whether it's
  picked up since it explains a real recurring-defect mechanism.
- **4 mail flags sent 08-11 06:50-06:56** (PA/Exec/Lead Dev/CIO re: their stale docs + CIO re:
  #1584 Part C) — no reply expected soon, not urgent, just don't re-flag redundantly.
- **Docs-tree flattening plan go/no-go** — plan posted, awaiting PM's decision on executing the
  one recommended flatten (`roadmap/CORE/`). Not chasing.

## Owed by me — unblocked, priority order

1. **#1486's actual checklist** — not urgent.
2. **methodology-20's compression rules mutually unsatisfiable** — CIO owns.
3. **`docs-standing-items.md` stale** — low priority.

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
