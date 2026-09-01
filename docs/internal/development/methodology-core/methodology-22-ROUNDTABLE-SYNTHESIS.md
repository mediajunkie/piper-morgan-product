# Methodology-22: Roundtable Synthesis

## Purpose

The Roundtable Synthesis is a structured decision-making process for strategic questions where multiple leadership perspectives are needed. It produces high-quality decisions through independent parallel analysis followed by synthesis, avoiding anchoring bias and surfacing genuine convergence.

## When to Use

**Trigger conditions** (any one is sufficient):
- PM identifies a strategic question that crosses role boundaries
- A product, architectural, or methodology decision would benefit from multiple perspectives before commitment
- A "nagging feeling" or observed failure needs diagnosis before action
- A significant change in direction is being considered

**Not appropriate for**:
- Routine decisions within a single role's authority
- Implementation details that the Lead Dev or Architect can resolve independently
- Time-critical decisions where parallel memo writing would cause unacceptable delay
- Questions with obvious answers that don't require multi-perspective analysis

## Process

### Phase 1: Prompt (PM)

PM poses a strategic question to 3-4 leadership roles simultaneously. The question should be:
- Open-ended enough to allow different framings
- Specific enough to produce actionable output
- Accompanied by context (screenshots, data, observations) that grounds the discussion

**Critical**: Each role receives the same prompt at approximately the same time, with no access to other roles' responses. This prevents anchoring — the value of the roundtable is that convergence emerges independently.

PM may suggest "no anchoring — write independently" explicitly, though this is implicit in the parallel delivery.

### Phase 2: Independent Memos (3-4 Roles, Parallel)

Each invited role writes a memo addressing the question from their domain perspective:
- **PPM**: Product implications, roadmap impact, user experience consequences
- **CXO**: User experience, Colleague Test assessment, voice and interaction design
- **Chief Architect**: Technical feasibility, architectural implications, risk assessment
- **CIO**: Methodology connections, innovation landscape, pattern recognition

Memos should be substantive (not just "I agree"), cite specific evidence, and include the role's honest assessment even if it might be unpopular. Each memo should conclude with specific questions for the other roles.

**Typical duration**: 30-60 minutes per role from prompt to memo delivery.

### Phase 3: Synthesis (PPM)

PPM reads all memos and produces a synthesis document that:

1. **Maps convergence**: Where do the memos independently agree? The strength of agreement (2/4, 3/4, 4/4) is itself a signal.
2. **Preserves productive divergence**: Where do the memos disagree or emphasize different concerns? These tensions often contain the most valuable insights.
3. **Identifies gaps**: What did no memo address that matters?
4. **Proposes concrete actions**: Sequenced, owned, with timelines.
5. **Attributes perspectives fairly**: Each role's framing should be represented accurately — check by asking "would this role recognize their position in my summary?"

The synthesis is a decision document, not a summary. It resolves disagreements where possible and flags unresolved tensions for PM decision.

### Phase 4: Review Cycle (All Roles)

PM circulates the synthesis to all participants for feedback. Reviewers should flag:
- Misrepresentation of their position
- Missing constraints or risks
- Factual corrections (scope estimates, technical feasibility)
- New concerns raised by seeing others' perspectives

**Typical duration**: 1-2 hours from circulation to revised synthesis.

### Phase 5: Ratification (PM)

PM reviews the revised synthesis and either:
- **Ratifies**: Synthesis becomes binding direction. PM adds to project knowledge.
- **Requests revision**: Specific concerns sent back to PPM or relevant role.
- **Overrides**: PM disagrees with synthesis and makes a different call. This is rare but the PM's prerogative — document the reasoning.

Ratified syntheses are the authoritative record of the decision. Future agents trace decisions back to these documents.

## Artifacts Produced

| Artifact | Author | Purpose |
|----------|--------|---------|
| Prompt | PM | Frames the question |
| Independent memos (3-4) | Invited roles | Domain-specific analysis |
| Synthesis | PPM | Decision document |
| Revised synthesis | PPM (with reviewer input) | Final binding direction |
| Issue draft (if applicable) | PPM or relevant role | Implementation specification |

## Template: Synthesis Document

```markdown
# Roundtable Synthesis: [Topic]

**To**: PM (xian)
**From**: PPM (synthesizer)
**Date**: [date]
**Re**: Synthesis of [N] leadership memos on [topic]
**Input memos**: [list with dates]

---

## Consensus: [Summary of agreement level]

### The Diagnosis ([N]/[N] agree)
[What the memos converge on]

### The Immediate Action ([N]/[N] agree)
[What everyone recommends doing first]

### The Principle
[Any durable principle that emerged]

---

## Where the Memos Diverge (Productively)
[Tensions, different emphases, unresolved questions]

---

## What's Not in These Memos
[Gaps no one addressed]

---

## Recommended Actions

### Immediate
[Actions for this sprint]

### Soon
[Actions for this or next sprint]

### Later
[Actions for future sprints]

---

## [Closing reflection on what this means]

---

*PPM Synthesis | [date]*
*Input: [N] roundtable memos ([roles])*
```

## Case Studies

### Roundtable 1: M1 Sprint Planning (March 10, 2026)

**Prompt**: PPM created a briefing on M1 scope and expansion risk, sent to CXO and Architect for parallel review.

