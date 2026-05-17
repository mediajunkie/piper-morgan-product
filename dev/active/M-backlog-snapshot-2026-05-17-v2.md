# M-sprint backlog snapshot — v2 (2026-05-17 14:03 PT)

**Source of truth**: PM-exported TSV at `dev/active/MVP-milestone-backlog.tsv` (Project Board export, not committed). v1 of this doc (`M-backlog-snapshot-2026-05-17.md`) was based on GitHub-Issue milestone field; v2 corrects via the Project Board's Sprint + Milestone columns.

**Key disambiguation**: there are TWO "milestone" surfaces in this product:
- **GitHub Issue milestone field** — shows "Fast Follow" / "MVP" / "Post-MVP" / "Enterprise" (visible via `gh issue list --milestone`)
- **Project Board "Milestone" field** — shows "MVP" for all M2–M5 sprint items (TSV column)

The Project Board's **Sprint** column (M2 / M3 / M4 / M5 / R1) is the authoritative sprint marker. Sub-sprint labels (M2e/M2f/M2g) live as GitHub labels on top of the Sprint assignment.

---

## M2 — Conscious Floor + Action Handlers (22 open, 2 labeled M2g)

### Currently M2g-labeled (2)

| # | Title | Lead Dev state |
|---|---|---|
| **1016** | ARCH-DESIGN: LLM-touch boundary principle (epic) | Architect-led; my #1016 status memo (`8ea7b5556`) got Architect's "concur option B (umbrella stays open)" reply with #1089 as the named sub-issue. Architect's lane to ratify final close. |
| **1089** | KG-PRIVACY-FILTER (design-gated) | Phase 0 design substrate **complete** (Architect Q3+Q4 ratified; HOST Q2 ratified with `filter_reason` enum refinement; CIO Q5 pending; PM Q1 pending — demand-gated cluster triage). |

### Not yet M2g-labeled — candidates for promotion / deferral / further break-up (20)

I'll group by my read of the work shape. Issue titles only — would need `gh issue view` to confirm complexity for each.

**Wire-up / handler completion** (5):
- **#692** WIRE-SLACK: blocker detection in Slack webhook
- **#693** WIRE-STANDUP: fetch standup workflow settings from user configuration
- **#694** WIRE-GITHUB-LLM: replace placeholder with actual LLM call in issue generator
- **#695** WIRE-GITHUB-CMD: integrate GitHub issue command with actual GitHub service
- **#1050** STANDUP-ACTIVE-REPOS: full active-repos resolution for morning standup

**Memory layer (MEM-*)** (4):
- **#972** MEM-TEMPORAL: temporal validity fields to memory frontmatter
- **#973** MEM-CACHE-AUDIT: document stable vs dynamic layers in context assembler
- **#974** MEM-EVAL: session-end memory evaluation question
- **#975** MEM-DELTA: 'Delta since last session' context injection

**Test/QA infrastructure** (5):
- **#989** CANONICAL-FIXTURES: warmed-up user fixture for canonical retest
- **#993** SCORER-VOCABULARY: AAXT six-failure-mode taxonomy for DeepEval
- **#994** TEST-PATHOLOGICAL-TAGS: tag canonical retest queries
- **#995** FABRICATION-PROBES: standalone absence probe set
- **#1047** M2D-UAT: Manual browser-smoke + a11y + performance verification of M2d shipped surfaces

**Integration follow-ups / demand-gated** (5):
- **#1080** NOTION-WRITE: activate update_document (in demand-gated cluster triage memo)
- **#1081** NOTION-SLACK-XREF: cross-references render post-#304 activation (demand-gated)
- **#1082** NOTION-TEST-REWRITE: test_notion_spatial_integration.py against notion-client
- **#1085** CONTEXT-ACTIVITY-SLACK: Slack source to recent-activity (demand-gated)
- **#1086** CONTEXT-ACTIVITY-CAL: calendar source to recent-activity (demand-gated)

**Bigger epic** (1):
- **#472** EPIC: Slack Integration TDD Gaps - OAuth and Spatial Methods

---

## M3 — Artifact Persistence (13 open)

