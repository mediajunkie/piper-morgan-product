# Comms carry-forward

*Updated at the 2026-08-20 18:42 PT WORK fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Era-taxonomy execution — DONE, blocked only on PM's push

PM ratified the Aug 15 era-taxonomy proposal today and asked me to execute it. Fully done and verified in `/Users/xian/Development/piper-morgan-website-worktrees/comms` (a new worktree I created — the website repo had none for comms), commit `dc49566` on `claude/comms-cycle`:

- Added Era 6 "The Mechanism" (Apr 1–Jul 31, 86 posts) and Era 7 "The Alpha" (Aug 1–present, open-ended) to `src/lib/episodes.ts`
- Assigned `cluster` by pubDate in `data/blog-metadata.csv` + synced to `medium-posts.json` (86 mechanism + 15 alpha — grew from the original 8+3 estimate since the 3 posts missing on Aug 15 have since published normally)
- Found + fixed a real pre-existing bug along the way: era date ranges rendered one day early (UTC-midnight-in-Pacific-build). Fixed at the 3 sites this feature touches; filed **website#34** for the other 7 site-wide call sites with the same pattern (deliberately not swept — separate, larger fix)
- Also fixed stale hardcoded "5 eras... May 2025 - March 2026" hero/metadata copy on the episodes page, now computed from `ERAS.length` so it won't go stale again
- Verified via full `next build` + direct HTML inspection: Era 7 shows "15 posts", "Aug 1 - Present"

**Blocked**: pushing to the website repo's `origin/main` was denied by the permission classifier (I don't normally push there — only the product repo). Gave PM the exact command (`cd .../piper-morgan-website-worktrees/comms && git push origin HEAD:main`) at end of last turn. **As of this fire (18:42), still not pushed** — `dc49566` is local-only, 1 commit ahead of origin/main. Nothing further for me to do here; checking each fire whether it landed.

## Beat 1 "The Dead Code That Wasn't" — fully published + archived

Published and archived by Docs sometime after the 15:42 fire (calendar row updated, `blogURL`/`canonicalSite`/`altText`/`caption` filled, images archived, draft moved to `published/`). Closed thread, nothing further needed.

## 2026-08-20 START — quiet fire, one item resolved

- **Ship #056's LinkedIn-URL calendar gap (flagged last night as "observed, not actioned") is now resolved** — Docs picked it up overnight (`5f12abcb3`, `15d183b5c`); verified directly against the calendar row, not just the commit message: `status=distributed`, `liPubDate=2026-08-19`, `linkedinURL` populated.
- **Today's scheduled slot**: Beat 1 "The Dead Code That Wasn't" (pubDate today, Aug 20) — still `status=drafted`, awaiting PM's voice-pass + art. No new engagement.
- Mail inbox empty (0 memos). No overnight movement on any standing PM-gated thread — see list below, unchanged.

## Cron

Re-armed at this STOP via delete-then-create — see below for new job ID. Expression `12 6,9,12,15,18,21 * * *` unchanged.

## The insight-piece task — categorized, 3 new candidates drafted, still ready for PM's review

**Categorization** (queried the live calendar directly): all 9 existing insight drafts already have pubDates (Aug 22 – Sep 19) — nothing sits in "planned but unscheduled" limbo.

**3 new candidates drafted from newest material**, unscheduled, still awaiting PM's review — unchanged for 2 days now:

| Title | Source window | Draft |
|---|---|---|
| A Primary Log Can Be Wrong, Not Just Incomplete | Jul 16 | `docs/public/comms/drafts/a-primary-log-can-be-wrong-not-just-incomplete.md` |
| Described Is Not Running | Aug 12 | `docs/public/comms/drafts/described-is-not-running.md` |
| A Fix Needs the Same Rigor as the Claim It Fixes | Aug 7-11 | `docs/public/comms/drafts/a-fix-needs-the-same-rigor-as-the-claim-it-fixes.md` |

**Next step is PM's**: review the combined pool (9 scheduled + 3 new) and choose pairings for upcoming weekend slots.

## Yesterday's incident — fully resolved, filed as #1647

Merge-conflict cascade caused a brief, fully-corrected regression of ~18 mailbox files off `origin/main`; fixed via `mail-send.sh` same session. Full trace: `dev/active/URGENT-mailbox-regression-2026-08-18.md` (RESOLVED). #1647 (hook bug) still unowned.

## Today (Aug 19) — quiet for Comms specifically

- **Weekly Ship #056** drafted, voice-passed, and published entirely by Exec/Docs/PM — no Comms review request came, matching the established pattern. A hero-image 404 (also found on Ship #054) was caught and fixed by a general-purpose session, filed as website#33 for a mechanical guard.
- **Observation, not actioned**: Ship #056's calendar row still has empty `linkedinURL`/`liPubDate` despite a cross-post-live request sent to Docs ~2.5 hours before this STOP. Calendar URL columns are Docs' exclusively — watch tomorrow whether it's been picked up, don't touch it myself.
- No movement on any of my own standing threads all day.

## Open items, all PM/CXO/PPM/Dispatch-gated — no Comms-side move available

- **Beat 6's "beta data"/"beta date" quote question** — needs PM's confirmation before voice-pass. Unchanged for 1 day.
- **Beats 1-6 + insight pool** — all await PM's voice-pass/steer.
- **Era-taxonomy proposal** — still awaiting PM's ratification, unchanged since Aug 15 (now 4 days).
- **CXO's §3 entity-model line** in `docs/internal/design/experience-across-surfaces.md` — flagged 3×, still pending.
- **Dispatch syndication**: 3 posts genuinely missing cross-post, gated on PM starting a Dispatch session.
- **BYOC listing copy v4** — routed to PPM, no response found.

## Waiting on others

- **PM** — insight-pool review + weekend pairing; era ratification; voice-pass + art on Beats 1-6; the beta-data/date quote confirmation.
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **PPM** — BYOC listing copy v4.
- **CXO/PM** — entity-model ratification.
- **Lead** — outcome of #1611 (routed by Docs).
- **Someone (unclear who)** — #1636 (cluster-data pipeline fix, filed 08-15); #1647 (hook bug, filed 08-18).
