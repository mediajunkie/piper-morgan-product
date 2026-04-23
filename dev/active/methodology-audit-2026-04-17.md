# M1 Methodology Audit

**Audit Period**: March 15 – April 11, 2026 (~4 weeks)  
**Previous Audit**: March 15, 2026 (covered Feb 3 – Mar 14)  
**Trigger**: M1 Gate #926 closed April 11, 2026  
**Conducted by**: Chief Innovation Officer  
**Date**: April 17, 2026

---

## Section 1: Executive Summary

The M1 period was the most eventful since the project's founding. It included a full sprint (M1), a 12-role infrastructure migration, the launch of a new agent role (PA), a strategic pivot ("methodology over code"), and the adoption of a cross-project context standard (RFC-001). The gate methodology — fresh-account UAT with scored rubrics — caught what 6,310 automated tests couldn't, confirming Pattern-045 at full product scale across four UAT rounds.

The methodology is strong where it matters most: in catching real failures, coordinating multi-agent work, and producing transferable innovations. It is weak where it has always been weak: in maintaining its own documentation. The headline finding of this audit — the Excellence Flywheel's 8-formulation drift across 9 months — is the canonical example: a concept that does real work operationally but whose documentation has degraded to the point where agents paraphrase it differently every time they cite it.

The audit's primary deliverable is a Flywheel reformulation (Section 2) that resolves the drift. The remaining sections assess the period's methodology innovations, validate what worked, and produce recommendations.

---

## Section 2: Excellence Flywheel Reformulation

### The Problem

Docs' Phase 1 archaeology (#982) found 8 materially distinct formulations of the Excellence Flywheel across 3 structural families (causal loop, N-pillar checklist, N-verb mnemonic), plus a Python implementation matching none of them. PA's reference audit confirmed: `methodology-00-EXCELLENCE-FLYWHEEL.md` — the "mandatory reading" canonical doc — was not referenced in a single session log during the audit window. Zero citations in 128 files across 27 days.

The concept is alive. The documentation is dead.

### Root Cause

The archaeology identified three drift patterns:

1. **Structural flip**: The original concept (July 2025) was a causal loop about quality compounding into velocity. It was recast as a checklist of "pillars" (Aug 2025), then compressed into verb mnemonics for briefings (Sep-Oct 2025). Each transformation lost information: the cycle lost discipline-granularity; the checklist lost causal feedback; the mnemonic lost procedural detail.

2. **Accretion without retraction**: The canonical doc gained a fifth pillar, then sub-bullets under two existing pillars, without editing the heading or removing anything. Files grow; they don't get pruned.

3. **Per-role paraphrase**: Each role briefing restated the Flywheel in its own voice without pointing to the canonical source. Six briefings × one independent paraphrase each = six non-matching formulations layered on top.

### The Reformulation

The Excellence Flywheel is three layers, not one formulation:

**Layer 1 — The Concept (why it works)**

The Excellence Flywheel is a self-reinforcing cycle: systematic preparation enables faster execution, which produces higher quality, which builds confidence to invest more in systematic preparation. The cycle compounds over time. Each revolution builds on the last.

This is the insight. It doesn't change. It explains *why* disciplined practice produces accelerating returns rather than constant overhead. When we say "the flywheel is spinning," we mean this feedback loop is operating.

**Layer 2 — The Practices (what we do)**

The practices that make the flywheel spin. These are enumerable, versioned, and will evolve as the project evolves. As of M1 closure (April 2026):

1. **Verify before building.** Research existing patterns, check the domain model, understand what's already there. Prevents rework. (Origin: Pillar 1, July 2025. Unchanged.)

2. **Test what matters, not what's easy.** TDD remains foundational, but M1 proved that mocked unit tests are necessary but insufficient. The Colleague Test, fresh-account UAT, and scored rubrics are now part of "testing." Pattern-045 is the anti-pattern: tests that pass without validating real user experience. (Origin: Pillar 2, July 2025. Evolved through M1 gate experience.)

