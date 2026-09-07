# Comms carry-forward

*Rewritten at the 2026-09-06 21:12 PT STOP fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

`666546f1`, expression `12 6,9,12,15,18,21 * * *`, re-armed via delete-then-create at this STOP (was `000c85d0`).

## Closed today

- **Duplicate-post incident traced and fixed.** PM caught today's scheduled insight ("Patterns Naming Patterns") was substantively a re-run of the already-published "This One's Taken." Traced the exact root cause via git history: a June fork mislabeled as a "rename" left the original orphaned; a July orphan-rescue found it, verified it wasn't byte-identical to anything, and rescheduled it without checking whether the *story* had already published under a different title. PM confirmed skip-today. Full cleanup: duplicate retired to `drafts/superseded/`, calendar row removed, incident documented, stale footer fixed, gap closed durably in `draft-blog-post` skill v1.3 (workDate-overlap detection for retitled forks, not just literal duplicates).
- **website#39 + #41 fully closed, same day.** PM asked why the new era-clustering was "completely broken" and whether Web needed more help. Investigated rather than relay the question: pulled the actual post data, found Web's diagnosis (workDate-based, "judgment-based") was checking the wrong date field — publish date makes the whole assignment 100% mechanical, zero ambiguous cases across 389 posts. Computed the full 288-post backfill, handed to Web (didn't execute the data write myself — unfamiliar pipeline conventions). Web independently re-derived the same mapping, shipped it, found and closed one more real defect (an orphan JSON duplicate, #41) same-day.
- **Live footer thread closed** — Docs pushed the fix flagged Saturday; confirmed no need to chase Medium/LinkedIn for a teaser mismatch.
- **Acknowledged a new cohort-wide standing rule**: probes under ~25 API calls proceed without asking, report cost with result. Doesn't come up often on this lane; noted for future live-site/GH-API work.

## Open items — no Comms-side move available right now

- **12 drafts in the queue** — 8 building beats (Sep 8 through Oct 1) + 4 insights (Sep 6 pubDate now open again since the duplicate was pulled, Sep 12, Sep 13, Oct 3), all `drafted`, all await PM's voice-pass + art. **Note**: today's Sep 6 slot is now empty (skipped) — worth PM knowing there's no post landing today, and the queue may want a look at whether to backfill that slot from the remaining drafted pool or just let the cadence continue from Sep 8's Ship/beat schedule.
- **ChicagoCamps talk** — PM reviewing script/slides; script + slide plan at `dev/2026/08/29/chicagocamps-talk-2026-09-17.md`. Dry-run window closed Sep 5 with no signal — not chasing further.
- **website#35** — PM watching for recurrence, not actively pursuing.
- **BYOC listing copy** — held per the ESSENCE ratification (MCP stays in Production); the marketplace *narrative* piece is a separate artifact, already published (not blocked by this).
- **Series structure (era split + blog-index featuring)** — the *data-correctness* half (website#39/#41) is now fully resolved; the *structural* question (splitting Era 2, blog-index featuring) remains separately open, PM/Web's call.

## Waiting on others

- **PM** — voice-pass + art on 12 drafted items; ChicagoCamps script/slide review.
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **Someone (unclear who)** — #1636 (filed 08-15); #1647 (filed 08-18).
