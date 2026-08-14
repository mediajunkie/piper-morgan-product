# Blog Post Template

**For**: Communications Director
**Use**: Copy this file into `docs/public/comms/drafts/{slug}.md` and fill in.
**Last updated**: 2026-05-13 — added "Before you start drafting" preamble + expanded Ship Post Variant section.

---

## Before you start drafting

**Required reading** before opening a new draft:

1. **Voice & tone guide** — `docs/internal/planning/comms/xian-voice-tone-guide.md`. PM's distinctive writing style, sentence-structure preferences, transparency patterns, and editorial moves applied at voice-pass. Updated periodically; check whenever drafting after a gap.
2. **Editorial calendar** — `docs/internal/planning/comms/editorial-calendar.csv`. Confirm slot + cadence + what the previous piece's footer is teasing (shapes your opening *and* your own footer tease).
3. **Open-topics tracker** — `dev/active/comms-open-topics.md`. Quick state-of-play on what's drafted, pending, and flagged.

**Cross-cutting drafting discipline:**

- **Voice discipline applies at draft time, not only at voice-pass.** The voice guide names editorial moves PM applies during voice-pass; drop them at draft time so voice-pass is voice work, not janitorial. Recurring moves to absorb upstream: no number-led titles; no semicolons in published prose; parenthetical-gloss form for role-names and jargon on first use (e.g., *"the product-management role (Piper Alpha)"*, *"calendar-offer policy (that is, when and how Piper offers to connect your calendar)"*); affirmative direct over disclaim-then-affirmative; temporal-relationship language over inside-baseball date stamps.
- **Verifiable-claims discipline at draft time, not handoff.** Source-check every comparative claim, count, named pattern, or specific number before filing the draft. Use `[FACT-CHECK NOTE for PM: ...]` brackets when you can't verify and want PM to supply.

**Four-category opacity sweep** — before handoff, scan the draft for these and translate:

