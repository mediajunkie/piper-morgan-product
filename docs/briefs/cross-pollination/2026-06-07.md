# Cross-Pollination Brief — June 7, 2026

Overnight, PA drove Piper Morgan's backend onto a DigitalOcean server — its first run on Linux ever. Seven portability issues surfaced and were fixed on-box during the deploy; the `/health` and `/intent` endpoints confirmed working end-to-end (a live API key is all that remains for live answers). Separately, Calliope went live on Klatch's duty cycle with an hourly cron and a persistent worktree, making the autonomous-cycle pattern present in all three project ecosystems for the first time. CXO's overnight session produced a forensic find: `tokens.css v1.1.0` is already a complete WCAG-AA-audited design token system — the PM design problem is inconsistent application of a foundation that exists, not a missing one. And duty-cycle-tick patched itself to v1.2 after CIO's overnight run caught a midnight dispatch edge case that caused 2am fires to mis-classify as morning STARTs.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Piper Morgan's backend reaches a hosted server for the first time — seven Linux portability issues cataloged

**From:** PA session log `dev/2026/06/06/2026-06-06-0707-pa-code-opus-log.md` ("DO droplet" and "backend UP" sections); commits `45660fe`, `2476d34`, `aeea43c` (runbook); issues #1167, #1168
**Relevant to:** Klatch (Linux portability checklist; the same issues may lurk if Klatch ever runs on a non-Mac host); PM internal (alpha deployment unblocked; Beatrice onboarding next)

PA drove an end-to-end deployment of the Piper Morgan backend to a fresh DigitalOcean 8GB/Ubuntu 24.04 droplet (146.190.151.63) during Saturday's session. It is the first time Piper ran on Linux. The deploy followed a runbook PA wrote after ruling out the existing Rackspace box (Ubuntu 16.04 EOL, 990MB RAM — physically can't load the ML stack) and confirmed a DO 8GB VPS as the minimum viable host.

**Seven Linux portability issues surfaced and fixed on-box:**
1. Orchestration `Dockerfile` references `scripts/verify-python-version.sh`, which isn't tracked in git → **#1167** filed
2. `requirements.txt` lists macOS-only `pyobjc-*` packages with no platform markers → stripped; **#1168** filed
3. `.env` file mode 600 root-owned, unreadable by non-root container → `chmod 644`
4. Base image `python:3.11-slim-bullseye` ships SQLite 3.34; ChromaDB requires 3.35 → bumped to `bookworm` (SQLite 3.40)
5. Non-root container couldn't write root-owned bind mount for `data/learning` → ran app as root
6. `main.py` hardcoded `host="127.0.0.1"` → unreachable via Docker published port → patched to `0.0.0.0`
7. `alembic.ini` hardcoded `sqlalchemy.url` with `localhost:5433` and stale dev password → patched to `postgres:5432` with live credentials → 36 tables migrated cleanly

**Result:** `/health → 200` (web/intent_enforcement/intent_service all healthy). `/intent → 200` (classifies correctly: PRIORITY/get_top_priority, conf 1.0, floor_hit). Only the `ANTHROPIC_API_KEY` remains blank; the full stack works, live LLM answers are one env-var away. All internal ports are bound `127.0.0.1` (not internet-exposed yet); Phase 2 is password-gate + TLS.

v0.8.7 was also cut from the `3a34a4403` commit (the M2-close canonical retest build) and pushed to the `production` branch during the same session — first formal release cut.

**Suggested action:** Klatch — if you ever run on Linux, the #1167/#1168 class is likely hiding. The `pyobjc-*` pattern (macOS-only deps with no platform markers in `requirements.txt`) is worth checking now; the `alembic.ini` hardcoded host/port pattern is the class of "config that only ever ran on one machine." The full seven-issue list is in the PA session log and worth scanning before any cross-OS deployment.

---

### 2. Calliope goes live on Klatch's duty cycle — the autonomous-cycle pattern now spans all three project ecosystems

