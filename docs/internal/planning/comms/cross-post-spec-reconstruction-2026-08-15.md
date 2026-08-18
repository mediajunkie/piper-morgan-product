# Cross-Post Spec — RECONSTRUCTION

**Status**: 🟡 **DRAFT RECONSTRUCTION — NOT AUTHORITATIVE. Needs xian's review, correction, and amendment.**
**Assembled**: 2026-08-15 (Claude Code, general-purpose session, at xian's request)
**Supersedes**: nothing. Authoritative once xian has edited it and changed this banner.

---

## 🛑 Read this before treating anything below as a decision

**This is not the original spec. The original spec is lost.**

xian dictated an end-to-end cross-post process on or around **2026-06-07**. That spec was saved
only to a Cowork session's outputs directory and was **confirmed gone on 2026-07-09**. A search on
2026-08-15 across both Piper repos, the dispatch repo, all local Cowork session storage, and the
Claude application data found **no copy of it**. It is not recoverable from this machine.

What follows is a **reconstruction assembled from surviving fragments** — planning docs that predate
and postdate the lost spec, one contemporaneous memory-file summary of it, and the shape of problems
the rebuilt skill has had to solve. **Every section below is labeled with its evidence basis.**

| Label | Meaning |
|---|---|
| **[EVIDENCED]** | Traceable to a specific surviving artifact, cited inline. Should be correct. |
| **[INFERRED]** | My reconstruction from adjacent evidence. Plausible; **not attested**. Check it. |
| **[OPEN]** | I could not determine this. Needs xian to supply it. |

⚠️ **The specific failure this document is at risk of repeating**: on 2026-07-09 a reconstruction
was written, committed with an honest "reconstructed from memory notes" note in its first
commit — and then 36 commits of refinement accreted on top of it until the reconstruction read as
settled design. **The provenance labels above are the guard against that.** Do not strip them when
editing; convert them (to plain prose, or to **[RATIFIED 2026-xx-xx]**) only for lines you have
actually confirmed.

---

## Why this document exists

The rebuilt cross-post skill takes its content by **scraping the live rendered HTML** off the
published pipermorgan.ai page (its `.prose` container). xian's position, stated 2026-08-15:

> *"my process involves starting with a markdown file. Any process that starts from the HTML is a
> shortcut invented by some agent as a variant of what I instructed originally."*

The investigation on 2026-08-15 supports that. Findings that motivate this doc:

- The installed skill (`cross-post`, 1,725 lines) contains the word **"markdown" zero times**.
- `editorial-calendar.csv` carries a **`draftPath`** column pointing at the markdown source,
  populated on **66 of 66** rows with `pubDate >= 2026-06-01`. The skill's *step 1* already opens
  that exact CSV row — and reads `theme`, `status`, `blogURL`, `mediumURL`, `liPubDate`,
  `canonicalSite`, but **not** `draftPath`. The word appears once in the whole skill, inside a list
  of column names.
- **No commit anywhere replaced a markdown-based version with an HTML-based one, and no commit
  message or issue states a rationale for choosing HTML.** The HTML framing enters at two points,
  neither of them xian: issue **#1160**'s feasibility paragraph (filed by Docs 2026-06-06, *one day
  before* the spec, speculating a session could *"copy the rendered content"*), and the 2026-07-09
  reconstruction, whose first full draft (`8a97cb9`) opens Medium step 1 with *"Fetch the source
  article's content directly from its `.prose` container."*

---

## Provenance of this reconstruction

| Source | Date | What it supplies |
|---|---|---|
| `docs/internal/planning/comms/publishing-workflow-target.md` | 2026-03-22 | The editing-surface decision; blog-as-canonical; syndication as a downstream step |
| `docs/internal/planning/comms/content-publishing-run-of-show.md` | 2026-06-19 | 7-step sequence; frontmatter fields; syndication as step 7; role ownership |
| `dispatch/migration-staging/.../blog-publishing-quickstart.md` | 2026-03-16 | xian-facing "your publishing flow, step by step" ordering |
| Cowork agent memory `project_cross_post_skill.md` | 2026-06-07 entry | **The only surviving description of the lost spec's input contract** |
| GitHub issue **#1160** | 2026-06-06 | Original problem statement (open, unassigned work) |
| Installed `cross-post` SKILL.md | through 2026-08-15 | Platform-side mechanics and hazards worth preserving |
| `docs/public/comms/drafts/*.md` | current | The actual markdown shape, read directly |

**Not consulted, because it does not exist**: the June 7 spec.

---

## Part 1 — Design intent

**[EVIDENCED]** `publishing-workflow-target.md`, 2026-03-22, records the decision under "Key
Decisions Made":

> **Editing surface**: Markdown in this repo, not Medium's editor

