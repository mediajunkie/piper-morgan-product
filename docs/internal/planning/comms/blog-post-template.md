# Blog Post Template

**For**: Communications Director
**Use**: Copy this file into `docs/public/comms/drafts/{slug}.md` and fill in.
**Last updated**: 2026-10-08 — template review (PM 10-05: "Blog template is likely stale"). Added scaffold mode (PM ruling 10-07), they/them for agents, title case, the tease-skips-Ships rule. Fixed `###` (the audit fails it). The Ship variant now points to the Ship skill, because its old text contradicted it (Ship footer tease, section order). Previous: 2026-09-26, 5th opacity category.

> **Default for new pieces is now a SCAFFOLD, not a full draft** (PM 2026-10-07, "AI prompts human"). See **Scaffold mode** below. The full template is for when PM asks for a full draft.

---

## Before you start drafting

**Required reading** before opening a new draft:

1. **Voice & tone guide** — `docs/internal/planning/comms/xian-voice-tone-guide.md`. PM's distinctive writing style, sentence-structure preferences, transparency patterns, and editorial moves applied at voice-pass. Updated periodically; check whenever drafting after a gap.
2. **Editorial calendar** — `docs/internal/planning/comms/editorial-calendar.csv`. Confirm slot + cadence + what the previous piece's footer is teasing (shapes your opening *and* your own footer tease).
3. **Pipeline state** — run `python3 scripts/comms-open-topics.py` and `python3 scripts/reconcile-drafts-calendar.py`. (The hand-kept `dev/active/comms-open-topics.md` went stale in July; the scripts read the calendar directly.)
4. **Blog style guide** — `docs/internal/planning/comms/blog-style-guide.md`. House terminology decisions that deliberately override the conventional term (e.g. "minimum valuable product," not "viable"). Check this before "correcting" any spelled-out term that looks like an error — two separate incidents (pre-06-10, and 2026-09-12) came from treating a deliberate house choice as a typo.

**Cross-cutting drafting discipline:**

