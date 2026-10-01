# Lead carry-forward — rewritten 2026-09-26 21:5x PT at STOP; queue refreshed 2026-10-01 15:5x PT at the 15:17 fire (tape run day 2; STOP entry still owed at 21:17) (resolved threads deleted, history lives in the session logs)

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
- **Alpha = Fly v161 (10-01 14:1x `cd4b87d980` — #1858/#1912/#1914 fixes, admin calendar card hidden, review_issue/list_issues descriptions; flag has 8 tokens incl. delete_todo); MCP v7** — everything on main deployed. Deploy = detached throwaway
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

## Queue (Thu 10-01 15:5x — budget 91% @15:23, line 95%; quota resets 21:59 PDT; STOP fire 21:17)
1. **FIRST UNIT TOMORROW (fresh session, after reset): #1606 — 4b floor-element extension**, Arch's ruling
   (`mailboxes/lead/read/rule-arch-to-lead-cc-cxo-ppm-4b-floor-elements-...-2026-10-01.md`): by KIND not position;
   five conditions = AC (FLOOR disposition AND READ verb, mechanical; ≥1 live rail element else stand down to one
   floor turn; floor call scoped to the element via router rationale; compose in execution order, rail text verbatim;
   three proofs incl. #1606's row live-probed end to end). `_resolve_plan_for_dispatch` + the rail loop's plan
   consumer (`intent_service.py:~15603`). Then close #1606 with the delete half + capability answer; flag PPM to strike.
2. **PM's re-tests** on v161 (card rows A–D) — anything that fails jumps the queue. #1913 (keyless chat vanish) is
   the open fix PM is waiting on (row F).
3. **Rulings owed** (bundled 10-01, PPM/CXO): STATUS 14 router disagreements (tasks→list_todos_query ×7,
   assignments→attention_query ×5, report→generate_report ×2) + "what am I working on?" STATUS-vs-PRIORITY; GITHUB
   3 ("prs needing review", "when's the milestone deadline", "what version are we on" — the last is GITHUB's only
   gate FAIL). Apply via RULED_EXPECTATIONS, one re-score per row, wire report at the FRONT of PHASE3_REPORTS.
4. **STATUS's 3 sub-threshold rows** (session_activity_query @0.7x ×2, meeting_time @0.6) — router grammar, mine;
   gate stays NO-GO on them + the ruling row.
5. **Free lanes** (next deposit lists, biggest live first): PRIORITY is scored 35/38 but has no live group (Arch);
   DISCOVERY (20), ANALYSIS (16), MEMORY (15), TRUST (16, 1 FAIL). Every deposit: UNSCORED → I score on Haiku
   (`--provider anthropic`), FLOOR-disposition expectations now MATCH on NONE/CLARIFY (scorer rule 10-01).
6. **Ruff hook** widened to all roles 10-01 (`00ae947019`) — watch for a week whether it fires for the seats;
   Docs' blocking-push option is next if reds continue. CIO told.
7. **PM's hand**: Google OAuth secrets (row E) · #1885 reissues next week · TSVs for Exec's weekly review (refresh
   tracker v38 if asked; the 48/49 vs 10/11 is UTC-vs-Pacific, explained 14:3x).
8. Cron `5f15d993` expires ~10-05 (rotate by Sat 10-03 START).

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
