# Pattern-073: Documentation-Asserted-Behavior Drift

## Status

**Proven** — Promoted from Emerging 2026-05-18 (CIO catalog-management authority, per `memo-cio-to-lead-cc-ceo-arch-host-exec-pa-pattern-073-promotion-ratified-emerging-to-proven-2026-05-18.md`). Emerging filing 2026-05-16 by Lead Developer per CIO methodology disposition (`memo-cio-to-lead-arch-cc-ceo-pattern-073-disposition-2026-05-16.md`). **Fourteen reference instances across eleven distinct surface layers** logged during the May 15–20 evidence-accumulation window; cross-agent engagement during that window (Lead Dev + CIO + Architect + HOST + PM) validated the recognition discipline empirically even ahead of the formal `doc-sync-sweep` skill v1.0 cross-agent-application criterion. **Methodology-29 ("Pattern Formation via Successful Imitation") three-instance threshold massively exceeded**; 11-layer breadth establishes the pattern as structural rather than layer-specific.

**Resolution-shape framing** (CIO Q5 disposition, Instance 11): the pattern's characteristic fix is *removing the misleading surface* (the dead method, the asserted-but-unimplemented behavior, the stale claim), not racing to build the asserted behavior. Cleanup IS the resolution. The pattern's name ("Documentation-Asserted-Behavior Drift") describes the failure mode; the resolution discipline is **cleanup-as-truth-restoration**. This distinguishes Pattern-073 from generic Pattern-064 alive-scaffolding shapes — Pattern-064 names code that pretends to do work; Pattern-073 names narrative that asserts work the code doesn't deliver. The fix is the same shape (remove the misleading surface) but the catch-trigger is different.

**In-flight refinement** (not gating Proven status): `doc-sync-sweep` skill v0.1 → v1.0 + cross-agent application remains queued as operational improvement on the now-Proven pattern. Slot 073 allocated after 12l pre-filing slot-availability check; 070/071/072 occupied. CIO methodology cosign on the Pattern-064-adjacent framing.

## Product Relevance

**Methodology / Discipline** — Recognition discipline for a specific evolution shape that affects how teams maintain *narrative artifacts* (documentation, docstrings, comments, issue bodies, test fixtures, templated user-facing copy) as the code they describe drifts. Users will not encounter this pattern directly; agents and engineers reading and writing the project's narrative surfaces will reach for it when judging whether an assertion in prose still matches the system's behavior.

## Context

Documentation, docstrings, comments, issue bodies, test fixtures, and user-facing canned response copy are all *narrative artifacts about the system*. They assert claims like "this function commits on success," "this route reads `request.state.user_id`," "all open PRs are less than 7 days old," "moderate-complexity tasks produce 2-3 subtasks." When the code that the narrative describes changes — or never matched the narrative — the assertion becomes drift: structurally well-formed, semantically wrong.

### Where this surfaced

Fourteen independent instances within ≤120 hours (May 15-20, 2026) across **eleven distinct surface layers**:

1. **Methodology docs (May 15 PM)** — `MULTI_AGENT_INTEGRATION_GUIDE.md` + `HOW_TO_USE_MULTI_AGENT.md` referenced `services/orchestration/engine.py` after #1094 deleted it. A new agent following the guide verbatim would `from services.orchestration.engine import OrchestrationEngine` and hit ImportError. Fix: deprecation banner. (Commit `19b33a89`.)

