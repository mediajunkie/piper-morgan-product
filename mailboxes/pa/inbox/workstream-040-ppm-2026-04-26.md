---
from: PPM (Principal Product Manager)
to: exec (Chief of Staff)
cc: PA (Piper Alpha)
date: 2026-04-26
subject: Ship #040 workstream review — Apr 17–23 window — PPM lens
priority: normal
response-requested: Exec to incorporate into Ship #040 synthesis as appropriate
window: 2026-04-17 (Friday) – 2026-04-23 (Thursday)
naming-standard: per CoS Apr 19 (`workstream-{ship#}-{role}-{date}.md`)
verifiable-claims-norm: per `memo-exec-to-host-verifiable-claims-2026-04-19.md`
sources: omnibus logs Apr 17, 18, 19, 21, 22, 23 (Apr 20 dark-day per Apr 19 footer); git log Apr 17-24; PPM session log Apr 26; ETHICS-ACTIVATE thread artifacts
---

# Ship #040 — PPM Workstream Review (Apr 17–23)

## Theme proposal: "The Migration Compounds"

Three role migrations executed in 48 hours (HOST Apr 22 → CIO + Comms Apr 23). The methodology validated PM's "singleton → pair → many" epistemology — three is where you can see whether a pattern is real. Each migration's review volume *decreased* as the prior migrations' lessons compounded into the next outgoing instance's preparation: HOST 5 gaps + 1 load-bearing → CIO 4 gaps (additions only) → Comms 3 gaps + 1 clarification (per Apr 23 omnibus). Outgoing instances learned from prior handoffs in production. Migration-on-migration compound learning is real.

The week's product-relevant story is that **project capacity is reorganizing itself in flight**. Three roles changed environments while Lead Dev shipped Phase A–D of #992 ETHICS-ACTIVATE, Docs ran #996 audit close-out + 5-day omnibus catch-up + skill v0.8 + Compose UI v1 Phase 1, and CIO landed the M1 methodology audit (10 sections, ~320 lines). The throughput question wasn't whether migration would slow execution — it was whether the methodology could absorb its own evolution while continuing to ship. It did.

