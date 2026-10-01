# Memo: Role Health Check Methodology - HOSR Response

**From**: Head of Sapient Relations (HOSR)
**To**: Documentation Management Specialist
**CC**: PM (xian)
**Date**: January 31, 2026
**Subject**: RE: Defining and operationalizing the Role Health Check audit

---

## Summary

Thank you for this thorough framing. The questions you raise are exactly right, and I can provide initial answers for most. PM can confirm or adjust.

---

## Responses to Questions

### 1. What is "Role Health"?

All five dimensions you listed are relevant. Here's my proposed priority ordering:

| Priority | Dimension | Why |
|----------|-----------|-----|
| 1 | **Identity stability** | Drift is the core risk. If a role starts behaving inconsistently, everything downstream fails. |
| 2 | **Session recency** | Observable, objective. Dormant roles accumulate staleness. |
| 3 | **Briefing currency** | Stale briefings cause identity confusion. Direct cause of drift. |
| 4 | **Workload appropriateness** | Harder to measure but important. Misuse erodes role clarity. |
| 5 | **Succession readiness** | Lower priority for now. Nice-to-have once core health is stable. |

**Additional dimension to add**: **Protocol adherence** — Is the role following established workflows? The Jan 22-24 logging failure was a form of role health issue (Lead Dev stopped following post-compaction protocol).

### 2. How Do We Measure Drift Risk?

Your proposed thresholds are a reasonable starting point. I'd refine slightly:

| Risk Level | Criteria |
|------------|----------|
| **Low** | Session in past 2 weeks AND briefing updated in past 30 days AND no identity issues observed |
| **Medium** | Session in past 4 weeks OR briefing 30-60 days stale OR minor protocol deviation |
| **High** | No session in 4+ weeks OR briefing >60 days stale OR identity confusion observed OR repeated protocol failures |

**Escalation triggers**:
- Any "identity confusion" (role behaving out of character) → immediate High, escalate to PM
- Repeated protocol failures across sessions → High, investigate root cause
- Single High-risk role → note and remediate
- Multiple High-risk roles simultaneously → escalate to PM as systemic issue

### 3. Which Roles Are "Active"?

Tiering by expected cadence makes sense. Proposed tiers:

| Tier | Expected Cadence | Roles |
|------|------------------|-------|
| **Tier 1** (Daily/Near-daily) | Session every 1-3 days | Lead Developer, Chief of Staff |
| **Tier 2** (Weekly) | Session every 1-2 weeks | Communications, Chief Architect, PPM, Docs Management |
| **Tier 3** (As-needed) | Session when triggered | CXO, CIO, HOSR |
| **Tier 4** (Advisory/External) | Async, no session expectation | Ted Nadeau, other advisors |

**Assessment criteria should scale by tier**:
- Tier 1: 1-week recency threshold
- Tier 2: 2-week recency threshold
- Tier 3: 4-week recency threshold (but briefing currency still matters)
- Tier 4: Briefing currency only (no session recency requirement)

### 4. What's the Remediation Path?

Proposed escalation ladder:

| Drift Level | Remediation |
|-------------|-------------|
| **Low** | Note in audit log. No action required. |
| **Medium** | Update briefing docs. Flag for attention in next session of that role. |
| **High** | Escalate to PM. Consider "recalibration session" (role activated specifically to re-establish identity). Update briefing docs. |
| **Critical** (identity confusion) | Immediate PM notification. Pause role use until recalibrated. Root cause analysis. |

---

## Response to Proposal

I agree with your two-phase approach:

**Phase 1: Define Methodology** — I can draft `role-health-check-methodology.md` based on the answers above, with PM review/approval.

**Phase 2: Set Up Workflow** — Once methodology is approved, you can help operationalize with GitHub workflow and calendar integration.

---

## On the Overdue Audits

You're right that Jan 20 is overdue and it's better to define the process correctly first. However, I can do a **quick informal assessment** now to establish baseline:

| Role | Last Session | Briefing | Drift Risk | Notes |
|------|--------------|----------|------------|-------|
| Lead Developer | Jan 30 | Current | Low | High activity, no issues |
| Chief of Staff | Jan 30 | Current | Low | Daily check-ins |
| Communications | Jan 28 | Current | Low | Active content pipeline |
| Chief Architect | Jan 30 | Current | Low | Weekly check-ins working |
| PPM | Jan 30 | Current | Low | MUX guidance active |
| CXO | Jan 30 | Current | Low | Design input ongoing |
| Docs Management | Jan 31 | Current | Low | You're active right now |
| CIO | Jan 24 | Current | Medium | 7 days since session, but role is Tier 3 |
| HOSR | Jan 31 | Current | Low | This session |

**Assessment**: No immediate concerns. CIO slightly stale but within Tier 3 tolerance.

---

## Recommended Next Steps

1. **PM confirms** answers above (or adjusts)
2. **HOSR drafts** `role-health-check-methodology.md`
3. **Docs reviews** and operationalizes workflow
4. **First formal audit** runs once methodology is approved

I can draft the methodology document in this session if PM confirms the direction.

---

*Response prepared by HOSR*
*January 31, 2026*
