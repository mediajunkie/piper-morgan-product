# Methodology Documentation Index

**Quick Navigation Guide**: Find the right methodology document for your needs.

## By Purpose

| Need                   | Location                                                               | Description                          |
| ---------------------- | ---------------------------------------------------------------------- | ------------------------------------ |
| **Quick Start**        | [METHODOLOGY.md](../../../briefing/METHODOLOGY.md)                     | Operational "How We Work" guide      |
| **Deep Reference**     | This directory (methodology-core/)                                     | Comprehensive numbered methodologies |
| **Implementation**     | [/methodology/](../../../../methodology/)                              | Python code and live implementation  |
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
- **🐍 Implementation**: [/methodology/](../../../../methodology/) _(Python code)_

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
- **Implement in code** → [/methodology/](../../../../methodology/)
- **Learn from case studies** → [Pattern-061](../../architecture/current/patterns/pattern-061-human-ai-collaboration-referee.md)

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
- [31-APPEND-ONLY-AUTONOMOUS-CYCLE-ARCHITECTURE.md](methodology-31-APPEND-ONLY-AUTONOMOUS-CYCLE-ARCHITECTURE.md) - Append-Only Autonomous-Cycle Architecture — design discipline for autonomous loops sharing `.git/` with concurrent agents; structural elimination of rebase-onto-main hook-race failure mode ⭐ **NEW**

---

**Last Updated**: May 18, 2026
**Maintained By**: Methodology Team
**Questions?** Check [METHODOLOGY.md](../../../briefing/METHODOLOGY.md) or create a GitHub issue
