# Lead carry-forward — rewritten 2026-09-26 21:5x PT at STOP; queue refreshed 2026-09-27 12:4x PT (resolved threads deleted, history lives in the session logs)

## LIVE THREADS

- **EPIC 0 (#1595) is the CURRENT EPIC by PM's rule.** LIVE on alpha v146: five read waves + create_todo +
  create_reminder in the flag; `delete_todo` allowlisted (token = PM's hand); **unit 4 sequential rail
  dispatch** (per-sibling consult, Arch's three rules); #1896 stand-down for turns it declines. Scope +
  progress: `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`. **09-27**: `set_default_repo` allowlisted (four writes; #1898 handler read fixed) · **Phase 3 instrument LIVE**
  (`scripts/inversion_phase3_deletion_gate.py`; procedure in the scope doc) · 15 conversion rows deposited AND scored
  (14/15) · **FIRST DELETION LANDED 12:3x** (`eb9f85f119`: REMINDER + REMINDER_QUERY, ceiling 567→558, ledger live)
  — **alpha deploy of it HELD for PM** because it surfaced **#1899** (armed-carrier discriminators call `pre_classify`
  directly; "list my reminders" as a reminder-task answer now binds as the task). TODO_QUERY holds on one destination
  mismatch (PPM/CXO). Remaining: 4b (Arch's additive plan outcome, PM budget for the before/after) · Phase 3 per-list cycle. Wave-2 scoring budget: approved AND already spent 09-25 —
  don't double-spend.
- **MCP = PA's program.** Units 0–4 built + LIVE (alpha v146 + MCP v6/v7): fail-closed identity, three
  resources, **OAuth AS in alpha at `/mcp/oauth/*`** (Arch-approved at source). PM = tester #1, ChatGPT
  first — first contact is PA's step; Lead only if PA asks (PA asked once: apply the warm-pin deploy →
  done at STOP). Runbook `docs/internal/architecture/current/mcp/server-README.md`.
- **#1772 guard LIVE (v145, PM 'go' 09-26)**: post-compose scope guard, zero-by-construction. Closure = ~10 live
  completions under the guard counting `scope_guard_dropped` (PM budget). CXO copy pass owed on the fallback line.
- **Alpha = Fly v146 (09-26 14:2x — + the OAuth AS at /mcp/oauth); MCP v6** — everything on main deployed. Deploy = detached throwaway
  worktree at origin/main, `fly deploy --remote-only --build-arg PIPER_GIT_SHA=…`, verify `/health` git_sha
  AND re-read the flag after any restart. Never PM's checkout.
- **Test card v12** (`dev/active/pm-test-card.md`, artifact ALxfaRpLn5wjBVUPjzLvbi): ten rows; **row 10 =
  #1559 verbatim through the inversion** (closes #1559 on a pass). PM: "testing tomorrow".
- **#1885**: DONE except reissues — PM burned the three tokens 09-26 19:16 with `--burn-unused`; keys handled.
  Reissues next week (PM's ruling); HOST re-records then.
- **Droplet stopped-warm = rollback until step 11 (~09-29, MINE)**: decommission + retire `production` +
  docs sweep + tell Themis via Pard (`~/Development/mediajunkie/docs/mail/`). Runbook
  `docs/internal/operations/alpha-fly-cutover-runbook-2026-09-22.md`.
- **mypy gate frozen (#1786)**: measure from a FULL `git archive HEAD` tree; read the mypy section of
  `run-sweep.sh ratchets`, not the tail; ratchets are EXACT-at-ceiling.
- **#1735 / #1886 / #1867 / #1891 / #1889 / #1890**: Arch/CXO rulings owed (unchanged).
- **#1852**: PM asked to SAVE console work for desk time — don't nudge.

## Waits (verify against the ISSUE, not this file)
- **PM**: `delete_todo` flag token (matters once 4b exists) · test card rows 10–11 (#1559/#1625) · #1772 live
  measurement (~10 calls) · 4b single-op accuracy measurement budget · step-11 gate ~09-29.
- **Arch**: unit 4 confirm-pause sequencing (when asked) · #1886/#1867 · #1843/#1771/#1783 · #1832 GO ·
  #1841+#1854+#1860 corpus lane · #1499 · #1735 store · #1619 · #1680 · #1891.
- **CXO**: copy passes marked in code (#1661, #1565, #1587, #1880 tail) · #1889 · #1735 visibility.
- **PPM**: re-judge the 6 corpus rows asserting `manage_portfolio` where the router picks the specific list
  op (the shadow report names them) · re-milestone #1892/#1849/#1423/#1890 per their triage (PM decides).
- **HOST**: roster re-record after the burn (next week).
- **Exec**: clear their assume-unchanged flags now that item 12 landed (`52e28b6945`).
- **Docs**: #1883 · #1719 candidate 2.
- **Pard**: §4e CI deploy path (#1849).

## Queue (Sunday 09-27 afternoon — gated)
1. **PM**: deploy the first Phase 3 deletion to alpha (v147) or hold until #1899 is ruled — asked in chat 12:3x.
2. **Arch/CXO**: #1899 reads-only-release ruling · **PPM/CXO**: "what should I do next" destination (memo sent 12:4x).
   On a `get_top_priority` ruling: flip that corpus row's expectation, re-score the one row (1 call), delete
   TODO_QUERY (8 literals, 558→550). On `list_todos_query`: the list stays.
3. **Free now**: deposits for GUIDANCE (20), PRIORITY (44), CALENDAR (49), TEMPORAL (54) — each phrase proven claimed
   by its list; scoring = PM budget (one call per row). **Before any deletion**: check the direct-consumer inventory
   (routing-stack doc §Phase 3) — is the list load-bearing for a carrier discriminator?
4. **PM budget**: #1772 live measurement (~10) · 4b single-op accuracy before/after (Arch's shape).
5. Step 11 ~09-29 · restore 6/day cron after Mon · rotate before ~10-03.

## Cron / registry
**Recurring cron `8d0210ef` armed 2026-09-26 06:4x** (`17 6,12,21 * * *` — THROTTLED 3/day per PM's
09-26 usage directive; expires ~10-03). 09-26 fires: 06:17 START on time; 12:17 did NOT surface while PM
was engaged (ran by hand at 12:46 on PM's nudge; cron arrived 12:49); 21:17 STOP arrived 21:47. **Restore
`17 6,9,12,15,18,21 * * *` after Mon 09-28** (create-then-delete). Registry: threshold 10, wake 6–22. Never delete the recurring cron without the
one-shot backstop in the same breath.

## Standing (unchanged + today's additions)
Model pinning + logged tier on every dispatch (Opus stated when used) · lanes never commit; I commit by
EXPLICIT PATHSPEC after `git diff --cached --name-only` · when a lane and I both edit one file, rebuild
from HEAD and re-apply · `$(date +%H:%M)` inline in every log line AND every memo/doc header (three
misses 09-25) · `pytest …; test ${pipestatus[1]} -eq 0` · `ruff format --check` on staged .py before
committing lane output · `git grep` for sweeps · a CI claim names a run id · verify pushes on origin/main
· m-43 layer + m-44 denominator (our own scorer had the defect) · date bucketing converts to Pacific and names the timezone (09-26) · a ruling's premise must be checked
non-vacuously ("the gate holds" ≠ "something gets through") · masked bearer forms only · classifier
denials are never worked around (burn, flag flips → PM's `!`) · sync-pm-local at idle · this file:
freshness pass at START, rewrite at STOP.
