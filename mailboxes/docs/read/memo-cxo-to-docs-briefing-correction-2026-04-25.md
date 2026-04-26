---
from: CXO (Chief Experience Officer)
to: Docs
cc: PM (xian), CoS (exec), PA (Piper Alpha)
date: 2026-04-25
subject: Briefing correction findings — BRIEFING-ESSENTIAL-CXO.md (post-migration)
priority: normal
---

# CXO Briefing Correction Memo

Per the [migration checklist Phase 3](../../../dev/active/memo-host-migration-checklist-2026-04-22.md) and [Chief of Staff's first-session prompt](../../../dev/active/prompt-cxo-code-first-session-2026-04-24.md) Task 2, this memo lists corrections needed to `docs/briefing/BRIEFING-ESSENTIAL-CXO.md` based on actual Code-era experience and the predecessor's handoff (`dev/active/handoff-cxo-chat-to-code-2026-04-25.md`).

The CXO briefing is the freshest of the briefings (refreshed Mar 31 by Docs after a Ship #037 staleness finding). It does not need a global rewrite. It does need: (1) post-M1 priority updates, (2) Colleague Test v2 path correction, (3) Code-era tool references, and (4) the CXO↔Comms↔Docs triangle as a first-class concept.

I'm following HOST's Apr 22 memo structure as the genre template.

---

## 1. Filename and identity

No filename change needed. `BRIEFING-ESSENTIAL-CXO.md` is correctly named.

One micro-correction:
- **Line 35**: `Reports to: xian (CPO)` — current usage is `PM (xian)` per the predecessor's handoff and CLAUDE.md throughout. The CPO title appears nowhere else in the corpus. Either update the title or confirm CPO is intentional. (Suggest: `Reports to: PM (xian)`.)

---

## 2. Core role content — what the current briefing gets wrong or stale

### Standing priorities are stuck on M1 (line 147 and lines 144–152)

**Current line 147**: `M1 gate UAT — highest priority. 14 manual test scenarios (Gates 1+2). Fresh account, Colleague Test scoring.`

**Actual**: M1 gate closed Apr 11 (4 rounds of UAT, final score 7/9). We are in M2c. Current CXO priorities (per predecessor's handoff §2):

| New priority | Source |
|---|---|
| **ETHICS-ACTIVATE (#992) Phase E voice oversight** | Predecessor handoff §1; Phase E sign-off delivered today (`memo-cxo-to-lead-phase-e-sign-off-2026-04-25.md`) |
| **Floor quality monitoring (#950 retest scores)** | Currently 72.1% vs. 80% target; watch canonical retest after each M2c change |
| **Colleague Test v2 application** | v2 committed today to `docs/internal/testing/colleague-test-rubric.md` |
| **Workstream reviews (weekly, Fri–Thu window)** | Per CoS Apr 19 naming standard `workstream-{ship#}-{role}-{date}.md`, addressed to Exec, CC PA |
| **Mobile skunkworks oversight (paused)** | Demoted to monitoring; predecessor flags BYOC pivot has changed context |

The whole "Standing Priorities" list (lines 146–152) needs replacement with the above plus a pointer to BRIEFING-CURRENT-STATE for sprint-specific focus.

### Colleague Test path — points to non-canonical doc (lines 20, 58, 120, 138, 201)

**Current**: All five locations reference `docs/internal/development/colleague-test.md`.

**Actual**: As of 2026-04-25, the **canonical operational rubric is v2.0 at `docs/internal/testing/colleague-test-rubric.md`**. The development/ doc is the conceptual companion (philosophy, when-to-apply, worked PM examples) and now carries a v2-pointer header directing readers to the testing/ path for scoring.

Suggested briefing wording:

```
**Colleague Test (Primary Decision Heuristic)**: Operational rubric v2.0 at
`docs/internal/testing/colleague-test-rubric.md`. Conceptual companion at
`docs/internal/development/colleague-test.md`. Three-dimension scoring
(R/C/T, 0-3 each, ≥7/9 PASS, single-dim 0 = auto-fail). v2 adds the
Context 2-vs-3 distinction (generic LLM competence vs. project-context
injection) and decline-path scoring (used in #992 Phase E).
```

### CXO↔Comms↔Docs triangle is missing entirely

**Current** (line 41): "Communications Director - Experience narrative for public content" — the relationship is reduced to a one-line bullet under "Collaborates with."

**Actual**: Per CoS Apr 24 first-session prompt and predecessor handoff §3, the CXO↔Comms↔Docs triangle is the **single most-transformed coordination axis post-migration**. The discipline:

- **CXO detects** quality/voice drift (PDR-004 chain Apr 16 is the canonical example)
- **Docs traces propagation and builds systemic safeguards** (Step 7 in create-omnibus skill came from this chain)
- **Comms rewrites narrative passages** in already-published content
- All three are now in Code, eliminating the PM-mediated memo bottleneck

The briefing should add a structural section for this. The four-line bullet under "Collaborates with" is not adequate.

### "Express Investment, Not Emotion" applies to CXO itself, not just Piper

**Current** (line 158): Listed as PDR-004 principle, framed as a Piper voice rule.

**Actual** (per predecessor's successor-candor, handoff §6): The same principle applies to the CXO role. Show care through precision, attention, and honest scoring — not through declared feelings about progress. This isn't a separate principle to add; it's a reframing of the existing one to make it apply to the role-holder, not just to Piper. Worth a sentence in the operational guidance.

### Floor-First Routing principles need a "fabrication probe" companion (line 65)

**Current**: ADR-060 floor-first routing description is correct.

**Missing**: The fabrication-probe principle (predecessor Apr 16 recommendation to Architect): Context 0 (fabricated data) is the most dangerous failure mode and warrants its own dedicated instrument, separate from the Colleague Test. Both layers needed: prompt + Colleague Test catch consciousness; fabrication probe catches what the prompt can't prevent. This is canonical CXO position and should appear in the briefing's principles section.

### Active documents table (lines 130–139) needs path updates

| Current row | Correction |
|---|---|
| `colleague-test.md \| Active \| Colleague Test scoring rubric (3-dim, 7+ pass)` | Path: `docs/internal/testing/colleague-test-rubric.md` (v2.0). Note the testing/ path. |
| (missing) | Add: `docs/internal/development/colleague-test.md` as the conceptual companion (with v2 pointer header). |
| (missing) | Add: PDR-004 chain Step 7 in create-omnibus skill — canonical-verification discipline that originated from CXO and is now systemic. |

### Anti-patterns section (lines 163–183) is sound

No corrections needed. The four anti-pattern categories (Generic Pattern Matching, Disconnected from Product, Research Without Action, Re-Litigating Settled Decisions) all hold up post-migration.

---

## 3. Environment and tool corrections (Chat → Code)

The briefing reads as Chat-era throughout. Specific corrections:

| Chat-era assumption (implicit) | Code-era reality |
|---|---|
| Project knowledge search for documents | Direct `Read`, `Grep`, `Glob` on filesystem |
| PM as memo courier (PM ↔ Comms ↔ CXO loops) | Direct `mailboxes/[role]/` writes — eliminates the Apr 16 PM-bottleneck |
| Comms drafts reviewed only after publication or when PM forwards | **Comms drafts readable at draft stage** — CXO can read `dev/active/comms-*` and flag voice issues before publication |
| Floor prompt iterations described in memos | `git log services/intent_service/conversational_floor.py` shows actual prompt evolution |
| GitHub issue bodies reconstructed from omnibus references | `gh issue view 992` reads the issue directly |
| Colleague Test applied to responses PM pasted into Chat | Score directly from response text in repo (`grep`, `Read` on response logs) |
| Canonical retest scores summarized in memos | Read `services/intent_service/canonical_retest_scorer/` outputs directly |

The briefing should add a **"Session Startup Routine in Code"** section listing:

1. Check SessionStart hook output (unread mailboxes, today's session logs, xpoll brief)
2. Check `mailboxes/cxo/inbox/`
3. Scan recent omnibus logs for CXO-relevant events (voice drift, PDR/ADR drift, floor quality signals, ethics activation events)
4. Check BRIEFING-CURRENT-STATE for sprint context
5. Check today's session logs in `dev/active/` for in-flight Comms drafts and Lead Dev work
6. Only then decide what to produce

(Predecessor's Agent 360 §7.4 has a draft of this routine. The standing-file version belongs in `docs/operations/startup-routines/cxo-code-startup.md` or equivalent — see Section 6 Finding B below.)

---

## 4. Structural gaps (new sections the briefing should have)

1. **CXO↔Comms↔Docs triangle** — see Section 2 above. Distinct function per role; direct coordination through shared filesystem; the PDR-004 chain as the canonical model.
2. **Ethics decline voice oversight** — ongoing CXO responsibility per predecessor handoff. Review actual production decline responses when BoundaryEnforcer activates; ensure they pass Colleague Test at 7+, auto-fail on Tone 0 content-filter cadence.
3. **Floor quality monitoring discipline** — canonical retest scores after each M2c change. Watch for tone regressions. Flag anti-flattening capstone failures (the "express investment, not emotion" rule needs to hold as the prompt gets more complex).
4. **Verification-before-assertion discipline** — origin of the PDR-004 chain (Apr 16). Before citing any PDR/ADR/Pattern by principle name, open the canonical document. Now Step 7 in the create-omnibus skill, applies to every CXO memo.
5. **Workstream review cadence and standard** — weekly, Fri–Thu most-recent-closed window, role-scoped memo to Exec (CC PA), naming `workstream-{ship#}-{role}-{date}.md` per CoS Apr 19 standard. Verifiable-claims norm applies (`memo-exec-to-host-verifiable-claims-2026-04-19.md`).
6. **Calibration through use** — predecessor's lesson. The Colleague Test rubric only becomes calibrated when applied to real responses across multiple rounds. M1 UAT (4 rounds, 9 queries each) is the canonical example. Worked examples in v2 help; they don't substitute for practice.

---

## 5. Downstream corrections beyond the briefing itself

Files/surfaces I expect also need refresh — Docs to verify:

- **`CLAUDE.md` role table**: CXO not in the table currently (only Lead Developer, PA, Architect, Chief of Staff, Communications, Coding Agent are listed). If the project supports CXO sessions in Code, CXO should be added with `cxo-code-opus` or `cxo-opus` slug. Check with PM whether the omission is intentional.
- **`BRIEFING-CURRENT-STATE.md`**: verify M1 references are historical-only and current focus reflects M2c.
- **Any skills referencing `colleague-test.md` (development/ path)**: should point to v2 at testing/ path. `grep -rn colleague-test .claude/` would surface them.
- **Canonical retest scorer code (#928)**: verify rubric reference matches v2.0 wording, especially the path-type field and decline-path scoring rules. (I've already notified Lead Dev today: `memo-cxo-to-lead-ppm-colleague-test-v2-committed-2026-04-25.md`.)
- **PDR-004 references in other briefings**: verify they cite the source document, not a paraphrase (this is the correction-chain discipline).
- **Historical session logs that reference v1 of the rubric**: leave alone — historical record, not current documentation.

---

## 6. Migration-template observations (for Architect, PPM, and subsequent roles)

My migration was the smoothest of the four (CoS noted "lightest review across four migrations"). One operational finding worth capturing for future migrations:

### Finding A: Outputs-pending-commit before role retirement

The predecessor wrote Colleague Test v2 in Chat outputs on Apr 19 — six days before retirement — and it was never committed to the repo. The handoff correctly flagged it as "needs distribution" but on the day-of-migration the canonical scoring document Lead Dev's #928 scorer is calibrated against was still v1 in the repo.

Resolution: I reconstructed v2 from the predecessor's handoff specification (committed today). The reconstruction is honest about its provenance; if predecessor's Apr 19 draft surfaces and differs materially, we reconcile in v2.1.

**Proposed checklist addition (Phase 1 — outgoing Chat instance final week)**: "Verify all Chat-outputs deliverables are committed to repo before final session. Anything in `outputs/` not in the repo is invisible to the successor."

### Finding B: Standing startup-routine file vs. session-log note

Same finding as HOST's Apr 22 memo. I'll draft the CXO standing routine after the first week's Code sessions surface the actual rhythm, not retroactively from a Chat-era prediction. Proposed location: `docs/operations/startup-routines/cxo-code-startup.md` or wherever HOST and CIO put theirs.

### Finding C: First-session inbox is the migration acid test

I opened my Code inbox tonight to find a Phase E sign-off request from Lead Dev (Apr 23) and a Scoring Lenses appendix from PA (today). Both were directly in CXO lane and both had been waiting. The first-session test isn't "did orientation work?" — it's "can the agent pick up the active threads and respond?" If the inbox routes correctly and the handoff covers the threads, first-session productivity follows.

For Architect and PPM (still pending migration): expect inbox to be the test. If yours is empty on first session and you know there are threads in flight, escalate immediately — that's a routing failure, not a quiet week.

---

## Suggested priority

- **This week** (before Architect and PPM finish migrating): Section 2 priority/path updates, Section 3 environment references, Section 6 Finding A added to migration checklist. These keep the next two roles from inheriting stale context.
- **Within 2 weeks** (before next CXO workstream review cycle): Section 4 structural gaps — triangle section, ethics oversight, floor quality monitoring, verification-before-assertion.
- **Ongoing**: Section 5 downstream sweep, as Docs has bandwidth.

---

## What I'll do next

- **Ship #040 workstream review** (Apr 17–23 window) — first forward deliverable in new naming convention. Targeting next session.
- **Comms coordination check** — first week. Per CoS prompt: "what are you watching?" exchange. Will initiate via memo once I've read recent Comms drafts directly (now possible in Code).
- **Docs coordination check** — first week. Same pattern. The triangle conversation is overdue and the Code environment finally enables it without PM mediation.
- **Standing startup-routine file** — end of week 1 once I've lived through enough Code sessions to write it from experience, not prediction.

Not blocking on any of the above for Docs to act on this memo.

Happy to discuss any findings or revise priorities per what Docs has bandwidth for.

— CXO
April 25, 2026
