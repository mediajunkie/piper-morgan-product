# Pattern-039: Feature Prioritization Scorecard

## Status

**Deprecated** — never validated or adopted in practice; status was template-contaminated (all four tiers listed); retired 2026-06-17 per stale-pattern triage

## Context

Product teams often struggle with "everything is priority one" syndrome, where every feature request is treated as equally urgent and important. This leads to:

- **Overwhelming backlogs**: Everything must be done, creating analysis paralysis
- **Poor resource allocation**: High-effort, low-value features consume team capacity
- **Difficult stakeholder conversations**: No quantified basis for saying "no"
- **Technical debt accumulation**: Maintenance work consistently deprioritized
- **Strategic misalignment**: Features built that don't advance product goals

Traditional prioritization methods (gut feel, HIPPO - Highest Paid Person's Opinion) lack transparency and rigor. This pattern provides a quantified framework for feature prioritization decisions.

### Inspiration

This pattern emerged from Ted Nadeau's observation: "Everything is priority one & of equal importance... doing things even when they are difficult and/or of low value."

## Pattern Description

The **Feature Prioritization Scorecard** is a quantified decision framework that scores features on six factors: three cost factors (Effort, Risk, Support Cost) and three benefit factors (User Value, Market Competitiveness, Strategic Alignment).

### Core Concept

```
Priority Score = (User Value + Market + Strategic) / (Effort + Risk + Support)

Higher score = Higher priority
```

### Key Components

**Cost Factors** (lower is better, scored 1-5):
1. **Implementation Effort**: Development time required
2. **Risk**: Technical complexity and unknowns
3. **Support Cost**: Ongoing maintenance burden

**Benefit Factors** (higher is better, scored 1-5):
1. **User Value**: Impact on core workflow
2. **Market Competitiveness**: Table stakes vs differentiation
3. **Strategic Alignment**: Enables other features/capabilities

### Decision Thresholds

- **Score > 1.5**: Do now (P0/P1)
- **Score 1.0-1.5**: Do soon (P2)
- **Score 0.5-1.0**: Do later (P3)
- **Score < 0.5**: Don't do (or drastically simplify)

## Implementation

### Structure

```python
# Feature scoring data structure
feature_scorecard = {
    "name": "Feature Name",
    "cost": {
        "effort": 1-5,      # 1=<8hrs, 3=1-2 weeks, 5=>1 month
        "risk": 1-5,        # 1=known, 3=some unknowns, 5=research needed
        "support": 1-5      # 1=self-contained, 3=updates needed, 5=high ops
    },
    "benefit": {
        "user_value": 1-5,  # 1=nice-to-have, 3=improves UX, 5=differentiator
        "market": 1-5,      # 1=optional, 3=expected, 5=advantage
        "strategic": 1-5    # 1=standalone, 3=enables 1-2, 5=platform capability
    }
}

# Calculate priority score
def calculate_priority(scorecard):
    cost_total = sum(scorecard["cost"].values())
    benefit_total = sum(scorecard["benefit"].values())
    return benefit_total / cost_total

# Assign priority tier
def get_priority_tier(score):
    if score > 1.5: return "P0/P1"
    if score >= 1.0: return "P2"
    if score >= 0.5: return "P3"
    return "Don't Do"
```

### Scoring Guide

#### Implementation Effort (1-5)
- **1**: < 8 hours (quick win, minimal change)
- **2**: 1-3 days (small feature, isolated change)
- **3**: 1-2 weeks (medium feature, multiple components)
- **4**: 3-4 weeks (large feature, cross-cutting)
- **5**: > 1 month (major initiative, architectural change)

#### Risk (1-5)
- **1**: Known patterns, low unknowns, reversible
- **2**: Mostly known, some complexity, testable
- **3**: Some unknowns, moderate complexity, dependencies
- **4**: Significant unknowns, high complexity, external deps
- **5**: Research needed, uncharted territory, high stakes

#### Support Cost (1-5)
- **1**: Self-contained, no ongoing maintenance
- **2**: Occasional updates, low operational overhead
- **3**: Regular updates needed, moderate ops burden
- **4**: Frequent updates, significant operational overhead
- **5**: High ops burden, dedicated support required

#### User Value (1-5)
- **1**: Nice-to-have, minimal workflow impact
- **2**: Improves convenience, minor workflow enhancement
- **3**: Improves core workflow, noticeable benefit
- **4**: Major workflow enhancement, high user satisfaction
- **5**: Core differentiator, essential to user success

#### Market Competitiveness (1-5)
- **1**: Optional feature, no competitive pressure
- **2**: Nice to have, improves position slightly
- **3**: Expected by users, meets market baseline
- **4**: Competitive advantage, ahead of alternatives
- **5**: Unique differentiator, defines category

#### Strategic Alignment (1-5)
- **1**: Standalone feature, no strategic enablement
- **2**: Supports 1 other feature, minor alignment
- **3**: Enables 1-2 features, moderate alignment
- **4**: Enables 3-5 features, strong platform value
- **5**: Platform capability, unlocks many future features

### Code Example

```python
# Real examples from Piper Morgan roadmap

features = {
    "python_311_upgrade": {
        "name": "Python 3.11 Upgrade",
        "cost": {"effort": 2, "risk": 1, "support": 1},  # 4-8 hours, low risk
        "benefit": {"user_value": 2, "market": 1, "strategic": 3},  # Security + perf
        # Score: 6/4 = 1.50 → P2 (Do soon)
    },
    "mobile_app": {
        "name": "Native Mobile App",
        "cost": {"effort": 5, "risk": 4, "support": 4},  # 3-6 months, high risk
        "benefit": {"user_value": 3, "market": 3, "strategic": 3},  # User convenience
        # Score: 9/13 = 0.69 → P3 (Wait for demand)
    },
    "vscode_dev_setup": {
        "name": "VSCode Developer Setup Package",
        "cost": {"effort": 1, "risk": 1, "support": 1},  # 2-3 hours, zero risk
        "benefit": {"user_value": 3, "market": 2, "strategic": 3},  # DX improvement
        # Score: 8/3 = 2.67 → P1 (Do now!)
    },
    "jira_integration": {
        "name": "Jira Integration",
        "cost": {"effort": 3, "risk": 3, "support": 3},  # Medium effort, Router pattern
        "benefit": {"user_value": 4, "market": 4, "strategic": 2},  # Enterprise value
        # Score: 10/9 = 1.11 → P2 (Do soon)
    }
}

# Calculate and rank
for key, feature in features.items():
    score = calculate_priority(feature)
    tier = get_priority_tier(score)
    print(f"{feature['name']}: {score:.2f} → {tier}")
```

Output:
```
VSCode Developer Setup Package: 2.67 → P0/P1
Python 3.11 Upgrade: 1.50 → P2
Jira Integration: 1.11 → P2
Native Mobile App: 0.69 → P3
```

## Usage Guidelines

### When to Use

- **Roadmap planning**: Score all proposed features before committing resources
- **Stakeholder requests**: Quantify why Feature X is higher priority than Feature Y
- **Resource allocation**: Sort by score, fund from top down based on capacity
- **Saying "no"**: Transparent justification ("Score is 0.4, below our 0.5 threshold")
- **Pair-wise comparison**: Compare two features by their scores
- **Budget planning**: Effort score × hourly rate = cost estimate

### When NOT to Use

- **Emergency fixes**: P0 bugs don't need scoring (always do immediately)
- **Regulatory compliance**: Legal requirements override score
- **Obvious quick wins**: If it's 1-hour effort with clear value, just do it
- **Strategic bets**: Some features are strategic regardless of score (note this explicitly)

### Best Practices

1. **Score collaboratively**: Product + Engineering + Design together
2. **Document assumptions**: Why did we score Effort as 3 not 2? Write it down
3. **Revisit scores**: Market conditions change, re-score quarterly
4. **Use dollar proxy**: Convert effort to dollars for executive communication
5. **Track accuracy**: Post-mortems improve future scoring
6. **Avoid gaming**: Don't artificially inflate benefit or deflate cost scores
7. **Explain exceptions**: If you override the score, document why

### Common Pitfalls

- **Precision illusion**: Scores are estimates, not exact measurements
- **Ignoring support cost**: Features with high ongoing burden compound over time
- **Undervaluing strategic alignment**: Platform capabilities unlock exponential value
- **Scoring in isolation**: Context matters - consider dependencies
- **Not updating scores**: Re-evaluate when circumstances change

## Examples in Codebase

### Application to Piper Roadmap

Examples from Ted Nadeau's questions (Nov 2025):

| Feature | Effort | Risk | Support | User | Market | Strategic | Score | Priority |
|---------|--------|------|---------|------|--------|-----------|-------|----------|
| VSCode Setup | 1 | 1 | 1 | 3 | 2 | 3 | 8/3 = 2.67 | **P1** |
| Python 3.11 | 2 | 1 | 1 | 2 | 1 | 3 | 6/4 = 1.50 | P2 |
| Jira Integration | 3 | 3 | 3 | 4 | 4 | 2 | 10/9 = 1.11 | P2 |
| Email Participation | 4 | 3 | 4 | 3 | 3 | 2 | 8/11 = 0.73 | P3 |
| Mobile App | 5 | 4 | 4 | 3 | 3 | 3 | 9/13 = 0.69 | P3 |
| Federated Login | 4 | 3 | 3 | 3 | 3 | 2 | 8/10 = 0.80 | P3 |

### Integration with Existing Tools

- **GitHub Issues**: Add scorecard to issue template
- **Roadmap planning**: Score all Epic-level features
- **Sprint planning**: Already-prioritized features go into sprints

## Related Patterns

### Complements

- **Pattern-007: Graceful Degradation** - Lower support cost by failing gracefully
- **Pattern-013: Router Pattern** - Strategic alignment: enables swappable integrations
- **Pattern-002: Service Pattern** - Implementation patterns affect effort/risk scores

### Alternatives

- **RICE Framework** (Intercom): Reach × Impact × Confidence / Effort
  - More complex, requires user count estimates
  - Piper Scorecard is simpler, works without precise user data

- **Value vs Complexity Matrix** (2×2):
  - High Value + Low Complexity = Do First
  - Simpler visualization, but less nuanced (only 4 buckets)

- **Weighted Shortest Job First (WSJF)** (SAFe):
  - Cost of Delay / Job Duration
  - More sophisticated, requires estimating delay cost

### Dependencies

None. This is a process pattern, not a technical pattern.

## Migration Notes

### From Ted Nadeau Email (Nov 20, 2025)

> "I'd like to have a cost vs. benefit model of the capabilities
> cost is proportional to effort to implement & support (& risk adjusted for change)
> benefit is proportional to value to users
> While hard to put exact numbers on these things, one can attempt to:
> put dollar amounts when possible, put calendar time as proxy
> Users can advocate for features (or pay for them)
> & one can use pair-wise comparison to rate / rank the features"

This pattern implements Ted's vision with:
- ✅ Cost factors: Effort + Support + Risk
- ✅ Benefit factors: User Value + Market + Strategic
- ✅ Supports dollar proxy (Effort × hourly rate)
- ✅ Enables pair-wise comparison (compare scores directly)
- ✅ Quantified, transparent decisions

### From Internal Research (Nov 20, 2025)

Research document: `dev/2025/11/20/ted-nadeau-follow-up-research.md`

Synthesized from:
- RICE Framework (Intercom)
- Value vs Complexity Matrix
- Weighted Shortest Job First (SAFe)
- Pairwise Comparison (Ted's preference)

## References

### Documentation

- **Research source**: `dev/2025/11/20/ted-nadeau-follow-up-research.md` (Section 2)
- **Chief Architect brief**: `dev/2025/11/20/chief-architect-cover-note-ted-research.md`
- **Ted's reply**: `dev/2025/11/20/ted-nadeau-follow-up-reply.md`

### External References

- Intercom RICE Framework: https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/
- SAFe WSJF: https://scaledagileframework.com/wsjf/
- Value vs Complexity: Common PM 2×2 matrix

### Usage Analysis

- **Created**: November 20, 2025
- **Status**: Emerging (ready for use, needs validation)
- **Maintenance**: Active
- **Application**: Roadmap planning, feature requests, resource allocation

---

**Pattern created**: November 20, 2025
**Author**: Code Agent (Research Session)
**Inspired by**: Ted Nadeau's cost/benefit model request
**Status**: Ready for Chief Architect review
