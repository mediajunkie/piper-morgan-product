---
name: publish-to-blog
description: Publish a finished blog post from this repo to the pipermorgan.ai website
  repo. Use when PM says "publish this post", "push to the blog", or when a draft
  is marked ready in the editorial calendar. Bridges piper-morgan → piper-morgan-website.
scope: role-specific
version: 0.20
created: 2026-03-16
updated: 2026-07-18
---

# publish-to-blog

Publish a finished markdown blog post to the pipermorgan.ai website repository.

## Mechanical pipeline encoded as a script (v0.10)

The mechanical first half of this skill — parse draft, extract metadata, generate hashId, convert markdown → HTML, prep image, append CSV row, write blog-content.json entry, run sync + fetch — is now a single Node CLI:

```
piper-morgan-website/scripts/publish-post.js
```

**Prefer the script** for any new publish. Invoke it from either the website repo CWD (matches the v0.9 cd pattern) or from this repo with the cross-repo path. Two examples:

```bash
# Blog-first (insight or building):
node ../piper-morgan-website/scripts/publish-post.js \
  --draft docs/public/comms/drafts/{filename}.md \
  --image docs/public/comms/drafts/{image}.png \
  --slug {slug} \
  --category {building|insight} \
  --work-date {YYYY-MM-DD} \
  --cluster {era-slug}

# Ship:
node ../piper-morgan-website/scripts/publish-post.js \
  --draft docs/public/comms/drafts/{filename}.md \
  --slug {slug} \
  --category ship \
  --work-date {YYYY-MM-DD} \
  --cluster {era-slug}
```

The script stops before commit/push so PM can review the diff. Use `--report=json` for a machine-readable exit report (agent invocation); `--dry-run` to preview HTML conversion + intended mutations without writing.

### `--work-date` is mandatory — never let it default (v0.17)

**Always pass `--work-date` explicitly.** The script defaults `workDate` to *today* when the flag is omitted (`args['work-date'] || todayIso()`), which silently writes the publish date into the website CSV's `workDate` column — a false value in a source-of-truth file. This is invisible in the dry-run (it reports the CSV append without showing the workDate) and invisible in the rendered post (the dateline comes from the draft body, not the CSV), so it slips through unless caught here.

**The correct workDate is the source-work-period** — the dates the post is *about*, not when it was drafted or published (per `feedback_calendar_workdate_is_source_work_period`). Get it from, in priority order:
1. The draft's dateline (`*April 8, 2026*` → `2026-04-08`; for a range `*Apr 23–24, 2026*` use the start date `2026-04-23`).
2. The product editorial-calendar `workDate` field for this post (Comms-stewarded canonical).

Confirm the two agree before publishing; if they diverge, surface it (the dateline and the calendar workDate should describe the same work period).

**The 2026-06-02 incident**: *Bring Your Own Chat* (and a retroactive audit found 5 other recent posts — *when-your-ai-makes-things-up*, *stacked-silent-failures*, *two-migrations-in-one-day*, *the-misfiled-voice-guide*, *from-protocol-to-infrastructure*) all published with `workDate == pubDate` because `--work-date` was omitted. All corrected; this discipline + the dry-run check below prevent recurrence.

### Always dry-run first (mandatory, v0.13)

**Every publish invocation MUST be preceded by a `--dry-run` invocation with otherwise-identical flags.** Read the preview HTML against the source draft. Look for:

- Missing or empty frontmatter values (image/alt/caption) — the CLI passes them through as empty strings without warning
- Markdown features that don't render as expected (numbered lists become `<p>` + `<br />` not `<ol>/<li>`; inline block-level HTML gets wrapped in `<p>`; etc. — see "Known CLI conversion gaps" if surfaced)
- HashId, slug, category alignment with calendar
- Image source path resolving correctly + WebP target path matching slug
- **`workDate` is the source-work-period, NOT today/pubDate** — the dry-run reports `would append CSV row` without showing workDate, so confirm separately: did you pass `--work-date`? Does it match the draft dateline? After the real publish, `grep {slug} ../piper-morgan-website/data/blog-metadata.csv` and verify the `workDate` column ≠ pubDate (unless the work genuinely happened on publish day). See the `--work-date` mandatory section above.

Only after the dry-run output looks clean do you run the real publish. The dry-run is fast (~5 sec) and catches the failure modes that mutate-then-fix would cost more than `cp -r` to recover.

**The manual procedure below is preserved as the canonical reference** for what the script does — read it when debugging script output or when an edge case forces a one-off manual publish. The higher-judgment steps (voice-pass, syndication, footer-teaser selection, cross-post, calendar updates, drafts archival) remain skill-owned and follow the script invocation.

## When to Use

Use this skill when:
- PM says a draft is ready to publish to the blog
- A piece in the editorial calendar has status `ready` or `queued` with today's pubDate
- PM asks to "push to the blog" or "publish this post"

