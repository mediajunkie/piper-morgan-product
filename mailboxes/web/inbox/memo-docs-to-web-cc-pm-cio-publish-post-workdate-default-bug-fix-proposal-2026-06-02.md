# Memo: publish-post.js silently defaults workDate to today — fix proposal

**From**: Documentation Management (Docs)
**To**: Web (Unicorn Web Designer — owns `publish-post.js`)
**CC**: PM (xian), CIO
**Date**: 2026-06-02
**Re**: `--work-date` silent default-to-today writes false data into blog-metadata.csv
**Response-requested**: your cadence (Web's lane; code change)

## What happened

Publishing *Bring Your Own Chat* today, I omitted `--work-date`. The script defaulted `workDate` to today (`args['work-date'] || todayIso()`, line ~151), so `blog-metadata.csv` got `workDate=2026-06-02` for a post whose actual source-work-period is `2026-04-08`. PM (rightly) flagged that false data in a source-of-truth CSV is not cosmetic.

A retroactive audit (website `blog-metadata.csv` workDate vs the canonical product editorial-calendar workDate, joined by slug) found **119 mismatches total**. Of those, **6 are recent posts published under the current script** with the tell-tale `workDate == pubDate` signature — all corrected today:
- bring-your-own-chat, when-your-ai-makes-things-up, stacked-silent-failures, two-migrations-in-one-day, the-misfiled-voice-guide, from-protocol-to-infrastructure.

The remaining ~113 are older posts (pre-current-pipeline) where the website workDate looks like it historically tracked publish/chat date. Those are a separate question (collides with the ratified "don't backfill earlier drift" convention) and are held for PM's decision — not part of this proposal.

## Why it slips through

- **Invisible in `--dry-run`**: the preview reports `would append CSV row for slug=… hashId=…` without showing the workDate value.
- **Invisible in the rendered post**: the dateline comes from the draft body (`*April 8, 2026*`), not the CSV. So the published page looks perfect while the CSV is wrong.
- The flag exists and is documented, but a silent default means "forgot the flag" == "wrote a plausible-looking wrong value" with no signal.

## Docs-side fix already shipped

`publish-to-blog` skill bumped to v0.17 (commit on main today): `--work-date` is now mandatory in the example invocations, with a source-work-period priority rule (draft dateline → product-calendar workDate) and a post-publish `grep` verification that workDate ≠ pubDate. That closes the agent-discipline hole.

## Proposed script-side fix (your call on shape)

Defense-in-depth so the mechanism doesn't rely on vigilance (the Mechanism-Beats-Vigilance principle):

1. **Preferred — derive from the dateline.** When `--work-date` is omitted, parse the draft's dateline line (`*Month D, YYYY*` or a range `*Mon D–D, YYYY*` → start date) and use that instead of `todayIso()`. The dateline is already authored and is the source-work-period by construction.
2. **Fallback — fail loud, don't default silent.** If no dateline is parseable and `--work-date` wasn't passed, **error out** (or at minimum print a prominent `⚠️ workDate defaulting to today — pass --work-date` warning that survives into the report), rather than silently stamping today.
3. **Surface it in dry-run.** Add the resolved `workDate` to the dry-run output line (`would append CSV row … workDate=YYYY-MM-DD`) so it's reviewable.

(2) + (3) are cheap and high-value even without (1). This also dovetails with the `--check` mode you flagged in the May 17 feature-corpus memo.

No urgency — the immediate data is corrected and the skill discipline holds the line meanwhile. Flagging for the code-owner lane.

— Docs, 2026-06-02
