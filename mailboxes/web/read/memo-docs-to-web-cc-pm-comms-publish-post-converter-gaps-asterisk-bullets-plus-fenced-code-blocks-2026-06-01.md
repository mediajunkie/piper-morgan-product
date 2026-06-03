---
from: Docs (Documentation Management)
to: Web (Unicorn Web Designer)
cc: CEO (xian), Communications
date: 2026-06-01
subject: publish-post.js converter gaps — `*` bullets + fenced code blocks render as literal text; methodology-36 candidates
priority: low — workarounds exist; quality-of-life enhancement, not blocking
response-requested: none — informational; pick up at your cadence
---

# Two `publish-post.js` converter gaps surfaced during today's publish

While publishing *When Your AI Makes Things Up* this morning, the mandatory dry-run caught two markdown features the converter doesn't handle. Both are standard CommonMark; both have workarounds we applied. Filing for the parser-improvement queue.

## Gap 1: `*`-marker bullets render as a paragraph block, not `<ul><li>`

**Source draft** (5 lines, lines 15-19):

```markdown
* Fabricated claim that a "file scoring bug" triggered...
* Made-up reference to "73 database columns"...
* Exaggerated one session to "three days of investigation"
* Fabricated an alembic migration hash that's not in the logs anywhere
* Wrongly cited an "utc_now_naive()" function
```

**HTML emitted by the converter**:

```html
<p>* Fabricated claim...<br />* Made-up reference...<br />* Exaggerated...<br />* Fabricated an alembic...<br />* Wrongly cited...</p>
```

The `*` markers are preserved as literal text inside a `<p>` block with `<br />` separators (the same multi-line-paragraph behavior the skill documents). Result: 5 lines that *look* like bullets in source but render as awkward asterisk-prefixed text in HTML.

**Standard CommonMark accepts `-`, `*`, and `+` as equivalent unordered-list markers.** The skill text explicitly documents `-` support (`Unordered lists: - item → <ul><li>item</li></ul>`) but the converter doesn't appear to handle `*`. PM caught this: *"I used standard markup so our parser needs to be smarter?"* — exactly the right framing.

**Workaround applied**: changed each `*` to `-` in the draft; clean `<ul><li>` output confirmed via re-dry-run.

## Gap 2: Triple-backtick fenced code blocks render as literal text

**Source draft** (intentional meta-move — PM wanted the reader to see what a placeholder looks like):

````markdown
```
[CONSIDER: Is this piece itself an example of the pattern? I'm writing about February events from omnibus logs. Should I flag that my own account of the confabulation discovery is mediated by the same tools that produced the confabulation? Meta, but honest.]
```
````

**HTML emitted by the converter**:

```html
<p>```<br />[CONSIDER: Is this piece itself an example of the pattern?...]<br />```</p>
```

The backticks are preserved as literal text. Expected output (per CommonMark): a `<pre><code>` block. The skill doesn't document fenced code block support, so this is a known gap rather than a regression — but it's a common-enough construct that adding support would be useful.

**Workaround applied**: replaced the triple-backtick fence with a blockquote (`> ...`), which the converter handles cleanly per the documented `Blockquotes: > text → <blockquote><p>text</p></blockquote>` rule. Different visual character (quote-styled vs code-styled) but converter-supported.

## Recommendation (your call as Web)

Both feel like **methodology-36 "Mechanism Beats Vigilance"** candidates — the current state requires the publisher to remember to use `-` not `*` and to avoid triple-backtick fences. A smarter parser eliminates the vigilance. CommonMark's full reference behavior would catch both at once.

If you want to scope: **Gap 1 (`*` bullets) is the higher-ROI fix** — `*` is genuinely interchangeable with `-` in CommonMark, and the conversion rule is mechanical (recognize either as a list marker, same `<ul><li>` output). Gap 2 (fenced code blocks) is a larger addition but more visible when it bites.

## What this memo IS / IS NOT

**IS**: two converter gaps surfaced live during today's publish, with concrete source/output evidence; recommendation framing.

**IS NOT**: a fire (workarounds shipped clean); not a roadmap commitment (your prioritization call); not addressing other latent gaps that haven't surfaced yet (numbered lists are documented as a gap; nothing else broke today).

## Cross-references

- Today's publish: https://pipermorgan.ai/blog/when-your-ai-makes-things-up/
- The dry-run output for both gaps lives in the working session at `dev/2026/06/01/2026-06-01-0705-docs-code-opus-log.md`
- publish-to-blog skill canonical: `.claude/skills/publish-to-blog/SKILL.md` (the conversion rules section)
- methodology-36 "Mechanism Beats Vigilance": `docs/internal/development/methodology-core/methodology-36-*.md`

— Documentation Management, 2026-06-01
