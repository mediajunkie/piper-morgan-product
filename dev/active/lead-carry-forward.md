# Lead carry-forward — Fable 5.1 seat (PM moved it back 10-05 09:3x); Model A worktree ~/Development/piper-morgan-worktrees/lead

## STATE @ 2026-10-06 08:4x PT — mid-day (log dev/2026/10/06/2026-10-06-0623-lead-code-log.md)
- **10-06 so far (all on main, HEAD `6c7244dd45`)**: Arch's (a) steps 1–5 for complete_todo DONE (router args mini-grammar, 14 corpus rows
  with expected target sets, scorer ARGS_MISMATCH, handler `handle_complete_todo_targets`, CXO's five strings + the NUMBERED-list scope
  rule, served-answer live probe PASSES with PM's sentence). Step 6 (delete the single-ordinal binder, lower `todo-floor-binding`) waits
  for `complete_todo` in alpha's flag (PM's hand). Clear family: not started (strings to CXO first). **#1951**: week_calendar description
  text (4) landed — both conflict rows at the floor on the full corpus; "what projects do I have?" added to PPM's re-judge list; gate
  wiring of all three 10-06 reports HELD for PPM. **#1945 slice 2 + Arch GO DONE** (unlink deletes the mirror; dual-write +
  `get_github_repository()` gone). **#1925 (b) DONE** (hang ceiling 60 s, p50/p95 reported). Pattern-073 marker fix (CI was red on my
  push for ~30 min, 3 NEW failures, fixed `5da0592672`). Standing items corrected (pre-claim probe = measurement not build; #1522 lane done).
- **Deploy manifest for PM grows**: + #1945 slice 2, #1925 (b) test-only, week_calendar text. Still: "ready for PM" = PM deploys →
  I re-test A and D live → then say so. C needs the `complete_todo` token added to the flag at deploy.

### (10-05 STOP state, kept for context)
- **PM's state**: ran the test card 16:21–16:35 on alpha v169, stopped tired and discouraged ("I am questioning the whole project!",
  "I don't know what to decide… Ask Arch"), then: "Don't take my discouraged mood as a final word on anything" and keep working
  unblocked MVP issues. **Arch answered** (doc for PM: `docs/internal/architecture/current/llm-decides-meaning-code-decides-permission-
  2026-10-05.md` — "LLM decides meaning, code decides permission"; Exec carries it to PM as a DIRECTION TO CONFIRM, not a decision).
