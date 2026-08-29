# ADR-016: Ambiguity-Driven Architecture with Chain-of-Draft Integration

**Status**: Superseded (status corrected 2026-08-29)
**Date**: August 17, 2025
**Decision Makers**: PM, Chief Architect, Chief of Staff
**Classification**: Revolutionary Bundle (includes Chain-of-Draft Integration, Ambiguity Assessment, Three-Tier Orchestration)

## Context

Our research into agent architectures revealed a fundamental insight that challenges conventional wisdom: **solution path ambiguity, not computational complexity, should drive architectural decisions** for single vs. multi-agent systems.

This discovery emerged from:
1. Analysis of Rahul Vir's Framework 3: "Choose an Architecture Based on Problem's Complexity" (which actually emphasizes ambiguity)
2. Chain-of-Draft research showing 92% token reduction makes multi-agent systems economically viable
3. Industry patterns from Anthropic, Microsoft, IBM, and LangChain

The convergence of these insights, combined with our MCP federation and spatial intelligence capabilities, creates a paradigm shift in how we architect Piper Morgan's decision-making.

### Economic Transformation Claims

The economic implications require verification per ADR-015:

| Original Cost | Optimized Cost | Reduction | Verification Status |
|---------------|----------------|-----------|-------------------|
| Daily standups: $15 | $0.75 | 95% | Calculated from token reduction, needs production validation |
| Sprint planning: $125 | $6.25 | 95% | Calculated from token reduction, needs production validation |
| Quarterly analysis: $2,500 | $125 | 95% | Calculated from token reduction, needs production validation |

*Note: Cost reductions based on 92% token reduction from Chain-of-Draft paper (verified) applied to estimated token costs (unverified). Actual costs will vary based on model pricing and task complexity.*

## Decision

We will implement an **Ambiguity-Driven Architecture** that routes tasks based on solution path clarity rather than computational complexity, using Chain-of-Draft optimization to make multi-agent orchestration economically viable.

### Core Components

#### 1. Solution Path Assessment Framework

```python
class AmbiguityAssessor:
    """Evaluates solution path clarity, not task complexity"""

    def assess_solution_clarity(self, task: Task) -> float:
        """
        Returns clarity score 0.0-1.0 based on:
        - Precedent existence (have we solved similar before?)
        - Step predictability (can we enumerate the steps?)
        - Success criteria clarity (do we know what "done" looks like?)
        - Domain consensus (is there an accepted approach?)
        """
        indicators = {
            'precedent_exists': self.check_precedent(task),
            'steps_enumerable': self.can_enumerate_steps(task),
            'success_measurable': self.has_clear_success_criteria(task),
            'domain_consensus': self.check_domain_consensus(task)
        }
        return self.calculate_clarity_score(indicators)
```

#### 2. Three-Tier Orchestration Model

**Tier 1: Clear Path (Score > 0.8)**
- Single agent with tools
- Sequential execution
- Example: "Create GitHub issue for login bug"
- Architecture: Direct execution with CoD optimization

**Tier 2: Exploratory Path (Score 0.4-0.8)**
- Supervised multi-agent
- Human checkpoints at ambiguity points
- Example: "Improve user onboarding experience"
- Architecture: Orchestrator + specialized agents with approval gates

**Tier 3: No Clear Path (Score < 0.4)**
- Full multi-agent orchestration
- Debate-driven consensus building
- Example: "Predict competitor's next strategic move"
- Architecture: Blackboard pattern with emergent solutions

#### 3. Chain-of-Draft Integration

```python
class DebateDrivenCoD:
    """Enables rapid multi-agent consensus at 1/20th token cost"""

    def compress_reasoning(self, agent_thought: str) -> str:
        """Compress to 5-word expressions per CoD methodology"""
        # Example:
        # Original: "I believe we should prioritize the authentication
        #           feature because security is critical for enterprise..."
        # Compressed: "authentication→security→enterprise→critical→priority"
        return self.extract_semantic_core(agent_thought, max_words=5)

    def orchestrate_debate(self, agents: List[Agent], problem: str):
        """Orchestrate compressed debate until consensus"""
        debate_rounds = []
        while not self.consensus_reached(debate_rounds):
            round_contributions = []
            for agent in agents:
                compressed = self.compress_reasoning(agent.reason(problem))
                round_contributions.append(compressed)
            debate_rounds.append(round_contributions)

        return self.synthesize_consensus(debate_rounds)
```

#### 4. Economic Optimization

```yaml
token_economics:
  traditional_debate:
    tokens: 50000
    cost: $2.50
    time: 45s

  debate_driven_cod:
    tokens: 2500  # 95% reduction [Verified: CoD paper]
    cost: $0.125  # 95% reduction [Calculated: Based on token reduction]
    time: 2.3s    # 95% reduction [Estimated: Needs measurement]
    quality_correlation: 0.96  # Only 4% quality loss [Source: CoD paper]

  confidence_note: "Token reduction verified in research, cost/time extrapolated"
```

### Routing Examples

