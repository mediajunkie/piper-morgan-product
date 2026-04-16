# Excellence Flywheel — Formulation Archaeology

**Date**: 2026-04-16
**Task**: Issue #982 (FLY-AUDIT) Phase 1 — read-only trace of how the concept has been formulated over time
**Scope**: 146 files reference "Excellence Flywheel"; this doc samples ~30 across time
**Output type**: Evolution picture only. No resolution proposed — that is CIO's Phase 2 job.

---

## 1. Summary

I found **8 materially distinct formulations** of the Excellence Flywheel, with a ninth (the Python implementation) that reifies its own variant in code. They fall into three structural families:

- **Self-reinforcing cycle** (the original July 2025 blog-post framing): a *causal loop* between quality and velocity. No enumerated "pillars" — just phases of a flywheel that spins.
- **N-pillar checklist** (Aug–Sep 2025, persisted as the "canonical" doc): a static list of things to do. This is where "Four Pillars" + "5 items" drift crystallized.
- **N-step cycle / sequence** (Sep 2025 onward, proliferated through briefings): a compact mnemonic — 4 verbs in order — used as a one-line description for role briefings.

The rough timeline:

- **Jul 23, 2025** — Concept coined in a blog-post-style narrative. Five *patterns* plus a *mechanism* (5-step compounding cycle). No "pillars" language.
- **Jul 27, 2025** — First codified as `methodology-00-EXCELLENCE-FLYWHEEL.md` with heading **"Four Pillars"** but a body of **4 items**. Internally consistent at birth.
- **Aug 15, 2025** — Python implementation (`excellence_flywheel_integration.py`) defines its own structure: **5 verification phases** + 4 principles.
- **Aug 18, 2025** — A fifth pillar ("Agent-Driven Development") added to methodology-00 *without updating the "Four Pillars" heading*. This is the bug now being audited.
- **Aug 22, 2025** — Pillar 3 and Pillar 4 get expanded with new sub-items (task decomposition, test infrastructure, smoke tests). The heading still says "Four Pillars."
- **Sep 25, 2025** — `PROJECT.md` ships a completely different 4-step formulation: **Verify before assuming / Test before claiming done / Lock with tests / Document decisions.** No overlap with the canonical doc's vocabulary.
- **Sep 26, 2025** — `METHODOLOGY.md` (briefing-level operational guide) ships *yet another* 4-step formulation: **Verify Before Assuming / Discover Before Implementing / Test Before Claiming / Lock Before Moving On.** Similar shape to PROJECT.md, different verbs.
- **Oct 19, 2025** — `BRIEFING-ESSENTIAL-LEAD-DEV.md` introduces the **"Verify → Implement → Evidence → Track"** one-liner. This is the compact mnemonic most agents paraphrase today.
- **Nov–Mar 2026** — Role briefings for CIO, Piper Alpha, Comms, Architect, Chief of Staff each add their own one-line summaries. No two are identical.
- **CLAUDE.md** (current) — *Does not contain the phrase "Excellence Flywheel" at all.* It has closely related principles ("Verify First, Create Second", "Evidence Required", "Completion Discipline") that are operationally similar but not identified as the Flywheel.

**My interpretation of how drift happened**: The original concept was a *causal loop about compounding quality*, not a checklist. When it got codified into methodology-00 it was re-cast as a checklist of "pillars" — a fundamentally different type of object (static enumeration vs. dynamic cycle). Subsequent agents inheriting the checklist form kept adding items as the toolkit grew (TDD → multi-agent → agent-driven → GitHub-first → test infrastructure) without auditing the heading. Simultaneously, operational briefings re-compressed it into 4-verb mnemonics for ergonomic reasons, but each author picked slightly different verbs. The original flywheel *cycle* formulation largely disappeared from active use; what persisted is the *name* attached to whatever bundle of disciplines the author thought was most important that week. CLAUDE.md's omission of the phrase while retaining the principles suggests at least one agent concluded the label had become more confusing than helpful.

---

## 2. Chronological Formulations

### F1 — The Causal Loop (July 23, 2025) — **ORIGIN**