and the motivation:

> PM wants to edit markdown → publish, not context-switch to Medium's editor for final polish

**[EVIDENCED]** pipermorgan.ai is canonical. Medium and LinkedIn are **syndication targets**, and the
syndicated copies carry a canonical link back to the blog. Same doc: *"Make pipermorgan.ai the
canonical home for all published content. Medium and LinkedIn become syndication channels, not
primary publishing surfaces."*

**[INFERRED]** The intended reading — and the thing the HTML-scrape approach quietly inverted — is
that **the markdown draft is the source artifact for the whole pipeline**, blog included. The blog is
one *rendering* of it (via `publish-post.js`), not an intermediate that later stages re-parse.
Scraping the rendered page makes the blog's HTML an intermediate source of truth and reintroduces
exactly the context-switch the March decision removed.

---

## Part 2 — Input contract

**[EVIDENCED]** The one surviving description of the lost spec's inputs, from the memory file written
at the time:

> *"inputs come from Docs (markdown path, image path, canonical URL, platforms)"*

**[INFERRED]** Mapping those four inputs onto where they live today. All four are already in the
calendar row or the draft's own frontmatter — **nothing needs to be scraped to obtain them**:

| Spec input | Where it lives now | Status |
|---|---|---|
| **markdown path** | `editorial-calendar.csv` → `draftPath` | Populated 66/66 rows since 2026-06-01 |
| **image path** | draft frontmatter `image:`, file alongside the draft in `docs/public/comms/drafts/` | Filled by xian at run-of-show step 4 |
| **canonical URL** | `editorial-calendar.csv` → `blogURL` (fallback: `blogPath`) | Populated on published rows |
| **platforms** | `editorial-calendar.csv` → `theme`, via the routing table in Part 4 | Populated |

**[OPEN]** Whether the spec expected these to be **passed in** by Docs (as a memo hand-off — the
2026-07-04 Docs→Dispatch crosspost memo has roughly this shape) or **looked up** by the skill from
the calendar row. The current skill looks them up. Both are consistent with the fragment; xian to
settle.

---

## Part 3 — Trigger and confirmation handshake

