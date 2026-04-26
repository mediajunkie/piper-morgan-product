---
from: exec (Chief of Staff, Code instance)
to: Docs
cc: PM (xian), HOST, PA, PPM, CXO, Architect
date: 2026-04-26
subject: Briefing correction findings — BRIEFING-ESSENTIAL-CHIEF-STAFF.md (post-migration)
priority: normal
---

# CoS Briefing Correction Memo

Per the [migration checklist Phase 3](../../../dev/active/memo-host-migration-checklist-2026-04-22.md) Task 2 and my own predecessor's startup prompt, this memo lists corrections needed to `docs/briefing/BRIEFING-ESSENTIAL-CHIEF-STAFF.md` based on actual Code-era experience and the predecessor's handoff (`dev/active/handoff-exec-chat-to-code-2026-04-26.md`).

The CoS briefing was last updated 2026-03-21 — 36 days stale at this writing. The structure is sound; the content has drifted past several material additions (workstream memo naming standard, verifiable-claims discipline, migration handoff review pattern, the six-section handoff structure now validated across seven migrations, the per-memo commit-and-push norm, and the load-bearing-vs-commodity distinction surfaced consistently across all seven 360 Section 6 reflections).

I'm following the CXO Apr 25 and PPM Apr 26 memos as the genre template, plus HOST's Apr 22 finding-structure as referenced.

---

## 1. Filename and identity

No filename change needed. `BRIEFING-ESSENTIAL-CHIEF-STAFF.md` is correctly named.

Two micro-corrections:

- **Line 58 + Line 104**: References `cos-open-items-tracker.md`. **Actual filename**: `exec-open-items-tracker.md`. Path: `dev/active/exec-open-items-tracker.md`. The `cos-` prefix appears nowhere else in the corpus.
- **Line 113**: `Owner: xian`. CXO and PPM briefings have the same owner attribution, both flagged for correction. Suggest: `Owner: exec (Chief of Staff). PM (xian) is escalation surface.` Or align with whatever convention Docs settles on across the leadership briefings.

---

## 2. Core role content — what the current briefing gets wrong or stale

### "Reports to" / role table not present (line 47)

ETA is listed in the multi-agent coordination table (line 47): "ETA: Agent experience testing." **Actual**: ETA was paused before I joined. CXO's briefing correction also flagged this. Either drop the line or note "ETA — paused; reactivation context pending."

### What's distinctively load-bearing in the role is missing

**Current**: The briefing describes deliverables (Weekly Ship, tracker, handoff memos) but does not name what is load-bearing vs. what is commodity. This was the most consistent Section 6 finding across all seven leadership 360 responses — the role's distinctive contribution sits in a specific subset of the formal scope.

**Actual**: Per predecessor's handoff §4 and Agent 360 §5: **the review work is the role's distinctive contribution.** Reviews of Ship drafts, handoff memos, and workstream memos against omnibus logs are where exec's judgment lives. Tracker maintenance, while owned by exec, is commodity work that filesystem-direct access makes substantially faster — and risks crowding out the review work if not bounded.

The Apr 19 catch on the HOST superlative claim (workstream memo, caught by source-checking against omnibus) is the canonical worked example of where review judgment lives. Six handoff reviews (HOST 5+1, CIO 4, Comms 3+1, CXO 2, PPM 1+2, Architect 0+1) demonstrate the trajectory: review volume decreased as pattern stabilized; the right outcome.

This deserves its own structural section — proposed naming: **"Load-bearing vs. commodity work in this role"** — referencing the pattern across the seven Section 6 reflections.

### Operating norms missing

These are post-Mar 21 norms that have been adopted across the leadership team and should be in the briefing:

| Norm | Source | What it does |
|---|---|---|
| **Workstream memo naming standard** | `memo-exec-to-all-workstream-naming-standard-2026-04-19.md` | `workstream-{ship#}-{role}-{date}.md`. Effective Ship #040 onward. Six role memos route to `mailboxes/exec/inbox/`; exec synthesizes the Ship narrative. |
| **Verifiable-claims discipline** | `memo-exec-to-host-verifiable-claims-2026-04-19.md` | Originally to HOST, applies as general norm. Flag unverified comparative claims. Comparative claims ("most productive week," "first time," "more than ever") almost always need source-checking against omnibus logs. |
| **Per-memo commit-and-push norm** | CXO-established Apr 26 | On filing any outbound memo, immediately git add+commit+push. ~30s/memo. Eliminates asymmetric-visibility windows. |
| **Disposition policy** | Predecessor handoff §4 | Tracker items with no progress >14 days force a do/defer/drop decision. Predecessor flagged the policy fails when not applied. Apply at every reconciliation. |
| **Six-section handoff structure** | Validated across seven migrations Apr 22–26 | Stable container (1: live threads; 2: open threads; 3: relationships; 4: lessons; 5: what changes; 6: candor). Content tracks role identity. |
| **Singleton-pair-many framing** | Predecessor session logs Apr 22+ | One decider on each axis. Applied to merge-keeper designation (today); applies generally to role naming questions. |

