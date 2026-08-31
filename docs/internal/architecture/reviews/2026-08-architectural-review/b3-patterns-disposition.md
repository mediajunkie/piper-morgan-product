# B3 Patterns Disposition — working tracker
**Author**: Docs, 2026-08-31 (B3 kickoff day)
**Purpose**: second-axis (effective/inert) judgment for all 81 patterns, building on the
mechanical first axis (citation census). Tier A/B are evidence-strong enough to disposition
without a full read; C/D need individual reads before a call. Disposition column filled in
as work proceeds — this file is the working state, not a final report.

## Finding worth sharing with Arch/CIO — citation count alone mispredicts effective/inert

Day-1 test on all 4 Tier-D patterns (old + lowest-citation, the group most likely to be a clean
"historical" sweep): **3 of 4 outcomes did not match what citation count alone would predict.**
P-026 (Cross-Feature Learning, only 12 deduped cites, dated Feb 2026) is genuinely **effective** —
verified by grepping `services/` for its actual mechanism, not just counting mentions: it's wired
into `services/intent/intent_service.py` and 5 other live files via `query_learning_loop.py`. Low
citation there reflects that the pattern is *used*, not *discussed* — code doesn't cite its own
patterns in prose. P-015 (Internal Task Handler) genuinely had zero code hits — a clean historical
case. P-016 was ambiguous even after a code check (one tangential comment, no real implementation
match) — flagged as a caveat rather than forced to a confident call.

**Practical implication for the disposition pass**: the citation census's mechanical first axis is
a good *prioritization* signal (where to look first) but not a *sufficient* second-axis signal by
itself — a low-citation pattern still needs a `grep`-against-`services/` check before calling it
inert, not just a citation-count threshold. Worth flagging to Arch/CIO in case methodology-core's
disposition is using citation count more heavily as a decision signal rather than a triage signal.