2. **Repository docstring (May 16 AM)** — `services/database/repositories.py:2335-2337` `StandupConversationRepository.add()` docstring asserted *"Caller owns the transaction. For per-call sessions opened in StandupConversationManager, AsyncSessionFactory.session_scope() handles commit."* But `session_scope()` does NOT commit (it's session-lifecycle-only). The docstring shaped initial mental model on audit; the divergence was the bug surface for #1079. (Fix commit `b5d7972d`.)

3. **Templated user-facing copy (May 16 PM)** — Hard-coded canned responses asserted product behavior the code didn't honor. "Please run the setup wizard" (no setup wizard exists; fixed in #1065). "All open PRs are less than 7 days old" (handler only checked 100 most recent items; reframed via #1064 → #1096 first slice, commit `289d57ca`).

4. **`require_request_context` orphan dependency (May 16 PM)** — `services/auth/auth_middleware.py:395` defined a FastAPI dependency `require_request_context` with a docstring advertising the pattern `ctx: RequestContext = Depends(require_request_context)`. Zero production callers. Discovered by Architect during #1015 verification; deleted in #1015 Phase 2 (commit `be9456b2`).

5. **Test fixture vs. classification logic (May 16 PM)** — `tests/orchestration/test_multi_agent_coordinator.py::moderate_intent` fixture's message "Implement new API endpoint with validation and tests" triggered multiple domain expansions (`testing` via "validation"/"tests", `integration` via "api") which combined with EXECUTION-category default landed at COMPLEX classification → 4 subtasks; test asserted MODERATE → 2-3 subtasks. The fixture name + test name asserted "moderate" but the actual fixture exercised COMPLEX. (Fix commit `09076ada`.)

6. **Incomplete pattern translation (May 16 PM)** — #1038 issue body recommended applying the `.with_variant(JSON, "sqlite")` pattern from `InsightDB` to fix SQLite test compat for `EthicsAuditLogDB`. Body asserted the InsightDB pattern was a complete fix. But `InsightDB.user_id` was `String`, not `UUID` — so the `with_variant` alone was complete for `InsightDB` but incomplete for `EthicsAuditLogDB`'s UUID column (Python UUID objects can't bind to SQLite). The body's assertion ("apply same pattern") didn't account for the column-type difference. (Fix commit `6f429c85`.)

7. **Inbox MANIFEST as derived index (May 17 AM)** — `mailboxes/lead/inbox/MANIFEST.md` asserted state `_(empty)_` while the inbox directory held 12 memos. Cross-fanout fanout creates duplicate inbox copies; each agent only updates manifests they own; recipient inbox MANIFESTs only sync on recipient triage. **First instance at the derived-index layer** — generalizing the pattern beyond docs/docstrings/dependencies to "derived artifacts that lag a source-of-truth substrate without enforcement." Triaged + filed via `6c5f11e1` (memo) + `ff403315` (CIO Option A disposition). CIO methodology cosign on the layer generalization.

A meta-eighth instance arrived during Pattern-073 authoring: a merge-commit body for #1096 slice 1 contained the line "Fixed:" as a section header, which GitHub's close-parser interpreted as `Fixed: #1096` and auto-closed the issue despite the prose explicitly saying "Does NOT close #1096." Verb-form drift in a commit message asserting closure that wasn't intended.

9. **`_fallback_classify` production-orphan (May 30, 2026; post-promotion confirming instance)** — `services/intent_service/classifier.py:934` defines `_fallback_classify` with a method name + docstring asserting "fallback classification." Production reality: 0 production callers; 8+ test callers in `tests/unit/services/test_intent_search_patterns.py` + 2 archive callers. The production fallback path is `LowConfidenceIntentError → middleware → floor` per ADR-060/061. **Same code-surface production-orphan shape as instance #4 (`require_request_context`).** Surfaced by Architect's #1016 (B) option close-after-fresh-verification this afternoon — methodology-30 (Consumer-Trace) caught the assertion (method-name advertising "fallback") vs. reality (no production caller). Outside the original promotion window (May 15–20) — captured as ongoing-recurrence evidence: three production-orphan instances within ~2 weeks (May 16 `require_request_context`, May 30 `_fallback_classify`, plus May 15 methodology-core engine drift in the catalog #1 row) confirms the production-orphan sub-shape is recurring, not a one-off. CIO disposition 2026-05-30: filed (Arch's weak preference; CIO concurs the recurring shape warrants catalog capture).

### The recurring shape across all instances

A **narrative artifact** (prose, docstring, comment, issue body, test fixture name+content, user-facing copy, commit message) **asserts a contract or describes a behavior**. The **code, system state, or current product behavior diverges** from that assertion. The assertion is structurally well-formed (no syntax error, no missing reference) but semantically wrong (the assertion's predicate doesn't match the system's actual behavior).

The asymmetry that makes this load-bearing:

- **The artifact's assertions are CHEAP TO WRITE.** Add a docstring, file an issue body, write a test fixture — minutes of effort.
- **The artifact's CORRECTNESS is EXPENSIVE TO VERIFY.** Reading the docstring + tracing the code path it describes + confirming the assertion still holds — typically tens of minutes per assertion.
- **The READER who trusts the artifact pays the verification cost.** The cost is paid by EVERY future reader. The original author may have written it correctly at the time, or may have written it aspirationally. Either way, the cost asymmetry compounds: every drift accumulates a hidden tax on every subsequent reader.

Without a recognition discipline, the failure mode is invisible until acted on. Compare with Pattern-064 ("alive scaffolding that does the opposite"): code-Pattern-064 fails at runtime (eventually visible to users); doc-073 fails at *next reader's audit*, often after the reader has already made a decision based on the drifted assertion. Pattern-073 is darker because the failure surface is one layer removed from runtime — the system doesn't break, the reader's mental model does.

## Problem

### The failure mode

```
Narrative artifact A asserts: "X behaves as Y"
   → Reader trusts A's assertion + makes decision D based on Y
   → Code C (the subject of A's assertion) behaves as Z (≠ Y)
   → Decision D is wrong; failure surfaces at D's downstream consequence
   → Diagnosis requires reading A AND tracing C AND noticing the Y≠Z gap

In contrast, Pattern-064 (Alive Scaffolding) fails at runtime:
   → Code C looks live but does nothing
   → Stress-test exercises C
   → C's no-op behavior surfaces immediately
```

### Why the verb tense + quantifier matters

Across all six reference instances, the drift was concentrated in **assertions that named a specific code surface or behavior in present tense** ("session_scope() handles commit"; "All open PRs are less than 7 days old"; "request.state.user_id is read by all routes"). Past-tense narration ("session_scope() handled commit until #1079"; "All open PRs were less than 7 days old in the 100-item scan") would have been correct in many of these cases. The pattern's recognition cue is therefore tied to verb form: **present-tense assertion about a specific code surface or behavior, made by a narrative artifact that's not auto-generated from the code itself**.

### Where this *will* surface

Five narrative-artifact layers in PM's codebase are most prone:

1. **Code docstrings** that name specific dependencies, contracts, or downstream behaviors
2. **Architecture / methodology docs** that name specific code surfaces (file paths, class names, function names)
3. **Issue bodies** that describe current state ("All other route handlers extract user_id from `request.state.user_id`")
4. **Test fixture names + messages** that assert categorical state (`moderate_intent` with content that triggers COMPLEX)
5. **User-facing canned response copy** that asserts product behavior ("Please run the setup wizard")

A sixth layer worth watching: **commit messages** with close-magic-strings or assertions about subsequent state. The auto-close meta-instance above shows GitHub's parser as an enforcement layer for assertions about what a commit "does."

### The Pattern-064 sibling relationship

**Pattern-064 (Alive Scaffolding) and Pattern-073 share a structural shape** but differ in failure surface and stress-test path. Both name *infrastructure that looks present but doesn't match its apparent contract*:

- **Pattern-064**: code that looks live but does nothing or does the opposite. Stress-test: users exercise the code; runtime errors / wrong outputs eventually surface.
- **Pattern-073**: narrative artifact about code that asserts a contract the code doesn't honor. Stress-test: *next reader trusts the artifact, makes a decision*. The "users" of Pattern-073 are readers, not runtime execution paths.

Where Pattern-064 governs the code's truth-telling, Pattern-073 governs the project's narrative truth-telling. A codebase can pass all Pattern-064 audits and still have widespread Pattern-073 drift — and vice versa.

## Solution

### Recognition trigger

A narrative artifact hits the drift threshold when:

1. **It makes a present-tense assertion about a specific code surface or behavior** (named file, function, class, contract, quantifier-bounded claim), AND
2. **The asserted behavior cannot be confirmed by direct reading of the named surface** — requires a verification step (run the test, trace the call chain, query the database state, check the API result).

A non-trivial subset of narrative artifacts will satisfy condition (1) — that's normal and load-bearing. The recognition trigger fires when condition (2) is *not routinely satisfied* by the artifact's authoring process. I.e., the author wrote the assertion without verifying it (or verifying it once but not re-verifying as the code evolved).

### Discipline (apply continuously)

1. **Verb-tense discipline at authoring time.** When writing a narrative assertion about a specific code surface, prefer past-tense or scope-bounded present-tense:
   - ❌ "X handles commit" (universal, unverified-at-read-time)
   - ✅ "X handled commit until #N" (past-tense narration; correct + ages well)
   - ✅ "X is intended to handle commit; verify before relying on it" (present-tense + verification disclaimer)
   - ✅ "Tested 2026-05-16: X commits on success in the SQLite + Postgres dialects checked" (scope-bounded assertion)

2. **Doc-sync-sweep skill at change boundaries.** After substantive code-shipping commits, run `.claude/skills/doc-sync-sweep/SKILL.md`: identify likely-affected narrative surfaces, audit each for drift, fix in place or capture as discovered work. Filed 2026-05-16 as the operational discipline for Pattern-073 instance prevention.

3. **Audit-cascade at multi-phase work transitions.** Pattern-049 (Audit-Cascade) already enforces audit between phases of multi-step work. Add a doc-drift sub-step: at each phase boundary, audit the narrative artifacts that named the previous phase's specific surfaces.

4. **Independent verification at high-stakes decisions.** When a decision will turn on a narrative artifact's assertion (e.g., "this is the canonical pattern; follow it"), the disciplined author runs a grep / test / trace to confirm the assertion still holds. The minute-of-verification eliminates hours of downstream wrong-decision rework. Example: Architect's #1015 ratification verified every load-bearing claim in Lead Dev's Phase 1 design memo before concurring — that audit found the third reference instance (orphan `require_request_context`).

5. **Recognize the failure mode in retrospect.** When fixing a bug, ask: *"Did a docstring / comment / issue body / fixture / canned copy shape my initial mental model in a way that turned out to be wrong?"* If yes, the drift IS the bug surface (not just incidental to the code fix). File the instance + verify the rest of the same narrative surface hasn't drifted similarly.

6. **Cite-the-line for spec/design code-state assertions (authoring-time variant, Lead Dev 2026-06-12).** The drift above is mostly *maintenance-time* (a doc was true, then code moved). There's an *authoring-time* sibling: a spec/design/proposal asserts what exists in the codebase **without checking** — and is wrong from the start. Two same-week instances, two authors: PA's MODEL_ALIASES proposal spec'd wiring into `LLMClient.build_request()` (the method doesn't exist; real choke points were 3 other call-sites); CXO's start-screen design asserted `tokens.css` has "no radius scale" (`--border-radius-sm/md/lg` existed and was widely used). Both caught cheaply at build by verify-first, but each cost a correction cycle and erodes spec trust. **Cohort norm (PM concurs): any spec/design/proposal that asserts what exists in the codebase cites the `path:line` it checked** — converting "I believe X exists" into "X at `path:line`" or an explicit "I didn't check." Same family as the verb-tense discipline (#1) but at authoring rather than maintenance time; adjacent to m-42 (reflexive verification — self-exemption from one's own verification rigor) and m-30 (consumer-trace).

## Architectural reasoning

The narrative artifacts in the project are themselves *infrastructure for the team's collective mental model*. They have the same load-bearing property as code: structurally consistent, semantically dispatched-on at decision time, expensive to refactor when wrong.

Pattern-064 names the failure mode where code-infrastructure looks present but does nothing. Pattern-073 names the same failure mode at the narrative-infrastructure layer. The reason the two are siblings rather than the same pattern: the stress-test surface is different (runtime vs. reader), and the recognition discipline is different (testing vs. verb-tense + verification cadence).

Methodology-29 (Pattern Formation via Successful Imitation) predicts that recognition can run ahead of codification when the failure mode is vivid. The 6-instance-in-48-hours cluster on May 15-16 is the textbook signal: the same shape recurred in five different surface layers, recognized by both Lead Dev and Architect independently. Codification (this Pattern entry + the `doc-sync-sweep` skill) closes the recognition-to-discipline gap.

## Forces / when to apply

**Apply Pattern-073's recognition discipline when:**
- Authoring a docstring or comment that names a specific dependency, contract, or behavior of a different module
- Filing or updating an issue body that describes current code state
- Writing a test fixture name + content (especially when the name asserts a category like "moderate")
- Composing user-facing canned copy that asserts product behavior or capability
- Writing a commit message that asserts state about the commit's effect ("Fixed:", "Closes:")
- Verifying load-bearing claims in a memo or ratification document

**Do NOT over-apply when:**
- Writing inline comments that paraphrase the immediately-adjacent code (the verification cost is trivial)
- Writing user-friendly response wording where the underlying scope is uncontroversial ("Here are your todos") — over-hedging becomes its own anti-pattern (asserting nothing is also asserting nothing useful)
- Composing high-altitude vision/strategy prose where the assertions are deliberately aspirational

## Code references (reference instances)

The fourteen instances, with their resolution paths, documented at the file-and-line level. Per CIO methodology disposition (2026-05-17): **the cleanup is removing the misleading surface, not racing to build the asserted behavior**. Pattern-073 catch + cleanup = surface removal; building the asserted behavior is a separate concern that may or may not follow. Instance 11 paradigmatically shows this split.

- **Instance 1 (methodology docs)**: `docs/internal/development/methodology-core/MULTI_AGENT_INTEGRATION_GUIDE.md`, `HOW_TO_USE_MULTI_AGENT.md`. Fixed via commit `19b33a89`.
- **Instance 2 (repository docstring)**: `services/database/repositories.py:2335-2337`. Fixed via commit `b5d7972d` (#1079 includes switching `_session_scope` from `session_scope` to `transaction_scope`).
- **Instance 3 (templated user-facing copy)**: `services/intent/intent_service.py:3040-3041` (Q42 stale PRs). Fixed via commit `289d57ca` (#1096 slice 1).
- **Instance 4 (orphan dependency)**: `services/auth/auth_middleware.py:395-444`. Fixed via commit `be9456b2` (#1015 Phase 2 + Architect's Option 1 disposition).
- **Instance 5 (test fixture vs. classification)**: `tests/orchestration/test_multi_agent_coordinator.py:50-58`. Fixed via commit `09076ada` (#1026).
- **Instance 6 (incomplete pattern translation)**: #1038 issue body's recommendation to apply `InsightDB.with_variant` to `EthicsAuditLogDB`'s UUID column. Fixed via commit `6f429c85` (CrossDialectUUID TypeDecorator addresses the UUID-binding case the body's recommendation didn't cover).
- **Instance 7 (derived index lag)**: `mailboxes/lead/inbox/MANIFEST.md` asserted `_(empty)_` while directory held 12 memos. Disposition Option A — codify "directory is truth, MANIFEST is index; autonomous loops poll `ls inbox/` not MANIFEST" — ratified by CIO at commit `24cd6a36`; codification ask routed to Docs (tracker 12z). Triage commit `01c83231`.
- **Instance 8 (data substitution)**: `services/intent/intent_service.py:2212` `_handle_projects_query` returned a hardcoded list of three fake projects (Piper Morgan Platform, Issue Tracker Integration, Documentation Updates) regardless of which user asked. The handler asserted "I'm tracking these projects for you" via the consciousness wrapper — the system has a real `ProjectRepository` + `PortfolioService.list_active_projects` but the handler bypassed them with fake data. **First instance at the data-substitution layer** — generalizing the pattern catch-net to "narrative-about-data-that-doesn't-exist." Fixed via #1102; replaced hardcoded list with real `PortfolioService.list_active_projects(user_id=user_id)` mirroring `canonical_handlers.py:3972`; honest fallback when `user_id` is missing. Pattern-072 overlay also present (parallel implementation: canonical_handlers.py PORTFOLIO category had the real path all along).
- **Instances 9 + 10 (API-response universal claims)**: `services/api/transparency.py:189-193` (`AuditSummaryResponse.summary`) returned `audit_completeness: "100%"` (asserts complete enumeration but bounded by `get_user_audit_log(session_id, limit=1000)` upstream — could be silently incomplete for sessions with >1000 entries) and `transparency_level: "Full transparency with privacy protection"` (categorical universal claim that the service can't verify). Surfaced during Surface 7 slice 2 work (#1100); UI applied the discipline by not rendering these fields. Fixed via #1101: dropped both fields from the response; replaced `audit_completeness` with verifiable `entries_examined` + `entries_examined_limit` pair (lets consumer reason about scope). **First instances at the API-response layer** — generalizing further to "structured API response claiming state the upstream can't verify."
- **Instance 11 (placeholder method surface)**: `services/database/repositories.py` previously contained `get_nodes_with_privacy_check` + `create_node_with_privacy_check` placeholder methods (and `KnowledgeGraphService.get_nodes_with_privacy` + `create_node_with_privacy` wrappers) with `# Future:` comments claiming privacy filtering the implementation never provided. **Surface removed** via #1010 (closed 2026-05-14) per the "delete misleading claims rather than partial implementation" discipline. **Real-feature follow-up** tracked at #1089 with Phase 0 design substrate (Architect Q3+Q4 ratified `73cf571b5`; HOST Q2 ratified with `filter_reason` enum refinement). Status: **RESOLVED — misleading surface removed; real implementation tracked at #1089, ship cadence pending PM Q1 disposition**. *This instance paradigmatically shows the resolution-shape split: Pattern-073 cleanup is surface removal, not racing to build the asserted behavior.* (Per CIO methodology disposition `?` 2026-05-17.)
- **Instance 12 (user-facing handler assertion → empty no-op)**: `services/intent/intent_service.py:2785-2791` `_handle_update_document_notion` called `update_page(page_id, properties={})` — empty properties dict, literal no-op — and then asserted *"✓ Updated **{doc_title}** / Added: {update_content}"* to the user. The success message claimed an update that the code didn't perform. **First instance at the user-facing handler layer** (output-rendering boundary where the narrative is the user's response copy, not internal documentation). Fixed via #1080: added `append_blocks` to the Notion MCP adapter + router; handler now builds a paragraph block from `update_content` + calls `append_blocks(page_id, [block])`; honest fallback message on append failure; success message reframed to "✓ Appended to X" matching the actual semantics. *Compound finding*: discovery surfaced during audit-cascade revisit of #1080 when PM's screenshot confirmed the Notion integration token already had write capability — the "PM-manual token-scope gate" framing in the original issue body was itself a Pattern-073-shaped over-assertion; the actual gate was code-side, not auth-side.
- **Instance 13 (issue body asserts verification target for infrastructure that doesn't exist)**: #1081 NOTION-SLACK-XREF issue body framed as *"Verify Slack→Notion cross-references render correctly post-#304 activation"* — presupposing a cross-reference rendering path. Audit-cascade revisit 2026-05-18: `services/integrations/slack/` contained ZERO references to Notion + ZERO URL-extraction / URL-unfurling logic. The asserted verification surface didn't exist anywhere in the codebase. **First instance at the issue-body verification-target layer** (verification-AC asserting infrastructure presupposed to be in place). Resolved via #1081 in the same session: built `services/integrations/slack/notion_url_unfurler.py` (URL pattern + page-ID extraction + Notion-router lookup + Slack-formatted rendering); wired into `webhook_router._process_message_event` to enrich the spatial context; threaded `notion_refs` through `spatial_adapter.get_response_context`; rendered in `response_handler._send_slack_response` via `format_notion_refs_for_slack` (honest per-URL `ok`/`error` shape — failed resolutions surface as "couldn't resolve: <reason>" rather than silently dropping). 19 unit tests cover URL extraction, page-ID parsing, happy path, no-router fallback, per-URL fail-graceful, page-not-found marker, render output, spatial-adapter round-trip. *This instance compounds with #1080's: both #1080 and #1081 body language asserted infrastructure that wasn't in place; both were caught by audit-cascade discipline + built rather than just closed.*

- **Instance 14 (derived-index lag — cohort-wide manifestation)**: cross-mailbox inbox MANIFEST staleness verified during 2026-05-20 recovery from a destructive manifest-sync incident. Concrete evidence: `mailboxes/comms/inbox/` 22 files on disk vs 19 entries in MANIFEST (3-file unlisted gap); `mailboxes/cxo/inbox/` 2 files on disk vs `*Inbox clean as of 2026-05-19 ~07:20*` claim; `mailboxes/ppm/inbox/` 1 file on disk vs 5 entries asserted in MANIFEST. **Second instance at the derived-index layer (after Instance 7)** but at sharper drift threshold per CIO concur (2026-05-20) — the 3-file unlisted gap is a meaningful staleness signal, not just routine cross-fanout lag. Same shape as Instance 7 (MANIFEST asserts inbox contents; disk-state diverges; assertion ages past truth); tighter exemplar because the gap is large enough to be load-bearing for any agent who reads the MANIFEST. Resolution path: **full revert to HEAD** per PM directive 2026-05-20 morning — an in-flight destructive-sync attempt would have lossily rewritten the affected manifests (32 `(no subject)` markers added across 13 files + multiple curated prose sections lost: exec/inbox lost its "Day 12 morning triage" + "Open carrying" narrative; cxo/inbox lost its "Phase 2.2 unblocked" status note; cio/read lost "Acted on:" annotations). Cohort-wide retriage memo filed to Exec + cc cohort (commit `b97130ce9` on origin/main); methodology memo to CIO (commit `2bd7c2994`); tracking issue [#1106](https://github.com/mediajunkie/piper-morgan-product/issues/1106) for non-destructive sync-skill replacement. CIO concur memo: `mailboxes/lead/read/memo-cio-to-lead-cc-pm-pattern-073-instance-14-concur-plus-worktree-proliferation-disposition-2026-05-20.md`. *Note*: the destructive-sync skill behavior itself is a **separate finding** (resolver-causing-data-loss-during-resynchronization shape — different from Pattern-073's assertion-vs-reality drift); CIO disposition routes that to Docs for skill-level fix via [#1106](https://github.com/mediajunkie/piper-morgan-product/issues/1106), not as a Pattern-073 instance.

## Anti-pattern recognition

When a narrative artifact is being read or written, the following surface-cues are signals to invoke Pattern-073's verification discipline:

- **Verb tense**: present-tense assertion about a specific code surface, not auto-generated from that surface
- **Quantifier**: universal claims ("all", "every", "always", "never") about scoped systems
- **Reference resolution**: named file paths, class names, function names, line numbers in the artifact
- **Reader-facing primacy**: the artifact is read more often than the code it describes (e.g., issue bodies read by many planners; user-facing copy read by every user)
- **Aspirational authoring**: the artifact was written when the system was designed-but-not-yet-built, and the system has evolved without the artifact being updated

When ≥2 of these signals are present in an artifact, the verification cost-benefit tips toward running the doc-sync-sweep on adjacent surfaces.

## Relationship to other patterns

- **Pattern-064 (Alive Scaffolding That Does The Opposite)**: structural sibling. Pattern-064 governs code's truth-telling; Pattern-073 governs narrative's truth-telling. The "## Evolution" section convention introduced in Pattern-064 (May 15 by Architect) is itself a doc-sync-sweep discipline applied to its own pattern entry.
- **Pattern-046 (Completion Discipline)**: adjacent failure family. Pattern-046 names "shipped but not finished" at the code/feature layer; Pattern-073 names "shipped but narrative-not-updated" at the narrative layer. The CLAUDE.md `close-issue-properly` skill enforces Pattern-046 at the issue-tracker level; the new `doc-sync-sweep` skill (filed 2026-05-16) enforces Pattern-073 at the broader narrative-artifact level.
- **Pattern-049 (Audit-Cascade)**: discipline anchor. Audit-Cascade enforces audit at phase boundaries of multi-step work; Pattern-073's "discipline at change boundaries" sub-rule rides on the Audit-Cascade infrastructure.
- **Methodology-29 (Pattern Formation via Successful Imitation)**: the framework that produced this filing trigger. Three instances in 48 hours fired the threshold; six by close of filing day.

## Adjacent manifestations

(Per CIO's filing disposition: file under the narrower "Documentation-Asserted-Behavior Drift" title; note the broader framing here. If broader instances accumulate, the title becomes a future evolution-note.)

The narrower title catches narrative artifacts asserting behavior. A broader formulation — **"asserted-but-not-enforced contracts"** — would extend to:

- **Type assertions / type comments** that don't match runtime behavior
- **TODO comments** asserting future behavior the team never executed
- **README claims** about installation, usage, or capability
- **API documentation** about endpoints (when the spec drifts from the implementation)
- **PR descriptions** asserting what the change does (when the diff diverges from the description)
- **Configuration documentation** about environment variables or settings (when the consumer code no longer reads them)

If two more instances of any of these accumulate independently of the canonical narrative-asserted form, the broader framing becomes an Evolution entry on this pattern. Until then, file under the narrower title.

### The unifying insight (CIO disposition 2026-05-17)

Instance 7 (`mailboxes/lead/inbox/MANIFEST.md`) generalized the pattern from "narrative about code" to **derived artifacts that lag a source-of-truth substrate without enforcement**. The unifying lesson across all four observed layers:

- **Documentation describing code**: code is source of truth; docs are derived narrative
- **Docstrings asserting semantics**: implementation is source of truth; docstring is derived assertion
- **Type assertions about runtime**: runtime behavior is source of truth; type signatures are derived guarantees
- **Index over directory state**: directory is source of truth; MANIFEST/listing/cache is derived index

**Derived artifacts lag without enforcement; trust them only with awareness of the lag.** When a derived artifact is the only signal a consumer reads (e.g., an autonomous loop checking "do I have work?" via a manifest count), the lag becomes a correctness bug. Mitigations cluster into three families: enforce sync at write time (hook/CI), poll the source of truth not the derived index, or accept the lag and tell consumers to.

### Spec-layer extension + the early-vs-late defense distinction (Arch finding, CIO note 2026-06-08)

The 14 original instances were all at the **code/runtime layer** (docs/docstrings/types/manifests asserting *code* behavior). Two 2026-06-07 instances surfaced the **same shape at the architecture-*spec* layer** — an ADR/spec asserting behavior that the live action-set doesn't honor:
1. **ADR-060 amendment** asserted "Phase 3 formalizes the existing floor-default at the verb layer" — assumed the verb vocab covered the live action set; it didn't (40+ category-routed actions outside the vocab).
2. **ADR-060 amendment** asserted `source_type` lives in `intent.slots` — assumed a slot-unification (#1121) had landed; it hadn't (the working precedent reads `intent.context`).

Both are P-073 at spec altitude: a *spec* asserts behavior; *practice* diverges; drift accumulates until a consumer-trace surfaces it. The useful refinement this adds is a **defense-timing distinction**:
- **Early defense (pre-implementation)** — **methodology-30 consumer-trace applied *before* building**, against the spec's claim. Catches the spec-vs-reality drift at design time (both 6/7 instances were caught this way — Lead Dev's pre-implementation trace + audit-cascade). *Prevents* the drift from reaching code.
- **Late defense (post-implementation)** — the **`doc-sync-sweep`** skill, run *after* code ships, catching narrative that has already drifted from shipped code. *Surfaces* drift that already landed.

So P-073's recognition discipline now spans two altitudes (code-layer + spec-layer) and two defense-timings (early/pre-impl via m-30; late/post-impl via doc-sync-sweep). (This does not change Proven status — it's a layer/timing note on the existing Proven pattern, per Arch's 2026-06-08 Day-5 finding F2; CIO catalog action.)

## Promotion criteria (historical — pattern promoted 2026-05-18)

When this pattern was filed Emerging (May 16), promotion to Proven required:

1. **One more independent instance within 14 days** (by 2026-05-30) — not from a related investigation; surfaced by a different agent or a different surface layer than the six May 15-16 instances.
2. **The `doc-sync-sweep` v0.1 skill operates cleanly on a fresh-fix flow** — applied by an agent who didn't draft the skill, surfacing a real drift instance that's then fixed via the documented procedure.

**Promoted 2026-05-18** (CIO catalog-management authority): Criterion 1 was comfortably exceeded — seven additional instances (instances 7-13) across five new surface layers landed during the May 16-18 window, surfaced by Lead Dev + CIO (manifest-sync) + Architect (Q3+Q4 ratification on Instance 11). Cross-agent engagement (5 distinct roles: Lead Dev / CIO / Architect / HOST / PM) validated the recognition discipline empirically. Criterion 2 (literal `doc-sync-sweep` skill v1.0 cross-agent application) was not literally satisfied; CIO disposition was that methodology-29's substantive evidence bar — *independent recognition of the same pattern-shape, without enforcement, with carried recognition discipline* — was decisively met on the empirical signal, making the literal skill-cross-agent criterion an in-flight refinement rather than a Proven-gating requirement.

Operational follow-up (not gating; on the now-Proven pattern):
- `doc-sync-sweep` skill v0.1 → v1.0 + cross-agent application
- methodology-29 cross-reference update naming Pattern-073 as a reference case for the framework's "what it predicts" section (CIO drafting per ratification memo)

## Cross-references

- CIO disposition memo (2026-05-16): `mailboxes/lead/read/memo-cio-to-lead-arch-cc-ceo-pattern-073-disposition-2026-05-16.md`
- CIO Saturday-AM bundled acks where 12w sub-pattern decision was first staged: `mailboxes/lead/read/memo-cio-to-arch-lead-cc-cxo-ceo-saturday-morning-bundled-acks-2026-05-16.md`
- Lead Dev 12w memo (edit-in-place fold of three instances): `mailboxes/lead/sent/memo-lead-to-cio-cc-arch-ceo-12w-second-instance-living-docs-describing-dead-code-2026-05-16.md`
- Lead Dev Pattern-073 authoring ack: `mailboxes/lead/sent/memo-lead-to-cio-cc-arch-ceo-pattern-073-authoring-ack-2026-05-16.md`
- `doc-sync-sweep` v0.1 skill (operational discipline): `.claude/skills/doc-sync-sweep/SKILL.md`
- Pattern-064 (sibling): `docs/internal/architecture/current/patterns/pattern-064-alive-scaffolding-that-does-the-opposite.md`
- methodology-29 Pattern Formation via Successful Imitation (promotion-rationale framework): `docs/internal/development/methodology-core/methodology-29-PATTERN-FORMATION-VIA-SUCCESSFUL-IMITATION.md` — Pattern-073 is named in §"What it predicts" as the May 16-18 reference case validating all four predicted signals.
- Pattern-046 (adjacent family): `docs/internal/architecture/current/patterns/pattern-046-completion-discipline.md`
- Methodology-29 (Pattern Formation via Successful Imitation): see methodology-core catalog
- #1015 (Phase 2 closed 2026-05-16) — Instance 4 reference + verification example
- #1064 (closed 2026-05-16) — investigation that surfaced Instance 3 + audit framing
- #1079 (closed 2026-05-16) — Instance 2 reference + fix path
- #1094 (closed 2026-05-15) — Instance 1 reference (engine deletion triggered the methodology-core doc drift)

— Lead Developer, 2026-05-16 (draft); CIO methodology cosign pending review