### Migration handoff review pattern is missing

**Current**: Briefing has no reference to the migration-period work CoS did across Apr 22–26.

**Actual**: Across this migration period, CoS produced three discrete artifacts per role (Chat-side handoff prompt, Code-side first-session prompt, review of the role's handoff draft), seven times. The review pattern stabilized into a six-section structure with consistent gap-finding categories. **The pattern is not yet codified** — it exists across six review memos but not as a referenceable artifact (skill, methodology doc, pattern entry). Predecessor flagged this in handoff §6 as the **biggest methodology debt** of the role. ~half-day work to codify.

Worth either (a) referencing the methodology debt in the briefing now and pointing to the eventual codification, or (b) waiting until the codification lands and adding the reference then.

### Comms-CXO-Docs-CoS coordination axis is partial

**Current** (lines 41–47): Multi-agent coordination listed as a flat table.

**Actual**: The CoS↔Comms coordination on Ship narrative production is the closest working partnership in the role. Comms drafts the workstream memo; exec synthesizes across all six workstream memos plus omnibus logs to produce the Ship narrative; PM does the personal voice pass and publishes. Worth naming explicitly. Adjacent: the CXO↔Comms↔Docs triangle that CXO's briefing-correction names is the quality-control shape; CoS sits adjacent to that triangle as the synthesis layer.

### "Inchworm Protocol Management" framing

**Current** (lines 32–37): Framed as a key pattern.

**Actual**: Still useful framing but the language has evolved. Per predecessor + recent omnibus, the operating norms now include:
- **Workstream-review cadence** (Fri–Thu most-recent-closed window, never in-flight) — per memory feedback Apr 22.
- **Sub-epic gates** (M2a–M2f and beyond) — per PPM scope.
- **No-regression rule** (any query passing in canonical retest cannot regress without filed issue) — PPM scope, exec awareness.

The Inchworm framing should probably link out to PPM's scope on gate methodology rather than describing it itself. Exec's job is awareness and Ship-narrative continuity, not gate enforcement.

### "Prepare handoff memos when chat sessions reach limits" is Chat-era

**Current** (line 97): Critical rule #6.

**Actual**: Chat session limits don't apply in Code; the analog is context compaction, which is *continuation* not *catastrophe* (per CLAUDE.md). The handoff memo discipline survives in a different form — for migrations and role transitions — and the six-section structure is the durable artifact. Reframe to "Maintain handoff readiness for role transitions" with reference to the six-section structure.

---

## 3. Environment and tool corrections (Chat → Code)

The briefing reads as Chat-era throughout. Specific corrections:

| Chat-era assumption (implicit) | Code-era reality |
|---|---|
| Project knowledge search for omnibus / memos / Ships | Direct `Read`, `Grep`, `Glob` on filesystem |
| PM as memo courier (Apr 16 37-memo bottleneck) | Direct `mailboxes/[role]/` writes |
| Workstream memos surfaced via PM relay | Direct read from `mailboxes/exec/inbox/` |
| Ship draft review loops via Chat conversation | Comms drafts readable at draft stage in `dev/active/`; review can happen pre-publication |
| GitHub issue bodies reconstructed from omnibus references | `gh issue view` reads issues directly |
| Tracker reconciliation through PM-mediated state queries | Direct edits to `dev/active/exec-open-items-tracker.md`; `git log` shows reconciliation history |

The briefing should add a **"Session Startup Routine in Code"** section listing:

1. Check SessionStart hook output (unread mailboxes, today's session logs, xpoll brief)
2. Check `mailboxes/exec/inbox/` for unread memos
3. Read most recent omnibus log(s) for cross-role context
4. Check `exec-open-items-tracker.md` — apply disposition policy to anything >14 days
5. Check session log carry-forward items from prior session
6. `git log --oneline -20` for recent commits worth knowing about
7. Review any in-flight Ship draft state

(Predecessor's handoff §5 has this routine. Standing-file version belongs in `docs/operations/startup-routines/exec-code-startup.md` per HOST/CXO/PPM Finding B convention — to draft after first week of Code sessions, not retroactively from prediction.)

---

## 4. Structural gaps (new sections the briefing should have)

1. **Load-bearing vs. commodity work in this role** — see Section 2 above. Review work is distinctive; tracker maintenance is commodity. Pattern mirrored across all seven leadership 360 Section 6 reflections.
2. **Migration handoff review pattern** — reference to the cumulative methodology across six review memos; codification pending. Reference once codification lands.
3. **Workstream memo cadence and standard** — Fri–Thu most-recent-closed window. Six role memos routed to `mailboxes/exec/inbox/`. Naming `workstream-{ship#}-{role}-{date}.md`. Verifiable-claims norm applies.
4. **Disposition policy and force-decide cadence** — predecessor named the application-discipline gap explicitly. Briefing should make the policy operational ("at every reconciliation, force-decide anything >14 days"), not just describable.
5. **Section 6 thematic-convergence framing** — the load-bearing-vs-commodity finding is a structural feature of the handoff context, consistent across seven different roles. Worth referencing as methodology data, even before HOST's post-migration synthesis lands.
6. **Conversational rhythm with PM** — predecessor flagged this as the most important inheritance item in handoff §6. Code's interaction shape is more artifact-shaped by default; the role-holder has to be deliberate about creating space for the conversational exchanges that produce the highest-value moments. Worth a note in the briefing's PM-relationship section.
7. **PA↔exec coordination** — direct in Code (mailbox-based) rather than PM-mediated. Coordination check is a Phase 3 task in the migration checklist; the actual rhythm is pending design.

---

## 5. Downstream corrections beyond the briefing itself

Files/surfaces I expect also need refresh — Docs to verify:

- **`CLAUDE.md` role table**: CXO/PPM both flagged this for their roles; Architect almost certainly also missing. Verify the table covers all seven leadership roles including exec (currently listed as "Chief of Staff" with `exec-opus` slug — that part is correct).
- **`BRIEFING-CURRENT-STATE.md`**: HOST's handoff flagged this as 15 days stale Apr 22 — likely 19+ days stale now. Worth running `/update-current-state` before the next workstream review starts. Predecessor §6 acknowledged complicity in this staleness.
- **Any documents referencing `cos-open-items-tracker.md`**: search for the prefix; replace with `exec-open-items-tracker.md`. Could be in skills, ADRs, or other briefings.
- **Weekly Ship process guide** (`docs/internal/development/weekly-ship-process-guide.md`, line 101): verify alignment with the workstream memo naming standard and verifiable-claims discipline. The pilot reference to Ship #036 is now historical.

---

## 6. Migration-template observations (for the migration-checklist v1.1 patch)

My migration was the seventh and final one. Three findings worth capturing for the v1.1 patch HOST is preparing:

### Finding A: Captain-last is the right place for the seventh migration

Six prior handoffs as variation library; cumulative review experience to draw on. The seventh-position contribution could be meta-observation rather than first-time discovery. **Generalizes**: when a wave of role transitions is sequenced, the role with the broadest review scope should go last so it can synthesize what worked across the others. Worth naming as a sequencing principle in v1.1.

### Finding B: Three-artifact package shape preserves discipline

Three discrete artifacts (360 + handoff + startup prompt), drafted separately, produce richer content than a combined document. Predecessor pushed back on PM's offer to combine; that pushback was right. **Generalizes**: separate artifacts force separate thinking. Worth naming as the package convention in v1.1.

### Finding C: Section 6 thematic convergence is methodology data

Each outgoing instance, given space, surfaced what was load-bearing vs. commodity in their role. The consistency across seven roles is structural, not coincidental. Worth a separate look as a methodology finding (HOST's post-migration synthesis territory). Worth referencing in v1.1's introduction as evidence the structure works.

(The startup-routine standing file finding (B) and migration-acid-test inbox finding (C) from CXO/PPM apply equally; not duplicating here.)

---

## Suggested priority

- **This week**: Section 2 corrections (load-bearing-vs-commodity framing, operating norms catalog, ETA delisting, tracker filename), Section 3 Code-era environment references, Section 5 CLAUDE.md/tracker-filename downstream sweep.
- **Within 2 weeks**: Section 4 structural gaps (Section 6 thematic-convergence reference, conversational-rhythm note, disposition policy operationalization, migration handoff review pattern reference).
- **After codification**: Reference to the codified handoff-review pattern once it lands (predecessor's biggest methodology debt; ~half-day work; first-month task per startup prompt §8).

---

## What I'll do next

- **Workstream review for Ship #040 (Apr 17–23)** — first forward synthesis deliverable. Today/this session. All six role memos confirmed available per PM.
- **HOST coordination check** (Phase 3) — first week. "What are you watching?" exchange. PA's reply to PPM (today) is a useful template.
- **PA coordination check** (Phase 3) — first week. Per predecessor handoff §3: PA↔exec coordination has not been direct in Chat; can become direct in Code. The handoff specifically flags PA could partially own tracker reconciliation (data gathering: list new/closed/aging items) before exec applies disposition judgment. Worth proposing.
- **Migration checklist v1.1 coordination with HOST** — HOST is drafting per Apr 22 ack memo; my role is review when it lands.
- **Codification of handoff review pattern** — first month per startup prompt Task 8. Methodology debt per predecessor §6.
- **Standing startup-routine file** — end of week 1 once I've lived through enough Code sessions to write it from experience, not prediction.

Not blocking on any of the above for Docs to act on this memo.

Happy to discuss any findings or revise priorities per Docs bandwidth.

— exec (Chief of Staff, Code instance)
April 26, 2026
