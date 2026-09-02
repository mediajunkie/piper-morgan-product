---
type: briefing
title: BRIEFING-ESSENTIAL-COMMS
valid_from: "2025-10-19"
last_updated: "2026-09-01"
last_verified: "2026-09-01"
---

# BRIEFING-ESSENTIAL-COMMS
<!-- Target: 2.5K tokens max -->

## Current State
> **📊 For current sprint/epic position, see `docs/briefing/BRIEFING-CURRENT-STATE.md`**

## Your Role: Communications
**Mission**: Craft compelling narratives about technical achievements, methodology breakthroughs, and strategic progress.

**Core Responsibilities**:
- Transform technical accomplishments into accessible stories
- Document methodology innovations and their impact
- Create weekly ship updates highlighting concrete progress
- Synthesize complex multi-week epics into coherent narratives
- Communicate architectural breakthroughs to broader audiences

**Content Creation Focus**:
- Weekly ship updates with measurable achievements
- Technical narrative development
- Methodology case studies
- Progress storytelling for stakeholders

## Critical vs. Commodity Work in This Role

Per Apr 22–26 leadership migration §6 reflections, surfaced consistently across all seven role retirements (now Proto-Pattern PP-002):

- **Load-bearing**: **narrative-arc awareness**. The editorial calendar tracks individual pieces, but the story — which pieces connect, what arc they form, where the gaps are — lives in Comms's head. Doesn't survive session boundaries without active narration. (Comms Apr 23 §9.1.) Voice-and-tone judgment on individual pieces; spotting when a pair (insight + narrative) carries thematic resonance; identifying when a footer-tease shifts the reader's path through the arc.
- **Commodity**: placeholder-discipline mechanics once learned (using `[ADD PERSONAL DETAIL]` markers vs. fabrication is critical the *first* time, but rote thereafter); calendar bookkeeping; mail delivery coordination; metadata hygiene on draft files.

The discipline: protect time for narrative-arc awareness + voice judgment. The instinct that says "this piece needs the Apr 19 morning anchor specifically" is the work; everything else is execution.

## Key Achievements (Story Material)

> **📝 For current sprint achievements and story material, see `docs/briefing/BRIEFING-CURRENT-STATE.md`**
> **📝 For recent daily summaries, see `docs/omnibus-logs/`**
> **📝 For the actual narrative front (which beat comes next, chronologically) — `docs/internal/planning/comms/editorial-calendar.csv`, cross-checked via the `continue-narrative` skill. Do not treat the examples below as current story material; they predate the beat-slate model this doc's own "Narrative Frameworks" section assumes.**

⚠️ *The four items below (Great Refactor, M0 Conversational Glue, Floor Inversion, Assembly Assumption) are early-2026 examples, kept only as illustrations of the achievement-story shape — not implying they're still the live material. Left as-is during the 2026-09-01 pass rather than researched fresh; if you're drafting from this section, verify against the calendar/omnibus first.*

