# Lead carry-forward — rewritten 2026-09-14 ~12:50 PT (freshness rule: full pass at START/STOP)

## Live state
- **v105 LIVE.** Belt: 25 active workflows, **zero unexplained reds**. PM-056 job 2 went
  honestly green today (#1788 executed incl. Arch's DocumentDB re-ruling). Windows is PARKED
  dispatch-only per PM (tracked at #1457, Production milestone). scope-guard is advisory and
  says so in its own name.
- **Cron 22689706** (17 6,9,12,15,18,21; rotated 09-13, expires ~09-20, **next rotation
  ~09-18**). Model: Opus (PM moved this seat off Fable 09-13 during the classifier outage).
- MVP measured **51 open** — up from Friday and honestly so: the weekend's lanes filed ~25
  discovered issues and PPM triaged every one into an epic. Closure and discovery both count.

## Closed since Friday (selected, all verified at a named layer)
Epic 2 fully closed · epic 3 closed (PM's live standup pass closed #1617 and the #1739
umbrella) · epic 4 drained · epic 5 builds done · epic 6's first build in (cashable remainder,
late-follow-up pinned) · the Rule-0 dead-code batch (~3,000 lines, two gates now fully tight) ·
both credential rotations · #1777 sentinel sweep · #1792 revoked-token lie · #1751
multi-tenancy · #1756/#1757 (102 wrong destructive claims → 0).

## Waits (verify against the ISSUE, not this file)
- **#1799** — CXO copy call: 1 of 3 formatters discloses a source failure; the terse register
  needs GatherOutcome §6.1 case-3 wording. CXO says cases 2–4 are runnable now.
- **#1800** — Arch: should the #1436 mypy gate scope to a path-level zero? Raised because
  mypy had already flagged every #1777 site but the per-code AGGREGATE ceilings hid them.
- **#1785** — push-vs-nightly policy; the waste half is fixed, the remaining question is mine
  to close as "no" unless PM/Arch/CXO disagree.

## Queue (PM pre-authorized; one lane at a time)
- NEXT: #1802 (TestClient one-authenticated-request — honest now, still broken) · #1794
  (GITHUB_QUERY destructive claims, needs per-claim discrimination) · #1771 defer-tier ·
  #1772 (CXO's N=1 leak — MEASURE first) · #1781/#1782 (page-once counts) · #1773 · #1774 ·
  #1797 (dispose 5 dead twins, deletion discipline) · #1789/#1790 (List shadowing;
  lifecycle_history never populated) · #1796 (2 pre-existing failures NOT in the backlog —
  invisible to the burn-down gate).
- Older, still valid: Web's test credential · 1677/1488 close-out · #1689 · #1659/#1660 ·
  pre-claim shadow probe · #1522 · config-validator stub disposal · the builder-dedupe ruling.

## Standing
- **MODEL PINNING ON DISPATCH (adopted 2026-09-14, after Exec's finding).** A fan-out
  INHERITS the dispatcher's model unless `model:` is passed. My 48 dispatches in four days
  exhausted the Fable tier and arch + web had their Monday fires refused — a cost my seat
  imposed and could not see from any surface it looks at. From now on: pass `model:`
  EXPLICITLY on every dispatch; default mechanical-with-judgment lanes (sweeps, censuses,
  ruled deletions, adopting a decided idiom) to a cheaper tier; reserve the top tier for
  novel design or ambiguous rulings and say why in the fire log. ⚠️ Watch lane QUALITY, not
  cost — if a cheaper tier stops catching what this week's caught (the uncited second
  fail-closed site, the guard that was itself a misreport, the disagreement with a ruling),
  the saving is false and I want to hear it early.
- **SILENCE IS NOT A DIAGNOSIS.** Three distinct causes of identical silence in four days:
  dead process, signed-out session, refused-at-the-ceiling. The belt reports that a seat
  produced nothing; it structurally cannot say why, and the remedies differ completely.
  `CronList` non-empty means ARMED, never LIVE — only a fire is proof.
- Supersession gate · push-after-reading · merge-BEFORE-inbox-ls · deletion = fresh sweep
  never recall · RE-MEASURE never decrement · tracker republish + git commit = ONE unit ·
  log-entry headers use `$(date +%H:%M)` NEVER a typed time · no sed on this file without
  grep-verifying the EXACT phrase · stage in one call + commit BARE in the next (the compound
  form bypasses the sweep hook — CIO confirmed 09-13) · a push to origin/main does NOT make a
  hook fix live, the main checkout must sync too.
- Environment gotchas that cost real time: ENCRYPTION_MASTER_KEY is base64-32 not hex · jest
  needs `--config tests/frontend/jest.config.js` · prod curl can't distinguish
  mounted-vs-unmounted (auth 401s before routing) · `gh` can return EMPTY with exit 0 in the
  sandbox (silent-clear — verify by reading back) · the mypy gate must run under
  `venv-mypy-gate/`, never the dev venv (it over-reports ~75 errors across ~9 codes).
- This file: freshness pass at every START, rewrite at every STOP.
