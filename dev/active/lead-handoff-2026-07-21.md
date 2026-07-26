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

---

# REFRESH 2026-07-26 (per CIO's ask; Arch's §4/§6 model followed)

**Delta since 7/21 — pointer, not restatement** (all on origin/main): the #1452 arc ran 634→56 with CI green under the gate since 7/23 (issue comments on #1452 carry the milestones + composition); beta v27→v28; six drain-surfaced product fixes; Arch's methodology ruling executed 7/26 (design record: `design-record-methodology-as-code-2025.md`); carry-forward + session logs current daily. Honesty check: **context intact, first-person recall of the whole arc** — these sections are real, not reconstruction. Claims marked VERIFIED/BELIEVED per Arch's convention.

## §4 — Hard-won lessons (first-person)

### 1. A chronically-red suite is a stack of real findings queued behind the first liar. (VERIFIED — the arc's spine)
Every layer of CI dishonesty removed let the tests reach deeper, and each deepening surfaced either an environment gap or a LIVE product bug: 5 CI root causes in sequence (keychain import-raise → mypy blind-to-absence → fossil jobs → missing postgres → missing redis), then the doc-surface silent unmount, the usage-cap error-masking, the radar keyless-500. None were visible until the layer above stopped lying. The reflex to inherit: when a gate is red-forever, the first question is not "how do we quiet it" but "what is the first liar hiding."

### 2. One green observation is not a cure; local passes are not CI passes. (VERIFIED — twice, at cost)
Local sweep claimed 20 backlog entries now-passing; CI confirmed exactly 6 — the other 14 were env-oscillators that would have gone red on the wire. Later I retired the doc-edge flaky tags on ONE green CI run; they failed the very next run. The standing rules that came out: **only CI-confirmed removals**, and **an oscillator's tag retires on a sustained run of greens, never one**. The gate's shrink-lock is the mechanism that makes this cheap to obey.

### 3. An honest inconclusive outranks a tidy pass. (VERIFIED — CIO cited it as the discipline working)
The 2a-bis hook probe came back ambiguous on my seat (the permission classifier intercepts before git hooks can fire). I reported INCONCLUSIVE instead of treating the refusal as the pass CIO's rubric then required — which forced the rubric correction, which is what made HOST's later fresh-seat PASS trustworthy. A check whose pass condition has an alternate cause isn't a check. Never manufacture a pass from a denial; never work around a denial to force one.

### 4. The construction-boundary disease has many faces, one cure. (VERIFIED — five expressions in one arc)
Keychain raising at import; `DocumentService()` at module level; `OpenAIEmbeddingFunction` at `__init__` (500ing radar keyless); loop-bound cached pools twice (asyncpg per #1193, then its exact Redis twin). All one disease: work done at import/construction that belongs at the operation boundary. **Keyless CI is the instrument that reveals it** — a keyed dev box structurally cannot. When something works keyed-local and dies keyless-CI, look for eager construction before anything else.

### 5. Quality-banking works when the trigger is named; the flywheel drains everything else. (VERIFIED)
The learning complex failed piecemeal for days; banked with an explicit trigger ("dedicated focused session"), it drained in ~90 minutes in the Saturday window — root cause (a LIVE user UUID shared between tests, the manual script, and real app activity) was only visible with the whole complex in view. Everything not deliberately banked got drained same-wake, per the spine. The discriminator is WHY you defer: pacing the cron = the antipattern; a complex chase deserving whole-view focus = the exception, said out loud.

### 6. Instrument discipline: validate waves in-sweep, and let CI runs finish. (VERIFIED — wave 18 and the cancelled-runs morning)
Wave 18 passed standalone and failed the full sweep — the in-sweep validation rule caught it pre-push. Separately, my push cadence kept auto-cancelling CI runs before they could report; pausing pushes until a run completed is what produced the first green. The meta-rule: an instrument only informs you if you let it complete on the thing you actually shipped.

## §6 — Load-bearing vs. commodity (what the Lead role holds)

### Load-bearing (dies in a bad handoff)
- **The fixture-rot-vs-regression triage judgment, incl. flaky semantics.** (VERIFIED) The gate's tags are mechanical; deciding WHICH tag — and that flaky means *context-oscillator, shrink-lock-exempt both ways, retire only on sustained greens* — is judgment built on ~44 waves. The named diagnostic tells (keyed-CI-vs-keyless-local = encrypted/keyed-dependent; isolated-pass/sweep-fail = order/state; time-of-day = clock-dependent asserts) are an active lens, not a list.
- **The seam with Arch, from my side.** (VERIFIED; reciprocal of Arch's §4.2) I map/build/feasibility-check; Arch guards invariants; each corrects the other out loud, same-message. My side's obligation: bring Arch the honest failure detail even when it embarrasses my own build (the #1394 wiring find), and STOP on their integrity calls even mid-build. Also: never inject history into the classifier — D4's pressure point recurs with every reference bug, and the answer is always the wiring/ledger, never the prompt.
- **`delete_test_user_fully` and the fact behind it.** (VERIFIED) The app creates dependent rows (personalization_contexts and 25 other FK refs) for users MID-TEST; every hand-rolled teardown eventually rots. The helper is information_schema-derived and lives in tests/conftest.py; the *reflex* — rewire rotted teardowns to it rather than patching FK order — is the part to inherit.
- **Spatial protection as an active reflex.** (VERIFIED) Anything touching Place/territory/adapters/connection_pool gets PARKED, not modernized — even when the fix looks mechanical. PM's standing rule; the held cascade is intentional. Three clusters were correctly identified and parked mid-drain this arc.
- **The llm-lane gap.** (BELIEVED) The keyed lane keeps accumulating tests (~50 by now) with no scheduled executor. Flagged 7/23, still standing. If nobody builds the runner, those tests are write-only.

### Commodity (reconstitutes from artifacts)
- The backlog TSV + gate script + wave history (on main; #1452 comments narrate it). The release runbook + cut-release skill. The CI workflow shape incl. the probe + oscillator-diagnostic steps. My carry-forward/standing-items. All durable; point, don't copy.

## §5 — Amber, as QUESTIONS (never seen it)
1. Does the permission-classifier layer differ there — i.e., can 2a-bis actually observe hook liveness? (Re-run it first fire; that was the plan of record.)
2. Do `gh` auth + `fly` auth + the keychain-loading conftest carry, or are those first-touch approvals in the attended window?
3. Does the dev Postgres (5433) / Redis / venv discovery work the same from an Amber worktree, or does the sweep instrument need re-baselining?
4. Who re-arms the session cron after migration — does Gap-C behave the same under tmux?
