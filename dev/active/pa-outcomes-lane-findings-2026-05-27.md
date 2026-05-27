---
from: PA (Piper Alpha)
to: CEO (xian)
cc: CIO (Chief Innovation Officer), Lead Developer
date: 2026-05-27
subject: Outcomes lane findings — paper-comparison against CT v2.3.1, UI Lifecycle Verification v0.1, multi-turn harness #1070; what migrates / composes / stays DIY (building on Lead Dev May 18 preview)
priority: standard — innovation-lane findings memo; feeds methodology-34 (CIO synthesis)
response-requested: at your cadence; CIO to absorb relevant material into methodology-34; Lead Dev for technical-shape flag-back if any verdict misreads the platform substrate
---

# Outcomes lane — PA paper-comparison findings

## TL;DR

- **Lead Dev's May 18 preliminary preview already covers the spec-read + audit-cascade comparison cleanly.** PA findings build on it rather than redo it. The four rubrics PA examined (CT v2.3.1, UI Lifecycle Verification v0.1, multi-turn harness #1070, plus a cross-check on audit-cascade) all share a structural pattern Outcomes maps to: dimensional scoring + threshold + verdict.
- **The mechanism layer migrates cleanly**. All four rubrics can be encoded as Outcomes rubric files (markdown per-criterion); the auto-provisioned grader replaces our same-agent-judges-its-own-output risk; max_iterations formalizes our implicit retry loops.
- **The discipline layer is the durable DIY value** — and it's substantial. Examples per rubric: CT's fresh-account-ceiling C=2 calibration, UI Lifecycle's Methodology-24 branch-or-anchor reasoning, multi-turn's judgment about which fixtures need follow_ups, audit-cascade's phase-boundary composition logic. None of these survive in the "rubric+grader+retry" primitive; all are how-to-use discipline that composes above.
- **One real friction at the artifact boundary**: Outcomes grades artifacts in `/mnt/session/outputs/` (file-based). CT v2.3.1 grades text responses; UI Lifecycle grades rendering. Migrating either means writing the response (or screenshot/HTML) to a file before grading — a small adapter layer, not a blocker.
- **Methodology-34 feed**: each of the four rubrics is a canonical worked example of a different shape of climb-up move. Suggest the synthesis lift them as a four-case taxonomy rather than treating Outcomes adoption as monolithic.

## What this memo IS / IS NOT

**IS**: PA's paper-comparison of Outcomes against PA-lane verification rubrics, building on Lead Dev's May 18 spec-read + audit-cascade case. Feeds CIO's methodology-34 synthesis with concrete instance material per the May 24 lane-assignment.

**IS NOT**: A migration plan (too early; no smoke test against Outcomes yet). Not a deprecation announcement for any rubric. Not gating any sprint work. Not pre-shaping methodology-34 (PM-hands-off framing per May 24).

## Paper-comparison per rubric

### 1. Colleague Test (CT v2.3.1) — `docs/internal/testing/colleague-test-rubric.md`

**Shape**: 3 dimensions (R/C/T) scored 0-3 each; PASS at ≥7/9 with no dimension at 0; MARGINAL 5-6; FAIL <5 or any zero.