- **Voice discipline applies at draft time, not only at voice-pass.** The voice guide names editorial moves PM applies during voice-pass; drop them at draft time so voice-pass is voice work, not janitorial. Recurring moves to absorb upstream: no number-led titles; no semicolons in published prose; parenthetical-gloss form for role-names and jargon on first use (e.g., *"the product-management role (Piper Alpha)"*, *"calendar-offer policy (that is, when and how Piper offers to connect your calendar)"*); affirmative direct over disclaim-then-affirmative; temporal-relationship language over inside-baseball date stamps.
- **Agents take they/them, Piper included** (PM 2026-09-29, extended to product copy 10-06). Never "it" for an agent. For a single agent's reflexive, PM uses "themselves".
- **Role names, PM's current form**: "my lead developer agent (Lead)", "my chief of staff agent (Exec)" on first use, then the short name.
- **Titles in title case** (template-audit check #2). PM retitles often. When the H1 changes, update the calendar title and, at PM's request, the filename.
- **Verifiable-claims discipline at draft time, not handoff.** Source-check every comparative claim, count, named pattern, or specific number before filing the draft. Use `[FACT-CHECK NOTE for PM: ...]` brackets when you can't verify and want PM to supply.

**Five-category opacity sweep** — before handoff, scan the draft for these and translate:

1. **Agent role names treated as proper nouns** (Lead Dev, Architect, PPM, CXO, CIO, HOST, Exec, PA, Comms) → use role functions with optional parenthetical-gloss form on first use.
2. **Internal acronyms not glossed** (M2 / M2d / M2e, MVP, BYOC, ADR, PDR, MUX, UAT, AAXT, etc.) → expand, replace, or gloss inline. **Expand from the glossary, never from memory** (`knowledge/piper-morgan-glossary-v1.1.md` is the single source — e.g. PDR = Product *Decision* Record, not "design"). If a term isn't in the glossary, STOP and look up its originating doc (or add it) — don't guess. Gloss-on-first-use form: `Product Decision Record (PDR)` then `PDR`. Don't plain-language a glossary term *away* — gloss it. Run the lint before handoff: `python3 scripts/check-acronyms.py <draft>` (⛔ FALSE-UNPACK must be fixed).
3. **Issue/commit numbers in narrative prose** (#1018, commit `fc79de31`, ADR-061) → drop, move to footnote, or replace with role-functional description. Keep where they carry coordinate-function (metrics tables, GitHub references in technical detail sections).
4. **Gnomic self-references** that need shared context to parse ("the cohort was running the methodology fluently"; "the catch caught itself") → replace with concrete language.
5. **Agent actors named with human-personhood nouns** ("person," "people," "someone," "everyone," "nobody" standing in for a named agent or agent group) → "an agent," the role name, or "the team." **Bidirectional**: crediting a human's actual action to an agent is exactly as wrong as the reverse — verify attribution against the primary source when in doubt, don't assume from a summary. Not a tone call like "cohort"/"team" — a false claim about who/what actually did something (agency and accountability, PM 2026-09-26). Run `template-audit` check #11's grep and give **every match its own verdict** — a holistic "sweep clean" is not a checkable claim (2026-09-26: exactly that phrasing hid a real miss). See `.claude/skills/template-audit/SKILL.md` check #11 for worked FAIL/PASS examples.

**Rough length targets** (voice and substance carry the calibration; these are creep guards, not minimums):

- **Ship posts**: measured norm ~1,600 words (see Ship Post Variant below).
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

## Scaffold mode (the default for new pieces since 2026-10-07)

PM writes the prose and Comms supplies the shape. A scaffold lives at the same path as a draft, with a calendar
row `status=drafted`, so the pipeline tracks it the same way. First worked example:
`docs/public/comms/drafts/the-unguarded-entrance.md` (Sep 6 beat, 2026-10-08).

What a scaffold contains, in this order:
1. Frontmatter (blank), a **working title** marked as a placeholder, and the dateline.
2. **The story in one sentence** (the A plot). If you can't write it, it isn't a beat yet (`continue-narrative`).
3. **Already told elsewhere**: earlier posts covering the same days, so PM doesn't retell them.
4. **Beats in order**, each a few lines of facts, each fact **cited to a source line** (log path + line, omnibus
   time, commit). Quotes verbatim. *PM choice* notes where a fact is PM's to include or not.
5. Optional B plot and "something strange", marked optional.
6. A possible closing thought, the footer tease target (or "nothing scheduled yet"), and a reader-question idea.
7. **Left out on purpose**, with the reason (names of people outside the team, engineering detail, unadjudicated
   counts).

No finished prose: PM's outside feedback (10-05) was that the posts had started to sound AI-written. Fragments and
"possible line" suggestions are fine, labelled as such.

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
- `###` and deeper: don't use in narrative/insight prose (template-audit check #4 fails them). Ships are the exception: their Metrics block uses `###`.

This two-level convention matters because LinkedIn collapses multiple `##` headings to the same size, which loses the visual hierarchy. By using `#` and `##` to produce `<h1>` and `<h2>` in the output, the hierarchy survives Medium and LinkedIn syndication.

### Dateline format

Italicized, right after the title, on its own line. Use en-dash between dates:

```
*March 20–22, 2026*
```

### Footer

Horizontal rule, then two italicized paragraphs:

1. Next-post teaser (one sentence). It teases the **next non-Ship post** on the calendar, whatever the category. If the literal next row is a Ship, skip it (template-audit check #6 has the snippet).
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

**Ships are drafted by Exec with the `draft-weekly-ship` skill. That skill and `knowledge/weekly-ship-template-v4.1.md`
are canonical.** The older notes that used to sit here contradicted both, so only the points Comms needs when
reviewing a Ship stay:

- **Frontmatter**: `image: piper-ship.png` (#056–#060 convention). Caption is often empty or `N/A`.
- **Section order**: Engineering & architecture first since #058, then Product & experience, Methodology,
  External relations, Governance & operations.
- **External relations** lists the window's posts (from the calendar, never from memory) and then one **hero
  image from a Tue/Thu narrative post**: `https://pipermorgan.ai/assets/blog-images/{slug}.webp`, never the
  frontmatter `image:` value.
- **Metrics**: a `### Metrics (date range)` heading plus bullets, never a table.
- **No footer tease.** Ships sit outside the tease chain (template-audit check #6).
- **Role names bare** (Lead, Arch, CXO…). Ships don't gloss on first use (template-audit, the Ship calibration table).
- **Length**: the measured norm is ~1,600 words. The 800–1,300 target is for narratives and insights only.
