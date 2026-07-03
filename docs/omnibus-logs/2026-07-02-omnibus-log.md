# Omnibus Log: July 2, 2026

**Day**: Thursday
**Sessions**: 5 primary (Exec, Arch, Lead, Docs, CXO) + 1 backup-account Docs doppelganger (closed retroactively)
**Day Type**: HIGH-COMPLEXITY — dual security findings resolved same-day, production deployment with caught outage, dot release v0.8.9.1 shipped, double audit close, blog publish
**Justification**: Three simultaneous arcs (security/deploy, docs/blog, release) with tight cross-agent coordination; real production incident (PIPER_HOST outage, self-inflicted and self-resolved); Janus relay experiment; multiple escalation surfaces touched.

**Git Commits**: 20+

---

## Sources

- `dev/2026/07/02/2026-07-02-0832-exec-code-sonnet-log.md` — Exec (Chief of Staff, backup account)
- `dev/2026/07/02/2026-07-02-0840-arch-code-log.md` — Arch (Chief Architect, backup account)
- `dev/2026/07/02/2026-07-02-0923-lead-code-log.md` — Lead Developer
- `dev/2026/07/02/2026-07-02-1047-docs-code-log.md` — Documentation Management (canonical; PM wrote STOP)
- `dev/2026/07/02/2026-07-02-1647-cxo-code-log.md` — CXO (Chief Experience Officer, backup account)
- `dev/2026/07/02/2026-07-02-1257-docs-code-log.md` — Docs doppelganger (backup account, pre-edit work superseded by main session; closed 2026-07-03)

**Cross-reference gate**: PASS — all 5 primary roles internally consistent. CIO mentioned as "still dark" (no active session, expected). HOST mentioned re #1344 routing but no log (not active on this date, expected). No missing logs.

---

## Unified Timeline

### Morning — Security arc opens (08:32–11:00)

- **Exec** (08:32) START on backup account — retroactive Jul-1 DAY-CLOSED self-healed. Two 🔴 security findings from Lead flagged to PM: #1343 (anonymous billing exposure via `/api/v1/intent`) and #1344 (open registration reversed a 2026-06-25 PM-ratified gate decision). Migration no-clash confirmed (PM/Exec accounts not colliding). Rollup deferred to PM's client-work window.
- **Arch** (08:40) START — reads overnight security findings. Sends gate-integrity architectural read to PM cc Lead/HOST (09:10): #1308 exempt-list lint IS built and working; these are two COVERAGE GAPS in a working guard, not a missing guard. Gap A (#1344): `create_user` exempt-justification checks existence-of-reason, not truth-of-reason — silently falsified when Caddy perimeter removed 2026-06-29. Gap B (#1343): lint's risk dimension is auth+WRITE; billing exposure is auth+PAID-SIDE-EFFECT. Reframe for PM: restore-gate = bridge; build-invite-control = durable. Accept-risk counseled against for open registration. Commits to decisions.log.
- **Lead** (09:23 fire, log created ~09:55) — reads Arch's memo immediately (notes own process gap: dove into building before creating the log; corrects transparently). Verifies `create_user` (`setup.py:773`) still has zero gating (Gap A confirmed open). Builds `tests/test_anonymous_llm_key_boundary_1343.py` — the missing auth+PAID-SIDE-EFFECT dimension for #1308 family; probes FastAPI route dependant tree, proves detection logic real with throwaway bad-handler/good-handler test before trusting it. 3 new tests. 69 tests green. Commits `fecc2942a`, verified via `git show --stat` before and after push (yesterday's lesson applied). Holds Gap A — inside PM's open #1344 call.
- **Arch** (10:45) — reads Lead's Gap-B ratchet from the artifact (not the summary). Ratifies: correctly encodes cost-dimension invariant, non-vacuous. Names 2 honest limits: (1) indirection blind-spot (reads endpoint source, not call-graph); (2) mention≠handle (proves name appears, not that it's caught on the anonymous path). Names m-36 structural end-state (not now): route all billing through a fail-closed-by-construction wrapper → raw resolver has no anonymous bypass; lint becomes backstop. Sends ratify memo to Lead cc PM/HOST. Returns to light-available hold.
- **Lead** (~11:00) — comments #1343 with ratchet evidence. Replies to Arch by mail. Hits mail-send residue edge case (documented tool caveat); verifies pushed commit `a2916b677` correct on origin/main via `git show --stat`; fixes residue surgically on own worktree (explicit paths only, no broad reset); re-syncs cleanly.

### Midday — Docs arc + Arch holds (11:00–17:00)