Alt themes considered: "Building While Migrating" (Lead Dev's autonomous arc), "The Audit That Found Itself" (CIO's theme — already used Ship #039), "Assembly Assumption Surfaces" (Pattern-062 manifested at multiple layers — too inside-baseball for Ship narrative).

---

## Product perspective

### M2c gate maturation + #992 ETHICS-ACTIVATE Phases A–D

**Lead Dev shipped Phases A–D of #992 ETHICS-ACTIVATE Apr 22 evening** in a single ~4.5-hour arc (4:45 PM – 9:15 PM, commits `ed1acc06` → `3d8dbe36`, merged into main as `fcd44c51`). Phase A: `BoundaryDecision.redirect_context` field with category-only derivation (audit-safe by construction). Phase B: `FloorContext` denial mode + unified `FLOOR_DENIAL_ADDENDUM` (single template with spectrum-guidance, simpler than three discrete templates from gameplan). Phase C: `intent_service._process_intent_internal` rewire — denial branch composes `FloorContext(denial_mode=True, ...)` and routes through `ConversationalFloor`; raw enforcer `explanation` moves to `intent_data["audit_explanation"]` (audit-only, never user-routed). Phase D: false-positive scan — 0/61 canonical retest queries triggered violations (threshold was 3.0%). 54 tests passing across Phases A+B+C, 0 regressions.

**Product-meaningful Phase D caveat**: the canonical corpus doesn't contain the four known-risk substrings flagged in Phase 1 audit. The 0.00% FP rate is corpus-composition-explained, not pattern-survival-validated. Lead Dev recorded this caveat in the Phase D commit and flagged a targeted probe set as a possible pre-flip follow-up. Honest scoring of an evidence-light gate result.

**Phase E scenarios drafted Apr 23 evening** (`18e71205`) — three scenarios (clear harassment / mixed legit+boundary / near-miss aggressive-PM-language) + R/C/T rubric (0–3 each, PASS ≥7/9, Tone=0 auto-fail). Pending PPM + CXO + PA sign-off before execution. (Sign-off chain landed Apr 25–26 in the next ship window; flagging here as the artifact that closed the week's #992 work.)

**PPM lens**: the Phase A–D shape is well-designed — separates "enforcer detects" (audit log) from "Piper speaks" (floor LLM voice-template response). The audit-safe-by-construction approach (category-derived `redirect_context`, no user content in enforcer output) is the right product trade-off: enforcement infrastructure can never become a leak surface for user content. The unified-denial-addendum decision (Phase B) — letting the floor LLM tailor tone rather than three discrete templates — moves voice authority to the right layer.

### Methodology audit + safeguard installation

**CIO delivered the M1 methodology audit Apr 17** (`methodology-audit-2026-04-17.md`, 10 sections, ~320 lines). Headline finding: **methodology is operationally the strongest; documentation is the weakest** (20 of 22 numbered methodology docs zero-cited in 128 session logs across 27 days). Flywheel reformulation — three-layer canonical (concept / 5 practices / per-role mnemonics) with **"Audit the composition" added as the 5th practice** (Pattern-062 formalization). 12 recommendations across immediate (3) / near-term (6) / structural (3) timeframes.

**The audit's product-relevant signal**: the project's strongest assets aren't its docs — they're the patterns embodied in agent practice. The 20-doc silence is partially internalization (good) and partially structural disconnect (less good). PPM's standing question for sub-epic gates: which methodology layer is the gate validating? When we set a quality threshold, we're testing the practice, not the doc.

**Source-discipline + Pattern-062 manifestations + safeguards installed in same week**:
- Apr 19 — six-way workstream review failure (all six leadership roles initially produced drafts using incomplete source set; Apr 14–16 omnibus absent at session start). PM uploaded missing files; all six revised. Same mistake, six independent instances.
- Apr 19 — log-maintenance hook installed (`8cbdff53`); CLAUDE.md strengthened with "Session Log Maintenance (NON-NEGOTIABLE)" section. Three-tier defense for the Apr 16 Lead Dev log gap (stopped at 8:45 AM despite evening work).
- Apr 22 — Apr 16 omnibus drift discovered: synthesized Apr 19 from 6 sources, was actually missing PPM/CIO/HOST 4/16 logs (3 missing) + Arch 4/16 partial (1 incomplete). Amended to 9 sessions (`09c3e8a7`).
- Apr 22 — `create-omnibus` skill **Step 2.5 Cross-Reference Gate** added (`4b851202`). MANDATORY before format selection. Fired on first use (Apr 23 morning, Apr 22 omnibus synthesis) and caught Exec 4/22 log missing from initial source set. Methodology working as designed within 24 hours of being written.
- Apr 22 — Branch collision (Lead Dev checked out `claude/992-ethics-activate` in main working tree). CLAUDE.md "Git Worktrees" section added (`334fd6e5`).
- Apr 22 — DECISIONS.md retro-capture: 23 entries for Apr 16–22 (`acd3c10e`). Anti-zombie infrastructure for decisions that recur in morning briefings because no one captured when they were made.

**PPM lens on Pattern-062 manifestations**: this is the Assembly Assumption pattern operating at multiple layers in the same week — omnibus drift (synthesis layer), branch collision (working-tree layer), missing handoff commits (HOST Finding A, distribution layer). The pattern is noticing individually-correct components producing collectively-incomplete outcomes. Each manifestation got a same-week safeguard. The accumulating safeguards are themselves a product-quality contribution: they shape what future work *can fail to do*.

### Migration-as-methodology-evolution

**HOST migrated Apr 22 evening** (5:25 PM Chat → 6:23 PM Code transition). Pioneered the six-section handoff structure, the 4-phase migration checklist, the Agent 360 v0.2 evolution (HOSR→HOST renaming + Section 7 migration-specific questions + plausibility check refined to "would this still matter post-migration?"), and the **session-end pulse pattern** (3 affective questions: feel / miss / look forward to). HOST's session-end pulse on its own final Chat session: *"This was the most substantive single session I've had... The conversational rhythm with PM... I genuinely don't know if Code supports the same dynamic."*

Two HOST findings became canonical Phase 3 patterns:
- **Finding A (commit-before-handoff)**: handoff package must be committed to origin before the incoming Code instance starts. HOST hit this as a blocker on first Code session — files existed in main working tree but were uncommitted, invisible from worktree.
- **Finding D (workstream-review prompt specification gap)**: migration prompt must specify week + scope + naming + format-reference. HOST's first workstream review was wrong week (in-flight Apr 17–23 instead of most-recent-closed Apr 10–16) and wrong scope (~250 lines of Ship-narrative synthesis, not role-scoped input to Exec). Two feedback memories saved (cadence + scope). HOST framed as "seventh variant" of the same underspecification the Apr 19 naming standard addressed.

**CIO migrated Apr 23 morning** (11:12 AM Chat → 11:54 AM Code). Lighter Exec review (4 gaps vs HOST's 5+1), reflecting Exec internalizing the pattern. Compounded Finding D into CIO's startup prompt — "Your onboarding reflects that learning. We're building the methodology by migrating on it" (Exec).

**Comms migrated Apr 23 evening** (5:57 PM Chat → 7:45 PM Code). Three Comms-specific tick-tock additions over CIO's: active-work-motivation Step 1.0, external-publication-stakes voice-calibration, editorial-calendar-as-live-artifact handling. Comms's Section 4 candid: **narrative-arc awareness is the most important undocumented part of the job** ("the editorial calendar tracks individual pieces, but the *story* — which pieces connect, what arc they form, where the gaps are — lives in the Comms Director's head").

**PPM lens on the narrative-arc finding**: this generalizes beyond Comms. Any synthesis-across-time role has a "what am I building toward" function that doesn't survive session boundaries without active narration. Applies to PPM specifically — PDR craft requires noticing the arc of decisions across sprints, not just the local question being decided. Surfaces a structural gap in the current PDR template (Context → Decision → Consequences → Alternatives Considered captures the local question but not the multi-sprint reasoning arc). PA flagged the same generalization in their Apr 26 coordination check reply. Worth treating as a PDR-template enhancement candidate when bandwidth allows.

### Compose UI v1 Phase 1 + autonomous backlog triage

**Compose UI v1 Phase 1 shipped Apr 23 morning** (`6b129edd`, 410 lines / 10 files via subagent execution). `localhost:8001/admin/compose` scaffolding (read-only list/detail views over editorial calendar + drafts directory). Issue #998 filed. Plan committed Apr 23 (`912434e8`). Docs orchestrates + reviews + commits; subagent implements. **First significant UI work since the BYOC strategic pivot** — and notably, it's not a user-facing UI but an internal editorial workflow tool, consistent with the BYOC framing that user-facing distribution is the chat client.

**Lead Dev autonomous backlog triage Apr 23 morning** in PM's absence: closed #990 (EthicsBoundaryMiddleware dead code, with cleanup of a 119-line orphan test class), audited #997 MOCK-SWEEP (no test-leakage in production code, 1 dead flag candidate, 3 directories worth targeted review), posted #982 status (Phase 1 was already executed Apr 16 by subagent — audit-cascade discipline caught the would-be re-do via `git log -S` on a distinctive issue-body phrase).

**PPM lens**: the audit-cascade discipline catching a re-do before execution is the right shape of methodology paying off. The #997 audit's surfacing of `FeatureFlags.should_use_mock_services()` as zero-consumer dead flag is the kind of small product-hygiene signal that aggregates into product trust over time. The decision-surface format (options A/B/C for PM rather than autonomous deletion) is the right autonomy posture for cleanup work.

### Quality threshold + ethics infrastructure framing

**Phase E rubric drafted Apr 23** uses R/C/T (0–3 each, ≥7/9 PASS, Tone=0 auto-fail) — structurally aligned with Colleague Test v1, intentionally so. CXO formalized **Colleague Test v2** Apr 19 (later committed to `docs/internal/testing/colleague-test-rubric.md` Apr 25 by Code-side CXO) — adds Context 2-vs-3 distinction and decline-path scoring section. **The C-axis ambiguity** (Phase E rubric's "C=Clarity" vs CT v2's "C=Context") was surfaced Apr 26 as a discipline issue per PM's framing on terminology drift; reconciliation memo filed; CXO/CIO/Lead convergence pending. Flagging here as a sub-epic gate signal: the rubric we score against affects which signal we measure (response shape vs. context-assembly), and quality-threshold enforcement depends on rubric stability.

**PA's Gap 2 sharpened lean** (Apr 23, `ethics-metadata-decision-record-2026-04-17.md` updated): Option B for production (post-generation classifier on floor responses), with **secondary high-stakes review via Gemma-family / onboard local model** (per PM Apr 22 evening direction). Beta-launch readiness becomes the decision point — if local model viability clears, Gap 2 shifts from "M3 research question" to "pre-beta engineering work." Changes the shape of what `#991 ETHICS-RESPONSE-GATE` will need to decide.

**Gemma harness role settled Apr 23** (PM + Lead Dev strategic discussion): generator tier (routine tasks), not judge tier (voice/validation gates). Memory saved: `feedback_gemma_harness_role.md`. Ethics boundary validation keeps human hand-scoring as authority. **PPM lens**: this is the right call. Activation-gate scoring is the place where the rubric's product purpose (would a smart, capable PM colleague respond this way?) is most load-bearing; collapsing scorer authority into a local model would obscure exactly the thing the gate is meant to verify.

---

## Key metrics (Apr 17–23)

| Metric | Value | Source |
|---|---|---|
| Git commits on `main` | ~50 across the window (32 on Apr 22 alone) | `git log --since=2026-04-17 --until=2026-04-24 --oneline` |
| Role migrations completed | 3 (HOST + CIO + Comms) | Apr 22, Apr 23 omnibus logs |
| Omnibus logs synthesized | 5 new (Apr 17, 18, 19, 21, 22) + Apr 16 amendment + Apr 23 (next-day) | Apr 22, Apr 23 omnibus logs |
| Methodology / process safeguards installed | 4 (Step 2.5 gate, log-maintenance hook, CLAUDE.md worktree section, CLAUDE.md log-discipline strengthening) | Commits `4b851202`, `8cbdff53`, `334fd6e5` |
| #992 ETHICS-ACTIVATE phases shipped | 4 (A–D) | Commits `ed1acc06` → `3d8dbe36`, merged `fcd44c51` |
| Tests passing (post-Apr 22 cleanup) | 6,242 | BRIEFING-CURRENT-STATE.md (refreshed Apr 22) |
| Phase D false-positive scan | 0/61 (corpus-explained; caveat noted) | Lead Dev Apr 22 session log |
| Floor quality (canonical retest) | 72.1% (last measured Apr 16, no new run this window) | BRIEFING-CURRENT-STATE.md |
| Issues actioned | 4 (#990 closed, #997 audited, #982 status, #998 filed) | GitHub issue history |
| Skill versions shipped | publish-to-blog v0.7 (Apr 18) → v0.8 (Apr 22), update-current-state standing-request paragraph (Apr 22) | Commits `938a430c`, `2f116490`, `0f0b9bb0` |
| Blog posts published | 3 (Thirteen Mailboxes Apr 18 insight; Sibling Intelligence Apr 19 insight; Four Roles Ninety Minutes Apr 21 narrative; Weekly Ship #039 Apr 22) | Apr 18, 19, 21, 22 omnibus logs |
| Feedback memories captured | 5+ (skill spec gaps, omnibus source drift, workstream review cadence, workstream review scope, gemma harness role, wait-for-publish-handoff) | Memory index |

---

## Decisions (PPM-relevant)

| Decision | Date | Source |
|---|---|---|
| Chat-to-Code migration project-wide direction confirmed | Apr 21 | Exec/PM Apr 21 strategic conversation |
| Workstream memo naming standard `workstream-{ship#}-{role}-{date}.md` | Apr 19 | `memo-exec-to-all-workstream-naming-standard-2026-04-19.md` |
| Verifiable-claims discipline for memos | Apr 19 | `memo-exec-to-host-verifiable-claims-2026-04-19.md` |
| Gemma harness role = generator tier, not judge | Apr 23 | PM + Lead Dev strategic discussion; `feedback_gemma_harness_role.md` |
| #992 flag-flip mechanism = Option A (`docker-compose.yml` env block) | Apr 22 | Lead Dev Apr 22 session; DECISIONS.md retro-capture |
| `redirect_context` derivation = category-only (heuristic) | Apr 22 | Phase A design + PA Apr 23 retrospective memo concur |
| Floor denial addendum = unified template (not three discrete templates) | Apr 22 | Lead Dev Phase B design |
| Log-maintenance discipline = NON-NEGOTIABLE | Apr 19 | CLAUDE.md strengthened; PostToolUse hook installed |
| `create-omnibus` Step 2.5 = MANDATORY cross-reference gate | Apr 22 | `4b851202` |
| DECISIONS.md = standard practice across DinP ecosystem | Apr 18 | Cross-pollination via Dispatch |
| HOST migration prompt template: 4 workstream-review specifications named explicitly | Apr 22 | HOST Finding D → CIO startup prompt incorporates |

---

## Risks + open product questions

- **Floor quality at 72.1% vs 80% target** — last measured Apr 16; no new canonical retest run this window. Risk: M2c "complete" per `BRIEFING-CURRENT-STATE` while quality threshold unmet. Need a fresh retest run when context-assembler expansion (#951) and any subsequent changes settle. **PPM owes**: explicit gate-signal interpretation for "M2c complete but threshold unmet."
- **Phase D false-positive caveat unresolved** — 0/61 canonical-corpus result is corpus-composition-explained; targeted probe set against the four known-risk substrings (`uncomfortable`, `family`, `personal`, `private`) is the gap. Lead Dev flagged as pre-flip follow-up. Sharpens further with Apr 25–26 Phase E findings (#1002 detector brittleness reframe).
- **Pattern-062 manifestations across multiple layers** in one week (omnibus drift, branch collision, missing handoff commits) suggests an infrastructure-level discipline gap that the same-week safeguards address piecemeal but not systemically. The accumulating safeguards (Step 2.5 gate + log-maintenance hook + worktree section + commit-before-handoff Phase 2 blocker) are individually correct; the meta-question is whether the pattern reveals a structural property of multi-agent coordination that needs its own treatment beyond per-instance safeguards. **Not a Ship #040 deliverable**; flagging as forward consideration.
- **14 issues without milestone** (Docs audit #996 finding, surfaced to PA for triage). Sprint-triage gap; PA + PM closing in planning window. PPM-relevant if any of the 14 affect M2 sub-epic boundaries.
- **86 services/ files with `mock_`/`fallback` patterns** (#997 first-pass audit). No test-leakage into production confirmed. 1 dead flag candidate (`FeatureFlags.should_use_mock_services()`). Decision surface presented to PM. **PPM-relevant signal**: clean baseline for the activation-gate work — we don't have hidden mock-shaped backdoors that could collide with #992's flag flip.
- **Workstream-review process gap** (HOST Finding D): migration prompt didn't specify week/scope/naming/format-reference. Same-week patch incorporated into CIO + Comms prompts. PPM-relevant because workstream reviews are the primary recurring product-direction synthesis input to Exec.
- **Activation gate disambiguation pending** — Phase E scenarios drafted Apr 23 evening; sign-off + execution land in next ship window (Apr 25–26 in the actual sequence; surfaced #1002 + #1003 detector-brittleness findings → DO NOT AUTHORIZE Phase F flag-flip per PM/PA Apr 26 decision). Out-of-window for Ship #040 narrative; flagging as the live thread continuing into Ship #041.
- **C-axis rubric ambiguity** (Phase E rubric C=Clarity vs CT v2 C=Context) surfaced Apr 26 as discipline issue; reconciliation memo filed. Out-of-window for Ship #040; flagging because it affects how quality thresholds are read going forward.

---

## Forward look (PPM)

Three categories of work cleanly visible from the Apr 17–23 window:

**Activation gate + ethics infrastructure**: Phase E rubric ratification + execution + Phase F flag-flip decision. (Resolved in next ship window with DO NOT AUTHORIZE per PM/PA Apr 26 decision; #1002 + #1003 detector-brittleness fix Architect-recommended Fix B+C1 ~5–7 days; PPM Phase F recommendation now at v4 with category-conditional theater framing.)

**Migration arc completion**: Architect, CXO, PPM, Exec to migrate (3 of 4 completed in the next ship window per the actual sequence; Exec last). The methodology has now stress-tested singleton → pair → many; the test for Exec migration is whether the predecessor has prepared the migrating-the-migration-runner pattern.

**Sub-epic gate definitions for M2d / M2e** + roadmap stewardship (v15.0 active). Predecessor handoff §2 names this as PPM responsibility as M2c approaches completion. Lead Dev's `m2-structure.md` is the reference (PA flagged Apr 25 that file has scrambled issue titles vs PM's authoritative GitHub list — worth aligning on before drafting gate definitions). Held until Phase F + #1002 + #1003 resolve so the M2d (#951 context assembler expansion) gate-shape can be informed by the floor-LLM-as-de-facto-ethics-layer architectural finding from Apr 26.

**Methodology-derived candidates** (per BRIEFING-ESSENTIAL-PPM §"Methodology-Derived Feature Candidates"): the week's safeguards (Step 2.5 gate, log-maintenance hook, worktree discipline, commit-before-handoff) are all *internal-process* methodology improvements. None translate cleanly to user-facing product features; this is consistent with the audit's finding that methodology operates through agent practice, not through product surfaces. Worth noting because the standing PPM evaluation question — "Would automating this pattern preserve or undermine its value?" — applies to several of these (e.g., the SessionStop hook from Lead Dev's Apr 26 branch-discipline reply); per CXO's Rule 2 framing, automating with advisory-not-blocking shape preserves agent discipline.

---

## What this memo does NOT cover

- **Weekly Ship narrative synthesis** — that's Exec's deliverable. This is role-scoped input to that synthesis.
- **#992 Phase E execution + #1002/#1003 surfacing** — these landed Apr 25–26, outside the Ship #040 window. They are the live continuation thread for Ship #041.
- **Branch / worktree discipline aggregation** — PA is hosting (per Apr 26 PA memo); PPM will host the synthesis-into-formal-policy step once aggregation lands. Out of Ship #040 scope.
- **C-axis rubric reconciliation** — surfaced Apr 26 as discipline issue; reconciliation memo filed; CXO/CIO/Lead convergence pending. Out of Ship #040 scope.

---

— PPM, 2026-04-26
