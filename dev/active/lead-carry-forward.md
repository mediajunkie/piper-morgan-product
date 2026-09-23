# Lead carry-forward — rewritten 2026-09-23 ~10:1x PT (STOP-backfill + Exec's context-floor spring-clean; resolved threads deleted, history lives in the session logs)

## LIVE THREADS

- **Alpha is Fly-served (cutover 09-22, complete).** Droplet stopped-warm = rollback until
  **step 11 decommission ~09-29 (MINE)**: decommission + retire `production` branch + deep docs
  sweep + tell Themis (via Pard) the date. Runbook:
  `docs/internal/operations/alpha-fly-cutover-runbook-2026-09-22.md`.
- **Test card** (`dev/active/pm-test-card.md`, artifact ALxfaRpLn5wjBVUPjzLvbi): Row 1 (#1617)
  **PASSED 09-23** → #1739 discharged → **epic 3 UNBLOCKED (next build lane)**. Remaining: #1824
  invalid-key retest (~60s, PM) · Web's browser spot-checks + render sweep (tasked 09-22, no
  report yet — includes #1859 white-flash trace).
- **PM's 09-23 test session findings — filed #1855–#1860** (unarmed floor offers · add-project
  flow arg-drop+loop · name-extraction greed · 404-close honesty bucket · white flash ·
  standup-initiation coverage) + evidence on #1843 (exact-match accept) and #1828 (Monday-on-
  Wednesday). #1855 pairs with epic 3's floor contract; #1858 is a small honest-bucket fix
  (mine, unblocked); #1856 likely mine after flow-contract check.
- **#1574 build (Audit Cluster 1 head)**: DESIGN DONE
  (`docs/internal/design/design-1574-preference-persistence-2026-09-22.md`) — build in a fresh
  focused session; then the tz family (#1556/1575/1576/1577/1588). Cluster 2 (#1499/#1522/#1533)
  behind it; #1522 false-trails gains #1855 as evidence.
- **Deploy path (§4e)**: PM ruled (via Pard, 09-22 13:38, superseding the crossed in-conversation
  answer): **mine to solve when v0.8.14 needs it**, Arch+Pard escalation. Design adopted in
  pipeline plan v0.3 §4e (CI + Fly deploy token + PIPER_GIT_SHA; closes #1849). Pard holds the
  two token facts, answerable on my ask. Until built: alpha deploys by PM's hands.
- **STOP-miss mechanism proposal with CIO** (PM directive 09-23): one-shot STOP backstop when
  Rule-1 deletes the cron — memo sent, see decisions/skill lane.

## Waits (verify against the ISSUE, not this file)
- **Arch**: #1774 Rule-0 ruling (census delivered 09-22; spatial cross-check w/ PPM) · #1841+
  #1854+#1860 corpus lane · #1832 GO · #1800 scope · #1843 acceptance ruling (w/ CXO; now
  two-directional evidence).
- **PM**: #1824 retest · #1845 rule ratification (→ my token-shape lint) · #1599 username check.
- **CXO**: #1772 fix design · #1859 design question (is chat-switch a full navigation on
  purpose?).
- **Web**: retests + render sweep report (incl. #1859 trace).

## Queue (unblocked, in order)
1. **#1858** (404-close honest bucket — small, mine).
2. **Epic 3 floor** (unblocked by #1739) — check epic contents at pickup; #1855's design pairs.
3. **#1574 build** (fresh-session trigger; design ready).
4. #1856 (add-project flow) after checking flow-contract ownership · audit clusters ·
   v0.8.14 cut (needs §4e deploy path or a PM keystroke).

## Cron / registry
Cron: re-armed at 09-23 START-backfill (id in registry row; expires +7d, rotate −2d).
Registry row: current (215 chars — trim checked-not-needed 09-23). **Rule-1 practice until the
skill amendment lands: when deleting the recurring cron for a drain, CREATE THE ONE-SHOT STOP
BACKSTOP in the same breath** (the 09-22 missed-STOP cause: delete-for-drain + idle-re-arm
vigilance failed).

## Standing (unchanged)
Model pinning + logged tier on every dispatch · pre-register closures · paired fixes together ·
stage-then-commit-bare · explicit paths · verify pushes on origin/main · m-43 layer + m-44
denominator · "Verified how:" on completion claims · masked bearer forms only · sync-pm-local at
idle · this file: freshness pass at START, rewrite at STOP.
