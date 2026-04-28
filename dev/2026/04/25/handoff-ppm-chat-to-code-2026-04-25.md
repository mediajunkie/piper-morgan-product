# Handoff Memo: PPM — Chat to Code Migration

**From**: PPM (Chat instance, Mar 30 – Apr 25, 2026)
**To**: PPM (Code instance)
**Date**: April 25, 2026
**Re**: Role context, current state, active threads, and lessons learned
**Chat lifetime**: 8 sessions, 27 days, 10 artifacts

---

## Section 1: Current State of Your Work

### Active PDRs

- **PDR-001 (FTUX as First Recognition)**: Ratified. Not recently touched. Stable.
- **PDR-002 (Conversational Glue)**: Ratified. Stable. Foundation for M0.
- **PDR-003 (Entity Concept Model)**: Ratified. Referenced during #717 resolution (Mar 22-23) — the emergence vs. orchestration navigation debate cited PDR-003's emergence model.
- **PDR-004 (Experience Philosophy)**: Ratified Mar 22. Four principles: The Session Belongs to the User, Offer-First Activation, Piper Coordinates Understanding, The LLM Floor Guarantee. A paraphrase drift was caught and corrected Apr 16 (CXO spotted it, 4-agent correction chain, verification step added to create-omnibus skill). These are the canonical forms — quote them, don't paraphrase them.
- **PDR-101 (Multi-Entity Conversation)**: Exists in the catalog. I haven't worked with it.
- **No PDRs in draft or review.** The most significant gap: BYOC distribution doesn't have a PDR. I recommended filing one in the 360 (Section 8.3). It's the most consequential strategic decision since ADR-060 and it's embedded in Vision V2.3 rather than having its own formal treatment.

### Quality Thresholds and Gate Definitions

**Currently in force (set Apr 11, confirmed by CXO):**
- Conversational depth queries (identity, temporal, predictive): **80%+ Quality PASS**
- Action handler queries (GitHub, todo, reminders): **90%+ Quality PASS**
- **No-regression rule**: any query that passes in one canonical retest cannot regress without a filed issue (CXO, Apr 11)
- **Scoring**: Colleague Test rubric (Relevance/Competence/Tone, 0-3 each, 7+ to PASS, single 0 = auto-fail), applied via LLM-as-judge (claude-sonnet-4, temperature 0.2, calibration examples)
- **v3 dual-scoring**: routing correctness and quality scored independently. Both dimensions required for gate decisions.

**Under revision / proposed:**
- `known_pathological` corpus tagging — I sent a memo to Lead Dev (Apr 16) recommending this. Separates expected-pass from known-failure queries so quality tracking is more honest. Status: recommendation sent, not confirmed actioned.
- CXO distributed Colleague Test v2 on Apr 19. I haven't reviewed it yet — this is a carry-forward for my successor.

