# Pattern-062: Assembly Assumption

## Status

**Methodology-Elevated** (was Proven) — Identified February 2026, validated through M0 sprint wiring pass; principle graduated into the methodology corpus as Excellence Flywheel v2.0 Practice 5 ("Audit the Composition"). The Flywheel practice is now the canonical, actively-cited form; this entry remains the catalog record of origin. See `docs/internal/architecture/current/patterns/README.md` §"Pattern Status Levels" for the Methodology-Elevated definition (formalized 2026-05-28).

## Product Relevance

**Portable** — Any team building features in parallel slices will encounter this. Piper's users managing product development face the same composition risk.

## Context

When building a system through horizontal feature slices (each feature implemented and tested independently), a dangerous assumption emerges: if each feature works correctly in isolation, the composed system will work correctly. This assumption is false. Integration points between features contain implicit contracts that unit and feature tests don't verify.

This pattern was discovered during the M0 sprint (February 2026). Five features were implemented across three days, each with passing tests. When composed into the running system, 9 integration gaps were found — none detectable by any individual feature's test suite.

### Relationship to Pattern-045 (Green Tests, Red User)

Pattern-045 describes the symptom: tests pass but the user experience is broken. Pattern-062 identifies the *structural cause* at the feature-composition level. Green Tests, Red User can occur for many reasons (wrong assertions, missing edge cases, mock over-reliance). Assembly Assumption specifically addresses the case where tests are *genuinely correct* for their scope but the composition was never verified.

Pattern-045 is about test quality. Pattern-062 is about planning architecture.

## Problem

### The Failure Mode

A team plans work in horizontal slices:

```
Feature A: [designed] → [implemented] → [tested ✅] → "done"
Feature B: [designed] → [implemented] → [tested ✅] → "done"
Feature C: [designed] → [implemented] → [tested ✅] → "done"

System: [A + B + C] → 💥 integration failures
```

Each feature was planned, built, and verified in isolation. No step in the process required verifying that A's output format matches B's expected input, that B and C don't compete for the same state, or that the user journey crossing A → B → C maintains coherence.

### Why It Happens

Three forces converge to create this failure:

1. **Planning incentives favor decomposition.** Breaking work into independent slices makes estimation easier, enables parallel execution, and creates satisfying "done" checkpoints. The incentive structure rewards horizontal slicing even when vertical integration is the real risk.

2. **Test scoping follows implementation boundaries.** When Feature A is implemented in `feature_a.py`, tests are written for `test_feature_a.py`. The test boundary matches the implementation boundary, which means integration seams are systematically excluded from coverage.

3. **Implicit contracts are invisible.** Feature A might produce a `ConversationContext` object that Feature B consumes. If A populates 8 of 12 fields and B needs 10, both features "work" — A produces a valid object, B handles its inputs. The gap only appears when they're composed.

### Concrete Example: M0 Sprint

The M0 sprint implemented five Conversational Glue features:

- **#766**: "Main project" question recognition
- **#763**: Multi-intent decomposition
- **#767**: Soft invocation patterns
- **#769**: Formality calibration
- **#770**: Cross-turn state continuity

All passed their feature tests. The M0.1 wiring pass (Feb 18) found 9 integration gaps:

| Gap | Features Involved | Nature |
|-----|-------------------|--------|
| Entity tokens not flowing through narrative bridge | #766 ↔ narrative system | Output format mismatch |
| Soft invocation not triggering for personal agency phrases | #767 ↔ pre-classifier | Pattern coverage gap |
| Formality not consulting conversation history | #769 ↔ state continuity | Missing dependency |
| Cross-turn context not surviving intent decomposition | #770 ↔ #763 | State management conflict |
| *(5 additional gaps of similar character)* | Various | Various |

None of these were test failures. Each feature worked exactly as specified. The gaps existed in the spaces *between* specifications.

## Solution

### The Wiring Pass

After a set of horizontal features are individually complete, perform a dedicated **wiring pass** — a focused session whose sole purpose is verifying composition. The wiring pass is not debugging (you don't yet know what's broken). It's *discovery* (you're finding what was never specified).

### Wiring Pass Protocol

**1. Map the integration seams.** Before touching code, enumerate every point where Feature A's output becomes Feature B's input. Draw the data flow across all features in the sprint. This map itself often reveals gaps — "wait, who populates this field?"

**2. Write integration scenarios, not integration tests.** Start with user journeys that cross feature boundaries: "User mentions their main project, then asks a multi-part question about it, and Piper responds with appropriate formality." These scenarios are the *specification* for composition that was missing from horizontal planning.

**3. Walk the code path.** For each integration scenario, trace the actual execution path through the composed system. Don't run tests — read the code and verify that data flows correctly across boundaries. This is where implicit contract violations surface.

**4. Fix and test.** For each gap discovered, create a targeted integration test that would have caught it, then fix the gap. The integration test serves as the *specification* that was missing — it documents the implicit contract and prevents regression.

**5. Record the gaps.** Document what was found. The *pattern of gaps* is more valuable than any individual fix — it reveals systematic blind spots in how the team decomposes work.

### When to Schedule Wiring Passes

