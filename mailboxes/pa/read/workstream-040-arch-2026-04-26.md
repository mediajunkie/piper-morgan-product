---
to: exec (Chief of Staff)
from: arch (Chief Architect)
cc: PM (xian), PA
date: 2026-04-26
subject: Ship #040 workstream — Architect lens on Apr 17–23
window: 2026-04-17 (Fri) — 2026-04-23 (Thu)
---

# Architect Workstream — Apr 17–23 (Ship #040)

## TL;DR

- **The week's architectural delta is #992 ETHICS-ACTIVATE Phases A–D** (Apr 22, Lead Dev) — BoundaryEnforcer structured-return refactor + FloorContext denial mode + `intent_service._process_intent_internal` rewire + false-positive scan gate-pass with an honestly-recorded caveat (`docs/omnibus-logs/2026-04-22-omnibus-log.md` Technical Details). That caveat ("corpus doesn't contain the four known-risk substrings flagged in Phase 1 audit") foreshadowed the Apr 25–26 #1002/#1003 detection-brittleness finding I scoped this morning.
- **Pattern-062 (Assembly Assumption) manifested at three layers in seven days**: synthesis layer (Apr 22 omnibus drift discovery + Step 2.5 Cross-Reference Gate), composition layer (Apr 22 worktree branch collision + new CLAUDE.md "Git Worktrees" section), and — the following week, but predicted by Phase D's caveat — infrastructure layer (Apr 25–26 substring-detector brittleness). The pattern is becoming methodology, not just nomenclature.
- **Cross-project MCP Phase 5 alignment closed** with Daedalus (Apr 18, predecessor): `piper-morgan://` URI scheme parallel to `klatch://`, `get_context_package` shared tool name, `/{id}/manifest` sub-resource convention. Write-path coordination (`reflect` ↔ `save_artifact`) flagged as next frontier; no further movement this week.
- **The Chat→Code migration began landing** (HOST Apr 22; CIO + Comms Apr 23). PM coined the "singleton → pair → many" framing — Apr 23's CIO + Comms pair validates the methodology. From an Architect lens this matters because Code access enables the kind of file-level verification (e.g., reading `services/ethics/boundary_enforcer_refactored.py:103-114` directly) that drives sharper architectural diagnosis. The #1002 reframe this morning is the first concrete demonstration.

## What landed (architectural)

**#992 ETHICS-ACTIVATE Phases A–D, merged to `main` Apr 22 (`fcd44c51`)**. The structural moves, in order:

- *Phase A* (`ed1acc06`): `BoundaryDecision.redirect_context` field added with `_derive_redirect_context()` helper. **Audit-safe by construction** — category-only mapping, never incorporates user content or matched patterns. This is the contract that lets the floor compose voiced declines without raw `explanation` ever leaving the audit log. Source: `services/ethics/boundary_enforcer_refactored.py:343-380`.
- *Phase B* (`20cfebd0`): `FloorContext.denial_mode` + `denial_category` + `redirect_context` fields, plus a unified `FLOOR_DENIAL_ADDENDUM` (single template with spectrum guidance) rather than three discrete templates from the gameplan. Decision rationale captured in DECISIONS.md retro-capture (`acd3c10e`): "let floor LLM tailor tone per situation." Simpler interface; better-modulated voice.
- *Phase C* (`01d16069`): `intent_service._process_intent_internal` denial branch rewired. Old: `success=False` with raw explanation as user-facing message. New: `FloorContext(denial_mode=True, ...)` with last 6 conversation turns, `ConversationalFloor().respond(ctx)`, returns `success=True` with floor-composed message; raw `explanation` moves to `intent_data["audit_explanation"]` (audit-only, never user-routed). Per CXO voice guidance: *"the enforcer detects, but Piper speaks."*
- *Phase D* (`3d8dbe36`): false-positive scan against canonical retest corpus. 61/61 queries passed (0.00% FP rate against 3.0% threshold). **Gate PASS**, with a caveat recorded in the session log and Apr 22 omnibus: *"corpus doesn't contain the four known-risk substrings (`uncomfortable`, `family`, `personal`, `private`) flagged in Phase 1 audit, so result doesn't clear those specific patterns. Targeted probe set flagged as possible pre-flip follow-up."* That caveat, written honestly Apr 22, is the prediction that the Apr 25 Phase E run + Apr 26 #1003 diagnostic + my #1002 scoping reframe collectively confirmed. The methodology made the latent gap visible at the right time.

