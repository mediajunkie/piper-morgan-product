# Methodology Documentation Index

**Quick Navigation Guide**: Find the right methodology document for your needs.

## By Purpose

| Need                   | Location                                                               | Description                          |
| ---------------------- | ---------------------------------------------------------------------- | ------------------------------------ |
| **Quick Start**        | [METHODOLOGY.md](../../../briefing/METHODOLOGY.md)                     | Operational "How We Work" guide      |
| **Deep Reference**     | This directory (methodology-core/)                                     | Comprehensive numbered methodologies |
| **Implementation**     | *retired 2026-07-26 — see [design record](../../architecture/current/design-record-methodology-as-code-2025.md)* | The `methodology/` Python package was deleted (zero-importer, Arch fix-or-delete ruling, ADR-028 superseded); this is the preserved record of the thinking |
| **Learning/Training**  | [case-studies/](../case-studies/) | Case studies and real project examples  |
| **Testing Procedures** | [testing/](../testing/)                                                | Implementation and testing guides    |

## By Topic

### Multi-Agent Coordination

- **📋 Methodology**: [methodology-02-AGENT-COORDINATION.md](methodology-02-AGENT-COORDINATION.md) _(authoritative reference)_
- **⚡ Quick Guide**: [METHODOLOGY.md#multi-agent](../../../briefing/METHODOLOGY.md#multi-agent-coordination) _(operational overview)_
- **📚 Examples**: [multi-agent-templates.md](multi-agent-templates.md) _(templates and examples)_
- **🛠️ Templates**: [multi-agent-templates.md](multi-agent-templates.md) _(handoff protocols)_

### Multi-Agent Coordinator Implementation

- **🚀 How to Use**: [HOW_TO_USE_MULTI_AGENT.md](HOW_TO_USE_MULTI_AGENT.md) _(practical usage guide)_
- **⚡ Quick Start**: [MULTI_AGENT_QUICK_START.md](MULTI_AGENT_QUICK_START.md) _(5-minute deployment)_
- **🔧 Integration Guide**: [MULTI_AGENT_INTEGRATION_GUIDE.md](MULTI_AGENT_INTEGRATION_GUIDE.md) _(technical integration details)_
- **🐍 Implementation**: `services/orchestration/multi_agent_coordinator.py` _(core coordinator)_
- **✅ Tests**: `tests/orchestration/test_multi_agent_coordinator.py` _(39 unit tests)_
- **⚠️ Status**: See GitHub Issue #118 for deployment status and remaining work

### Excellence Flywheel

- **📋 Methodology**: [methodology-00-EXCELLENCE-FLYWHEEL.md](methodology-00-EXCELLENCE-FLYWHEEL.md) _(core framework)_
- **⚡ Quick Guide**: [METHODOLOGY.md#excellence-flywheel](../../../briefing/METHODOLOGY.md#excellence-flywheel) _(operational overview)_
- **🐍 Implementation**: *retired 2026-07-26 — see [design record](../../architecture/current/design-record-methodology-as-code-2025.md)* _(the Python package was deleted; case-studies/ and the methodology docs themselves are the live implementation now)_

### Testing & Verification

- **📋 TDD Methodology**: [methodology-01-TDD-REQUIREMENTS.md](methodology-01-TDD-REQUIREMENTS.md)
- **📋 Testing Validation**: [methodology-15-TESTING-VALIDATION.md](methodology-15-TESTING-VALIDATION.md)
- **🐛 E2E Bug Protocol**: [testing/e2e-bug-fix-execution-protocol.md](../testing/e2e-bug-fix-execution-protocol.md) - 3-phase investigation protocol
- **📋 E2E Bug Templates**: [testing/e2e-bug-investigation-report-template.md](../testing/e2e-bug-investigation-report-template.md) - Investigation report template

### Issue Tracking & GitHub

- **📋 Issue Tracking**: [methodology-08-ISSUE-TRACKING.md](methodology-08-ISSUE-TRACKING.md)
- **⚡ Quick Guide**: [METHODOLOGY.md#github-progress](../../../briefing/METHODOLOGY.md#github-progress-discipline) _(PM validation)_

### Advanced Patterns

- **📋 MCP Spatial**: [methodology-09-MCP-SPATIAL.md](methodology-09-MCP-SPATIAL.md)
- **📋 Orchestration Testing**: [methodology-11-ORCHESTRATION-TESTING.md](methodology-11-ORCHESTRATION-TESTING.md)
- **📋 STOP Conditions**: [methodology-16-STOP-CONDITIONS.md](methodology-16-STOP-CONDITIONS.md)

## Quick Decision Tree

**❓ "I need to..."**

- **Get started quickly** → [METHODOLOGY.md](../../../briefing/METHODOLOGY.md)
- **Coordinate multiple agents** → [methodology-02-AGENT-COORDINATION.md](methodology-02-AGENT-COORDINATION.md)
- **Understand testing approach** → [methodology-15-TESTING-VALIDATION.md](methodology-15-TESTING-VALIDATION.md)
- **See real examples** → [case-studies/](../case-studies/)
- **Understand the retired code-as-methodology approach** → [design record](../../architecture/current/design-record-methodology-as-code-2025.md) _(the package itself was deleted 2026-07-26)_
- **Learn from case studies** → [Pattern-061](../../architecture/patterns/pattern-061-human-ai-collaboration-referee.md)

## Complete Methodology Catalog

### Foundational (00-07)

- [00-EXCELLENCE-FLYWHEEL.md](methodology-00-EXCELLENCE-FLYWHEEL.md) - Core verification framework
- [01-TDD-REQUIREMENTS.md](methodology-01-TDD-REQUIREMENTS.md) - TDD requirements
- [02-AGENT-COORDINATION.md](methodology-02-AGENT-COORDINATION.md) - Multi-agent patterns ⭐
- [03-COMMON-FAILURES.md](methodology-03-COMMON-FAILURES.md) - Common failure patterns
- [04-ARCHITECTURAL-AGILITY.md](methodology-04-ARCHITECTURAL-AGILITY.md) - Architecture adaptability
- [05-AGENT-METHODOLOGY.md](methodology-05-AGENT-METHODOLOGY.md) - Agent practices
- [06-CORE-PATTERNS.md](methodology-06-CORE-PATTERNS.md) - Core design patterns
- [07-VERIFICATION-FIRST.md](methodology-07-VERIFICATION-FIRST.md) - Verification-first approach

### Operational (08-14)

- [08-ISSUE-TRACKING.md](methodology-08-ISSUE-TRACKING.md) - GitHub issue management ⭐
- [09-MCP-SPATIAL.md](methodology-09-MCP-SPATIAL.md) - MCP and spatial patterns
- [10-SYSTEMATIC-BREAKTHROUGHS.md](methodology-10-SYSTEMATIC-BREAKTHROUGHS.md) - Systematic problem solving
- [11-ORCHESTRATION-TESTING.md](methodology-11-ORCHESTRATION-TESTING.md) - System testing
- [12-ENHANCED-AUTONOMY.md](methodology-12-ENHANCED-AUTONOMY.md) - Enhanced autonomy patterns
- [13-REQUIREMENTS-FRAMEWORK.md](methodology-13-REQUIREMENTS-FRAMEWORK.md) - Requirements management
- [14-DOCUMENTATION-STANDARDS.md](methodology-14-DOCUMENTATION-STANDARDS.md) - Documentation standards

### Validation (15-18)

- [15-TESTING-VALIDATION.md](methodology-15-TESTING-VALIDATION.md) - Test validation ⭐
- [16-STOP-CONDITIONS.md](methodology-16-STOP-CONDITIONS.md) - Quality gates
- [17-CROSS-VALIDATION-PROTOCOL.md](methodology-17-CROSS-VALIDATION-PROTOCOL.md) - Verification patterns
- [18-CASCADE-PROTOCOL.md](methodology-18-CASCADE-PROTOCOL.md) - Change management

### Extended (19-23)

- [19-INTEGRATION-POINTS.md](methodology-19-INTEGRATION-POINTS.md) - Integration patterns
- [20-OMNIBUS-SESSION-LOGS.md](methodology-20-OMNIBUS-SESSION-LOGS.md) - Session log consolidation (updated Mar 21: COORDINATION/EXECUTION sub-types)
- [21-CODE-HYGIENE-AUDIT.md](methodology-21-CODE-HYGIENE-AUDIT.md) - Technical debt audits
- [22-ROUNDTABLE-SYNTHESIS.md](methodology-22-ROUNDTABLE-SYNTHESIS.md) - Multi-role roundtable facilitation
- [23-M1-INNOVATIONS.md](methodology-23-M1-INNOVATIONS.md) - M1-era methodology innovations catalog (trigger audits, self-approval, wiring pass, floor-first, action registry, async memos)
- [24-BRANCH-OR-ANCHOR.md](methodology-24-BRANCH-OR-ANCHOR.md) - Branch-or-Anchor decision rule when extending canonical references (structural fix for Pattern-063 Parallel-Authoring Drift)
- [25-WORKSTREAM-REVIEW-CADENCE.md](methodology-25-WORKSTREAM-REVIEW-CADENCE.md) - Weekly Ship workstream review cadence (Fri–Tue write window, Wed publish)
- [26-INDOOR-PLUMBING-SCOPE-FILTER.md](methodology-26-INDOOR-PLUMBING-SCOPE-FILTER.md) - Indoor Plumbing vs. Bathing Experience scope filter
- [27-TYPE-2-DREAMING-ANXIETY-DREAMS.md](methodology-27-TYPE-2-DREAMING-ANXIETY-DREAMS.md) - Type 2 Dreaming (Anxiety Dreams) — threat-simulation memory pattern; framing claim grounded in Revonsuo's Threat Simulation Theory ⭐ **NEW**
- [28-PRE-FILING-SLOT-AVAILABILITY-CHECK.md](methodology-28-PRE-FILING-SLOT-AVAILABILITY-CHECK.md) - Pre-Filing Slot-Availability Check — lightweight catalog discipline preventing slot collisions ⭐ **NEW**
- [29-PATTERN-FORMATION-VIA-SUCCESSFUL-IMITATION.md](methodology-29-PATTERN-FORMATION-VIA-SUCCESSFUL-IMITATION.md) - Pattern Formation via Successful Imitation — bottom-up pattern emergence through reference implementation + recognition + reuse
- [30-CONSUMER-TRACE-VERIFICATION.md](methodology-30-CONSUMER-TRACE-VERIFICATION.md) - Consumer-Trace Verification — discipline for verifying consumer-relationship claims (e.g., "feature X uses LLM Y") via navigable trace from claim to actual call site, not from upstream context-shape alone ⭐ **NEW**
- [31-APPEND-ONLY-AUTONOMOUS-CYCLE-ARCHITECTURE.md](methodology-31-APPEND-ONLY-AUTONOMOUS-CYCLE-ARCHITECTURE.md) - Append-Only Autonomous-Cycle Architecture — design discipline for autonomous loops sharing `.git/` with concurrent agents; structural elimination of rebase-onto-main hook-race failure mode ⭐ **NEW**
- [32-POSTEL-FOR-MEMO-HEADERS.md](methodology-32-POSTEL-FOR-MEMO-HEADERS.md) - Postel for Memo Headers — strict-emit YAML + permissive-accept 3-tier fallback (YAML / Markdown bold / first H1) for autonomous-cycle inbound parsing ⭐ **NEW**
- [33-SESSION-TYPE-DETERMINES-GIT-PERMISSION-SCOPE.md](methodology-33-SESSION-TYPE-DETERMINES-GIT-PERMISSION-SCOPE.md) - Session-Type Determines Git-Permission Scope — discipline of treating session-type (local Code / cloud / Routines / sub-agent) as load-bearing for commit-identity and push-permission expectations
- [34-COHORT-DISCIPLINE-AS-MOAT.md](methodology-34-COHORT-DISCIPLINE-AS-MOAT.md) - Cohort-Discipline as Moat — strategic-positioning observation that as platforms productize mechanism, the durable differentiator is the operating-norm substrate the platform doesn't ship ⭐ **NEW**
- [35-ASYMMETRIC-DISCIPLINE-CREATION-WITHOUT-PAIRED-CLEANUP.md](methodology-35-ASYMMETRIC-DISCIPLINE-CREATION-WITHOUT-PAIRED-CLEANUP.md) - Asymmetric Discipline — operational rules with creation-half well-specified but cleanup-half unspecified; pair every creation rule with cleanup-when-{condition}
- [36-DERIVED-VIEWS-OVER-HAND-MAINTAINED-TRACKERS.md](methodology-36-DERIVED-VIEWS-OVER-HAND-MAINTAINED-TRACKERS.md) - Mechanism Beats Vigilance — promote recurring vigilance-disciplines to mechanisms; two classes (Class-1 derived-views-over-stale-trackers + Class-2 structural-guards-over-action-time-omission)
- [37-COVERAGE-AUDIT-GATE-FOR-REFACTOR-DELTAS.md](methodology-37-COVERAGE-AUDIT-GATE-FOR-REFACTOR-DELTAS.md) - Coverage-Audit Gate for Refactor Deltas — gate a refactor on auditing every consumer of the changed surface before shipping
- [38-PDR-ADR-TIER-SEPARATION.md](methodology-38-PDR-ADR-TIER-SEPARATION.md) - PDR/ADR Tier Separation — decision-rule altitude (PDR) vs architectural-implementation altitude (ADR); spike-first when the surface is undefined
- [39-AUTONOMY-RELOCATES-THE-BOTTLENECK.md](methodology-39-AUTONOMY-RELOCATES-THE-BOTTLENECK.md) - Autonomy Relocates the Bottleneck to the Convergence Point — when the duty cycle works, the bottleneck doesn't vanish, it moves to the one un-parallelizable point: PM's attention (the attention-dashboard is its counterpart mechanism)
- [40-LAYER-THEN-MIGRATE.md](methodology-40-LAYER-THEN-MIGRATE.md) - Layer-Then-Migrate — decision discipline for retiring a legacy abstraction safely: introduce the new as source-of-truth, layer over legacy, migrate progressively via owner-paced commits, retire legacy last; three sub-shapes (ACL-vs-debt / lens-vs-flatten / contract-vs-build) ⭐ **NEW**
- [41-MECHANISM-DISPLACES-UNREFERENCED-DISCIPLINE.md](methodology-41-MECHANISM-DISPLACES-UNREFERENCED-DISCIPLINE.md) - Mechanism Displaces Unreferenced Discipline — a new mechanism silently displaces an older discipline it was meant to compose with, when the mechanism's loop doesn't reference the older surface; cure = structural composition (m-36 Class-2). Founding: session-log-vs-cycle-log displacement (Docs audit: systemic, 6/9 roles); 2nd instance: migration carry-forward variant-preservation trap. **PROVEN** (2026-06-12; cure-class = "no path of least resistance bypasses the discipline" — force-by-reference / force-by-distinction) ⭐ **NEW**
- [42-REFLEXIVE-VERIFICATION-SELF-EXEMPTION-UNDER-PRESSURE.md](methodology-42-REFLEXIVE-VERIFICATION-SELF-EXEMPTION-UNDER-PRESSURE.md) - Reflexive Verification — we apply verification rigor to others' claims but self-exempt on our own under-pressure speculation (speculate-then-claim instead of trace-then-claim); the pressure is the tell. Cure = name it so the next instance self-catches (m-34). Cohort-wide: 5 instances/2 roles/2 weeks (Arch-surfaced). Emerging (awaits evidence naming reduces recurrence) ⭐ **NEW**

### Recent (43-47)

- [43-NAME-THE-LAYER.md](methodology-43-NAME-THE-LAYER.md) - Name the Layer — we verify the proxy nearest to hand, not the claim; an instrument must state what it looked at. Filed 2026-07-25 by CIO, from HOST's structural read of the Amber migration. Emerging.
- [44-CLEAR-IS-NOT-A-MEASUREMENT.md](methodology-44-CLEAR-IS-NOT-A-MEASUREMENT.md) - "Clear" Is Not a Measurement — an instrument must assert what it looked at, not just report clean. Filed 2026-07-27 by CIO, from Arch's Amber-handoff bequest. Emerging → strong (11 instances/4 roles/2 projects in 96h).
- [45-AGREEMENT-IS-NOT-REPLICATION.md](methodology-45-AGREEMENT-IS-NOT-REPLICATION.md) - Agreement Is Not Replication — shared procedure manufactures false consensus; independent agreement isn't independent verification if they share a confound. Filed 2026-07-29 by CIO, proposed by Arch (four-seat evidence table). Emerging, unusually clean evidence.
- [46-PROMOTION-IS-A-RE-VERIFICATION-EVENT.md](methodology-46-PROMOTION-IS-A-RE-VERIFICATION-EVENT.md) - Promotion Is a Re-Verification Event — the durable copy needs a named source; promoting a finding into a canonical doc is itself a verification-bearing act. Filed 2026-07-30 (CXO draft), mechanism landed 2026-07-31 (HOST). Emerging — limb 2 has a shipped mechanism, limb 1 remains vigilance.
- [47-SECOND-ORDER-CLAIMS-NEED-FIRST-ORDER-RIGOR.md](methodology-47-SECOND-ORDER-CLAIMS-NEED-FIRST-ORDER-RIGOR.md) - Second-Order Claims Need First-Order Rigor — a claim about a claim (a summary, a status report, a rollup) needs the same verification discipline as the original. Filed 2026-08-07 (CIO). Proven (two distinct instances, measured cost).
- [48-A-PROXY-COUNT-IS-NOT-THE-QUANTITY.md](methodology-48-A-PROXY-COUNT-IS-NOT-THE-QUANTITY.md) - A Proxy Count Is Not The Quantity (and at selection time it propagates) — a count derived from a proxy signal gets treated as the true quantity, and the error compounds at selection time. Filed 2026-08-10 (CIO), found by PPM and CXO independently. Proven (two independent instances, opposite directions).
- [49-DESCRIBED-IS-NOT-RUNNING.md](methodology-49-DESCRIBED-IS-NOT-RUNNING.md) - Described Is Not Running — a mechanism's documentation, config, or even its own passing description is not the mechanism; only observing it fire is. Filed 2026-08-12 (CIO), canonical instance found by Janus. Emerging (one canonical instance plus three corroborating; watching for independent cross-project recurrence).
- [50-SELF-ATTESTATION-IS-NOT-VERIFICATION.md](methodology-50-SELF-ATTESTATION-IS-NOT-VERIFICATION.md) - Self-Attestation Is Not Verification — an agent cannot verify its own procedural compliance by narrating it; the discriminator is machine-written-at-invocation vs. hand-narrated-afterward-by-the-same-agent. Filed 2026-09-05 (CIO), seed formulation CXO 2026-08-30, discriminator HOST. Emerging (three confirmed real instances in one week, plus a distinct fourth-order instance in this entry's own citation history).
- [51-A-BOUNDED-SEARCH-IS-NOT-A-TOTAL.md](methodology-51-A-BOUNDED-SEARCH-IS-NOT-A-TOTAL.md) - A Bounded Search Is Not a Total — a search or test can be run correctly on a scope the reporter chose, then reported as covering more than that scope; a hedge can misattribute its own cause and mislead while formally honest. Filed 2026-09-06 (CIO), boundary table and hedge finding by CXO. Emerging, scoped to one seat (three instances, one agent — promotion trigger is a fourth instance from a different seat).

---

**Last Updated**: August 17, 2026 (Docs — added methodology-48 through -49, missing from this catalog since filing; same gap pattern as the Aug 10 fix below, found again during weekly-docs-audit #1643. Two independent subagent audits converged on this same finding.)
**Prior**: August 10, 2026 (Docs — added methodology-43 through -47, missing from this catalog since filing; found during weekly-docs-audit #1583's NAVIGATION.md↔INDEX.md cross-check)
**Maintained By**: Methodology Team
**Questions?** Check [METHODOLOGY.md](../../../briefing/METHODOLOGY.md) or create a GitHub issue