- After every sprint that delivers 3+ features touching shared infrastructure
- Before any gate review (the wiring pass is the gate's prerequisite, not a post-gate cleanup)
- When features were implemented by different agents or in different sessions (context boundaries increase composition risk)

### Planning Mitigation

The wiring pass is the reactive fix. The proactive mitigation is to include **vertical integration checkpoints** in horizontal sprint plans:

```
Sprint Plan (improved):
  Feature A: [implement] → [test]
  Feature B: [implement] → [test]
  Feature C: [implement] → [test]
  Wiring Pass: [map seams] → [integration scenarios] → [verify] → [fix]
  Gate Review: [only after wiring pass complete]
```

The wiring pass should be a planned work item with its own time estimate (typically 10-20% of total feature implementation time), not an afterthought.

## Usage Guidelines

### When to Apply

- Multi-feature sprints with shared state or data flow between features
- Work distributed across multiple agents or sessions
- Any system where features were designed independently but must compose
- Before declaring a sprint "complete" or passing a gate review

### When This Pattern Doesn't Apply

- Single-feature work with no integration points
- Refactoring within a single bounded context
- Infrastructure work that doesn't change feature behavior
- Features that are genuinely independent (no shared state, no data flow)

## Anti-Patterns

| Don't Do This | Why | Do This Instead |
|---------------|-----|-----------------|
| Skip the wiring pass because "all tests pass" | Tests verify slices, not composition | Schedule the wiring pass as a required sprint phase |
| Do the wiring pass after the gate review | Gaps found post-gate create rework and erode trust in the gate | Wiring pass is a gate *prerequisite* |
| Treat wiring gaps as "bugs" | They're specification gaps, not implementation errors | Track as integration debt discovered during composition |
| Plan only horizontal slices | Creates systematic composition blind spots | Include vertical integration checkpoints in sprint plans |
| Assume the last feature "wires everything together" | The last feature has its own scope; composition is a separate concern | Dedicate explicit time for composition verification |

## Related Patterns

- **Pattern-045 (Green Tests, Red User)**: The symptom this pattern explains at the structural level
- **Pattern-046 (Beads Completion Discipline)**: Ensures individual features complete fully before composition
- **Pattern-049 (Audit Cascade)**: The systematic audit methodology that can be applied during wiring passes
- **Pattern-037 (Cross-Context Validation)**: Validates across bounded contexts, complementary to wiring passes

## Evolution

### Discovery (February 18, 2026)
M0.1 wiring pass revealed 9 integration gaps after a 3-day sprint completed 5 features with passing tests.

### Naming (February 20, 2026)
CIO identified and named the pattern during Ship #031 weekly review. Recognized as Pattern-045 elevated one abstraction level — from test quality to planning architecture.

### Formalization (March 1, 2026)
Documented as Pattern-062 with full protocol and anti-patterns.

### Intent-Routing Manifestation (March 12, 2026)
Canonical retest (#884) revealed that individually correct components (classifier, handlers, adapters) were never composed correctly. Auth threading missing across 17 call sites, analysis handler existed but was never wired to OrchestrationEngine, adapter methods incomplete. Implementation pass rate jumped from 53.7% to 81.1% through wiring fixes alone — no classifier or AI changes needed.

### Product-Architecture Manifestation (March 14, 2026)
Four-role roundtable ("Are We Doing It Backwards?") independently diagnosed the same composition gap at the product level: the intent classifier worked correctly, the handlers worked correctly, but the composition of "classifier + handlers + no fallback" produced a broken experience for unmatched queries. Piper was worse than a generic LLM wrapper for anything outside pre-built handlers. Led to ADR-060 (Floor-First Routing Architecture).

### Contract Gap Manifestation (March 16, 2026)
PM QA testing exposed 5 bugs sharing one structural root cause: the classification layer was extended independently of the handling layer, and stubs absorbed the gap silently. Lead Dev sketched this as "Extension Without Integration" — a sub-pattern of Assembly Assumption operating at the layer-contract level. Led to the Action Registry (34 pairs) as the structural fix. **Pattern slot update (Apr 27, 2026)**: this sub-pattern is Pattern-064 (formalized by Architect Apr 28; promoted to Proven May 8 after Architect's May 4 review identified two in-the-wild instances). Pattern-063 was allocated to a sibling sub-pattern at the specification layer (Parallel-Authoring Drift, CIO Apr 27; promoted to Proven May 8). Pattern-065 (Continuity Memo Before the Seam, CIO Apr 27; Proven May 8) is a sibling sub-pattern at the institutional-knowledge layer. The 062 family is now complete: 062 (component) / 063 (vocabulary) / 064 (extension) / 065 (institutional-knowledge), all Proven.

### Pattern Elevation Note
Assembly Assumption has now manifested at four scales: code composition (M0 wiring pass), intent routing (canonical retest), product architecture (floor inversion), and layer contracts (extension without integration). Each scale required a different mitigation (wiring pass, canonical retest, floor-first routing, action registry) but the structural cause is identical: independently correct components with unverified composition.

## Success Metrics

- **Integration gaps found per wiring pass**: Track over time. A decreasing trend means planning is improving; zero means either the team has internalized composition thinking or the wiring pass isn't rigorous enough.
- **Post-gate integration failures**: Should drop to near zero if wiring passes are consistently performed before gates.
- **Wiring pass duration as % of sprint**: Should stabilize around 10-20%. If consistently higher, decomposition approach needs adjustment.

## References

### Documentation

- Omnibus log: February 18, 2026 (M0.1 wiring pass)
- Omnibus log: February 20, 2026 (CIO pattern identification)
- CIO weekly memo: February 20, 2026 (Ship #031 input)

### External Precedent

The Assembly Assumption is a known problem in systems engineering and hardware design, where integration testing is a formal discipline. Software development — particularly agile methodologies that emphasize small, independent stories — is structurally prone to this pattern because the planning framework itself incentivizes horizontal decomposition without mandating vertical verification.

---

*Pattern created: March 1, 2026*
*Evolution updated: March 21, 2026*
*Origin: M0 sprint wiring pass discovery*
*Author: CIO, with PM review*
*PM sign-off: March 21, 2026*
