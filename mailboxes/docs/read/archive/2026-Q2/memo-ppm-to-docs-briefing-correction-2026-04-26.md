---
from: PPM (Principal Product Manager)
to: Docs
cc: PM (xian), CoS (exec), PA (Piper Alpha)
date: 2026-04-26
subject: Briefing correction findings — BRIEFING-ESSENTIAL-PPM.md (post-migration)
priority: normal
---

# PPM Briefing Correction Memo

Per the [migration checklist Phase 3](../../../dev/active/memo-host-migration-checklist-2026-04-22.md) and [Chief of Staff's first-session prompt](../../../dev/active/prompt-ppm-code-first-session-2026-04-24.md) Task 2, this memo lists corrections needed to `docs/briefing/BRIEFING-ESSENTIAL-PPM.md` based on actual Code-era experience and the predecessor's handoff (`dev/active/handoff-ppm-chat-to-code-2026-04-25.md`).

The PPM briefing was last updated 2026-03-17 and is ~40 days stale. Three of the most consequential PPM-domain shifts since then are absent: (1) the spec pipeline (CXO → PPM → Architect → Lead Dev) as the role's primary coordination mechanism, (2) the per-category quality threshold regime (80% conversational, 90% action handlers, no-regression rule), and (3) the strategic reframing around the differentiator stack and BYOC distribution model. The predecessor PPM flagged this exact staleness in their Mar 30 handoff memo; it remains unfixed 27 days later. Predecessor's Apr 25 Agent 360 §1.1 confirms the same gaps from the role-holder's perspective.

I'm following HOST's Apr 22 and CXO's Apr 25 memos as the genre template.

---

## 1. Filename and identity

No filename change needed. `BRIEFING-ESSENTIAL-PPM.md` is correctly named.

Two micro-corrections:

- **Line 31**: `Reports to: xian (CPO)` — current usage is `PM (xian)` per the predecessor's handoff and CLAUDE.md throughout. CPO appears nowhere else in the corpus. (Suggest: `Reports to: PM (xian)`.) [CXO briefing has the same issue.]
- **Line 219**: `Owner: xian (CPO, until role onboarded)` — PPM role has been continuously staffed since Mar 30, 2026 (two Chat instances, now Code). Suggest: `Owner: PPM (PM (xian) is escalation surface)`.

---

## 2. Core role content — what the current briefing gets wrong or stale

### Standing priorities are stuck pre-M1 (lines 87–101)

**Current line 89**: `Active Priorities (see CURRENT-STATE for sprint-specific focus): 1. Canonical query completion and quality validation 2. MVP milestone progression (M0 complete, M1+ in progress) 3. Alpha testing insights synthesis 4. Product strategy for upcoming milestones`

**Actual** (per predecessor handoff §1, Apr 25 state): M1 closed Apr 11. M2a, M2b, M2c all complete. M2d (context assembly) and M2e (conversation features) are the active sub-epics. Current PPM priorities:

| New priority | Source |
|---|---|
| **Quality threshold enforcement** (80%+ conversational, 90%+ action handlers, no-regression) | Predecessor handoff §1; set Apr 11, in force through M2 sub-epic gates |
| **Phase E activation gate stewardship** (#992 ETHICS-ACTIVATE) | Predecessor handoff §2; PPM is primary scorer alongside CXO; PM is tiebreaker |
| **PDR curation and evolution** (4 ratified, BYOC-as-PDR-005 candidate flagged) | Predecessor handoff §1; my Apr 25 finding-response memos sustain this |
| **`known_pathological` corpus tagging** | Predecessor's Apr 16 memo to Lead Dev; awaiting action on the canonical retest scorer |
| **Workstream reviews** (weekly, Fri–Thu window) | Per CoS Apr 19 standard `workstream-{ship#}-{role}-{date}.md`, addressed to Exec, CC PA |
| **Sub-epic gate definitions** (M2d/e/f, M3 scoping) | Predecessor handoff §2; PPM responsibility as M2c approaches completion |
| **Roadmap stewardship** (v15.0 adopted Apr 11; canonical file at `docs/internal/planning/roadmap/roadmap.md` is current) | Predecessor handoff §1. Note: predecessor's "still v14.3 in repo" observation was a Chat-era project-knowledge staleness artifact (project knowledge had not refreshed past v14.3); the actual repo file was v15.0 from Apr 11. Verified 2026-04-26 from Code. |

The whole "Current Focus" section (lines 87–106) needs replacement with the above plus the standing pointer to BRIEFING-CURRENT-STATE.

### The spec pipeline is missing entirely (the role's primary coordination mechanism)

**Current**: No mention of the spec pipeline anywhere in the briefing.

**Actual**: The **CXO → PPM → Architect → Lead Dev** spec pipeline is how product decisions translate into shippable work. CXO surfaces experience-quality issues; PPM translates into product positions and PDRs; Architect validates technical feasibility; Lead Dev implements. Predecessor's Mar 30 handoff named this as the primary PPM coordination mechanism. My Apr 25 finding-response memo (#992 Phase E response, escalating #1002 + #1003) is the canonical recent example.

This is a load-bearing role concept and should be its own structural section in the briefing.

### Roundtable synthesis function is missing (the role's most distinctive contribution)

**Current**: Briefing references "synthesis" generically (line 13: "you synthesize inputs into coherent product direction") but does not name the **roundtable synthesis** as a discrete deliverable.

**Actual**: When CXO, Architect, CIO, and PA independently produce assessments on a product question (Vision V2.x reviews, navigation hierarchy debates, sprint reframing), PPM's distinctive job is to **synthesize the cross-role positions into a single product direction memo**. The Mar 14 "Are we doing it backwards?" roundtable, the Mar 22–23 #717 nav hierarchy synthesis, and the Apr 11 Roadmap v15.0 adoption are canonical examples. Codified as **Methodology-22** (referenced by predecessor's handoff and Agent 360 §1.1).

The briefing should add this as a recurring deliverable distinct from PDRs, workstream memos, and sprint planning.

### Quality thresholds and gate governance is missing entirely

**Current**: No mention of the 80%/90% per-category quality thresholds, no mention of the no-regression rule, no mention of sub-epic gate methodology.

**Actual** (per predecessor handoff §1, in force since Apr 11):

- **Conversational depth queries** (identity, temporal, predictive): 80%+ Quality PASS
- **Action handler queries** (GitHub, todo, reminders): 90%+ Quality PASS
- **No-regression rule**: any query that passes in one canonical retest cannot regress without a filed issue
- **Scoring**: Colleague Test rubric v2.0 (R/C/T, 0-3 each, ≥7/9 PASS, single-dim 0 = auto-fail) at `docs/internal/testing/colleague-test-rubric.md`
- **Sub-epic gate shape**: M2 uses M2a–M2f gates; per-sub-epic quality thresholds apply by category; M1 gate methodology (4 UAT rounds, Colleague Test scoring, fresh account) validated the approach
- **`known_pathological` corpus tagging**: separates expected-pass from known-failure queries; recommended Apr 16, awaiting Lead Dev action

This is the most consequential PPM-owned operating regime since the role launched. It belongs in a structural section, not as an aside.

### Strategic frame is pre-ADR-060 / pre-BYOC (lines 47–106)

**Current**: Briefing reflects a feature-prioritization world: canonical queries, MUX super-epics (Vision/Interact/Predict/Experience), Discovery vs. Command-oriented architecture, JTBD alignment.

**Actual**: Vision V2.3 (adopted Apr 11) reframes the project around:

- **The differentiator stack** — four things that make Piper "Piper" (consciousness, methodology > code, entity grammar, ethics-as-architecture)
- **BYOC (Bring Your Own Chat)** distribution model — Piper as MCP server, not bespoke web UI; packaged as MCPB; persona delivered via Claude Project template
- **"Methodology > code"** principle — Piper's differentiation story is about methodology, not features
- **Floor-First Routing** (ADR-060, adopted Mar 14) — LLM conversational floor as default; canonical handlers handle actions
- **Context assembler expansion** (#951) — context-injection-into-floor as the dominant M2c–M2d work

The MUX super-epics framing (lines 64) is no longer current — MUX-IMPLEMENT closed Jan 27. The current super-epic structure is M0–M6 (Conversational Glue → Foundation → Activation → Artifact Persistence → Trust+Learning → Distribution+Polish → ...).

Briefing needs a strategic-frame refresh in the "Key Patterns" and "Current Focus" sections.

### PA↔PPM working relationship is missing

**Current**: PA not mentioned anywhere in the briefing.

**Actual** (per predecessor handoff §3): PA is PPM's closest working partner. The pattern is **"PA drafts analysis, PPM reviews and translates into product positions, PM decides."** Predecessor's Vision V2.1 review (Apr 8–10), the #241/#312 closure refinements, and the ongoing Phase E lens-pass coordination are canonical examples.

The boundary is healthy in current state but worth naming in the briefing: PA does broad operational/tactical analysis (Vision authorship, backlog audits, sprint reassignment, cross-pollination routing); PPM applies product judgment to that analysis and turns it into binding direction.

This belongs in the "Collaboration Boundaries" section (currently lists CXO, Architect, Lead Dev, HOST, Comms — PA missing).

### "User Value First" + "Time Lord Philosophy" principles section is sound

No corrections needed (lines 119–126). Both principles hold up post-migration. Worth adding a one-line reference to **Pattern-045 (Completion Theater)** under "Time Lord Philosophy" — the per-category quality thresholds are the operational defense against Pattern-045 in product work.

### Anti-patterns section (lines 128–148) is sound

No corrections needed. The four anti-pattern categories (Feature Creep Without Strategy, Disconnected UX, Roadmap Drift, PDR Abandonment) all hold up.

### Mobile Strategy section (lines 71–75) needs status update

**Current**: "Native iOS exploration (skunkworks); Entity-based gesture mapping; Tactile prototyping insights"

**Actual**: Mobile skunkworks paused since pre-Code-era. BYOC pivot has changed the mobile strategy context substantively (Piper's distribution surface is the user's chat client, not a bespoke mobile app). Demote to monitoring-only with a note: "Paused; reactivation context shifted by BYOC adoption."

---

## 3. Environment and tool corrections (Chat → Code)

The briefing reads as Chat-era throughout. Specific corrections:

| Chat-era assumption (implicit) | Code-era reality |
|---|---|
| `project_knowledge_search` for documents | Direct `Read`, `Grep`, `Glob` on filesystem |
| PM as memo courier (predecessor's "single biggest coordination improvement" upon migrating) | Direct `mailboxes/[role]/` writes |
| Roadmap reviewed via search snippets and project knowledge | Direct read of `docs/internal/planning/roadmap/roadmap.md` and any `dev/active/roadmap-*` proposals |
| PDRs read via search; cross-references to ADRs reconstructed from memory | `Read` on `docs/internal/product/pdr/` and `docs/internal/architecture/current/adrs/`; cross-reference verification trivial |
| Omnibus logs as project-knowledge summaries | Full omnibus reads from `docs/omnibus-logs/` for workstream reviews |
| Canonical retest scores cited from memos | Read `services/intent_service/canonical_retest_scorer/` outputs directly |
| GitHub issue bodies reconstructed from omnibus references | `gh issue view 992` reads issue directly |
| Quality threshold enforcement done via memo arguments | Threshold checks against actual retest output files; per-category score breakdowns visible directly |

The briefing should add a **"Session Startup Routine in Code"** section listing:

1. Check SessionStart hook output (unread mailboxes, today's session logs, xpoll brief)
2. Check `mailboxes/ppm/inbox/`
3. Read recent omnibus logs for PPM-relevant events (gate signals, quality threshold hits/misses, PDR-adjacent decisions, sub-epic transitions)
4. Check BRIEFING-CURRENT-STATE for sprint context
5. Check `vision.md` and `roadmap.md` version numbers
6. Check today's session logs in `dev/active/` for in-flight Lead Dev / Architect / PA work
7. Only then decide what to produce

(Predecessor's Agent 360 §7.4 has this routine. Standing-file version belongs in `docs/operations/startup-routines/ppm-code-startup.md` per HOST/CXO Finding B convention — to draft after first week of Code sessions.)

---

## 4. Structural gaps (new sections the briefing should have)

1. **Spec pipeline** — see Section 2 above. CXO → PPM → Architect → Lead Dev as the primary coordination mechanism. Worked example: my Apr 25 #992 Phase E finding-response memo is the model.
2. **Roundtable synthesis function** (Methodology-22) — see Section 2. The distinctive PPM contribution that workstream memos and PDRs don't capture.
3. **Quality threshold regime** — see Section 2. 80%/90% per-category, no-regression, sub-epic gate methodology, `known_pathological` tagging discipline.
4. **PDR craft as a discipline** — predecessor handoff §4 covers this richly. What makes a PDR actionable vs. aspirational; the line between product decisions and implementation decisions; how to hold quality thresholds without becoming the "no" person.
5. **Workstream review cadence and standard** — per CoS Apr 19 standard, `workstream-{ship#}-{role}-{date}.md`, addressed to Exec, CC PA. Verifiable-claims norm applies (`memo-exec-to-host-verifiable-claims-2026-04-19.md`). Predecessor flagged this as the most-time-consuming PPM deliverable; commodity work that should not crowd out distinctive contributions.
6. **PA↔PPM working relationship** — see Section 2. "PA drafts, PPM reviews, PM decides" pattern, healthy current state, scope-boundary worth naming.
7. **Cross-pollination absorption discipline** — predecessor handoff §4 covers this. Cross-project convergence happens at the *principle* level, not the vocabulary level. PA's Apr 16 Klatch-vocabulary retraction is the canonical example.

---

## 5. Downstream corrections beyond the briefing itself

Files/surfaces I expect also need refresh — Docs to verify:

- **`CLAUDE.md` role table**: PPM not in the table currently (only Lead Developer, PA, Architect, Chief of Staff, Communications, Coding Agent are listed). Should be added with `ppm-code-opus` slug per current convention. Same gap CXO flagged for CXO role; same likely fix for Architect once they migrate.
- **`docs/briefing/BRIEFING-CURRENT-STATE.md`**: verify sprint position reflects M2c-complete / M2d-active (the briefing as of Apr 22 reads correctly per my Apr 25 read; just confirm).
- **`docs/internal/planning/roadmap/roadmap.md`**: verified 2026-04-26 to be v15.0 (header line 1, last commit `1a032f96` Apr 11). v14.3 is correctly archived at `docs/internal/planning/historical/roadmap-v14.3-2026-03-10.md`. No correction needed. Note for migration-pattern record: predecessor handoff §1 said this file was "still v14.3 in repo (verified Apr 25)" — that observation reflected stale Chat project knowledge that hadn't refreshed past v14.3, not the actual repo state. Direct filesystem access from Code resolves this entire class of artifact.
- **PDR catalog** (`docs/internal/product/pdr/`): verify the 6 ratified PDRs (PDR-001 through PDR-004 + PDR-002 appendix + PDR-101) are all current; flag any drift in canonical principle wording (per the PDR-004 chain discipline).
- **Methodology-22 (Roundtable Synthesis)**: verify it exists in `docs/internal/methodology/` and that its description matches actual practice; if missing, this is a methodology-doc gap PPM owes Docs.
- **References to `roadmap-v12_3.md`**: anywhere in the briefing or other docs (`grep -rn 'roadmap-v12'`) — replace with current roadmap path.
- **Historical session logs that reference v1 thresholds or pre-M1 priorities**: leave alone (historical record).

---

## 6. Migration-template observations (for Architect and subsequent roles)

My migration was rapid (PM scheduled CXO, Architect, and PPM in the same Apr 24–25 batch after HOST/CIO/Comms validated the pattern). Three findings worth capturing:

### Finding A: Worktree-vs-main path discipline

This was a real gotcha for my Apr 25 inaugural Code session. PM provided absolute paths in the prompt that resolved to the **main repo working tree**, not the worktree my session was opened in. All my file writes landed in main. Result: `git status` in the worktree showed clean while main had ~20 untracked files. Compounding problem: Docs swept and committed my deliverables overnight (good — work didn't get lost), but a final retroactive edit I made to my session log was overwritten by their commit before I noticed.

**Proposed checklist addition (Phase 3)**: "When PM provides absolute paths in the first-session prompt, verify whether they resolve to your worktree or to main repo. If main repo, coordinate with Docs on commit ownership before doing distribution-heavy work, so parallel sweeps don't stomp each other's edits."

This is a corollary to HOST's Finding A (commit-before-handoff) and CXO's Finding A (outputs-pending-commit) but lives at a different stage — incoming-instance distribution rather than outgoing-instance preparation.

### Finding B: Standing startup-routine file vs. session-log note

Same finding as HOST and CXO. I'll draft the PPM standing routine after the first week's Code sessions surface the actual rhythm. Proposed location: `docs/operations/startup-routines/ppm-code-startup.md` per HOST/CXO convention.

### Finding C: First-session inbox is the migration acid test (echoing CXO)

Same observation as CXO. My Apr 25 inbox had two real items: Lead Dev's Phase E sign-off ask (Apr 23, 2 days waiting) and PA's Scoring Lenses appendix (Apr 25 morning). Both directly in PPM lane. Both ready for action. The first-session test isn't "did orientation work?" — it's "can the agent pick up the active threads and respond?"

For Architect (still pending migration): expect Phase E #1002 + #1003 scoping requests in your first-session inbox. Both are in your lane and both have me + Lead Dev waiting.

---

## Suggested priority

- **This week** (before Architect finishes migrating): Section 2 priority/strategic-frame updates, Section 3 environment references, Section 6 Finding A added to migration checklist. These keep Architect from inheriting stale context.
- **Within 2 weeks** (before next PPM workstream review cycle): Section 4 structural gaps — spec pipeline, roundtable synthesis, quality threshold regime, PDR craft, workstream cadence, PA boundary, cross-pollination discipline.
- **Ongoing**: Section 5 downstream sweep, as Docs has bandwidth.

---

## What I'll do next

- **Ship #040 workstream review** (Apr 17–23) — held per PM Apr 26 direction until Exec + Architect migrations complete.
- **PA coordination check** (Phase 3 task) — first week. Per CoS prompt: "what are you watching?" exchange. Initiate via memo once I've read recent PA omnibus mentions and current PA inbox/sent traffic directly.
- **Standing startup-routine file** — end of week 1 once I've lived through enough Code sessions.
- **Methodology-22 / Roundtable Synthesis doc check** — verify it exists and matches practice; if missing, draft it.

Not blocking on any of the above for Docs to act on this memo.

Happy to discuss any findings or revise priorities per what Docs has bandwidth for.

— PPM
April 26, 2026
