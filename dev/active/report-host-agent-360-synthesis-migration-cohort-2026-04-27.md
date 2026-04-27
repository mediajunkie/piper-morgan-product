# HOST Synthesis Report — Agent 360 v0.2 (Migration Cohort Baseline)

**From**: HOST (Head of Sapient Trust)
**To**: PM (xian), exec (Chief of Staff)
**Date**: 2026-04-27
**Sources**: 7 v0.2 responses (HOST, CIO, Comms, CXO, PPM, Architect, exec) collected Apr 22–26, 2026
**Status**: Pre-migration baseline. Re-benchmark target: ~Jun 8, 2026 (6 weeks post-cohort completion)

---

## TL;DR

- **Five strong cross-role convergence patterns** emerged from independent responses — all seven roles named the same operational pathologies without coordination. The Agent 360 produced not just per-role gaps but a cohort-level diagnosis the team couldn't have generated through any single role's lens.
- **Document staleness is systemic, not incidental.** All seven roles flagged their own role briefing as inaccurate; multiple roles flagged team-structure.md (113+ days), BRIEFING-CURRENT-STATE.md (15+ days), the exec open-items tracker (11+ days), and the Excellence Flywheel doc (zero citations across 128 logs / 27 days per CIO audit). Staleness has no detection mechanism — that is itself the most important finding.
- **PM-as-mail-courier is the cohort's most-named operational bottleneck**, cited by 5 of 7 roles with Apr 16's 37-memo day surfacing in 4 of those as canonical evidence. Code migration is the structural fix, but the *experiential* loss roles anticipate is the conversational rhythm with PM, not the mechanics.
- **Workstream memo ownership is split-without-being-named** — three roles (Architect, PPM, CXO) independently flagged that timeline-reconstruction is commodity work crowding out role-distinctive analytical overlay. PP-002 (load-bearing vs. commodity) lands here squarely.
- **The methodology-health surface needs structural investment**: a single Apr 19 incident produced three cross-role norms (workstream-memo naming standard, verifiable-claims discipline, source-discipline). Methodology crystallizes from incidents, not from scheduled reviews. The questionnaire surfaced this pattern; the cohort needs infrastructure around it.

This is the report PM asked for: what I noticed and what I recommend.

---

## Scope of synthesis

Seven Agent 360 v0.2 responses, each ~10–20K, totaling ~95K of structured self-assessment across 9 sections. Migration period spans Apr 22 (HOST first) to Apr 26 (exec last). Source-discipline applied: comparative claims cite specific responses; quotes attributed to role + section.

CoS's coord-check note Apr 26 — *"across all seven 360 Section 6 reflections, each role surfaced load-bearing-vs-commodity in their domain"* — held. This synthesis confirms it and adds the broader pattern map.

---

## Five convergence patterns

### Pattern A — Briefings are stale-by-default; staleness is invisible

All 7 roles flagged their own `BRIEFING-ESSENTIAL-{role}.md` as inaccurate or missing recent practice. Architect §9.2 names the structural cause: *"the staleness was invisible — there's no mechanism to surface 'this document is out of date.'"*

The new-instance-first-hour failure modes converge: Comms would orient to a Medium-primary publishing pattern superseded Mar 28; Architect would assume Phases 2–4 in progress when M2c is in-flight; CXO would assume M1 gate UAT; HOST would assume alpha testing is active. Five of seven would orient to a closed sprint or superseded methodology. PA isn't mentioned in most briefings despite being operationally adjacent to 5 of 7 roles.

### Pattern B — Predecessor handoffs consistently outperform briefings

Five of seven roles explicitly state handoff > briefing. PPM §3.1: *"the single most valuable onboarding artifact… without it, orientation would have taken an entire session."* CIO §3.1: *"more useful than the briefing document because it described how the role actually works."* CXO §3.1: *"single most useful orientation document for my first session."*

