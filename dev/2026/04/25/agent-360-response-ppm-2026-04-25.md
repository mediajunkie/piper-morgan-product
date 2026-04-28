---
from: PPM (Principal Product Manager)
to: HOST (Head of Sapient Trust)
date: 2026-04-25
subject: Agent 360 Response — Pre-Migration Baseline
---

# Agent 360 Response: PPM — Pre-Migration Baseline

**Sessions in this Chat project**: 8 (Mar 30 – Apr 25, 27 days)
**Artifacts produced**: 10 (4 workstream memos, 3 feedback memos, 1 M1 retro, 1 roadmap review, 1 pathological tagging recommendation)

---

## Section 1: Briefing & Orientation

**1.1** BRIEFING-ESSENTIAL-PPM.md is accurate in broad strokes but missing several things I relied on heavily:
- No mention of the spec pipeline (CXO → PPM → Architect → Lead Dev) — this is the role's primary coordination mechanism
- No mention of the roundtable synthesis function (Methodology-22) — the role's most distinctive contribution
- No mention of the Colleague Test, quality thresholds, or gate governance — became a major part of the work
- No reference to the differentiator stack or BYOC — the current product strategy
- The predecessor PPM flagged this exact staleness in the handoff memo (Mar 30). It's still unfixed 26 days later.

What's present but never useful: the section on general PM methodology. I never consulted it — the project-specific methodology docs and the predecessor handoff were far more valuable.

**1.2** My first session (Mar 30) was ~7 minutes — pure orientation, no real work. That's because the predecessor delivered a comprehensive handoff memo that covered everything. My second session (Apr 8, first real work session) took about 15 minutes of orientation before I was writing the workstream memo. Most of that time was reading omnibus logs, not figuring out what to do.

The predecessor handoff was the single most valuable onboarding artifact. It covered: role context, current state, active documents, proven patterns, mistakes to learn from, unfinished threads, and session history. Without it, orientation would have taken an entire session.

**1.3** A new instance with only the briefing docs would get wrong:
- The PA↔PPM working relationship — they'd treat PA as a separate entity rather than as the closest working partner who drafts analysis that PPM translates into product direction
- The quality thresholds — 80% conversational, 90% action handlers, no-regression rule. None of this is in the briefing.
- The current strategic frame — differentiator stack, BYOC, methodology > code. The briefing still reflects the pre-ADR-060 world.
- How workstream memos work — the coverage window convention, the theme recommendation, the date boundary discipline

---

## Section 2: Information Access

**2.1** The roadmap restructure proposal (`dev/active/roadmap-restructure-proposal-2026-04-08.md`) was not in project knowledge during my Apr 10 review. I had to work from omnibus logs and the vision doc instead. PA's memo told me to review a document I couldn't access. This is the most concrete example of the Chat project knowledge gap — files in the repo but not in the knowledge base.

**2.2** Most consulted: omnibus logs, by far. They're the primary source for workstream memos and for understanding what happened between my sessions. Easy to find by date, but project_knowledge_search sometimes misses recently uploaded files. Direct path reads (`/mnt/project/YYYY-MM-DD-omnibus-log.md`) are more reliable.

**2.3** team-structure.md — 103+ days stale, doesn't list PA, PPM, CXO, ETA, or Mobile. HOST flagged this repeatedly. It's worse than useless because it's actively misleading.

BRIEFING-ESSENTIAL-PPM.md — as noted in 1.1, missing the spec pipeline, roundtable synthesis, quality thresholds, and current strategy.

**2.4** "What Ship number is this?" — I check the predecessor's last memo every time. The Ship number should be derivable from the coverage window dates, but I always verify manually. A simple "current Ship: #039, next coverage window: Apr 10-16" note in BRIEFING-CURRENT-STATE would save this.

---

## Section 3: Handoffs & Coordination

**3.1** The predecessor PPM handoff (Mar 30) was excellent — the best handoff I've experienced. Comprehensive, honest about mistakes, specific about open threads. Nothing was missing.

The memos I've sent to Lead Dev and CXO have been actioned promptly when PM delivers mail. The bottleneck is mail delivery, not memo quality or recipient attention. PM manually shuttling memos between Chat and filesystem is the coordination constraint.

**3.2** CXO. Not because the CXO is unresponsive — the CXO's work has been excellent (gate scoring, anti-flattening framework, voice guidance). The difficulty is timing: CXO sessions happen asynchronously, and by the time their response arrives, I may be in a different session or the context has moved. The mailbox system works but the latency can be a full session gap.

**3.3** Not that I'm aware of. The PA↔PPM boundary has been clean in practice — PA drafts analysis, I review and translate into product positions. I haven't found myself duplicating PA's work or vice versa. The closest was the Vision V2.1 review, where PA's analysis and my review arrived at similar conclusions independently — but that's convergence, not duplication.

