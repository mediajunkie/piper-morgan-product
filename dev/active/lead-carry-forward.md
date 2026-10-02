# Lead carry-forward — rewritten 2026-09-26 21:5x PT at STOP; queue refreshed 2026-10-01 21:2x PT at STOP (tape run day 2 closed; quota reset 21:59) (resolved threads deleted, history lives in the session logs)

## LIVE THREADS

- **EPIC 0 (#1595) is the CURRENT EPIC by PM's rule.** LIVE on alpha v146: five read waves + create_todo +
  create_reminder in the flag; `delete_todo` allowlisted (token = PM's hand); **unit 4 sequential rail
  dispatch** (per-sibling consult, Arch's three rules); #1896 stand-down for turns it declines. Scope +
  progress: `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`. **09-27**: `set_default_repo` allowlisted (four writes; #1898 handler read fixed) · **Phase 3 instrument LIVE**
  (`scripts/inversion_phase3_deletion_gate.py`; procedure in the scope doc) · **FIRST DELETION LANDED + DEPLOYED (v147)**:
  REMINDER + REMINDER_QUERY gone, ceiling 567→558, ledger live. It surfaced **#1899 (CLOSED same day)**: armed-carrier
  discriminators now carry the reads-only release (`inversion_live.read_op_claims_turn`, CXO-ruled, both sites) — a
  WRITE-destination list deletion is still an erosion risk for them (doc'd). "what should I do next" RULED
  `get_top_priority` (CXO/PPM), re-scored 1/1 → **TODO_QUERY DELETED 09-28 (v148), ceiling 548**; PRIORITY reabsorbed 'what next' (ledgered, agrees).
  **GUIDANCE scored 8/20 → NO-GO, stays** (12 destination rows to PPM/CXO; not in any live group → Arch). Corpus 151. Remaining: 4b (Arch's additive plan outcome, PM budget for the before/after) · Phase 3 per-list cycle. Wave-2 scoring budget: approved AND already spent 09-25 —
  don't double-spend.
- **MCP = PA's program.** Units 0–4 built + LIVE (alpha v146 + MCP v6/v7): fail-closed identity, three
  resources, **OAuth AS in alpha at `/mcp/oauth/*`** (Arch-approved at source). PM = tester #1, ChatGPT
  first — first contact is PA's step; Lead only if PA asks (PA asked once: apply the warm-pin deploy →
  done at STOP). Runbook `docs/internal/architecture/current/mcp/server-README.md`.
- **#1772 guard LIVE (v145, PM 'go' 09-26)**: post-compose scope guard, zero-by-construction. Closure = ~10 live
  completions under the guard counting `scope_guard_dropped` (PM budget). CXO copy pass owed on the fallback line.
- **Alpha = Fly v164 (10-02 07:4x `c49c5c82b2` — #1606 floor-element plans + verbatim element text; GITHUB_QUERY_PATTERNS deleted, ceiling 376; flag 8 tokens incl. delete_todo); MCP v7** — everything on main deployed. Deploy = detached throwaway
  worktree at origin/main, `fly deploy --remote-only --build-arg PIPER_GIT_SHA=…`, verify `/health` git_sha
  AND re-read the flag after any restart. Never PM's checkout.
- **Test card v14 (remaining-only, PM's ask 10-01)** (`dev/active/pm-test-card.md`, artifact ALxfaRpLn5wjBVUPjzLvbi): re-tests A–D on v161 (#1858, #1912, #1914, get-issue/issue-count), **row E = calendar setup (PM's hand: GOOGLE_CLIENT_ID/SECRET Fly secrets; 0 of 2 set at 14:1x)**, waiting rows F (#1913) G (#1606) H (Slack).
- **#1885**: DONE except reissues — PM burned the three tokens 09-26 19:16 with `--burn-unused`; keys handled.
  Reissues next week (PM's ruling); HOST re-records then.
- **Droplet era OVER (09-29)**: destroyed by PM, `production` deleted, docs stamped. Themis told via Pard's update memo
  (mediajunkie/docs/mail). One lineage: origin/main → Fly; §4e CI path is Pard's.
- **mypy gate frozen (#1786)**: measure from a FULL `git archive HEAD` tree; read the mypy section of
  `run-sweep.sh ratchets`, not the tail; ratchets are EXACT-at-ceiling.
- **#1735 / #1886 / #1867 / #1891 / #1889**: Arch/CXO rulings owed (unchanged). **#1900** (prompt caching, Pard's finding) filed, behind epic 0 unless PM promotes.
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

## Queue (Fri 10-02 07:5x — budget fresh; GitHub API rate-limited until ~08:0x)
1. **File the #1899 write-half erosion issue** (body = the 10-02 finding memo to CXO/Arch) once `gh` works again;
   then act on CXO/Arch's answer (a) router releases any live-eligible op / (b) carrier exit phrase / (c) keep re-ask.
2. **Arch's GO on gate condition (d)** (destination reached by category, measured at surface 2; asked 07:3x). On GO:
   three deletion lanes — PRIORITY (47), GUIDANCE (21), STATUS (56) — same template as GITHUB (`dfec3e908d` /
   this morning's `c49c5c82b2` pair); ceiling 376 → 252. Each: ledger entry, reabsorption census, pins converted.
3. **PM's re-tests** on v164 (card rows A–D + G); row E waits on the two Fly secrets; **#1913** waits on PM's two answers.
4. Next write-bearing lists (REPO_MANAGEMENT 12, SET_DEFAULT_REPO 4) only after the #1899 ruling — deleting them
   widens the carrier erosion.
5. Pre-existing, not mine: todo-marker ratchet 36 vs 35 in `run-sweep.sh ratchets` (services/+web/ scan) — whoever
   added the 36th owns it; flag to CIO if it's still red at STOP.
6. Cron `5f15d993` expires ~10-05 (rotate by Sat 10-03 START). Heartbeat line at the END of every fire (missed 4 on 10-01).

## Cron / registry
**Recurring cron `5f15d993` armed 2026-09-28 06:5x** (`17 6,9,12,15,18,21 * * *` — 6/day restored per PM
'Monday ok'; expires ~10-05). Previous `8d0210ef` (3/day throttle) deleted same breath. 09-26 fires: 06:17 START on time; 12:17 did NOT surface while PM
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