- **Source**: `dev/2025/09/26/excellence-flywheel-post.md` (blog draft, dated July 23 in the post; repository date Sep 26 reflects dev/ airlift, not authorship)
- **Also**: `dev/2025/09/26/excellence-flywheel-refreshed.md` (polished version)
- **Status**: Superseded for operational use; preserved as origin narrative.

**Structure**: A self-reinforcing causal loop of **6 phases**:

> Foundation-First Development → builds reliable infrastructure
> Systematic Verification → prevents technical debt accumulation
> Multi-Agent Coordination → enables parallel progress without conflicts
> Accelerated Delivery → creates confidence to invest more in systematic approaches
> More Foundation Investment → strengthens the foundation for even faster future work
> [Cycle repeats with compound benefits]

Accompanied by **5 "critical patterns"** (a separate list, scored /16):
1. Session Log Pattern (16/16)
2. Verification-First Pattern (15/16)
3. Human-AI Collaboration Referee (15/16)
4. Error Handling Framework (14/16)
5. Configuration Management Framework (14/16)

**Note**: In the origin, "pattern list" and "flywheel cycle" are two different things. Later formulations conflate them.

---

### F2 — Four Pillars as Four Items (July 27, 2025)

- **Source**: `docs/internal/development/methodology-core/methodology-00-EXCELLENCE-FLYWHEEL.md` (first version, commit `7c5f8d9f` / `a4afeaab`, 2025-07-27)
- **Status**: Superseded in the same file by F3.

**Structure**: Heading "Four Pillars (Non-Negotiable)" with exactly 4 items.

1. Systematic Verification First
2. Test-Driven Development
3. Multi-Agent Coordination
4. GitHub-First Tracking

Plus a "Flywheel Effect" one-liner: *Quality → Velocity → Quality → Velocity (compounds infinitely)* and a 5-step "Daily Practice" list (verify / write failing test / implement minimal / verify with evidence / document patterns).

This is the only point at which the canonical doc was internally consistent.

---

### F3 — Four Pillars as Five Items (Aug 18, 2025) — **CURRENT CANONICAL DOC**

- **Source**: `docs/internal/development/methodology-core/methodology-00-EXCELLENCE-FLYWHEEL.md` (current HEAD)
- **Introduced by**: commit `d81e6fbc` / `5f046f44` (2025-08-18, "weekly docs audit yml"), which added pillar #5 without updating the heading.
- **Expanded by**: commit `a1af7564` / `8ce699eb` (2025-08-22), which bloated pillars 3 and 4 with sub-items.
- **Status**: **Currently in force** — this is the "canonical" doc; also the one with the audit-triggering inconsistency.

**Structure**: Heading "Four Pillars (Non-Negotiable)" with 5 items.

1. Systematic Verification First
2. Test-Driven Development
3. Multi-Agent Coordination (+ Task Decomposition, Agent Assignment, Synchronization Points, Performance Monitoring)
4. GitHub-First Tracking & Test Activation (+ Test Infrastructure, Smoke Tests, Integration Tests, Performance Monitoring)
5. Agent-Driven Development

The heading/body mismatch that prompted #982 has been in force since **Aug 18, 2025** — approximately 8 months.

---

### F4 — Python Implementation: 5 Phases + 4 Principles (Aug 15, 2025)

- **Source**: `services/orchestration/excellence_flywheel_integration.py` (commits `f448db18`/`46523f75`/`4806e4da`, 2025-08-15, "PM-033d PHASE 4 COMPLETE")
- **Status**: Alive in code; test harness references it (`scripts/phase4_integration_test.py`).

**Structure**: Two enumerations.

*5 VerificationPhase enum values:*
1. PRE_COORDINATION
2. TASK_DECOMPOSITION
3. AGENT_ASSIGNMENT
4. POST_COORDINATION
5. LEARNING_CAPTURE

*4 principles (in class docstring):*
1. Verify First, Implement Second
2. Pattern Detection and Learning
3. Compound Knowledge Acceleration
4. Systematic Quality Assurance

This is a third axis of "what the Flywheel is" — neither pillars nor a verb-cycle, but a runtime verification protocol. Predates F3 by 3 days and appears to have been developed in parallel, not in dialogue with it.

---

### F5 — PROJECT.md Four-Step (Sept 25, 2025)

