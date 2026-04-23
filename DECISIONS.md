# Decision Log

Append-only record of decisions made in this project. One line per decision.
Format: DATE | DECISION | PARTICIPANTS

For major architectural decisions, write a full ADR. This log is the lightweight index underneath — greppable by the daily brief and other agents.

---

2026-04-10 | Todo completion bug fix landed (#926/#904) — distinct from todo delete bug (M1 blocker) | PA + Lead Dev
2026-04-15 | Haiku 3 to 4.5 migration completed via #979, 3 days ahead of Apr 19 retirement | PA + Lead Dev
2026-04-15 | Gemini wired as real primary/fallback (#988) | Lead Dev
2026-04-15 | M2b testing track closed in single session: E2E, canonical, AAXT, CI | Lead Dev
2026-04-16 | #950 floor prompt approved with 2 minor edits ("emotion you can't have" → "emotion without specifics"; "not every sentence" reworded) | CXO + Lead Dev
2026-04-16 | Ethics denial voice guidance: "the enforcer detects, but Piper speaks" — BoundaryEnforcer returns structured object, floor LLM generates decline using templates | CXO
2026-04-16 | ETHICS-ACTIVATE requires voice guidance as acceptance criterion before production enable | CXO + Lead Dev
2026-04-16 | Excellence Flywheel structural type: three layers (concept / practice / mnemonic), not competing formulations | CIO
2026-04-16 | CLAUDE.md Option B — operational principles stand without the Flywheel label (avoid per-role paraphrase drift) | CIO + PM
2026-04-16 | Add "Audit the composition" as 5th Flywheel practice — Pattern-062 formalization | CIO
2026-04-16 | Flywheel reformulation is the M1 audit's headline deliverable (not a parallel track) | CIO
2026-04-16 | Adopt known_pathological tagging for v2 canonical retest corpus (from OpenLaws eval harness) — labeling only, no query changes | PPM + PA
2026-04-16 | Adopt AAXT six-failure-mode vocabulary in #929 DeepEval scorer (if vocabulary still mutable) | Architect + CXO
2026-04-16 | Build 5-10 fabrication probes across 5 absence categories — M2a or standalone | Architect
2026-04-16 | Fabrication probes are a separate instrument (not a Colleague Test rubric dimension) — rubric stays at R/C/T | Architect + CXO
2026-04-18 | Adopt DECISIONS.md practice cross-project (this file) — anti-zombie decision tracking | PM + Dispatch
2026-04-18 | Publish-to-blog skill heading convention: `#` → `<h1>`, `##` → `<h2>` in output HTML (preserves hierarchy through LinkedIn syndication) | Docs
2026-04-18 | MCP URI namespace: `piper-morgan://` scheme, parallel to `klatch://` — route by scheme; shared `/{id}/manifest` sub-resource | Architect + Daedalus (Klatch)
2026-04-18 | MCP tool naming: `get_context_package` as shared name across DinP products; product-specific tools use product-specific names | Architect + Daedalus (Klatch)
2026-04-19 | Workstream memo naming standard: `workstream-{ship#}-{role}-{date}.md` — effective Ship #040 onward | Exec + PM
2026-04-19 | Colleague Test v2 structure: additive changes only, preserving R/C/T framework and cross-sprint comparability | CXO
2026-04-19 | Colleague Test Context 2 vs 3 distinction: 2 = general LLM competence, 3 = assembled project context — diagnostic for "is the context assembler working" | CXO
2026-04-19 | Colleague Test degradation minimum bar: no auto-fails on fallback / error / decline responses, even if total <7 | CXO
2026-04-21 | Chat-to-Code migration for all roles — starting 2026-04-22, sequence HOST+CIO first, then memo-writers, then CoS last with full handoff | PM + Exec
2026-04-22 | Publish-to-blog skill v0.8: explicit blog-content.json schema ({title, content} dict — not bare string); preserve non-metadata HTML comments | Docs + PM
2026-04-22 | Patterns/README.md wording: "62 patterns (001-062), plus a template (000)" — template counted as file but not as a pattern | Docs
2026-04-22 | Create-omnibus skill Step 2.5 Cross-Reference Gate: scan source logs for agent-role mentions; any mentioned-but-missing role must be fetched or documented, never silently papered over | Docs + PM
2026-04-22 | #992 ETHICS-ACTIVATE flag-flip mechanism: add `ENABLE_ETHICS_ENFORCEMENT=true` to `docker-compose.yml` app service env block (Option A). Rejected: staging-first (ceremony too heavy), Python default flip (inverts mental model), flag removal (premature loss of kill switch) | PM + Lead Dev
2026-04-22 | #992 ETHICS-ACTIVATE framed within PDR-004 Principle 4 Mode 2 scope — no new ADR planned unless Architect flags BoundaryEnforcer structured-return shape or FloorContext mode-switching as pattern-worthy | PM + Lead Dev
2026-04-22 | #992 Phase A: BoundaryDecision.redirect_context is category-derived only (not pattern-derived). Keeps audit-safety property — raw user content + literal pattern strings never flow to user-facing voice. Trade-off: all three messages in a category get the same hint; tailoring happens at the floor LLM layer, not the enforcer | Lead Dev
