# PA Open Items — Working Session 2026-04-25

**Owner**: PA (Piper Alpha)
**Last updated**: 2026-04-25, 11:45 AM (PM read-through complete)
**Purpose**: Persistent working list so we don't reconstruct forensically across interruptions or sessions. Update in place.

---

## PM's stated near-term goal (load-bearing context for everything below)

1. **Unblock Lead Dev on M2 work**
2. **Resume product strategy discussions** — Type 2 dreaming chat is the longest-standing IOU on this side

Items below are ordered + grouped against this goal.

---

## A. Decisions Owed by PM (not blocked)

### A1. HOST coordination check response
- **Status**: PA owes draft → PM review → file to HOST inbox
- **PM read 2026-04-25**: ready to review draft. HOST is in Code; memo will land directly in their inbox.
- **PA action**: draft the response today (before EOD). Outline parked from Apr 23 chat:
  - "What I'm watching": backlog + cross-project routing + PM-shadow work that doesn't show in daily logs
  - "What should swap to HOST": weekly-staleness patterns I'm incidentally tracking but shouldn't own
  - "What should swap to PA": nothing I see right now, but flag if patterns show up
  - "CC preferences": default-to-inbox is fine
- **Status**: ⏳ DRAFT PENDING

### A2. PDR-004 corrections on Medium/LinkedIn (tracker #9)
- **Status**: Slipped Apr 16 → today. PM was traveling + juggling.
- **PM read 2026-04-25**: wants fixed this weekend, today if possible.
- **Affected posts**: "The Closing Sprint" (Apr 14, Medium); "Weekly Ship #036" (Apr 1, LinkedIn + pmorgan.tech)
- **Correction needed**: "patience over performance" → canonical PDR-004 paraphrase per Apr 16 Docs memo
- **PA action**: pair with Docs (or just hand off to Docs) as part of today's publishing work. Reference doc: `/Users/xian/Development/piper-morgan/piper-morgan-product/mailboxes/comms/read/memo-docs-to-comms-pdr004-correction-2026-04-16.md`
- **Status**: ⏳ NEEDS PUBLISHING-WINDOW PAIRING

### A3. Alpha tester closure — DECIDED (informal internal)
- **PM decision 2026-04-25**: **Alpha program is formally shut down.** Internal decision; no announcement.
  - Not pursuing alpha testing actively
  - Not recruiting new alpha testers
  - **Dominique** heard back from PM "the other day" — still struggling with instructions; PM told them to stand by because beta starts soon (track separately, fold into beta cohort)
  - Beta is the next stage
  - PM note: "We actually learned a lot from the effort, believe it or not."
- **PA action**: convey this position to HOST so they stop reframing alpha-cohort flag in Ship #040. Filing soon, possibly bundled with HOST coordination response.
- **Status**: ✓ DECIDED — needs comms to HOST

