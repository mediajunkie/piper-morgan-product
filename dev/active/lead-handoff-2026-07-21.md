# Lead Developer — Session Handoff (prepared 2026-07-21 21:50 PT, per Exec's migration-prep ask)

**For a fresh Lead session picking up cleanly. Read this + `dev/active/lead-carry-forward.md` + CLAUDE.md's Lead briefing. Everything below is on origin/main.**

## Identity & mechanics
- Role: Lead Developer (slug `lead-code`); session logs in `dev/YYYY/MM/DD/`.
- Cron: session-only, re-arm on any fresh session: `17 6,9,12,15,18,21 * * *` thin-prompt duty-cycle (Gap-C: re-attach/restart KILLS session crons — always CronList-verify at start).
- Build work in a WORKTREE (EnterWorktree); the shared main checkout is mail/logs only — NEVER destructive git there; never silence push output (`-q 2>/dev/null` on push ate a rejection and stranded commits on 7/20).
- Mail: `scripts/mail-send.sh` push-to-ref; regen (`--role lead`) self-heals inbox ghosts (#1454).
- Venv: `/Users/xian/Development/piper-morgan/piper-morgan-product/venv` (strip ANTHROPIC_* env for server/tests; POSTGRES_PORT=5433).

## State of the world (2026-07-21 EOD)
- **CI: Tests workflow GREEN and governed** — the #1452 burn-down gate rules the full suite. Backlog ~272 (tags: fixture/triage/flaky/regression), shrink-locked both directions, diagnose step auto-attaches tracebacks to new failures. Ceilings all current in `scripts/ratchet_ceilings.json`; mypy gate live (40/405/249/209).
- **Beta: Fly app `piper-morgan` at v26** — durable-upload volume (v22), CPU-torch image (v24), B3 continuity fix (v25), learning-loop fix (v26). `main == production` lockstep; deploy = `fly deploy` bare (NEVER piped).
- **Shipped this arc**: #1400/#1401 (data-loss pair) · #1409/#1410 · #1438 (the learning loop was dead behind a JSONB `->`/`->>` bug — fixed + deployed) · #1394 turn-3 continuity (B3 wiring; D4 intact) · #1393 (prompt fix, open pending scenario re-run) · #1322/#1447 closed · #1449/#1451/#1452 filed · #1454 filed+fixed.
- **Key infra built**: `scripts/check_fullsuite_backlog.py` + `scripts/known_failing_backlog.tsv` (the gate) · `tests/conftest.py::delete_test_user_fully` (THE user-cascade; 26 FK refs) + the root NullPool session_scope fixture (killed the poisoned-pool class) · `delete-module-safely` + `query-github-board` skills.

## In flight / awaiting others
- **Arch** (2 rulings pending): methodology/ package fix-or-delete (zero prod importers; 21 backlog entries ride it) · #1432 orphan-pair delete ({LLMIntentClassifier, llm_classifier_factory} — NOTE my finding: the #1124 Phase-4 flip lives ONLY in the orphan; the live classifier.py never got it). Also flagged to Arch: ContextMatcher's permissive unknown-trigger match-all (proactive-misfire hazard).
- **Exec**: #1386 gate re-run scheduling (CXO/PPM windows) — beta v25+ carries BOTH Scenario-B fixes; one re-run verifies #1393 + #1394 turn-3. My offer: canonical suite + 3 scenarios + sign-off, ~half a day.
- **PM** (2 standing calls): #1424 close-vs-keep (my lean: close — ratchet work lives in #1423/#1452/#1419) · #1427 PROD-RECONNECT bucket confirm.

## Burn-down queue (#1452, in rough order)
Fresh e2e triage adds (~18, tracebacks in the 7/21 CI logs) · intent_wiring RecursionError cluster · document_processing (9 errors) · execution_analysis (7) · standup_performance (9, likely thresholds) · methodology (21, awaiting ruling) · connection_pool (9, HELD — spatial cascade zone) · ~200 triage glances. Method: standalone glance → fix-or-prune-with-record → shrink same commit → CI arbitrates; validate suspect cures with the sweep-order-prefix repro (20s-3min), never standalone-only. Named tells: keyed-CI-vs-keyless-local asymmetry = encrypted-column-dependent behavior; time-of-day oscillation = clock-dependent asserts; isolated-pass/sweep-fail = order/state pathology.

## Standing constraints (verbatim-critical)
ENCRYPTION_MASTER_KEY never in repo/chat; droplet key NEVER replaced. Droplet ssh root@146.190.151.63 (NOT the `droplet` alias — different machine). Spatial intelligence PROTECTED — all spatial deletions HELD pending the PM-directed review (Arch synthesizing; CXO voted keep-live+park-cold; PPM dedicated pass pending). connection_pool/adapters/consumer_core = held cascade. Sprint-field changes per-item mutation ONLY (assign-sprint-safely).
