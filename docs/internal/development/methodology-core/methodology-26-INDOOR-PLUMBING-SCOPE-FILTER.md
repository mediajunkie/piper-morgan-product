# Indoor Plumbing vs. Bathing Experience — Scope Filter

## Overview

The **Indoor Plumbing vs. Bathing Experience** scope filter is a one-question decision rule applied at scope-definition time to catch scope errors *before* they become sprint work. It asks of any candidate feature, capability, or integration:

> *"Is this indoor plumbing (commodity, use existing infrastructure) or the bathing experience (differentiator, build it)?"*

The filter operates the same way the object model grammar (*"Entities experience Moments in Places"*) does — as a test that catches scope errors at their cheapest moment, before resources commit to building commodity work that doesn't differentiate.

This methodology entry was formalized April 27, 2026, per audit recommendation B3 (`methodology-audit-2026-04-17.md` §3.3). It originated from PA's backlog deep review work, where it was applied repeatedly to justify ~12 issue closures.

## Why This Methodology

### The Failure Mode It Prevents

Without an explicit scope filter, project teams systematically over-build infrastructure. Three forces converge:

1. **"We could build that"** is always true. Engineering capacity exists; therefore any feature *can* be built. The capacity question is not the scope question.
2. **NIH bias** (Not Invented Here) makes building feel safer than depending. Building gives full control; depending introduces a risk surface. The bias is rational at the local level and damaging at the strategic level.
3. **Commodity infrastructure has plugins available**. MCP plugins, third-party integrations, well-supported open-source libraries — all of these solve infrastructure problems that the team would otherwise spend sprint capacity rebuilding. The plugin/integration option is structurally invisible until someone names it.

The scope filter forces the question explicitly: is this work *differentiating*, or is it *commodity*? If commodity, plug it in; don't build it. Sprint capacity belongs to the differentiator.

### Why "Indoor Plumbing" and "Bathing Experience"

The metaphor is intentional and stable. Indoor plumbing is essential infrastructure — when it works, no one notices; when it breaks, everything falls apart; building it from raw materials is technically possible but obviously absurd when functioning systems exist. The bathing experience is what users actually pay for — temperature, pressure, ritual, ambiance. The two are necessarily related (no plumbing, no bath) but compete for attention and resources.

For Piper Morgan specifically: the differentiator stack (context methodology + conscious floor + artifact persistence + trust graduation) is the bathing experience. Authentication, third-party API integration, file storage, search infrastructure, transcript fetching — these are indoor plumbing. The team's sprint capacity should be reserved for the differentiators.

## When to Apply

### Apply this filter when