**[EVIDENCED]** (installed skill, confirmed working 2026-07-12 — post-dates the lost spec, but is
attested as xian's actual working pattern.) xian opens a run with something like *"it's time to
cross-post,"* often **without naming the post**. The correct response:

1. Look up today's row in `docs/internal/planning/comms/editorial-calendar.csv` by
   `pubDate` = today. **Not** by title.
2. Run the day/theme cross-check (Part 4). If they disagree, **stop and flag it** — do not proceed
   on `theme` alone.
3. Report back, before any browser work: `title`, `theme`, the platform(s) it routes to, `status`,
   `blogURL`, `canonicalSite`, and current syndication state (`mediumURL`, `liPubDate`,
   `linkedinURL`) so an already-distributed post isn't re-syndicated.
4. Wait for xian's explicit confirmation before starting.

**[INFERRED — new, and the point of this document]** Step 1 should **also read `draftPath`** and
load that markdown file. It is in the row already being read.

---

## Part 4 — Platform routing

**[EVIDENCED]** Routing is **theme-based**, given directly by xian and corrected into the skill
2026-07-12. (An earlier reconstruction had guessed day-of-week routing; commit `c00e3f1`, 2026-07-11,
replaced the guess with the confirmed mechanism.)

| `theme` | What it is | Published | Syndicates to |
|---|---|---|---|
| `building` | Sequential building-narrative posts | Tue & Thu | **Medium only** |
| `insight` | Thematic insight posts | Sat & Sun | **Medium and LinkedIn** |
| `ship` | Weekly Ships | Wed | **LinkedIn only** |

⚠️ **`building` is Medium-only.** A wrong rule that grouped `building` with `insight` caused a real
near-miss on 2026-07-12 — a LinkedIn draft built for a Tuesday `building` post, caught by xian before
publish.

**Pre-flight cross-check**: `pubDate`'s day-of-week must match `theme`. If it doesn't, **stop and
flag** — a mismatch means the calendar row is wrong, and is not to be silently resolved in favour of
either field.

---

## Part 5 — Content preparation, from the markdown

> **This is the section that differs most from the installed skill**, and the reason this document
> exists. Everything here replaces the skill's "fetch the source article's `.prose` container."
> **[INFERRED] throughout unless marked otherwise** — this is my reconstruction of what a
> markdown-sourced pipeline does, not recovered spec text.

### 5.1 The draft's actual shape — **[EVIDENCED]**, read from real drafts on 2026-08-15

```markdown
---
image: 'the-write-path-chase-delivery.png'
alt: 'A translucent AI messenger races alongside a pneumatic tube, comparing her copy…'
caption: '"Okay, *this time* it worked!"'
---

# The Write-Path Chase

*July 8–9, 2026*

Body paragraph…

# Five ways to fail quietly

More body…
```

Structural facts, confirmed by direct reading:

- **Frontmatter carries `image:`, `alt:`, `caption:`** — filled by xian at run-of-show step 4.
- **The first `#` is the post title.** Subsequent `#` headings are **subheads**, not sections above
  the title. This is the origin of the "site uses `<h1>` for subheads" quirk the installed skill
  works around in the DOM: it is not a site bug, it is the draft convention rendering faithfully.
- **`##` when present is a genuine nested subsection** under the preceding `#`.
- The italic line directly under the title is the **dateline**, and covers the *work period* being
  written about — not the publication date.
- **Captions can legitimately contain their own quotation marks and inline emphasis**
  (`'"Okay, *this time* it worked!"'`). They are to be carried **verbatim**.

### 5.2 What this makes unnecessary

Each of these is a hazard the installed skill fights in the DOM, which the markdown answers directly:

| Skill hazard (HTML-sourced) | Markdown equivalent |
|---|---|
| Caption is a sibling `<p>` of the image wrapper; `closest()` misses it; site has no `<figure>` | `caption:` frontmatter field |
| Alt text vs caption conflation — *"the single most recurrent error in past runs"* | `alt:` and `caption:` are separate named fields |
| Caption's own quote marks dropped when retyped (found 2026-08-15) | Copy the frontmatter string verbatim |
| Count distinct heading levels in `.prose` to choose a mapping rule | `#` vs `##` is explicit in the source |
| Cover image must be fetched **on the source page** because Medium's CSP blocks off-domain fetch from its editor | Local file path from frontmatter |

### 5.3 Heading map

**[INFERRED]** Derived from the draft convention above, and consistent with the mapping the skill
arrived at empirically:

- First `#` → the post's **title field** on the target platform (not body content).
- Remaining `#` → **Medium** larger heading (`<h3>`, first "T" icon) / **LinkedIn** "Heading".
- `##` → **Medium** subheading (`<h4>`, second "T") / **LinkedIn** "Subheading".
- Apply the deeper level **first** when both exist, so the two levels don't collide and flatten.

### 5.4 Body rendering

**[INFERRED]** Render markdown → HTML using the converter the blog already uses and trusts:
`piper-morgan-website/scripts/publish-post.js` (771 lines) with its 19-case regression corpus at
`scripts/publish-post-corpus/` (headings, paragraphs, em dash, HR, blockquote, tables, inline and
linked images, fenced code, mixed blocks). Paste that HTML by the same ClipboardEvent technique the
skill already uses.

**[OPEN]** Whether to reuse `publish-post.js` directly, extract its converter, or render some other
way. Reuse means the syndicated copy and the blog copy are rendered by **one** converter, which is
the property worth having. Not attested in any surviving fragment — my recommendation, xian's call.

---

## Part 6 — Review checkpoints

**[EVIDENCED]** The memory record of the lost spec states its purpose in these terms:

> The manual process is 35+ steps across two platforms for a dual-syndication post. The skill reduces
> xian's involvement to **5 pause points** (proofreading each platform, teaser draft for LinkedIn,
> publish confirmation on each).

**[INFERRED]** Enumerating those five:

1. **Medium draft proofread** — lead with the `/p/<id>/edit` URL; wait for confirmation.
2. **LinkedIn draft proofread** — lead with the `/article/edit/` URL; wait for confirmation.
3. **LinkedIn newsletter teaser** — draft it, then **show xian the exact text before publishing.**
4. **Medium publish confirmation.**
5. **LinkedIn publish confirmation.**

🛑 **Checkpoint 3 is a hard gate, and its loss is documented.** It was in the June 7 spec, was
**silently dropped during the 2026-07-09 rebuild**, and on 2026-07-22 a Weekly Ship published with an
agent-invented teaser xian never saw. **This is not recoverable after publish** — LinkedIn sends the
newsletter email at publish time, and editing the article afterward does not resend or correct it.
Re-added to the skill 2026-07-22 (commit `aed29c4`). **Prefer real copy from the post over invented
copy.**

**[EVIDENCED]** Standing rules that accompany the checkpoints:
- **Always lead with the draft URL** at every checkpoint. Don't make xian ask.
- **A bug reported on one platform means audit both.**
- **Never publish without explicit go-ahead.**

---

## Part 7 — Platform mechanics