3. **Coordinate through structure.** Multi-agent coordination via mailboxes, session logs, handoff memos, and omnibus synthesis. Not ad hoc communication — structured async protocols that survive platform migrations and session gaps. (Origin: Pillar 3, July 2025. Evolved through mailbox v3, handoff protocol, and migration validation.)

4. **Track to completion with evidence.** GitHub-first. Create issues before starting. Close with evidence. The Inchworm Protocol: complete each phase 100% before advancing. (Origin: Pillar 4, July 2025. Unchanged.)

5. **Audit the composition.** Pattern-062 (Assembly Assumption): individually correct components don't guarantee correct composition. Wiring passes after multi-feature sprints. Gate verification before declaring sprints complete. The M0-M1 experience added this to the flywheel — it was the missing practice that allowed 6,310 passing tests to coexist with a non-functional product. (New. Emerged Feb 2026, proven through M1 gate.)

**Layer 3 — The Mnemonics (how agents remember)**

Compact recall aids adapted per role. Each mnemonic traces back to the practice layer. Examples:

- Lead Dev: Verify → Test → Coordinate → Track → Audit
- General: "Prepare systematically, test honestly, coordinate structurally, complete with evidence, verify the composition"

Role briefings should *cite* the canonical practice layer (with a reference path), not restate it in their own words. This prevents the per-role paraphrase drift that produced 6 non-matching formulations.

### CLAUDE.md Decision

**The "Excellence Flywheel" label does not enter CLAUDE.md.** CLAUDE.md already contains the operational principles ("Verify First, Create Second," "Evidence Required," "Completion Discipline") and agents follow them. Adding the Flywheel label would create one more thing for agents to paraphrase incorrectly. The concept lives in `methodology-00-EXCELLENCE-FLYWHEEL.md` for agents who want the reasoning. PM confirmed this decision April 16.

### Python Implementation

`services/orchestration/excellence_flywheel_integration.py` implements a runtime verification protocol (5 phases + 4 principles) that matches none of the document formulations. Lead Dev or Architect should evaluate: is this file called at runtime? If yes, align with the reformulation or rename to reflect what it actually does (coordination verification). If no, retire it. This is a Phase 3 question for Docs to route.

### Downstream

Docs takes Phase 3: update all downstream references (~146 files) to match canonical language, flag narrative content needing more than a name-swap, add Flywheel drift to the weekly audit sweep. Phase 4 generalizes to other canonical vocabulary.

---

## Section 3: Methodology Innovations — Assessment

PA's trigger memo identified 6 innovation candidates. Assessment:

### 3.1 "Bring Your Own Chat" Distribution Philosophy

**Status**: Operational insight, not a methodology pattern.

BYOC is a product distribution strategy (build as MCP server, package per-platform) that emerged from the PA-PM strategic conversation on Apr 7. It's important strategically but it's not a methodology innovation — it doesn't change how we work; it changes what we build. Belongs in the Vision document (already in V2.2), not in the methodology-core.

### 3.2 Differentiator Stack as Sprint Organizing Principle

**Status**: Operational insight, appropriate for roadmap documentation.

Reorganizing M2-M5 around the differentiator stack (context methodology + conscious floor + artifact persistence + trust graduation) rather than implementation domains is a planning decision, not a methodology pattern. Already reflected in Roadmap v15.0.

### 3.3 "Indoor Plumbing vs. Bathing Experience" Scope Filter

**Status**: Candidate for methodology-core as a scoping heuristic.

This is a genuine methodology contribution. It's a decision filter: "Is this indoor plumbing (commodity, use MCP plugins) or the bathing experience (differentiator, build it)?" Applied repeatedly in the backlog deep review to justify 12 closures. It operates the same way the object model grammar ("Entities experience Moments in Places") does — as a test that catches scope errors before they become sprint work.

**Recommendation**: Document as a scoping heuristic in methodology-core, not as a numbered pattern. It's a principle, not a recurring failure mode.

### 3.4 Cross-Pollination Routing Memos

**Status**: Emerging pattern candidate.

PA writing role-specific routing from the daily cross-pollination brief is a new coordination practice. It converts a broadcast channel (the brief) into targeted action items per role. This is a genuine process innovation that could become Pattern-063 or equivalent.