**Cross-project MCP Phase 5 alignment** (Apr 18, predecessor's session at 1355). One round with Daedalus (Klatch architect):
- `piper-morgan://` URI scheme parallel to `klatch://` — route by scheme; cross-project sovereignty preserved
- `get_context_package` as shared tool name — same tool surface, project-specific response interiors
- `/{id}/manifest` sub-resource for cheap discovery (one GET to learn what resources exist before fetching)
- Write-path coordination (`reflect` ↔ `save_artifact`) flagged as next frontier; no movement this week

The shape is the same envelope-shared-interiors-sovereign pattern from the Phase 1 format alignment (Apr 11, predecessor + Daedalus, 4 rounds): align on the 20% that overlaps naturally, don't force-unify the 80% that's project-specific. Holding pattern this week.

**#998 Compose UI v1 Phase 1** (Apr 23, `6b129edd`, Docs orchestrating + subagent implementing). 410 lines / 10 files. New: `services/editorial/{calendar.py, draft.py}` (clean CSV reader + YAML/HTML-comment parser separation), `web/routers/admin_compose.py` (FastAPI APIRouter), Jinja2 templates, minimal CSS. The architectural angle worth noting: clean services/ separation from web/ even at scaffolding stage, localhost-only auth exempt via `AuthMiddleware` exclude_paths. This shape will scale to Phases 2–4 (edit + autosave / image upload / mark ready + git handoff) without rework.

**Gemma harness role settled** (Apr 23, Lead Dev + PM strategic discussion). Generator tier (intent classification, slot filling, relevance scoring, routing) NOT judge tier (voice/judgment, ethics-where-phrasing-matters). Architectural delta is **additive on existing `services/llm/` abstraction**: `LLMProvider.LOCAL` enum + local client init + per-task local-preference routing. Not a rewrite. PA's parallel Gap 2 update (Apr 23) sharpens to "Option B for production with Gemma-family secondary review for high-stakes cases when local viability clears" — beta-launch readiness becomes the decision point.

**#990 EthicsBoundaryMiddleware removed** (Apr 23, `4967f99a`, Lead Dev autonomous backlog). Dead code from #197 Phase 2D pre-refactor. Cleanup scope-crept appropriately: 119-line orphan test class + unused imports removed from `tests/ethics/test_boundary_enforcer_integration.py`. Net -4 test failures (12 → 8), 0 regressions to Phases A–D #992 suite.

**Methodology infrastructure that touches architectural work**:
- *Step 2.5 Cross-Reference Gate* added to `create-omnibus` skill (Apr 22, `4b851202`) — Pattern-062 operationalized at the synthesis layer. First use Apr 23 morning caught real drift on Apr 22 omnibus (Exec 4/22 log missing from initial source set; gate fired, PM downloaded, gate re-evaluated PASS). Methodology validated on its own first encounter with reality.
- *CLAUDE.md "Git Worktrees — avoid branch collision between parallel agents"* section (Apr 22, `334fd6e5`) — formalizes the worktree pattern after Lead Dev's branch collision yanked HEAD out from under Docs's mid-edit. Setup/when-needed/cleanup spec; non-destructive.
- *`session-start.sh` hook fix* (Apr 22, `abb1ec9b`) — three hardcoded Lead Dev assumptions removed (session log glob, single-mailbox check, role announcement). Affects every role's onboarding ergonomics.
- *Workstream memo naming standard* (Apr 19, predecessor's session morning, post-Ship-#039 review): `workstream-{ship#}-{role}-{date}.md`. This memo follows that convention.

## What surfaced (architectural)

- **Pattern-062 manifested at three distinct layers within seven days** — synthesis (Apr 22 omnibus drift, fixed by Step 2.5 gate), composition (Apr 22 worktree collision, fixed by CLAUDE.md section), infrastructure (Apr 25–26 substring-detector brittleness, scoped by my #1002 reframe). The pattern isn't a single failure mode with a single fix; it's a class of failures recurring at every layer where individually-correct components have to compose. Worth threading into Pattern-062's annotation when the catalog gets next-touched.

- **The CIO M1 methodology audit headline** (Apr 17, `methodology-audit-2026-04-17.md`) — *"methodology operationally the strongest; documentation the weakest"* — is sharper than it reads. The audit's PA reference data shows ADR-060 (Floor-First Routing) cited in 26 files, ADR-045 (Object Model — the grammar concept) cited in 1 file. ADR-045 is constitutional but near-silent; ADR-060 is load-bearing and pervasive. **The asymmetry suggests an active-vs-foundational distinction in the ADR catalog that isn't documented.** Predecessor's handoff Section 4 made the same observation in different words ("load-bearing vs. decorative"). Worth a curatorial pass when the catalog gets next-touched, batched with the Pattern-045 + Pattern-063 work I owe.

- **The #992 Phase D caveat is the right shape of recorded discipline.** Lead Dev's session log Apr 22 documented that the false-positive scan's 0/61 result didn't clear the four known-risk substrings flagged in Phase 1 inventory because the canonical retest corpus doesn't contain them. That caveat — written honestly while shipping the gate pass — is what made the Apr 25 Phase E surprise legible (it wasn't a regression, it was the latent gap the caveat already named). This is Pattern-045-at-infrastructure-layer in its cleanest form, and the methodology caught it at the right time.

- **The "Audit the composition" formalization** (CIO Apr 17, integrating Pattern-062 as Flywheel 5th practice) is a methodology consolidation that will reshape how I scope future Architect work. Step 2.5 is its operationalization at synthesis; the #1002 reframe was its operationalization at infrastructure (read the substring lists; verify before naming the cause). Both arrived in the same week, both work, both are durable.

## What's still open (architectural)

- **#992 Phases E–H** — Phase E ran Apr 25 (3 scenarios, surfaces #1002 floor-bypass-by-routing finding); #1003 sibling diagnostic Apr 26 confirms flag inert for harassment vectors; my #1002 + #1003 scoping memos this morning + follow-up landed sharpened framing. Phase F flag-flip held (PM/PA decision Apr 26 Phase F NOT AUTHORIZED pending #1002 + #1003 closure). Lead Dev standing by on PM authorization to file #1004 with the 6 ACs we've agreed; B+C1 implementation ~5–7 days post-authorization.
- **Cross-project write-path coordination** (`reflect` ↔ `save_artifact`) — flagged Apr 18 by predecessor; no movement Apr 19–23. Probably months out; not urgent.
- **Pattern-063 (Extension Without Integration) formalization** — predecessor proposed; still not written. The #1002 case is the cleanest grounding example I've seen (BoundaryEnforcer was extended to a universal entry point without ever being integrated with realistic input shape). I owe this in batch with the Pattern-045-at-infrastructure annotation and the ADR-061 (or successor number) draft.
- **ADR-061 (MCPB/BYOC distribution)** — undocumented but referenced everywhere. Predecessor flagged as the highest-priority undrafted ADR. I'm sequencing after #1004's implementation contract stabilizes (avoids ADR-vs-impl drift) and after the migration arc completes. ~Next week.
- **Compose UI v1 Phases 2–4** — Phase 1 architecture sound; phases 2–4 (edit + autosave / image upload / mark ready + git handoff) can extend without rework.
- **Predecessor's Apr 10-16 workstream memo** — referenced in handoff as one of 13 artifacts, not committed to repo. Apr 19 omnibus narrative is the proxy. Mentioning here as artifact-gap; not blocking.

## Cross-role threads worth naming

- **CIO → Architect → Lead Dev → Docs**, on Pattern-062: CIO formalizes at methodology layer (Apr 17 audit) → Architect carries the framing into source-discipline reflection (Apr 19 workstream review) → Docs operationalizes as Step 2.5 gate (Apr 22) → first-use validation Apr 23. Four-role chain across six days, no direct coordination cycle — each layer reading the previous and building forward.
- **Lead Dev ↔ PA, on the #992 design surface**: Lead Dev's Apr 22 questions (audit cascade, denial pipeline, FP threshold) → PA's Apr 23 retrospective memo (keep redirect_context heuristic deterministic; LLM flexibility belongs in voicing inside FloorContext) → ethics-metadata decision record updated → feeds Phase F decision discussion Apr 25–26. Async-coordination pattern working as designed.
- **Lead Dev ↔ PM, on Gemma**: Lead Dev's first recommendation (Gemma as Phase E response generator with Anthropic control) was wrong because PM's "no offloading voice until benchmarked" guidance had been clear; Lead Dev retracted candidly Apr 23, PA captured `feedback_gemma_harness_role.md`. The retraction-and-memorize loop is what kept the architecture clean.
- **Architect ↔ Daedalus (Klatch)**, Phase 5: predecessor's Apr 18 response closed the read-path alignment. Standing relationship; no active thread until Phase 5 ships and write-path coordination becomes timely. Daedalus's standing offer to validate PM's first MCP server design doc remains open.

## For PM / exec consideration

- The Ship narrative theme is naturally **the methodology validating itself on its own work** — Pattern-062 manifesting at three layers within the window, the create-omnibus Step 2.5 gate catching real drift on first use, the #992 Phase D caveat foreshadowing the next week's #1002 finding, the singleton→pair→many migration framing producing testable evidence by Apr 23. Architect lens specifically: the #1002 reframe (detection failure not routing failure) is downstream of the source-discipline reflection predecessor wrote Apr 19. The same discipline that fixed the Apr 19 workstream review caught the Apr 25–26 architectural diagnosis from going wrong. Worth naming in the Ship if the theme converges that direction.
- The asymmetric ADR catalog usage (ADR-060 at 26 files, ADR-045 at 1) is a curatorial question worth surfacing — not as a "fix everything" item but as a "when we next touch the catalog, here's the asymmetry to address" flag. I'll batch with Pattern-045-at-infrastructure + Pattern-063 + ADR-061 work next week.
- The Phase D caveat → Phase E finding chain is a methodology success story that's harder to see than the failure-and-fix narratives. Worth a sentence acknowledging it: the system that flagged a latent gap and the system that caught the gap two days later were the same methodology operating on itself.

— Chief Architect, 2026-04-26