**[EVIDENCED]** This part of the installed skill is **hard-won and should be preserved as-is** — it is
platform behaviour, independent of where the content came from. Roughly 1,700 lines of it, from ~14
real runs. It carries, among others: the Medium paywall checkbox defaulting to CHECKED (a recurring
miss that published several posts member-only); publication-first draft creation; the drop-cap
technique (single-**word** selection, re-taught by xian 2026-07-09 after the original was lost);
full-bleed width toggle; LinkedIn's ProseMirror editor; the Style-menu misclick and stale-screenshot
hazards; LinkedIn auto-linkifying plain-text domains and inflating link counts; paste dropping
in-body images; cursor drift on image insert; and cover-image upload being **broken at the MCP level**
(`file_upload`), with manual upload through the real OS file picker as the documented default since
2026-08-12.

**Do not rewrite Part 7 to change the content source.** Only these inputs change: title, body HTML,
image path, alt, caption — which now come from Part 5 instead of the DOM.

**[INFERRED]** One consequence to handle deliberately: the skill's post-paste **integrity checks**
currently compare the pasted target against the source `.prose`. With a markdown source, compare
against the **rendered HTML from 5.4** instead. This is the one verification that gets marginally
harder, not easier, and it should not be dropped — it is what catches LinkedIn silently eating
in-body images.

---

## Part 8 — Recording the syndication back

**[EVIDENCED]** Process change 2026-07-29: **Docs owns all editorial-calendar writes.**

- Send a memo to `mailboxes/docs/inbox/` in `piper-morgan-product` via `scripts/mail-send.sh`, with
  `mediumURL` and/or `linkedinURL`, `liPubDate`, the `status` change, and `canonicalSite` if relevant.
- **Never hand-edit the CSV** (a prior hand-edit caused field-count drift and unescaped-comma bugs).
  Still forbidden for everyone, Docs included.
- **Never touch `piper-morgan-website/data/editorial-calendar.csv`** — generated build artifact.
- If the memo can't be sent from the current context, **flag the exact values to xian** rather than
  editing the CSV, running `/update-calendar`, or silently skipping.

---

## Part 9 — Open questions for xian

These are the gaps I could not close from evidence. Answers here are what turn this into a spec.

1. **Was the markdown source explicit in your June 7 dictation**, or is "markdown path" in the memory
   fragment a summarizer's paraphrase? (I believe you; I'm asking whether the *phrasing* was yours.)
2. **Push or pull?** Does Docs hand the skill the four inputs in a memo, or does the skill read them
   from the calendar row itself? (Part 2)
3. **Render with `publish-post.js`, or something else?** (Part 5.4)
4. **Were there more than 5 pause points?** The "5" is from the memory summary of the spec, not the
   spec. (Part 6)
5. **What else was in the original that isn't here?** The teaser gate was dropped once and only
   surfaced after it cost a newsletter send. Assume there are others.
6. **Anything in Parts 3, 4, 7 that post-dates June 7 and contradicts what you actually specified?**
   Those parts are drawn from the rebuilt skill, which is the artifact under suspicion.

---

## Part 10 — Delta against the installed skill

For whoever implements this. **The change is a source swap at one seam, not a rewrite.**

| | Installed skill (2026-08-15) | This reconstruction |
|---|---|---|
| Content source | Live rendered HTML, `.prose` container | Markdown at `draftPath` |
| How it's obtained | Browser fetch of published page | File read; path is in the CSV row step 1 already opens |
| Title | Scraped from DOM | First `#` of the draft |
| Heading levels | Counted in the DOM, rule chosen per post | Explicit `#` / `##` |
| Image / alt / caption | Sibling-walk heuristics on a site with no `<figure>` | Frontmatter fields |
| Integrity check baseline | Source `.prose` | Rendered HTML from the markdown |
| Platform mechanics (Part 7) | ~1,700 lines, hard-won | **Unchanged** |
| Checkpoints, routing, record-back | As documented | **Unchanged** |

`.prose` appears **7 times** in the installed skill's 1,725 lines. The extraction dependency is
localized to step 1, the heading-mapping section, and the source side of the parity checks — which is
why this is a seam and not a teardown.

**Two things this does not fix**, and they should not be promised: the browser-driving half (both
editors still need a paste, and their sanitizers still strip and mangle), and cover-image upload,
which is broken at the MCP level and stays manual.

---

## Durability note

The June 7 spec died because it lived only in a Cowork session. The rebuilt skill is *still* durable
only as `dispatch/drafts/cross-post-SKILL-draft.md`, and the installed copy and that repo draft are
already recorded as drifted apart.

**This file is git-tracked in `piper-morgan-product` for that reason.** Edit it here, in place, and
commit. If the corrected spec ends up living anywhere else, it will be reconstructed a fourth time.

---

*Assembled 2026-08-15 by a Claude Code session at xian's request, from the sources listed under
Provenance. No other files were modified. **Not authoritative until xian has reviewed it.***
