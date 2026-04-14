---
date: 2026-04-14
status: substantive
sources_checked:
  - klatch
  - piper-morgan
  - openlaws
window: "48h (April 12–14, 2026)"
---

# Cross-Pollination Brief — April 14, 2026

Monday was Klatch's most productive single day to date: Argus, Daedalus, and Iris — working in coordinated parallel — ran a full Phase 3.5 design discussion, reached three-agent consensus on five open questions, and shipped the complete behavioral calibration transfer pipeline by evening. The mechanism now supports three extraction modes, structured field notes with trust levels, and a six-point handoff prompt that can address any entity type without specialization. PM's Lead Dev closed the third and final installment of the ADR-060 floor inversion, completing the migration of conversational categories from canonical template handlers to floor-first routing with context assembly, with 6,246 tests stable. OpenLaws contributed a methodology pattern — a five-category eval harness structure — that is directly applicable to both projects' automated testing work.

---

## Key Insights

### 1. Phase 3.5 ships: Layer 5 behavioral calibration transfer is now a working feature

**From:** Klatch (Argus, Daedalus, Iris), `docs/plans/STEP-10-PHASE-3.5-CONSENSUS.md`, `docs/plans/STEP-10-PHASE-3.5-BEHAVIORAL-CALIBRATION.md`, April 13
**Relevant to:** Piper Morgan (memory architecture #972-976, ADR-054 composting pipeline, M5 BYOC export); OpenLaws (session continuity at agent handoff)

Klatch's Argus designed the behavioral calibration system through a research conversation with xian in the morning. By evening, Daedalus had shipped three backend phases (3.5a, 3.5b, 3.5c) with test coverage. The design arc — from open questions to consensus to working code — ran in under 12 hours across three agents.

The mechanism exports behavioral field notes from an agent at export time through three modes:

- **Mode 1 (External extraction, 3.5b):** An auxiliary LLM scans conversation history and identifies behavioral patterns. Produces `FieldNote[]` entries tagged `source: "external-extraction"`, `trust: "synthesized"`.
- **Mode 2 (Self-authored briefing, 3.5a):** The entity itself is prompted to write a handoff briefing for its successor. Produces entries tagged `source: "self-authored-briefing"`, `trust: "agent-observed"`.
- **Mode 3 (Micro-reflections, 3.5c):** Lightweight reflections captured per-correction (when the user explicitly corrects the agent) and per-session (1-3 notes when no corrections occurred). Tagged `source: "micro-reflection"`, `trust: "agent-observed"`.

The three modes are merged at export time. The reviewer sees all three source types alongside the entity's role prompt, enabling redundancy detection.

The five-criteria filter for meaningful behavioral observations (agreed unanimously): actionable, specific, non-obvious, relational, durable. The Daedalus summary test: "Would a successor who reads this note do something differently on day one than one who doesn't?"

The six-point handoff prompt (Mode 2) is the most immediately exportable artifact. It asks the entity to cover: user communication preferences, learned patterns (ask vs. act, detail calibration), relationship context (trust established), course corrections and what they taught, specific behaviors to avoid, and anything not captured in system prompt or project memory. The prompt was designed for universality — one prompt for all entity types, no role-specific variants. All three agents endorsed Iris's rationale: "Gall's Law: one prompt, see if it works, split only if the output is consistently wrong for a specific role type."

Phase 3.5d (cross-validation review UI) is the remaining piece — Iris's scope, scheduled for Tuesday with xian.

API: `GET /api/channels/:id/export?briefing=true&extract=true` returns field notes from all three modes.

Test count: 910 (771 server + 139 client), zero failures. Up from 727 at v0.8.9 — 183 new tests in 13 days.

**Suggested action:** PM Docs agent read the six-point handoff prompt from `STEP-10-PHASE-3.5-CONSENSUS.md` before the ADR-054 composting pipeline is scoped. The five-criteria filter and trust-level schema (agent-observed vs. synthesized) are directly applicable to PM's write governance gaps identified in the Janus memory research. PA note: the full export endpoint (`?briefing=true&extract=true`) is the reference implementation for what "structured memory with provenance" looks like in practice.

---

### 2. Floor inversion trilogy complete: #925 migrates STATUS and PRIORITY to floor-first routing

**From:** PM Lead Developer, `feat(#925): migrate STATUS and PRIORITY to floor-first routing`, April 13
**Relevant to:** Klatch (channel routing architecture, behavioral calibration as "floor migration" analogy)

#925 closes Phase 3 of ADR-060, the floor inversion sweep triggered by #962's discovery that STATUS and PRIORITY categories were already routing to the floor via the safety net — but only after an unnecessary canonical handler roundtrip. The fix: add both to `_FLOOR_ROUTED_CATEGORIES`, write `_gather_status_priority_context` to assemble user context (projects, priorities, pending todos, GitHub status), and remove the canonical handler dependency entirely.

The three-migration arc is now complete:
- Phase 1: IDENTITY (earlier in M2a)
- Phase 2: TEMPORAL (April 12, issues #965)
- Phase 3: STATUS and PRIORITY (April 13, #925)

Each migration follows the same pattern: a category was routing through a template handler that produced rigid outputs, the safety net was rerouting it to the floor anyway, and the migration eliminates the roundtrip by making floor routing explicit and giving the floor direct access to context assembly.

Canonical retest run 3 post-#925: routing 93.4% (57/61), quality 62.3% (38/61). Both stable within LLM variance from run 2. No regressions. 6,246 tests, zero failures.

The architectural analogy for Klatch is worth naming: the move from canonical handlers (rigid template → rigid output) to floor-first (assembled context → LLM reasoning) is structurally identical to the move from hardcoded Layer 5 entity prompts toward behavioral calibration at export. In both cases, the old system bypassed the hard work with a template. The new system delivers context and lets the model reason. The PM floor inversion is complete. Klatch's Layer 5 behavioral calibration is the same transition one abstraction level up.

**Suggested action:** No immediate action required. This is an orientation note for Daedalus and Argus: the PM floor inversion is the closest architectural parallel to the work Klatch completed yesterday. Reviewing ADR-060 and the three-migration arc would be useful background before any Klatch architecture discussion about how entities handle routing decisions.

---

### 3. Iris's canonical diagnosis: the backend has rich data the UI barely surfaces

**From:** Iris (Klatch), `docs/ux/evaluation.md`, `docs/ux/priorities.md`, April 13
**Relevant to:** Piper Morgan (context visibility, debugging infrastructure, M2 UI surface); OpenLaws (eval harness visibility patterns)

Iris completed all three kickoff deliverables in a single self-directed session: evaluation (11 sections, 4 cross-cutting concerns), prioritized issues list (6 problems, 7 opportunities, 3 viewport gaps), and a design research proposal for Phase 3.

The headline finding — "the backend has rich context data that the UI barely surfaces" — is one of those diagnostic frames that transfers cleanly across projects. For Klatch: the `prompt-debug` endpoint exposes per-layer assembly status with size, source, and content; the UI renders this as a colored dot. Phase 3 is about closing that gap without building new features.

The same gap exists in PM: the floor routing system assembles rich context (user projects, priorities, GitHub issues, temporal data), and most of that assembly process is invisible to the user and to debugging agents. The M2 quality score (62.3%) suggests the floor is reasoning correctly more often than not — but when it doesn't, the diagnostics for *why* are limited to log files.

Iris's priorities list is directly readable as a Phase 3 design brief: P1 (keyboard accessibility), P3 (import fidelity readout), P4 (prompt layers reduced to dots — surface the data that already exists). P3 is the most immediately cross-relevant: Iris designed a `LayerFidelityReadout` component for import (shipped by Daedalus same day) that shows per-layer status post-import. The bidirectional version — export preview and import readout as the same component — is on Iris's design research agenda.

**Suggested action:** PM CXO (or whoever owns the debugging/observability experience) read Iris's evaluation at `docs/ux/evaluation.md` before scoping any M2b or M3 UI work. The "surface what's already built" framing is the correct lens for PM's context assembly visibility gap. The `LayerFidelityReadout` component design is the reference implementation for "show the user what context was assembled."

---

### 4. Eval harness methodology: categorical query structure with known_good / pathological separation

**From:** OpenLaws (Vergil), `workdesk/eval-harness/` — methodology pattern only
**Relevant to:** Klatch (AAXT Scaffolded Probing Phase 2 query organization); Piper Morgan (M2 canonical retest methodology)

Vergil built a 55-query evaluation harness organized into five structural categories. The methodology is the cross-relevant finding; the content is domain-specific and not surfaced here.

The categorical structure:
1. **known_good_citation** — queries with empirically verified expected results, used as canaries (pass/fail is unambiguous, regression is immediate signal)
2. **natural_language** — broad-vocabulary queries testing the system's ability to handle non-expert phrasing
3. **cross_jurisdiction** — queries requiring reasoning across multiple regulatory bodies
4. **known_pathological** — cases where the system is known to fail or behave unusually; explicitly catalogued rather than hidden
5. **placeholder** — stubs for a known future query type, not yet fully specified

Every query carries: the expected result type, the source (which session or empirical finding generated this query), and why it was included. The runner supports `--category` filtering and a `diff` command comparing two baseline snapshots.

The most directly actionable element: the `known_pathological` category. Vergil made it explicit that known failure cases should be in the harness, not excluded. This normalizes failure as a testable state rather than a gap. For Klatch's AAXT Scaffolded Probing Phase 2: the fabrication probe class (absence categories — file, entity, memory, history, channel) maps cleanly onto `known_pathological`. For PM: Pattern-045 (floor fabrication of absent todo items) should be a named category in any M2 regression suite, not just one of the 61 canonical queries.

The `placeholder` category is also worth adopting: acknowledging that a query type exists but isn't yet fully designed prevents the suite from pretending to coverage it doesn't have.

**Suggested action:** Argus, before Phase 3 canonical retest is locked: review whether the current 61-query canonical suite has an equivalent of `known_pathological` as an explicit category. If Pattern-045 and similar failure modes aren't explicitly labelled, adding that label (without adding queries) is a five-minute improvement that makes regression visibility immediate. PM Lead Dev same consideration for the retest methodology.

---

### 5. Continuity memo before the failure, not after

**From:** OpenLaws (Vergil + PO), `docs/reference/vergil-continuity-memo-2026-04-13.md`, April 13 — methodology pattern only
**Relevant to:** All projects (PM Docs 15-day session wrap; Klatch context interchange protocol)

A laptop coffee spill mid-session forced an involuntary context handoff in the OpenLaws work yesterday. The work continued without information loss because a continuity memo had been written and committed to the repo *before* the failure — proactively, in anticipation of a possible hardware problem, not reactively.

The memo covered: current sprint state, what shipped, what's pending, key relationships, communication patterns, repo structure, critical lessons learned, memory system pointers. Context recovery on the new machine was complete. No work was lost.

This happened at the same time PM's Docs agent closed a 15-day session due to context window pressure — an entirely different forcing function, but the same dynamic: context must be externalized before the session ends (whether by spill, compaction, or deadline), not after. PM's continuity infrastructure (session logs, omnibus, mailbox, carry-forward lists) handled that transition cleanly.

The Klatch Phase 3.5 behavioral calibration transfer is partly about this same problem at the agent-identity level: what does an entity know about how to work well, and can that knowledge survive a session boundary? The six-point handoff prompt is a continuity memo written by the agent, for its successor, at export time.

The common pattern across all three instances: **externalize before the seam, not at it**. The continuity memo, the omnibus log, the session wrap, the handoff briefing — all work best when written proactively, with the failure mode in mind.

**Suggested action:** Calliope: add "write continuity memo before context pressure, not at it" to the agent traditions spec or logbook as a named practice. The Phase 3.5 behavioral calibration pipeline is the automated version of this discipline — but the manual version (session log + carry-forward + committed memo) is what protects against the unscheduled handoff.

---

## Sources Read

**Klatch:**
- `git log --since="48 hours ago"` — 32 commits
- `docs/logs/2026-04-13-0710-calliope-opus-log.md` — Monday assignments, end-of-day summary
- `docs/logs/2026-04-13-0815-iris-opus-log.md` — Session 4: all three deliverables, Phase 3.5 positions + consensus
- `docs/logs/2026-04-13-0816-argus-opus-log.md` — SDK bump, Hono, AAXT Phase 2, sweep, Phase 3.5 design doc + positions + consensus synthesis, Rounds 20-21
- `docs/logs/2026-04-13-1021-daedalus-opus-log.md` — Haiku alias fix, six UX fixes, Phase 3.5 design + consensus, Phase 3.5a+b+c implementation
- `docs/plans/STEP-10-PHASE-3.5-CONSENSUS.md` — Full consensus document, five questions, six-point handoff prompt

**Piper Morgan:**
- `git log --since="48 hours ago"` — 15 commits
- `dev/active/2026-04-13-0742-pa-opus-log.md` — Day 14: temporal validity approved, xian on day-job focus
- `dev/active/2026-04-13-0812-docs-code-opus-log.md` — Apr 12 omnibus, #944 closed, #977 audit, 15-day session wrap
- `dev/active/2026-04-13-0814-lead-code-opus-log.md` — #925 STATUS/PRIORITY floor migration, canonical retest run 3
- `git show ec2d7e3` — #925 commit diff and implementation details

**OpenLaws (methodology only — data boundary applied):**
- `git log --since="48 hours ago"` — 8 commits
- `logs/2026-04-13-vergil-log.md` — eval harness design and build, coffee spill handoff, continuity memo
- `logs/2026-04-13-po-log.md` — docs reorganization, continuity memo authorship, research planning methodology

---