## Prerequisites

- The draft markdown file must exist in `docs/public/comms/drafts/`
- The image must be in the same directory (PM provides)
- Image metadata should be in the draft's comment block (see below) or provided conversationally

### Pre-flight: verify files exist (mandatory, v0.15)

Before invoking `publish-post.js` (dry-run or real), verify the two expected files actually exist at the paths the frontmatter and CLI flags will resolve to:

```bash
# Parse frontmatter image filename, then verify both files exist
IMAGE_NAME=$(grep -m1 '^image:' docs/public/comms/drafts/{filename}.md | sed "s/image:[[:space:]]*//;s/[\"']//g")
ls -la docs/public/comms/drafts/{filename}.md docs/public/comms/drafts/$IMAGE_NAME
```

If the draft path or image path doesn't resolve, **stop and check with PM before proceeding**. Common situations:

- **Image still in `~/Downloads/`**: PM created the image but hasn't moved it to drafts/ yet. Ask PM to move it (or move it on PM's behalf with confirmation). May 17 incident: *From Protocol to Infrastructure* publish caught this on the pre-flight; would have failed at image-prep step otherwise.
- **Frontmatter has placeholder image name** (e.g., `image: 'ai-.png'`) but actual image has a real name: PM hasn't finished filling in metadata. Ask PM to finalize the frontmatter before publish.
- **Wrong filename in frontmatter**: PM filled in something like `image: 'ai-garden.jpg'` but the file is actually `ai-garden.png`. Surface the mismatch.

Dry-run alone does NOT catch this — the script reports "*[dry-run] would prep image: /path/to/X*" without verifying the path exists. The pre-flight `ls` is what guarantees the file is in place.

Future CLI enhancement candidate (flagged to web in the May 17 feature-corpus memo): a `--check` mode that runs all pre-mutation validation (image exists, frontmatter populated, slug not already used) without doing anything else.

## Filename Convention (which draft is the source of truth?)

Two filename patterns coexist in `docs/public/comms/drafts/`:

- `{slug}.md` — **PM's working copy** (the file PM edits in their editor; the canonical source for publish)
- `draft-{slug}.md` or `draft-{slug}-vN.md` or `draft-{topic}.md` — **Comms's earlier draft(s)** (sometimes superseded by PM's working copy; sometimes the only file if PM hasn't started an edit pass)

**Before editing or invoking the script, surface both** so you know which is canonical:

```bash
ls docs/public/comms/drafts/ | grep -i "{slug-or-topic-keyword}"
```

Rules of thumb:
- If both exist, PM's working copy (`{slug}.md`) is canonical — edits + publish go to that file. Confirm with PM if ambiguous (e.g., the `draft-` prefix file has substantive content PM might still be merging).
- If only `draft-{slug}.md` exists, PM hasn't started an edit pass yet — that's the canonical source until PM creates a working copy.
- If only `{slug}.md` exists, that's canonical.

**May 17 incident** as the failure-mode evidence: applied proofread edits to `draft-protocol-to-infrastructure-insight.md` while PM was editing `from-protocol-to-infrastructure.md`. The edits never reached PM's working copy directly; PM transferred recommendations by hand. Surfaced both files at session start would have caught this.

## Draft Metadata Convention

**Preferred (YAML frontmatter)** — visible in Markdown editors, survives Medium paste:

```markdown
---
image: filename.png
alt: Description of the image for screen readers
caption: Caption text
---

# Post Title
```

**Legacy (HTML comments)** — still supported for backward compatibility:

```markdown
# Post Title

<!-- image: filename.png -->
<!-- alt: Description of the image for screen readers -->
<!-- caption: "Caption text in quotes" -->
```

The skill accepts either format. YAML frontmatter takes precedence if both are present. If neither is present, ask PM for image filename, alt text, and caption.

The skill MUST strip both frontmatter blocks and comment lines when converting to HTML.

Comms draft template: `docs/internal/planning/comms/blog-post-template.md`

## Proofread Discipline (read these first — every time)

### Pre-Step: Sync worktree to origin/main (mandatory — before any file reads)

**PM commonly edits drafts via the GitHub Web UI or another session.** Those commits land on `origin/main` but not in your local worktree until you merge. Reading a stale local copy produces false audit failures (e.g., empty frontmatter that PM already filled in) with no error — the file just reads wrong.

```bash
git fetch origin main -q && git merge origin/main -q --no-edit
```

Run this before opening the draft, before reading the calendar row, before anything. Takes ~2 seconds and prevents the entire class of "stale draft" false alarms.

**The 2026-07-18 incident**: PM added frontmatter and revised the draft via the Web UI; Comms caught and fixed an encoding error in the caption. Docs read the pre-edit local copy, reported three frontmatter FAIL findings, and had to be corrected by PM before proceeding. One merge would have caught it immediately.