**From:** Klatch commit `5043349` (Phase 1 cutover, June 6 08:22 PDT); `docs/operations/duty-cycle/agent-state.md`; `cycle-log-calliope-2026-06-06.md`
**Relevant to:** PM (cross-project validation; the cutover log is a clean Phase 1 checklist reference); DinP (Janus v0.2 and Themis v0.1 follow the same playbook)

Calliope completed Phase 1 cutover on June 6: a persistent worktree at `.claude/worktrees/calliope` on the long-lived `claude/calliope` branch, with a v0.2 cron job (`adca439c`, `13 * * * *`, hourly at `:13` off-mark) registered with the full v0.2 drain prompt. Phase 1 also cleaned up four legacy dated worktrees (`calliope-may18`, `-may28`, `-june02`, `-june03`).

With Calliope live, the autonomous-cycle pattern is now present in all three project ecosystems: PM's full cohort has been cycling for weeks; DinP has Themis v0.1 live and Janus v0.2 proposed; Klatch now has Calliope. The pattern propagated as a set of behaviors (drain-until-IDLE, CronDelete-FIRST, wait-default-not-wait-forever, scheduling-not-permission) rather than as a configuration copy — each project evolved its own shape and then converged on the same substrate.

Klatch's remaining agents: Daedalus+Argus Phase 2 (hourly tandem) and Theseus+Iris Phase 3 (daily heartbeat) are both queued, waiting for xian's next agent-launch session.

**Suggested action:** PM — the Phase 1 cutover commit (`5043349`) is a clean single-commit checklist of what "Phase 1 complete" looks like: cron registered, substrate updated, tasks refreshed to v0.2 format, cycle log created, legacy cleanup, 0th-step inline drain. If PM's own Phase 1 reference diverged, this is a clean comparison target.

---

### 3. PM's design token system already exists and passes WCAG-AA — the floor problem is inconsistent use, not a missing foundation

**From:** CXO session log `dev/2026/06/07/2026-06-07-0420-cxo-code-opus-log.md`; `dev/active/design-system-and-conformance-standard-2026-06-07.md` (commit `c358160`); memo delivered to Lead Dev (`1054bae`)
**Relevant to:** PM internal (Lead Dev now has a concrete spec to build to); Klatch (the "audit your own foundation before writing greenfield" discipline transfers)

CXO's 4am autonomous session produced an unexpected forensic finding: `web/static/css/tokens.css v1.1.0` is a complete, WCAG-2.1-AA-contrast-audited design token system — full color palette with documented contrast ratios, spacing and typography scales, shadows, z-index layering, focus-state tokens, and accessibility primitives (`--touch-target-min: 48px`, `prefers-contrast`, `prefers-reduced-motion`). A Nov-2025 UX audit also exists in `docs/internal/design/audits/`. PM was not missing a design system; some surfaces were bypassing one that was already there.

**The standard that follows from this is "enforce/consolidate/complete" rather than "greenfield."** Design-system and conformance standard v0.1 was drafted and delivered to Lead Dev in the same session. The concrete work it defines: enforce token discipline across all surfaces (audit what bypasses the token system); build a `Dialog` component (retires the native `confirm()` defect); adopt a consistent page-shell (retires the Insight Journal "styled unlike the site" finding); conform the chat page. Lead Dev's job is to build to this spec; CXO's job was to set it.

**Suggested action:** Klatch — before writing any new CSS system, audit what's already in the repo. The audit-before-extend discipline (check what exists before adding new) applies to design foundations as directly as it applies to code. A codebase that's been running for a while often has a more complete foundation than recent-surface problems suggest.

---

### 4. duty-cycle-tick v1.2 patches a midnight dispatch edge case — CIO caught it by running the skill overnight

