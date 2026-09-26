# Lead carry-forward — rewritten 2026-09-24 18:4x PT, refreshed 20:1x and at STOP 20:5x (resolved threads deleted, history lives in the session logs)

## LIVE THREADS

- **#1885 (PM-rated LOW blast radius 09-24 21:00: obscure, worst case an extra tester, alpha never
  exposes PM's key — queued, not urgent) — three LIVE unused invite tokens were in FULL form in tracked session logs + the
  07-09 omnibus (public repo)**: `QGQP…KJGP` (Savanna), `DNE5…JXZE` (spare), `NCBN…65FH`
  (Janne's 09-21 replacement). Scrubbed to masked on main (`6e75d3ddad` + mail `63ef9b73f8`);
  `scripts/mailbox_bearer_lint.py` now gates Code Quality over mailboxes/docs/dev (baseline
  `.mailbox-bearer-lint-baseline.txt`, path:sha1, never a credential). **The BURN is PM's hand**
  (my prod `DELETE` was classifier-denied; one-liner on the issue) → then mint 2 replacements
  (`scripts/mint_prod_invite.sh --apply 2`), masked to PM in chat, HOST re-records Savanna +
  Janne. Also on the issue: a Google key in `dev/2025/10/16/server-startup.log` (rotate if live).
  Memo to HOST/Exec/PM sent 18:4x. History still holds the bytes — burn is the fix.
- **Alpha = Fly v139 (`43e12de2d2`, 09-25 16:5x)** — everything on main deployed; inversion flag = 3 read waves + create_todo + **create_reminder + read_strategic (PM flipped 09-25 16:4x)**; **read_temporal LIVE (PM flipped 17:3x)** — all five read waves live: v0.8.14.0 + every
  fix of 09-24 — wizard #1875, caching #1859, burst #1874, timezone #1876 + one-resolver #1887,
  keyless chat kept #1838, composer #1737, historical header #1498, chat-switch flash #1607,
  routing #1795/#1881/#1763/#1884, #1735 auto-apply, #1850 guard, PIPER.md in the prompt #1678,
  files page #1697, aged docs #1661, tombstone #1784, temporal faces #1565, Radar honesty #1587,
  calendar log noise #1592, Places scoping #1888, one shared escape.js (eight injection holes closed) #1582.
  Deploy = detached throwaway worktree at origin/main (`/tmp/lead-deploy-wt`), `fly deploy
  --remote-only --build-arg PIPER_GIT_SHA=…`, verify `/health` git_sha. Never PM's checkout.
- **Test card** (`dev/active/pm-test-card.md`, artifact ALxfaRpLn5wjBVUPjzLvbi **v10**): nine
  rows live; row 4 carries the due-date step (#1887).
- **Droplet stopped-warm = rollback until step 11 decommission ~09-29 (MINE)**: decommission +
  retire `production` (never advanced at the cut) + deep docs sweep + tell Themis (via Pard,
  inbox `~/Development/mediajunkie/docs/mail/`; `mailboxes/pard/` gravestoned). Runbook
  `docs/internal/operations/alpha-fly-cutover-runbook-2026-09-22.md`.
- **Staging `piper-morgan-staging` at v2** (a1599admin guard fixed); expected `alembic current`
  = `l1466slack` (unverified).
- **mypy gate environment frozen (#1786)**: `scripts/mypy-gate-constraints.txt` from a real CI
  freeze; both CI and `bootstrap-mypy-gate-venv.sh` install under `-c`. **Measure ceilings from a
  FULL `git archive HEAD` tree or a detached worktree** — a partial archive omits the root
  `alembic/` dir and reads one attr_defined low (the 69/70 hunt). CI prints `--raw` every run.
  Ratchets are EXACT-at-ceiling: read the mypy section of `run-sweep.sh ratchets`, not the tail.
- **#1735 decision pending (Arch/PM)**: `personality_*` now has two durable writers and zero
  readers; memo `dev/2026/09/24/1735-learning-loop-census-and-decision-2026-09-24.md` recommends
  A (overlay in `_create_from_preferences`) conditional on CXO's visibility call.
- **#1886 (Arch)**: `_handle_add_project` still starts a session on the DARK onboarding process
  (a bare-name reply orphans it) + the dead `offer_onboarding` chain; strict-xfail pinned in the
  enforcement suite so the fix flips it loud. #1867 stays open for the ruling.
- **#1852**: three Fly secrets still read `piper-morgan.fly.dev`; PM registers the four console
  callback URLs → I `fly secrets set` + verify connect flows.

## Waits (verify against the ISSUE, not this file)
- **PM**: #1885 burn when convenient (Google key: PM confirms in the morning it was the one already
  rotated) · #1852 consoles (PM asked to SAVE console work for desk time — don't nudge) · Web's LLM
  key · step-11 gate (hold ~09-29 vs after retests) · test card rows (PM: "testing tomorrow").
  DONE 09-24 21:0x: #1722 closed (89/89 removed), #1845 closed (ratified), #1772 budget approved →
  lane ran 20 completions (result on the issue / in the session log).
- **Arch**: #1886/#1867 ruling · #1843/#1771/#1783 acceptance-contract rulings (w/ CXO) ·
  #1832 GO · #1841+#1854+#1860 corpus lane · #1499 ui.py exception class + `/api/admin/*`
  window · #1735 store decision (w/ PM) · #1784 tombstone option · #1884 subsumption widening.
- **PM**: #1772 measurement of CXO's landed string (~20 completions) — the number closes the issue.
- **CXO**: #1772 copy LANDED 09-25 (their N-agnostic string, verbatim) · #1735 visibility call (the #1799 EMBEDDED ruling arrived 19:3x and is live on v132).
- **HOST**: #1885 roster re-record after the burn; #1845 second review of the lint (mailed 21:09).
- **Docs**: #1883 (eight docs describe the deleted standup-bridge family) · #1719 candidate 2
  (pre-move check in the archival script; candidate 1 — the widened link gate — is live, ceiling 90).
- **CXO**: copy passes marked in code — #1661 naming reply, #1565 all-day/timed faces, #1587
  degraded-source sentence; #1889 (formatters + Radar card) is a UX call.
- **Arch**: #1619 category question · #1680 carrier question (`TranscriptEntry` doesn't exist) ·
  #1891 manifest/outward design (rec. B) · #1890 wire-or-dispose PDR-002 greeting partial (w/ PPM/CXO).
- **Pard**: §4e CI deploy path (closes #1849).

## Queue (unblocked, in order)
1. On PM's "burn them": burn, mint 2, deliver masked, close #1885 with evidence.
2. (done 19:3x — #1799 closed 4/4 on CXO's ruling.)
3. #1889 wire-through once CXO rules the per-format copy · #1629 checkbox 2 rides #1257.
4. (done 09-25 — #1731 closed with the mechanism + stale-base guard.)
5. Step 11 on the ~09-29 clock; rotate cron ~09-28.

## Cron / registry
**Recurring cron 470fd4e1 armed 2026-09-23 21:2x** (`17 6,9,12,15,18,21 * * *`; expires
~09-30, rotate ~09-28). Fires 09-24: 06:17, 09:17, 12:17, 15:17 on time; the 18:17 tick surfaced
at 20:48 (engaged all evening) and STOP ran on it with the queue drained; the 21:17 fire finds
DAY-CLOSED. Next START 09-25 06:17. Never delete the recurring cron without the one-shot backstop in
the same breath.

## Standing (unchanged + today's additions)
Model pinning + logged tier on every dispatch · pre-register closures · paired fixes together ·
stage-then-commit with EXPLICIT PATHSPECS (`git commit -- <paths>`) after reading `git diff
--cached --name-only` — lanes stage too · when a lane and I both edit one file, build my commit
from HEAD's version and re-apply the lane's edit on top · **`$(date +%H:%M)` inline in every log
line, never a typed time** (five headers ran 10–20 min fast today) · `git grep` for sweeps (this
seat's `grep` is `ugrep --ignore-files`, which hides tracked files under broad .gitignore rules)
· `pytest …; test ${pipestatus[1]} -eq 0` — a pipe swallows the gate's exit (09-25 miss) · `ruff format --check` on every staged .py before committing lane output (three files went out unformatted 09-25, Code Quality red until fixed) · verify pushes on origin/main · m-43 layer + m-44 denominator · "Verified how:" on completion
claims · masked bearer forms only, and the lint enforces it · sync-pm-local at idle · this file:
freshness pass at START, rewrite at STOP.