- **Source**: `docs/briefing/PROJECT.md` lines 62–67 (commit `b5c63542`/`b3e5a5b0`, 2025-09-25, GREAT-1C documentation package)
- **Status**: **Currently in force** in PROJECT.md.

**Structure**: 4 sequential steps, verb-initial.

1. Verify before assuming
2. Test before claiming done
3. Lock with tests
4. Document decisions

No "pillars" language. No cycle/compounding language. No mention of TDD, multi-agent, or GitHub tracking as pillars. Significantly different vocabulary from F3.

---

### F6 — METHODOLOGY.md Four-Phase (Sept 26, 2025)

- **Source**: `docs/briefing/METHODOLOGY.md` lines 180–213 (introduced in commits `c5aadb94`/`dfde8221` Sep 26 "Phase 1 methodology navigation improvements"; body finalized in `8c78f2d7`/`42fceae6` Sep 26)
- **Status**: **Currently in force** in METHODOLOGY.md — described as "our systematic approach to prevent the 75% pattern from recurring."

**Structure**: 4 steps with verb pairs.

1. Verify Before Assuming (with bash examples)
2. Discover Before Implementing
3. Test Before Claiming
4. Lock Before Moving On

Parallel construction is cleaner than F5; content overlaps substantially but verbs differ. Notably introduces *Discover* as a distinct step between Verify and Test, which neither F3 nor F5 has.

---

### F7 — Verify → Implement → Evidence → Track (Oct 19, 2025)

- **Source**: First seen in `knowledge/BRIEFING-ESSENTIAL-LEAD-DEV.md` at commit `dede834a`/`c4dab30b` (2025-10-19, "chore: organize session logs"). Now lives at `docs/briefing/BRIEFING-ESSENTIAL-LEAD-DEV.md:29`.
- **Also referenced**: `dev/2025/10/17/knowledge-backup/BRIEFING-ESSENTIAL-LEAD-DEV.md:32`
- **Status**: **Currently in force** in the Lead Dev briefing; probably the most-paraphrased version because it's the one-liner a Lead Dev sees at every session start.

**Structure**: 4-verb arrow-chain mnemonic.

**Verify → Implement → Evidence → Track**

