# The Multi-Wave Investigation

*December 25, 2025*

We had a problem: 44 new canonical queries to investigate. Each one needed infrastructure assessment, blocker identification, implementation complexity rating. Traditional approach: investigate them one by one, maybe three or four per session.

At that pace, the reconnaissance alone would take two weeks.

Instead, we deployed 13 subagents across 4 waves in a single 90-minute session. All 44 queries investigated. Complete infrastructure map. Priority matrix created.

## The wave structure

**Wave 1: Core Infrastructure Audit** (3 agents)
- Intent Router Auditor: 8 intent categories mapped, coverage percentages calculated
- Integration Inventory: 6 integration routers catalogued, 200+ methods found
- Repository Method Scan: 97 methods across 6 repositories analyzed

These three agents established the baseline. What existed? What was complete? Where were the foundations solid?

**Wave 2: Category Deep Dives** (4 agents)
- GitHub Operations: 8 queries mapped, complexity breakdown (2 LOW, 4 MEDIUM, 2 HIGH)
- Slack Operations: 5 queries mapped, infrastructure complete except LLM summarization
- Calendar Operations: 7 queries mapped, critical OAuth scope constraint identified
- Todo Operations: 4 queries mapped, critical blocker found (hardcoded user_id)

These four agents worked in parallel, each focused on a specific integration category. They didn't need to coordinate—they were examining independent infrastructure.

**Wave 3: Gap Analysis** (synthesis)
- Priority matrix created: Phase A (5 LOW), Phase B (11 MEDIUM), Phase C (8 HIGH), Phase D (12 blocked)
- Critical blockers documented with priority levels (P0, P1, P2)

Wave 3 synthesized the category deep dives into actionable prioritization.

**Wave 4: Remaining Categories** (6 agents)
- Help/Capability System, Activity/Audit Logging, Notion Write Operations
- Notification Infrastructure, Conversation Serialization, File Upload
- Each assessed independently, blockers identified, readiness scored

## Why it worked

The key insight: investigation parallelizes well. Analysis doesn't require shared state. Each agent can examine a portion of the codebase without coordinating with others.

Implementation is different. Two agents trying to modify the same file create merge conflicts. Two agents implementing related features need to coordinate on interfaces.

But two agents reading different parts of the codebase? They can run simultaneously without collision.

[PLACEHOLDER: Did this feel risky when you launched it? Or did it feel obvious in retrospect?]

## The blocker taxonomy

Wave 3 produced something useful beyond the priority matrix: a blocker taxonomy.

- **P0** (blocks all): Problems that prevent any query from working. User_id hardcoded as "default" was P0—it broke multi-user isolation across everything.
- **P1** (blocks category): Problems that prevent a category from working. Calendar OAuth readonly scope was P1—it blocked all scheduling features.
- **P2** (nice to have): Problems that degrade experience but don't block core functionality. Missing LLM summarization in Slack was P2.

This taxonomy separated complexity from criticality. A query could be easy to implement (LOW complexity) but blocked by a P0 issue. Another could be hard to implement (HIGH complexity) but have no blockers.

The priority matrix combined both dimensions.

## When to use this model

Multi-wave investigation works when:
- The problem space can be partitioned cleanly (categories, modules, time periods)
- Each partition can be analyzed independently
- Synthesis can happen after parallel analysis completes
- You need breadth more than depth initially

It doesn't work when:
- Agents need to coordinate during investigation
- Analysis requires iterative refinement based on early findings
- The partitions have hidden dependencies

[PLACEHOLDER: Are there other situations where you've parallelized investigation work like this?]

## The compound effect

90 minutes of parallel investigation saved roughly 10 days of sequential work. But the real value wasn't time saved—it was the complete picture.

Sequential investigation would have answered questions as they arose. Parallel investigation answered questions we hadn't thought to ask yet. The OAuth scope constraint. The hardcoded user_id. The missing router methods.

These weren't on anyone's checklist. They emerged from comprehensive coverage.

---

*Next on Building Piper Morgan: Turning these drafts into published posts, and tackling the insight backlog assessment.*

*Have you found ways to parallelize investigation work? What made it succeed or fail?*
