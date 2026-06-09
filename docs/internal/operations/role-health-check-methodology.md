# Role Health Check Methodology

**Owner**: Head of Sapient Trust (HOST)
**Cadence**: Every 4 weeks (per staggered audit calendar)
**First Formal Audit**: February 2026
**Version**: 2.0
**Created**: January 31, 2026
**Last Refreshed**: 2026-06-08 (v2.0 — post-duty-cycle-migration refresh: tiers re-based on work-shape, PA/Web/Ted added, cycle-era drift surfaces + content-currency check added. See Revision History.)

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

## Operating Modes (v2.0 — replaces cadence "Tiers")

**Why this changed (v2.0, 2026-06-08)**: the v0.7 duty-cycle migration (completed 2026-06-02) put **all leadership + staff roles on a daily/near-daily autonomous cycle**. Cadence is now *uniform* — every cycling role fires every day — so the old cadence-tiers (Tier-1 daily … Tier-3 as-needed) no longer discriminate health (a CIO "session 5 weeks ago" can't happen anymore). Health is now assessed by **operating mode** (work-shape), and recency is reframed as **cycle liveness** (is the agent's cron/cycle actually firing within its mode's expected interval).

| Mode | Description | Expected signal | Roles |
|------|-------------|-----------------|-------|
| **Continuous-cycle** | Hourly-ish duty cycle; high mail/coordination throughput | A cycle/session log dated *today* (≤1 day) | Lead Developer, Chief of Staff (Exec), CIO, Docs, PPM, Communications |
| **Intermittent-cycle** | Low-frequency duty cycle (e.g. every-3hr); periodic deliverables, low mail | A cycle log within ≤2 days (low-freq = fewer fires, longer quiet stretches are normal) | HOST, Chief Architect, CXO |
| **Staff / PM-paired** | Daily, but paced to PM presence rather than autonomous mail | A cycle/session log within ≤2 days | PA (Piper Alpha) |
| **Off-cycle by design** | Intermittent / handoff-driven; substantive work in a separate repo | **Expected-absent**: absence is *healthy*, not drift. Assess on briefing + channel only | Web |
| **Advisory / async** | External; no session requirement | Channel health only | Ted Nadeau, external advisors |

**Key v2.0 reframes:**
- **Recency → liveness.** The question is no longer "has this role been activated recently" (everyone has) but "is the cycle firing as its mode expects, and is the agent *self-aware* it's cycling" (carry-forward current, cycle log not trailing).
- **Expected-absent is a first-class status.** Web's absence from the product-repo cycle is by ratified design (separate-repo lane); the methodology must not score expected-absence as drift. Same for any future off-cycle lane.
- **Mode ≠ importance.** A role's mode reflects its work-shape, not its value — intermittent-cycle (HOST/Arch) is not "lesser" than continuous.

---

## Drift Risk Scoring

### Criteria

| Risk Level | Criteria (v2.0 — liveness + content-currency + protocol) |
|------------|----------|
| **Low** | Cycle live within its mode's expected interval AND briefing content-current AND no protocol/identity issues. (Off-cycle-by-design roles: expected-absent + briefing/channel healthy.) |
| **Medium** | Cycle missed ~2× its expected interval (continuous role silent >2 days; intermittent >4 days) OR briefing content-stale (predates a major operating-model change even if commit-date is recent — see Content-Currency below) OR minor protocol deviation OR carry-forward/cycle-log trailing the actual work |
| **High** | Cycle silent ≫ expected with no expected-absence reason OR repeated protocol failures (e.g. mailbox-MANIFEST contention, directory-level git adds, STOP-deletes-cron-unre-armed) OR briefing badly out of sync with the operating model |
| **Critical** | Identity confusion observed (role behaving out of character; auditing artifact misnaming a role — see §"Audit-instrument self-check") |

### Cycle-era drift surfaces (v2.0 — new failure modes the duty cycle introduced)

Beyond the classic dimensions, the autonomous cycle created drift surfaces that didn't exist when roles were manually activated. Assess these for cycling roles:

- **Frozen-state-rots**: a fat cron prompt carrying transient state (paths, "do not chase #X") that *outlived its trigger* — the prompt silently feeds a stale instruction. (The thin-prompt + carry-forward migration structurally closes this; flag any role still on a fat prompt with stale frozen state.)
- **Overnight-continuity / Gap-A**: STOP that deletes the cron without re-arming → no morning self-wake. (Fixed by STOP-leaves-armed; flag regressions.)
- **Session-death / Gap-B**: a session that dies (compaction, laptop-sleep) never self-wakes — shape-independent residual. Manifests as a role silent past its interval *with* a dead session. (Sub-mechanism: agent-side re-arm at SessionStart:resume; external Routines watchdog if/when built.)
- **Carry-forward / cycle-log currency**: is the role's ephemeral state file + cycle log current, or trailing the actual work? A trailing log is the cycle-era version of "stale briefing."

### Examples (v2.0)

| Scenario | Risk Level |
|----------|------------|
| Any role with a cycle log dated today, briefing content-current | Low |
| Web absent from the product-repo cycle (separate-repo lane, ratified) | Low (expected-absent) |
| Continuous-cycle role (e.g. Docs) silent >2 days, no stated reason | Medium |
| Briefing commit-date <30 days but omits the entire duty-cycle operating model | Medium (content-stale; date-fresh) |
| Role still on a fat cron prompt carrying a stale "do not chase #X" clause | Medium (frozen-state-rots) |
| Communications role started giving architectural advice | Critical |
| The audit instrument names the role "HOSR / Sapient Relations" (retired name) | Critical (identity drift in the instrument itself) |

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

### Per-Role Assessment (v2.0)
- [ ] Operating mode identified (continuous / intermittent / staff / off-cycle / advisory)
- [ ] Cycle live within mode's expected interval? (Y/N — or "expected-absent" for off-cycle lanes)
- [ ] Carry-forward + cycle log current (not trailing the actual work)? (Y/N)
- [ ] Briefing **content-current**, not just commit-date-fresh? (does it reflect the current operating model? Y/N) — see Content-Currency note
- [ ] Cycle-era drift surfaces clear (frozen-state-rots / Gap-A / Gap-B / carry-forward currency)? (Y/N)
- [ ] Any protocol deviations observed? (describe if yes)
- [ ] Any identity concerns? (describe if yes)
- [ ] Drift risk assigned (Low/Medium/High/Critical)

### Content-Currency (v2.0) — briefing freshness is not commit-date

A briefing can be **date-fresh but content-stale**: its last-commit date passes the 30-day window, yet it omits a major operating-model change (e.g. the v0.7 duty cycle). Commit-date alone *understates* staleness. So: when a cohort-wide operating-model change lands, check whether each briefing *reflects* it — not just when the file was last touched. **DRY corollary**: if the same content is missing from *many* briefings, it does not belong copy-pasted into each — it belongs in **one shared doc the briefings point to** (for the duty cycle, that's `docs/operations/duty-cycle design/v0.7.0-adoption-package.md` + the `duty-cycle-tick` skill + `CLAUDE.md`). Audit for the *pointer*, not for duplicated content.

### Audit-instrument self-check (v2.0)

The role-health-check is itself a documented artifact that can drift. Each audit, verify the **generating workflow** (`.github/workflows/role-health-check.yml`) and this methodology use **current role names** (HOST / Head of Sapient Trust — NOT the retired "HOSR / Head of Sapient Relations / Sapient Resources") and the **current operating-mode structure** (not the retired cadence-tiers). An identity auditor that misnames a role is itself a Critical identity-drift instance.

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
| 2.0 | 2026-06-08 | Post-duty-cycle-migration refresh (HOST, from #1178 findings). Cadence "Tiers" → work-shape "Operating Modes" (cadence now uniform — all roles cycle daily); recency reframed as cycle-liveness; PA + Web (expected-absent) + Ted added; cycle-era drift surfaces (frozen-state-rots / Gap-A / Gap-B / carry-forward currency) added; content-currency briefing check (date-fresh ≠ content-fresh) + DRY-pointer corollary; audit-instrument self-check added. |

---

*Methodology owned by HOST. Questions or proposed changes should be directed to HOST via memo or PM.*