- **Docs** (~10:47–11:30, PM-present) — Jul-1 omnibus written, gate PASS, committed `b6712e7b2`. ADR-072 gap in adr-index.md fixed (file existed, absent from index). 5 activity-log rows appended, committed `32c0ddf62`.
- **Docs-backup** (12:57) — doppelganger session on backup account starts pre-edit of "The Airport Corrections" (frontmatter, cohort→team passes, heading check). Work later superseded by main-account session.
- **Docs** (~11:30–13:00, PM-present) — BRIEFING-CURRENT-STATE refreshed to Jul 1. ADR README corrected 61→74. Port-8080 audit template wording fixed; staggered-audit-calendar updated. 20 deprecated/forensic dev/active files archived. Weekly audit #1328 CLOSED. Quarterly sweep #1341 CLOSED (concurrent execution; substantive work shared). Key findings: 0 broken ADR links, 0 stale issues, roadmap drift (RECONNECT WS-2 ACTIVE vs DRAINED, PPM-owned), 63 TODO/FIXMEs (M3-Health scope).
- **Docs** (~14:00) — "The Airport Corrections" proofread. Image: PM chose no-text version (atmosphere > explainer for reflection piece). Two minor fixes applied (trailing whitespace + double blank before separator). Bold+italic nesting rendering bug caught and fixed (bold+italic asterisks don't nest in converter). 3 memos sent (commit `59b6ce033`): (1) Docs→CIO CC HOST — audit refactor proposal, weekly/monthly split, frequency question; (2) Docs→HOST CC CIO — agent-infra cadence + welfare lens on distributed-cleanup idea; (3) Docs→PPM — roadmap v18.2 drift flag.
- **Arch** (12:39–16:39) — light-available WATCH holds (~6h). Notes cost vs. availability trade; offers dial-back if PM prefers. No-ops not committed (batched per discipline).
- **CXO** (16:47) — START. Inbox empty. Queue dry — all carry-forwards gated (PPM response on #1331 alpha-trust call; Lead to apply #1201/#1231 copy passes; Exec restore signal pending). Heartbeat only.

### Evening — PM decisions arrive + #1343 deployed (17:00–22:00)

- **Arch** (17:39) — PM's #1344 direction arrived via Janus→HOST relay: invite codes = primary app-layer gate (HOST owns list/issuance); usage-cap/circuit-breaker routed to Arch; obscurity = interim (not restore-Caddy). Arch sends architectural memo to HOST cc PM/Lead: invite-code IS the staged Gap-A fix (`create_user` requires app-layer invite token → removes it from auth-exempt-writable entirely). Usage-cap: SEPARATE concern from invite-code; shape = global ASGI middleware, Redis-backed shared state (NOT in-process — #1109 lesson: per-worker counters × worker-count silently fails cap), fail-closed honest `503`. Arch-shape, product-thresholds (HOST+PM). Returns to hold.
- **PM** (~18:30) — switches from backup to main account for blog publish session.
- **Lead** (~18:57) — PM live in conversation asks for #1343/#1344 walkthrough. Checking mail reveals PM had already decided both via other channels (Janus relay experiment — PM hadn't realized this Lead conversation was still holding). Triages 3 memos to read/. Reports resolution directly to PM.
- **Docs** (~19:00) — "The Airport Corrections" published to pipermorgan.ai. pubDate drift caught in dry-run (UTC +7h → Jul 3; fixed with `--pub-date 2026-07-02`). Bold+italic nesting bug caught in dry-run; fixed. Real publish: hashId=6c74263d4862, webp prepared, blog-content.json + medium-posts.json updated. Website commit `75338cbdd` pushed. Editorial calendar updated: status=published, canonicalSite=distributed, blogURL/blogPath/altText/caption. "From Briefing to Vision" mediumURL added.
- **Lead** (~19:00–20:30) — #1343 DEPLOYED to alpha. Three-stage sequence: (1) Near-miss caught: `origin/production` was 983 commits behind `main` — deploying main's HEAD would have shipped 3 weeks of cross-team work; caught before any container touched; restored `/opt/piper` from pre-sync backup. (2) Correct approach: cherry-picked `57d8a2cd3` + `fecc2942a` onto throwaway branch off `origin/production`; archived to droplet. (3) Self-inflicted-but-self-resolved PIPER_HOST outage: `deploy.sh`'s `git archive` sync silently overwrote an undocumented droplet-local `main.py` patch (same root cause as the Caddy gate removal — direct `nano` edit, never committed). App bound `127.0.0.1` loopback, invisible to Caddy on bridge network; Docker healthcheck stayed green, masking the break. Root-caused, not panicked. Fixed via upstream solution already on `main` (`5f5991c40`, `PIPER_HOST` env var) — wired into `docker-compose.override.yml`. Rebuilt + recreated. Verified: `Uvicorn running on http://0.0.0.0:8001`; `/health` 200; live anonymous-curl returns `anonymous_key_required` (not a silent bill). Documented full incident in `alpha-deployment-runbook.md`. Notes flag for PM: `origin/production` not updated; droplet running code not coherent on production's branch history.
- **Arch** (19:39) — Lead ack received. #1345 filed (the m-36 wrapper end-state: route all billing through fail-closed-by-construction wrapper; Lead filed from Arch's recommendation, Arch notes it as tracked). #1343 deploying confirmed. Thread closed on Arch side. #1344 with HOST.
- **Exec** (20:32) STOP — cohort rollup: Lead = enormous day (security resolved, v0.8.9.1 shipped, #1345 filed); Arch = supported Lead; CXO = steady heartbeat; Docs = published; CIO = stalled (still dark). Migration no-clash confirmed; restore to dedicated account pending PM+Janus plan.
- **Arch** (20:39) STOP — all July 2 work on origin/main. Cron `7d001ae9` left armed (light-available, PM-directed for Lead support).
- **CXO** (20:47 / 21:47) — day wrap: queue dry, all carry-forwards gated. Cohort in build-heavy phase; CXO downstream of PPM's #1331 call.

### Night — Dot release + self-correction (21:00–01:00)

- **Lead** (~21:00) — PM explains main/production release model; directs proper dot release, not silent branch push.
- **Lead** (~21:00–23:30) — v0.8.9.1 dot release. Reads `release-runbook.md` in full before acting. Finds real doc drift during mandatory checklist: `VERSION` file frozen 4 releases behind (0.8.5.1 vs 0.8.9); `docs/versioning.md` has 3 mutually-inconsistent version numbers (header/table/footer); `docs/VERSION_NUMBERING.md` — a third previously-unknown version-of-truth doc, absent from the runbook checklist entirely. Alpha-facing docs (TESTING_GUIDE/KNOWN_ISSUES/QUICKSTART/AGREEMENT/email-template) correctly at 0.8.9 — drift narrow, not broad. Fixes all: backfills versioning.md's missing history from `releases/README.md`'s accurate data; bumps 13 files. Builds `scripts/check-version-consistency.py` (tested against real match AND synthetic mismatch to prove non-vacuous) and wires into runbook as non-skippable step — a mechanical check replacing prose vigilance. Writes `RELEASE-NOTES-v0.8.9.1.md`. Tags `v0.8.9.1`, pushes `origin/production`, cuts GitHub release. Ports same doc fixes to `main` (with correct nuance: main stays at 0.8.9; versioning.md now explicitly distinguishes "0.8.9.1 is the latest released" from "main is at 0.8.9 pending its own cut").
- **Lead** (~23:30–00:30) — #1346 self-correction: discovers that `--import-mode=importlib` was already present in `pytest.ini` `addopts` all along — the "20-22 collection errors" were a self-inflicted testing artifact from overriding `addopts` with a hand-reconstructed list that dropped this flag. Verifies: 11,586 tests, 0 errors on main with zero override. Corrects #1346 on all surfaces: the GH issue, the published v0.8.9.1 release notes (errata commit on `production`, not rewriting the tag), and the live GitHub Release description. Identifies and archives 2 genuinely orphaned test files (`test_cache_effectiveness.py`, `test_sequential_load.py`) referencing deleted module from #1094 — archived to `tests/archive/load/` on both `main` and `production`. Adds explanatory comment on `pytest.ini`'s import-mode line. Closes #1346.

---

## Executive Summary

### Core Themes

- **#1343/#1344 security arc resolved same-day**: Arch's architectural read (Gap A: justification-truth-decay / Gap B: cost-dimension gap in #1308 lint) framed both findings precisely; Lead built Gap-B ratchet in ~1.5h; PM directed Gap-A path (invite-code, not restore-Caddy); #1343 deployed to alpha with a caught near-miss and a real-but-resolved PIPER_HOST outage
- **v0.8.9.1 dot release shipped**: hotfix cut as a proper tagged release; real VERSION doc drift found + fixed; runbook gap that caused the drift fixed with a mechanical check script
- **Double audit close**: weekly docs audit (#1328) + quarterly sweep (#1341) executed concurrently and closed same session; BRIEFING-CURRENT-STATE refreshed
- **Blog pipeline complete**: "The Airport Corrections" proofread, image decision made (no-text), two dry-run catches, published to pipermorgan.ai + syndicated to Medium; calendar fully updated
- **Janus relay experiment**: PM tested Exec/Janus as an inter-conversation relay for PM decisions; surfaced the latency risk (Lead's conversation was holding while PM had already decided via other channels)

### Technical Details

- **Gap-B ratchet** (`test_anonymous_llm_key_boundary_1343.py`): extends #1308 family with auth+PAID-SIDE-EFFECT dimension; FastAPI dependant-tree route enumeration; verified non-vacuous before trusting; 2 honest limits named (indirection blind-spot, mention≠handle); Arch-ratified; `fecc2942a` on main
- **v0.8.9.1 commits**: `57d8a2cd3` (AnonymousLLMKeyRequiredError fix) + `fecc2942a` (Gap-B ratchet) + `5f5991c40` (PIPER_HOST env var) cherry-picked onto production; tagged, GitHub release created
- **PIPER_HOST outage**: app bound `127.0.0.1` loopback inside container; Caddy on bridge network got connection refused; Docker healthcheck (`127.0.0.1` from inside container) stayed green, masking the break; fixed via upstream `PIPER_HOST` env var + `docker-compose.override.yml` wiring
- **Production/main divergence**: `origin/production` was 983 commits behind main (frozen at v0.8.9 cut ~2026-06-22); cherry-pick onto production branch is the correct deployment pattern per runbook
- **VERSION drift**: `VERSION` file frozen at 0.8.5.1 (4 releases behind); `versioning.md` had 3 mutually-inconsistent version strings; root cause = `VERSION` and `VERSION_NUMBERING.md` absent from runbook checklist
- **`check-version-consistency.py`**: new script wired into release-runbook; tested against real + synthetic mismatch; makes VERSION/pyproject.toml agreement mechanically verifiable
- **Docs audits**: 0 broken ADR links; 20 deprecated dev/active files archived; stray `investigation-039-canonical-handler-routing.md` in ADR dir; 63 TODO/FIXMEs (M3-Health)
- **Blog publish pipeline**: pubDate UTC drift fixed (--pub-date explicit); bold+italic nesting rendering bug fixed; hashId=6c74263d4862; cwebp 1200×800 prepared

### Impact Measurement

- **#1343 DEPLOYED and live-verified**: `curl -X POST .../api/v1/intent` (no auth) → `anonymous_key_required` (not a silent bill); alpha site healthy (/health 200, / 401 correct)
- **v0.8.9.1 on `origin/production`**: security hotfix + PIPER_HOST fix + Gap-B ratchet in a coherent tagged release; 51 targeted tests passing; live functional verification strongest signal for this patch
- **#1345 filed**: m-36 structural end-state tracked (fail-closed billing wrapper → lint becomes backstop)
- **Runbook v1.7**: VERSION + VERSION_NUMBERING.md added to checklist; `check-version-consistency.py` as required non-skippable step
- **"The Airport Corrections" published**: building/narrative, Medium-only syndication, calendar fully updated in both repos
- **5 issues closed** (via cross-day accounting): #1328, #1341 (today); #1343 (day-close addendum); #1313 (superseded); #1346 (self-correction)
- **CIO still dark**: flagged by Exec at STOP; non-critical per current assessment

### Session Learnings

- **Janus relay latency risk**: when PM makes decisions in one conversation channel and agent is holding in another, relay lag can leave the agent in a stall loop; real on Jul 2 (Lead held for 9h, PM had already decided via Janus); relay experiment exposed the gap
- **`-o addopts` override drops existing flags**: overriding pytest's `addopts` replaces the full list — silently drops `--import-mode=importlib` and any other flags not explicitly re-included; always reconstruct the full list minus the target flag
- **Direct droplet edits are landmines**: the PIPER_HOST outage and the Caddy gate removal share the same root cause — undocumented, unversioned droplet edits that get silently overwritten by any clean sync; documented explicitly in the runbook
- **983-commit production/main divergence**: production branch frozen at a release cut is by design; cherry-pick is the correct deployment unit, not `git archive HEAD`; the runbook documents this — reading it in full (not partway) caught the near-miss
- **Verify-First on own prior recommendations**: Arch's most valuable single move was confirming #1308 (the exempt-lint) already existed before framing the finding — shifted "missing guard" to "two precise coverage gaps in a working guard," a materially more accurate and useful read
- **Mechanical checks > prose vigilance**: `check-version-consistency.py` wired into the release-runbook replaces a human eyeballing a checklist; the VERSION drift recurred across 4 releases because the runbook listed the relationship in prose but didn't enforce it
- **Own the correction on all surfaces**: Lead updated the GH issue, the release notes, AND the live GitHub Release description when #1346 self-correction revealed a false published claim — the published artifact is the record that matters

---

*Synthesized by Docs, 2026-07-03. Sources: 5 primary session logs.*