| Task | Clarity Score | Route | Rationale |
|------|--------------|-------|-----------|
| "Fix typo in README" | 0.95 | Single agent | Clear path, simple execution |
| "Generate test suite for auth module" | 0.85 | Single agent + CoD | Clear path but complex |
| "Improve team morale" | 0.3 | Multi-agent debate | No clear path, needs perspectives |
| "Optimize database performance" | 0.7 | Supervised multi-agent | Partially clear, needs exploration |
| "Predict market disruption" | 0.2 | Full orchestration | Highly ambiguous, emergent solution |

*Note: Clarity scores are illustrative. Actual scoring algorithm to be developed and calibrated through production usage.*

## Consequences

### Positive

1. **Economic Viability**: 92% token reduction makes multi-agent practical for routine tasks
2. **Better Decisions**: Ambiguous problems get appropriate multi-perspective analysis
3. **Resource Efficiency**: Clear problems avoid unnecessary orchestration overhead
4. **Adaptive Architecture**: System matches approach to problem nature
5. **Paradigm Shift**: Changes PM assistance from $2,500/quarter to $125/quarter

### Negative

1. **Assessment Overhead**: Must evaluate ambiguity before routing (adds ~100ms)
   *[Confidence: Medium - Estimated based on similar classification tasks]*
2. **Training Required**: Team needs to understand ambiguity vs. complexity distinction
   *[Confidence: High - Observed confusion in our own research process]*
3. **Debugging Complexity**: Multi-agent debates harder to trace than single agent
   *[Confidence: High - Known challenge from industry experience]*
4. **Quality Risk**: 4% degradation from CoD compression
   *[Confidence: High - Measured in CoD paper, but our implementation may vary]*

### Neutral

1. **Cultural Shift**: Move from "how complex?" to "how clear is the path?"
2. **Metrics Evolution**: New KPIs around ambiguity assessment accuracy
3. **Architecture Documentation**: Must explain when/why multi-agent triggers

## Implementation Plan

### Phase 1: Foundation (Week 1)
- Implement AmbiguityAssessor with basic heuristics
- Create clarity score benchmarks from existing tasks
- Document solution path patterns

### Phase 2: CoD Integration (Week 2)
- Implement compression algorithms
- Create debate orchestration framework
- Validate quality preservation

### Phase 3: Routing Logic (Week 3)
- Wire ambiguity assessment into QueryRouter
- Implement three-tier orchestration
- Add monitoring and metrics

### Phase 4: Production (Week 4)
- Deploy with feature flags
- A/B test against current architecture
- Measure token savings and quality

## Alternatives Considered

### Alternative 1: Complexity-Based Routing
**Description**: Use computational complexity as routing criterion
**Rejected Because**: Our research shows clear complex tasks succeed with single agents

### Alternative 2: Always Multi-Agent
**Description**: Use multi-agent for everything (Anthropic approach)
**Rejected Because**: 15x token cost unnecessary for clear-path problems

### Alternative 3: Always Single-Agent
**Description**: Force all problems through single agent (Cognition approach)
**Rejected Because**: Genuinely ambiguous problems need multiple perspectives

## References and Influences

- **Rahul Vir**: "The Agentic PM's Guide" (2025) - Framework 3 on ambiguity-based architecture
- **Chain-of-Draft Research**: arXiv:2502.18600v1 - 92% token reduction methodology
- **Anthropic**: Multi-agent research system architecture and debate patterns
- **Microsoft Magentic-One**: Dynamic orchestration for open-ended problems
- **Our Discovery**: Solution path clarity as architectural driver (August 17, 2025)

## Related ADRs

- ADR-001: MCP Integration (enables tool federation)
- ADR-013: MCP+Spatial Integration (provides context for ambiguity assessment)
- ADR-014: Attribution-First Development (credits Vir and CoD research)
- ADR-015: Wild Claim Verification (validates 92% token reduction)

## Notes

This ADR represents a paradigm shift in our architectural thinking. The key insight—that solution path ambiguity rather than computational complexity should drive architecture—fundamentally changes how we approach PM assistance.

The economic implications are staggering: what was a $2,500 quarterly PMF analysis becomes $125, making sophisticated multi-agent analysis accessible for routine PM work.

Success metrics:
- 90% accuracy in ambiguity assessment
  *[Target: Requires calibration through production usage]*
- 92% token reduction achieved in practice
  *[Target: Match research paper results]*
- <5% quality degradation from compression
  *[Target: Acceptable trade-off per paper]*
- 10x increase in multi-agent usage due to economics
  *[Aspirational: Depends on cost sensitivity of use cases]*
---

## Status correction (2026-08-29, Chief Architect — Architectural Review 2026, mechanical win #4)

**Status corrected Accepted → Superseded.** The Chain-of-Draft implementation this ADR's economics
rested on was deleted 2026-07-18 in the Tier-3 fix-or-delete pass (decisions.log; `services/
orchestration/` family), and the 92%-token-reduction premise was never independently validated
(see ADR-015's own verification protocol, filed the same day). No successor decision is needed —
the multi-agent economics question, if it returns, re-enters through the scope-bet gate. The ADR
remains as history; this note exists so the trail tells the truth about itself.