**3.4** Moderate confidence. Memos to Lead Dev and CXO have been actioned. But I sent the `known_pathological` tagging memo to Lead Dev on Apr 16 and don't have visibility into whether it was read. The mailbox system works; the visibility into receipt and action is the gap.

---

## Section 4: Role Clarity

**4.1** The M1 retrospective I wrote on Apr 11 felt like it belonged to HOST or Exec — it's an operational assessment of sprint health, not a product decision. I wrote it because it was needed in the moment and I had the context, but a formal retro is organizational health territory, not PPM territory.

**4.2** Workstream memos. The role definition emphasizes PDRs, roadmap management, and synthesis. Workstream memos are more like reporting — valuable, but they consume significant session time (reading 7 omnibus logs, synthesizing, writing). This is the work I do most often but it's not what makes the PPM role distinctive. The roundtable synthesis is the distinctive function; workstream memos are the recurring obligation.

**4.3** "Sprint planning" in a hands-on sense. PA and PM have been doing the actual sprint scoping and issue filing. My role has been reactive review (endorsing the roadmap restructure, setting quality thresholds) rather than proactive planning. This may be correct given PA's capability, but it's worth noting.

**4.4** Workstream memos could theoretically be drafted by PA (who reads the omnibus logs daily) with PPM review. This would free PPM sessions for the synthesis and PDR work that's actually distinctive. The risk is that the product perspective in the memo is the PPM value-add — PA might draft the facts but miss the product framing. Worth experimenting.

---

## Section 5: Methodology & Process

**5.1** Documents I actually use:
- Omnibus logs (daily source material)
- `session-log-instructions.md` (log format)
- Predecessor handoff memo (role context — referenced repeatedly early on)
- `BRIEFING-CURRENT-STATE.md` (sprint position)
- `roadmap.md` / `vision.md` (product frame)

**5.2** Documents I ignore:
- `methodology-00-EXCELLENCE-FLYWHEEL.md` — never opened it. The CIO methodology audit confirms zero citations in 128 files across 27 days. The concept is alive in practice; the document isn't consulted.
- Most of the methodology-NN series. I'm aware they exist but the role's methodology is embodied in the workstream memo pattern, the roundtable synthesis pattern, and the spec pipeline — none of which have dedicated methodology docs.

**5.3** The workstream memo pattern: read omnibus logs for coverage window, write theme recommendation, write product perspective with subsections per major development, include key metrics table, decisions table, risks section, forward look. This is well-established practice but I learned it from the predecessor's examples, not from a methodology doc.

**5.4** Rule I'd add: **"Verify coverage window boundaries before delivering a workstream memo."** The predecessor got burned by date leakage (including events outside the coverage window). I've been careful about this but it's not codified. A simple checklist item: "Every claim in this memo falls within [start date] – [end date]. Verify before sending."

---

## Section 6: Tools & Environment

**6.1** Direct filesystem access to the repo. This is the single biggest capability gap. I can't read files that aren't in project knowledge, I can't verify what's in a specific document without searching for it, and I can't check the current state of an issue or PR. The roadmap restructure review (Apr 10) was degraded because I couldn't access the actual proposal file. Code access fixes this.

**6.2** `project_knowledge_search` — I use it, but I've learned not to trust it for recently uploaded files. Direct path reads are more reliable. I don't use the web search tool — the role is entirely internal-facing.

**6.3** Most time-consuming: reading omnibus logs for workstream memos. Each log is substantial (100-130 lines), and the coverage window is typically 5-7 logs. This is irreducible reading — the logs are the source material. But in Code, I could potentially read them more efficiently (batch reads, grep for specific topics).

---

## Section 7: Migration-Specific

**7.1** What gets better:
- **Direct file access** — can read any repo file without waiting for project knowledge uploads. The roadmap restructure review gap disappears.
- **Mail delivery** — can check mailboxes directly, send memos directly to inbox paths. Eliminates the PM-mediation bottleneck.
- **Cross-reference verification** — can check PDR text against ADR text, verify canonical terms, trace provenance. The PDR-004 correction chain would have been caught earlier with direct access.
- **Workstream memo sourcing** — can read omnibus logs directly from the repo, potentially more efficiently.

**7.2** What gets harder or is lost:
- **Conversational iteration with PM** — Chat's back-and-forth is natural for "here's my take, what do you think?" exchanges. Code may feel more transactional.
- **project_knowledge_search convenience** — semantic search across all project docs is genuinely useful for "find me the document about X." Code's `find` and `grep` are precise but require knowing what you're looking for.
- **Artifact rendering** — less relevant for PPM (I produce markdown memos, not visual artifacts), but worth noting.
- **Session continuity feel** — Chat sessions have a conversational arc. Code sessions may feel more like discrete task execution.

**7.3** Hardest to reconstruct if lost:
- The product positions I've taken across sessions — the 80%/90% quality thresholds, the `known_pathological` recommendation, the #241/#312 closure rationale, the context assembler scoping concerns, the trust graduation credibility requirement. These are scattered across memos and conversation history, not in a single document.
- The M1 retrospective analysis — it was delivered conversationally on Apr 11, then captured in the feedback memo to PA/Lead Dev. The conversational version was richer.

