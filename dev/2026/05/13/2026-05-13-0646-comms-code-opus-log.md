# Communications Director Session Log

**Date**: May 13, 2026 (Wednesday)
**Start Time**: 6:46 AM ET
**Role**: Communications Director (Comms)
**Model**: Claude (Opus 4.7)
**Environment**: Claude Code (seventh Code session)
**Branch**: `main`

---

## Session Context

Two-day gap from May 11. PM ask for today: review the Weekly Ship #042 draft at `docs/public/comms/drafts/weekly-ship-042-draft-2026-05-10.md` for plain language. Specifically: would an intelligent layperson — someone who knows about AI but isn't fluent in our internal vocabulary — understand what the team did this past week? The lens: solipsistic language, jargon, idiolects (agent names, internal acronyms, internal process labels) all opaque to outside readers. Same general direction as the voice-guide-additions sitting at PROPOSED in the voice/tone guide.

If we figure out what works, formalize it.

PM is publishing today — review is urgent, not exploratory.

Voice-guide PROPOSED additions still pending PM voice-pass; deferred.

## ~6:50 AM — Ship #042 review (in progress)

Approach: deliver review in chat with diagnosis + spot-edits + sample rewrites of key passages. Let PM apply selectively in PM's working edit. Not modifying the canonical draft.

## ~7:00 AM — A/B plain-language pass

PM asked for full pass (option a) as alternative file + spot-check on length (Ships have been creeping; need punchier).

Length baseline pulled: Ship #036 was 124 lines / 1320 words; Ships #037–041 ran 136–158 lines / 2200–2500 words; current #042 draft 133 lines / 1831 words. Target for rewrite: ~1100–1300 words.

Plain version filed at `docs/public/comms/drafts/weekly-ship-042-draft-2026-05-10-plain.md` — 107 lines / 1252 words pre-blog-list addition. Commit `88aabf97`.

Four-category opacity sweep applied throughout:
- Agent role names as proper nouns → role functions (Lead Dev / Architect / PPM / CXO / HOST → developer / architecture role / product-management role / experience-design role / etc.)
- Internal acronyms (M2/M2d/M2e/M2f/M2g, MVP, BYOC, ADR, PDR, MUX, UAT) → expanded or replaced
- Issue numbers and commit hashes removed from narrative prose
- Gnomic self-references replaced ("the cohort was running the methodology fluently" → "the team's recent shipping pace"; "the catch caught itself" → "that same checklist caught a problem in its own quality rubric")

Sections compressed: learning-pattern dropped its five sub-sections to three paragraphs; resource-allocation percentage breakdown cut entirely; weekend reading dropped.

## ~7:07 AM — PM feedback: "big improvement, reads much more smoothly"

PM asked to add the weekly blog-post list per established format. Pulled May 2-7 publications (excluding Ship #041 itself per established pattern) from editorial-calendar.csv with full alt text + slugs + workDates. Added list + two featured-image options (Six Issues flywheel cartoon / A Hail of Memos hailstorm cartoon) to the plain version. Commit `9d365927`. Updated length: 120 lines / 1402 words.

## ~7:11 AM — Publish handoff

PM accepted the plain version, picked the A Hail of Memos hailstorm image, and is publishing now. Plain-language pass is the version going to publication.

The four-category opacity sweep + the ~1200-word target are now a working calibration sample. Worth extracting into the `draft-blog-post` skill design when we get to it. Specifically:
- The four-category sweep as a procedural step
- The ~1200-word target as a calibration baseline for Ships specifically (different targets likely for narratives vs. insights)
- The blog-post-list format (with featured-image-option fallback) as a Ship-specific structural element worth codifying

Standing by.

## ~7:30 AM — Step 1 of formalization: four new memories filed

PM gave green light on full plan (steps 1-4). Filed step 1 — four new memories capturing today's edit lessons:

1. `feedback_parenthetical_gloss_on_first_use.md` — hybrid role-naming + inline jargon-gloss share the parenthetical-on-first-use shape; both go in one memory
2. `feedback_affirmative_direct_over_disclaim_then_affirmative.md` — direct over "wasn't this — was that"
3. `feedback_no_semicolons_in_published_prose.md` — scoped to public prose; internal docbase keeps semicolons
4. `feedback_temporal_relationship_over_date_stamps_in_public_prose.md` — relationship language over inside-baseball date specifics

MEMORY.md index updated with four new entries. All filed at `~/.claude/projects/.../memory/` (user-side memory, no project-repo commit needed for these files).

Step 5 (metrics-as-table-or-bullets): PM confirmed canonical stays rich (tables); LinkedIn cross-post handles flattening. No change to Ship structure.

## ~7:45 AM — Step 2 done: voice-guide PROPOSED additions stacked

PM chose to stack today's lessons alongside May 11 PROPOSED for single voice-pass sweep. Filed two PROPOSED additions in voice/tone guide:

- Sentence Structure block: "Affirmative direct over disclaim-then-affirmative" + "No semicolons in published prose"
- Editorial Moves block: "Bare role-name or jargon term → parenthetical-gloss form" + "Inside-baseball date stamp → temporal-relationship language"

Voice-tone guide now carries 7 PROPOSED blocks awaiting PM voice-pass (5 from May 11 + 2 from today).

## ~8:00 AM — Step 3 done: blog-post template preamble + Ship Post Variant expansion

Added "Before you start drafting" preamble at top of `docs/internal/planning/comms/blog-post-template.md`:
- Required reading: voice/tone guide, editorial calendar, open-topics tracker
- Cross-cutting drafting discipline (voice + verifiable-claims at draft time)
- Four-category opacity sweep (procedural step)
- Rough length targets (Ships ~1100–1400 words; narratives/insights ~800–1300 words)

Expanded "Ship Post Variant" section at bottom:
- Ship-specific length target with creep-guard framing
- Blog-post-list section convention (heading-flexible, ordered by date, one-line teaser, featured-image-option-with-PM-pick fallback)
- Metrics-table note (canonical rich; PM handles LinkedIn flattening)
- Footer convention reminder (teases next-on-calendar regardless of category)

Last Updated stamp: "2026-05-13 — added 'Before you start drafting' preamble + expanded Ship Post Variant section."

## Pending: step 4

Step 4 (skill design for `draft-blog-post`) is the bigger commit; needs PM input on scope:
- One skill or two (Ship vs narrative/insight)?
- Gates at pre-draft / in-draft / pre-handoff, or just pre-handoff sweep?

Deferred until PM has bandwidth for a dedicated design conversation.