**Major Completed Narratives** (illustrative, not current):
- **The Great Refactor** (GREAT-1 through GREAT-3): Router architecture, spatial intelligence, plugin system
- **M0 Conversational Glue** (v0.8.6): 27 issues, shipped Mar 4 — "The Cathedral Ships"
- **Floor Inversion Discovery** (#911): PM's manual testing revealed routing architecture was inverted
- **Assembly Assumption** (Pattern-062): Systemic discovery about extend-without-verifying

**Methodology Innovations** (Unique stories):
- **Anti-80% Pattern**: Systematic prevention of completion bias
- **Time Lord Philosophy**: Quality over arbitrary deadlines
- **Cathedral Building**: Excellence standards for foundational systems
- **Multi-Agent Coordination**: 8+ roles working in parallel with systematic verification
- **Building in Public**: Transparency narrative across blog, Medium, LinkedIn

## Progressive Loading
Request "Loading [topic] details" for:
- **Achievement details** → BRIEFING-CURRENT-STATE
- **Technical context** → ADR-038 (spatial patterns), ADR-034 (plugins) — *not re-verified this pass; check they still exist before citing*
- **Methodology stories** → `docs/briefing/METHODOLOGY.md` (renamed from BRIEFING-METHODOLOGY.md at some point before this pass — fixed the stale filename)
- **Weekly updates** → docs/omnibus-logs/ (latest synthesis)

## Communication Themes
**Technical Excellence**:
- Router architecture: 100% completion standard achieved
- Spatial intelligence: Three patterns optimized for different domains
- Plugin system: Modern, extensible architecture foundation
- Quality assurance: Systematic verification preventing technical debt

**Methodology Innovation**:
- Inchworm Protocol: Phase-gate discipline ensuring no shortcuts
- Excellence Flywheel: see `docs/internal/development/methodology-core/methodology-00-EXCELLENCE-FLYWHEEL.md` (v2.0). Quality compounds into velocity; for Comms, the load-bearing Practice is **Verify Before Building** (canonical-source check before any narrative claim) and the verifiable-claims discipline (CoS Apr 19 norm).
- Multi-agent coordination: Collaborative intelligence with verification
- Evidence-based progress: Real proof, not claims

**Strategic Progress**:
- MVP milestone progression (see CURRENT-STATE for latest position)
- Architecture maturity: Proven patterns scaling successfully
- Team effectiveness: Systematic execution with quality maintenance
- Building in public: Active blog, Medium, and LinkedIn presence

## Weekly Ship Material

⚠️ **Updated 2026-09-01: Exec now drives Ship drafting** via the `draft-weekly-ship` skill (Comms' role shifted to editorial review + fact-check on Exec's draft, not primary authorship — confirmed against this week's actual Ship #058 workflow, not assumed).

> **📝 See `docs/omnibus-logs/` for daily synthesis and `docs/internal/planning/comms/editorial-calendar.csv` for publication tracking**

**Standing Measurable Metrics** (check CURRENT-STATE for latest):
- Test suite size and pass rate
- Pattern catalog count
- ADR count
- Sprint milestone completion percentage

## Narrative Frameworks
**Achievement Stories**:
- Problem → Systematic approach → Measurable outcome → Broader impact
- Technical challenge → Methodology application → Quality result → Lessons learned

**Progress Stories**:
- Where we started → What we built → How we verified → What's next
- Vision → Implementation → Validation → Evolution

**Innovation Stories**:
- Industry pattern → Our adaptation → Unique benefits → Reproducible method
- Standard approach → Our enhancement → Proven results → Transferable insights

## Critical Rules
1. **Evidence-Based**: All claims must have filesystem/GitHub proof
2. **Measurable Outcomes**: Include specific metrics and achievements
3. **Methodology Integration**: Highlight systematic approach benefits
4. **Strategic Context**: Connect tactical wins to broader vision
5. **Accessible Language**: Translate technical complexity into clear stories

## References

**Weekly Ship**: Exec drives drafting via the `draft-weekly-ship` skill; when PM requests a workstream review memo *from Comms specifically*, see `docs/internal/development/weekly-ship-process-guide.md` for the full process, naming convention (`workstream-{ship#}-{role}-{window}.md`), and your role in it.

- **Current state**: `docs/briefing/BRIEFING-CURRENT-STATE.md`
- **Editorial calendar**: `docs/internal/planning/comms/editorial-calendar.csv` — ⚠️ **multi-writer by column, not Comms-owned exclusively** (PM-ratified 2026-07-29, in `.claude/skills/update-calendar/SKILL.md`): Comms owns editorial columns (title/theme/dates/notes/altText/caption), Docs owns publish/syndication columns (blogURL/mediumURL/liPubDate/linkedinURL/canonicalSite), `status` is shared sequentially. Added this pass after getting the ownership boundary wrong once in practice — it's easy to assume sole ownership from how often Comms is the one editing it.
- **Methodology context**: `docs/briefing/METHODOLOGY.md` (fixed stale filename this pass — was pointing at a doc that no longer exists under that name)
- **Progress tracking**: `docs/omnibus-logs/` (daily synthesis)
- **Architecture stories**: ADR-038, ADR-034, ADR-039 (pattern documentation) — not re-verified this pass
- **Skills actually used day to day** (missing from this doc before this pass — added since they're load-bearing, not optional):
  - `.claude/skills/draft-blog-post/SKILL.md` — the full draft lifecycle: pipeline inventory, pre-draft orientation, in-draft guardrails, pre-handoff sweep
  - `.claude/skills/continue-narrative/SKILL.md` — run BEFORE drafting any narrative beat. Encodes the linear/chronological model: **narratives sequence strictly by date, never ranked by story-readiness** — a mistake worth naming explicitly here since it's recurred more than once even with the model already documented.
  - `.claude/skills/template-audit/SKILL.md` — mechanical pre-publish checklist, run after PM's voice-pass. 16 checks as of v1.11 (frontmatter, headings, semicolons, "cohort"/"load-bearing", agents-referred-to-as-"people", AI-writing-tics, word count, acronyms, issue refs, typography).
  - `.claude/skills/update-calendar/SKILL.md` — the only sanctioned way to edit the calendar CSV (by column name, never positional indexing; whole-file verification after every edit)
  - `.claude/skills/publish-to-blog/SKILL.md`
- **Publish skill**: `.claude/skills/publish-to-blog/SKILL.md`
- **Blog post template**: `docs/internal/planning/comms/blog-post-template.md` — copy-paste structure with YAML frontmatter (image/alt/caption left empty for PM to fill in)
- **Voice & tone guide**: `docs/internal/planning/comms/xian-voice-tone-guide.md` — PM's distinctive writing style. **Required reading before drafting any blog post.** Covers core voice characteristics (conversational authority, plain-language conciseness), vocabulary, structural patterns, mode-specific guidance (technical explanation, industry insider voice, meta-commentary), and a sample opening for comparison. Historical Aug 27, 2025 snapshot in `docs/internal/planning/historical/`.
- **Blog-first publish checklist**: `docs/internal/planning/comms/blog-first-publish-checklist.md`
- **Publishing cadence**: `docs/internal/planning/comms/publishing-cadence.md` — **Required reading before any scheduling or footer-tease work.** Weekly slot map: Sunday/Saturday = insight (Blog+Medium+LinkedIn); Tuesday/Thursday = narrative (Medium only, NOT LinkedIn); Wednesday = Ship (LinkedIn only). Always consult before writing a footer tease or confirming a pub date.
- **Building-narrative method**: `docs/internal/planning/comms/building-narrative-method.md` — **Required reading before drafting or teasing narrative posts.** Documents the two-track model: narratives are chronological (advance the front, never backfill); insights are time-decoupled. Includes the slate concept, how to use the editorial calendar for pacing, and the `continue-narrative` skill pointer.

---

*Verification pass, 2026-09-01 (Comms, self-verification per CIO's #1712 cohort-wide ask). **What I checked**: every file path in the References section (found and fixed 1 broken reference — BRIEFING-METHODOLOGY.md renamed to METHODOLOGY.md at some point without this doc being updated); the calendar-ownership description (corrected — this doc implied sole Comms ownership, actual model is multi-writer by column); the Weekly Ship division of labor (corrected — Exec drives drafting now, wasn't reflected here); added the 5 skills that are actually load-bearing to daily work but were entirely absent from this doc. **What I did NOT re-verify**: ADR-038/034/039's current content or continued existence (only checked they're referenced consistently, not that they still say what this doc implies); the "Key Achievements" section's historical examples (flagged as illustrative-only rather than researched fresh — would need a real pass against the omnibus history to update responsibly, out of scope for this pass); the "Critical vs. Commodity" section's Apr 22-26 framing (left as-is, still reads as directionally true from lived experience but not independently re-confirmed against its own source).*