- Scoping a new capability, feature, or integration during sprint planning
- Triaging issues in a deep-review pass (PA's Apr 2 backlog audit was the canonical application)
- Considering whether to take on infrastructure work in-house vs. integrate
- Deciding whether to extend an existing system surface vs. plug in an alternative
- Drafting the issue-creation gate question: *"is this commodity or differentiator?"*

### This filter does not apply when

- The candidate is clearly platform-essential (CI infrastructure, deployment, basic auth) — these are *foundation*, not commodity, and have to be built or chosen carefully
- The work is integration glue between differentiators (the seams are themselves differentiating)
- The team is genuinely innovating in commodity space (rare; would need explicit justification)

## Core Principle

### The Decision Tree

```
Candidate work surfaces
       │
       ▼
┌─────────────────────────────────┐
│ Is this differentiating         │
│ for users, or commodity?        │
└─────────────────────────────────┘
       │
   ┌───┴────────┐
   ▼            ▼
 Differentiating  Commodity
   │            │
   ▼            ▼
 Build it     Is there an
   │         existing plugin /
   │         integration / library?
   │            │
   │        ┌───┴────┐
   │        ▼        ▼
   │       Yes      No
   │        │        │
   │        ▼        ▼
   │       Use it   Investigate
   │                why none
   │                exists before
   │                building
   ▼
 Sprint capacity
```

### The "Why None Exists" Branch

If a candidate is clearly commodity but no plugin or integration is available, that's itself a signal. Either:

- The commodity is too new (ecosystem hasn't caught up) — fine, but worth noting; might be worth waiting one cycle
- The commodity has a well-known reason no one ships it (security, licensing, fragmentation) — investigate before building, because the same reason applies to your build
- The commodity is genuinely something only your team needs (rare; usually misclassified — it might actually be differentiating)

Do not skip the "why none exists" question. Commodity work that no one else has done is usually misclassified.

## Application Examples

### From PA's Backlog Deep Review (April 2, 2026)

PA closed 12 issues across the backlog using this filter. Sample dispositions:

- **Slack integration** → indoor plumbing (use MCP plugin) → close direct-build issue
- **Custom auth flows** → indoor plumbing (use platform auth) → close
- **Email parser** → indoor plumbing (commodity NLP, use existing libs) → close direct-build
- **Conscious floor** → bathing experience → keep, prioritize
- **Trust graduation system** → bathing experience → keep, expand spec
- **Context-assembly with AAXT** → bathing experience → keep, central to M2

The pattern: any capability the user perceives as part of "Piper" (the bathing experience) gets sprint capacity. Any capability that's about *getting data in or out* (the plumbing) gets a plugin or integration.

### From the Differentiator Stack (Roadmap v15.0)

Vision V2.3's differentiator stack is the formal expression of the bathing experience: the four pillars are explicitly named as the things sprint capacity should be reserved for. M2-M5 are organized around them rather than around implementation domains.

The roadmap restructure (Apr 8-11) was itself an application of the indoor-plumbing filter at the strategic level: "what should our roadmap *actually* be about?" The answer was the differentiators, not the implementation work that supports them.

### From Issue-Creation Discipline

When filing a new issue, the issue-creation gate now includes (implicitly per practice, will be explicit per this methodology entry): *"is this work commodity or differentiator?"* Commodity issues should explicitly cite the integration alternative being chosen instead, or justify build-over-integrate with reasoning. Differentiator issues should explicitly tie back to a Vision pillar or roadmap milestone.

## Anti-Patterns

| Don't Do This | Why | Do This Instead |
|---|---|---|
| Build commodity infrastructure because "we could" | Sprint capacity is the constraint, not engineering ability | Apply the filter explicitly; choose plugin/integration when commodity |
| Skip the "why none exists" check on commodity-with-no-plugin | Often signals misclassification or hidden cost | Investigate before building; the absence of an existing solution is information |
| Apply the filter only to large work items | Small commodity work accumulates into large opportunity cost | Apply the filter to anything ≥1 sprint of work, including bundled small items |
| Treat "we have engineering capacity" as the scope question | Capacity availability ≠ strategic fit | Capacity is the budget; the filter is the spend test |
| Use NIH bias as a tiebreaker | Build vs. integrate has structural cost differences (maintenance, security, opportunity) | Default to integrate-when-commodity; reserve build-for-commodity for explicitly justified cases |

## Related Methodologies and Patterns

- **Methodology-04 (Architectural Agility)**: the filter operates on the architectural-agility principle — keep flexibility where it matters, commit where it differentiates.
- **Pattern-049 (Audit Cascade)**: a backlog audit that applies the indoor-plumbing filter is a specific kind of audit cascade (scope cascade rather than implementation cascade).
- **Object-model grammar** ("Entities experience Moments in Places"): a peer scoping filter that catches a different class of scope error (data-shape errors). Both filters operate the same way — short, memorable, applied at scope-definition time, surfaces wrong scoping cheaply.
- **Vision V2.3 differentiator stack**: the formal expression of the bathing-experience side of the filter.
- **Roadmap v15.0**: organizational manifestation — sprint structure built around the differentiator stack rather than implementation domains.

## Evolution

### Origin (March–April 2026)
PA introduced the indoor-plumbing/bathing-experience framing during backlog deep review work. The metaphor stabilized through repeated application; no single moment of formal coinage.

### Strategic Adoption (April 8–11, 2026)
Vision V2.3 + Roadmap v15.0 ratified the differentiator-stack framing — the bathing-experience side of the filter became the project's organizing principle. Twelve issue closures during backlog deep review were justified using this filter.

### Audit Recommendation (April 17, 2026)
M1 methodology audit §3.3 recommended formalizing as a methodology-core entry: *"Document as a scoping heuristic in methodology-core, not as a numbered pattern. It's a principle, not a recurring failure mode."*

### Filing (April 27, 2026)
Filed under CIO authority per PM concurrence on M1 audit recommendation B3. Status: current. Operational across PA backlog work, sprint planning, and issue-creation gate.

## References

### Origin Material

- **PA backlog deep review (Apr 2, 2026)**: 12 issue closures justified using this filter
- **Vision V2.3** (`docs/internal/planning/current/vision.md`): differentiator stack as bathing-experience formalization
- **Roadmap v15.0**: M2-M5 organized around differentiator stack
- **CIO M1 methodology audit (Apr 17)**: §3.3 ("'Indoor Plumbing vs. Bathing Experience' Scope Filter") — the recommendation that produced this entry

### Related Documents

- **Methodology-04 (Architectural Agility)**: peer principle on flexibility-vs-commitment
- **Object-model grammar** (ADR-045 + Vision): peer scoping filter
- **`docs/internal/planning/current/vision.md`**: differentiator-stack canonical

---

*Methodology entry created: April 27, 2026*
*Origin: PA backlog deep review, March–April 2026*
*Author: CIO (formalizing PA's operational coinage)*
*Status: Filed per PM concurrence on M1 audit recommendation B3*
