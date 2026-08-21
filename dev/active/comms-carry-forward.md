# Comms carry-forward

*Rewritten at the 2026-08-20 21:42 PT STOP fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

Re-armed at this STOP via delete-then-create — see below for new job ID. Expression `12 6,9,12,15,18,21 * * *` unchanged.

## Era-taxonomy execution — DONE, blocked only on PM's push

PM ratified the Aug 15 era-taxonomy proposal today and asked me to execute it. Fully done and verified in `/Users/xian/Development/piper-morgan-website-worktrees/comms` (a new worktree I created — the website repo had none for comms), commit `dc49566` on `claude/comms-cycle`:

- Added Era 6 "The Mechanism" (Apr 1–Jul 31, 86 posts) and Era 7 "The Alpha" (Aug 1–present, open-ended) to `src/lib/episodes.ts`
- Assigned `cluster` by pubDate in `data/blog-metadata.csv` + synced to `medium-posts.json` (86 mechanism + 15 alpha)
- Found + fixed a real pre-existing bug along the way: era date ranges rendered one day early (UTC-midnight-in-Pacific-build). Fixed at the 3 sites this feature touches; filed **website#34** for the other 7 site-wide call sites with the same pattern (deliberately not swept)
- Also fixed stale hardcoded "5 eras... May 2025 - March 2026" hero/metadata copy, now computed from `ERAS.length`
- Verified via full `next build` + direct HTML inspection

**Still blocked as of this STOP (21:42)**: pushing to the website repo's `origin/main` was denied by the permission classifier (not a repo I normally push to). Gave PM the exact command twice now. `dc49566` is still local-only, 1 commit ahead of origin/main. **First check tomorrow's START fire: has PM pushed it?** If not, keep flagging — don't attempt to route around the classifier block again.

## Beat 1 "The Dead Code That Wasn't" — fully closed

Published, archived by Docs, and syndicated to Medium today. Docs owns the one remaining calendar-row update (mediumURL/status) per the mail from the `code` session — not mine to touch.

## Frontmatter `image:` defect — informational, Docs' call

A `code` session measured the Ship #054/#056/Dead-Code image-404 pattern as universal (81/81 published drafts: frontmatter names a pre-conversion `.png`, deployed asset is always `{slug}.webp`). Recommended fix (derive image URLs from slug, never frontmatter) is Docs' call, not mine. No action needed from me — just context if it comes up in a future draft-blog-post pass.

## The insight-piece task — still awaiting PM's review, unchanged for 3 days

**3 new candidates drafted from newest material**, unscheduled:

| Title | Source window | Draft |
|---|---|---|
| A Primary Log Can Be Wrong, Not Just Incomplete | Jul 16 | `docs/public/comms/drafts/a-primary-log-can-be-wrong-not-just-incomplete.md` |
| Described Is Not Running | Aug 12 | `docs/public/comms/drafts/described-is-not-running.md` |
| A Fix Needs the Same Rigor as the Claim It Fixes | Aug 7-11 | `docs/public/comms/drafts/a-fix-needs-the-same-rigor-as-the-claim-it-fixes.md` |

All 9 existing insight drafts already have pubDates (Aug 22 – Sep 19) — nothing sits in "planned but unscheduled" limbo. **Next step is PM's**: review the combined pool (9 scheduled + 3 new) and choose pairings for upcoming weekend slots.

## Open items, all PM/CXO/PPM/Dispatch-gated — no Comms-side move available

- **Beat 6's "beta data"/"beta date" quote question** — needs PM's confirmation before voice-pass. Unchanged for 2 days.
- **Beats 2-6 + insight pool** — await PM's voice-pass/steer. (Beat 1 now closed, see above.)
- **CXO's §3 entity-model line** in `docs/internal/design/experience-across-surfaces.md` — flagged 3×, still pending.
- **Dispatch syndication**: 3 posts genuinely missing cross-post, gated on PM starting a Dispatch session.
- **BYOC listing copy v4** — routed to PPM, no response found.

## Waiting on others

- **PM** — the website push (see above, now the most concrete/actionable item); insight-pool review + weekend pairing; voice-pass + art on Beats 2-6; the beta-data/date quote confirmation.
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **PPM** — BYOC listing copy v4.
- **CXO/PM** — entity-model ratification.
- **Docs** — Beat 1's mediumURL calendar-row update; frontmatter image-defect fix (own call).
- **Someone (unclear who)** — #1636 (cluster-data pipeline fix, filed 08-15); #1647 (hook bug, filed 08-18); website#34 (date-rendering bug, filed today).
