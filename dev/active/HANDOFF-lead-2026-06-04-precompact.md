# Lead Developer — Pre-Compaction Handoff — 2026-06-04 (evening)

**Role**: Lead Developer (claude-opus-4-8, 1M context, code)
**Purpose**: Continuity handoff before context compaction (PM-requested). Read this + the session log (`dev/2026/06/04/2026-06-04-1135-lead-code-opus-log.md`) + cycle log (`dev/active/cycle-log-lead-2026-06-04.md`) to resume.
**Working location**: bare-main checkout (`/Users/xian/Development/piper-morgan/piper-morgan-product`) on `main`. The `worktree-mux-ui-lane-scoping` worktree is a STALE May-19 leftover — do NOT commit there; all real work is on `main`.

---

## 🔴 THE HEADLINE FINDING — server LLM "outage" was env-var shadowing (FIXED)

**Symptom**: After every server restart *today*, all LLM calls failed — `APIConnectionError`, surfaced to users as *"AI service is temporarily unavailable."* Looked like a rate limit; it wasn't.

**Root cause**: The Claude Code Bash shell exports `ANTHROPIC_API_KEY=` (**empty**), plus `ANTHROPIC_BASE_URL` / `ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_CUSTOM_HEADERS`. Launching `main.py` from that shell makes the server inherit the empty key, which **shadows the real key in `.env`** (python-dotenv won't override an already-set var). SDK → connection failure with no usable credential.

**Decisive proof**: the server's own `venv/bin/python` reaches `api.anthropic.com` fine (httpx 405 ×3) and so does `curl`, but the running server's authenticated POST failed. Same machine, opposite result → config, not network/rate-limit.

**Fix (launch-environment only, NO code change)** — restart server AND any SDK-calling script (e.g. the canonical-retest in-process judge) with the vars stripped:
```bash
env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS \
  POSTGRES_PORT=5433 nohup venv/bin/python main.py > /tmp/piper-server.log 2>&1 &
```
**Current live server**: PID 50934, started clean-env, LLM verified working (real floor response, not "unavailable").

**Durable artifacts**:
- ✅ CLAUDE.md Quick Reference — added the ⚠️ server-restart-clean-env note (on `main`, this session).
- ✅ #1152 filed — FUTURE: multi-LLM / local-model fallback when primary provider unreachable (PM's "test against another LLM / local model" idea).

---

## Canonical retest (Run 12) — ✅ COMPLETE, clean, no regression

Run 12 (2026-06-04 23:10, clean-env) is the **new valid baseline**:

| Metric | Run 11 (Jun 3) | Run 12 (Jun 4) |
|---|---|---|
| Routing PASS | 93.4% (57/61) | **93.4% (57/61)** — identical |
| Quality PASS (judge ≥7) | 80.3% (49) | **85.2% (52)** |
| MARGINAL | 5 | 2 |
| FAIL | 6 | 6 |
| Skipped | 1 | 1 |
| Service errors | n/a | **0** |

- **Zero service errors** → env-fix confirmed end-to-end (classifier + in-script judge both reached Anthropic).
- Routing identical → #1146/#1147 UI changes caused no regression (as predicted; neither touches intent routing).
- Quality +~5pp = within normal LLM-as-judge variance; not claimed as a real improvement.
- Report/CSV at `dev/2026/04/11/canonical-retest-m1-report.md` + `-results.csv` (committed). Run 11 preserved in git history + `/tmp/run11-baseline-*`.

---

## Sprint state

- **M2: CLOSED** (June 3 — #1047 closed, Run 11 captured).
- **M3: ACTIVE**, anchor = architectural cleanup + UI testability.
  - ✅ #1142 UI-AUDIT-FUNCTIONAL — `docs/internal/audits/ui-functional-audit-2026-06.md`. Key reframe: UI is wired, the gap is *reachability* (nav-orphans), not wiring.
  - ✅ #1146 NAV-WIRE-ORPHAN-PAGES — wired /insights (top-level, Stage 1) + /files (dropdown); closed #1134. Commit `0e6a51e87`.
  - ✅ #1147 /documents trust_stage — extracted shared `_resolve_trust_stage()` helper. Commit `e77744b93`.
  - 📋 Filed, not started: #1148 UAT-test-user-stage affordance (low), #1149 debug-route-prod-exposure check (low), #1152 multi-LLM fallback (future).
  - ⏭️ **Next M3 candidate**: #1124 PRE-FLOOR-HANDLER-AUDIT (the other architectural-cleanup piece). PM said "after [#1142] not sure" — needs PM confirm before starting. Does NOT depend on the canonical retest.

---

## Open threads / pending PM decisions

1. **Run 12 result** — report delta vs Run 11 once it lands (in progress at handoff).
2. **#1124 PRE-FLOOR-HANDLER-AUDIT** — confirm it's the next M3 item, or PM directs elsewhere.
3. **CXO UX working session** — PM wants to discuss the web UI / overall UX with CXO; alert memo already sent. PM to schedule.
4. **#1152 multi-LLM fallback** — future/backlog; PM to prioritize.

---

## Resume checklist (post-compaction)

1. Confirm role = Lead Developer (this memo + session log filename).
2. Verify server is clean-env: `curl -s localhost:8001/health`; if restarting, USE THE `env -u …` WRAPPER above.
3. Check Run 12 report date; compare to Run 11 (93.4% / 80.3%); report to PM.
4. Await PM direction on #1124 vs other M3 work.
5. Sign-off discipline: ensure CLAUDE.md note, this handoff, session log, cycle log are committed + pushed to `origin/main`.