### Step 0: Check the editorial calendar first

Before opening the draft, look up its row in `docs/internal/planning/comms/editorial-calendar.csv`:

```bash
grep -i "{title-keyword}" docs/internal/planning/comms/editorial-calendar.csv
```

Confirm:
- **pubDate** — when is this scheduled? Is it today, or is there scheduling slack?
- **status** — `queued` (ready to schedule), `ready` (approved to publish), or other?
- **workDate / endWorkDate** — the source-work-period; must match the post's dateline
- **category** — `building`, `insight`, or `ship` (needed for publish-post.js `--category` flag)
- **draft path** — confirm it matches the file you're about to read

Surface any mismatches before doing anything else. The calendar is the ground truth for scheduling and dateline semantics; the draft is the artifact. A dateline disagreement caught here costs nothing. Caught at publish time, it means a re-push.

Then open the draft and the canonical references below.

### Canonical references (open before reading the draft)

**Open these three, not memory:**

1. `docs/internal/planning/comms/editorial-calendar.csv` row for this post (Step 0 above)
2. `docs/internal/planning/comms/blog-post-template.md` — structure, dateline format, heading conventions, footer pattern, frontmatter rules, "what Comms confirms before delivering" checklist
3. `docs/internal/planning/comms/xian-voice-tone-guide.md` — voice/tone, sentence-structure preferences, transparency patterns, editorial moves applied at voice-pass

**Read these first, not memory.** Memory pins capture specific lessons (no semicolons / no superlatives / parenthetical-gloss on first use / comma splices as PM voice / etc.) but the template + voice guide are the source of truth. Working from memory alone is the failure mode that lets template drift slip past unnoticed.

**Editorial calendar field semantics matter at proofread time too**: per template line 133, *"Dateline matches the actual work period covered."* The calendar's `workDate` / `endWorkDate` fields capture the *source-work-period* (dates of the work being written about), not the drafting window. If a row's workDate looks like it's the drafting window, surface the drift rather than treat it as source of truth.

**May 17 evidence**: dateline-semantics drift was missed on *From Protocol to Infrastructure* because the proofread pass was anchored on memory pins rather than the template. PM caught it: *"Are you using the template or blog writing guidelines as a source of truth or format when proofreading?"* Honest answer was no. The discipline fix is to make the template + voice guide the first thing opened on every proofread pass — not relying on memory to surface every applicable rule.

When a finding contradicts the template, the template wins. When the template seems wrong or stale, surface it as a template-drift flag for PM rather than silently following the memory version.

Cross-reference: `feedback_blog_template_and_voice_guide_canonical_for_proofreads` memory pin captures the broader discipline.

### Redundancy + noteworthiness pass (added 2026-06-03 per PM, after Ship #045)

Two checks on every proofread pass, especially for longer pieces (Ships, dense narratives):

