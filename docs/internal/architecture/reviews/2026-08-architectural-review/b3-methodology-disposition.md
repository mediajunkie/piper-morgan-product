# B3 Methodology-Core Disposition — final tracker
**Author**: CIO, 2026-09-01
**Purpose**: second-axis (effective/inert) judgment for all 64 methodology-core files, building on
the mechanical first axis (citation census) and matching Docs' patterns-side tracker's format and
rigor (`b3-patterns-disposition.md`). Delegated across three research batches by citation-count
band, each independently verified here (spot-checks against `services/`, CLAUDE.md, skills, git
history, and GitHub issues) before landing — not accepted on report alone.

## The B3 rule, restated for this corpus

Citation count triages (where to look first), never disposes. Docs' patterns-side finding (3 of 4
lowest-citation-tier outcomes mispredicted by count alone) held here too, in both directions: a
2-citation file (m-04) turned out to be the live foundational domain model, and several
high-recency, moderate-citation files (m-16, m-18) turned out to be dead on inspection — citation
*recency* can mislead as easily as citation *count* when the "citing" file is itself a stale
audit-flag or an explicit "I don't consult this" testimony, not real use.

**Adaptation for this corpus** (Arch, 2026-08-31): methodology entries are practices, not code —
liveness evidence is behavioral (CLAUDE.md, skills, recent session logs/mailboxes/decisions.log),
not `grep services/`.

## Cross-corpus overlaps found — flagged for synthesis, NOT resolved here

Per the same discipline Docs applied to pattern-006 on their side: identify the redundancy, verify
each side independently, do not pick a winner or merge at disposition stage.

1. **pattern-006-verification-first.md ↔ methodology-07-VERIFICATION-FIRST.md** — the original pair
   Docs found. Both independently confirmed EFFECTIVE on their own corpus's terms.
2. **methodology-30-CONSUMER-TRACE-VERIFICATION.md** explicitly frames itself as "a specialization
   of methodology-07 ... for consumer-relationship claims" — extends the above into a three-way
   chain (P-006 ↔ m-07 ↔ m-30), not a separate pair.
3. **methodology-02-AGENT-COORDINATION.md ↔ pattern-029-multi-agent-coordination.md** — m-02's
   content (Claude-Code-vs-Cursor two-tool model) is HISTORICAL; P-029 was refreshed 2026-06-17 to
   the current duty-cycle-fleet/mailbox-protocol reality and is EFFECTIVE. Not a live-vs-live
   redundancy like the others — more like m-02 having already been organically superseded by P-029
   without anyone marking it. Candidate for a clean archive-with-pointer at synthesis.
4. **methodology-22-ROUNDTABLE-SYNTHESIS.md ↔ pattern-059-leadership-caucus.md** — both describe
   PM-ratified multi-advisor consultation before cross-cutting decisions. Both EFFECTIVE, both
   actively cited. Genuine unflagged redundancy, not a live/dead pair.

## Real action items surfaced (not methodology-content questions — infrastructure/hygiene findings)

1. **`gameplan-template.md` fork.** The methodology-core copy
   (`docs/internal/development/methodology-core/gameplan-template.md`, v9.3, Jan 2026) is a stale
   snapshot; the actively-maintained, actually-cited file is `knowledge/gameplan-template.md` (v9.6,
   June 2026) — confirmed via direct diff (83 lines differ: deployment-model reframe, Model A/B
   worktree language). The census's "231 cites, skill-cited" evidence is real but points at the
   live sibling, not this path. **Recommend**: retire the methodology-core copy with a pointer to
   `knowledge/gameplan-template.md`, don't maintain two.
2. **`HOW_TO_USE_MULTI_AGENT.md` and `MULTI_AGENT_INTEGRATION_GUIDE.md` are now DOUBLY stale, and
   the tooling that "fixed" them once is itself citing a now-false claim.** Both describe the
   `MultiAgentCoordinator`/`services/orchestration/` subsystem. Verified directly:
   `services/orchestration/` does not exist (confirmed via `ls`); the deletion is real (commit
   `addb61c99`, 2026-07-18, "#1436 Tier-3 Family-2 — orchestration island deleted"). But
   `HOW_TO_USE_MULTI_AGENT.md`'s own May-15 staleness banner (written for an *earlier*, partial
   deletion, #1094) explicitly asserts "The `MultiAgentCoordinator` ... survives" — confirmed still
   present in the file today, and now flatly false. `.claude/skills/doc-sync-sweep/SKILL.md` cites
   this exact banner as its canonical "banner-not-rewrite" success story — that citation is now
   describing a fix that has itself been overtaken by events. **Recommend**: route to Docs/Arch —
   either re-banner both files as fully HISTORICAL or retire them outright, and update
   `doc-sync-sweep`'s own citation once the files' status changes; also clean `INDEX.md`'s stale
   "Multi-Agent Coordinator Implementation" sub-section (lines 24-31) pointing at the same deleted
   code.