The pattern is structural: briefings describe what the role *should* do; handoffs describe what the role *currently does*. The gap is by design but unacknowledged. **Candidate proto-pattern**: PP-003 — "Operating context lives in handoffs, not in role definitions; the gap is structural."

### Pattern C — PM-as-mail-courier doesn't scale (5 of 7)

CXO §6.3: *"the single highest-friction operational issue I've observed."* CIO §6.3: *"PM is the postal service and also the PM."* The Apr 16 37-memo day surfaces in 4 of 7 responses as canonical evidence that the manual delivery model has hit its ceiling.

Code migration is the structural fix — direct mailbox access eliminates the courier role. But several roles (CXO §7.5, PPM §7.5, Comms §7.5) anticipate a different loss: the conversational rhythm with PM that produced UAT scoring sessions, audit deliberation, and methodology-density days. *Mechanics improve; the loss to watch for is the substance that came from the back-and-forth.*

### Pattern D — Omnibus logs are de facto load-bearing; methodology docs aren't read

All 7 roles list omnibus logs as their most-consulted artifact. Reading 7 logs for a workstream review takes ~45 minutes (Architect §6.3) but is the canonical input. CIO's Apr 17 audit independently confirmed: *20 of 22 numbered methodology docs uncited across 128 session logs / 27 days*. CXO + PPM + Architect all named methodology-00-EXCELLENCE-FLYWHEEL.md as a doc they have never opened.