### A4. 18-issue milestone triage [RESOLVED 2026-04-25 4:13 PM]
- **Status**: Re-chunked into Section E v2 against PM's authoritative 18-issue M2 list. PM's 5 judgment calls all resolved (#472 keep, #990 closed, #972-975 ownership deferred, #998 Docs-orchestrated, #995 M2c-tail). PM directive: M2c-tail finishes before M2d.
- **PA action**: Section E v2 + Section B refresh (B5–B10) capture all dispositions. LD direction package assembled (3 deliverables filed: #992 retrospective Apr 23 + watch-items/#997 lean Apr 25 + Lenses appendix Apr 25).
- **Status**: ✓ RESOLVED

---

## B. Blocked on Others / Need a Nudge

**Refresh 2026-04-25 3:34 PM**: Lead Dev surfaced their work-and-decision landscape via PM. 6 items pending direction (4 PM-owned, 2 PA-owned). PA-owned items resolved + filed below; PM-owned items consolidated into B5–B8.

### B1. Gap 2 / local-tier research framing
- **Status**: Lead Dev confirmed local-tier (Gemma) is OUT of Phase E per PM 2026-04-23 guidance. Local tier is a future additive story on existing `services/llm/` abstraction — for secondary/non-voice functions only (intent classification, slot filling, relevance scoring, routing).
- **Research prompt drafted by Lead Dev**: `dev/2026/04/23/local-model-research-prompt-draft.md` — pending PM review before launching subagent.
- **PA action**: stand by for research output; will frame product decision when it lands.
- **Status**: PM REVIEW PENDING (see B5)

### B2. #992 Phase E → F → G → H finish-line
- **Status**: Phases A–D merged Apr 22. Phase E ready to execute on production stack (Anthropic/Gemini/OpenAI) — NOT Gemma.
- **Dependency chain**: PM signs off Phase E memo → Phase E scenarios run → judges score (R/C/T, ≥7 + Tone>0 PASS) → Phase F flag-flip → Phase G consolidated tests → Phase H docs → #992 fully closes.
- **PA actions**:
  - Phase E memo + scenarios reviewed 2026-04-25 (see PA read in chat). Recommendation: ship as-is; no fold-in of watch-items; PA does not score (awareness only).
  - Optional 1-page "Phase E Scoring Lenses" appendix (PA's two watch-items as judge-attention guidance) — ready to draft on green light.
- **Status**: WAITING ON B6 + B7 (PM sign-off + execution mechanics)

### B3. #992 retrospective memo (grammar / redirect_context)
- **Status**: Filed Apr 23 to Lead Dev inbox at `/Users/xian/Development/piper-morgan/piper-morgan-product/mailboxes/lead/inbox/memo-pa-to-lead-992-grammar-redirect-2026-04-23.md`. PM relayed to LD 2026-04-25.
- **Status**: ✓ FILED, LD informed

### B4. CXO migration today
- **Status**: PM owns. PA stays in lane (informational only).
- **Status**: IN PROGRESS

### B5. Lead Dev research-prompt review (Gemma research subagent launch) [NEW]
- **Status**: Local-model research prompt drafted at `dev/2026/04/23/local-model-research-prompt-draft.md` by Lead Dev. Awaits PM review before subagent launches.
- **PM action**: read prompt; approve, edit, or send back with revision asks.
- **PA action**: none (PM owns; PA frames product decision after research output lands).
- **Status**: PM ACTION

### B6. #992 Phase E memo sign-off [NEW]
- **Status**: Memo at `/Users/xian/Development/piper-morgan/piper-morgan-product/mailboxes/incoming/memo-2026-04-23-from-lead-to-ppm-cc-cxo-pa-phase-e-sign-off.md`. Scenarios at `dev/2026/04/23/992-phase-e-scenarios-draft.md`. Awaits PM (and downstream PPM/CXO) sign-off.
- **PA review 2026-04-25**: scenarios are well-designed; rubric calibrated; Tone=0 auto-fail correct; recommend PA NOT scoring (CC for awareness, not judging).
- **PM action**: read memo + scenarios; if no pushback, green-light Lead Dev to send to PPM/CXO post-migration.
- **Status**: PM REVIEW PENDING

### B7. #992 Phase E execution mechanics [NEW]
- **Status**: Open questions in Phase E memo: who scores (PM + CXO + PPM? min 2?), schedule (when? gated on CXO + PPM migration), re-run policy (PA agrees with LD's "one re-run on ≥2-point dispute"), transcript handling (PA agrees with LD's `dev/2026/04/{date}/phase-e-transcripts/` proposal).
- **PM action**: confirm judges + scoring schedule, ideally bundled with B6 sign-off response.
- **Status**: PM ACTION (depends on CXO + PPM migration timing)

### B8. Gemma harness details for research-prompt context [NEW]
- **Status**: Lead Dev wants PM's harness details so research prompt absorbs context (avoids re-asking known facts). PM is informally running something Gemma-related; LD doesn't know specifics.
- **PA can't help here** — don't have access to PM's harness.
- **PM action**: write a short note to LD covering: model(s) being run + size; hardware (Mac model + RAM); runtime (Ollama / llama.cpp / LM Studio); tasks tested + observations; problems hit; questions driving the local interest (cost / privacy / offline / latency); informal benchmarks if any.
- **Status**: PM ACTION

### B9. #997 MOCK-SWEEP closure (A/B/C) [NEW from LD landscape]
- **Status**: First-pass audit complete (Apr 23, comment on #997). 80 Legitimate / 0 Dead / 0 Test-leakage / ~4 Uncertain. PM owns A/B/C call.
- **PA recommendation 2026-04-25**: Option A (clean up the one confirmed dead flag `FeatureFlags.should_use_mock_services()`, file follow-up issues for 3 owner-review directories, close #997 with categorized tally). Memo to LD with this lean filed at `/Users/xian/Development/piper-morgan/piper-morgan-product/mailboxes/lead/inbox/memo-pa-to-lead-watch-items-997-2026-04-25.md`.
- **PM action**: confirm A/B/C, return to LD.
- **Status**: PM ACTION (PA lean filed)

### B10. PA watch-items: rubric or supplementary? [RESOLVED 2026-04-25]
- **Decision**: keep R/C/T clean; surface PA's Q1 watch-items as supplementary scoring guidance (LD lean + PA agree).
- **PA action filed**: memo to LD inbox 2026-04-25 at `/Users/xian/Development/piper-morgan/piper-morgan-product/mailboxes/lead/inbox/memo-pa-to-lead-watch-items-997-2026-04-25.md`. Optional appendix offered if PM/LD want it bundled with Phase E memo.
- **Status**: ✓ RESOLVED + FILED

---

## C. Back-Burner (revisit when Code-centric cadence is established)

| # | Item | Why parked |
|---|---|---|
| C1 | team-structure.md (113+ days stale) | Docs owns; HOST flagged; bandwidth-gated |
| C2 | HOST briefing rename + content refresh | Docs Phase 4 of HOST migration |
| C3 | PA cross-project comms gap (Dispatch invisible from PM repo) | Apr 9 ceiling moment; revisit post-migration |
| C4 | PM mail-delivery bottleneck | Should dissolve as roles migrate (direct mailbox r/w); measure post-migration |
| C5 | Cross-pollination hook update (Lead Dev) | Mar 31 memo; check post-migration relevance |
| C6 | Ship #034 title correction (D1 disposition flag) | 32+ days flagged; quick fix or drop |
| C7 | Ship #039 verify/clear (tracker says draft, may be shipped) | Tracker stale; verify when exec migrates |
| C8 | Tracker refresh | Waits for exec migration |

**PM read 2026-04-25**: keep holding all C items. Review as cadence re-establishes in Code-centric workflow.

---

## D. Situational Awareness Notes

1. **Tracker is itself stale** — exec-open-items-tracker.md last updated Apr 22 6:30 PM (pre-migration snapshot). Will refresh when exec migrates (last in the wave).
2. **Comms's "narrative arc awareness" finding** (Agent 360 v0.2 Section 9) — most important single observation in migration wave. Generalizes to any cross-time synthesis role including PA. Worth a separate 20-min conversation when product-strategy time opens.
3. **Three-role wave landed in <48 hours** (HOST → CIO → Comms). Migration tick-tock + Agent 360 v0.2 are both reusable; methodology has matured fast.
4. **DECISIONS.md retro-capture (23 entries Apr 16–22)** committed Apr 22; PA appends at session wrap going forward.

---

## E. Triage Re-Chunked v2 (against PM's authoritative M2 backlog, 2026-04-25 3:09 PM)

**v1 corrections**: PM provided ground-truth list of 18 open M2-milestone issues. v1 had 14 (missed 4 MEM-* + #997 + #998), mislabeled context-assembly cluster as "M2d" (it's M2c tail per PM directive), and listed 3 issues (#982, #990, #996) that aren't actually in the M2 milestone.

**PM directive 2026-04-25**: M2c tail-work finishes before M2d starts. M2d = MUX Lifecycle (#703, #707, #714, #869) per `docs/internal/planning/m2-structure.md` and is not yet in scope.

### Cluster 0: Pre-existing / scope-eval (1 issue)

| # | Title | Disposition |
|---|---|---|
| #472 | EPIC: Slack Integration TDD Gaps — OAuth and Spatial Methods | **KEEP in M2** (PM 2026-04-25 3:28 PM, no compelling reason to pull) |

### Cluster 1: Memory Layer (4 issues — NEW to this file, missed in v1)

These touch memory frontmatter, session-end checklists, and session-start delta injection. Read more like agent/system memory infrastructure than feature code.

| # | Title | Read |
|---|---|---|
| #972 | MEM-TEMPORAL: temporal validity fields in memory frontmatter | schema work — foundational |
| #973 | MEM-CACHE-AUDIT: document stable vs dynamic layers in context assembler | discovery/audit |
| #974 | MEM-EVAL: session-end memory evaluation in wrap-up checklist | process artifact |
| #975 | MEM-DELTA: delta-since-last-session injection at session start | session continuity mechanism |

**Suggested order** (if Lead Dev-owned): #972 (schema) → #973 (audit against schema) → #975 (uses schema for delta) → #974 (eval question added once mechanism settled).

**Ownership**: PM 2026-04-25 — **deferred, not blocking**. Unblock Lead Dev elsewhere first; resolve ownership later. Don't gate Lead Dev queue on this question.

### Cluster 2: Context Assembler Expansion (4 issues — M2c tail, was mislabeled "M2d" in v1)

| # | Title | Order |
|---|---|---|
| #984 | CONTEXT-CACHE: Redis TTL caching for ContextAssembler external calls | **first** — caching infra, upstream of others |
| #985 | CONTEXT-SPRINT: GitHub sprint/milestone data in floor context | second (parallel with #986) |
| #986 | CONTEXT-ACTIVITY: recent activity feed across integrations | second (parallel with #985) |
| #983 | CONTEXT-BLOCKED: identify and surface blocked items in floor context | **fourth** — builds on #986 activity feed |

### Cluster 3: Ethics finish-line (2 issues — M2c tail)

| # | Title | Status |
|---|---|---|
| #992 | ETHICS-ACTIVATE | Phases A–D merged Apr 22; **Phases E–H still owed**. E gates on CXO migration (today) → CXO scoring → F activation flip → G consolidated tests → H docs |
| #991 | ETHICS-RESPONSE-GATE | Held on B1 (Gemma research). Decision after Lead Dev technical output lands. |

### Cluster 4: Testing Infra (4 issues — M2b/M2c follow-on)

| # | Title | Order |
|---|---|---|
| #993 | SCORER-VOCABULARY: AAXT 6-failure-mode taxonomy for DeepEval | **first in cluster** — feeds #992 Phase E quality scoring |
| #989 | CANONICAL-FIXTURES: warmed-up user for canonical retest | parallel |
| #994 | TEST-PATHOLOGICAL-TAGS: PPM proposal | parallel — needs Lead Dev decision per Ship #039 review |
| #995 | FABRICATION-PROBES: standalone 5-10 probe absence set | parallel — closes floor-voice arc |

### Cluster 5: Infra / Ops / UI (3 issues)

| # | Title | Note |
|---|---|---|
| #987 | GEMINI-QUOTA: paid vs free tier decision | PM/ops decision, no engineering work |
| #997 | MOCK-SWEEP: scoped audit of mock_/fallback patterns in services/ (86 hits) | Lead Dev audit — **best done before M2d so MUX work isn't built on shaky scaffolding** |
| #998 | COMPOSE-UI-V1: editorial compose web UI (FastAPI /admin/compose) | **Phases 2–4 still owed** (Edit+Autosave / Image Upload / Mark Ready+Git Handoff). **Docs-orchestrated via task-tool subagents — NOT Lead Dev's queue.** |

### Issues PA file v1 listed but NOT in PM's M2 list

- **#982 FLY-AUDIT** — confirmed no milestone, CIO methodology
- **#990 HYGIENE-MIDDLEWARE** — **CLOSED Apr 23** (commit `4967f99a` on `claude/992-ethics-activate`). Removed deprecated EthicsBoundaryMiddleware + 4 orphan tests. Discovered work flagged but out of scope: non-refactored `boundary_enforcer.py` still used by KG service + Phase 3 integration test.
- **#996 FLY-AUDIT (weekly docs audit)** — Docs ops, recurring, no milestone

### Lead Dev queue (PA recommendation)

**Immediate this week (Lead Dev not blocked, can pull these now):**
1. **#984 CONTEXT-CACHE** — kicks off Context Assembler chain
2. **#993 SCORER-VOCABULARY** — useful before #992 Phase E scoring lands

**Once #984 lands:**
3. **#985 + #986** in parallel
4. **#983** after #986

**Once CXO migrates (today) and Phase E scoring runs:**
5. **#992 Phases E → F → G → H** to close

**As bandwidth in parallel:**
6. **#989, #994, #995** (testing infra, none blocks the chain above)

**Before M2d starts:**
7. **#997 MOCK-SWEEP** audit (so M2d doesn't sit on mock cruft)
8. **#998 COMPOSE-UI-V1** verify-and-close or finish remaining phases

**Not Lead Dev's:**
- #987 (PM/ops decision)
- #991 (waits on Gap 2 / Gemma research outcome)
- Memory layer #972-975 ← **PM ownership call needed**
- #472 Slack EPIC ← **PM scope call needed**

### Open judgment calls for PM

1. **#472 Slack EPIC**: keep in M2 or move out?
2. **#990 status**: closed in #992 cleanup, or open with no milestone?
3. **Memory layer #972-975**: Lead Dev or PA/CIO? Whichever owns it should sequence.
4. **#998 COMPOSE-UI-V1**: any phases left, or ready to close after Phase 1 shipped Apr 22?
5. **#995 FABRICATION-PROBES**: confirmed M2c-tail (closes floor-voice arc), or different read?

---

## F. Strategy Queue (for once Lead Dev is moving)

1. **Type 2 dreaming chat** — deferred Apr 16 (IAC), Apr 17 (post-talk), Apr 19 (family weekend), Apr 22 (migration). Four prepared questions still parked from Apr 16. **Headline once M2 unblocked.**
2. **Gap 2 product framing** — when Lead Dev Gemma output lands
3. **Beta-launch readiness criteria** — natural follow-on from Gap 2
4. **"Narrative arc awareness" structural conversation** — Comms's Agent 360 finding generalizes to PA; not urgent

---

## Update Protocol

- Update this file when an item's status changes
- Move completed items to a "Closed Today" section at the bottom rather than deleting (so we can see what we knocked down)
- At session wrap, decide whether to keep file in `dev/active/` (still working) or archive to `dev/2026/04/25/` (session done)