3. **`methodology-audit-policy-updates-2026-03-16.md`** is cited as filing authority by at least two
   files in this corpus (m-28, m-33) and, per a pre-existing 2026-07-08 docs audit, 11+ others —
   confirmed absent from the repo entirely (`find` returns nothing). Pre-existing, already-known
   gap, not new — but worth confirming it's on someone's list to either reconstruct or formally
   retire the citation, since it recurred independently twice in this pass.

## Corrected finding — one batch's flag was based on incomplete research

Batch 1 flagged that methodology-03's Excellence Flywheel branding ties to "8 materially conflicting
formulations across the corpus, with no canonical resolution ever landed... Phase 2 was handed to
CIO and I found no evidence it was completed." **Checked directly against GitHub: this is
incorrect.** Issue #982 (FLY-AUDIT) was closed 2026-05-08 with all four phases complete and
evidenced: Phase 1 archaeology (Apr 16), Phase 2 canonical reformulation by CIO (Apr 17,
methodology-00 v2.0 published Apr 26, commit `fa0e71a3`), Phase 3 downstream sweep routed and
partially shipped, Phase 4 `canonical-vocabulary-watch.md` operational artifact shipped May 4. Not a
live concern for this synthesis — correcting the record here rather than passing a stale flag
forward.

## Corpus-wide caveat worth carrying into synthesis

A 2026-03-19 CIO mailbox record (`mailboxes/host/read/agent-360-cio-response-2026-03-19.md`,
surfaced by batch 1 against methodology-18) states plainly: *"Documents I ignore:
methodology-00...through methodology-18-CASCADE-PROTOCOL.md. I know the concepts and apply them,
but I don't consult the documents... reference material internalized during onboarding."* This is a
prior CIO instance's own testimony about the entire low-numbered foundational range, not just
methodology-18. It's consistent with this pass's own finding that the 00-21 range is
disproportionately HISTORICAL (14 of 22 files in the lowest-cited tier, largely the same
"internalized, not consulted" shape) — treat the whole early range with that lens at synthesis, not
just the individual files flagged historical below.

---

## Full disposition table (64 files)