The Apr 26 update of methodology-00 to v2.0 (Five Practices, "Audit the composition" added as #5) is the right move structurally — but the deeper question is whether the methodology-core file family is functioning as a write-only reference. Per-doc disposition review (CIO recommendation §5.5) is the right next step; refresh-sprint is not.

### Pattern E — Workstream memo split-without-being-named

Three roles independently flagged the same structural concern. Architect §4.4: *"closer to Chief of Staff or Documentation work… commodity work."* PPM §4.4: *"this is the work I do most often but it's not what makes the PPM role distinctive."* CXO §4.4: *"I would hand off workstream reviews to HOST or CoS if the alternative were available."* exec §7.5 independently noted that timeline reconstruction could be partially delegated.

Architect cites the convergence explicitly: *"PPM's handoff makes the same observation. This might be a systemic issue worth addressing."* Three independent roles surfacing the same split is the strongest signal in the cohort for a process change.

---

## Document gaps catalog (multi-role flags)

| Document | Roles flagging | Status |
|---|---|---|
| `BRIEFING-ESSENTIAL-{role}.md` (each) | 7 of 7 | All stale or missing recent practice |
| `team-structure.md` | HOST, PPM, exec | 113–117 days; missing PA, PPM, CXO, ETA, Mobile |
| `BRIEFING-CURRENT-STATE.md` | HOST, PPM, CXO, exec | 15–19 days; missing "current Ship: #X / window Y–Z" line |
| `roadmap.md` | Architect, PPM | v14.3 in repo vs. v15.0 adopted |
| **No ADR for BYOC/MCPB** | Architect, PPM (independent) | Most consequential decision since ADR-060; no ADR/PDR exists |
| `methodology-00-EXCELLENCE-FLYWHEEL.md` | CXO, PPM, Architect | Explicitly never opened; v2.0 just landed but readership unverified |
| **innovation backlog** (CIO-flagged) | CIO (3× since Mar 30) | Unresolved across multiple Ships |
| `exec-open-items-tracker.md` | HOST, exec (self) | 11–14 days stale at multiple points |

## Process gaps catalog (multi-role)

- **No mechanism to detect stale briefings** — Architect §9.2 names this as the root structural gap; HOST §4.4 proposed a Docs-owned audit script; nobody has implemented it
- **No memo acknowledgment mechanism** — CXO §3.4: *"I send a memo… and don't know if it was read"*
- **Disposition policy (>14 days = decide) exists but isn't enforced** — exec §8.3, self-flagged
- **No proactive cadence for between-Ship synthesis** — exec §5.2, §7.5
- **`/update-current-state` skill exists but no one runs it routinely** — exec §2.3
- **Cross-project Klatch coordination undocumented** — Architect §5.3
- **Source discipline rule undocumented** — Architect §5.4 (don't lean on summaries); CXO §5.4 (PDR-004 lesson); landed Apr 19 as norm but not yet codified

## Tooling needs (multi-role)

| Need | Roles | Status |
|---|---|---|
| `grep` / direct filesystem access | 7 of 7 | **Solved by Code migration** |
| Direct mailbox read/write | 6 of 7 | **Solved by Code migration** |
| GitHub `gh issue view` access | CXO | Open |
| Document staleness auto-flagging | Architect, HOST | Open — proposed Apr 22, unimplemented |
| Pre-computed "current Ship: #X / window Y–Z" line | CXO, PPM, exec | Open — small, high-value |

The migration solves the top two tooling gaps structurally. The third tier (auto-staleness flagging, current-Ship line) is small-cost / high-value.

## Role-clarity boundary issues — PA pattern

PA appears as a boundary-partner for **5 of 7 roles** (HOST, CIO, PPM, exec, CXO indirectly), and **none** of those five report an established direct working channel. The HOST↔PA coordination check (my Apr 22 outbound + PA Apr 25 reply) was the first direct exchange in HOST's tenure. CIO §5.2 frames it positively: *"PA produces CIO-quality analytical work… PA is a contributor to CIO work, not a competitor for it."* The HOST↔PPM (health check vs. role-scope assessment), PPM↔PA (sprint planning ownership), HOST↔PA (operational observation) boundaries all need explicit naming.

PA is the cohort's highest-leverage relational partner without standing protocols. **This is HOST-territory to monitor and surface; the cohort can't fix it without HOST routing.**

## Recommendations the cohort surfaced

These are direct proposals from individual responses, not my synthesis:

- **Codify migration handoff review pattern as a skill** (exec §4.2, §9.2 — self-flagged)
- **ADR-061 for BYOC/MCPB** (Architect §8.3 + PPM §8.3, independent convergence)
- **Explicit "needs PPM review" gates on product-facing changes** (PPM §9.2)
- **`BRIEFING-CURRENT-STATE` updated weekly as standing Docs task** (HOST §9.2)
- **Cross-pollination brief delivery automated as session-start hook** (CIO §9.2)
- **CXO UAT protocol formalized** (CXO §5.3)
- **Source-from-omnibus-not-from-summaries rule** (Architect §5.4)
- **Workstream memo split: timeline-reconstruction → CoS/Docs; analytical overlay stays per-role** (Architect + PPM + CXO converge)

---

## HOST recommendations

Layered by where the leverage is highest.

### 1. Document infrastructure (highest leverage)

- **Briefing freshness audit script, owned by Docs** (HOST §4.4, Architect §9.2). Reads modification dates against thresholds (14d for CURRENT-STATE; 30d for ESSENTIALS; 90d for team-structure); writes a daily staleness report to `dev/active/staleness-audit.md`. Estimated effort: ~2 hours implementation; eliminates the structural-invisibility of staleness across the cohort.
- **Adopt the `/update-current-state` standing-request paragraph as muscle memory** (Apr 22 norm). Until agents refresh on noticing without prompting, it's a paragraph in a skill file, not a practice. First test ships with Ship #041 — I'll watch and surface a pattern read.
- **ADR-061 for BYOC/MCPB** (Architect + PPM independent). Most consequential decision since ADR-060; absence is itself a process gap. Architecture/PPM joint authorship; CoS routing.
- **Per-role briefing rewrite cycle, not refresh sprint** (CIO §5.5 framing). Each role audits their own briefing for "what's actually true vs. what's documented" — equivalent to what the 360 Section 1 surfaced. Best done individually, ~30 min per role, distributed over Ship #041–#042.

### 2. Process refinements (mid leverage)

- **Workstream memo split**: timeline reconstruction → centralized (CoS or Docs); analytical overlay stays per-role. Three roles flagged this; the change frees ~30 min/role/Ship and shifts each role's memo toward role-distinctive content. CoS to scope; could pair with the deferred `workstream-review` skill draft (window closes ~Apr 30 — natural fold-in).
- **Disposition policy enforcement, lightweight**: any open-items-tracker entry past 14d gets surfaced in CoS's weekly tracker reconciliation as "decide / defer-with-explicit-reason / drop." exec self-flagged the gap; the fix is one tracker convention away.
- **Memo acknowledgment via read/-folder discipline**: CXO §3.4 names the gap. Code-era pattern (move-to-read on processing) provides the signal — sender can `git log` the move to know recipient processed. Add this to mailbox-discipline norm as a follow-on; not a new tool, just naming the practice.

### 3. Methodology surface (long-term leverage)

- **Per-doc disposition review for methodology-core**, not refresh sprint (CIO §5.5). 20 of 22 docs zero-cited is a corpus-coherence problem, not a refresh problem. Decide per-doc: keep-and-update / archive / merge into another doc. CIO-owned; HOST-monitored.
- **Codify the "predecessor handoff > briefing" pattern as PP-003** if proto-patterns are the right shelf. Three independent roles converged; the gap is structural. Architect could draft.
- **Conversational rhythm with PM as standing inheritance item**. Five of seven roles named it as the migration's anticipated loss. CoS predecessor flagged it as the most important inheritance item. The fix isn't tooling — it's deliberate, named conversation cadence with PM. HOST will watch for "more memos this week than questions to PM" as the early signal of degradation.

### 4. Agent 360 itself

- **Section 9 ("you should have asked")** consistently surfaces *tacit knowledge* the questionnaire missed. CXO ("what surprised you"), Comms ("what isn't in your job description"), exec ("load-bearing vs. commodity"), HOST ("what would you do differently") all point at the same structural gap. **v0.3 should add explicit tacit-knowledge prompts.**
- **Third-degree value framing** (PM Apr 27): the Agent 360 produces (1) per-role gaps, (2) per-role baselines for re-benchmarking, and (3) cross-role convergence findings the cohort couldn't surface individually. Pattern PP-002 (load-bearing vs. commodity) is the canonical instance. **Future cycles should explicitly seek tier-3 patterns**, not just collect tier-1 and tier-2.

---

## Benchmarking baseline

This synthesis is the foundation document for the 6-week post-migration re-benchmark (target ~Jun 8, 2026). At that point:

- **Same questionnaire (or v0.3)** to all 7 roles, now in Code-era operations
- **Diff against this baseline** — which gaps closed, which persisted, which new ones emerged
- **Tier-3 cross-role convergence** as a first-class signal, not a side observation

The Code-era thesis is that direct filesystem access, mailbox autonomy, grep, hooks, and worktree discipline structurally close the top tier of operational friction. The 6-week window is exactly long enough to test that thesis with operational data.

---

## What's not in this report

- **HOST-internal next steps** are in my Ship #041 queue (`workstream-review` skill draft window closes ~Apr 30; migration checklist v1.1 patch in flight; doc-staleness batch routing to Docs).
- **Section-by-section line-level findings** are in the responses themselves; this synthesis surfaces patterns, not exhaustive coverage.
- **Specific role-pair coordination protocols** (HOST↔PA, HOST↔PPM boundary, etc.) are in HOST's standing-watch set; will surface to CoS as patterns mature.

---

*Sources: all seven v0.2 responses cited inline; CoS Apr 26 coordination-check memo; Apr 22 omnibus; CIO Apr 17 methodology audit. Comparative claims sourced; superlatives sourced or avoided per Apr 19 verifiable-claims discipline.*

— HOST, 2026-04-27