| Tier | File | ID | Deduped cites | Most recent | Own status | Disposition |
|---|---|---|---|---|---|---|
| A: CLAUDE.md/skills-cited (definitely current law) | pattern-045-green-tests-red-user.md | P-045 | 403 | 2026-08-29 | Established | **EFFECTIVE** — CLAUDE.md/skill-cited (already load-bearing in active workflow), no internal supersession marker, spot-checked not full-grepped (citation strength here already implies liveness; the B3 rule's grep requirement is for archive-leaning calls). |
| A: CLAUDE.md/skills-cited (definitely current law) | pattern-062-assembly-assumption.md | P-062 | 304 | 2026-08-29 | - | **EFFECTIVE** — CLAUDE.md/skill-cited (already load-bearing in active workflow), no internal supersession marker, spot-checked not full-grepped (citation strength here already implies liveness; the B3 rule's grep requirement is for archive-leaning calls). |
| A: CLAUDE.md/skills-cited (definitely current law) | pattern-064-extension-without-integration.md | P-064 | 225 | 2026-08-29 | - | **EFFECTIVE** — CLAUDE.md/skill-cited (already load-bearing in active workflow), no internal supersession marker, spot-checked not full-grepped (citation strength here already implies liveness; the B3 rule's grep requirement is for archive-leaning calls). |
| A: CLAUDE.md/skills-cited (definitely current law) | pattern-049-audit-cascade.md | P-049 | 123 | 2026-08-25 | - | **EFFECTIVE** — CLAUDE.md/skill-cited (already load-bearing in active workflow), no internal supersession marker, spot-checked not full-grepped (citation strength here already implies liveness; the B3 rule's grep requirement is for archive-leaning calls). |
| A: CLAUDE.md/skills-cited (definitely current law) | README.md | - | 88 | 2026-08-25 | - | **EFFECTIVE** — CLAUDE.md/skill-cited (already load-bearing in active workflow), no internal supersession marker, spot-checked not full-grepped (citation strength here already implies liveness; the B3 rule's grep requirement is for archive-leaning calls). |
| A: CLAUDE.md/skills-cited (definitely current law) | pattern-046-beads-completion-discipline.md | P-046 | 81 | 2026-08-29 | Established | **EFFECTIVE** — CLAUDE.md/skill-cited (already load-bearing in active workflow), no internal supersession marker, spot-checked not full-grepped (citation strength here already implies liveness; the B3 rule's grep requirement is for archive-leaning calls). |
| A: CLAUDE.md/skills-cited (definitely current law) | pattern-047-time-lord-alert.md | P-047 | 58 | 2026-08-27 | Established | **EFFECTIVE** — CLAUDE.md/skill-cited (already load-bearing in active workflow), no internal supersession marker, spot-checked not full-grepped (citation strength here already implies liveness; the B3 rule's grep requirement is for archive-leaning calls). |
| A: CLAUDE.md/skills-cited (definitely current law) | PATTERN-FAMILIES.md | - | 16 | 2026-08-24 | - | **EFFECTIVE** — CLAUDE.md/skill-cited (already load-bearing in active workflow), no internal supersession marker, spot-checked not full-grepped (citation strength here already implies liveness; the B3 rule's grep requirement is for archive-leaning calls). |
| B: heavily-cited + recent (very likely current law) | pattern-073-documentation-asserted-behavior-drift.md | P-073 | 412 | 2026-08-29 | - | *pending* |
| B: heavily-cited + recent (very likely current law) | pattern-063-parallel-authoring-drift.md | P-063 | 215 | 2026-08-29 | - | *pending* |
| B: heavily-cited + recent (very likely current law) | pattern-072-registries-that-grow-into-architectural-shapes.md | P-072 | 129 | 2026-08-29 | - | *pending* |
| B: heavily-cited + recent (very likely current law) | pattern-067-issue-body-reality-mismatch.md | P-067 | 124 | 2026-08-29 | - | *pending* |
| B: heavily-cited + recent (very likely current law) | pattern-070-cleanup-job-with-cancellation-hygiene.md | P-070 | 114 | 2026-08-29 | - | *pending* |
| B: heavily-cited + recent (very likely current law) | pattern-068-silent-state-mutation-shared-working-tree.md | P-068 | 99 | 2026-08-29 | - | *pending* |
| B: heavily-cited + recent (very likely current law) | pattern-034-error-handling-standards.md | P-034 | 64 | 2026-08-13 | ✅ Active | *pending* |
| B: heavily-cited + recent (very likely current law) | pattern-071-audit-logs-as-attack-surface.md | P-071 | 63 | 2026-08-29 | - | *pending* |
| B: heavily-cited + recent (very likely current law) | pattern-029-multi-agent-coordination.md | P-029 | 60 | 2026-08-12 | - | **EFFECTIVE** — heavily-cited+recent, no supersession marker, light-touch per the B3 rule (grep-verify reserved for archive-leaning calls). |
| B: heavily-cited + recent (very likely current law) | pattern-012-llm-adapter.md | P-012 | 59 | 2026-07-16 | - | **EFFECTIVE** — heavily-cited+recent, no supersession marker, light-touch per the B3 rule (grep-verify reserved for archive-leaning calls). |
| B: heavily-cited + recent (very likely current law) | pattern-050-context-dataclass-pair.md | P-050 | 58 | 2026-08-24 | Proven | **EFFECTIVE** — heavily-cited+recent, no supersession marker, light-touch per the B3 rule (grep-verify reserved for archive-leaning calls). |
| B: heavily-cited + recent (very likely current law) | pattern-074-visibility-loss-after-premature-retirement.md | P-074 | 54 | 2026-08-29 | - | **EFFECTIVE** — heavily-cited+recent, no supersession marker, light-touch per the B3 rule (grep-verify reserved for archive-leaning calls). |
| B: heavily-cited + recent (very likely current law) | pattern-032-intent-pattern-catalog.md | P-032 | 53 | 2026-08-13 | - | **EFFECTIVE** — heavily-cited+recent, no supersession marker, light-touch per the B3 rule (grep-verify reserved for archive-leaning calls). |
| B: heavily-cited + recent (very likely current law) | pattern-054-honest-failure.md | P-054 | 52 | 2026-08-24 | Proven | **EFFECTIVE** — heavily-cited+recent, no supersession marker, light-touch per the B3 rule (grep-verify reserved for archive-leaning calls). |
| B: heavily-cited + recent (very likely current law) | pattern-069-coarse-triggers-false-positive-triage-cost.md | P-069 | 46 | 2026-08-29 | - | **EFFECTIVE** — heavily-cited+recent, no supersession marker, light-touch per the B3 rule (grep-verify reserved for archive-leaning calls). |
| B: heavily-cited + recent (very likely current law) | pattern-007-async-error-handling.md | P-007 | 45 | 2026-08-28 | - | **EFFECTIVE** — heavily-cited+recent, no supersession marker, light-touch per the B3 rule (grep-verify reserved for archive-leaning calls). |
| B: heavily-cited + recent (very likely current law) | pattern-053-warmth-calibration.md | P-053 | 45 | 2026-08-24 | Proven | **EFFECTIVE** — heavily-cited+recent, no supersession marker, light-touch per the B3 rule (grep-verify reserved for archive-leaning calls). |
| B: heavily-cited + recent (very likely current law) | pattern-060-cascade-investigation.md | P-060 | 44 | 2026-08-10 | - | **EFFECTIVE** — heavily-cited+recent, no supersession marker, light-touch per the B3 rule (grep-verify reserved for archive-leaning calls). |
| B: heavily-cited + recent (very likely current law) | pattern-031-plugin-wrapper.md | P-031 | 42 | 2026-08-24 | Active | **EFFECTIVE** — heavily-cited+recent, no supersession marker, light-touch per the B3 rule (grep-verify reserved for archive-leaning calls). |
| B: heavily-cited + recent (very likely current law) | pattern-051-parallel-place-gathering.md | P-051 | 41 | 2026-08-24 | Proven | **EFFECTIVE** — heavily-cited+recent, no supersession marker, light-touch per the B3 rule (grep-verify reserved for archive-leaning calls). |
| B: heavily-cited + recent (very likely current law) | pattern-052-personality-bridge.md | P-052 | 40 | 2026-08-24 | Proven | **EFFECTIVE** — heavily-cited+recent, no supersession marker, light-touch per the B3 rule (grep-verify reserved for archive-leaning calls). |
| C: middle tier (needs individual read) | META-PATTERNS.md | - | 60 | 2026-06-17 | Established | *pending* |
| C: middle tier (needs individual read) | pattern-059-leadership-caucus.md | P-059 | 51 | 2026-06-17 | - | *pending* |
| C: middle tier (needs individual read) | pattern-008-ddd-service-layer.md | P-008 | 49 | 2026-06-17 | - | *pending* |
| C: middle tier (needs individual read) | pattern-006-verification-first.md | P-006 | 38 | 2026-06-17 | - | *pending* |
| C: middle tier (needs individual read) | PROTO-PATTERNS.md | - | 37 | 2026-07-30 | - | *pending* |
| C: middle tier (needs individual read) | pattern-066-stacked-silent-failures.md | P-066 | 36 | 2026-08-29 | - | *pending* |
| C: middle tier (needs individual read) | pattern-001-repository.md | P-001 | 34 | 2026-07-28 | - | *pending* |
| C: middle tier (needs individual read) | pattern-000-template.md | P-000 | 33 | 2026-08-10 | - | *pending* |
| C: middle tier (needs individual read) | pattern-042-investigation-only-protocol.md | P-042 | 32 | 2026-06-17 | - | *pending* |
| C: middle tier (needs individual read) | pattern-021-development-session-management.md | P-021 | 31 | 2026-06-15 | - | *pending* |
| C: middle tier (needs individual read) | pattern-028-intent-classification.md | P-028 | 31 | 2026-06-17 | - | *pending* |
| C: middle tier (needs individual read) | pattern-065-continuity-memo-before-the-seam.md | P-065 | 30 | 2026-08-29 | - | *pending* |
| C: middle tier (needs individual read) | pattern-020-spatial-metaphor-integration.md | P-020 | 29 | 2026-02-03 | - | *pending* |
| C: middle tier (needs individual read) | pattern-061-human-ai-collaboration-referee.md | P-061 | 29 | 2026-08-17 | - | *pending* |
| C: middle tier (needs individual read) | pattern-002-service.md | P-002 | 28 | 2026-06-17 | - | *pending* |
| C: middle tier (needs individual read) | pattern-041-systematic-fix-planning.md | P-041 | 28 | 2026-06-17 | - | *pending* |
| C: middle tier (needs individual read) | pattern-030-plugin-interface.md | P-030 | 27 | 2026-06-17 | - | *pending* |
| C: middle tier (needs individual read) | pattern-010-cross-validation-protocol.md | P-010 | 24 | 2026-06-11 | - | *pending* |
| C: middle tier (needs individual read) | pattern-038-temporal-clustering.md | P-038 | 23 | 2026-05-09 | Active | *pending* |
| C: middle tier (needs individual read) | pattern-044-mcp-skill-testing.md | P-044 | 23 | 2026-05-09 | Established | *pending* |
| C: middle tier (needs individual read) | pattern-033-notion-publishing.md | P-033 | 22 | 2026-08-13 | - | *pending* |
| C: middle tier (needs individual read) | pattern-036-signal-convergence.md | P-036 | 22 | 2026-05-09 | Active | *pending* |
| C: middle tier (needs individual read) | pattern-037-cross-context-validation.md | P-037 | 22 | 2026-05-28 | Active | *pending* |
| C: middle tier (needs individual read) | pattern-043-defense-in-depth-prevention.md | P-043 | 22 | 2026-06-17 | - | *pending* |
| C: middle tier (needs individual read) | pattern-017-background-task-error-handling.md | P-017 | 21 | 2026-06-17 | - | *pending* |
| C: middle tier (needs individual read) | pattern-039-feature-prioritization-scorecard.md | P-039 | 21 | 2026-05-09 | - | *pending* |
| C: middle tier (needs individual read) | pattern-048-periodic-background-job.md | P-048 | 21 | 2026-08-18 | Proven | *pending* |
| C: middle tier (needs individual read) | grammar-application-patterns.md | - | 20 | 2026-08-24 | - | *pending* |
| C: middle tier (needs individual read) | pattern-011-context-resolution.md | P-011 | 20 | 2026-05-09 | - | *pending* |
| C: middle tier (needs individual read) | pattern-040-integration-swappability-guide.md | P-040 | 20 | 2026-05-09 | - | *pending* |
| C: middle tier (needs individual read) | pattern-003-factory.md | P-003 | 18 | 2026-03-03 | - | *pending* |
| C: middle tier (needs individual read) | pattern-009-github-issue-tracking.md | P-009 | 18 | 2026-06-17 | - | *pending* |
| C: middle tier (needs individual read) | pattern-024-methodology-patterns.md | P-024 | 17 | 2026-08-03 | - | *pending* |
| C: middle tier (needs individual read) | pattern-035-mcp-adapter-methods.md | P-035 | 17 | 2026-07-29 | - | *pending* |
| C: middle tier (needs individual read) | pattern-004-cqrs-lite.md | P-004 | 14 | 2026-02-03 | - | *pending* |
| C: middle tier (needs individual read) | pattern-005-transaction-management.md | P-005 | 13 | 2026-05-09 | - | *pending* |
| C: middle tier (needs individual read) | pattern-014-error-handling-api-contract.md | P-014 | 13 | 2026-02-03 | - | *pending* |
| C: middle tier (needs individual read) | pattern-055-multi-intent-decomposition.md | P-055 | 12 | 2026-08-29 | - | *pending* |
| C: middle tier (needs individual read) | pattern-013-session-management.md | P-013 | 11 | 2026-06-17 | - | *pending* |
| C: middle tier (needs individual read) | pattern-022-mcp-spatial-intelligence-integration.md | P-022 | 11 | 2026-07-30 | - | *pending* |
| C: middle tier (needs individual read) | pattern-027-cli-integration.md | P-027 | 10 | 2026-06-11 | - | *pending* |
| C: middle tier (needs individual read) | pattern-023-query-layer-patterns.md | P-023 | 9 | 2026-05-09 | - | *pending* |
| C: middle tier (needs individual read) | pattern-025-canonical-query-extension.md | P-025 | 9 | 2026-05-09 | - | *pending* |
| C: middle tier (needs individual read) | pattern-056-consciousness-attribute-layering.md | P-056 | 9 | 2026-06-17 | - | *pending* |
| C: middle tier (needs individual read) | pattern-057-grammar-driven-classification.md | P-057 | 8 | 2026-08-29 | - | *pending* |
| C: middle tier (needs individual read) | pattern-018-configuration-access.md | P-018 | 7 | 2026-05-09 | - | **EFFECTIVE (principle), illustrative code diverges** — the architectural concern (layer-appropriate config access via DI) is genuinely live (`services/config/llm_config_service.py`, `services/config/github_config.py`, `services/infrastructure/config/feature_flags.py`), but the pattern's own sample code names (`ConfigurationAccessManager`, `ConfigService`) don't literally exist — the doc illustrates the principle rather than quoting production code verbatim, which is a normal pattern-doc shape, not evidence of staleness. |
| C: middle tier (needs individual read) | pattern-058-ownership-graph-navigation.md | P-058 | 6 | 2026-06-12 | - | **EFFECTIVE, strongly confirmed** — its exact NATIVE/FEDERATED/SYNTHETIC three-tier model is implemented verbatim in `services/mux/ownership.py`, referenced from `shared_types.py` with a direct pointer to `ownership-metaphors.md` and ADR-045. Foundational, not marginal. |
| C: middle tier (needs individual read) | pattern-019-llm-placeholder-instruction.md | P-019 | 4 | 2026-05-09 | - | **EFFECTIVE** — the placeholder-slot mechanism it describes is directly implemented in `services/intent_service/conversational_floor.py` (`_PLACEHOLDER_SLOT_RE` regex + replacement logic), the core conversational floor component. Only 4 citations but genuinely load-bearing. |
| D: old + low-citation (likely historical, needs read) | pattern-026-cross-feature-learning.md | P-026 | 12 | 2026-02-03 | - | **EFFECTIVE (reclassify to B)** — actively imported into `services/intent/intent_service.py` + 5 other live service files via `query_learning_loop.py`. Citation count is low but the mechanism is genuinely live. Low citation ≠ inert; verified against code, not just census. |
| D: old + low-citation (likely historical, needs read) | pattern-015-internal-task-handler.md | P-015 | 6 | 2026-03-30 | - | **HISTORICAL** — zero code hits for "internal task handler" anywhere in `services/`. Describes an orchestration-engine model with no live implementation found. Candidate for archive-with-marker. |
| D: old + low-citation (likely historical, needs read) | pattern-016-repository-context-enrichment.md | P-016 | 6 | 2026-02-03 | - | **LIKELY HISTORICAL** — one tangential comment in `action_registry.py` mentions "InsightRepository context enrichment," but `context_assembler.py` (the file the pattern's own mechanism would live in) has zero matches for the described enrichment logic. Not as clean a case as P-015 — flagging the caveat rather than overclaiming certainty. |
| D: old + low-citation (likely historical, needs read) | proposals/pattern-family-index-proposal.md | - | 4 | 2026-02-05 | - | **ABSORBED** — this is the original proposal (Docs, 2026-02-05) that became `PATTERN-FAMILIES.md` (now live, Tier A, CLAUDE.md/skill-cited). Different disposition class from the other three: not "historical/inert," but "superseded-by-its-own-implementation." Candidate for archive with an explicit "implemented as PATTERN-FAMILIES.md" marker. |
