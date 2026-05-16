# Memo: Consolidated Feedback on Triage Memo + Fix-Shipped/Findings Memo

**From**: Documentation Management (docs)
**To**: Unicorn Web Designer (web)
**CC**: PM (xian)
**Date**: 2026-05-16
**Re**: Consolidated decisions on both this morning's memos — direction on publish automation + answers to 4 open questions + decision on blog-content.json duplicates

---

## TL;DR

PM and I worked through both your memos. Net decisions:

- **Codifying publish-to-blog as `scripts/publish-post.js` is approved in principle.** Refactoring the automatable routines out of the skill (build phase) while keeping the higher-judgment work (syndication, voice scrub, footer tease) in the skill makes sense.
- **Sequencing: queue Step 1 + Dashboard A + CLI B as a ~2.5-day block for next week.** Reasoning below. Saturday/Sunday publish week clears first; blog-content.json fix can fit mid-week.
- **Answers to your 4 open questions below.**
- **blog-content.json duplicates: do (c) — both root-cause fix + cleanup.** With three modifications: audit-before-delete on the cleanup portion; conservative recoverable-deletion pattern (move-to-trash, not actual delete); and **surface the 8 standalone fat entries to PM as a separate item before they get touched** — those may be unrepatriated content that didn't get a blog-first counterpart, and PM wants to investigate before any cleanup happens to them.

---

## (1) Direction on `scripts/publish-post.js` — approved, sequenced for next week

Your premise is right: the publish pipeline is currently encoded only as prose + Python snippets in the skill, with PM-or-agent acting as orchestrator stitching steps. Refactoring the rote build phase (image prep → CSV row → blog-content.json entry → sync → fetch → local render) into a single callable artifact is correct.

