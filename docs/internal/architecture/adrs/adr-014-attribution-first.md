# ADR-014: Attribution-First Development

**Status**: Proposed
**Date**: August 17, 2025
**Decision Makers**: PM, Chief Architect, Chief of Staff

## Context

Piper Morgan's development has benefited from numerous external sources: frameworks, research papers, open-source patterns, and community knowledge. As we formalize our Agent Charter and operational principles, we recognize that intellectual integrity requires systematic attribution of these influences.

Recent discoveries include:
- Rahul Vir's Agentic PM frameworks providing structural guidance
- Stanford's 4-axis evaluation model for comprehensive metrics
- Chain-of-Draft research enabling 92% token reduction
- Community patterns from LangChain, Anthropic, and others

Without systematic attribution, we risk:
- Appearing to claim others' work as our own
- Missing opportunities to contribute back to the community
- Accumulating "attribution debt" similar to technical debt
- Damaging credibility and relationships with the broader AI community

## Decision

We will adopt an **Attribution-First Development** methodology where acknowledging sources is as fundamental as writing tests or documentation.

### Core Components

1. **CITATIONS.md Maintenance**
   - Living document in `docs/governance/`
   - Structured format with categories (Frameworks, Research, Code Patterns, Tools)
   - Version controlled with semantic versioning
   - Regular audits for completeness

2. **Pattern → Citation Mapping**
   ```python
   # Example: When implementing CoD optimization
   # Citation: Chain-of-Draft (arXiv:2502.18600v1)
   def compress_reasoning(prompt: str) -> str:
       """Compress reasoning to 5-word expressions per CoD methodology"""
       ...
   ```

3. **Attribution Workflow Integration**
   - Pre-commit hooks check for unattributed patterns
   - PR template includes "New Influences" section
   - Weekly Pattern Sweep includes citation discovery
   - Monthly attribution audit against codebase

4. **Attribution Debt Tracking**
   - Treat missing attributions like technical debt
   - Create GitHub issues for attribution gaps
   - Track metrics: attributed vs. unattributed patterns
   - Regular debt reduction sprints

5. **Operational Tooling**
   ```yaml
   # .pre-commit-config.yaml
   - id: attribution-check
     name: Verify Attribution
     entry: scripts/validation/citation_checker.py
     files: \.(py|md)$
   ```

### Attribution Standards

**Required Attribution**:
- External frameworks adapted or implemented
- Research papers influencing architecture
- Code patterns from other projects
- Significant algorithmic approaches
- Theoretical concepts applied

**Attribution Format**:
- In code: Comment with citation at point of use
- In docs: Inline references with full citation in CITATIONS.md
- In ADRs: Explicit "Influences" section
- In commits: Note new attributions in message

**Not Required** (but encouraged):
- Common programming patterns
- Standard library usage
- Trivial implementations
- General knowledge

## Consequences

### Positive

1. **Ethical Leadership**: Sets industry standard for AI development integrity
2. **Community Building**: Creates goodwill and collaboration opportunities
3. **Knowledge Lineage**: Clear tracking of intellectual heritage
4. **Legal Protection**: Reduces risk of plagiarism claims
5. **Learning Acceleration**: The Attribution Flywheel:
   ```
   Discover → Attribute → Share → Community Learns →
   → They Share Back → We Discover More
   ```

### Negative

1. **Development Overhead**: ~5-10 minutes per PR for attribution review
   *[Confidence: Medium - Estimated based on similar review processes, needs measurement]*
2. **Initial Debt**: Need to retrofit existing code with attributions
3. **Tooling Investment**: Time to build attribution infrastructure
4. **False Positives**: Attribution checker may flag common patterns

### Neutral

1. **Cultural Shift**: Team must internalize attribution as core practice
2. **Process Evolution**: Workflows will adapt around attribution needs
3. **External Visibility**: Our attribution practices become public

## Implementation Plan

### Phase 1: Foundation (Week 1)
- Create initial CITATIONS.md with known influences
- Add attribution section to PR template
- Document attribution standards in contributing guide

### Phase 2: Automation (Week 2)
- Implement basic citation_checker.py
- Add pre-commit hook (warning only)
- Integrate with Pattern Sweep

### Phase 3: Enforcement (Week 3)
- Citation checker becomes blocking
- Attribution debt dashboard
- Monthly audit process established

### Phase 4: Maturity (Month 2+)
- Pattern → Citation mapping database
- Automated attribution suggestions
- Community attribution contributions

## Alternatives Considered

### Alternative 1: Ad-hoc Attribution
**Description**: Attribute on case-by-case basis without system
**Rejected Because**: Inconsistent, easily forgotten under pressure

### Alternative 2: Legal Minimum Only
**Description**: Only attribute where legally required
**Rejected Because**: Misses opportunity for community building and ethical leadership

### Alternative 3: Post-hoc Attribution
**Description**: Add attributions during quarterly reviews
**Rejected Because**: Attribution debt accumulates, context lost

## References and Influences

- **Agent Charter Framework**: Rahul Vir's "The Agentic PM's Guide" (2025)
- **Technical Debt Metaphor**: Ward Cunningham (1992)
- **Open Source Attribution Practices**: Apache Foundation, Linux Kernel
- **Academic Citation Standards**: ACM, IEEE guidelines
- **Ethics in AI Development**: Partnership on AI recommendations

## Related ADRs

- ADR-015: Wild Claim Verification Protocol (ensures cited metrics are valid)
- ADR-000: Meta-Platform Vision (attribution as platform differentiator)
- Agent Charter v1.0: Section 10 (Attribution and Acknowledgments)

## Notes

This ADR itself demonstrates attribution-first development by explicitly crediting all influences on our attribution methodology. The recursive nature (attributing our attribution approach) exemplifies the principle.

The 5-10 minute overhead per PR is estimated based on:
- 2 minutes: Developer self-check
- 2 minutes: Automated tool run
- 1 minute: Review suggestions
- 5 minutes: Add missing attributions (worst case)

Success metrics:
- 100% of external patterns attributed within 30 days
  *[Target: Aspirational but achievable with systematic review]*
- Zero attribution debt growth after Month 1
  *[Target: Requires disciplined process]*
- Positive community feedback on attribution practices
  *[Measure: Survey and social media sentiment]*
- At least one upstream contribution based on attribution relationships
  *[Target: Demonstrates reciprocal value]*