**Outcome**: CXO recommended fresh-account testing and UI polish track. Architect recommended deferring WebSocket (#557) and KMS (#482), proposed spec pipeline for epics. PPM synthesized into the M1 sprint plan: 16 issues, 4 phases, explicit wiring pass. PM made final scope calls (#715 promoted, #372 committed to M3).

**Convergence signal**: Both independently flagged WebSocket as high-risk. Spec pipeline appeared in both memos.

**Time**: One evening — PPM briefing at 9:58 PM, CXO and Architect responses by 10:35 PM, PPM synthesis next morning.

### Roundtable 2: "Are We Doing It Backwards?" — The Floor (March 14, 2026)

**Prompt**: PM shared screenshot of Piper refusing a reasonable PM query and asked: "Why does Piper function less well at general communication than a generic LLM-wrapper chatbot?"

**Outcome**: 4/4 unanimous convergence on diagnosis (layer inversion — ceiling without floor) and immediate action (route UNKNOWN to LLM with context). Each role contributed a distinct framing: PPM (layer inversion), CXO (bouncer vs. concierge), Architect (classify but don't respond), CIO (cliff at boundary). PPM synthesis ratified with three revisions from reviewers. LLM-FLOOR issue filed, implemented same day.

**Convergence signal**: Strongest in project history. All four memos independently recommended the same one-thing-to-change-first. The four-framing table became a reference artifact.

**Time**: ~3 hours from PM prompt to ratified synthesis. Implementation by evening.

### Roundtable 3: Floor Inversion Architecture (March 16, 2026)

**Prompt**: Lead Dev delivered floor inversion architecture report and advisory memo with three infrastructure questions, sent to PPM, Architect, and CXO.

**Outcome**: Three-way convergence on all three questions (quality monitoring, cost management, model selection). Architect refined the Action Gate criterion. CXO delivered voice guidance for floor responses. PPM synthesized with addendum connecting CXO's earlier failure gap analysis to the new architecture. All three infrastructure questions answered definitively.

**Convergence signal**: Independent agreement on every advisory question. The CXO's "never say I can't" principle and the Architect's "no actions from floor" constraint both appeared independently and were incorporated as non-negotiable constraints.

**Time**: ~2 hours from memos received to synthesis delivered.

## Why This Works

The roundtable's effectiveness comes from three properties:

**Independence prevents anchoring.** When roles write simultaneously without seeing each other's work, convergence is genuine — it means the evidence points the same direction, not that everyone agreed with the first person to speak.

**Diverse framings reveal facets.** The March 14 roundtable produced four complementary framings of the same problem. No single perspective would have been as complete. The PPM's job is to see how they fit together, not to pick a winner.

**Synthesis creates commitment.** A ratified synthesis is a shared decision that every participant helped shape. It's harder to undermine or relitigate than a unilateral call, because every role's concerns are visibly addressed in the document.

## Anti-Patterns

*(Folded in from `pattern-059-leadership-caucus.md` on absorption, 2026-09-01 — see note at end of file.)*

| Anti-Pattern | Why It's Wrong | Correction |
|--------------|----------------|------------|
| Roundtable for single-domain decisions | Overkill; wastes reviewer time | Use direct consultation or mailbox |
| Skipping the roundtable for cross-cutting strategic questions | Creates alignment debt; the decision may need relitigating later | Convene the roundtable upfront |
| No independent-delivery discipline | Anchoring — later memos echo the first instead of reasoning independently | Deliver the prompt to all roles at approximately the same time, with no visibility into others' answers |
| Synthesis as pure summary | Fails to resolve tensions or propose action; not doing the synthesizer's job | Synthesis must make at least one decision or identify at least one gap |
| Full participant roster always | Not every strategic question needs every role | Invite only roles with real domain standing on the question |

## Differentiation: Roundtable Synthesis vs. Multi-Agent Coordination (Pattern-029)

*(Folded in from `pattern-059-leadership-caucus.md` on absorption — the same distinction the caucus pattern drew against P-029 applies here.)*

Roundtable Synthesis and [Pattern-029: Multi-Agent Coordination](../../architecture/patterns/pattern-029-multi-agent-coordination.md) both involve multiple agents but serve different purposes:

| Dimension | Roundtable Synthesis (m-22) | Pattern-029 (Multi-Agent Coordination) |
|-----------|------------------------------|----------------------------------------|
| **Domain** | Leadership alignment | Technical execution |
| **Purpose** | Converge on a strategic decision before work begins | Coordinate parallel implementation work |
| **Participants** | Advisory roles (PPM, CXO, Architect, CIO) + PM | Coding agents |
| **Timing** | Before execution | During execution |
| **Output** | A ratified synthesis document — decision, assignments, direction | Code, tests, validated changes |
| **Coordination mode** | Independent parallel memos, then synthesis | Cross-validation, handoffs, parallel phases |

**In practice**: A ratified roundtable synthesis produces the decision and assignment that triggers a Multi-Agent Coordination deployment. They are sequential, not competing — one decides *what* and *how*; the other *executes*.

## Common Failure Modes

**Anchoring**: If one memo is shared before others are complete, subsequent memos anchor to it. Maintain independence through parallel delivery.

**Consensus theater**: If all memos just agree without adding distinct perspectives, the roundtable didn't need to happen. The synthesizer should note when this occurs — it may mean the question was too narrow or the answer too obvious.

**Synthesis as summary**: The synthesis must make decisions and propose actions, not just restate what everyone said. If the synthesis doesn't resolve at least one tension or identify at least one gap, it's not doing its job.

**Staleness window**: If the synthesis takes too long, the context may shift (as happened with the CXO failure gap memo — correct on March 13, partially obsolete by March 16). The synthesizer should note when input documents may have been superseded by subsequent work.

---

*Methodology-22 | Created March 21, 2026*
*Based on 3 successful applications (March 10, 14, 16, 2026)*
*Author: PPM, in response to HOSR Agent 360 action item*
