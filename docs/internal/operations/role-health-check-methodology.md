# Role Health Check Methodology

**Owner**: Head of Sapient Trust (HOST)
**Cadence**: Every 4 weeks (per staggered audit calendar)
**First Formal Audit**: February 2026
**Version**: 1.0
**Created**: January 31, 2026

---

## Purpose

Role Health Checks ensure that agent roles maintain consistent identity, appropriate workload, and current documentation across sessions. The goal is to detect and remediate "drift" before it causes coordination failures or identity confusion.

---

## Definition of Role Health

Role health is assessed across six dimensions:

| Priority | Dimension | Description |
|----------|-----------|-------------|
| 1 | **Identity Stability** | Does the role maintain consistent behavior, tone, and boundaries across sessions? |
| 2 | **Session Recency** | Has the role been activated within its expected cadence? |
| 3 | **Briefing Currency** | Are the BRIEFING-ESSENTIAL-* docs accurate and up to date? |
| 4 | **Protocol Adherence** | Is the role following established workflows (logging, handoffs, etc.)? |
| 5 | **Workload Appropriateness** | Is the role being used for its intended purpose? |
| 6 | **Succession Readiness** | Could another agent pick up this role if needed? |

**Note**: Dimensions 1-4 are assessed every audit. Dimensions 5-6 are assessed quarterly or when concerns arise.

---

## Role Tiers

Roles are classified by expected activation cadence. Assessment thresholds scale by tier.

| Tier | Expected Cadence | Recency Threshold | Roles |
|------|------------------|-------------------|-------|
| **Tier 1** | Daily or near-daily | 1 week | Lead Developer, Chief of Staff |
| **Tier 2** | Weekly | 2 weeks | Communications, Chief Architect, PPM, Docs Management |
| **Tier 3** | As-needed | 4 weeks | CXO, CIO, HOST |
| **Tier 4** | Advisory/Async | N/A (no session requirement) | Ted Nadeau, external advisors |

**Tier 4 roles** are assessed on briefing currency and communication channel health only.

---

## Drift Risk Scoring

### Criteria

| Risk Level | Criteria |
|------------|----------|
| **Low** | Session within tier threshold AND briefing updated in past 30 days AND no issues observed |
| **Medium** | Session within 2x tier threshold OR briefing 30-60 days stale OR minor protocol deviation |
| **High** | Session exceeds 2x tier threshold OR briefing >60 days stale OR repeated protocol failures |
| **Critical** | Identity confusion observed (role behaving out of character) |

### Examples

| Scenario | Risk Level |
|----------|------------|
| Lead Dev session 3 days ago, briefing current | Low |
| Chief Architect session 3 weeks ago (Tier 2 = 2-week threshold) | Medium |
| CIO session 5 weeks ago (Tier 3 = 4-week threshold) | Medium |
| Communications role started giving architectural advice | Critical |
| Lead Dev skipped logging protocol twice in one week | High |

---

## Escalation Ladder

| Risk Level | Action |
|------------|--------|
| **Low** | Note in audit log. No action required. |
| **Medium** | Update briefing docs if stale. Flag for attention in next session of that role. Note protocol deviation if applicable. |
| **High** | Escalate to PM. Schedule remediation (briefing update, recalibration session). Root cause analysis for protocol failures. |
| **Critical** | Immediate PM notification. Pause role use until recalibrated. Conduct identity investigation. Update briefings and prompts as needed. |

### Recalibration Session

When a role shows High or Critical drift, a "recalibration session" may be needed:

1. Activate the role with explicit identity reinforcement
2. Review recent sessions for drift patterns
3. Update briefing documents with any clarifications
4. Verify role understands its boundaries and responsibilities
5. Document recalibration in audit log

---

## Audit Checklist

### Pre-Audit (HOST)
- [ ] Pull session log inventory for past 4 weeks
- [ ] Check briefing document timestamps
- [ ] Review any incident reports mentioning role issues

### Per-Role Assessment
- [ ] Last session date recorded
- [ ] Session within tier threshold? (Y/N)
- [ ] Briefing updated within 30 days? (Y/N)
- [ ] Any protocol deviations observed? (describe if yes)
- [ ] Any identity concerns? (describe if yes)
- [ ] Drift risk assigned (Low/Medium/High/Critical)

### Post-Audit
- [ ] All roles assessed
- [ ] Remediation actions identified for Medium+ risks
- [ ] Audit summary written
- [ ] Calendar updated with next audit date
- [ ] PM notified if any High/Critical findings

---

## Audit Output Template

```markdown
# Role Health Check: [Date]

**Auditor**: HOST
**Period Reviewed**: [Start Date] - [End Date]

## Summary

| Risk Level | Count |
|------------|-------|
| Low | X |
| Medium | X |
| High | X |
| Critical | X |

## Role Assessments

| Role | Tier | Last Session | Briefing Age | Drift Risk | Notes |
|------|------|--------------|--------------|------------|-------|
| Lead Developer | 1 | YYYY-MM-DD | X days | Low | |
| Chief of Staff | 1 | YYYY-MM-DD | X days | Low | |
| ... | | | | | |

## Findings Requiring Action

### [Role Name] - [Risk Level]
- **Issue**: [Description]
- **Remediation**: [Action]
- **Owner**: [Who]
- **Due**: [When]

## Next Audit

Scheduled: [Date per staggered calendar]
```

---

## Integration Points

### With Other Audits

- **Weekly Docs Audit**: May flag stale briefings → input to Role Health Check
- **Pattern Sweep**: May reveal role misuse patterns → input to workload assessment
- **Omnibus Logs**: Primary source for session recency and protocol adherence

### With Incident Response

Role-related incidents (e.g., Jan 22-24 logging failure) should trigger:
1. Immediate assessment of affected role(s)
2. Root cause analysis
3. Potential out-of-cycle Role Health Check
4. Updates to this methodology if systemic issue identified

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-31 | Initial methodology defined |

---

*Methodology owned by HOST. Questions or proposed changes should be directed to HOST via memo or PM.*
