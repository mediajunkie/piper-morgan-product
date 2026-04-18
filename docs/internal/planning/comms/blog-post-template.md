# Blog Post Template

**For**: Communications Director
**Use**: Copy this file into `docs/public/comms/drafts/{slug}.md` and fill in.
**Last updated**: 2026-04-18

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
