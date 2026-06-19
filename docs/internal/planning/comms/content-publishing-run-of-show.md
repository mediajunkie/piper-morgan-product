# Content Publishing Run of Show

**Status**: DRAFT — pending PM ratification
**Scope**: Building narratives and insights. Ships are simpler (see § Ships below).
**Ratified**: — (PM to confirm; discussion June 19, 2026)

---

## The 7-Step Sequence

| Step | Who | What | Output / Signal |
|------|-----|------|-----------------|
| 1 | **Comms** | Drafts from session logs / omnibus. Applies four-category opacity sweep, voice discipline, length targets. | Draft at `docs/public/comms/drafts/{slug}.md` |
| 2 | **PM** | Voice pass + edit/rewrite. | Revised draft; or **route back to Comms** if structural issues surface (see Revision Loop below) |
| 3 | **Comms** | Template + voice audit against `blog-post-template.md` and `xian-voice-tone-guide.md`. Fills footer teaser. | Publish-ready memo to Docs inbox (June 18 handoff protocol) |
| 4 | **PM** | Creates image (ChatGPT cartoon for narratives/insights). Fills frontmatter: `image:`, `alt:`, `caption:`. | Frontmatter populated in the draft |
| 5 | **Docs** | Final proof: template checklist + voice guide + ready-for-publication check. Confirms image frontmatter complete. | Verbal or memo go-ahead to PM; or routes back to Comms with specific flags |
| 6 | **Docs** | Runs `publish-to-blog` skill. Updates `editorial-calendar.csv` with blog URL + pubDate. | Post live at `pipermorgan.ai/blog/{slug}` |
| 7 | **Dispatch** | Syndicates to Medium (canonical link back to blog). Cross-posts to LinkedIn. Updates `editorial-calendar.csv` with Medium + LinkedIn URLs. | Calendar row complete; `canonicalSite: distributed` |

---

## Revision Loop

PM may stop mid–step 2 and route back to Comms if the draft has structural issues (opacity overcorrection, source errors, pacing problems). Comms revises and re-delivers. PM resumes the edit on the revised draft.

When routing back to Comms, PM or Docs names the specific issues — not a general "fix it." Time pressure applies: if pubDate is <2 days out, treat the revision as same-session urgent.

---

## Ships

Ships skip steps 1–4 as defined above:

1. Exec synthesizes the Ship draft (from week's session logs + context)
2. PM reviews / light edit
3. Docs final proof
4. Docs publishes + updates calendar
5. Dispatch publishes to LinkedIn newsletter + updates calendar

Ships currently have no image and no Medium syndication.

---

## Adjacent Docs

| Doc | Purpose |
|-----|---------|
| `blog-post-template.md` | Comms's drafting reference — opacity sweep, length targets, voice discipline |
| `xian-voice-tone-guide.md` | Voice / tone reference — used by Comms (step 3) and Docs (step 5) |
| `blog-first-publish-checklist.md` | Legacy PM-centric checklist (March 2026); superseded by this doc for multi-agent sessions |
| `publishing-workflow-target.md` | Blog-first infrastructure decision (March 2026); still accurate on infrastructure, not on role sequencing |
| `.claude/skills/publish-to-blog/SKILL.md` | Mechanical publish pipeline for step 6 |
| `editorial-calendar.csv` | Source of truth for scheduling, URLs, status |

---

*Drafted: 2026-06-19 (Docs). First formal documentation of multi-agent run-of-show. Ratification by PM pending.*
