# M2 Unmapped-Families Triage — Per-Issue Verdicts

**Author**: Lead Developer
**Date**: 2026-05-05
**Trigger fired**: post-M2e closure (#790, #900, #1039, #1040, #1052 all closed today)
**Source memo**: `mailboxes/lead/read/memo-pa-to-lead-cc-ceo-exec-ppm-m2-unmapped-families-triage-after-m2e-2026-05-04.md`
**Method**: same audit-cascade shape as #1041 (WIRE-* triage) and the M2d audit-cascade May 2

---

## TL;DR

27 issues triaged across 6 families.

| Verdict | Count |
|---|---|
| **SUPERSEDED** (close immediately) | 2 |
| **STILL NEEDED** (keep open; PA proposes sub-epic) | 22 |
| **NEEDS PM CALL** (verdict unclear without PM input) | 2 |
| **RE-SCOPED** (rewrite body, sub-epic decision after) | 1 |

PA's family-level prior was right for Families 1+2+5+6 (mostly STILL NEEDED, post-MVP). Family 3 (CONV/Context) had the most supersession — temporal context fully shipped via #951; project-portfolio basics shipped via user_context_service. Family 4 (Memory) has substantial overlap with shipped session-start hook but the bulk of the work is still unshipped.

---

## Family 1 — Older SEC/INFRA (6 issues)

PA prior: "likely high close-supersede rate."
Actual: **all STILL NEEDED, post-MVP**. None superseded by recent work (composting/MUX/audit-transparency don't touch this surface).

| # | Title | Verdict | Notes |
|---|---|---|---|
| #557 | ARCH WebSocket Infrastructure | **STILL NEEDED** | P3 future; arch question raised during #554 spike. Suggest sub-epic: post-MVP infra or M3 |
| #542 | SEC Token revocation on disconnect | **STILL NEEDED** | P2 integrations security hygiene; not blocking alpha. Suggest sub-epic: post-MVP integrations or M2f |
| #482 | SEC-KMS-INTEGRATION (env var → AWS KMS) | **STILL NEEDED** | Post-alpha production hardening (no production deployment yet). Suggest sub-epic: M3 or later |
| #470 | EPIC SEC-RBAC Phases 4-5 (Projects + Files) | **STILL NEEDED** | Post-alpha sharing model. Phases 1-2 already shipped per body. Suggest sub-epic: M3 |
| #471 | EPIC Infrastructure (OAuth/Learning/TimeSeries/Conversation) | **NEEDS PM CALL** | Multi-component parent epic; 4 sub-beads listed. Worth PM+PA discussion on whether to keep as one epic or break sub-beads into named sub-epics for M3. |
| #371 | INFRA-TIMESERIES (time-series DB) | **STILL NEEDED** | Post-alpha; blocks #366. Suggest sub-epic: post-MVP infra |

---

## Family 2 — Older Integration (3 issues)

PA prior: "likely mixed."
Actual: **2 STILL NEEDED + 1 NEEDS PM CALL**.

| # | Title | Verdict | Notes |
|---|---|---|---|
| #472 | EPIC Slack Integration TDD Gaps | **STILL NEEDED** | "Future sprint" per body — 8 stub methods across SlackOAuthHandler + SlackSpatialMapper. Not blocking alpha. Suggest sub-epic: post-MVP Slack |
| #304 | CONV-INFR-NOTN Activate Existing Notion Integration | **NEEDS PM CALL** | Body claims 1,112 lines of Notion code are 78% complete (Aug 2025). Two questions for PM: (a) does the code still exist post-floor-migration? `services/integrations/mcp/notion_adapter.py` and `services/intelligence/spatial/notion_spatial.py` referenced. (b) Is Notion in alpha scope? If no to (b), this drifts to post-MVP regardless of (a). |
| #366 | SLACK-MEMORY (persist spatial patterns over time) | **STILL NEEDED** | Blocked by #371 (time-series DB). Suggest sub-epic: post-MVP Slack/Memory (after #371 lands) |

---

## Family 3 — Older CONV/Context (6 issues)

PA prior: "likely high re-scope rate" given recent ContextAssembler work.
Actual: **2 SUPERSEDED, 4 STILL NEEDED (all explicitly deferred from #951)**. PA's read was accurate — context-assembler shipping caught up with the older pre-floor convergence work.

| # | Title | Verdict | Notes |
|---|---|---|---|
| #100 | CONV-FEAT-PROJ Project Portfolio Awareness | **RE-SCOPED** | Basic project-list shipped: `services/user_context_service.py:189` calls `list_active_projects` and surfaces projects in floor context. **The "comprehensive portfolio with time-allocation percentages + status tracking + recent-activity-driven discovery" layer is NOT shipped.** Recommend: close this one and file a new, narrower issue scoped only to the analytics/allocation layer (with clear cross-reference). Or rewrite body to scope only the post-#951 gap. |
| #101 | CONV-FEAT-TIME Temporal Context System | **SUPERSEDED** | Fully landed via #951 + `_gather_temporal_context` (services/intent_service/context_assembler.py:353). Floor reads `current_date`, `current_time`, `current_day_of_week`. AC items "current date/time context available in all conversations" satisfied. Close-supersede with reference to #951. |
| #983 | CONTEXT-BLOCKED (blocked items in floor) | **STILL NEEDED** | Explicitly deferred from #951; blocked on label-convention decision (PM+Architect). Suggest sub-epic: M2f post-floor-coverage |
| #984 | CONTEXT-CACHE (Redis TTL caching) | **STILL NEEDED** | Explicitly deferred from #951. Suggest sub-epic: M2f post-floor-coverage; tied to #973 (cache audit doc) |
| #985 | CONTEXT-SPRINT (GitHub milestone data) | **STILL NEEDED** | Explicitly deferred from #951. Suggest sub-epic: M2f post-floor-coverage; aligns with #1039 milestones-handler work landed today |
| #986 | CONTEXT-ACTIVITY (recent activity feed cross-integration) | **STILL NEEDED** | Explicitly deferred from #951; larger scope (event sourcing decision). Suggest sub-epic: M2f post-floor-coverage |

---

## Family 4 — Memory (4 issues)

PA prior: "likely needs PM-call subset."
Actual: **all STILL NEEDED**, with partial overlap on #975 vs the shipped session-start hook. None need PM call.

| # | Title | Verdict | Notes |
|---|---|---|---|
| #972 | MEM-TEMPORAL (valid_from/ended frontmatter) | **STILL NEEDED** | Convention/spec work, no code shipped against it. Cross-project coordination with Janus/Klatch. Suggest sub-epic: M2g (memory governance) |
| #973 | MEM-CACHE-AUDIT (stable-vs-dynamic doc) | **STILL NEEDED** | Documentation + minor refactoring; pre-work for #984's caching strategy. Suggest sub-epic: M2g (memory governance) |
| #974 | MEM-EVAL (session-end evaluation question) | **STILL NEEDED** | Process change in CLAUDE.md session-wrap checklist. Tiny scope. Suggest sub-epic: M2g (memory governance) |
| #975 | MEM-DELTA (delta-since-last-session injection) | **STILL NEEDED** (partial overlap) | Shipped session-start hook (`.claude/hooks/session-start.sh`) covers (1) log continuity (2) mailbox count (3) briefing freshness (4) role identity. The MEM-DELTA scope (commits + memos + issues filed/closed since last session) is **NOT shipped**. Issue body should be updated to reflect partial overlap with hook. Suggest sub-epic: M2g (memory governance) |

---

## Family 5 — Testing/scoring infra (6 issues)

PA prior: "likely keep-with-rescope."
Actual: **all STILL NEEDED**. None superseded; testing/scoring infra is its own track largely independent of M2 sub-epic ships.

| # | Title | Verdict | Notes |
|---|---|---|---|
| #987 | GEMINI-QUOTA (paid-tier vs free-tier decision) | **STILL NEEDED** | Specific PM decision pending (paid-tier billing call). Sub-epic: M2-discovered (testing infrastructure) |
| #989 | CANONICAL-FIXTURES (warmed-up user fixture) | **STILL NEEDED** | Identified during #950 iter 2 verification; test-fixture work. Sub-epic: M2-discovered (testing infrastructure) |
| #991 | ETHICS-RESPONSE-GATE (post-generation floor content check) | **STILL NEEDED** | Filed from #964 Gap 2; PM/CXO decision pending on Option A/B/C/D. CXO non-binding view (Apr 16): Option A defensible for alpha. Sub-epic: M2-discovered or M3 ethics-hardening (depending on PM decision) |
| #993 | SCORER-VOCABULARY (AAXT six-failure-mode taxonomy) | **STILL NEEDED** | Architect+CXO endorsed Apr 16. Diagnostic-layer adoption underneath the Colleague Test rubric. Sub-epic: M2-discovered (testing infrastructure) |
| #994 | TEST-PATHOLOGICAL-TAGS (expected-pass vs known_pathological) | **STILL NEEDED** | Filed from PPM Apr 16 memo; small scope (61 queries). Sub-epic: M2-discovered (testing infrastructure) |
| #995 | FABRICATION-PROBES (5-10 probe absence regression set) | **STILL NEEDED** | Architect+CXO "DO IT" Apr 16. Standalone instrument alongside Colleague Test. Sub-epic: M2-discovered (testing infrastructure) |

---

## Family 6 — UI/Process (2 issues)

PA prior: "small, likely fast-verdict."
Actual: **both STILL NEEDED**, fast-verdict confirmed.

| # | Title | Verdict | Notes |
|---|---|---|---|
| #683 | MUX-WIRE-DOD (DoD requires interface verification) | **STILL NEEDED** | P3 process improvement; deferred from #670 MUX-WIRE epic. Light scope (DoD checklist + PR review checklist). Sub-epic: M2g (methodology) or fold into testing-rigor ADR Architect is preparing |
| #998 | COMPOSE-UI-V1 (editorial compose web UI) | **STILL NEEDED** | Active per recent PM discussions; localhost-only `/admin/compose`. Sub-epic: post-MVP tooling or comms-ops |

---

## Recommended immediate actions

### Close-supersede (2 issues — safe to close right now)

- **#101 CONV-FEAT-TIME** — close-supersede; reference #951 + `_gather_temporal_context`
- **#100 CONV-FEAT-PROJ** — close-supersede on basic portfolio-awareness scope; **file a new narrower issue** for portfolio analytics/allocation if PM still wants that layer post-MVP

### NEEDS PM CALL (2 issues — verdict cannot be determined without PM input)

- **#304 CONV-INFR-NOTN** — is Notion in alpha scope? Does the 1,112 lines of pre-floor Notion code still exist? PA + PM + Lead Dev should walk this 5 min.
- **#471 EPIC Infrastructure parent** — keep as parent epic OR break out 4 sub-beads into M3 sub-epics? PA + PM call.

### Specific PM decisions inside STILL NEEDED issues (not blocking the triage but tracked)

- **#983 CONTEXT-BLOCKED** — canonical labels for "blocked"
- **#987 GEMINI-QUOTA** — paid-tier billing call
- **#991 ETHICS-RESPONSE-GATE** — Option A/B/C/D selection (CXO Apr 16: Option A defensible for alpha)

---

## Suggested sub-epic placement (PA+PM call)

These are **proposed groupings**, not assignments:

- **M2f post-floor-coverage**: #983, #984, #985, #986 (all 4 explicitly deferred from #951 — natural cohort)
- **M2g memory governance**: #972, #973, #974, #975 (Janus-aligned memory infrastructure)
- **M2-discovered (testing infra)**: #987, #989, #991, #993, #994, #995 (testing/scoring instrumentation)
- **M3 / post-alpha**: #482, #470, #557, #542, #371, #366, #472 (production hardening + post-alpha integrations)
- **Post-MVP tooling**: #683, #998 (process + tooling)

---

## Outputs

- **Per-issue verdicts table** — this memo
- **Immediate close-supersede actions** — 2 items (#100, #101)
- **NEEDS PM CALL list** — 2 items (#304, #471) for PA+PM walk
- **Sub-epic placement proposals** — for PA to ratify with PM

Per the audit-cascade shape: PA hosts the synthesis after this. Lead Dev's role (per the May 4 memo) is verdicts + immediate close-supersedes; PA+PM own sub-epic placement decisions.

— Lead Developer, 2026-05-05