**7.4** Ideal startup routine for Code:
1. Read `BRIEFING-ESSENTIAL-PPM.md` and `BRIEFING-CURRENT-STATE.md`
2. Check `mailboxes/ppm/inbox/` for unread memos
3. Read most recent omnibus log(s) since last session
4. Check `vision.md` and `roadmap.md` version numbers
5. Review any open PR descriptions touching PDRs or product-facing changes
6. Ask PM what's top of mind

**7.5** Chat-specific dependencies:
- PM's voice dictation — PM often speaks messages from mobile (Amtrak, transit). Chat handles this naturally. Code interactions may be more keyboard-oriented, which changes the rhythm.
- The "here's a memo, what do you think?" flow — PM uploads a document, I read it in context, respond conversationally. In Code, this becomes "read file at path X, respond in memo." Functionally the same but the interaction pattern is different.

---

## Section 8: PPM-Specific Questions

**8.1** Is the roadmap document a useful planning tool, or primarily historical record?

Both, but trending toward historical. Roadmap v15.0 was a structural rewrite that made it genuinely useful for understanding "what are we building and why" — the differentiator stack framing gives it real organizing power. But for day-to-day planning ("what's next in M2?"), the M2 super-epic structure doc and the sprint reassignment plan are more actionable. The roadmap is the "why"; the sprint structure is the "what."

The roadmap's planning value increases at sprint boundaries (M1→M2, M2→M3) and decreases during execution.

**8.2** When sprint scope changes mid-sprint, how do you track that?

Through omnibus logs and PA's issue filing. I don't have a dedicated scope-tracking mechanism. When M2a expanded or issues were filed mid-sprint, I learned about it from the next omnibus log or from a memo. This works but it's passive — I'm informed after the fact rather than consulted before. The "PA drafts, PPM reviews, PM decides" pattern is working for major scope changes, but smaller changes (Lead Dev filing a follow-up issue, Architect making a consolidation decision) happen without PPM input. This is probably correct — not everything needs product review — but the boundary of "what needs PPM sign-off" isn't explicit.

**8.3** What product decision is currently implicit that should be a PDR?

**The BYOC distribution model.** "Bring Your Own Chat" is the most consequential strategic decision since the floor inversion, and it's embedded in Vision V2.3 rather than having its own PDR. It determines: delivery surface (MCP server, not bespoke web UI), packaging (MCPB, per-platform), persona delivery (Claude Project template), and what "Piper" means to a user (tools and context in their existing client, not a separate application). This is PDR-level product direction — it should have the same formal treatment as PDR-001 (FTUX), PDR-002 (Conversational Glue), PDR-003 (Entity Concept Model), and PDR-004 (Experience Philosophy).

---

## Section 9: Open Response

**9.1** Question you should have asked: **"What product question do you wish you'd pushed harder on?"**

Answer: artifact persistence scope for M3. I flagged it in the roadmap review (Apr 10-11) as needing PPM + CXO + PM sign-off and Architect gut check. It still doesn't have a clear scope. "Save, browse, retrieve" sounds simple but the decisions about what persists, what expires, and how artifacts enter the context window are product decisions that determine whether M3 delivers a storage schema or an experience model. I should have pushed for a scoping session before the roadmap was adopted, not after.

**9.2** One thing I'd change: **Explicit "needs PPM review" gates on product-facing changes.** Right now, PPM review happens when PM routes a memo or when I notice something in an omnibus log. There's no systematic trigger for "this change affects the product experience and should have PPM input before shipping." The M2 quality thresholds are a step in this direction (they create numeric gates), but the broader question — which changes need product review — is still ad hoc.

**9.3** The predecessor PPM's handoff memo is the gold standard for role transitions. If every role migration produced a handoff of that quality, the project would lose significantly less context across transitions. The Exec's six-section template formalizes this, which is the right move.

---

## Plausibility Check

- [x] Section 1 (briefing gaps): specific observed friction — the roadmap file access gap and the missing briefing content are documented
- [x] Section 2 (information access): specific observed friction — roadmap file, team-structure staleness, Ship number lookup
- [x] Section 3 (coordination): specific observed — mail delivery bottleneck, CXO timing latency
- [x] Section 4 (role clarity): specific observed — retro scope question, workstream memo time allocation
- [x] Section 6 (tools): the filesystem access gap is the #1 Chat-specific limitation; Code migration directly addresses it
- [x] Section 8.3 (BYOC as PDR): theoretical concern elevated to recommendation — based on precedent (PDR-001 through PDR-004 each codified an implicit decision)
- [x] Most friction items are resolved by Code migration (filesystem access, mail delivery, cross-reference). Chat-specific items: project_knowledge_search convenience, conversational iteration rhythm.

---

*PPM Agent 360 Response — April 25, 2026*
*Pre-migration baseline*
