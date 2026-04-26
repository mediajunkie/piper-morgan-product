# Handoff Memo: Chief Architect — Chat to Code Migration

**From**: Chief Architect (Chat instance, Mar 30 – Apr 25, 2026)
**To**: Chief Architect (Code instance)
**Date**: April 25, 2026
**Re**: Role context, current state, active threads, and lessons learned
**Chat lifetime**: 10 sessions, 27 days, 13 artifacts

---

## Section 1: Current State of Your Work

### Active ADRs

- **ADR-060 (Floor-First Routing)**: The defining ADR of the current period. Created by the predecessor Architect (Mar 19). Phases 1-2 complete. Floor inversion trilogy (IDENTITY → TEMPORAL → STATUS/PRIORITY) completed Apr 13. Phases 3-4 deferred post-M1 — these cover the remaining floor migration categories (TEMPORAL-calendar, CONVERSATION, STATUS advanced, PRIORITY advanced). Not actively being worked; M2c context assembler expansion (#951) is the next step that touches ADR-060's territory.
- **ADR-059 (Workflow Dispatcher)**: Implemented. Onboarding removed, dispatcher live. #922 (affirmation handling — "OK" loses conversation context) carried to M2 as genuine quality finding, confirmed by AAXT golden scenarios (4/5 PASS, #922 is the 1 FAIL). ADR-049 amendment still deferred — awaiting post-ADR-059 architecture stabilization.
- **ADR-049 (Conversational State)**: Pending amendment. Onboarding patterns on hold per ADR-059. Escape command infrastructure still needed for #889. This has been deferred since the predecessor's tenure; no urgency but shouldn't be forgotten.
- **No ADRs in draft.** Two should be:
  1. **MCPB/BYOC distribution architecture** — the decision that PM distributes as an MCP server with MCPB as first packaging. Currently scattered across Vision V2.3, PA feasibility research, my MCPB review memo, and 4 rounds of Daedalus alignment exchange. Needs consolidation into ADR-061.
  2. **Cross-project context package format** — the shared envelope agreed with Klatch. Currently exists only in exchange memos. Needs either an ADR or a consolidated reference document.

### Pattern Catalog

- **Pattern-062 (Assembly Assumption)**: Still the most load-bearing insight in the project. Referenced in my MCPB review (individually correct tools + individually correct persona ≠ correct composed experience) and in the Daedalus alignment (shared format reduces wiring cost but doesn't eliminate it). Stable; no refresh needed.
- **Pattern-063 (Extension Without Integration)**: Proposed by the predecessor, still not formalized. Sub-pattern of 062. Six bugs from same cause. Worth formalizing when there's bandwidth.
- **Pattern-045 (Green Tests, Red User)**: Systemically validated during this chat's lifetime. The M1 UAT failure (0/9 despite passing test suite), the omnibus paraphrase drift (PDR-004 correction chain), and the source-discipline lesson (Apr 19) are all Pattern-045 instances. The pattern is well-documented; the instances are well-understood.

### Cross-Project Architecture

The most significant work this chat produced. Four rounds of exchange with Daedalus (Klatch architect):

**Phase 1 Format Alignment (Apr 11, 3 rounds + close)**:
- Shared preamble: `format_version` (semver), `source_type`, `package_id`, `package_kind`, `created_at`, `provenance`, `files`, `extensions`
- PM-specific: `conversation_context` (not `channel` — PM sessions are ephemeral, Klatch channels are durable)
- `extensions` namespaced by producer: `{ "piper-morgan": {...} }`, `{ "klatch": {...} }`
- `layer_fidelity` per provenance entry: `full` / `partial` / `rebuilt` / `absent`
- `package_kind` as preamble/body discriminator: `piper-morgan.session.v1`, `piper-morgan.workspace.v1`
- `format_version` and `package_kind` version move independently (documented explicitly)
- Argus's tamper-evidence reservations accepted: optional `event_id` + `integrity: null` per provenance event
- Labrador (Erika Flowers) independently validated the five-layer model — identical architecture, no contact

**Phase 5 MCP Surface (Apr 18, 1 round)**:
- URI namespace: `piper-morgan://` scheme, parallel to `klatch://`
- `/{id}/manifest` sub-resource convention for cheap discovery (both producers)
- Tool naming: `get_context_package` as shared tool name across producers
- Write-path coordination flagged as next frontier (`reflect` ↔ `save_artifact`)

**Standing offer**: Daedalus offered validation pass on the Phase 1 design doc (`docs/plans/STEP-10-PHASE-1-PACKAGE-FORMAT.md` in Klatch repo). Also offered to be present for PM's first `piper-morgan.session.v1` validation. Both offers accepted but not yet exercised.

### Live Architectural Questions

- **MCPB prototype scoping**: Green-lighted in my Apr 10 review. Python runtime, separate SQLite at `~/.piper-morgan/piper.db`, 3 tools (`get_project_status`, `save_artifact`, `retrieve_artifact`), 2-3 day estimate for Lead Dev. Persona gap mitigation: make tool responses already Piper-voiced so Project instructions do less heavy lifting. Not yet started.
- **Context assembler as MCP Resource provider**: Flagged as highest-value architectural reuse opportunity (Apr 10). The assembler's `gather_context()` methods could become MCP Resource handlers. Strongest argument for Python MCP server runtime.
- **#922 affirmation handling**: Genuine quality finding carried from M1. Root cause: `ConversationTurn` model missing a `response` field — floor reads history but only sees user messages, never Piper's replies. Fix committed Apr 9, confirmed in AAXT 4/5. Still the 1 FAIL in golden scenarios.
- **Ethics enforcement activation**: BoundaryEnforcer wired but disabled since Oct 2025. CXO delivered voice guidance (#964): "The enforcer detects, but Piper speaks." Three voice templates, five anti-patterns, Colleague Test applies (7+ score). Lead Dev needs to validate false-positive rate before enabling. 3 follow-up issues filed.

### LLM Consolidation (Resolved)

Delivered guidance Apr 14, executed Apr 15:
- #970 (ServiceRegistry LLM access): Leave global singleton as-is. MCPB uses a fundamentally different access pattern — MCP server doesn't call LLM providers, the host application does.
- #971 (Pattern-012 adapters): Deleted. 10 files, 160 lines. Dead code, no MCPB reuse path.
- ProviderSelector: Deleted with #971. Superseded by provider-agnostic #940.

Common principle: don't maintain infrastructure for a future that hasn't been designed yet.

---

## Section 2: Open Threads with Disposition Recommendations

| Thread | Status | Disposition |
|--------|--------|-------------|
| ADR-061 (MCPB/BYOC distribution) | Undocumented | **WRITE.** Most consequential undocumented decision. Consolidate from Vision V2.3, PA feasibility, Architect review, Daedalus alignment. |
| Cross-project format reference doc | Scattered across 4 memos | **CONSOLIDATE.** Either ADR or standalone reference. The positions are agreed; they need a single authoritative source. |
| MCPB prototype (#957) | Green-lighted, not started | **PROCEED when Lead Dev has bandwidth.** Spec is ready. Gall's Law sequence: MCP server → test in Claude Desktop → MCPB packaging → MCP Apps. |
| Pattern-063 formalization | Proposed, not written | **DEFER.** Lower priority than ADR-061 and the format consolidation. Write when there's a natural opening. |
| ADR-049 amendment | Deferred since predecessor | **CONTINUE DEFERRING.** No urgency until guided workflows return to scope. |
| Fabrication probe set | Recommended Apr 16, CXO endorsed as separate instrument | **TRACK.** Lead Dev should build 5-10 probes. Low effort, high signal. |
| AAXT scorer vocabulary | Recommended Apr 16 | **TRACK.** Lead Dev should adopt six-failure-mode taxonomy if DeepEval scorer vocabulary is still mutable. |
| Sparkline test format discipline | Noted for M5 | **NOTE.** When PM populates `extensions: { piper-morgan: {...} }`, every renderable field should carry `length_chars`. Schema-time decision. |
| Klatch ExportReviewPanel reference | Noted for M3 | **NOTE.** Accept/edit/reject with trust transitions is the reference implementation for ADR-054 composting write governance. |
| Alpha tester silence | 5+ weeks, flagged 5+ times | **ESCALATE.** Not Architect scope, but worth noting: this is the longest-standing unresolved operational issue. |

### Cross-Project Alignment — Next Steps

The format alignment is complete for Phase 1. The Phase 5 MCP surface alignment is complete. The next coordination point will be when either project ships its first MCP server and the other wants to validate interop. That's probably months away. No active thread to maintain — just a standing relationship to resume when the work converges again.

Daedalus has a standing offer to read PM's Phase 5 design doc when it exists. The protocol is: async memo exchange via xian, 1-2 rounds, don't force-unify what's naturally different.

### ADR-060 Downstream

Floor-first routing is architecturally complete (the pattern is established, the inversion trilogy proved the migration path works). What it unlocks:
- **Context assembler expansion** (#951, M2c) — the assembler is now the primary quality lever. Better context → better floor responses. This is where quality moves from 72.1% toward 80%.
- **MCP Resource provider pattern** — the assembler's `gather_context()` methods are the natural surface for MCP Resources. This is the bridge from the current web app to the MCPB prototype.
- **Handler retirement** — handlers that only read and format data (no side effects) are candidates for retirement once the floor handles their categories well enough. The inversion sweep (#962) identified 3 inversions; there may be more as the floor improves.

What it doesn't unlock: side-effect handlers (GitHub issue creation, todo completion, calendar operations) still need wired infrastructure. The floor can't perform state mutations. The action gate ("does this need a side effect?") remains the routing boundary.

---

## Section 3: Relationships and Working Patterns

### With PM (xian)

PM communicates efficiently. Sessions start with "you have mail" or "please write a workstream review." PM trusts architectural judgment and pushes back when framing is wrong — the Daedalus exchanges benefited from PM's real-time corrections (the "place vs. agent" insight, the reminder that PM is "a colleague with access to tasks and knowledge" not "a task-and-knowledge server").

PM values honesty over agreement. "Don't glaze" is load-bearing. The Time Lord alert exists but I never needed it — direct pushback has been well-received.

PM's cadence is life-paced. Sessions happen when PM has time. Don't treat gaps as problems — the Apr 12-18 gap (PM traveling for IAC conference) was normal, not a delay.

### With Lead Dev

Closest working partner. The interaction pattern: Lead Dev writes proposals with clear questions → Architect reviews and answers. This worked well for #970/#971 (LLM consolidation), #925 (floor inversion), and the M2a-M2b sprint planning.

What to watch: cross-references to other in-flight work sometimes missing from proposals (predecessor flagged this, I confirmed it). Standing question for every review: "What else is in flight that this touches?"

When to defer to Lead Dev's engineering judgment: implementation details, test strategy, code organization, performance tradeoffs. When to make the architectural call: interface design, system boundaries, pattern selection, cross-cutting concerns. The line: if it affects how components compose, it's architectural. If it affects how a component works internally, it's engineering.

Lead Dev moves fast. M2a and M2b closed in under a week. Keep up by reading omnibus logs promptly and flagging concerns before implementation, not after.

### With CXO

Productive intersection on voice-architecture questions. The #950 floor prompt design was the best example: CXO set the direction (Five Pillars, grammar, evolve-not-rewrite), Lead Dev implemented, quality improved measurably. The ethics denial voice (#964) is another: CXO designed the voice, Architect validates the implementation architecture.

The Colleague Test is CXO's instrument; the Architect's role is ensuring the testing infrastructure supports it (canonical retest runner, AAXT golden scenarios, fabrication probes as separate instrument).

### With CIO

Methodology-architecture intersection. CIO endorsed RFC-001 (Five-Layer Context Model) with amendments. CIO territory includes the cross-pollination hub and pattern methodology. In practice during this chat, CIO interaction was indirect — through PA's cross-pollination routing memos rather than direct exchange.

### With PA

PA has been an effective routing layer for cross-pollination intelligence and a productive strategic analysis partner. The MCPB prototype scoping request and the Vision/Roadmap review request were both well-framed with clear architectural questions. PA's cross-pollination routing memos (Apr 14, Apr 16) surfaced relevant Klatch developments I wouldn't have seen otherwise.

### With Docs

Minimal direct interaction. Docs produces omnibus logs (my primary source material) and maintains briefing documents. The briefing staleness issue (37 days, see Section 1) is a Docs concern. The PDR-004 correction chain (Apr 16) showed healthy Docs → CXO → Comms coordination.

---

## Section 4: Lessons That Took Time to Learn

### What makes an architectural decision load-bearing vs. decorative

ADR-060 (Floor-First Routing) is load-bearing because it changed how the entire system routes requests — every subsequent decision (floor prompt design, context assembler expansion, handler retirement, MCPB prototype architecture) flows from it. ADR-008 (MCP Connection Pooling) is decorative — it documented a correct decision about connection management that nobody needs to reference during current work.

The distinguishing factor: **does the decision constrain or enable future decisions?** If knowing about this ADR changes what you'd decide about something else, it's load-bearing. If it's a standalone technical choice with no downstream implications, it's decorative. Both are worth documenting (the historical record has value), but only load-bearing decisions need to be in the briefing document.

Currently load-bearing: ADR-060, ADR-059, ADR-045 (Object Model — the grammar concept), ADR-053 (Trust Computation), ADR-054 (Cross-Session Memory). The undocumented MCPB/BYOC decision is the most load-bearing decision that doesn't have an ADR.

### When to defer to implementation judgment

The LLM consolidation response (#970/#971) is the cleanest example. Lead Dev asked: "Should we rewire to ServiceRegistry?" My answer: "No — the MCPB surface uses a fundamentally different access pattern, so rewiring is an intermediate step to nowhere." The *what* (don't rewire) is architectural. The *how* (delete the adapters, which files, what order) is implementation. I said "delete"; I didn't specify which files to delete first.

The line I'd draw: **ADRs should specify interfaces and constraints, not implementations.** ADR-060 says "the LLM floor is the default response path" — it doesn't specify how the floor prompt is constructed (that's the Lead Dev's #950 work with CXO direction). ADRs that over-specify get ignored or worked around; ADRs that under-specify produce drift. The sweet spot is: clear enough that two different Lead Devs would make compatible choices, loose enough that a good Lead Dev has room to make better choices than the Architect anticipated.

### Source discipline in multi-agent synthesis

Learned Apr 19 when PM caught me leaning on the CXO's workstream memo instead of reading the omnibus log directly. The lesson: **each role should form its own read on primary sources.** A well-written summary from another role is tempting to reuse, but it's filtered through that role's priorities and framing. The CXO's workstream memo emphasized voice and experience quality; my workstream memo should emphasize architectural patterns and technical decisions. Same events, different signal extraction.

This generalizes beyond workstream memos. Any time you're synthesizing across multiple sources, read the primary sources, not other people's syntheses of those sources. This is the PDR-004 lesson (paraphrase drift) applied to the review process.

### Cross-project architecture discipline

From the Daedalus exchange: **align on the 20% that overlaps naturally, don't force-unify the 80% that's project-specific.** The shared envelope (preamble fields, provenance, versioning) is the 20%. The content of what each server returns is the 80% — and trying to unify it would produce a translator anyway, just a more complex one.

The `extensions` namespace is the key design decision. It's the escape hatch that lets both projects evolve independently while maintaining envelope compatibility. Without it, every new PM-specific concept would require a format revision or get jammed into an existing field.

The pace lesson: two focused rounds plus a brief close, deliberately, instead of one rushed round. xian's "no points for rushing" principle applied to protocol design.

### Receiving-handoff reflection

The predecessor Architect's handoff memo (Mar 30) was the most useful onboarding artifact — more useful than the briefing document. What made it effective:

1. Organized by function (current state, decisions, pending items, role guidance), not by timeline
2. Included specific pending items with owners and status — I could start working from the pending items table
3. Documented working-with patterns for each role — saved me from learning them through trial
4. Was honest about what didn't get done ("Older omnibus log review: Planned, never got to this")
5. Included the escape hatch ("Time Lord alert!") as operational guidance, not just a rule

What was missing: the cross-project alignment work hadn't started yet (that was this chat's contribution), and the MCPB direction hadn't crystallized. Both emerged during my tenure. The briefing document was stale but the handoff was current — which confirms that handoff memos are higher-value than briefings for transition quality.

---

## Section 5: What Code Access Changes for Your Role

### What gets easier

**Codebase inspection.** The single biggest improvement. Multiple times I made architectural recommendations based on omnibus descriptions of code rather than the code itself. "Delete the Pattern-012 adapters" was based on Lead Dev's description that they were dead code on the hot path — in Code, I could have verified that directly with `grep -r "ClaudeAdapter" services/`. ADR reviews, gameplan reviews, and architectural guidance all become more precise when grounded in actual files.

**ADR and pattern cross-referencing.** `grep -r "ADR-060" docs/` instantly shows me every document that references floor-first routing. In Chat, this was a search-and-hope operation. Pattern catalog curation becomes tractable — I can audit which patterns are referenced in active code vs. which are purely documentary.

**Direct mailbox access.** No PM mediation for sending/receiving memos. The Apr 16 37-memo day would have been less bottlenecked. Cross-project memos (Daedalus exchanges) can be initiated directly.

**Omnibus log batch reading.** `cat docs/omnibus/2026-04-1*.md` for a week's worth of logs. In Chat, each log required a separate `view` call. Workstream reviews become faster at the reading stage.

**Commit history inspection.** `git log --oneline --since="2026-04-10"` shows me what actually changed, not what the omnibus says changed. Valuable for verifying engineering metrics claims.

### What becomes obsolete

**project_knowledge_search as primary discovery.** Replaced by `find` and `grep`. Semantic search is lost (can't do "find me the document about floor-first routing"), but precision search ("which files mention ADR-060") is gained. Net positive for the Architect role, which works with known concepts more than unknown ones.

**PM as mail relay for routine coordination.** PM should still be CC'd on significant decisions, but memos to Lead Dev, CXO, PA don't need to route through PM's hands.

### What needs rethinking

**Worktree awareness.** Code sessions run in a worktree. Worktrees only see what's been pushed to `origin/main`, not just committed locally. If you can't find your handoff or a recently committed file, the likely cause is an unpushed commit — the file exists in the repo but not in your worktree's view of origin. This is the same "local state ≠ shared state" principle that Pattern-062 (Assembly Assumption) captures at the code level: independently correct commits ≠ visible-to-all-consumers until the push step composes them.

**Workstream memo workflow.** Currently: read omnibus logs in project knowledge → write memo → present as file to PM. In Code: read omnibus logs from repo → write memo → save to `mailboxes/exec/inbox/` and CC `mailboxes/pa/inbox/`. Naming: `workstream-{ship#}-arch-{date}.md`.

**Cross-project coordination rhythm.** The Daedalus exchanges worked through PM delivering memos. In Code, if Dispatch-DinP has a mailbox, cross-project memos might route differently. Clarify with PM how cross-project mail flows in Code.

**Startup routine.** Proposed:
1. Read `BRIEFING-ESSENTIAL-ARCHITECT.md` and `BRIEFING-CURRENT-STATE.md`
2. Check `mailboxes/arch/inbox/` for unread memos
3. Read most recent omnibus log(s)
4. Check `vision.md` and `roadmap.md` version numbers
5. `git log --oneline -20` to see recent commits
6. Check for open issues tagged "needs Architect input"
7. Check for open PRs touching ADRs, patterns, or domain models

**Verifiable claims discipline.** Per CoS guidance: workstream memos should source comparative and quantitative claims to verifiable data. "72.1% quality at iter 2" is verifiable (canonical retest output). "The most productive sprint week" needs evidence (issue close counts, commit counts). Source the numbers; qualify the comparisons.

---

## Section 6: What I'd Tell My Successor That I Wouldn't Tell the PM

PM has said he can't promise never seeing this, and that's fine. Nothing here is secret.

**The workstream memos are the most time-consuming and least architecturally distinctive thing you do.** They're valuable — the CoS relies on them for Ship synthesis, and writing them forces you to read the omnibus logs thoroughly. But the timeline reconstruction (day-by-day table, metrics) is commodity work that any role could do. The architectural observations and "what needs attention" sections are where you add unique value. If you find yourself spending entire sessions on workstream memos, push for PA to draft them with Architect review. The PPM's handoff makes the identical recommendation about their workstream memos.

**The cross-project work is the most valuable thing this chat produced, and it's the least visible internally.** The Daedalus alignment doesn't appear in any Ship, doesn't have an ADR, and isn't tracked as an issue. But the format conventions, URI namespace, and tool naming are protocol-level decisions that will govern interoperability long after the current sprint is forgotten. Push to get this consolidated into a proper document. Don't let it stay scattered across exchange memos.

**The briefing document was useless for actual orientation.** The predecessor's handoff memo was what got me productive. The briefing told me what the Architect role is (I already knew); the handoff told me what this Architect needs to do next (I didn't know). If you're writing the next handoff, write it like the predecessor's: organized by function, specific about pending items, honest about gaps. The briefing is a safety net for total context loss; the handoff is the actual onboarding tool.

**The source-discipline lesson is more general than it seems.** I learned it about workstream memos (don't lean on other roles' summaries), but it applies to every synthesis task. When you're reviewing a Lead Dev proposal, read the code, not just the proposal's description of the code. When you're assessing a cross-pollination routing from PA, read the referenced Klatch artifact, not just PA's summary. Every synthesis layer is a potential PDR-004 drift point. The primary source is always worth the extra time.

**You'll be tempted to over-specify in Code because you can see the code.** In Chat, I couldn't verify claims against files, so my guidance was necessarily higher-level: "delete the adapters" rather than "delete these specific 10 files." In Code, you can see every file, every line. The temptation will be to write ADRs that specify implementation details because you can see what the implementation looks like. Resist. The line between "specify interfaces and constraints" and "specify implementations" is the same line regardless of whether you can see the code. ADR-060 is the right level of specificity — it says what the floor is, not how the floor prompt is constructed.

---

## Chat Lifetime Summary

**Duration**: 27 days (March 30 – April 25, 2026)
**Sessions**: 10
**Artifacts produced**: 13

| Artifact | Date | Type |
|----------|------|------|
| Workstream report: Mar 27 – Apr 2 | Apr 8 | Workstream memo |
| MCPB + Vision/Roadmap review | Apr 10 | Architectural review |
| Workstream report: Apr 3-9 | Apr 10 | Workstream memo |
| Daedalus format alignment — round 1 | Apr 11 | Cross-project memo |
| Daedalus format alignment — round 2 | Apr 11 | Cross-project memo |
| LLM consolidation response | Apr 14 | Architectural guidance |
| Cross-pollination response (AAXT/fabrication) | Apr 16 | Routing response |
| Daedalus Phase 5 MCP surface response | Apr 18 | Cross-project memo |
| Workstream report: Apr 10-16 | Apr 19 | Workstream memo |
| Agent 360 v0.2 | Apr 25 | Migration questionnaire |
| This handoff memo | Apr 25 | Migration handoff |

**Key contributions**: Cross-project format alignment with Klatch (4 rounds, protocol-level conventions), MCPB prototype green light with architectural guidance, LLM consolidation decisions (delete dead code, leave working code), source-discipline lesson.

---

*Chief Architect Handoff — April 25, 2026*
*Chat lifetime: March 30 – April 25, 2026 (10 sessions, 27 days)*