| # | Title |
|---|---|
| 470 | EPIC: SEC-RBAC Phases 4-5 - Projects and Files Ownership |
| 118 | INFR-AGENT: Multi-Agent Coordinator Operational Deployment |
| 313 | CONV-UX-DOCS: File Browser & Document Management UI |
| 355 | DOCS-STOPGAP: Basic Artifact Persistence |
| 366 | SLACK-MEMORY: Persist spatial patterns over time |
| 371 | INFRA-TIMESERIES: Time-Series Database Infrastructure |
| 496 | CANONICAL-#9: Enhance priority queries with real priority data |
| 497 | CANONICAL-#10: Enhance focus guidance synthesis |
| 669 | COMPOSTING-HYBRID-TRIGGER: time-based forcing per unihemispheric dreaming |
| 952 | ARTIFACT-MODEL: Artifact data model with lifecycle states |
| 953 | CONTEXT-PERSIST: Cross-session memory persistence (Layer 4 gap) |
| 976 | MEM-COMPOSTING: ADR-054 composting pipeline implementation |
| 1060 | INFRA-CONVERSATION-REPO: ConversationRepository DB integration |

PM note: "sprints expand 5x or more lately" — M3 may grow substantially during scope.

---

## M4 — Trust + Learning (8 open)

| # | Title |
|---|---|
| 558 | MUX-STANDUP-CONVERSE: LLM-based preference extraction |
| 302 | CONV-MCP-DOCS: Unified Document Processing via Skills |
| 712 | MUX-DOCUMENT-VIEWER: Create Document Viewer with Lifecycle |
| 713 | MUX-DOCUMENTS-LIFECYCLE-UI: Wire Lifecycle to Documents View |
| 954 | TRUST-LITE: Trust graduation via context (lightweight) |
| 955 | PREF-INFER: User-correctable preferences (Claude memory model) |
| 956 | LEARNING-SURFACE: Trust-graduated learning surfacing |
| 1062 | CORE-LEARN-PHASE-3: Learning infrastructure phase 3 (from #471) |

---

## M5 — Distribution + Polish (20 open, expected to grow as MVP/beta gate epic)

| # | Title |
|---|---|
| 557 | ARCH: WebSocket Infrastructure for Real-Time Communication |
| 542 | SEC: Implement actual token revocation on disconnect |
| 482 | SEC-KMS-INTEGRATION: Migrate from env var to AWS KMS |
| 441 | CORE-UX-AUTH-PHASE2: Registration, Password Reset, Security Polish |
| 829 | DIST-MCP-PACKAGE: Package Piper as MCP server |
| 830 | DIST-MCP-DOCS: Integration documentation for MCP clients |
| 831 | DIST-MCP-REGISTRY: Publish to package registries |
| 832 | DIST-MCP-TEST: Integration testing with MCP clients |
| 865 | REFACTOR: Extract setup wizard into component-based steps |
| 957 | DIST-MCPB-BUNDLE: MCPB packaging for Claude Desktop one-click |
| 958 | DIST-PROJECT-TEMPLATE: Claude Project template for Piper persona |
| 959 | DIST-MCP-APPS: Artifact canvas via MCP Apps |
| 966 | DIST-VISUAL-IDENTITY: Visual identity for MCPB + MCP Apps |
| 998 | COMPOSE-UI-V1: editorial compose web UI (FastAPI /admin/compose) |
| 1028 | PERPLEXITY broader sweep — 4 files still reference perplexity |
| 1043 | En-masse copy review pass for new M2e handlers + standup prompts |
| 1001 | Owner-review: services/publishing/publisher.py retry/fallback |
| 1048 | MUX-INSIGHT-STAGE-VISUAL: stage-specific visual treatment |
| 1090 | UI-1.0-PLAN: scope conversation history + settings UI for 1.0 (epic) |
| 1061 | INFRA-OAUTH-MULTI: Multi-OAuth installation infrastructure |

---

## R1 — Recurring Audits (separate from M-sprint flow)

| # | Title |
|---|---|
| 683 | MUX-WIRE-DOD: Definition of Done update |
| 967 | TRACKING: Backlog Deep Review — Surviving Edges |
| 1058 | Template hygiene review: agent-prompt-template.md + gameplan-template.md |

Plus two merge/PR refs (#856, #941) — likely housekeeping items in the project board.

---

## Lead Dev assessment for "how to finish M2g + rest of M2"

### Finishing M2g (the 2 currently labeled)

- **#1016**: needs Architect to land the "boundary-map" deliverable (Architect's option C from their reply) OR close as umbrella when #1089 settles. Not gating Lead Dev; Architect's cadence.
- **#1089**: needs (a) CIO Q5 (Pattern-073 numbering — minor), (b) PM Q1 ratification via demand-gated cluster triage. Once those land, design substrate is locked. If PM picks (1b) ship-when-triggered, #1089 stays open with blueprint complete; if (1c) ship-now, Lead Dev implements per Architect's Q3/Q4 + HOST Q2 ratified design.

### Triaging the rest of M2 (20 issues) — Lead Dev's read

For each, the question is: **M2g promotion / defer to later M2 sub-sprint / break out as own scope / close as obsolete**. Some are bounded chip-away material; others need PM scoping decisions before they're actionable.

**Likely bounded chip-away (good M2g promotion candidates)**:
- **#1082** NOTION-TEST-REWRITE — tech-debt, bounded; likely <1 day
- **#1086** CONTEXT-ACTIVITY-CAL — same pattern as #1085 (demand-gated); would benefit from a combined disposition with that cluster
- **#994** TEST-PATHOLOGICAL-TAGS — test infra, bounded
- **#989** CANONICAL-FIXTURES — test infra, bounded
- **#993** SCORER-VOCABULARY — would need design read (AAXT taxonomy adoption)

**Wire-up work — bounded but needs Phase 0 audit per issue**:
- **#692** WIRE-SLACK blocker detection
- **#693** WIRE-STANDUP settings
- **#694** WIRE-GITHUB-LLM replace placeholder
- **#695** WIRE-GITHUB-CMD GitHub service integration
- **#1050** STANDUP-ACTIVE-REPOS

Each looks like a focused 1-2 day chip-away if Phase 0 confirms scope.

**Memory layer (MEM-*)** — likely needs coordinated design pass:
- #972, #973, #974, #975 — these look like a memory-layer mini-sprint of their own. Worth a Phase 0 audit on the cluster.

**M2D-UAT (#1047)** — manual smoke testing; needs PM cycles, not Lead Dev cycles. Triage decision: who runs it + when.

**FABRICATION-PROBES (#995)** — CIO/Methodology-adjacent. Worth a CIO lens before promotion.

**Epic (#472 Slack Integration TDD Gaps)** — needs breakdown into sub-issues before chip-away. Possibly an epic that should land in M3 since it intersects #366 SLACK-MEMORY.

### Lead Dev recommendation for next moves

1. **Resolve #1089 PM Q1** (via demand-gated cluster triage memo) — closes the M2g design substrate gate
2. **Bundle disposition for #1080 + #1081 + #1085 + #1086** (the four Notion + Slack/Calendar context-activity demand-gated items) as a cluster — your reframe about "MVP roadmap commitment IS the demand signal" may flip some of these from defer to chip-away
3. **Pick 2-3 bounded chip-aways from the rest of M2** based on capacity + your priority sense. My weak preferences: #1082 (smallest), #1086 (clusters with the cluster triage), one wire-up (#693 or #694 looks most bounded).
4. **Memory-layer cluster (#972-975)** — Phase 0 audit memo before any individual chip-away; these likely need coordinated design.

---

## Gaps that remain

- **M2g sub-label assignment** — PM call which of the 20 non-M2g-labeled M2 issues should be promoted; #1080/#1085 cluster question still open
- **Memory-layer (MEM-*) coordinated scope** — Phase 0 audit memo would help
- **#472 epic breakdown** — separate scoping pass needed
- **#1047 M2D-UAT staffing** — manual PM cycles or coordinated agent test pass?

---

*Supersedes*: `M-backlog-snapshot-2026-05-17.md` (v1 — used wrong milestone field)
*Source*: `dev/active/MVP-milestone-backlog.tsv` (PM export, not yet committed)
*Last updated*: 2026-05-17 14:03 PT (Lead Dev, via TSV ingestion)