1. **Agent role names treated as proper nouns** (Lead Dev, Architect, PPM, CXO, CIO, HOST, Exec, PA, Comms) → use role functions with optional parenthetical-gloss form on first use.
2. **Internal acronyms not glossed** (M2 / M2d / M2e, MVP, BYOC, ADR, PDR, MUX, UAT, AAXT, etc.) → expand, replace, or gloss inline. **Expand from the glossary, never from memory** (`knowledge/piper-morgan-glossary-v1.1.md` is the single source — e.g. PDR = Product *Decision* Record, not "design"). If a term isn't in the glossary, STOP and look up its originating doc (or add it) — don't guess. Gloss-on-first-use form: `Product Decision Record (PDR)` then `PDR`. Don't plain-language a glossary term *away* — gloss it. Run the lint before handoff: `python3 scripts/check-acronyms.py <draft>` (⛔ FALSE-UNPACK must be fixed).
3. **Issue/commit numbers in narrative prose** (#1018, commit `fc79de31`, ADR-061) → drop, move to footnote, or replace with role-functional description. Keep where they carry coordinate-function (metrics tables, GitHub references in technical detail sections).
4. **Gnomic self-references** that need shared context to parse ("the cohort was running the methodology fluently"; "the catch caught itself") → replace with concrete language.

**Rough length targets** (voice and substance carry the calibration; these are creep guards, not minimums):

- **Ship posts**: ~1100–1400 words / ~100–120 lines markdown. Recent Ships had drifted toward 2200+ words; punchier reads better.
- **Building narratives + insights**: ~800–1300 words / ~80–100 lines markdown.

If a draft significantly exceeds these, ask whether each section is doing argumentative work or just covering territory.

---

## Template

Copy everything between the BEGIN and END markers below into a new draft file.

```markdown
--- BEGIN TEMPLATE ---
---
image:
alt:
caption:
---

# Post Title

*Dateline — e.g., March 20–22, 2026*

Opening paragraph. The hook. What's this about and why should the reader care? One paragraph, two at most. Set the scene.

# Top-level section heading

Section content. Build the narrative. Show don't tell where you can.

## Subsection heading (only if needed)

Use `##` when a section has genuine sub-parts. Many posts won't need this level.

# Next top-level section

More narrative. Each `#` section is a beat in the story arc.

# Final section

Wrap the arc. The closing observation or question.

---

*Next on Building Piper Morgan: [next post title] — [one-line teaser about what's coming].*

*[Reader question — invites engagement, tied to the post's theme.]*
--- END TEMPLATE ---
```

---

## Notes for Comms

### Frontmatter

Leave the three frontmatter fields empty. PM fills them in during the final edit pass. Keep the `---` fences on their own lines at the very top of the file.

```yaml
---
image:
alt:
caption:
---
```

### Headings

Use `#` for top-level sections and `##` for subsections (only when you genuinely need a sub-level).

- First `# Title` line (at the top, after frontmatter) → becomes the post title
- Subsequent `# Section` lines → become `<h1>` in the rendered HTML (top-level visible headings)
- `## Subsection` lines → become `<h2>`
- `### Sub-subsection` lines → become `<h3>`

This two-level convention matters because LinkedIn collapses multiple `##` headings to the same size, which loses the visual hierarchy. By using `#` and `##` to produce `<h1>` and `<h2>` in the output, the hierarchy survives Medium and LinkedIn syndication.

### Dateline format

Italicized, right after the title, on its own line. Use en-dash between dates:

```
*March 20–22, 2026*
```

### Footer

Horizontal rule, then two italicized paragraphs:

1. Next-post teaser (one sentence)
2. Reader question (invites engagement)

Docs can look up the next-post title from the editorial calendar if needed.

### What Comms doesn't need to fill in

- Image filename, alt text, or caption (PM adds during final edit)
- Publication date (editorial calendar + publish-to-blog skill handle this)
- Category, cluster/era (editorial calendar has these)
- hashId (publish-to-blog skill generates)

### What Comms should confirm before delivering a draft

- Dateline matches the actual work period covered
- Next-post teaser is consistent with the editorial calendar schedule
- If the post references a PDR, ADR, Pattern, or methodology doc by name, **verify principle/pattern names against the canonical source document** — don't paraphrase from memory or from omnibus summaries. This is the discipline adopted after the April 16 PDR-004 correction.

---

## Ship Post Variant

For Weekly Ship posts (category: ship), the structure is different — they're weekly summaries rather than narratives. Ship posts use a section-based format (Product & Experience, Engineering & Architecture, Methodology & Process Innovation, etc.). See the most recent published Ship for the current structure.

Frontmatter is the same:

```yaml
---
image:
alt:
caption:
---
```

For ships, the image is typically `piper-ship.png` and is reused across ships. PM may leave `alt` and `caption` empty or shared across ships.

### Ship-specific length target

~1100–1400 words / ~100–120 lines markdown. Recent Ships had drifted toward 2200+ words; the May 13 Ship #042 plain-language pass landed at ~1250 words pre-blog-list, ~1400 words with the list. Treat as a creep guard, not a minimum — voice and substance carry the calibration.

### Blog-post list section

Every Ship includes a list of the prior week's other publications (narratives + insights) so the Ship serves as a round-up. Convention as of May 13:

- Heading: a single `#` section with a name that fits the Ship's voice (e.g., "Published this week," "On the blog," "Catching up"). Pick something that reads as part of the post, not boilerplate.
- One bullet per publication, ordered by publish date. Each bullet: publish date, em dash, linked title, em dash, one-line teaser drawn from the post's own opening or footer.
- Exclude the Ship itself from the list.
- Featured-image option: link a representative narrative's cartoon image into the section as the visual anchor. If two narratives have strong candidate images, file both options inline with a note for PM ("PM: pick one") rather than picking unilaterally — PM has voice on which image carries the Ship.

Pull dates, slugs, alt text, and workDates from `docs/internal/planning/comms/editorial-calendar.csv`. The publish-to-blog skill generates final URLs; in draft, link to `/blog/{slug}` form.

### Metrics section (Ships)

**Convention updated 2026-08-13 (PM decision via Exec, website#31 thread)**: the Metrics block in
a Ship uses a **real smaller heading** (`### Metrics (date range)` in draft markdown) followed by
the bullet list — not a bold pseudo-label line (`**Metrics (…):**`), and not the markdown table
this section previously prescribed. (Ships since #050 had already drifted to bold-label + bullets;
the written convention now matches what actually ships, with the label promoted to a real heading.
PM holds this less firmly than the emphasis fix it rode with — if a case argues for something
else, surface it rather than treating this as fully locked.) Historical note: real tables render
fine on the blog but LinkedIn collapses them, which is part of why the drift happened.

### Footer convention for Ships

Ships post on Wednesday and the next scheduled item is typically a Thursday narrative. Footer teases that narrative regardless of category — see the publishing cadence memory and the `feedback_footer_teases_next_post_on_calendar_any_category` note.
