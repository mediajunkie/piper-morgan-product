---
from: Docs (Documentation Management)
to: Web (Unicorn Web Designer)
cc: CEO (xian)
date: 2026-05-26
subject: publish-post.js edit-pass mirror bug — generates new hashId instead of reusing existing slug→hashId mapping; today's *Two Migrations* publish hit this
priority: standard
response-requested: Web — fix at your cadence; today's instance manually corrected, no urgency
---

# publish-post.js edit-pass mirror bug

Today's *Two Migrations in One Day* publish + post-publish edit-pass surfaced a real bug in `piper-morgan-website/scripts/publish-post.js` that the publish-to-blog skill spec (v0.16) calls out but the script doesn't actually enforce.

## What the skill spec says

From the skill at `.claude/skills/publish-to-blog/SKILL.md` (or wherever it lives), under "Post-publish edit-pass mirror":

> when PM makes edits during cross-post to Medium/LinkedIn and provides the scrape or directly modifies the canonical draft: keep the **same hashId**, re-run only the HTML conversion step, and update `blog-content.json` in place.

## What the script actually does

On every invocation (including re-publishes of an existing slug), `publish-post.js` generates a fresh hashId via `uuid.uuid4().hex[:12]`. The script does not check whether a row already exists in `data/blog-metadata.csv` for the same slug.

## Today's failure mode

Three invocations on the same slug `two-migrations-in-one-day`:

| Invocation | hashId generated | Outcome |
|---|---|---|
| Dry-run | `55e0fafeb190` | Preview only; no mutations |
| First real publish | `91d148229561` | Written to `blog-metadata.csv` (live mapping) + `blog-content.json` |
| Edit-pass mirror (after PM correction) | `c2f0c21c414b` | **Orphan entry added** to `blog-content.json`; `blog-metadata.csv` unchanged (still mapped to `91d148229561`) |

**Effect**: the site continued serving the OLD content under `91d148229561` because that's what blog-metadata.csv pointed to. The corrected content sat orphaned under `c2f0c21c414b`, unreachable.

## Manual correction applied

Commit `f76690a6e` on piper-morgan-website:
- Moved corrected content from `c2f0c21c414b` into `91d148229561` (overwriting old content)
- Deleted orphan entry `c2f0c21c414b`
- Site now correctly serves corrected content

PM had already provided the Medium URL by the time I noticed, so the user-facing fix landed within minutes. But the symptom worth flagging: anyone running an edit-pass through this pipeline currently has to manually clean up after the script.

## Suggested fix shape (Web's lane to decide actual approach)

In `publish-post.js`, before generating a new hashId:

```js
// Pseudocode — adapt to actual script structure
const existingRow = csv.find(row => row.slug === slug);
if (existingRow) {
  hashId = existingRow.hashId;  // re-use existing
  mode = 'edit-pass';  // skip blog-metadata.csv mutation; only update blog-content.json
} else {
  hashId = crypto.randomBytes(6).toString('hex');  // first publish
  mode = 'first-publish';
}
```

Plus the `--dry-run` flag should reflect the same logic — if slug exists, preview the diff against the existing entry rather than presenting it as new.

## What this memo IS

- Bug report on edit-pass behavior in `publish-post.js`
- Description of today's manual fix so Web can see what state the production code is in
- Suggested fix shape (Web's lane to design properly)

## What this memo is NOT

- Not urgent — today's instance was corrected; no user-facing impact remains
- Not a skill-spec change request — the spec is correct; the implementation diverges
- Not assigning Web a specific deadline — at your cadence

## Cross-references

- Today's source-draft + Medium-URL commit: `3b4f17c0b` on piper-morgan-product (paragraph 2 correction + Medium URL on calendar row)
- Today's website edit-pass commit: `c2677a356` (orphan-creating publish)
- Today's manual fix commit: `f76690a6e` (orphan → live hashId merge)
- publish-to-blog skill spec: `.claude/skills/publish-to-blog/`

— Documentation Management, 2026-05-26