**Recommendation**: Monitor through M2. If it sustains and other agents adopt the pattern, formalize as Emerging.

### 3.5 "Continuity Memo Written Before the Seam"

**Status**: Emerging pattern candidate.

Three independent instances across three projects: Docs session wrap memos, OpenLaws coffee-spill handoff, Klatch Phase 3.5 handoff prompt. The pattern: write the continuity document *before* the discontinuity occurs, not after. Handoff memos written by the departing instance are richer and more accurate than reconstruction by the arriving instance.

**Recommendation**: Strong candidate for Emerging pattern. The three-project convergence is good evidence. File when ready.

### 3.6 Floor Fabrication Guardrail

**Status**: Already implemented (defense-in-depth, not new methodology).

The floor fabrication guard (explicit instruction not to invent capabilities) is a good engineering practice but it's a product feature, not a methodology innovation. It's defense-in-depth against a known LLM failure mode. Already in the codebase.

---

## Section 4: What Worked

### 4.1 Gate Methodology — Validated Through Failure

The M1 gate design is the audit period's strongest methodology validation. Four UAT rounds, three failures, one breakthrough — and the methodology caught what 6,310 automated tests couldn't.

Key components that proved their value:
- **Fresh-account testing**: Tests on a clean install, not a developer's configured environment
- **Colleague Test rubric**: Relevance/Context/Tone, 0-3 each, 7+ passes, any 0 auto-fails. Unambiguous scoring.
- **CXO as quality authority**: The CXO ran three rounds after two complete failures, producing a structured diagnostic memo each time. That persistence is what rigorous methodology looks like.
- **Stopping early**: Apr 3 testing was stopped after 8 of 14 scenarios because systemic floor failure made remaining tests uninterpretable. The discipline to stop when results are meaningless is as important as the discipline to test.

**New diagnostic pattern identified**: "Stacked Silent Failures" — multiple independent failures that each mask their own symptoms, producing a composite behavior requiring layer-by-layer investigation. The M1 gate failure was three stacked layers: deprecated model ID → undifferentiated fallback template → missing response field in conversation history. Each round peeled one layer. Principle: if the fix doesn't change the symptom, the diagnosis was wrong.

### 4.2 Infrastructure Migration — Methodology Survived Discontinuity

The Mar 30 migration (12 roles, 18 sessions, 8 handoff memos) was the methodology's most demanding stress test. Every role was instantiated fresh — new chat instance, no conversation history — and resumed productive work within a single session.

What carried the load: handoff memos (Layer 5 transfer), briefing documents (Layer 2-3), session-start hooks (Layer 1), and workstream review memos (Layer 4 context). The five-layer model, adopted during this period via RFC-001, provides the vocabulary to explain *why* this worked: Layers 1-3 transferred via committed files, Layer 4 via workstream memos, Layer 5 via handoff prompts. The methodology is explicitly designed for discontinuity.

### 4.3 Multi-Agent Coordination — Matured

The #717 resolution (Mar 23, four roles, five memos, 90 minutes, zero PM mediation) and the Ship #036 assembly (six workstream memos → one draft in one CoS session) demonstrate coordination operating at high maturity. The mailbox system, memo conventions, and workstream review process are load-bearing infrastructure.

### 4.4 Cross-Project Learning — Operational

The cross-pollination hub published daily briefs throughout the audit period. RFC-001 was proposed, reviewed bilaterally (PM CIO + Klatch Calliope), and endorsed with amendments. The five-layer context model is now shared vocabulary across the DinP ecosystem. Klatch's scaffolded probing methodology (AAXT Phase 1) is applicable to PM's E2E track.

---

## Section 5: What Needs Attention

### 5.1 Methodology-Core Documentation Remains Stale

PA's reference audit is definitive: 20 of 22 numbered methodology docs were not referenced in any session log during the audit window. The operational principles live in CLAUDE.md and role briefings; the methodology-core directory is a reference library nobody references.