- **Round results**: B PASS, E2/G PASS; A FAIL (third 404 shape, #1941 FIXED on main); C FAIL ("first three" bound one; #1943 → router
  args, Arch (a)); D FAIL ×3 (#1942 Intent shape FIXED at the model, #1944 bare repo name FIXED, #1945 Project→Config redundancy → CXO);
  clear-default answer with the list → complete_todo('it') (#1943); Radar stale (#1946 FIXED). **Held, by my call + Arch (c): the two
  regex binders** — patch `dev/2026/10/05/held-regex-pair-first-N-range-and-exception-combined-answer.patch`, never to main.
- **Alpha = Fly v169 `36b11f3b2c` (12:55), 12 tokens.** NOTHING deployed since. **Next deploy is PM's hand** (my seat is denied `fly
  deploy`); manifest on the card: 1941, 1942, 1944, 1946, 1918 (PA's Revoke), 1915 (zone names), list_repos fallback, n=1 copy, mypy
  type fixes. **"Ready for PM" = deploy on alpha → I re-test A and D LIVE (served answer, not route) → then say so.** C and the clear
  flow stay off the card until (a) lands (~a week per Arch's doc).
- **CI**: Tests AND Architecture Enforcement both GREEN on main (8257d5c9c5 → 5ec039f395) — first time together since 10-01. #1947
  (41-run red mypy ratchet) CLOSED: fixed not frozen; CI-pinned toolchain recipe below. Arch's floor-regex ratchet is on main
  (`todo-floor-binding` 9, `reminder-clear-binding` 17 — down only).
- **Arch's rulings (10-05)**: (a) complete_todo + clear family consume router args (ordinals/ranges/names/exception sets/verb answer),
  deterministic code only at resolution-against-data + the #1190 confirm which must ENUMERATE ("Complete A, B, C? Leaving D."); gate =
  Phase-3 discipline: corpus rows WITH EXPECTED TARGET SETS + shadow score + a LIVE PROBE THAT ASSERTS THE SERVED ANSWER; then delete the
  floor binders. (b) prose floor stays per carrier until its args land. (c) held pair: never. (d) source fix + model shape pin: done.
- **Arch's late rulings (21:4x), all GO**: #1832 deleted tonight; **#1925 perf contract = (b)** report p50/p95, keep ONE hang ceiling
  (~60 s), don't assert latency; **#1522**: delete `services/persistence/` + its pin + `scripts/create_missing_init_files.sh` ref, table-drop
  migration WITH (a) a prod row count stated in the commit (prod reads are PM's hand — ask via Exec) and (b) a `downgrade()` that recreates
  the empty schema; remove Places + Documents surfaces once CXO concurs (grep NON-browser callers of the Documents API first — MCP,
  scripts, tests — and state the denominator; `update_document_query` hits document services, not the route); **#1945**: retire
  setup.py's dual-write AND remove the dormant `Project.get_github_repository()` legacy fallback (`models.py:503-504`, zero callers) in
  the same commit; slice 2 delete-on-unlink covers existing mirrors.
- **Open with me**: #1931 (rail entry, bounded); #1931 reopen_todo chat route (rail entry — permission shape, fine
  to build, fresh-session item); #1522 scan; pre-claim shadow probe; #1925 CI decision; #1930 step 2; #1936; GUIDANCE deletion (GO under
  the 12-token set — re-score first); (b) multi-intent sibling rail. #1880 is DONE in code (CXO copy pass owed). #1949 corpus row.
- **Habits earned today**: a route-level probe is NOT a served-answer probe (today's whole lesson); the dev venv's mypy is skew, not
  drift — measure with the pinned toolchain; every push cancels the previous CI run — hold pushes while a verdict is pending; background
  test runs must capture `-rf` to a file, not `tail -2`; `gh run list` sanity-checked by createdAt; a test's PRECONDITION can be the
  very shape a fix removes; `Intent` now mirrors its message both ways — write handlers reading either field.

## CI-pinned mypy toolchain (reproduces CI exactly; the dev venv does not)
`/opt/homebrew/bin/python3.11 -m venv $TMPDIR/mypy-gate-venv && $TMPDIR/mypy-gate-venv/bin/pip install -c scripts/mypy-gate-constraints.txt
"mypy==2.3.0" "sqlalchemy==2.0.23" "pydantic==2.12.5" "fastapi==0.115.14"`, then `…/bin/python scripts/check_mypy_gate.py [--raw]`.
Attribute drift by `--raw` on a detached worktree at the last green sha vs now, diffing per `[code]` with line numbers stripped.

## THINGS NOT WRITTEN DOWN ANYWHERE ELSE (the category that disappears)
- **Deploy**: from the detached throwaway worktree `/tmp/lead-deploy-wt`: `git fetch origin main && git checkout
  --detach origin/main && fly deploy -a piper-morgan --remote-only --build-arg PIPER_GIT_SHA=$(git rev-parse HEAD)`;
  verify `curl -s https://alpha.pipermorgan.ai/health` git_sha and re-read the flag (`fly ssh console -a piper-morgan
  -C 'printenv PIPER_INVERSION_LIVE_CATEGORIES'`). Never from PM's checkout.
- **Live probes** (llm-marked e2e, real app + Postgres 5433): `K=$(venv/bin/python -c "from services.infrastructure.
  keychain_service import KeychainService; print(KeychainService().get_api_key('anthropic'))" 2>/dev/null | tail -1)` — **the `| tail -1` is load-bearing (10-06): KeychainService logs two lines to STDOUT first; without it the "key" is log text and every call fails with a misleading `APIConnectionError: Connection error` (cause: `LocalProtocolError Illegal header value`). Check the mask reads `sk-ant…` before spending.** Then `env -u
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

## Queue (Tue 10-06 mid-day)
1. **Deploy follow-through** (PM's hand): on deploy verify `/health` sha, re-read the flag (ask for `complete_todo` in it), re-test A, C
   and D live (served answers), THEN tell Exec "ready" with the answers quoted. Then step 6: delete the single-ordinal floor binder,
   lower `todo-floor-binding`.
2. **Clear family args** (Arch's (a) second carrier): draft the five strings for CXO first (mirror the complete_todo set), then corpus
   rows with target sets → shadow → served probe → delete the clear binders (`reminder-clear-binding` 17 → down).
3. GUIDANCE re-score (running 08:4x) → if at bar, wire + cycle under the 12-token set per Arch's GO · #1522: persistence delete needs the
   prod row count (Exec/PM) · Places remove (CXO yes; non-browser-caller grep + denominator) · Documents HELD #1270 · #1931 reopen_todo
   rail entry (fresh-session item) · pre-claim shadow probe MEASUREMENT (needs the flag on a live env or a local traffic pass).
4. Memory eval section + registry row at each STOP; cron rotates by Sun 10-11 START.

## Cron / registry
**Recurring cron `1224eddf`** (`17 6,9,12,15,18,21 * * *`), armed 10-05 21:5x at STOP (delete-then-create; was b32d3b97), expires ~10-12 → rotate by Sun 10-11 START
(CronList → CronDelete → CronCreate → CronList, exactly one). 10-05: 06:17/09:17/12:17/15:17 arrived ~30 min late each; 18:17 arrived
18:47 (the turn was live). Heartbeat every fire (`scripts/duty-cycle-heartbeat.sh lead WORK`; the post-push marker often already counts).

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