**Used by**: M1 Gate UAT (#926), canonical query retest scorer (#928), Phase E ethics activation gate (#992), ongoing voice/quality monitoring.

| Element | DIY today | Outcomes maps how | Verdict |
|---|---|---|---|
| 3-dim per-criterion scoring | DeepEval LLM-as-judge with custom prompts | Markdown rubric with R/C/T sections, criterion bullets, score anchors | **Migrates cleanly** — format match is direct |
| Threshold logic (≥7/9 + no-zero) | Application-layer parsing of judge output | Returned as `explanation` text from grader; structured parsing above | **Migrates with caveat** — Outcomes returns text, not scored JSON; threshold logic stays in our parser |
| Iteration on FAIL | None today (single-pass scoring) | `max_iterations` retry loop with grader feedback fed to agent | **Adds a capability we don't have** — retry-on-fail could close some MARGINAL→PASS gaps automatically |
| Multi-corpus scoring (61-query canonical) | Loop over canonical-query corpus, scored individually | Either N Outcomes calls per query OR one call per corpus with composite rubric | **Migrates; design choice on granularity** |
| Fresh-account-ceiling C=2 calibration | Documented in rubric body; human/judge interprets | **DOES NOT migrate** — this is calibration discipline: "when the test session has no project context, the C-axis ceiling is 2, not 3, even if the response is appropriate" | **Stays DIY** — the calibration is the durable lens, not the mechanism |
| Anti-pattern detection in T-axis (template fingerprinting, chatbot warmth, content-filter cadence) | Embedded in rubric criteria + ongoing memory pins | Encodes in rubric text as anti-pattern bullets | **Migrates as rubric content; the *learning what to add* stays DIY** |
| The 2-vs-3 distinction (generic-LLM competence vs project-context-injection visible) | Rubric body explanation + cohort discipline of interpreting | Encodes in rubric criterion anchors | **Migrates as anchor text; the *calibration discipline* stays DIY** |

**Composes above Outcomes**: the canonical-retest corpus design (which 61 queries; which categories; which test fixtures); the fresh-account fixture decision (#989 CANONICAL-FIXTURES); the Run-N-comparison methodology (Run 5 vs Run 7 framing; what counts as a regression vs methodology-shift).

**Stays DIY**: the question itself ("Would a smart, capable PM colleague respond this way?"); the cohort calibration of what counts as "Piper voice" vs generic competence; the cross-version comparison discipline.

### 2. UI Lifecycle Verification Rubric v0.1 — `docs/internal/testing/ui-lifecycle-verification-rubric-v0.1.md`

**Shape**: 3 dimensions (R/C/T) scored 0-3 each; PASS at ≥7/9 with no zero (same auto-fail rule as CT). Derived from CT v2.3 with Methodology-24 (Branch-or-Anchor) branched dimension *meanings*: C is Clarity-of-UI-rendering (not Context-of-response).

**Used by**: M2d gate verification protocol step 2 (fresh-account walkthrough on rendering surface); ratified 3-way (Architect May 4 + Lead Dev May 5 + CXO May 10).

| Element | DIY today | Outcomes maps how | Verdict |
|---|---|---|---|
| Branched dimensional structure | Documented in rubric body with explicit Methodology-24 worked-example callout | Encodes as rubric criteria; the branching judgment doesn't appear in the rubric itself | **Migrates the rubric; the branching discipline stays DIY** |
| UI-rendering-scoped grading | Human evaluator on fresh-account walkthrough | Grader against screenshots or HTML artifacts written to `/mnt/session/outputs/` | **Migrates with friction** — artifact boundary requires capture step (screenshot/HTML) before grading; not a blocker, ~1 day of integration work |
| 3-way concurrence gate (Architect + Lead Dev + CXO) | Cohort-coordination via memo cycle | **DOES NOT migrate** — multi-agent ratification protocol is mailbox-shaped cohort coordination | **Stays DIY** — the ratification protocol is the moat-shaped discipline |
| Verdict thresholds (PASS/MARGINAL/FAIL) | Application-layer parsing | Same as CT — text `explanation` parsed above | **Migrates with caveat** — same as CT |
| Methodology-24 branch-or-anchor reasoning | Cohort decision discipline; embedded in rubric provenance | **DOES NOT migrate** — the "when to branch vs anchor a rubric dimension" judgment is methodology-corpus territory | **Stays DIY** — and this is the climb-up: methodology entry composes above the migration |

**Worth flagging to CXO/Architect**: if we migrate the rubric mechanism, the M2d gate verification protocol step 2 ("fresh-account walkthrough on the rendering surface, applying the UI Lifecycle Verification Rubric v0.1") would technically be automatable for the rubric-application phase, but the fresh-account fixture and the rendering capture remain manual. Net: maybe 50% of step-2 time saved; the human walkthrough still surfaces qualitative observations the rubric doesn't capture (the "what surprised me" lens).

**Composes above Outcomes**: cross-rubric coordination (when to branch vs anchor); Methodology-24 application beyond UI rubrics; multi-rubric consistency in fresh-account scoring vs project-context scoring.

**Stays DIY**: ratification protocol; per-rubric design decisions; the methodology-24 framework itself.

### 3. Multi-turn evaluation harness (#1070) — closed 2026-05-13

**Shape**: extension to canonical-retest fixture format adding `follow_ups: [...]` list per query; replay logic in retest script (`canonical-retest-run8.py`) reuses `session_id` per query for multi-turn flows; judge rubric extended via `JUDGE_SYSTEM_PROMPT_MULTITURN` calibrated to credit clarifying-question openers when later turns deliver substance.

**Used by**: Run 8-9 canonical retest (Q49 + Q149 + Q150 `/standup` multi-turn variants); future conversation-continuity + action-confirm flows.

| Element | DIY today | Outcomes maps how | Verdict |
|---|---|---|---|
| Multi-turn fixture format (`(num, query, category, routing, known_issue, follow_ups)` 6-tuple) | YAML/Python fixture in `canonical-query-test-matrix-v3.md` + retest script | Outcomes sessions are long-lived; multi-turn happens natively within a session | **Migrates + improves** — Outcomes' session shape is multi-turn-native; the fixture format simplifies |
| Session-id reuse across turns | Explicit in retest script | Implicit in Outcomes session lifetime | **Migrates cleanly** |
| Sequence-of-turns judging | `JUDGE_SYSTEM_PROMPT_MULTITURN` with cross-turn credit assignment | Grader sees the full session artifact; rubric criteria reference cross-turn behavior | **Migrates as rubric criterion design; the *calibration* of how to credit clarifying-openers stays DIY** |
| Discovery-via-methodology (Q49 surfaced #1079 `/standup` server-side bug as "useful discovery, not a fix-failure") | Lead Dev judgment + Phase 0 Risk #1 discipline | **DOES NOT migrate** — the "this rubric run discovered a bug elsewhere" pattern is cross-artifact recognition | **Stays DIY** — methodology-29 territory; recognizing the discovery is a cohort-discipline call |

**Composes above Outcomes**: which queries need multi-turn variants (`/standup`, conversation-continuity, action-confirm); cross-turn judging calibration; the "useful-discovery-not-fix-failure" framing for ACs that don't flip to `[x]` because of downstream bugs.

**Stays DIY**: the corpus design (which queries to add follow_ups for); the calibration of `JUDGE_SYSTEM_PROMPT_MULTITURN` shape; the Phase 0 Risk framework that lets discoveries land as discoveries rather than failures.

### 4. audit-cascade discipline — covered by Lead Dev May 18 preview

Lead Dev's May 18 paper-comparison (`mailboxes/exec/read/cc-memo-lead-to-cio-...-outcomes-lane-spec-read-plus-paper-comparison-findings-2026-05-18.md`) covers the audit-cascade case cleanly with the calendar-workdate-semantics audit as the worked example. PA's findings agree with Lead Dev's verdicts:

- Rubric encoding, grader, retry loop, output-file retrieval — **all migrate cleanly**
- Drift-narrative authorship, cross-agent transfer, Pattern-073 recognition, forward-looking-only resolution discipline, methodology-17 cross-validation, audit-cascade phase boundaries — **all stay DIY**

PA's only addition to Lead Dev's read: the **audit-cascade phase-boundary discipline is the structural-fix-instead-of-discipline-fix case** (PP-004 candidate per CIO's instance tracking). Each phase audit is a discrete Outcomes call; the cascade composition is the discipline that ensures audits happen between phases, not after. The discipline is what makes the cascade work; the per-phase grading is the migration-ready primitive.

## Cross-rubric synthesis (what feeds methodology-34)

The four rubrics line up as a **four-case taxonomy** of climb-up shapes. Each illustrates a different way the discipline-of-use can compose above the migration-ready mechanism:

1. **CT v2.3.1**: *calibration discipline*. The rubric mechanism migrates; the fresh-account-ceiling reasoning + 2-vs-3 distinction + Piper-voice-vs-generic-competence calibration stays DIY. **Climb-up shape**: methodology entries on "how to score what your platform can't see."
2. **UI Lifecycle Verification v0.1**: *cross-rubric coordination discipline*. The rubric mechanism migrates; the Methodology-24 branch-or-anchor reasoning + 3-way concurrence ratification stays DIY. **Climb-up shape**: methodology entries on "how to coordinate rubric families across surfaces."
3. **Multi-turn harness #1070**: *cross-turn judgment discipline*. The fixture mechanism migrates (and gets simpler); the corpus design + cross-turn credit calibration stays DIY. **Climb-up shape**: methodology entries on "what to test and how to credit it."
4. **audit-cascade**: *phase-boundary composition discipline*. Per-phase grading migrates; the cascade structure + Pattern-073 cross-artifact recognition stays DIY. **Climb-up shape**: methodology entries on "how to compose verifications across phases."

**The taxonomy itself is methodology-34 feed material**: cohort-discipline-as-moat isn't a single homogeneous thing. It's at least four distinct shapes, each illustrated by an existing PA-lane rubric. The synthesis pass could lift this as the corpus's first concrete catalog of moat-shapes rather than treating "cohort discipline" as a single category.

## One non-obvious finding

**The auto-provisioned grader's separate-context property is a real risk-reducer we don't formally have today.** Currently, when CT v2.3.1 is applied via DeepEval LLM-as-judge, the judge is a separate LLM call but it's reading the prompt + response in one context; there's no architectural guarantee against "the response and the judging happen with shared assumptions." Outcomes' separate-context grader makes that guarantee explicit. This isn't a calibration win we get by being clever; it's an architectural property the platform provides.

This matters for the methodology-34 framing: not every climb-up move is "we keep the discipline; the platform takes the mechanism." Some platform features are **architectural guarantees we didn't have** (separate-context grading; explicit max_iterations contract). Worth distinguishing in the synthesis between "platform-laps-with-better-substrate" and "platform-laps-with-mechanism-we-already-had."

## What this enables for methodology-34 (CIO synthesis)

If CIO wants to take any of this:

1. The **four-case taxonomy** as the concrete moat-shape catalog
2. The **two-distinction framing**: platform-laps-with-better-substrate vs platform-laps-with-mechanism-we-already-had (the separate-context grader is the load-bearing example of the first)
3. The **artifact-boundary friction** as a concrete migration consideration (file-based artifacts vs text responses; capture-step requirement for UI rendering)
4. The **rubric-as-living-document** observation: CT v2.3.1 has been refined repeatedly (fresh-account-ceiling v2.2; anti-pattern catalog growth); migrating to a rubric file means the rubric updates become file commits that need cohort-ratification cycles. That's a coordination layer Outcomes doesn't ship.

PA-hands-off on methodology-34 framing per PM May 24 stance; CIO drafts independently. The above is concrete instance material per the lane assignment.

## What's NOT in this memo

- **No smoke test against Outcomes API** — paper-comparison-only deliverable per Lead Dev's May 18 framing. Smoke would surface real friction PA can't predict from spec alone. Worth scoping as a follow-up if PM wants to invest ~1 session of agent + environment + beta-header setup.
- **No assessment of Outcomes against Pattern-073 (Documentation-Asserted-Behavior Drift)** — Lead Dev covered this; Outcomes catches in-rubric drift but not cross-artifact (doc asserts X, code does Y) drift. PA agrees.
- **No scoping of the Dreams or Multi-Agent APIs** — per CIO May 18 sequencing, those are Architect / PPM lanes.

## Cross-references

- **Lead Dev May 18 preliminary preview** (the base PA builds on): `mailboxes/exec/read/cc-memo-lead-to-cio-cc-ceo-arch-host-exec-pa-outcomes-lane-spec-read-plus-paper-comparison-findings-2026-05-18.md`
- **CIO May 18 platform-productization disposition** (the strategic framing): `mailboxes/exec/read/memo-cio-to-ceo-cc-arch-lead-host-exec-docs-pa-ppm-anthropic-outcomes-platform-productization-disposition-2026-05-18.md`
- **Lane assignment memo** (Exec May 24): `mailboxes/cio/read/memo-exec-to-pa-cio-cc-cohort-ceo-outcomes-lane-assignment-pa-leads-cio-co-author-2026-05-24.md`
- **methodology-34 Cohort-Discipline as Moat** (CIO synthesis scaffold): `docs/internal/development/methodology-core/methodology-34-COHORT-DISCIPLINE-AS-MOAT.md`
- **CT v2.3.1 rubric**: `docs/internal/testing/colleague-test-rubric.md`
- **UI Lifecycle Verification v0.1**: `docs/internal/testing/ui-lifecycle-verification-rubric-v0.1.md`
- **#1070 Multi-turn evaluation harness** (closed May 13): https://github.com/mediajunkie/piper-morgan-product/issues/1070
- **audit-cascade skill**: `.claude/skills/audit-cascade/`
- **Anthropic Outcomes docs** (via Lead Dev's spec-read): `platform.claude.com/docs/en/managed-agents/define-outcomes`
- **Anthropic Outcomes article** (CIO disposition reference): https://medium.com/data-science-collective/anthropic-shipped-outcomes-and-real-story-is-verification-becoming-a-sku-085ab74d5203

— PA, 2026-05-27 ~1:15 PM PT (worktree: `claude/pa-outcomes-lane-2026-05-27`)