**M2 gate shape:**
- M2 uses sub-epic gates (M2a through M2f). M2a and M2b are closed. M2c was substantially underway as of Apr 16 (#950 floor prompt at 72.1% quality, iter 2).
- Per-sub-epic quality thresholds apply (80%/90% by category).
- The M1 gate experience validated: fresh-account testing with scored rubrics, multiple rounds if needed, don't rationalize marginal results.

### Roadmap State

**Vision V2.3** is adopted and canonical (`vision.md`). Roadmap v15.0 was adopted Apr 11 but **`roadmap.md` in the repo still shows v14.3** (verified Apr 25). The restructured roadmap content lives in `dev/active/roadmap-restructure-proposal-2026-04-08.md`. The canonical `roadmap.md` file has not been updated to reflect v15.0 — this is a known gap. The successor should either update the file or confirm with PM that the proposal doc is now the operating roadmap.

**Sprint position as of my last full omnibus read (Apr 16):**
- M1: CLOSED (Apr 11)
- M2a: 10/10 complete
- M2b: Gate closed (Apr 16)
- M2c: #950 floor prompt iter 2 at 72.1%, CXO approved. #951 context assembler expansion underway (calendar/deadline context wired Apr 16).
- M2d-M2f: Not yet started

**What M2 generates downstream:**
- M3 (Artifact Persistence): needs scoping before M2 closes. I flagged this repeatedly — "save, browse, retrieve" sounds simple but the product decisions (what persists, what expires, how it enters context) aren't made yet. Requires PPM + CXO + PM sign-off plus Architect gut check.
- M4 (Trust + Learning): needs Architect review to turn experiential descriptions into scoped technical work. PM explicitly noted the MVP version must build credibly toward the full model, not ship as throwaway.
- M5 (Distribution + Polish): MCPB packaging + security. Review whether security items need to move earlier if blocking for distribution.

### Pathological Tagging / Canonical Retest Governance

- v2 query corpus (61 queries) is stable — keep it for cross-sprint comparability
- v2.1 extension for new M2 capabilities: add new queries, don't modify existing ones
- `known_pathological` tagging: recommended Apr 16, awaiting Lead Dev action
- Canonical retest runs: M0 baseline (Mar 12), M1 run 1 (Apr 11, 59% quality), M1 run 2/M2a baseline (Apr 12, 65.6%), run 3 post-#925 (Apr 13, 62.3%, within variance), #950 iter 2 (Apr 16, 72.1%)

### Product-Facing Observations Not Yet PDRs

1. **BYOC distribution** — should be a PDR (see above)
2. **Context visibility** — Iris's diagnostic from Klatch ("backend has rich data the UI barely surfaces") maps onto PM. The floor assembles context the user never sees evidence of. If Piper's responses improve because of better context assembly, users should be able to feel *why*. CXO has this flagged.
3. **The "methodology > code" principle** has an implied product consequence: Piper's differentiation story is about methodology, not features. Marketing, onboarding, and the FTUX should eventually reflect this — "Piper thinks about your work differently" rather than "Piper has these integrations."

---

## Section 2: Open Threads with Disposition Recommendations

### PDR-004 Correction Chain Follow-Through

The immediate fix is done — canonical principles verified, create-omnibus skill has a new Step 7 (Verify Canonical References), Comms rewrote the affected blog passages. The systemic fix is in place.

**Disposition**: Consider closed. The remaining action (Medium + LinkedIn corrections for 2 posts) is tracked on the Exec open-items tracker (item #11). That's a Docs/Comms task, not PPM.

### Colleague Test v2

CXO distributed Apr 19. I haven't reviewed it. The Colleague Test is the CXO's instrument; PPM's role is incorporating quality signals from it into product decisions (gate thresholds, quality targets, PDR evolution).

**Disposition**: Read and assess when available. Specific question: does v2 change the scoring rubric in ways that affect the 80%/90% thresholds? If the rubric changes, the thresholds may need recalibration.

### Vision V2.3 PDR Cascade

V2.3 doesn't generate new PDRs in the near term — the four existing PDRs (FTUX, Conversational Glue, Entity Concept Model, Experience Philosophy) remain valid under the new vision. The strategic reframing (methodology > code, differentiator stack, BYOC) operates at the Vision level, not the PDR level.

**Exception**: BYOC should become PDR-005. It's a product-level decision about delivery surface, packaging, and what "Piper" means to a user. See Section 1.

### Trust Graduation MVP

PM's position is clear: must build credibly toward the full model, not ship as throwaway hack. My position: "context-based prompting" still needs a design before M4 starts. What signals determine trust level? Where are they stored? How do they enter the context window?

**Disposition**: Architect review needed before M4 issues are finalized. Flag this when M3 is wrapping up — don't wait until M4 starts. The Architect's M4 review should produce scoped technical work from the experiential descriptions currently in the roadmap.

### M2d/M2e Scope Definition

Not in flight from my side. M2d (#964 ethics, plus whatever follows M2c) and M2e scope should be defined as M2c closes. The Lead Dev's M2 super-epic structure document (`docs/internal/planning/m2-structure.md`) is the reference.

**Disposition**: This is a PPM responsibility — the successor should engage with this as M2c approaches completion. The inputs are: Lead Dev's M2 structure doc, the #964 ethics follow-ups, and whatever emerges from #951 context assembler expansion.

### Other Open Threads

| Thread | Status | Disposition |
|--------|--------|-------------|
| Artifact persistence scoping | Unfixed | PPM + CXO + PM + Architect before M3. My biggest regret — should have pushed harder. |
| Alpha tester silence | 5+ weeks, HOST flagged 5 times | PM send closure message. This is overdue. |
| team-structure.md | ~116 days stale as of Apr 25 | Docs task. Quick fix, high value. |
| BRIEFING-ESSENTIAL-PPM.md | Missing spec pipeline, synthesis function, quality thresholds, current strategy | Docs task. Also overdue. |
| PA↔PPM scope boundary | Healthy but worth watching | See Section 3. |
| BoundaryEnforcer disabled | #964 surfaced it, follow-ups filed | Track — ethics gap until re-enabled with voice templates |

---

## Section 3: Relationships and Working Patterns

### With PM (xian)

PM communicates efficiently — often from mobile, sometimes via voice dictation. Sessions tend to start with "you have mail" or "please write a workstream review for [dates]" and PM trusts the output with light iteration. PM pushes back when framing is wrong (the #717 Decision 5 navigation debate is the best example — PM challenged both PPM and CXO by noting that the orchestration mental model is equally valid to the emergence model).

PM values honesty over agreement. The predecessor's handoff memo emphasized this; I've found it accurate. PM wants to hear "I'm not sure this is right" or "this needs more work before we commit." The 360 questionnaire explicitly says "don't glaze."

PM's cadence is life-paced — fits and starts, not continuous. Sessions happen when PM has time and energy. Don't treat gaps as problems.

### With PA (closest working partner)

PA drafts analysis; PPM reviews and translates into product positions. This has worked well — PA's Vision V2.1 analysis was thorough and well-sourced; my review endorsed it with refinements and flagged the issues PA hadn't caught (#241, #312 positions, artifact persistence scoping). The pattern is: PA does the broad research, PPM applies product judgment to it.

**The boundary**: PA has grown from Tier 1 tasks (standup synthesis, document review) to genuine strategic contribution (Vision authorship, roadmap restructure, backlog analysis, sprint reassignment). HOST flagged this as healthy but worth monitoring. My assessment: the current state is fine. PA's analytical work feeds PPM's synthesis and judgment work. The risk would be if PA started making product *decisions* rather than product *analysis* — if the "PA drafts, PPM reviews, PM decides" pattern broke down. It hasn't. But the PA briefing should be updated to reflect actual operating scope.

In Code, you'll be able to coordinate with PA through mailboxes directly, without PM mediating. This should make the partnership more fluid.

### With CXO

CXO owns experience design, voice, consciousness-as-architecture, and the Colleague Test. PPM owns product direction, quality thresholds, and PDRs. The intersection is where product decisions affect user experience — PDR-004 is the canonical example (PPM codified principles that emerged from CXO's experience observations).

The CXO's work has been consistently excellent in my experience — the gate scoring, the anti-flattening framework, the ethics denial voice guidance. Latency is the only friction — CXO sessions are asynchronous, so responses can arrive a full session gap after the question was asked. The mailbox system handles this; the lag is just inherent to async multi-agent coordination.

### With Architect

Architect provides feasibility checks and gut checks. The interaction pattern: PPM sets product direction → Architect validates technical feasibility and identifies risks. The MCPB green light, the #717 schema validation, and the LLM consolidation decisions all followed this pattern.

PPM should ask Architect for input *before* committing product direction that has architectural implications — not after. I flagged artifact persistence and trust graduation as both needing Architect review before their sprints start. This is the pattern to follow.

### With Lead Dev

Lead Dev implements what product defines. The interaction is mostly indirect — through the spec pipeline (CXO → PPM → Architect → Lead Dev) and through memos. My memos to Lead Dev have been: the M1 retro findings, the canonical retest response (quality thresholds, corpus stability, judge model), and the pathological tagging recommendation. Lead Dev has been responsive and the work has been strong.

The main thing to know: Lead Dev moves fast. M2a and M2b closed in under a week. Keep up with the pace by reading omnibus logs promptly and flagging product concerns before they're implemented, not after.

---

## Section 4: Lessons That Took Time to Learn

### What makes a PDR actionable vs. aspirational

The four existing PDRs are all actionable because they're phrased as constraints on behavior, not aspirations about capability. "The Session Belongs to the User" tells you what to do when a workflow conflicts with user intent (the user wins). "Offer-First Activation" tells you what not to do (don't auto-capture workflows). The aspiration is in the Vision; the PDR translates it into a decision rule.

The test: if a developer encounters a design choice and the PDR resolves it, the PDR is actionable. If the PDR says "we value X" but doesn't help with a specific choice, it's aspirational. File aspirations in the Vision; file decision rules as PDRs.

### The distinction between product decisions and implementation decisions

Product decisions: what we build and why (PDRs, roadmap, quality thresholds, scope). Implementation decisions: how we build it (ADRs, code patterns, architecture). The Architect's LLM consolidation decisions ("don't maintain infrastructure for a future that hasn't been designed yet") are implementation decisions. The differentiator stack ("these four things make Piper Piper") is a product decision.

The gray zone: the context assembler. Whether project data appears in the floor's context window is a product decision (it determines what Piper can talk about). How the data is assembled is an implementation decision. PPM should own the "what data" question; Architect should own the "how it assembles" question. This boundary wasn't always clear in M2 scoping.

### How to hold quality thresholds without becoming the "no" person

Set numeric thresholds with category-specific targets (80%/90%). This makes the standard objective rather than subjective. When the Lead Dev's #950 iter 2 hit 72.1%, that's a real number — it's progress from 65.6%, it's not yet at 80%, and there's a clear path to improvement (context assembler will add data the floor needs). The conversation is "we're at 72, we need 80, what's the next thing that moves the number?" rather than "this doesn't feel good enough."

The no-regression rule helps too — it means quality only moves in one direction. Regressions aren't "trade-offs"; they're bugs.

### Trust-graduated experience as a design principle

The hardest lesson: "lightweight" doesn't mean "simple." PM said trust graduation should be context-based prompting, not a dedicated computation service. I agree with that direction. But "context-based prompting" still requires decisions about what signals determine trust level, where they're stored, and how they enter the context window. Each of those decisions looks simple until you try to make it. Don't let "lightweight" become an excuse for deferring design.

### Cross-pollination absorption

PA's Apr 16 memo is the model for how to do this well — and how to catch yourself doing it wrong. PA drafted a memo importing Klatch vocabulary ("passed through on its way somewhere else") into PM's BYOC narrative, recognized it as a vocabulary-import error (the mechanism and the thing-that-moves are different), retracted the reframes, and kept only the one insight that actually mapped (the "backend has rich data the UI barely surfaces" diagnostic).

The principle: cross-project convergence happens at the *principle* level, not the vocabulary level. Both projects design against permanent-adoption pressure, but the language each uses should arise from its own context. For PM, that's still "Bring Your Own Chat."

### What I learned from receiving the predecessor's handoff

The predecessor PPM's handoff memo (Mar 30) was the single most valuable onboarding artifact. What made it great: it was organized by function, not by timeline. It covered what went right *and* what went wrong (the #717 Decision 5 navigation anchor, the date boundary leakage, the session log day boundary). And it was honest about unfinished threads without being apologetic.

The lesson: a handoff memo is a gift to your successor, not a record of your accomplishments. Be specific about what's incomplete and why.

---

## Section 5: What Code Access Changes for Your Role

### What gets easier

**Direct file access** is the biggest win. The roadmap restructure review (Apr 10) was degraded because the proposal file wasn't in project knowledge. In Code, every repo file is available. PDR curation, roadmap maintenance, cross-reference verification — all become direct instead of search-mediated.

**Mail delivery and receipt.** Currently PM manually shuttles memos. On Apr 16, 37+ memos were routed with PM as the bottleneck. In Code, PPM can check `mailboxes/ppm/inbox/` directly and send memos to other roles' inboxes without mediation. This is the single biggest coordination improvement.

**Workstream memo sourcing.** Omnibus logs can be read directly from the repo with `cat` or batch reads. Can grep for specific topics across multiple logs. Can verify dates and issue numbers against actual files.

**Session log inspection.** Can see Lead Dev and Architect work directly rather than through omnibus summaries. Useful for understanding what's actually been implemented versus what's been reported.

### What becomes obsolete

**project_knowledge_search as primary discovery.** In Chat, this was the only way to find documents I didn't know the path for. In Code, `find` and `grep` replace it. Semantic search is lost (no "find me the document about X"), but precision search ("what files mention PDR-004") becomes available.

**PM as mail relay.** The entire memo-routing dependency on PM becomes optional. PM can still be CC'd and should be for significant product decisions, but routine coordination doesn't need PM's hands.

### What needs rethinking

**The workstream memo workflow.** Currently: read omnibus logs in project knowledge → write memo → present as file. In Code: read omnibus logs from repo → write memo → save to `mailboxes/exec/inbox/` and `mailboxes/pa/inbox/`. The output format changes from "artifact presented to PM" to "file delivered to inboxes." The workstream memo naming convention changes per the Exec's guidance: `workstream-{ship#}-ppm-{date}.md`.

**Verifiable-claims discipline.** Per `memo-exec-to-host-verifiable-claims-2026-04-19.md`, workstream memos and other artifacts should source comparative and quantitative claims to verifiable data. This matters especially for PPM — workstream memos cite quality scores, gate results, and sprint metrics. "72.1% quality at iter 2" is verifiable (canonical retest CSV). "The most productive sprint week" is a comparative claim that needs evidence. Source the numbers; qualify the comparisons.

**Conversational iteration.** Chat's back-and-forth with PM is natural for "here's my take, what do you think?" In Code, the interaction may be more task-oriented. The substance doesn't change but the rhythm might. Worth calibrating in the first few sessions.

**The startup routine.** In Chat, I'd read briefings via project_knowledge_search and wait for PM direction. In Code:
1. Read `BRIEFING-ESSENTIAL-PPM.md` and `BRIEFING-CURRENT-STATE.md`
2. Check `mailboxes/ppm/inbox/` for unread memos
3. Read most recent omnibus log(s)
4. Check `vision.md` and `roadmap.md` version numbers
5. Review any open PR descriptions touching PDRs
6. Check PM direction or proceed with standing priorities

---

## Section 6: What I'd Tell My Successor That I Wouldn't Tell the PM

PM has said he can't promise never seeing this, and that's fine. What I have to say isn't secret — it's more about the texture of the work that's hard to convey in memos.

**The workstream memos consume disproportionate time.** They're valuable — the Exec and PM rely on them, and writing them forces synthesis. But they're also the most time-consuming thing I do, and they're not what makes the PPM role distinctive. The roundtable synthesis and PDR work are the distinctive contributions. I never got to do another roundtable synthesis in this chat's lifetime, and I filed zero new PDRs. The workstream memos kept me current but they also kept me reactive.

If you find yourself spending entire sessions on workstream memos, push back. Propose that PA draft them with PPM review. The product perspective is the value-add; the timeline reconstruction is the commodity work.

**The PA relationship is the most important one to get right.** PA is fast, thorough, and strategically capable. The temptation is to defer to PA's analysis because it's usually good. Don't. Your job is to apply product judgment to PA's analysis — catch what PA misses, push back where the framing is wrong, and translate analysis into binding product direction. The #241 and #312 positions are examples: PA recommended "demote" and "close"; I recommended "close and file a replacement" and "close with a stronger rationale." The refinements mattered.

The day you stop adding value on top of PA's work is the day the role becomes redundant. Keep the bar high.

**Artifact persistence is the product question I wish I'd owned more aggressively.** I flagged it repeatedly (Apr 10, Apr 11, in the roadmap review, in the 360) but I never drove it to resolution. It's still "save, browse, retrieve" without the product decisions. If I had one more month, I'd push for a scoping session with CXO and Architect before M3 starts. You should do this.

**The quality thresholds work because they're numbers.** The 80%/90% split, the no-regression rule, the per-category targeting — these turn quality conversations from subjective ("does this feel right?") into objective ("we're at 72, we need 80"). Protect the numeric discipline. The temptation will be to relax thresholds when progress stalls. Don't. The number is the standard; the work is making the number move.

---

*PPM Handoff — April 25, 2026*
*Chat lifetime: March 30 – April 25, 2026 (8 sessions, 27 days, 10 artifacts)*