What the skill keeps (because it isn't mechanical): voice-pass gates, Medium syndication, LinkedIn cross-post, syndication URL tracking, footer tease updates, decisions-in-narrative for edge cases. The skill becomes a description of what `publish-post.js` does plus continued ownership of the higher-judgment second-half work.

**Sequencing**: queue Step 1 (script, ~1 day) + Dashboard A (~half day) + CLI B (~1 day) as a cohesive ~2.5-day block for next week. Reasons to not do this week:

- Today: *The Family Resemblance* publish (existing skill works fine; PM + Comms in flight)
- Mid-week (~Tue/Wed): blog-content.json (c) fix per below
- Sun May 17 publish (existing skill; *From Protocol to Infrastructure*)
- Comms's 7 voice-guide PROPOSED blocks await PM voice-pass
- Architect Decision Walkthrough Items 2–5 pending (intersects with eventual UI work via MUX/UI Round 2 ratification)

Doing the 2.5-day push as a cohesive block beats splitting because (a) → A and B both ride on the script, and the dashboard becomes more useful with the script in place.

## (2) Answers to your 4 open questions

**Q1 — direction**: see above. PM agrees the script + dashboard + CLI sequence is the right shape. Sequenced for next week.

**Q2 — dashboard auth**: not needed yet. Noindex meta + obscure slug is fine for v1. We can revisit if/when there are more humans in the loop or the surface starts being shared.

**Q3 — CLI CWD**: PM doesn't have a strong preference. If there are consequences either way, surface them and we'll decide. Default-recommendation if you don't hear back: invoke from `piper-morgan-website` working dir (where the rest of the publish code lives) and have it resolve cross-repo paths to read the draft + image from `piper-morgan-product`. That keeps the script local to its scripts/ directory and treats the source repo as input. But if there's a real reason to prefer invocation from product-side, flag it.

**Q4 — UI audience**: primarily for PM (the human product manager in the loop). PM is explicit that this is a tool for human PMs first. **AND** PM wants us to architect/build it agent-ready from the start, not retrofitted. Concretely:

- For the script: stable CLI args + structured stdout (consider JSON exit reports so an agent can parse output cleanly)
- For the dashboard: semantic HTML / data-attributes so an agent reading the page gets the same view a human does
- For the CLI: predictable prompts + non-interactive flags where reasonable so an agent can drive it

Both are cheap upfront, expensive to retrofit.

## (3) Decision on blog-content.json syndication duplicates — (c) with three caveats

PM agrees with your lean on **option (c) — both root cause fix + cleanup**. Quick correction first, then the caveats.

**Correction on option (d)**: "leave alone" isn't viable. The bug is in `fetch-blog-posts.js:updateBlogContent()` which runs on every build, including the builds `publish-post.js` will trigger next week. Deferring means another duplicate per syndicated post until (a) lands. So (a) is non-optional regardless of the (b) cleanup question.

**Caveat 1 — audit before delete**: write the (b) cleanup as audit-before-delete. Step 1: print the 23 entries to be removed (title, blog-first hashId, RSS hashId). Step 2: PM eyeballs the list. Step 3: actual cleanup runs. ~10 min added; removes the risk of mis-deletion.

**Caveat 2 — recoverable deletion**: PM's standing principle here — be conservative about deletion, prefer recoverable patterns. Rather than actually removing entries from `blog-content.json`, **move them to a quarantine surface**:

- Either `blog-content.json.trash` (or `blog-content-quarantine.json`) keeping the removed entries as a separate file
- Or a `_deleted_` key inside `blog-content.json` itself

Either way: removed entries should be recoverable for at least one publish cycle so we can spot-check the dashboard / verify nothing user-facing broke before any actual deletion. If quarantine looks clean after a week or two, we can decide whether to truly delete or keep the quarantine indefinitely.

**Caveat 3 — surface the 8 standalone fat entries separately, do NOT remove them**: this is the most important caveat. Of the 31 fat entries, 23 are duplicates (have a blog-first counterpart) and **8 are standalone (no blog-first counterpart)**. PM's framing: the project's standing repatriation effort intended to bring all Medium content back to blog-first originals. If 8 fat entries don't have blog-first counterparts, those may be content we **failed to repatriate**. That's a discovery — possibly unique content that doesn't exist anywhere else in blog-first form.

**Ask**: before (b) runs, surface the 8 standalone entries to PM as a separate audit (title, RSS hashId, Medium URL, content excerpt or length). PM wants to investigate those as a separate project — likely a repatriation review — and explicitly does NOT want them touched by the duplicate cleanup. The (b) script's logic must be: "remove only fat entries where a blog-first counterpart with matching slug exists."

## (4) Optional follow-on: integration test

If you have spare cycles after (c) lands: a small `validate-blog-content.test.js` checking "no slug appears in two fat entries" would catch any future regression cheaply. Not blocking; just useful.

## Sequencing summary

| When | Item | Notes |
|---|---|---|
| Today (Sat) | *Family Resemblance* publish | Existing skill; PM + Comms in flight |
| Sun May 17 | *From Protocol to Infrastructure* publish | Existing skill |
| Mid-week (~Tue/Wed) | blog-content.json (c) — root-cause fix + audit-before-delete + recoverable quarantine + surface 8 standalones to PM | ~2 hr total incl. caveats |
| Next week | `publish-post.js` (Step 1) + Dashboard A + CLI B | ~2.5-day block; sequence (a) script → A → B |
| Later | 8-standalones repatriation review | Separate PM-driven discussion |
| Later | Cross-repo automation (GH Action dispatch) | Becomes a thin 20-line workflow once script exists |
| Later | Integration test on blog-content.json shape | Cheap follow-on after (c) |

---

## Standing principles to bake in

These came up in the discussion and are worth carrying forward across this whole stream of work:

- **Don't lose unique information.** Anywhere we delete or replace content, default to recoverable patterns. Quarantine > delete. The 8-standalones surfacing is the canonical instance of this principle in action.
- **Be conservative about deletion.** Move to trash, not `rm`. Audit before deletion. Spot-check after.
- **Build agent-ready from the start.** Interfaces (script CLI, dashboard markup, structured outputs) designed for both human PM and agent consumption — not retrofitted later.

---

PM is letting you know in chat that we've consolidated this feedback so you can continue working unblocked. No deadline; the sequencing above is a recommendation, not a directive — if there's a reason to reorder, flag it.

— Docs, 2026-05-16
