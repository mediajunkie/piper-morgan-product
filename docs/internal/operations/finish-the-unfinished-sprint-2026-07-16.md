# Finish-the-Unfinished Sprint — Plan of Record

**STATUS: RATIFIED** — PM approved in-conversation with Lead Dev, 2026-07-16 (~14:00 PT): *"This all sounds good to me. Yes let's just keep using this sprint. Please write down the plan. Then you are authorized to execute."*

**Tracking**: epic [#1424](https://github.com/mediajunkie/piper-morgan-product/issues/1424), on the **Beta Blockers - Hard Gates Only** sprint board. Executor: Lead Dev (+ subagents). Arch ratifies lint designs before CI-blocking.

---

## Why (one paragraph)

The 2026-07-16 multi-tenancy audit (#1419) + the first scenario-driver run (`tests/e2e/test_scenario_driver.py`) established that this codebase's bug **generator** is *work that stopped when the symptom stopped*: incomplete retrofits (#1415 provider selection, #1420 owner scoping, #1421 default project), half-done migrations (#1422 — #262 dropped the preferences column), silent-death exception handling (#1423 — 1,233 broad excepts converting feature death into invisible defaults), and unreachable capability (#1417 — connect-github declined while `link_repo` exists). Discovery rate has not flattened → gaps, not gremlins. This sprint closes the **generator**, not just the instances. PM: *"the problem is the path. now we know."*

## The admission rule (what keeps this out of rabbitholes)

**A category enters the census only if it has a cheap mechanical detector** — a grep, static check, or reachability sweep producing a *count + list* in ≤2 hours. No detector → the category waits for evidence (the way multi-tenancy waited for the provider incident). "Read everything and see what feels off" is banned.

## The six detectors (Phase 0 census)

| # | Category | Detector | Pre-census signal |
|---|---|---|---|
| 1 | Incomplete retrofits (multi-tenancy) | #1419 audit method (4 parallel investigators) | **DONE** — inventory in `docs/internal/architecture/current/multi-tenancy-audit-2026-07-16.md` |
| 2 | Silent-death handlers | Triage `except Exception` on core path into LEGIT / NARROW / UNSWALLOW | 1,233 total; **244 core-path** |
| 3 | Signature drift (#1420 class) | One-shot mypy (`--ignore-missing-imports --check-untyped-defs`), filtered to `call-arg` / `arg-type` / `attr-defined` | never type-checked; class unenumerated |
| 4 | Unreachable capability (#1417 class) | Reachability sweep: registry ∪ classifier vocab ∪ routes vs. what's dispatchable/reachable (extends the #1283 ratchet model) | link_repo exists yet "connect github" declines |
| 5 | Stubs shipped as done | Grep `NotImplementedError` + placeholder returns + TODO/FIXME | **12** NIE (prod), **78** TODO/FIXME |
| 6 | Promise/copy drift | Scenario driver (dynamic) — already running; extend scenarios as census finds candidates | #1416/#1417 reproduced deterministically |

## Phases

### Phase 0 — Census (no fixing; ~1 day, parallel subagents)
Run detectors 2–5 (1 and 6 already exist). Output: **ONE inventory doc** (`docs/internal/operations/finish-the-unfinished-census-2026-07-16.md`), counts + HIGH/MED/LOW triage. **The backlog freezes at census end** — that frozen list is the sprint scope. Mid-sprint discoveries are FILED (into the epic, tagged for the next census), never chased.

### Phase 1 — Guards first (~1–2 days)
Land enforcement **before** fixes, so the hole can't refill while we work:
- `scripts/check-unscoped-reads.py` — AST lint failing on unscoped user-specific credential/config/repo reads (extends #849 `check-keychain-scoping.sh` + #1252 principal-threading lint; design per the audit doc's enforcement section).
- `scripts/check-silent-death.py` — AST lint flagging `except Exception → return <default>` on core-path modules, allowlist via `# silent-ok: <reason>`.
- Ratchet test (`tests/test_completion_ratchets.py`) with census-frozen ceilings — a count that *grows* fails the build immediately (growth-only, cannot false-positive existing code → **CI-gates immediately**).
- Scenario driver added to CI (xfail-tolerant tier).
- **Arch ratification**: memo out at Phase 1 start with both lint designs; lints run warn-mode until ratified, then flip to CI-blocking.

### Phase 2 — HIGH fixes, user-impact order (bulk of sprint)
1. **#1422** personality prefs dead (systemic; likely behind #1416's weak feel)
2. **#1415** per-user provider selection (the exemplar; Arch-coordinated, ADR-071/075-adjacent)
3. **#1416/#1417** onboarding turns (classification-surface = routing-stack doc + Arch-coordinated)
4. **#1420/#1421** owner-scoping repo fixes
5. Un-swallow the worst of Census A's UNSWALLOW-HIGH list
Rules: each fix **lowers its ratchet ceiling in the same commit** (the `MAX_DISPATCH_SITES` discipline). **Time-box + tripwire**: half-day per MED, one day per HIGH — overruns escalate to PM rather than digging. Fixes ship to beta incrementally as they land (pre-prod: cut clean now); alpha parity at sprint end.

### Phase 3 — Acceptance (the driver is the referee)
Sprint exits when, on one clean run:
- [ ] Scenario driver passes with xfails flipped to **strict**
- [ ] Canonical suite green
- [ ] Both lints green (CI-blocking, post-ratification)
- [ ] Zero silent-death errors in a driver run's logs
- [ ] Ratchet ceilings all ≤ census baselines, HIGHs at zero

**This gate is identical to "ready for a second human tester."**

## Definition of done: ratchet, not zero
HIGHs fixed; every remaining count **visible and monotonically shrinking**. 78 TODOs may survive the sprint; a silent 79th may not. The sprint ends on the acceptance gate, not on exhaustion.

## Anti-rabbithole rules (summary)
1. **Census/fix separation** — finding and fixing never in the same phase; mid-sprint finds are filed, not chased.
2. **Ratchet, not zero** — done = HIGHs fixed + counters can't grow.
3. **Time-box + tripwire** — overruns escalate, never dig.
4. **Detector-gated categories** — no mechanical detector, no census entry.
5. **The driver is the referee** — acceptance is user-visible behavior, not internal beauty.

## Related
#1424 (this epic) · #1419 (multi-tenancy epic + audit doc) · #1414/#1415/#1416/#1417/#1420/#1421/#1422/#1423 · #1152 (resilience) · #928 (canonical suite) · patterns 045–047 (completion discipline — this sprint is that discipline applied at codebase scale).
