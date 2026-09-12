# Lead carry-forward — rewritten 2026-08-29 ~18:15 PT (freshness rule: full pass at START/STOP)

## Live state (receipts, refreshed 2026-09-12 07:0x — Saturday fire 1)
- **v76 LIVE** (three deploys this fire; v75 FAILED on flyctl wait-timeout mid-image-pull —
  retry with `--wait-timeout 600` fixed it; old machine kept serving throughout).
- **MVP: 44 open in the milestone, MEASURED** (= board 34 Sprint Backlog + 3 In Progress +
  7 In Review). ⚠️ My "25→24→23" was stale decrement-arithmetic, never a measurement —
  RE-MEASURE the headline every time (`gh issue list --milestone MVP --state open`); never
  decrement. Memo to PPM asks which denominator to pin; correction owned in PM's tracker.
- **EPIC 2**: 1690 + 1741 + 1733 closed + live-verified today; remainder = **1740** (dead
  renderer twin — folded into epic 2 per the order doc 9/10; my earlier "remainder EMPTY"
  note was wrong, caught on re-reading the order doc).
  New tail (unplaced, PPM's call): 1750 (standup.html stale twin) · 1751 (canonical
  personality page hardcodes user_id "default").
- **1741 CLOSED + deployed**: suggestions UI escaped per the 1578 treatment (user text out of
  onclick; deliberately NOT the DOMPurify chokepoint — inline handlers are by design).
  ⚠️ jest verifies need `--config tests/frontend/jest.config.js` — bare `npx jest` runs
  node-env and fails 9/9 while looking like a broken fix.
- **1690 CLOSED + verified in prod**: demo plugin default-OFF (opt-in `PIPER_DEMO_PLUGIN=1`);
  running instance shows "Initialized 4/4 plugin(s)" — demo absent. ⚠️ curl probes of prod
  routes are UNINFORMATIVE for mounted/unmounted: auth middleware 401s before routing
  (calibrated with a nonexistent-route control). Use startup logs or route-table pins.
- **Backlog burn-down**: test_github_place_has_name fixed (May-era #1042 sentinel bug,
  backlog entry removed per the #1452 gate; 59 entries remain).
- **Belt: SIX OF SEVEN GREEN** — E2E waits ONLY on PM's Anthropic repo-secret rotation
  (escalated via Exec, ~3 min). 1687 close-out awaits the full 7-green snapshot.
- **1617**: replay PASSED 3/3 (v72, still valid on v73) — PM's 90-second natural standup closes it.
- **The keyless illusion**: conftest reloads the real key from Keychain at session start —
  env-strip was NEVER keyless (1748 tracks the fix).
- Cron 28c6042f (expires ~9/16, **rotate ~9/14 — tomorrow-ish**).

## Queue (PM pre-authorized; one lane at a time in this worktree)
- INTAKE NEXT FIRE: next never-started MVP item per PPM's epic order
  (`dev/active/mvp-epic-order-2026-09-09.md`); epic-2 remainder = 1733 (stale unauth
  personality page) only — 1741 closed this fire.
- THEN: Web's test credential (real signup path — unblocks 1512/1568/1578/1581 browser
  closes) · 1677/1488 close-out on PM's transcript · #1689 native dialogs · #1659/#1660
  file residues · #1653/#1652 consent keeps · pre-claim shadow probe (measurement for the
  narrowing schedule) · #1522 fresh-scan-then-delegate · config-validator stub disposal ·
  unassigned follow-ons: 1747/1748/1749/1740/1743/1735.

## PM-attention items (both ~5 min, standing)
- (a) 90-second natural standup exchange → closes #1617.
- (b) ~3-minute Anthropic repo-secret rotation → unblocks E2E workflow (escalated via Exec).

## Recently resolved (for context, not action)
- 1711 (bounded keychain guard) · Tests workflow green first time since Aug 8 · triage cut
  fully executed · #1638 disposed · acceptance contract #1739 fully adopted, 1631/1650/1694
  closed · #1732 render boundary sanitized.

## Standing
- Supersession gate; push-after-reading (batteries ≠ push chain); merge-BEFORE-inbox-ls at every
  fire; verify awaited items against the ISSUE not this file; deletion = fresh sweep, never recall.
- **This file gets a freshness pass at every START and a rewrite at every STOP** (Exec/PM ask,
  8/29 — the 8/19 staleness is the incident that earned the rule).
- **Tracker artifact rule (adopted 09-12 after two same-day misses)**: an Artifact republish
  and the git commit of the tracker file are ONE unit — same Bash block, never separated.
- **PPM rulings 09-12**: tracker headline = milestone-wide + status breakdown (sprint-truth.py
  convention). #1750 parked (cleanup-class); **#1751 is MORE than cosmetic per PPM — real
  multi-tenancy bug on the CANONICAL personality page, #1419/#1734-adjacent, PUT admin-gate
  limits blast radius; take it when epic-2-class work resumes, not as cleanup.**
- **NEXT-FIRE REPLAY OWED**: live "show me issue #112" vs test-piper-morgan on v87+ — closes
  #1736 (code done, deployed; unit evidence covers the PAT path that produced PM's turn).
- **Log-entry mechanics (self-rule, 3rd timestamp guess today)**: entry headers use
  `$(date +%H:%M)` command substitution inside the heredoc — never a typed time.
