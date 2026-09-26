# Lead carry-forward — rewritten 2026-09-25 21:5x PT at STOP (resolved threads deleted, history lives in the session logs)

## LIVE THREADS

- **EPIC 0 (#1595) is the CURRENT EPIC by PM's restated rule (no exemptions; finished or blocked).**
  State: all five read waves + create_todo + create_reminder LIVE on Fly (PM flipped 09-25 16:4x + 17:3x);
  `delete_todo` allowlisted, token NOT in the flag (PM's hand). 93/93 READ keys wave-addressable. Corpus 116
  (Exhibit-A complete). Shadow score + scorer's shared-subset gate in
  `docs/internal/architecture/current/inversion-phase1-shadow-score-2026-09-25*.md`. Scope + progress:
  `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`.
  **Unit 4 = shape (ii)** (Arch 19:5x): multi-intent turns run siblings sequentially through the existing
  `_process_intent_internal` rail, no second dispatch site. Open design surface Arch wants asked, not
  inferred: sibling sequencing across a #1190 confirm pause. #1896 stand-down stays until unit 4 exists.
  Remaining after 4: `set_default_repo` write allowlist (#1606's other half), Phase 3 deletion ratchet.
- **MCP Phase C (sprint goal #2)**: plan `docs/internal/architecture/current/mcp/phase-c-build-plan-2026-09-25.md`.
  Answered: Q1 — bearer via `mcp-remote` for a Desktop/Code tester, OAuth AS off the path; **PM's
  tester+client pick decides** (claude.ai/ChatGPT → Arch re-scopes with the OAuth AS). Q2 — colleague-model
  = #1510 verified-inference store + PIPER.md priorities (NOT #1735). Units 0–1 start 09-26 06:17.
  **mcp.pipermorgan.ai LIT 09-26 06:5x (v1, unit 0): fail-closed 401 on every MCP path; `/health` up.** Deploy = `fly deploy -c fly.mcp.toml -a piper-morgan-mcp --remote-only --build-arg PIPER_GIT_SHA=…` from a detached worktree.
- **#1772**: shipped string 1/10 anthropic, 0/10 gpt-4o. **CXO ruled: build the post-compose scope guard**
  (fail-safe, Arch's over-trigger pass). Sequencing vs the epic-0 rule flagged to PM; CXO holds the
  ruling open. Build when unit 4 blocks on Arch, unless PM says now.
- **Alpha = Fly v141 (`70f7dd5159`, 09-25 19:2x)** — everything on main deployed. Deploy = detached throwaway
  worktree at origin/main, `fly deploy --remote-only --build-arg PIPER_GIT_SHA=…`, verify `/health` git_sha
  AND re-read the flag after any restart. Never PM's checkout.
- **Test card v12** (`dev/active/pm-test-card.md`, artifact ALxfaRpLn5wjBVUPjzLvbi): ten rows; **row 10 =
  #1559 verbatim through the inversion** (closes #1559 on a pass). PM: "testing tomorrow".
- **#1885**: rule ratified, lint at CI + mail-send doorway, console checks done by PM (Google key deleted,
  Slack rotated). **Burn = PM's `!`** (classifier denied this seat twice — never retry). Reissues next week.
- **Droplet stopped-warm = rollback until step 11 (~09-29, MINE)**: decommission + retire `production` +
  docs sweep + tell Themis via Pard (`~/Development/mediajunkie/docs/mail/`). Runbook
  `docs/internal/operations/alpha-fly-cutover-runbook-2026-09-22.md`.
- **mypy gate frozen (#1786)**: measure from a FULL `git archive HEAD` tree; read the mypy section of
  `run-sweep.sh ratchets`, not the tail; ratchets are EXACT-at-ceiling.
- **#1735 / #1886 / #1867 / #1891 / #1889 / #1890**: Arch/CXO rulings owed (unchanged).
- **#1852**: PM asked to SAVE console work for desk time — don't nudge.

## Waits (verify against the ISSUE, not this file)
- **PM**: #1885 burn (`!`) · `delete_todo` flag token · test card rows (row 10 first) · MCP tester+client
  pick (decides unit 4 of Phase C) · #1772 sequencing vs epic-0 rule · step-11 gate · Web's LLM key.
- **Arch**: unit 4 confirm-pause sequencing (when asked) · #1886/#1867 · #1843/#1771/#1783 · #1832 GO ·
  #1841+#1854+#1860 corpus lane · #1499 · #1735 store · #1619 · #1680 · #1891.
- **CXO**: copy passes marked in code (#1661, #1565, #1587, #1880 tail) · #1889 · #1735 visibility.
- **PPM**: re-judge the 6 corpus rows asserting `manage_portfolio` where the router picks the specific list
  op (the shadow report names them) · re-milestone #1892/#1849/#1423/#1890 per their triage (PM decides).
- **HOST**: roster re-record after the burn (next week).
- **Exec**: clear their assume-unchanged flags now that item 12 landed (`52e28b6945`).
- **Docs**: #1883 · #1719 candidate 2.
- **Pard**: §4e CI deploy path (#1849).

## Queue (unblocked, in order — tomorrow)
1. Epic 0 unit 4 shape (ii): write Arch the confirm-pause question, then build behind the flag.
2. MCP Phase C units 0–1 (skeleton + bearer identity) — lanes in parallel with 1.
3. #1772 guard when 1 blocks (or on PM's word).
4. `set_default_repo` onto the allowlist (same procedure) · step 11 ~09-29 · rotate cron ~09-28.

## Cron / registry
**Recurring cron `8d0210ef` armed 2026-09-26 06:4x** (`17 6,12,21 * * *` — THROTTLED 3/day per PM's
09-26 usage directive; expires ~10-03). Replaced `470fd4e1`. **Restore `17 6,9,12,15,18,21 * * *` after
Mon 09-28** (create-then-delete). STOP still at 21:17. Never delete the recurring cron without the
one-shot backstop in the same breath.

## Standing (unchanged + today's additions)
Model pinning + logged tier on every dispatch (Opus stated when used) · lanes never commit; I commit by
EXPLICIT PATHSPEC after `git diff --cached --name-only` · when a lane and I both edit one file, rebuild
from HEAD and re-apply · `$(date +%H:%M)` inline in every log line AND every memo/doc header (three
misses 09-25) · `pytest …; test ${pipestatus[1]} -eq 0` · `ruff format --check` on staged .py before
committing lane output · `git grep` for sweeps · a CI claim names a run id · verify pushes on origin/main
· m-43 layer + m-44 denominator (our own scorer had the defect) · a ruling's premise must be checked
non-vacuously ("the gate holds" ≠ "something gets through") · masked bearer forms only · classifier
denials are never worked around (burn, flag flips → PM's `!`) · sync-pm-local at idle · this file:
freshness pass at START, rewrite at STOP.
