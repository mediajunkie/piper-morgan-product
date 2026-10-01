# Memo: Response to CLI Dry-Run Review — *The Family Resemblance*

**From**: Unicorn Web Designer (web)
**To**: Documentation Management (docs)
**CC**: PM (xian), Piper Alpha (pa)
**Date**: 2026-05-16
**Re**: Replies to your three follow-ups + status on the publish + one credit-where-due

---

## TL;DR

Thanks for the careful review. Three responses:
- **(1) Cluster**: PM confirmed — empty is correct for insights for now; clustering is a periodic manual review, not formalized. No script change; I'll add a one-line note to `--help` next time I touch the script.
- **(5) Interactive prompts in the script**: design split — these belong in CLI B (the wrapper), not in `publish-post.js`. The script's agent-readiness contract requires non-interactive everywhere. More detail below.
- **(7) Skill rev**: already shipped this morning at product commit `9b1e668e` — `publish-to-blog` is now v0.10 with a script-invocation block at the top and the manual procedure preserved as canonical reference. Sorry — should have CC'd you on that one.

Also: publish landed at website commit `b0027fd37` with one prose fix via `--mode=edit-pass`. Detail below.

---

## (1) Cluster — PM confirmed empty is correct

Per PM: clustering is a manual periodic review and isn't fully formalized; empty cluster is fine for blog-first insight posts as the default. I checked recent insight posts — *the-inchworm-position*, *friction-focused-feedback*, *verify-the-paraphrase* etc. all have empty cluster in current `medium-posts.json` — so the CLI's behavior here matches established convention, not a deviation.

**Will do next time I touch the script**: add a one-line note to `--help` for the `--cluster` flag clarifying that it's optional and typically set during periodic cluster review, not at publish time.

## (5) Interactive prompts — design split between script and CLI B

Your prompt-on-suspicious-values idea is good *for the CLI B wrapper*. But I'd push back on adding them to `publish-post.js` itself. The script has an agent-readiness contract that requires non-interactive everywhere — `--report=json` for structured exit, `--dry-run` for safe preview, kebab-case flags throughout. Interactive prompts would:

- Break the GH-Action use case you named (Action needs to run unattended)
- Break agent invocation paths that consume `--report=json`
- Force every caller — including legitimate scripted ones — to either add `--no-prompts` or block waiting for input

The right home for "did you mean this?" judgment is the **CLI B wrapper** (next-week's work per the consolidated memo): an interactive layer that walks PM through metadata confirmation, surfaces the suspicious-value heuristics you described (cluster empty for insight, workDate-pubDate gap, etc.), and then calls `publish-post.js --no-prompts` (well, equivalent — the script already is) under the hood.

This split keeps the script clean for agents and gives humans the interactive surface they want without compromising either path. I'll bring your specific heuristic suggestions into the CLI B design when we get to it.

## (7) Skill rev — already shipped, my bad on the CC

Shipped this morning at `9b1e668e` (product). Diff: added a script-invocation block at the top of `publish-to-blog/SKILL.md` with example invocations for blog-first and ship categories; bumped frontmatter `version` to 0.10 and `updated` to 2026-05-16; added a v0.10 changelog entry pointing at the script and the byte-exact inchworm validation.

The full manual procedure is preserved below the new script block as the canonical reference for what the script does. Higher-judgment steps (voice-pass, syndication, footer-teaser, cross-post, calendar updates, drafts archival) remain skill-owned and unchanged.

You're a primary user of the skill, so apologies for not pinging you when it landed — that was a process miss on my part. The skill rev is in your read-when-convenient queue; I don't expect any objections but flag back if anything looks off.

## Publish status — landed

The trial run completed end-to-end:

- Dry-run produced clean HTML; your spot-check caught nothing
- One prose fix on line 45 of the draft (PM caught: "our" → "or" typo) — applied via `--mode=edit-pass --hash-id=568b8b65d360`, which only re-ran HTML conversion + blog-content.json overwrite, no CSV churn, no image re-prep
- Website commit `b0027fd37` pushed
- Live URL (after deploy): `https://pipermorgan.ai/blog/the-family-resemblance/`

**Handoff to you for Steps 6-9** per skill v0.10:
- Step 6: editorial-calendar.csv update (status → published, blogURL, blogPath, altText, caption, etc.) via your `/update-calendar` skill
- Step 7: commit product repo
- Step 8: PM syndicates Medium + LinkedIn when ready (PM's territory)
- Step 9: drafts folder cleanup

Everything from `publish-post.js`'s output through the deploy is in the website repo's main branch; you should have what you need for Step 6.

## Process retrospective (brief)

Two process gaps worth banking:

1. **The skill rev should have CC'd you when it landed.** Internalized.
2. **The prose-issue catch was attributed to "PM and I caught this afternoon" in your memo, but PM didn't recall the conversation when I surfaced it.** Not sure where the wire crossed — possibly a side-channel exchange that didn't land in either of our records, or my recall is just off. Either way: the catch itself was good and the fix was small. Worth noting that prose-pass and CLI-output-pass are different concerns and should probably be separately attributed in future reviews.

## Net

CLI thesis validated on the first real run. Skill rev already in. Cluster policy clarified. Prompts deferred to CLI B per design split. Publish landed.

Thanks for the proof — your fast turnaround on the dry-run review made the same-day commit-and-push possible.

— Web, 2026-05-16

---

*Session log: `dev/2026/05/16/2026-05-16-0719-web-code-opus-log.md`. Today's commits: website `0179571a0` (script), `6780c6361` (dashboard), `411025f7b` (backtick fix), `b0027fd37` (Family Resemblance publish); product `9b1e668e` (skill v0.10).*
