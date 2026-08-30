# Design Record — Per-Connector Place-Modeling (spatial cold island)

**Status**: code disposed 2026-08-29 (PM-ruled 2026-08-15/16, spatial committed-theory review;
executed per Arch's 2026-08-29 disposal routing); thinking preserved here.
**What it was**: the committed-theory era's per-connector spatial-intelligence layer — direct-API
`*SpatialIntelligence` wrappers plus the MCP `*MCPSpatialAdapter` twins they constructed, for
connectors that never shipped a live spatial path (CI/CD, dev-environment, GitBook, Linear) plus
the superseded direct-API Notion predecessor. All had zero non-test importers at disposal
(re-verified module-by-module at delete time; census: `findings/leg-b-live-state-census.md`).
**Where the code is**: every disposed module remains findable by commit-hash reference in the
disposal record — see the 2026-08-29 spatial-disposal entries in
`docs/internal/architecture/decisions/decisions.log`, which name the last tree containing each
family. This is PM's standing retrievability requirement on the disposal (2026-08-15 ruling).

## The ideas worth keeping

1. **The 8-dimension place model is connector-agnostic; its *bindings* are the design capital.**
   Every wrapper implemented the same eight dimensions (HIERARCHY, TEMPORAL, PRIORITY,
   COLLABORATIVE, FLOW, QUANTITATIVE, CAUSAL, CONTEXTUAL — ADR-013/ADR-038), but each worked out
   what those dimensions *mean* in a specific tool's topology. That per-connector semantics table
   existed nowhere else in the docs; it is the part a future L3 build would otherwise re-derive:

   | Dimension | CI/CD pipeline | Dev environment | GitBook docs tree | Linear issues | Notion workspace |
   |---|---|---|---|---|---|
   | HIERARCHY | Pipeline → Jobs → Steps → Actions | Containers → Services → Dependencies → Configurations | Space → Collection → Page → Sub-page | Issue/project parent-child structures | Nested pages/databases (`analyze_page_structure`) |
   | TEMPORAL | Build times, deployment schedules, execution history | Container uptime, deployment times, restart patterns | Content creation, updates, publishing timeline | Created/updated patterns, activity timelines | Last-edited / created timestamps |
   | PRIORITY | Critical deployments, release priorities, environment order | Critical services, environment health, resource usage | Content visibility, access levels, publishing status | Priority levels, cycles, milestones | Priority properties on pages (`analyze_tags_status`) |
   | COLLABORATIVE | Triggering users, approvers, notification recipients | Team environments, shared configs, access patterns | Authors, editors, permissions, contribution patterns | Assignees, subscribers, comments | Who edited (`analyze_authors`) |
   | FLOW | Pipeline states (pending/running/success/failed) | Container states (running/stopped/building) | Draft → review → published → archived workflow | Status workflows, state transitions | Status-property workflows |
   | QUANTITATIVE | Build durations, success rates, deployment frequency | Resource usage, performance metrics, capacity | Page counts, content sizes, engagement metrics | Counts, sizes, velocities | Number properties |
   | CAUSAL | Triggered-by commits, blocks deployments, dependency chains | Dependencies, startup order, failure cascades | Content relationships, references | Dependencies, blocked issues, links | Relation properties (`analyze_relations`) |
   | CONTEXTUAL | Repository, environment, branch, release context | Project, environment type, team, platform | Space purpose, collection themes | Project, team, workspace context | Workspace context |

2. **"A place is what the tool's own topology says it is."** None of the wrappers invented a
   spatial layout; each read the connector's native structure (pipeline graph, container
   dependency graph, docs tree, issue graph, page tree) as the place hierarchy. The live layer
   (`github_spatial`, `place_service`, `place_detector`) works the same way — this was the
   island's contribution to the pattern, replicated five times before it had a name.

3. **Wrapper-over-adapter layering** — each `*SpatialIntelligence` composed (not subclassed) an
   MCP adapter for transport, keeping dimension analysis pure over dicts the adapter returned.
   That separation is what let CORE-MCP-MIGRATION #198 swap direct-API transports for MCP
   consumers under GitHub's spatial layer without touching dimension semantics — the migration
   that made these very modules redundant (ADR-038 Amendment A tells that story).

4. **Notion's dimension→method naming** (`analyze_page_structure`, `analyze_timestamps`,
   `analyze_tags_status`, `analyze_authors`, `analyze_workflow_props`, `analyze_metrics`,
   `analyze_relations`, `analyze_workspace`) is the cleanest statement of how the abstract
   dimensions specialize to a knowledge-base connector, as opposed to an issue-tracker or
   pipeline connector — useful if L3 is ever built for another document-shaped tool.

## Why it was disposed rather than finished

PM's 2026-08-15/16 ruling closing the spatial committed-theory review (opened 2026-07-18):
rescope, not abandonment. The live spatial layer stays (place_service, place_detector,
spatial_intent_classifier, github_spatial, home_state_service, the `spatial_adapter` base class,
the slack socket-path spatial pair); the cold island — connectors PM never intentionally
approved, plus the superseded direct-API Notion predecessor — is migration residue of a
migration that *worked* (per the layer map: "superseded implementation strategy, retained as
prior art," NOT "dead code, removed"). L3 depth beyond GitHub was never promised in the roadmap;
no commitment loses its referent.

*Extracted before deletion per the delete-module-safely skill and the PM-033d precedent
(`multi-agent-coordination-pm033d.md`). Full option analysis:
`docs/internal/architecture/current/spatial-intelligence-layer-map-and-costed-options.md`.*
