# Lead carry-forward — HANDOFF for the Opus 5.5 restart (written 2026-10-03 10:1x PT by the Fable 5.1 session; PM-approved, Pard executes)

## STATE @ 2026-10-03 17:36 PT (Opus 5.5 session)
- **Cron `1e7b0a85`** (`17 6,9,12,15,18,21`, armed 13:22 10-03, expires ~10-10 → rotate by Fri 10-09 START).
- **Phase 3 today: deletions 9–18 on main, ceiling 259 → 155**, ledger 19 entries. Full tests/unit 12235/0, tests/intent 205/0.
  **gate --all: NO GO list left**, and every remaining list is rail-bound (its op isn't live). Proposal to Arch cc Exec
  (`41a8f07dc`): read_floor wave 2 (get_identity, check_completion_status, get_feature_info, write_stakeholder_update).
  **Waiting for Arch's yes before building.** Write rows (manage_repos [own memo b43bce304], manage_portfolio,
  explain_suggestion, get_contextual_guidance, complete_todo, update_document_query) wait for Arch's shapes;
  set_default_repo's flag token is PM's (via Exec).
- **1924 CLOSED** (greeting-swallow fix `3c20a952db`). **1925**: only the CI decision left (tests/intent in a workflow?).
  **1926** filed: manage_repos unlink has no destructive confirm (CXO/Arch ruling).
- **NOT DEPLOYED**: alpha still v166. `fly deploy` is blocked by the classifier [Production Deploy] and PM hasn't decided
  (allow rule / PM runs it / batch later). The read-only flag read IS allowed now.
- **Lane rules earned today:** lanes run full tests/unit with maxfail overridden + tests/intent; Lead diffs the FAILED
  set against origin/main in /tmp/lead-deploy-wt; the STOP on a disagreeing reabsorption must say whether same-batch
  self-resolution is allowed; lanes must not use `git checkout --` even on their own files.
- **Mail rule (PM 10-03, CLAUDE.md):** never write to `mailboxes/xian (ceo)/`; PM items go to Exec.

## THINGS NOT WRITTEN DOWN ANYWHERE ELSE (the category that disappears)
- **Deploy**: from the detached throwaway worktree `/tmp/lead-deploy-wt`: `git fetch origin main && git checkout
  --detach origin/main && fly deploy -a piper-morgan --remote-only --build-arg PIPER_GIT_SHA=$(git rev-parse HEAD)`;
  verify `curl -s https://alpha.pipermorgan.ai/health` git_sha and re-read the flag (`fly ssh console -a piper-morgan
  -C 'printenv PIPER_INVERSION_LIVE_CATEGORIES'`). Never from PM's checkout.
- **Live probes** (llm-marked e2e, real app + Postgres 5433): `K=$(venv/bin/python -c "from services.infrastructure.
  keychain_service import KeychainService; print(KeychainService().get_api_key('anthropic'))")`; then `env -u
  ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS PIPER_E2E_LIVE_HEADER_KEY=
  "$K" POSTGRES_PORT=5433 venv/bin/python -m pytest tests/e2e/test_1606_two_part_turn_floor_element_live.py -q -s -m llm`.
  Replies contain newlines — print with `tr`, don't grep (I lost six probe runs to that).
- **Scoring**: `scripts/inversion_phase1_shadow_score.py --provider anthropic --source-prefix 'phase3-conversion/
  X_PATTERNS'` (or `--phrase`), served line in the report; wire every new report at the FRONT of `PHASE3_REPORTS`.
  Surface-2 probe: `scripts/inversion_phase3_surface2_floor_probe.py --provider {anthropic,openai} --samples 5 …`,
  both legs, wire into `SURFACE2_FLOOR_PROBES` (gate refuses a report without a served line; all legs must agree).
  Phase-2 gate: `scripts/run_phase2_gate_envstripped.sh --provider anthropic --out …`.
- **The grammar reads a rail entry's description, not ACTION_DESCRIPTIONS, once an op has an entry** (memory
  `project_router_grammar_prefers_rail_entry_description`). Sharpen descriptions with a ×4 same-session control on
  the old text (an in-process map clear, never a tree revert) and re-score the list.