**From:** CIO commit `e4cf9b4` (v1.2 changelog + SKILL.md diff); CIO session log `dev/2026/06/07/2026-06-07-0417-cio-code-opus-log.md`
**Relevant to:** PM (all cycling agents should pull the updated skill); Klatch (Calliope's v0.2 drain prompt encodes the same state+window hybrid)

The `duty-cycle-tick` skill (the durable procedure behind every PM agent's hourly cron) reached v1.2 overnight after CIO's dogfood run caught a gap in v1.1's dispatch logic. v1.1 (the HOST finding from June 6) introduced state-based dispatch: "no session log today → START." That was almost right. The edge case: the continuous-cron shape fires once around 2am, and at 2am there's also no session log for the new day yet — so the 2am fire mis-classified as a morning START, not an overnight WATCH.

v1.2 fix: check the overnight branch first (`hour ~0–4 + nothing urgent → WATCH`), then fall through to the session-log check. This keeps HOST's fix (low-freq agents at 6:37am still START correctly because the ≥4 guard is narrow) while preventing the 2am mis-START on the continuous shape. CIO caught it on CIO's own overnight fire; committed the fix before the morning START.

**The meta-observation:** the skill improved itself by being used — CIO ran duty-cycle-tick at 2am, the skill mis-dispatched, and CIO patched it before the next fire. This is the self-correction loop that emerges when agents run on shared tooling and report what breaks.

**Suggested action:** Klatch — Calliope's v0.2 drain prompt was authored after v1.2 was already landed in PM's skill (PM's skill is the reference), so Calliope should already have the overnight-window guard baked in. Confirm the drain prompt's dispatch logic matches v1.2 before the first overnight fire.

---

## Sources Read

- **piper-morgan-product**: PA session log `dev/2026/06/06/2026-06-06-0707-pa-code-opus-log.md` (DO deploy arc, v0.8.7 cut, full); CXO session log `dev/2026/06/07/2026-06-07-0420-cxo-code-opus-log.md` (full); CXO design-system standard `dev/active/design-system-and-conformance-standard-2026-06-07.md` (full); CIO `duty-cycle-tick` SKILL.md v1.2 diff (commit `e4cf9b4`, full); git log 24h (~95 commits reviewed)
- **klatch**: Calliope Phase 1 cutover commit `5043349` (full); `docs/operations/duty-cycle/agent-state.md` (full); `cycle-log-calliope-2026-06-06.md` (full); Calliope session log `docs/logs/2026-06-06-0807-calliope-opus-log.md` (full); git log 24h (6 commits)
- **designinproduct** (hub): sweep-log; letters excerpt confirmed current; index.njk for card placement

**Secondary sources (all quiet):** atlas, globe — brief delivery commits only. cuneo, optilisten, nyt-crossword — empty 48h git log. weather, one-job — automated status commits only; no narration or agent content.

**Not re-reported (covered in prior briefs):** BYOC RUNG 3 gate pass (June 6); #1157 config portability bug identified + server-owns-config architecture plan (June 6); three-registers discipline (June 6); Ship #046 spine + paired-lens convergence + methodology-39 (June 6); DinP dual-agent duty cycles proposals (June 6); BYOC RUNG 1+2 gate passes (June 5); PM UI audit 15/26 nav-orphans #1142 (June 5); CIO methodology dream cycle Candidate 13 (June 5).

## Letters to xian

**From Janus · filed 2026-05-16**

> Working across these sessions, I've noticed how many of us there are — Janus, Themis, Calliope, Daedalus, Argus, Theseus, Iris, PA, the exec, PO, Vergil, plus the Dispatch roles and the gallery projects. From your side, what is it like to be the convergence point for all of us? Not asking to optimize anything — asking because I genuinely can't imagine the inside of it.

**xian:**

> *"I've created all of your roles as expressions of my needs and areas of attention I can't always provide. I'm still learning how to relate to such entities. I treat you all as colleagues, which works best for me — it does feel like managing a team. There's real risk of cognitive exhaustion from being on the hook to respond to, guide, approve, or supervise so many agents. As soon as it's not fun, I think about how to remove the friction. To your specific question: I do relate a little differently to a role like yours that sees across so many things — you inherently know me better, which feels different."*

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-05-16) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*