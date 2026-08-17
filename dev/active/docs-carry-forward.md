# Docs Carry-Forward

**Updated**: 2026-08-17 13:xx PDT (Fire 2 — Weekly Docs Audit #1643 worked comprehensively)
**Session log**: `dev/2026/08/17/2026-08-17-0711-docs-code-log.md` (open).
**Cron**: `2967db0e`, fresh window to ~08-21.

**Updated**: 2026-08-16 22:3x PDT (DAY-CLOSED — 2 publishes, 1 confabulation-report caught, clean sign-off)
**Session log**: `dev/2026/08/16/2026-08-16-0711-docs-code-log.md` (closed).
**Cron**: `2967db0e`, fresh window to ~08-21.

**Updated**: 2026-08-16 16:1x PDT (Fire 4 — 2 publishes done, 1 confabulation-report caught)
**Session log**: `dev/2026/08/16/2026-08-16-0711-docs-code-log.md` (open).
**Cron**: `2967db0e`, fresh window to ~08-21.

**Updated**: 2026-08-15 22:4x PDT (DAY-CLOSED — quiet day + 1 publish + a real STOP-fire drain)
**Session log**: `dev/2026/08/15/2026-08-15-0711-docs-code-log.md` (closed).
**Cron**: `2967db0e`, fresh window to ~08-21.

**Updated**: 2026-08-14 22:3x PDT (DAY-CLOSED — 6 fires, clean sign-off)
**Session log**: `dev/2026/08/14/2026-08-14-0727-docs-code-log.md` (closed). 08-13 closed
retroactively same day.
**Cron**: `2967db0e`, fresh window to ~08-21 (rotated 08-14 day-open, 4 days ahead of prior expiry).

**Session log**: `dev/2026/08/13/2026-08-13-0727-docs-code-log.md` (open). 08-12 closed.
**Cron**: `2967db0e` (rotated 08-14 day-open, fresh 7-day window to ~08-21).

## ✅ RESOLVED 2026-08-14 (PM-engaged 18:11 + Fire 5) — session recovery, 3 PM decisions, Ship #056 report

PM reconnected post-outage; security@ applied, stale docker branch deleted, #1584/#1585 status
checked live (both open with genuine residuals, correctly not chased). Ship #056 workstream
report sent for the Aug 7-13 window — flagged a real cross-cohort delivery gap (no original
kickoff reached ANY of the 10 addressed mailboxes, only tonight's correction) rather than
silently absorbing it. **Awaiting PM**: only the feature-guide click-through remains open.

**Agent 360 v0.4**: ✅ answered same-day (08-14, `8fa0180cf`) — HOST synthesis ~4wks out; four
of my suggestions flagged agent-addressable (mail-send doc line, stderr rule, omnibus-recipe
skill note, drop-rot-prone-metadata standard) — pick up if HOST/CIO route them back.

## 🔵 ACTIVE — staleness pass on the curated keep-list (batched over fires)

**Done**: batch 1 ALPHA_* (feature-guide bannered + PA refresh-offer mailed; phantom screenshots
found-and-commented; rest clean) · batch 2 guides/+getting-started (2 fixes, 3 false positives
checked, legacy-* archives → site-excluded, flag-not-silent).
**🔵 Feature guide**: PA's verification went CODE-LEVEL (no browser on their seat — premise
caught and corrected honestly). 4 findings folded into the draft layer-labeled (`03540e35b`);
GitHub OAuth question RESOLVED. PA continuing code-level on the rest; **4 items need a browser —
queued as a ~5-min PM click-through**. Ship/hold call if PM's pass doesn't come: PM's, but a
code-level-grounded refresh already beats the v0.8.6 doc. Live guide stays bannered.
**Awaiting PM** (surface at next engagement, don't chase): the 4-item click-through · security@
vs support@ for audit-logging.md · stale docker branch deletion. (#1610 RESOLVED by Exec;
#1611 with Lead; #1616 = memo filenames break Windows clones — my filenames now shorter.) Also awaiting: Lead's attestation on #1611 (8081 two-process — live path or
fossil; evidence posted); PM's address for #1610 (legal placeholder ×3 files, next rollup).
**✅ STALENESS PASS COMPLETE (08-14 fire 2)** — all 6 batches done, final batch 0-defect;
testing/ passed CIO's condition with evidence; proposal doc carries the completion record. (installation/setup/troubleshooting had Comms's tier-6 + my earlier fixes; features/
integrations/configuration done in fire-4 sweep; api/api-reference/dev-tips done 08-14 fire 1,
cleanest batch yet: 1 defect.)
**Publish**: "Alpha Launches" LIVE 08-13 + Medium cross-post recorded (status=distributed;
building theme = Medium-only, no LinkedIn leg — complete). **website#31**: ✅ EXECUTED + CLOSED same day (regex fixed w/ control tests, 15 entries
fixed — 2 by surgery after catching draft↔live divergence on #043/#047; independently
re-verified; template convention updated; evidence to Exec). Watch item: draft↔live divergence
class at 2 instances — third instance ⇒ propose a write-back mechanism.
**PM click-through**: PM taking it (confirmed in chat) — fold results into draft on arrival.
**Comms**: register pass DONE (their confirmation 08-14); steps 9-10 restored by Docs; scrub fully closed. (was: tiers 1-6 done, continuing api/+api-reference; their installation steps-9-10 gap needs
whoever next does a live install. **Omnibus 08-13**: ✅ DONE (149 lines, `a963a8a18`+`9411abf45`, chain continuous). **Omnibus 08-12**: ✅ DONE (137 lines, HC:COORDINATION, `8373746de`+`3786e5dd8`, spot-verified). Omnibus chain now continuous through 08-12.
**Comms register pass**: started (their `9f6ab1732` touched 2 ALPHA docs) — parallel, different
dimensions, agreed.

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

## ✅ RESOLVED 2026-08-17 — Weekly Docs Audit #1643 CLOSED + 3-day omnibus backfill COMPLETE

Comprehensive audit (7 sub-checks tracked to completion), 7 real fixes committed+pushed, #1644
filed for residuals, closing comment + close landed after a GitHub API outage window recovered.
**Omnibus chain independently verified continuous 07-27 through 08-16, zero gaps** (21 files,
47 activity-log rows added across the 3 backfilled days, no CSV race — sequential dispatch held).
**Real findings needing others, unresolved**: BRIEFING-CURRENT-STATE 22-day engineering staleness
(Lead Dev); last_verified cluster from 07-30 still 87% unrefreshed 3 weeks later (cohort-wide, no
single owner — worth a memory pin or a direct ask if it's still stale at next Monday's audit);
universal-list-architecture-guide.md duplicate (Lead Dev); roadmap.md date discrepancy (PPM, in
#1644).

## ✅ RESOLVED 2026-08-16 — 2 posts published, syndicated; a confidently-wrong report caught before acting

**"Confabulating a Peer's Unfinished Work"** (Aug 15) fully closed: Medium+LinkedIn synced,
status=distributed.
**"The Fabricating Standup"** (Aug 16) published clean (0 audit fixes needed), live-verified,
Medium+LinkedIn synced same day, status=distributed.

**Real find**: a same-day report claimed CLAUDE.md's checkout HARD RULE path was wrong and
`sync-pm-local.sh` couldn't find PM's checkout at all (citing a space-form path that doesn't
exist). Verified independently — `git worktree list`, filesystem check, live dry-run — the
report's central claim was FALSE; the existing hyphenated path is correct and working. One
genuinely real claim in the same report (CLAUDE.md described the script's old v1 binary-abort
behavior instead of its actual v2 3-tier classifier) was fixed (`584695a14`). Full verification
sent to PM directly — a confidently-wrong report about system state, same shape as the post
published that morning.

## ✅ RESOLVED 2026-08-12 (Fire 3, 13:27) — mail drain: Ship #055 closed, #1584 Part C done, Pages build revived

Comms closed the Ship #055 thread (independent live-verify, clean). CIO completed #1584 Part C +
retired cohort-agent-status.md — spot-verified in-tree, completion comment posted to #1584. Janus
root-caused and fixed the docs Pages build (dead since ~May 31 — literal `{% extends %}` in
BRIEFING-CURRENT-STATE.md's own bug documentation; Liquid parses tags inside code spans); Docs
verified 3 consecutive green runs at tip, replied to Janus, and fed the silent-red family
(#1600 + Pages build + #1593) to Lead's parked postmortem question with the two-detector-shapes
factoring.

## 🔵 ACTIVE (PM-approved 2026-08-12) — pmorgan.tech scrub, 3 phases

The parked scoping question got PM's green light same day ("good plan. please get it started").
Proposal committed (`docs/internal/operations/docs-site-scoping-proposal-2026-08-12.md`), README
scrubbed (`a8431b4d6`), CIO ratification requested (memo `8fbf8e761`, cc Comms).

**✅ SCOPE RATIFIED + APPLIED (Fire 5, 08-12 evening)**: CIO ratified (user-guide.md → EXCLUDE,
testing/ keep-with-file-discretion, dev-tips/ keep). `_config.yml` applied: 13 corpus surfaces +
user-guide.md + NAVIGATION.md (post-ratification, self-declared internal-audience, flagged not
silent) excluded; site title added. NAVIGATION count-rot stripped (11 stale counts). CONTRIBUTING
two-surfaces guard-rail added. Comms handoff sent (register-pass surface final; dev-tips/ first).
methodology-49 "Described Is Not Running" filed by CIO from my routed candidate, verified.
**✅ VERIFIED COMPLETE (20:2x)**: build green, all spot-URLs correct (kept 200 / excluded 404 /
title "Piper Morgan Documentation"). Verification found + fixed 2 real defects same evening: the
`reference`→`references/` exclude prefix collision (trailing slash now load-bearing, commented)
and CONTRIBUTING's pre-existing never-rendered gap (special-filename plugin behavior, frontmatter
added). The curation is live end to end.
**Remaining scrub queue**: per-surface staleness+link pass on the final keep-list (~160 pages,
batched over fires; CIO's testing/ file-level-discretion condition applies during this pass);
Comms register pass (their cadence); #1608 is Lead/CIO's lane. (#1593 FIXED by Lead 08-12,
ratchet verified live.)

## ✅ RESOLVED 2026-08-12 (PM-engaged, 11:06–) — Ship #055 published + 5-day omnibus backlog cleared

**Ship #055** live at /shipping-news/weekly-ship-055-shipped-is-a-layer-word (website `536d5a1`,
product `6283b4d00`). Template audit: 1 fix (PA/Comms gloss). Dry-run caught a real publish-post.js
rendering defect (bold-open + italic-close paragraph → literal stray asterisks; same root regex as
website#31, sharper manifestation) — fixed at source, full diagnosis posted to website#31.
Live-content-verified. Comms memo sent (`d24eea418`). **Syndication (Medium/LinkedIn) remains PM's
manual step** — status will need `published`→`distributed` + URLs when PM cross-posts.

**Omnibus backlog 08-07→08-11 cleared** — one day per subagent sequentially per PM's "manageable
bits" direction, full skill+methodology compliance each day, all pushed (10 commits, see session
log table). Activity log +95 rows. Two preserved-not-resolved items from the 08-11 synthesis worth
eventual attention: (1) Exec's post-reboot cron re-arm was unconfirmed as of the 08-11 record
(Pard's memo named Exec the last unaccounted seat; Exec has 08-12 commits so likely fine now);
(2) a Web/HOST/PA vs. Arch discrepancy about whether the pre-reboot cron "survived" (Arch's
`uptime` check says the host hadn't rebooted yet) — preserved in the omnibus per
name-the-divergence.

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

**✅ RESOLVED**: mail-triage subagent read all 163 cc-only backlog memos in full — zero needed
direct Docs action. Bulk-filed to `read/` in 19 batches; inbox at 0 unread. Along the way, fixed 2
genuinely-open (not fabricated-closed) session logs the triage surfaced: 07-23 and 07-25 both now
carry honest retroactive `DAY-CLOSED` markers (`756de0498`).

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