- **Gate's `CURRENT_LIVE_CATEGORIES` must mirror the flag** — change it in the same commit as any flip.
- **Mail**: `scripts/mail-send.sh` with every path explicit incl. both halves of inbox→read moves; filenames ≤150
  chars (main went red on one of mine); `mailboxes/pard/` is gravestoned — Pard's inbox is
  `~/Development/mediajunkie/docs/mail/` (commit+push there). cc PM only for (a)(b)(c).
- **Open with others**: "comment on 99" accepted variance (CXO may rule it back → one literal, not the list); B3 "how
  do we work together" open between CXO/PPM; "never mind" variants tolerance (CXO); #1922 ratchet coverage note;
  #1913 waits on PM's two answers (server path verified correct); Exec's Fable→Opus trial = this restart.
- **PM's state**: unwell this weekend; test card v16 rows A–D + G to re-test on v165+; row E needs two Fly secrets
  (`GOOGLE_CLIENT_ID/SECRET`; Google client "Piper Alpha" exists, Internal audience, redirect URI confirmed).
- **Never**: `git stash pop` (shared stash; `push -u -m tag` / `apply <sha>` / drop); destructive git in PM's
  checkout; controls by reverting the tree; `close/fix #N` adjacency in commit messages without `Auto-Close:
  intentional`; estimated timestamps (`date` first).

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
- **Alpha = Fly v165 (10-02 13:3x `20ecbda44e` — four deletions, ceiling 259; #1606 floor-element plans; #1920 cross-family carrier release; PA's #1911/#1918; flag 8 tokens incl. delete_todo). main carries read_floor (NOT flipped, not yet deployed); MCP v7** — everything on main deployed. Deploy = detached throwaway
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

## Queue (Fri 10-02 STOP — pace normally per PM; budget 18% @18:23; watch the burn)
1. **read_floor descriptions** (next unit): sharpen `explain_trust` (relationship / limits / why-did-you, not just data
   privacy), `get_memory` (history / search / recall phrasings), `analyze_blockers`, `get_capabilities` ("help") in
   ACTION_DESCRIPTIONS — same ×4 same-session control as the GitHub ones (old text via an in-process map clear);
   re-score the four lists on Haiku; re-run `scripts/run_phase2_gate_envstripped.sh --provider anthropic`. Phase-2
   report of record: `inversion-phase2-gate-2026-10-02-read-floor-haiku.md` (no regression; TRUST 0/10 router).
2. **Flip `read_floor`** = PM's hand (token in `PIPER_INVERSION_LIVE_CATEGORIES`, 9 tokens) — only after (1) reads
   clean; then deploy main (read_floor + whatever lands) and live-probe "what can you do?" / "do you trust me" through
   the rail. Only after it's live do DISCOVERY/TRUST/MEMORY/ANALYSIS lists go, on condition (a) evidence.
3. **Wire the 10-02 Phase-2 full-corpus Haiku run as the verdict of record** (replaces the 10-01 baseline at the gate's
   fallback position) — re-read all nine ledgers after; expect no change, verify.
4. **5 deletable literals** (ANALYSIS 3, MEMORY 2) + REPO_MANAGEMENT (12, GO) + SET_DEFAULT_REPO (4, NO-GO 4 rows) +
   PORTFOLIO (16, NO-GO 9) + INTEGRATION_CONNECT (1 literal) + TRUST/MILESTONE_STATUS_INLINE — small lanes when
   convenient; the #1920 cross-family rule now covers write-bearing lists.
5. **PM's re-tests** on v165 (card rows A–D + G); row E = two Fly secrets; #1913 waits on PM's two answers; #1922
   (spend-free ratchet GUIDANCE coverage) is a note for Arch/CXO.
6. **Open with others**: PPM/CXO — "comment on 99" accepted variance (flagged); CXO — "never mind" variants tolerance;
   Exec — Fable vs Opus trial (my answer: try a day on Opus 5.5 and compare review catches).
7. Cron `5f15d993` expires ~10-05 (rotate by Sat 10-03 START). Heartbeat at the END of every fire.

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