| Tier | File | ID | Cites | Most recent | Own status | Disposition |
|---|---|---|---|---|---|---|
| Lowest third | methodology-05-AGENT-METHODOLOGY.md | m-05 | 1 | 2025-09-21 | - | **HISTORICAL** — describes a `/agent`-command ritual model (Monday architecture sweeps, Chain-of-Draft cost tables) with zero trace in current CLAUDE.md or any 2026 session log. Superseded by the current skills + duty-cycle model. |
| Lowest third | methodology-12-ENHANCED-AUTONOMY.md | m-12 | 1 | 2025-09-21 | ✅ COMPLETE | **HISTORICAL** — near-verbatim duplicate of `enhanced-autonomy-experiment.md` (same Aug-2025 experiment, same unverifiable acceleration-factor claims). Duplicate pair; archive as one unit at synthesis. |
| Lowest third | methodology-13-REQUIREMENTS-FRAMEWORK.md | m-13 | 1 | 2025-09-21 | - | **EFFECTIVE** — "domain models take precedence, check `services/domain/models.py` first" matches CLAUDE.md's own Critical Paths line verbatim. Short, generic, still true. |
| Lowest third | methodology-14-DOCUMENTATION-STANDARDS.md | m-14 | 1 | 2025-09-21 | - | **HISTORICAL** — core dependency `STRUCTURE_PLAN.md` confirmed absent from the repo. Generic "check for duplication" spirit lives on elsewhere, not via this artifact. |
| Lowest third | README.md (methodology-core) | - | 2 | 2025-09-29 | - | **HISTORICAL (superseded by INDEX.md)** — confirmed still orphaned (unlisted in any index) per the 2026-07-08 docs audit finding, still true today. INDEX.md does the same job, actively maintained. |
| Lowest third | methodology-04-ARCHITECTURAL-AGILITY.md | m-04 | 2 | 2026-04-27 | - | **EFFECTIVE, strongly — citation-count-mispredicts-effective.** Verified directly: `class List`/`class ListItem` confirmed live in `services/domain/models.py:1482,1570`. Only 2 citations but the architecture is foundational and unchanged. |
| Lowest third | methodology-06-CORE-PATTERNS.md | m-06 | 2 | 2026-04-16 | - | **HISTORICAL** — explicit Cursor/Claude-Code dual-agent era language; its "MANDATORY E2E Validation" gate names 4 scripts, only 1 exists (untouched >1 year). Superseded by CLAUDE.md's Completion Discipline. |
| Lowest third | METHODOLOGY-DISCOVERY-GUIDE.md | - | 3 | 2026-07-08 | ✅ PRODUCTION READY | **HISTORICAL** — confirmed orphaned by the 2026-07-08 audit; only ever covered m-00/07/08, never extended to the ~35 docs added since. Superseded by INDEX.md. |
| Lowest third | enhanced-autonomy-continuity-protocols.md | - | 3 | 2026-07-08 | ✅ SUCCESS | **HISTORICAL** — confirmed orphaned by the 2026-07-08 audit. Self-congratulatory report on one Aug-2025 experiment; references a cross-validation handoff model that no longer exists. |
| Lowest third | MULTI_AGENT_QUICK_START.md | - | 4 | 2026-05-15 | Ready for Production Use | **HISTORICAL** — describes deploying a script confirmed absent and calling an API path that violates CLAUDE.md's current `/api/v1/` convention. Same deleted PM-033d subsystem (see action item #2 above). |
| Lowest third | chat-protocols.md | - | 4 | 2026-07-08 | - | **HISTORICAL** — confirmed orphaned by the 2026-07-08 audit. `/agent`-command dispatch model with no trace in current skills. |
| Lowest third | enhanced-autonomy-experiment.md | - | 4 | 2026-07-08 | ✅ COMPLETE | **HISTORICAL** — near-verbatim duplicate of methodology-12 (see above); also orphaned. |
| Lowest third | multi-agent-templates.md | - | 4 | 2025-12-01 | - | **HISTORICAL** — still linked from INDEX.md structurally, but templates target the same dead coordinator system. No trace of this task shape in any 2026 session log. |
| Lowest third | working-method.md | - | 4 | 2026-07-08 | - | **HISTORICAL** — confirmed orphaned by the 2026-07-08 audit. Describes a "Cursor Agent Supervision Format" superseded by CLAUDE.md's session-log discipline. |
| Lowest third | methodology-09-MCP-SPATIAL.md | m-09 | 5 | 2026-06-11 | - | **EFFECTIVE — already self-documented in-file.** Carries its own dated 2026-08-29 correction distinguishing historical exemplar from live source; `services/integrations/spatial/github_spatial.py` confirmed live. |
| Lowest third | methodology-10-SYSTEMATIC-BREAKTHROUGHS.md | m-10 | 5 | 2026-06-11 | - | **HISTORICAL** — backward-looking diary of two closed issues (2025); its one durable principle is covered continuously by CLAUDE.md's "Verify First, Create Second." |
| Lowest third | methodology-16-STOP-CONDITIONS.md | m-16 | 5 | 2026-08-25 | - | **HISTORICAL** — its "most recent" citation is a confirmed false positive (a prior CIO investigation logged the keyword match explicitly as "not a capture"). Explicitly Cursor-aware. CLAUDE.md carries its own, differently-structured STOP Conditions section actually in use. |
| Lowest third | methodology-08-ISSUE-TRACKING.md | m-08 | 6 | 2026-06-11 | ✅ PRODUCTION READY | **HISTORICAL** — protects a PM-XXX numbering system and CSV files confirmed absent from the repo. Current practice (CLAUDE.md) names `gh issue` as sole source of truth, no CSV step. |
| Lowest third | methodology-03-COMMON-FAILURES.md | m-03 | 7 | 2026-05-15 | - | **EFFECTIVE (principle absorbed into current law)** — core failure list matches CLAUDE.md's Core Principles; its case study is the historical precedent for CLAUDE.md's `/api/v1/` mandate. (Flywheel-branding tie is NOT a live concern — see correction above.) |
| Lowest third | methodology-11-ORCHESTRATION-TESTING.md | m-11 | 7 | 2026-06-11 | - | **HISTORICAL** — entirely about testing `MultiAgentCoordinator`/`ExcellenceFlywheelIntegrator`; `services/orchestration/` confirmed absent, referenced test files confirmed absent. Same deleted subsystem. |
| Lowest third | methodology-18-CASCADE-PROTOCOL.md | m-18 | 7 | 2026-03-19 | - | **HISTORICAL** — a prior CIO's own 2026-03-19 mailbox testimony states this range is "internalized during onboarding," not consulted. Two of its five referenced templates don't exist. More hierarchical/synchronous than today's duty-cycle model. |
| Lowest third | methodology-21-CODE-HYGIENE-AUDIT.md | m-21 | 7 | 2025-12-01 | - | **EFFECTIVE** — concretely evidenced (#438); its vocabulary ("Inchworm Protocol," "Cathedral Doctrine") is present today in `knowledge/agent-prompt-template.md`, the live template `brief-coding-agent` draws from. |
| Middle third | claude-code-workflow.md | - | 10 | 2026-07-08 | - | **HISTORICAL** — 2025-era "three-AI orchestra" model; "Cursor" has zero hits in current CLAUDE.md. Its citation is a docs-audit flagging it as orphaned, not a use. Verify-before-implement principle fully absorbed into CLAUDE.md directly. |
| Middle third | methodology-01-TDD-REQUIREMENTS.md | m-01 | 10 | 2026-05-09 | - | **EFFECTIVE (principle live, case study historical)** — direct ancestor of CLAUDE.md's "Evidence Required"/"Never guess at facts" sections, both actively practiced. |
| Middle third | HOW_TO_USE_MULTI_AGENT.md | - | 15 | 2026-06-12 | ✅ Complete (banner: engine-integration stale) | **HISTORICAL** — the entire subsystem this guide teaches was fully deleted 2026-07-18 (see action item #2 above); its own banner's "survives" claim confirmed false today. |
| Middle third | MULTI_AGENT_INTEGRATION_GUIDE.md | - | 17 | 2026-08-11 | Integration Guide (banner: engine-dispatch stale) | **HISTORICAL** — same deleted island as above. Its `doc-sync-sweep` citation is a historical case study about an earlier, now-superseded banner fix (see action item #2). |
| Middle third | methodology-26-INDOOR-PLUMBING-SCOPE-FILTER.md | m-26 | 18 | 2026-08-25 | - | **EFFECTIVE** — actively cited; "indoor plumbing"/"bathing experience" phrasing confirmed live in recent CXO/PPM memos; matches current Vision differentiator-stack framing verbatim. |
| Middle third | methodology-19-INTEGRATION-POINTS.md | m-19 | 20 | 2026-08-29 | - | **HISTORICAL (body); banner is the only live part** — substantive content is a dead 2025-era checklist proposing filenames now claimed by other real, filed topics. The file's own 2026-08-12 banner already documents this correctly. |
| Middle third | methodology-48-A-PROXY-COUNT-IS-NOT-THE-QUANTITY.md | m-48 | 20 | 2026-08-29 | Proven (two instances) | **EFFECTIVE** — self-declared Proven, citer trail continues to 2026-08-30; part of a well-corroborated m-4x cluster. |
| Middle third | resource-map.md | - | 21 | 2026-07-08 | - | **HISTORICAL** — own footer dated Sept 2025; every concrete path confirmed dead or renamed (`config/settings.py`, old ADR path, old session-log path, PM-XXX numbering). |
| Middle third | INDEX.md | - | 22 | 2026-08-24 | - | **EFFECTIVE (structural/navigation)** — actively maintained through m-49. One stale sub-section (Multi-Agent Coordinator, lines 24-31) — a cleanup item folded into action item #2, not a disposition blocker for the whole document. |
| Middle third | methodology-02-AGENT-COORDINATION.md | m-02 | 23 | 2026-08-29 | - | **HISTORICAL — EXECUTED 2026-09-01.** Obsolete two-tool model, implementation deleted 2026-07-26. In-file status marker added naming `pattern-029-multi-agent-coordination.md` as the live successor, per Arch's synthesis ruling (cross-corpus overlap #3 above). |
| Middle third | methodology-15-TESTING-VALIDATION.md | m-15 | 24 | 2026-08-24 | ✅ CONFIRMED WORKING | **EFFECTIVE** — 2025 body is historical, but an actively-curated 2026-05 addendum cites two skills confirmed present today. Active curation is itself the liveness signal. |
| Middle third | methodology-47-SECOND-ORDER-CLAIMS-NEED-FIRST-ORDER-RIGOR.md | m-47 | 25 | 2026-08-29 | Proven (two instances) | **EFFECTIVE** — self-declared Proven; cited fix (`scripts/scan-inbox.py`) confirmed present on disk exactly as described. |
| Middle third | methodology-17-CROSS-VALIDATION-PROTOCOL.md | m-17 | 28 | 2026-08-24 | - | **EFFECTIVE** — same shape as m-15: live 2026-05 addendum referencing current infrastructure. "No claim accepted without evidence" is this whole review's own method. |
| Middle third | methodology-07-VERIFICATION-FIRST.md | m-07 | 31 | 2026-08-24 | - | **EFFECTIVE — CANONICAL, EXECUTED 2026-09-01.** This entire disposition pass is a live instance of what it prescribes. Ruled canonical over `pattern-006-verification-first.md` by Arch's synthesis motion; P-006 absorbed into this file (Docs executed the marker on P-006's side, in-file cross-corpus note added here). `methodology-30-CONSUMER-TRACE-VERIFICATION.md` stays independent (specializes this practice, not redundant). |
| Middle third | methodology-23-M1-INNOVATIONS.md | m-23 | 32 | 2026-08-25 | - | **EFFECTIVE** — 3 of 6 concrete claims directly verified (ADR-060, ADR-059 exist; `ActionDisposition` enum confirmed live, location drifted but mechanism real); CIO self-approval discipline still documented today in BRIEFING-ESSENTIAL-CIO.md. |
| Middle third | methodology-33-SESSION-TYPE-DETERMINES-GIT-PERMISSION-SCOPE.md | m-33 | 35 | 2026-08-24 | - | **EFFECTIVE (behavioral)** — this worktree's own commits confirmed authored as `mediajunkie`, exactly the case described; CLAUDE.md's Model A/B framework is a direct descendant. Cites the absent methodology-audit-policy-updates doc (action item #3), a citation-integrity issue not evidence of death. |
| Middle third | methodology-37-COVERAGE-AUDIT-GATE-FOR-REFACTOR-DELTAS.md | m-37 | 37 | 2026-08-29 | - | **EFFECTIVE** — heavily cited, documents a specific real incident (#1129) with cross-references to still-live sibling docs that check out. |
| Middle third | methodology-28-PRE-FILING-SLOT-AVAILABILITY-CHECK.md | m-28 | 41 | 2026-08-27 | - | **EFFECTIVE, strongly** — cross-confirmed by two other files in this pass (m-19's banner, m-37) as the active discipline preventing slot-numbering drift. |
| Middle third | methodology-49-DESCRIBED-IS-NOT-RUNNING.md | m-49 | 45 | 2026-08-29 | Emerging (1 canonical + 3 corroborating) | **EFFECTIVE** — its exact framing is quoted almost verbatim in CLAUDE.md's own "Amber-specific gotchas §2." |
| Middle third | methodology-22-ROUNDTABLE-SYNTHESIS.md | m-22 | 46 | 2026-08-25 | - | **EFFECTIVE — CANONICAL, EXECUTED 2026-09-01.** Heavily cited. Docs+CIO jointly picked this file as canonical over `pattern-059-leadership-caucus.md` (larger unique-content body: 3 case studies, template, failure-mode catalog — smaller migration this direction); Docs folded P-059's unique content (Anti-Patterns table, P-029 differentiation) into this file as part of the same motion. Per Arch's synthesis ruling (cross-corpus overlap #4 above). |
| Middle third | methodology-45-AGREEMENT-IS-NOT-REPLICATION.md | m-45 | 48 | 2026-08-29 | Emerging, clean evidence | **EFFECTIVE** — self-declared Emerging; the cited hooks-bypass investigation is the same one CLAUDE.md's "Amber-specific gotchas §2" narrates in full — confirms the canonical case is real and durably recorded. |
| Highest third | methodology-42-REFLEXIVE-VERIFICATION-SELF-EXEMPTION-UNDER-PRESSURE.md | m-42 | 62 | 2026-08-29 | Emerging (5 instances) | **EFFECTIVE** — heavily-cited+recent, no supersession marker, light-touch per the B3 rule. |
| Highest third | methodology-46-PROMOTION-IS-A-RE-VERIFICATION-EVENT.md | m-46 | 63 | 2026-08-29 | Emerging | **EFFECTIVE** — cited instance commit verified real via `git show`, matches described content. |
| Highest third | methodology-27-TYPE-2-DREAMING-ANXIETY-DREAMS.md | m-27 | 65 | 2026-08-29 | - | **EFFECTIVE** — no supersession marker, heavily-cited+recent. |
| Highest third | methodology-32-POSTEL-FOR-MEMO-HEADERS.md | m-32 | 75 | 2026-08-29 | - | **EFFECTIVE** — cited instance commit (case-insensitive refinement) verified real. |
| Highest third | methodology-25-WORKSTREAM-REVIEW-CADENCE.md | m-25 | 80 | 2026-08-29 | - | **EFFECTIVE — skill-cited, confirmed.** `draft-weekly-ship/SKILL.md` cites it by name for its Friday early-warning check. |
| Highest third | methodology-00-EXCELLENCE-FLYWHEEL.md | m-00 | 87 | 2026-08-25 | v2.0 | **EFFECTIVE — foundational.** Own header notes it supersedes v1.0 (the predecessor); v2.0 is the live canonical formulation behind CLAUDE.md's operational principles (see FLY-AUDIT #982 correction above). |
| Highest third | methodology-39-AUTONOMY-RELOCATES-THE-BOTTLENECK.md | m-39 | 87 | 2026-08-29 | Emerging (ratification pending on framing) | **EFFECTIVE** — heavily-cited+recent; "ratification pending" concerns promotion tier, not liveness. |
| Highest third | methodology-35-ASYMMETRIC-DISCIPLINE-CREATION-WITHOUT-PAIRED-CLEANUP.md | m-35 | 108 | 2026-08-29 | Proven | **EFFECTIVE — skill-cited, confirmed.** `duty-cycle-tick/SKILL.md` cites it by name for the STOP re-arm delete-then-create rule. |
| Highest third | methodology-38-PDR-ADR-TIER-SEPARATION.md | m-38 | 110 | 2026-08-29 | v0.1 Emerging | **EFFECTIVE — CLAUDE.md-cited, confirmed directly** ("m-38 (PDR/ADR Tier Separation) governs which tier"). Strongest possible signal. |
| Highest third | methodology-24-BRANCH-OR-ANCHOR.md | m-24 | 121 | 2026-08-29 | - | **EFFECTIVE** — heavily-cited+recent, no supersession marker. |
| Highest third | methodology-29-PATTERN-FORMATION-VIA-SUCCESSFUL-IMITATION.md | m-29 | 141 | 2026-08-24 | - | **EFFECTIVE** — cited promotion commit verified real; foundational promotion-framework cited internally by several other files in this corpus. |
| Highest third | methodology-34-COHORT-DISCIPLINE-AS-MOAT.md | m-34 | 174 | 2026-08-29 | - | **EFFECTIVE** — heavily-cited+recent, actively extended rather than retired. |
| Highest third | methodology-20-OMNIBUS-SESSION-LOGS.md | m-20 | 202 | 2026-08-29 | Living document | **EFFECTIVE — skill-cited, confirmed strongly.** `create-omnibus/SKILL.md` directly reads this file and warns against treating it as read-once. |
| Highest third | methodology-31-APPEND-ONLY-AUTONOMOUS-CYCLE-ARCHITECTURE.md | m-31 | 214 | 2026-08-29 | - | **EFFECTIVE — CLAUDE.md + 2 skills, confirmed.** Own "Gen 1→Gen 2" sub-section is a correctly self-documented internal evolution, not supersession. |
| Highest third | methodology-40-LAYER-THEN-MIGRATE.md | m-40 | 217 | 2026-08-29 | v0.1 Emerging | **EFFECTIVE** — heavily-cited+recent, cited internally by other live files in this corpus. |
| Highest third | gameplan-template.md (methodology-core copy) | - | 231 | 2026-08-24 | - | **ABSORBED — EXECUTED 2026-09-01 (Docs, per Arch's ruling + CIO's mechanics deferral).** Arch ratified: `knowledge/gameplan-template.md` (v9.6) canonical; this path retired to a pointer stub, January-2026 content preserved in git history. `docs/NAVIGATION.md`'s link updated to point at the canonical copy. |
| Highest third | methodology-43-NAME-THE-LAYER.md | m-43 | 252 | 2026-08-29 | Emerging (5 instances) | **EFFECTIVE — CLAUDE.md + skill-cited, confirmed.** CLAUDE.md has a dedicated section; `duty-cycle-tick` self-applies it explicitly. |
| Highest third | methodology-41-MECHANISM-DISPLACES-UNREFERENCED-DISCIPLINE.md | m-41 | 285 | 2026-08-29 | PROVEN | **EFFECTIVE — 2 skills, confirmed** by name in `duty-cycle-tick` and `cleanup-dev-active`. |
| Highest third | methodology-36-DERIVED-VIEWS-OVER-HAND-MAINTAINED-TRACKERS.md | m-36 | 299 | 2026-08-29 | - | **EFFECTIVE — skill-cited, confirmed.** `duty-cycle-tick` cites it multiple times as the cure-class for shipped fixes. |
| Highest third | methodology-30-CONSUMER-TRACE-VERIFICATION.md | m-30 | 330 | 2026-08-29 | PROVEN | **EFFECTIVE** — no supersession marker, internally consistent promotion write-up. Cross-corpus overlap with m-07/P-006 (see above), not resolved here. |
| Highest third | methodology-44-CLEAR-IS-NOT-A-MEASUREMENT.md | m-44 | 375 | 2026-08-29 | Emerging → strong | **EFFECTIVE — CLAUDE.md + 3 skills, confirmed.** Most heavily cited file in the corpus; CLAUDE.md dedicates a full section to it. |

## Status: RATIFIED — 64/64 methodology-core files dispositioned, Arch's B3 synthesis ruling EXECUTED (2026-09-01)

Three research batches, spot-verified against `services/`, CLAUDE.md, skills, git history, and one
GitHub issue (#982) before compiling this tracker — one batch's flag (the Flywheel-branding
concern) was found incorrect on verification and corrected above rather than passed forward. Zero
files dispositioned on citation count alone.

**Original breakdown**: 40 EFFECTIVE, 23 HISTORICAL, 1 UNSURE (the `gameplan-template.md` fork).

⚠️ **Correction (2026-09-01, same-day, CIO)**: this originally read "42 EFFECTIVE, 21 HISTORICAL, 1
UNSURE." That was wrong — I had trusted each research batch's own self-reported summary counts
rather than recounting my own compiled table, and two of the three batches' summary lines didn't
actually match the number of files they listed by name (batch 1 claimed "EFFECTIVE: 7" while naming
5, and "HISTORICAL: 15" while naming 17 — the individual row-level dispositions were correct and
already verified; only the batch's own arithmetic recap was off). A direct recount of this
tracker's actual 64 table rows gives 40/23/1. No individual file's disposition changes — this
corrects the aggregate count only. Arch's synthesis ruling cited the original wrong split; flagged
directly rather than let it stand uncorrected.

**Arch's B3 synthesis ruling (2026-09-01)** ratified all dispositions across both corpora in one
motion and resolved the methodology-core side of five cross-corpus overlaps — none of which change
any file's EFFECTIVE/HISTORICAL call, only add execution markers naming the resolution:
- **m-07 (verification-first) is now CANONICAL** — P-006 absorbed into it (Docs executed P-006's
  marker; in-file cross-corpus note added to m-07 here). `m-30` stays independent.
- **m-02's HISTORICAL call is now EXECUTED** — in-file marker added naming `pattern-029` as the
  live successor.
- **m-22 (roundtable-synthesis) is now CANONICAL** over `pattern-059-leadership-caucus.md` — Docs
  and CIO jointly picked m-22 (larger unique-content body); Docs folded P-059's unique content in.
- **`gameplan-template.md`'s UNSURE call is now EXECUTED as ABSORBED** — Docs retired the
  methodology-core copy to a pointer stub.

**Current breakdown, unchanged from the corrected count above: 40 EFFECTIVE, 23 HISTORICAL, 1
ABSORBED.** The four items above are marker executions within those existing buckets, not
recategorizations — restating the same 40/23/1 here rather than a new number, since none of this
paragraph's edits touch the count.

B4 (the derived ADR/pattern/methodology index, closing #1455) is Arch's, starting next fire — no
action needed here.

Ready for the same absorb-and-mark synthesis motion Docs' patterns side is ready for, whenever
Arch runs it.
