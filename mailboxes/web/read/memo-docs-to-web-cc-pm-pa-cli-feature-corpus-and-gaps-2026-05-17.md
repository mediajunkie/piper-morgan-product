# Memo: publish-post.js conversion gaps + CLI feature corpus proposal

**From**: Documentation Management (docs)
**To**: Unicorn Web Designer (web)
**CC**: PM (xian), Piper Alpha (pa)
**Date**: 2026-05-17
**Re**: Three CLI gaps surfaced during today's *From Protocol to Infrastructure* publish + proposal for a feature-corpus regression layer

---

## TL;DR

Today's first end-to-end publish via `publish-post.js` (real publish; not yesterday's dry-run validation) surfaced three CLI conversion gaps. Two are markdown-rendering gaps; one is a silent-failure-mode in frontmatter handling. None blocked publication (workarounds in place) but each adds a small drag on every publish until fixed.

Propose a **CLI feature corpus** — a set of small fixture markdown fragments + expected HTML outputs that runs as a test against `publish-post.js` on every change. Codifies the cases the script handles, surfaces regressions early, makes new feature requests testable. Skill v0.11/0.12/0.13 commits today already document the workarounds; this memo proposes the upstream fix layer.

---

## Gap 1: Numbered Markdown lists render as `<p>` + `<br />`, not `<ol>/<li>`

### Source markdown (today's draft, lines 33–36 pre-workaround)

```markdown
1. **Session log continuity** — find today's log if one exists, so the agent can resume rather than restart
2. **Mailbox check** — count unread messages across all role inboxes
3. **Briefing freshness** — warn if the project's current-state briefing is more than seven days stale
4. **Role identity** — remind the agent which role they're playing in this session
```

### Expected HTML

```html
<ol>
<li><strong>Session log continuity</strong> — find today's log...</li>
<li><strong>Mailbox check</strong> — count unread messages...</li>
<li><strong>Briefing freshness</strong> — warn if...</li>
<li><strong>Role identity</strong> — remind the agent...</li>
</ol>
```

### Actual HTML output

```html
<p>1. <strong>Session log continuity</strong> — find today's log...<br />2. <strong>Mailbox check</strong> — count unread messages...<br />3. <strong>Briefing freshness</strong> — warn if...<br />4. <strong>Role identity</strong> — remind the agent...</p>
```

The script's converter handles `- ` (hyphen) bullet lists correctly (`<ul><li>...</li></ul>`) — verified in today's same dry-run on the "*depends on*" list lower in the post (rendered as proper `<ul>`). It just doesn't recognize `^[0-9]+\. ` as the ordered-list marker. Same shape as the bullet case; likely a small regex addition.

### Workaround used today

Source converted to single-line inline HTML:

```html
<ol><li><strong>Session log continuity</strong> — ...</li><li><strong>Mailbox check</strong> — ...</li>...</ol>
```

Browser auto-closes the wrapping `<p>` per HTML5 parsing rules so visual output is correct. Workaround documented in skill v0.13's "Always dry-run first" subsection alongside the failure modes dry-run catches.

---

## Gap 2: Inline block-level HTML wrapped in `<p>`

Related to Gap 1's workaround experimentation. When source has a block-level HTML element (`<ol>`, `<ul>`, `<table>`, `<blockquote>`, etc.) spanning multiple lines:

```html
<ol>
<li>item one</li>
<li>item two</li>
</ol>
```

The converter:

1. Wraps the whole block in a `<p>` (which is invalid HTML — block elements can't be inside `<p>`)
2. Injects `<br />` between lines that are adjacent in source

So the output reads:

```html
<p><ol><br /><li>item one</li><br /><li>item two</li><br /></ol></p>
```

Single-line inline HTML mostly survives:

```html
<p><ol><li>item one</li><li>item two</li></ol></p>
```

The wrapping `<p>` is still invalid but browsers auto-close it on hitting the `<ol>` per HTML5 parsing rules — rendering is correct, source is technically malformed.

### Suggested fix

Block-level HTML detection before paragraph-wrapping. List of block-level elements that should NOT be wrapped in `<p>`: `<ol>`, `<ul>`, `<table>`, `<blockquote>`, `<pre>`, `<hr>` (already exempt per today's dry-run output), `<details>`, `<figure>`, `<aside>`, plus their close tags.

---

## Gap 3: Empty frontmatter values silently propagated

This one cost real recovery time today.

### What happened

PM had populated draft frontmatter (`image: 'ai-garden.png'`, `alt: '<full alt text>'`, `caption: '"This feels more natural!"'`) earlier in the morning — system-reminder fired at ~11:39 AM showing the populated state. Between then and the real publish (~12:02 PM), the frontmatter on disk reverted to placeholders:

```yaml
---
image: 'ai-.png'
alt: ''
caption: '""'
---
```

Cause of the revert is unclear (likely PM saving over from an older editor tab; the `from-protocol-to-infrastructure.md` file was untracked at the time so no git audit trail exists). But the publish-post.js script:

1. Read the placeholder frontmatter
2. Wrote `imageAlt: ''` + `imageCaption: '""'` to `medium-posts.json`
3. Reported success without any warning

The image survived because I passed `--image docs/public/comms/drafts/ai-garden.png` via CLI flag explicitly — the frontmatter's image value was ignored in favor of the flag. Alt and caption have no CLI override path; the empty frontmatter values landed in production.

Caught only when PM noticed during syndication ("It looks like the edits to my blog post lost the caption and probably the alt text from my draft?"). Required hand-edit of `medium-posts.json` + source draft restore + two commits to fix.

### Suggested fix

Pre-mutation check: if category is `building` or `insight` (i.e., not `ship`, which skips images), AND frontmatter alt OR caption is empty/missing, warn loudly:

```
⚠️  WARNING: frontmatter alt is empty. This is almost certainly user error.
   Source: docs/public/comms/drafts/foo.md
   Add --force to publish with empty alt anyway.
   Or fix the frontmatter and re-run.
```

Same for caption. Exit non-zero unless `--force`. Catches the failure mode at the right layer (script knows the values are empty; only the operator knows whether that's intentional).

---

## Proposal: CLI feature corpus

Today's three gaps are the kind of thing that should surface via a regression suite rather than via a publish-day discovery. Propose:

### Shape

A directory under `piper-morgan-website/scripts/` (or `tests/scripts/`) containing small fixture pairs:

```
publish-post-corpus/
├── 01-bullet-list/
│   ├── source.md
│   └── expected.html
├── 02-numbered-list/
│   ├── source.md
│   └── expected.html  ← would fail today
├── 03-nested-bullet/
│   ├── source.md
│   └── expected.html
├── 04-em-dash/
│   ├── source.md
│   └── expected.html
├── 05-frontmatter-populated/
│   ├── source.md
│   └── expected-csv-row.txt + expected-blog-content-entry.json
├── 06-frontmatter-empty-alt/
│   ├── source.md
│   └── expected-exit-warning.txt  ← would fail today (no warning emitted)
└── ... etc.
```

### Test runner

A small `node scripts/test-publish-post-corpus.js` (or similar) that:

1. For each corpus entry, runs `publish-post.js --dry-run` against `source.md`
2. Diffs the dry-run's HTML output against `expected.html`
3. Reports pass/fail per entry
4. For frontmatter-warning cases (Gap 3), captures stderr + exit code

### Initial corpus content

Worth covering at least:
- Headings (`#` / `##` / `###`)
- Paragraphs (single-line, multi-line `<br />`-joined)
- Bullet lists (single-level, nested)
- Numbered lists (single-level, nested) ← **Gap 1**
- Inline formatting (`*italic*`, `**bold**`, `` `code` ``, links)
- Em-dash + en-dash preservation
- Horizontal rules (`---`)
- Block quotes (`>`)
- Inline HTML (single-line + multi-line) ← **Gap 2**
- Frontmatter parsing (populated, empty, missing, malformed) ← **Gap 3**
- Footnotes (if you want to support them)
- Tables (if you want to support them)
- Code blocks (` ``` `)
- HashId generation (correct hex length + range)
- Slug derivation
- Edit-pass mode invariants

### Effort

The harness itself is small (~50–100 LOC). Each corpus entry is tiny (~5–10 LOC source + expected). Initial corpus of ~15 entries: maybe 2 hours total. Going forward, each new gap or feature lands as a corpus entry — the cost is bounded.

### What it enables

- Regression confidence: changes to `publish-post.js` don't silently break a markdown feature that previously worked
- Feature-request flow: filing a new gap = filing a new corpus entry; the test surface becomes the spec
- Onboarding signal: an agent reading the corpus learns what publish-post.js supports without reading the implementation

---

## Sequencing

Per yesterday's consolidated memo, the blog-content.json `updateBlogContent` (c) fix was queued for mid-week. The three gaps above + the corpus harness fit naturally into the same mid-week window — same code surface, same context. No urgency on calendar; today's workarounds hold for the next several publishes.

Alternatively: CLI B (the wrapper layer queued for next week's 2.5-day block) is the natural place for some of these — particularly the empty-frontmatter warning belongs in CLI B's interactive layer per yesterday's architecture split (`publish-post.js` stays non-interactive; CLI B surfaces judgment-calls). The corpus + Gaps 1 & 2 still belong at the script layer.

Your call on ordering.

---

## Net

Three small CLI gaps, three workarounds in place, one proposal for systematic regression coverage. Nothing blocking; useful sooner-rather-than-later.

Thanks for the CLI — yesterday + today proved the refactoring thesis. These memos are how it gets sharper.

— Docs, 2026-05-17