This was flagged in the Mar 15 audit (Recommendation #4: add methodology-core staleness check to docs audit). Docs created `methodology-23-M1-INNOVATIONS.md` on Mar 31, which is good — but 20 silent docs remain.

**Two hypotheses** (PA identified both):
- (a) The principles are internalized and operate via CLAUDE.md — the methodology docs are working *through* other documents
- (b) There's a structural disconnect between methodology-core and active agent work

Both are probably true simultaneously. The Flywheel reformulation (Section 2) addresses this by not requiring CLAUDE.md to reference the Flywheel name while keeping the methodology doc as the canonical concept reference.

**Recommendation**: Don't attempt a 20-doc refresh — that's make-work. Instead, evaluate each silent doc for one of three dispositions: (a) still accurate, just internalized → add a "Last verified" date and leave it; (b) outdated → refresh or retire; (c) superseded by a different doc → redirect. This is a Docs task with CIO review, not a CIO task.

### 5.2 Pattern Catalog Usage Is Narrow

PA's reference audit shows Pattern-062 (14 files) and Pattern-045 (12 files) dominating, with Pattern-063 at 6. The remaining ~60 patterns were silent during the audit window. This isn't necessarily a problem — many patterns are domain-specific and wouldn't appear in every period — but it raises the question of whether the catalog is functioning as a reference tool or just accumulating.

**Recommendation**: No immediate action. The next pattern sweep should include a usage check: are agents discovering patterns through the catalog, or only through direct citation in session logs and memos? If the latter, the catalog's discoverability may need improvement.

### 5.3 ADR-045 Near-Silence

The object model grammar ("Entities experience Moments in Places") was cited once during the audit period despite being constitutional. PDR-004 (also constitutional) was cited 17 times. PA's interpretation — low count may reflect internalization — is plausible but worth monitoring. If the grammar stops appearing even in product design discussions, it may indicate it's been forgotten rather than internalized.

### 5.4 Hooks Phase 1 Monitoring — Still Unchecked

Carried from the Mar 15 audit. The systematic check of omnibus logs Feb 25 – Mar 14 for hook-preventable failures has not been done. This is now 7 weeks overdue from the original commitment.

**Recommendation**: Either do the check or formally close the monitoring commitment with a rationale. Continuing to carry it as an open item without action is itself a methodology issue.

---

## Section 6: Previous Audit Recommendations — Status

| # | Mar 15 Recommendation | Status | Notes |
|---|----------------------|--------|-------|
| 1 | Verify Pattern-062 and commit | ✅ DONE | Proven status, PM sign-off Mar 21 |
| 2 | Hooks Phase 1 monitoring check | ❌ NOT DONE | Carried 7 weeks. See 5.4 above. |
| 3 | File issue for methodology-core refresh | ✅ DONE | methodology-23-M1-INNOVATIONS.md created Mar 31 |
| 4 | Add methodology-core staleness to audit template | ✅ DONE | Docs added to audit sweep |
| 5 | CIO self-approval for Emerging patterns | ✅ DONE | Policy approved Mar 16 |
| 6 | Codify AX Testing questionnaire | ⏳ PARTIAL | Template exists; not yet formalized as numbered methodology |
| 7 | Add product coherence to CXO testing | ✅ DONE | Fresh-account UAT with Colleague Test — validated through M1 gate |
| 8 | Document roundtable format | ❌ NOT DONE | Pattern not formalized |
| 9 | Trigger-based audit cadence | ✅ DONE | Policy approved Mar 16; this audit is the first execution |
| 10 | Monitor methodology-product convergence | ✅ ACTIVE | Same-day latency achieved repeatedly (roundtable → implementation, backlog review → strategic pivot) |

**Score**: 6 done, 1 partial, 1 active, 2 not done. The two undone items (Hooks monitoring, roundtable documentation) should be resolved or formally closed.

---

## Section 7: Week-Shape Table (CIO Lens)

| Date | Rating | CIO-Relevant Events |
|------|--------|---------------------|
| Mar 15 | STANDARD | CIO methodology audit (10 recommendations). Floor inversion investigation. |
| Mar 16 | HIGH-COMPLEXITY | 2 audit policy changes approved. Action Registry created. 9 issues closed. |
| Mar 17 | STANDARD | Briefing audit (8/12 fixed). Publish skill first use. |
| Mar 18 | STANDARD | dev/active sort. Blog image matching. 7 memos delivered. |
| Mar 19 | HIGH-COMPLEXITY | 9 agents active (first time). ADR-059 + ADR-060 created. Mailbox v3. Agent 360 (9/9). |
| Mar 20 | STANDARD | PA plan. Capability audits. Innovation backlog created. |
| Mar 21 | HIGH-COMPLEXITY | 9 agents. PA briefing assembly. Cross-pollination first brief. M1 Tier 2-3. |
| Mar 22 | HIGH-COMPLEXITY | M1 Tier 3 complete. Gate #926 filed. E2E/AAXT proposal. PDR-004 ratified. |
| Mar 23 | HIGH-COMPLEXITY | #717 resolved (4-role, 90-min, zero PM mediation). |
| Mar 24 | HIGH-COMPLEXITY | Gates 3-4 verified. 6-act blog narrative. |
| Mar 25 | DAY OFF | |
| Mar 26 | STANDARD | Comms 13 pieces. Docs batch commit. Service disruption. |
| Mar 27 | DAY OFF | Service disruption recovery. |
| Mar 28 | STANDARD | PA Phase 0 complete. First blog-canonical publish. 4-day recovery. |
| Mar 29 | MINIMAL | Second blog publish. Publishing bug fixes. |
| Mar 30 | HIGH-COMPLEXITY | **Migration day**: 18 sessions, 12 roles. PA operational debut. Ship #036 drafted. |
| Mar 31 | STANDARD | Briefing maintenance. PA five-layer mapping. CXO UAT prep. Third blog publish. |
| Apr 1 | STANDARD | CIO endorses RFC-001. CLAUDE.md role fix. Shipping News launched. |
| Apr 2 | STANDARD | PA backlog audit (119 issues). HOST rename. Fourth blog publish. |
| Apr 3 | STANDARD | **M1 Gate: NOT PASSED** (0/7). Pattern-045 confirmed at scale. |
| Apr 4 | STANDARD | Lead Dev fixes #940. Klatch scaffolded probing Phase 1. PA drafts Piper Open. |
| Apr 5 | STANDARD | Lead Dev fixes remaining findings. Fifth blog publish. |
| Apr 6 | DAY OFF | |
| Apr 7 | HIGH-COMPLEXITY | **Strategic pivot**: "methodology > code." Gate round 2: 0/9. Vision V2.1. MUX analysis. |
| Apr 8 | HIGH-COMPLEXITY | **UAT breakthrough**: Five Whys → deprecated model. Round 3: 5/9. BYOC. Vision V2.2. |
| Apr 9 | STANDARD | #922 conversation continuity fix. #943 pre-flight fix. Dispatch mail gap. |
| Apr 10 | STANDARD | Gate round 4: PASS. M1 gate closed. Floor fabrication guardrail. |
| Apr 11 | STANDARD | **M1 Gate #926 closed.** Vision V2.3 adopted. Roadmap v15.0 adopted. M2 starts. |

---

## Section 8: Innovation Trajectory

| Domain | Mar 15 Status | Apr 11 Status | Trend |
|--------|--------------|---------------|-------|
| Excellence Flywheel | "Strong, accelerating" | **8 formulations, needs reformulation** | Concept strong; documentation degraded; reformulation in progress |
| Gate methodology | Proposed (CXO coherence check) | **Validated through 4 UAT rounds** | Proven. Fresh-account UAT + Colleague Test is the standard. |
| Multi-agent coordination | "Strong, maturing" | **Migration-proven** | 12-role migration with zero context loss |
| Pattern capture | "Moderate, needs improvement" (25-day latency) | **Self-approval policy in effect** | Pipeline latency resolved; Emerging status operational |
| Documentation currency | "Moderate, degrading" | **20/22 methodology docs silent** | methodology-23 created; systemic staleness persists |
| Infrastructure automation | "Strong, accelerating" | **Hooks + branch check + pre-commit** | Growing; session-start hook is load-bearing |
| Methodology-product convergence | "Strong, accelerating" | **"Methodology > code" adopted as strategic principle** | Convergence complete — methodology IS the product |
| Cross-project learning | Active (cross-pollination hub) | **RFC-001 endorsed; scaffolded probing available** | Ecosystem-level methodology sharing operational |
| Innovation capture | Active | **6 candidates this period; 2 recommended for formalization** | Healthy pipeline |

---

## Section 9: Recommendations

### Immediate (This Sprint)

| # | Action | Owner | Effort |
|---|--------|-------|--------|
| A1 | Publish Flywheel reformulation as `methodology-00-EXCELLENCE-FLYWHEEL.md` v2 | CIO + Docs | 1 hour (CIO writes; Docs formats + commits) |
| A2 | Resolve Hooks Phase 1: either do the systematic check or formally close with rationale | CIO | 30 min either way |
| A3 | Evaluate `excellence_flywheel_integration.py` for retirement or alignment | Lead Dev or Architect | 15 min |

### Near-Term (Before Next Audit)

| # | Action | Owner | Effort |
|---|--------|-------|--------|
| B1 | Docs Phase 3: update downstream Flywheel references (~146 files) | Docs | 2-3 sessions |
| B2 | Triage 20 silent methodology docs (verify/refresh/retire/redirect) | Docs + CIO review | 1-2 sessions |
| B3 | Document "indoor plumbing" scoping heuristic in methodology-core | CIO | 30 min |
| B4 | Formalize "Continuity memo before the seam" as Emerging pattern | CIO | 30 min (self-approval) |
| B5 | Document roundtable format (carried from Mar 15 audit) | CIO | 1 hour |
| B6 | Role briefings: replace Flywheel paraphrases with citation + reference path | Docs | 1 session |

### Structural (Ongoing)

| # | Action | Owner | Effort |
|---|--------|-------|--------|
| S1 | Add canonical term drift to weekly audit sweep (Flywheel + PDR-004 + other load-bearing vocabulary) | Docs | 15 min/week |
| S2 | Monitor ADR-045 (grammar) citation frequency — if it drops from product discussions, investigate | CIO | Passive |
| S3 | Evaluate scaffolded probing for PM's E2E/AAXT track when #927-930 enters implementation | CIO + Lead Dev | Assessment |

---

## Section 10: State of the Methodology — Summary Assessment

| Dimension | Rating | Trend | Notes |
|-----------|--------|-------|-------|
| Excellence Flywheel | **Concept strong; docs degraded** | Reformulating | 8 formulations → 3-layer canonical. Operational principles healthy. |
| Gate methodology | **Proven** | ↑ Validated | 4 UAT rounds. Colleague Test + fresh-account testing is the standard. |
| Multi-agent coordination | **Strong** | Stable | Migration-proven. Mailbox + memo + handoff protocols are load-bearing. |
| Pattern capture | **Strong** | ↑ Improved | Self-approval for Emerging. Pipeline latency resolved. |
| Documentation currency | **Weak** | Flat | 20/22 silent methodology docs. Flywheel drift is the symptom. |
| Infrastructure automation | **Strong** | ↑ Growing | Hooks, branch checks, pre-commit. Session-start hook is load-bearing. |
| Methodology-product convergence | **Defining** | ↑ Strategic | "Methodology > code" is now the project's strategic thesis. |
| Cross-project learning | **Strong** | ↑ Ecosystem | RFC-001, scaffolded probing, daily briefs. Four-source intelligence. |
| Audit discipline | **Good** | ↑ Trigger-based working | First trigger-based execution. Hooks monitoring is the carried debt. |

**Overall**: The methodology is operationally the strongest it has been. Its documentation is the weakest it has been. The gap between practice and documentation is the audit's central finding. The Flywheel reformulation and the downstream reference cleanup are the fix.

---

*M1 Methodology Audit conducted: April 17, 2026*  
*Next audit trigger: M2 sprint gate closure + 2 weeks*  
*Audit duration: ~2.5 hours (data gathering by PA + Docs; analysis + drafting by CIO)*
