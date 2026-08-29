# ADR-015: Wild Claim Verification Protocol

**Status**: Proposed
**Date**: August 17, 2025
**Decision Makers**: PM, Chief Architect, Chief of Staff

## Context

On August 15, 2025, during dual RAG analysis of session logs, we discovered that a widely-cited "7626x acceleration factor" lacked mathematical derivation. This claim had propagated through multiple analyses, appearing to gain credibility through repetition rather than verification.

Similar unverified claims discovered:
- "150x-500x performance improvements" from mocked tests, not production
- "<1ms federated search" measured dictionary lookups, not actual API calls
- "630x faster than planned" without baseline definition

This pattern poses serious risks:
- **Credibility Damage**: One exposed false claim undermines all legitimate achievements
- **Echo Chamber Effect**: AI agents perpetuate unverified claims from training data
- **Decision Distortion**: Resource allocation based on inflated metrics
- **Reputation Risk**: "Getting high on our own supply" perception

Stanford's 4-axis evaluation model emphasizes empirical validation, and our Agent Charter commits to intellectual honesty. We need systematic verification to maintain integrity.

## Decision

We will implement a **Wild Claim Verification Protocol** that requires mathematical proof and empirical validation for all extraordinary claims, particularly those exceeding 100x improvement.

### Core Components

1. **Wild Claim Triggers**
   ```python
   class ClaimVerifier:
       WILD_CLAIM_THRESHOLDS = {
           "performance_multiplier": 100,  # >100x requires proof
           "cost_reduction": 0.90,          # >90% reduction requires proof
           "accuracy_improvement": 0.50,    # >50% improvement requires proof
           "time_savings": 0.90,            # >90% time saved requires proof
       }

       def is_wild_claim(self, claim: Claim) -> bool:
           """Identify claims requiring extraordinary evidence"""
           return any(claim.exceeds_threshold(t) for t in self.WILD_CLAIM_THRESHOLDS)
   ```

2. **Verification Requirements**

   **For All Wild Claims**:
   - Baseline measurement with methodology
   - Mathematical derivation or calculation trail
   - Reproducible test scenario
   - Production validation (not just test environment)
   - Confidence intervals or error margins

   **Documentation Template**:
   ```markdown
   ## Claim: [Specific metric and improvement]

   ### Baseline
   - Measurement: [Original performance]
   - Methodology: [How measured]
   - Date: [When established]
   - Environment: [Test/Production]

   ### Improved Performance
   - Measurement: [New performance]
   - Methodology: [How measured, must match baseline]
   - Date: [When measured]
   - Environment: [Test/Production]

   ### Calculation
   ```math
   Improvement = (New - Baseline) / Baseline × 100
   ```

   ### Validation
   - [ ] Reproduced by independent party
   - [ ] Confirmed in production environment
   - [ ] Statistical significance verified
   ```

3. **Verification Workflow**

   ```mermaid
   graph TD
       A[Claim Made] --> B{Wild Claim?}
       B -->|No| C[Standard Documentation]
       B -->|Yes| D[Verification Required]
       D --> E[Baseline Documented?]
       E -->|No| F[Establish Baseline]
       E -->|Yes| G[Mathematical Proof]
       G --> H[Production Validation]
       H --> I{Verified?}
       I -->|No| J[Retract/Revise Claim]
       I -->|Yes| K[Document with Evidence]
   ```

4. **Claim Categories**

   **Green (Pre-verified)**:
   - Industry standard benchmarks
   - Peer-reviewed research claims
   - Vendor-documented specifications

   **Yellow (Trust but Verify)**:
   - Internal test results
   - Calculated projections
   - Theoretical maximums

   **Red (Extraordinary Evidence Required)**:
   - >100x improvements
   - Revolutionary breakthroughs
   - Claims contradicting established limits

5. **Anti-Patterns to Prevent**

   - **Repetition ≠ Validation**: Multiple sources citing same unverified claim
   - **Test ≠ Production**: Mocked service results extrapolated
   - **Peak ≠ Average**: Cherry-picked best case as typical
   - **Compound Inflation**: Multiplying uncertain figures

## Consequences

### Positive

1. **Credibility Protection**: Every claim defensible with evidence
2. **Trust Building**: Stakeholders know metrics are reliable
3. **Better Decisions**: Resource allocation based on reality
4. **Scientific Rigor**: Elevates AI development standards
5. **Anti-Hype**: Counters AI industry exaggeration tendency

### Negative

1. **Velocity Impact**: ~1-2 hours to properly verify wild claims
   *[Confidence: Medium - Based on complexity of establishing baselines and running tests]*
2. **Marketing Constraints**: Can't match competitors' inflated claims
3. **Documentation Overhead**: Detailed proof requirements
4. **Innovation Perception**: May appear less revolutionary

### Neutral

1. **Cultural Change**: Team must embrace "show your work" mentality
2. **Baseline Investment**: Time to establish proper baselines
3. **Tooling Needs**: Performance measurement infrastructure

## Implementation Plan

### Phase 1: Immediate (Week 1)
- Review all existing claims in documentation
- Flag unverified wild claims for validation
- Create baseline measurement infrastructure
- Document known-good benchmarks

### Phase 2: Systematic (Week 2)
- Implement ClaimVerifier utility
- Add verification gates to PR process
- Create claim documentation templates
- Train team on verification requirements

### Phase 3: Automated (Month 1)
- Automated claim detection in PRs
- Performance regression testing
- Baseline drift monitoring
- Verification dashboard

### Phase 4: Mature (Month 2+)
- Public verification reports
- Community validation program
- Standardized benchmark suite
- Industry verification standards advocacy

## Alternatives Considered

### Alternative 1: Post-Hoc Verification
**Description**: Verify claims only when challenged
**Rejected Because**: Damage already done, reactive not proactive

### Alternative 2: No Extraordinary Claims
**Description**: Never claim >10x improvements
**Rejected Because**: Undersells legitimate breakthroughs when they occur

### Alternative 3: Peer Review Only
**Description**: External validation for all claims
**Rejected Because**: Too slow, blocks velocity unnecessarily

## References and Influences

- **Stanford's 4-Axis Evaluation Model**: Emphasis on empirical validation
- **Scientific Method**: Hypothesis, test, reproduce, verify
- **Mythbusters Methodology**: "Failure is always an option"
- **Academic Publishing Standards**: Peer review and reproduction
- **Friday Night Discovery**: The 7626x wake-up call (August 15, 2025)

## Related ADRs

- ADR-014: Attribution-First Development (cite AND verify sources)
- ADR-016: Ambiguity-Driven Architecture (clear metrics for routing decisions)
- Agent Charter v1.0: Commitment to intellectual honesty

## Notes

The phrase "extraordinary claims require extraordinary evidence" (Carl Sagan, popularizing Laplace's principle) guides this protocol.

Example verification from our own claims:
- ❌ "150x performance" was from mocked tests *[Status: Retracted - failed verification]*
- ✅ "92% token reduction" has mathematical proof from CoD paper *[Status: Verified - external validation]*
- ⚠️ "10x productivity" needs production validation *[Status: Pending - aspirational claim]*

Success will be measured by:
- Zero unverified wild claims in production docs after 30 days
- All performance metrics include methodology
- External validation of at least one major claim
- Industry adoption of our verification standards