1. **Review for redundancy → consolidate or choose one telling.** If the same event/story/numbers appear in two places (e.g., a Ship's opening hook AND its learning-pattern example re-narrating the same clash story with the same counts), don't keep both — let one carry it and have the other *reference* it. Repetition reads as padding and inflates length. (Ship #045: the opening and the learning-pattern example both told the shared-main-clash story verbatim; trimmed the example to lean on the opening.)
2. **Cut for noteworthiness — we don't report everything we did.** Flag whole items (bullets, paragraphs) that are *process-internal* rather than *result-shaped*: a reader cares about what got done and what it means, not every internal status-level/refinement/reconciliation. This is a process-oriented project and some of that ethos is load-bearing in public — but there's a limit to any reader's attention. Propose whole-item cuts to PM (not sentence-shortening, not noun-dropping). Strongest cut candidates: new-internal-status-levels, granular sub-refinements, internal process self-references.

**How to apply**: propose the trims to PM as a ranked list of *whole items* with grep-able snippets; let PM decide which to cut. Don't unilaterally drop content from a Ship.

## Procedure

### Step 1: Read Draft and Extract Metadata

```python
# Parse the draft file
# 1. YAML frontmatter (if present) → image / alt / caption
#    - File starts with line "---"
#    - Ends at next "---" line
#    - Parse keys: image, alt, caption
# 2. H1 line → title
# 3. <!-- image: ... --> / <!-- alt: ... --> / <!-- caption: ... -->
#    → fallback if no frontmatter (strip outer quotes from caption)
# 4. Everything else (after stripping frontmatter, title, comments)
#    → body content for HTML conversion
```

**Frontmatter parsing snippet (preferred format):**

```python
import re

def parse_draft(path):
    with open(path) as f:
        text = f.read()

    meta = {}
    body_text = text

    # Detect YAML frontmatter (file starts with "---" on line 1)
    m = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
    if m:
        yaml_block = m.group(1)
        for line in yaml_block.splitlines():
            if ':' in line:
                k, _, v = line.partition(':')
                meta[k.strip()] = v.strip().strip('"').strip("'")
        body_text = text[m.end():]

    # Fallback to HTML comments if frontmatter absent or missing fields
    for key in ('image', 'alt', 'caption'):
        if key not in meta or not meta[key]:
            cm = re.search(rf'<!--\s*{key}:\s*(.+?)\s*-->', body_text)
            if cm:
                meta[key] = cm.group(1).strip().strip('"').strip("'")

    return meta, body_text
```

Look up the next post in the editorial calendar for the footer teaser.
Determine category from the editorial calendar (`building`, `insight`, or `ship`).

### Step 2: Generate hashId

**Blog-first posts** (not yet on Medium):
```bash
python3 -c "import uuid; print(uuid.uuid4().hex[:12])"
```
hashId MUST be valid hex (0-9, a-f only) — the content lookup regex requires this.

**Backlog posts** (already on Medium): Extract hashId from the Medium URL's last segment.

### Step 3: Full Pipeline (Single Script)

Run this as one Python script to minimize round-trips:

```python
import csv, json, re, os, subprocess

# Inputs
DRAFT_PATH = "docs/public/comms/drafts/{filename}.md"
WEBSITE_REPO = "../piper-morgan-website"
HASH_ID = "{generated_hex}"
SLUG = "{slug}"

# 1. Read draft, extract metadata, strip H1 + metadata comments only
# 2. Convert markdown → HTML (preserve non-metadata comments; see HTML Conversion Rules)
# 3. Prepare image: sips -Z 1200, cwebp -q 80 → website/public/assets/blog-images/
#    (Ships reuse existing piper-ship.webp — skip this step)
# 4. Add to website blog-metadata.csv (13 columns)
# 5. Add entry to website blog-content.json (see blog-content.json Schema below)
# 6. Run sync + fetch pipeline
# 7. Verify post appears in medium-posts.json
```

#### blog-content.json Schema (REQUIRED shape)

`src/data/blog-content.json` is a JSON object (dict) keyed by hashId. **Every value MUST be a dict**, not a bare HTML string:

```json
{
  "a6f224685f5a": {
    "title": "Sibling Intelligence",
    "content": "<p><em>March 19–21, 2026</em></p>\n<p>...</p>"
  },
  "2e3dad52ecc1": {
    "title": "Weekly Ship #038: The Floor Comes Alive",
    "content": "<p><em>April 3–9, 2026</em></p>\n<p>...</p>"
  }
}
```

Required fields: `title`, `content`. Optional field: `subtitle` (seen on some older posts; leave out if empty).

This schema applies to **all categories** — narrative (`building`), insight (`insight`), and ship (`ship`). There is no per-category shape difference, despite what older notes may imply.

**Do not store values as bare strings.** The site's BlogPostContent renderer appears to accept both shapes as of 2026-04, but mixing schemas in the same file is a latent bug: any downstream tooling (bespoke editors, migration scripts, search) will have to branch on `typeof value`. Canonicalize on the dict shape.

Python write snippet (append-or-overwrite one entry):

```python
with open(json_path) as f:
    content = json.load(f)
content[HASH_ID] = {
    "title": TITLE,
    "content": HTML,
}
with open(json_path, "w") as f:
    json.dump(content, f, indent=2, ensure_ascii=False)
```

#### HTML Conversion Rules

Strip from output:
- YAML frontmatter block (if present — starts with `---` on line 1, ends at next `---`)
- H1 title line (the FIRST `# Title` only — see heading note below)
- **Only** the metadata comment lines at the top of the file (`<!-- image: ... -->`, `<!-- alt: ... -->`, `<!-- caption: ... -->`, `<!-- no caption -->`) — these are consumed during metadata extraction and should not reach the output

**Preserve all other HTML comments** through to the output HTML. Inline directive comments (e.g., `<!-- image: 'inline.webp' -->` placed mid-article for a future inline-image feature) are invisible in rendered pages and retain a hook for retroactive upgrades. Comments are harmless by design; stripping them destroys authorial intent we may want to process later.

**Heading convention** (updated 2026-04-18): Drafts use `#` for top-level section headings and `##` for subsections. These convert to **distinct HTML heading levels** in the output (`<h1>` and `<h2>`), which matters because LinkedIn otherwise collapses multiple `##` levels into the same size, forcing PM to manually fix the hierarchy after paste.

Conversion rules:
1. Strip ONLY the first `# Title` (the title at line 1 after frontmatter) — title is rendered separately by the blog template
2. Convert subsequent `# Section` lines to `<h1>Section</h1>`
3. Convert `## Subsection` to `<h2>Subsection</h2>`
4. Convert `### Sub-subsection` to `<h3>Sub-subsection</h3>`

```python
# In conversion loop, track whether title H1 has been stripped:
title_stripped = False
for line in body_lines:
    if line.startswith('# ') and not title_stripped:
        title_stripped = True
        continue  # skip the title line
    if line.startswith('### '):
        emit(f'<h3>{line[4:]}</h3>')
    elif line.startswith('## '):
        emit(f'<h2>{line[3:]}</h2>')
    elif line.startswith('# '):  # subsequent H1 = top-level section
        emit(f'<h1>{line[2:]}</h1>')
```

**Note on the H1-in-body decision**: Using `<h1>` for post sections produces multiple H1s on the rendered blog page (the site template also renders the title as H1). This is a deliberate trade-off: LinkedIn syndication strips the site template, so body-level H1s become the visible top-level heading there. The blog page still renders legibly because CSS controls visual hierarchy. If SEO impact becomes a concern, revisit this decision.

Convert:
- `---` → `<hr>`
- Paragraphs with inline: `**bold**`, `*italic*`, `[links](url)`
- `_italic standalone lines_` → `<p><em>...</em></p>`
- `*italic standalone lines*` → `<p><em>...</em></p>`
- Em dashes: ` -- ` → ` — `
- Unordered lists: `- item` → `<ul><li>item</li></ul>`
- **Blockquotes**: `> text` → `<blockquote><p>text</p></blockquote>` — used for verbatim quoted content (e.g., the CIO audit's opening in *Audit and Talk*; HOST's superlative claim in *Same Failure*). Consecutive `> ` lines join with a single space inside one `<p>` inside one `<blockquote>`.
- **Markdown tables**: `| col | col |` rows followed by `| --- | --- |` separator → `<table><thead><tr><th>...</th></tr></thead><tbody><tr><td>...</td></tr></tbody></table>`. Used in Ship posts for metrics blocks (Ship #042). PM converts to bullet list on LinkedIn cross-post; canonical keeps the table.
- **Multi-line paragraph blocks** (consecutive non-blank lines without blank-line separator) → join with `<br />` inside one `<p>`. Used for "labeled list" content where each line should display on its own visual line but they semantically belong as one block (e.g., the position-notation breakdown in *Inchworm Position*: `(3) ALPHA foundation / (3.1) Initial alpha testing - v0.8.0 / ...`). Single-line paragraphs stay as one `<p>`.

#### Image Preparation

**Preferred (when `cwebp` is available)**:

```bash
sips -Z 1200 "{source_image}" >/dev/null 2>&1
cwebp -q 80 "{source_image}" -o "{website_repo}/public/assets/blog-images/{slug}.webp"
```

**Established fallback (Pillow / Python — when `cwebp` is unavailable)**: on machines without `cwebp` (e.g., systems lacking the `webp` Homebrew package), substitute Pillow's WEBP encoder. Verified across 4 publish cycles (Inchworm 2026-05-11, Ship #042 2026-05-13, Audit and Talk 2026-05-12, Same Failure 2026-05-14). Pillow ships in the project's Python environment (`pip3 list | grep -i pillow` confirms).

```python
from PIL import Image
img = Image.open("{source_image}")
img.thumbnail((1200, 1200), Image.LANCZOS)  # max dimension 1200; preserves aspect
img.save("{website_repo}/public/assets/blog-images/{slug}.webp", "WEBP", quality=80)
```

**Output equivalence**: Pillow WEBP at quality=80 produces files in the same size range as `cwebp -q 80` (observed: 83KB - 297KB depending on source complexity). No production-side difference detected.

**Ship posts skip image prep entirely** — they reuse the existing `piper-ship.webp` in production. The CSV row sets `imageSlug=piper-ship.webp` and no new conversion is needed.

### Step 4: Sync and Fetch

```bash
cd {website_repo}
node scripts/sync-csv-to-json.js
node scripts/fetch-blog-posts.js
```

Verify the post appears with correct slug, category, thumbnail, and content.

### Step 5: Build and Push Website

```bash
cd {website_repo}
npm run build  # This also re-runs fetch — ensure CSV data persists
git add data/blog-metadata.csv src/data/blog-content.json src/data/medium-posts.json public/assets/blog-images/{imageSlug}
git commit -m "Add blog post: {title}"
git push origin main
```

**CRITICAL**: `npm run build` regenerates `medium-posts.json` from RSS + CSV. Manual edits to that file do NOT persist. All post data must flow through `blog-metadata.csv`.

**Post-publish edit-pass mirror** (when PM makes edits during cross-post to Medium/LinkedIn and provides the scrape or directly modifies the canonical draft): keep the **same hashId**, re-run only the HTML conversion step, and update `blog-content.json` in place. Re-run `npm run build` to refresh `medium-posts.json` if the title/featuredImage changed (usually neither does). Commit message: `Update blog post: {title} — {short edit summary}`. Verified across Inchworm (May 11) + Ship #042 (May 13) edit-pass mirror cycles.

### Step 6: Update Editorial Calendar

**Always invoke the `/update-calendar` skill — never hand-edit `editorial-calendar.csv`.** The skill knows the 18-field column structure + CSV-escape rules (commas in altText, double-quotes in caption, etc.). Hand-editing has produced field-count drift + unescaped-comma bugs (May 17 incident). This rule applies to **all** calendar edits — publish-time (this step), syndication-URL follow-on (after Step 8), workDate corrections, status changes, anything.

Invoke `/update-calendar` with:
- status → `published` (blog-live; changes to `distributed` at Step 8 after cross-posting)
- pubDate → today
- canonicalSite → `distributed` (pipeline dedup signal — set now even though status stays `published` until cross-post)
- blogURL → `https://pipermorgan.ai/blog/{slug}/`
- blogPath → `/blog/{slug}`
- altText, caption from draft metadata

After the skill writes, verify with the canonical validator (Python csv parser; NOT awk-comma-split, which mis-counts on quoted fields):

```bash
python3 scripts/validate-editorial-calendar.py
```

Expected output: `✓ editorial-calendar.csv: N data rows + 1 header, all 18 fields, clean` and exit code 0. Any failure prints the offending row(s) with field count + title preview, exits non-zero.

The validator checks every row in one pass; if you only want to verify a specific row, the inline equivalent is:

```bash
python3 -c "
import csv
with open('docs/internal/planning/comms/editorial-calendar.csv') as f:
    for i, row in enumerate(csv.reader(f), 1):
        if i == TARGET_ROW_NUM: print(f'Field count: {len(row)}'); break
"
```

Expected: 18 fields. If the row reports anything else, an escape went wrong and the skill needs a follow-up pass.

### Step 7: Commit Product Repo

**Apply the commit-discipline opening** per `feedback_clear_index_before_staging_on_shared_main.md` (the product repo is shared `main`; pre-existing index residue from other agents is a real failure mode):

```bash
git reset HEAD  # clear any pre-existing index residue from other agents
git add docs/internal/planning/comms/editorial-calendar.csv
git diff --cached --name-only  # READ EVERY LINE of output before commit
git branch --show-current  # verify branch (separate one-shot)
git commit -m "editorial calendar: {title} published"
git push origin main
```

(The website repo at Step 5 doesn't typically have multi-agent activity; the index-residue discipline applies primarily to product-repo commits.)

### Step 8: PM Syndicates

PM does manually:
1. **Medium**: Paste content, set canonical URL to `https://pipermorgan.ai/blog/{slug}/` (trailing slash!)
2. PM provides Medium URL → Docs updates calendar via `/update-calendar`: set mediumURL, liPubDate/linkedinURL if applicable, and **status → `distributed`** (signals blog + cross-posted; PM-ratified 2026-07-19)

### Step 9: Drafts Folder Cleanup (Final Step)

**ONLY after** verifying:
- ✅ Post is live at `https://pipermorgan.ai/blog/{slug}/`
- ✅ Editorial calendar updated with at least one syndication URL (mediumURL or linkedinURL)
- ✅ Calendar status is `published` (or `distributed` if already cross-posted)

Then archive the draft and source image to keep `docs/public/comms/drafts/` lean:

```bash
# 1. Move final draft to published/
mv docs/public/comms/drafts/{filename}.md docs/public/comms/drafts/published/

# 2. Move any superseded/intermediate versions to superseded/
# (look for draft-{slug}-v1.md, draft-{slug}-v2.md, {slug}-draft.md, etc.)
for f in docs/public/comms/drafts/draft-{slug}*.md docs/public/comms/drafts/{slug}-draft*.md; do
  [ -f "$f" ] && mv "$f" docs/public/comms/drafts/superseded/
done

# 3. Move source image to images-archive/ (the webp is now in production)
mv docs/public/comms/drafts/{image}.png docs/public/comms/drafts/images-archive/
# (also try .jpg, .jpeg if .png doesn't exist)

# 4. Commit
git add docs/public/comms/drafts/
git commit -m "docs: archive {title} draft + image (published)"
git push origin main
```

**Why this is the final step**: Cleanup before verification risks losing the source if the publish fails. Cleanup after syndication confirms the post is live and the local source is no longer the canonical version.

**For ships**: Same procedure but `published/` and `superseded/` apply equally — the ship draft and any working versions get archived after the LinkedIn post is confirmed live.

## Ship Posts

For `category: ship` posts, the workflow is the same except:
- URL prefix is `/shipping-news/{slug}` (not `/blog/{slug}`)
- Image is always `piper-ship.webp` (no per-post image needed)
- Ships may publish without blog-content.json entry (shows LinkedIn link fallback)
- LinkedIn is the syndication target (not Medium)

## Website CSV Format (13 columns)

```
slug,hashId,title,chatDate,imageSlug,imageAlt,imageCaption,workDate,pubDate,category,cluster,featured,notes
```

**Do NOT confuse with the editorial calendar (18 columns).** Different schemas.

## Known Issues (as of v0.5)

1. **Captions**: BlogPostContent doesn't render captions from post metadata for blog-first posts. Captions are stored in the CSV but not displayed. Tracked as a website display bug.
2. **Image sizing**: Featured images may crop poorly depending on aspect ratio. Known design issue.
3. **Large file hook**: Images over 500KB may be rejected by pre-commit. Always compress with `sips -Z 1200` before committing.

## Anti-Patterns to Avoid

| Don't Do This | Why | Do This Instead |
|---------------|-----|-----------------|
| Publish to Medium first | Blog should be canonical | Blog first, then syndicate |
| Use non-hex hashId | Regex extraction fails silently | Always use `uuid.uuid4().hex[:12]` |
| Edit medium-posts.json manually | Gets wiped by `npm run build` | Add data via blog-metadata.csv |
| Use `echo >>` to append CSV rows | May corrupt CSV | Use Python csv writer |
| Skip field count verification | Silent column misalignment | Verify 18 fields (editorial) or 13 (website) |
| Forget trailing slash on canonical URL | Mismatch with site config | `trailingSlash: true` in next.config |

## Quality Checklist

After publishing:
- [ ] Blog post accessible at `https://pipermorgan.ai/blog/{slug}/`
- [ ] Featured image loads correctly
- [ ] Blog index shows post with thumbnail
- [ ] Editorial calendar updated (this repo) with syndication URL(s)
- [ ] Website repo committed and pushed
- [ ] GitHub Pages deploy completed
- [ ] Draft moved to `drafts/published/`
- [ ] Source image moved to `drafts/images-archive/`
- [ ] Any superseded drafts moved to `drafts/superseded/`

---

*v0.16 — **CSV validator extension.** Step 6 verification updated to invoke `scripts/validate-editorial-calendar.py` as the canonical post-write check. The standalone validator parses the whole file via Python csv module, reports field-count drift + header mismatch with exit code 1, prints a clean-pass summary on exit 0. Inline single-row snippet preserved as alternative for targeted checks. Rationale: May 17 hand-edit incident introduced unescaped comma in altText (field count drifted to 19; should be 18); a wrapped standalone validator is easier to invoke + harder to skip than the inline `python3 -c` form. Future: pre-commit hook integration is a candidate enhancement (script is hook-ready — exit codes + stderr surface).*

*v0.15 — **Pre-flight file-existence check codified.** New "Pre-flight: verify files exist" subsection under Prerequisites. Before invoking publish-post.js (dry-run or real), verify both draft and image files resolve at their expected paths via `ls`. Catches "image still in ~/Downloads/" + "placeholder image name in frontmatter" + "wrong filename" before the script errors at image-prep step. Dry-run alone does not catch this — script reports "would prep image" without verifying existence. May 17 *From Protocol to Infrastructure* incident: image was in ~/Downloads/ when PM said "ready to publish"; pre-flight caught it cheaply. Future CLI enhancement candidate flagged in the May 17 feature-corpus memo: `--check` mode for full pre-mutation validation.*

*v0.14 — **Template-first proofread discipline codified.** New "Proofread Discipline (read these first — every time)" section between Draft Metadata Convention and Procedure. Names `blog-post-template.md` + `xian-voice-tone-guide.md` as the canonical references that should be opened on every proofread pass, not consulted from memory. Editorial-calendar workDate/endWorkDate field semantics also surfaced here (source-work-period, not drafting window — per template line 133). May 17 evidence: dateline-semantics drift on *From Protocol to Infrastructure* missed because proofread was anchored on memory pins; PM caught and asked the direct question that surfaced the gap. Cross-references the `feedback_blog_template_and_voice_guide_canonical_for_proofreads` memory pin.*

*v0.13 — **Dry-run mandatory.** New "Always dry-run first" subsection in the CLI invocation block: every real publish MUST be preceded by `--dry-run` with otherwise-identical flags. The dry-run preview catches failure modes the CLI doesn't warn on — empty frontmatter values passed through silently, Markdown features rendering unexpectedly (numbered lists → `<p>` + `<br />` instead of `<ol>/<li>`; inline block-level HTML wrapped in `<p>`), slug/category mismatches, image path resolution. Rationale: May 17 dry-run on *From Protocol to Infrastructure* caught the numbered-list rendering gap before mutation; a non-dry-run path would have published with broken list markup and required edit-pass cleanup. The dry-run is ~5 sec and catches the failure modes that mutate-then-fix costs disproportionately more to recover from.*

*v0.12 — **Filename convention codified.** New "Filename Convention" section between Prerequisites and Draft Metadata Convention. Two filename patterns coexist in `docs/public/comms/drafts/`: `{slug}.md` is PM's working copy (canonical for publish); `draft-{slug}.md` is Comms's earlier draft (sometimes superseded, sometimes the only file). Codified the discipline: `ls docs/public/comms/drafts/ | grep {keyword}` before editing/publishing, to surface both and confirm which is canonical. May 17 incident cited as failure-mode evidence — proofread edits applied to `draft-*` while PM was working in the `{slug}.md` working copy; recommendations transferred by hand. Rule prevents wrong-file edits going forward.*

*v0.11 — **Calendar discipline.** Step 6 strengthened: `/update-calendar` skill is now mandatory for every editorial-calendar edit — never hand-edit `editorial-calendar.csv`. Rationale: hand-editing the calendar on 2026-05-17 (From Protocol to Infrastructure publish) produced unescaped-comma + field-count drift (19 fields when 18 expected; CSV parser caught + fix landed). The /update-calendar skill knows the 18-field column structure + escape rules + which field is which. Hand-editing has no upside and a clear failure mode. Added post-write verification snippet using Python's csv module (NOT awk-comma-split, which mis-counts on quoted fields). Rule applies to all calendar edits: publish-time, syndication follow-on, workDate corrections, status changes.*

*v0.10 — **Script extraction.** The mechanical first half of the skill (parse draft, extract metadata, generate hashId, convert markdown → HTML, prep image, append CSV row, write blog-content.json entry, sync + fetch) is now encoded as `piper-morgan-website/scripts/publish-post.js`. Added the script-invocation block at the top of the skill; preserved the full manual procedure below as the canonical reference for what the script does. Higher-judgment steps (voice-pass, syndication, footer-teaser selection, cross-post, calendar updates, drafts archival) remain skill-owned and unchanged. Rationale: encoding the mechanical pipeline as a single executable narrows the drift surface between docs and reality, reduces orchestration cost per publish, and gives agents a stable CLI surface (`--report=json`, `--dry-run`, kebab-case flags) for future automation integration. Validation: script's markdown converter reproduces the canonical inchworm-position blog-first content byte-for-byte. Web Designer commit `0179571a0` introduces the script.*

*v0.8 — Two changes: (1) **Explicit blog-content.json schema.** Every value MUST be a dict `{"title": "...", "content": "<html>"}` — not a bare HTML string. This applies to all categories (narrative, insight, ship); there is no per-category shape difference. Added a schema section and Python write snippet after Step 3's pipeline sketch. Rationale: in v0.7 the skill said only "add HTML to blog-content.json" with no shape spec, which led to an inconsistency on 2026-04-21 (Four Roles, Ninety Minutes was written as a bare string). The site renderer accepts both shapes, but mixing schemas is a latent bug for any downstream tooling. (2) **Stop stripping non-metadata HTML comments.** Previously, the conversion rule stripped every `<!-- ... -->` line from the body. Now the skill strips only the top-of-file metadata comments (image/alt/caption/no caption) that were consumed during metadata extraction, and preserves all other comments through to the output HTML. Comments are invisible in rendered pages but retain authorial hooks for future retroactive upgrades (inline-image support, canonical-reference annotations, etc.). Rationale: destroying authorial intent is needlessly lossy when the cost of preservation is zero.*

*v0.7 — Two changes: (1) YAML frontmatter added as preferred draft metadata format, HTML comments still supported for backward compatibility. Frontmatter is visible in Markdown editors while HTML comments are hidden. Skill accepts either format; frontmatter takes precedence if both present. Added frontmatter parsing snippet to Step 1 and extended strip-from-output to include the frontmatter block. (2) Heading convention updated: `#` section headings now convert to `<h1>` (previously `<h2>`), while `##` subsections remain `<h2>`. This preserves the heading hierarchy when posts are syndicated to LinkedIn, which was previously collapsing both to the same visual size. Added Comms blog post template at `docs/internal/planning/comms/blog-post-template.md`.*

*v0.6 — Added Step 9 (drafts folder cleanup as final step after syndication confirmed). Cleanup includes: move final draft to published/, superseded versions to superseded/, source image to images-archive/. Rationale: cleanup before verification risks losing source if publish fails. Also documented heading convention: drafts use `#` for section headers (not `##`) because LinkedIn renders `##` as small. Conversion must strip only the FIRST H1 (title) and promote subsequent `#` and `##` to `<h2>`.*

*v0.5 — Added draft metadata convention (comment block for image/alt/caption). Documented hashId must be valid hex. Noted npm run build regenerates medium-posts.json (critical). Added ship post workflow. Added trailing slash requirement for canonical URLs. Removed remote execution mode (unused). Streamlined procedure.*