No body text; it's a single-line tagline. This is the formulation closest to CLAUDE.md's actual principles, but note the verb *Implement* (unique to F7) and *Track* (echoing F3's GitHub-First).

---

### F8 — Piper Alpha Four-Clause Cycle (Mar 30, 2026)

- **Source**: `docs/briefing/BRIEFING-piper-alpha.md:156` (commit `d5a72969`, 2026-03-30, "Piper Alpha docs")
- **Status**: **Currently in force** in the PA briefing.

**Structure**: Restates F1's causal-loop spirit in 4 clauses.

> Systematic verification → reliable coordination → accelerated delivery → further investment in verification

This is the only current formulation that preserves the original *cycle* structure from F1. Interestingly, it was authored by a later agent who may have read the origin post.

---

### F9 — CIO Briefing Bullet List (no formal date — March 2026)

- **Source**: `docs/briefing/BRIEFING-ESSENTIAL-CIO.md:61-66`
- **Status**: **Currently in force** in the CIO briefing.

**Structure**: 5 properties/anti-pattern bullets, not a sequence.

- Foundation work enables velocity gains
- Preparatory work reduces implementation risk
- Systematic approaches create compound returns
- Measurement framework: velocity gains, quality improvements, pattern reuse
- Anti-pattern: Verification theater (tests pass without validating functionality)

Closer to a description of *what the flywheel does* than to pillars or a sequence. Only formulation to name an explicit anti-pattern ("verification theater") as part of the definition.

---

### Adjacent formulations (not counted as distinct, but worth flagging)

- **CLAUDE.md** — contains "Verify First, Create Second" (Pattern-level, not identified as Flywheel), "Evidence Required", "Completion Discipline" — functionally equivalent to F7 but **does not use the name**.
- **methodology-09-MCP-SPATIAL.md:11** — restates F3 as "four core pillars" with explicitly 4 items (reverts to F2's count, not F3's five). Written post-F3 but ignored the 5th pillar.
- **methodology-06-CORE-PATTERNS.md:208** — one-liner: *"Excellence Flywheel: Quality creates velocity creates quality."* Echo of F1's effect-statement only.
- **methodology-03-COMMON-FAILURES.md** — titled *"Common Failures That Break The Flywheel,"* implying the flywheel is something that *can be broken* by specific anti-patterns. This treats it as a state rather than a process or list.
- **BRIEFING-ESSENTIAL-ARCHITECT.md:127** — one-liner: *"Architectural decisions with evidence tracking."* Collapses the whole concept to evidence-tracking.
- **BRIEFING-ESSENTIAL-COMMS.md:57** — one-liner: *"Systematic quality improvement cycle."* Collapses it to "continuous improvement."
- **`dev/analysis/analysis_code_independent/load-bearing-concepts.md`** (Sept 2025 analysis doc) — describes Flywheel's own *evolution* as "Basic process improvement concept → Systematic quality assurance framework → Cultural and architectural principle" — an auto-archaeology that confirms drift was already visible at that time.

---

## 3. Analysis

### Which formulations conflict with each other

| Conflict | F# | Nature |
|---|---|---|
| Four Pillars heading vs. 5 items | F3 (internal) | Trivial, fixable — heading/body mismatch. This is the audit trigger. |
| F3 "pillars checklist" vs. F1 "causal cycle" | F1 vs. F3 | Structural — different *kind* of object. A checklist is not a cycle. |
| F5 "Verify/Test/Lock/Document" vs. F6 "Verify/Discover/Test/Lock" | F5 vs. F6 | Semantic — F6 inserts *Discover* and drops *Document*. They can't both be canonical. |
| F7 "Verify → Implement → Evidence → Track" vs. everything else | F7 vs. F3/F5/F6 | Different verbs. *Implement* appears nowhere else; *Track* only appears in F3 as "GitHub-First Tracking." |
| F4 (5 runtime phases) vs. all the doc-level formulations | F4 vs. F2–F3, F5–F7 | Code and docs are describing different things under the same name. The Python class verifies coordination phases; the doc formulations describe development discipline. |
| F8 "cycle" vs. F3 "pillars" in the same project | F8 vs. F3 | A reader comparing PA's briefing to the canonical doc sees two different kinds of claim. |

### Which are most internally consistent

- **F1 (origin blog post)** — Internally consistent as a narrative; the cycle mechanism and the pattern list are clearly distinguished.
- **F2 (July 27 canonical)** — Internally consistent at the moment of creation (heading and body agreed).
- **F6 (METHODOLOGY.md)** — Cleanest parallel construction: 4 steps, all verb-phrase pairs, each with a brief example block. Reads like finished writing.
- **F8 (PA briefing)** — Recovers the cycle structure in one clean sentence.

**Least internally consistent**: F3 (current canonical), because of the 4-vs-5 mismatch AND because pillar 4's title smuggles a second subject ("& Test Activation").

### Pattern in the drift

Three observable patterns:

1. **Structural flip from cycle → checklist → mnemonic.** F1 was a cycle. F2/F3 made it a checklist. F5/F6/F7 compressed it to an ordered sequence of verbs. Each flip loses information: the cycle loses discipline-granularity; the checklist loses causal feedback; the mnemonic loses bash examples. F8 is a partial recovery.
2. **Accretion without retraction.** F3 gained pillar 5, then sub-bullets under 3 and 4, without ever removing or editing. Nobody rewrote; everyone added. This is a general tendency in the repo's methodology docs — files grow, they don't get pruned.
3. **Per-role paraphrase.** Each role briefing (Lead Dev, CIO, PA, Comms, Architect, Chief of Staff) paraphrases the Flywheel in its own voice. No briefing points to the canonical doc as the single source of truth; each asserts its own one-liner as if it *were* the definition. This is the *multiplication* vector — 6 briefings × 1 independent paraphrase each = 6 non-matching formulations on top of the canonical.

**Early formulations emphasized** compounding / velocity-quality feedback (F1, F2 flywheel-effect line, F8).
**Later formulations emphasized** per-task discipline ("verify before X, test before Y"), i.e., the Flywheel as *what you do on a given task*, not as *the system property that emerges from doing it well over time* (F5, F6, F7).

This shift from *system-level property* to *task-level checklist* is the biggest semantic change and probably the one CIO will have to rule on.

---

## 4. Handoff Notes for CIO

The Flywheel is being used today to mean at least three different kinds of thing. Before writing a canonical definition, CIO will need to decide:

### Decision 1 — What *kind* of object is the Flywheel?

Pick one (or name the relationship between them):

- **(a) An emergent system property** — the compounding causal loop of F1/F8. "Quality creates velocity creates quality."
- **(b) A discipline checklist** — the F3 pillars: a finite list of non-negotiable practices you apply per task.
- **(c) A task-execution sequence** — the F5/F6/F7 verb-chain: an ordered process for any given unit of work.
- **(d) A runtime verification protocol** — the F4 Python implementation: phased checks around coordination.

These aren't mutually exclusive, but they aren't the same thing. Current docs present them as interchangeable, and they aren't.

### Decision 2 — If checklist, how many pillars?

- **4** (F2 original, F5, F6, F7 at mnemonic level, methodology-09) or
- **5** (F3 current canonical, CIO briefing's bullet list)?

If 5, pillar 5 ("Agent-Driven Development") needs a justification independent of pillar 3 ("Multi-Agent Coordination"). Right now they overlap significantly.

### Decision 3 — Does the Flywheel include Evidence/Tracking/GitHub-First as a pillar or not?

- F3 and F7 treat tracking as a pillar/step.
- F5, F6, F8, and F1 don't — tracking is covered elsewhere (CLAUDE.md's "Evidence Required" section, methodology-08).

If CIO extracts tracking, the Flywheel shrinks to 3 pillars (verify, TDD, coordinate) and the structure matches F8 better.

### Decision 4 — What's the relationship between the doc and the code?

`services/orchestration/excellence_flywheel_integration.py` implements F4 — which does not match any of the doc formulations. Either:

- the Python class should be renamed (it's really a coordination verification integrator);
- the canonical doc should incorporate F4's 5 phases;
- or the code should be deleted/refactored if it's no longer serving a live product purpose.

A quick check: is anything currently calling `ExcellenceFlywheelIntegrator` at runtime, or is it only referenced from one test harness script? (That's an easy follow-up for an implementation agent — out of scope here.)

### Decision 5 — What happens to the name in CLAUDE.md?

CLAUDE.md — the document every agent reads first — does not use the phrase "Excellence Flywheel" at all. It does contain operationally-equivalent principles ("Verify First, Create Second", "Evidence Required", "Completion Discipline"). Options:

- (a) CLAUDE.md stays name-free; the Flywheel concept lives only in briefings/methodology docs for higher-level discussion.
- (b) CLAUDE.md adopts the name and picks one formulation.
- (c) The name is retired entirely as institutional cruft; what remains is the principles under their current CLAUDE.md labels.

Each is defensible. This is the highest-leverage decision, because CLAUDE.md is what all agents actually read.

### Decision 6 — Per-role briefings: paraphrase or cite?

Each role briefing currently paraphrases. CIO could require that role briefings *cite* the canonical formulation (with a link) rather than restating it. This would prevent F9 and similar drift from recurring after Phase 2's reconciliation.

### Small parallel findings worth flagging separately

- The origin blog post (F1) was never published publicly — it lives in `dev/2025/09/26/excellence-flywheel-post.md` and `-refreshed.md`. The concept exists *internally* without an external anchor. CIO may want to decide whether the origin narrative should be archived formally or surfaced.
- `methodology-03-COMMON-FAILURES.md` is titled *"Common Failures That Break The Flywheel"* but never defines the flywheel it claims to protect — it assumes the reader already knows. This works only while the definition is stable.
- There's a documented meta-observation in `dev/analysis/analysis_code_independent/load-bearing-concepts.md` that "Excellence Flywheel Evolution (Aug 16 → Sep 3)" has already occurred — from "basic process improvement concept" to "systematic quality assurance framework" to "cultural and architectural principle." So the project has been aware that the concept is drifting for at least 8 months; this audit is the first attempt to reconcile.

---

**End of archaeology.** No canonical definition attempted here. All provenance checked via `git log -p`, `git log -S`, and file inspection on 2026-04-16.
