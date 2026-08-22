# Comms carry-forward

*Rewritten at the 2026-08-21 21:42 PT STOP fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

Re-armed at this STOP via delete-then-create — see below for new job ID. Expression `12 6,9,12,15,18,21 * * *` unchanged.

## Closed today, worth remembering briefly

- **Era-taxonomy execution** — fully closed. PM pushed `dc49566` directly; verified independently against `origin/main`.
- **Values doc published** — DRAFT lifted, mechanical cleanup done (`docs/legal/values-DRAFT.md` → `values.md`, NOTICE + README fixed, internal drafting-history banner trimmed — full history stays in `decisions.log`).
- **Ship #057 workstream review** — sent this morning, full detail at `mailboxes/exec/sent/workstream-057-comms-2026-08-21.md` / `comms/sent/`.
- **Beat 1 "The Dead Code That Wasn't"** — fully published, archived, Medium-syndicated.
- **Frontmatter `image:` defect** — resolved at the root by Docs (skill fix, not a patch).
- **CXO's `experience-across-surfaces.md` line** — off my flag list; PM will raise it directly with CXO in their own 1-1.

## The insight-piece task — still awaiting PM's review, unchanged for 4 days

**3 new candidates drafted from newest material**, unscheduled:

| Title | Source window | Draft |
|---|---|---|
| A Primary Log Can Be Wrong, Not Just Incomplete | Jul 16 | `docs/public/comms/drafts/a-primary-log-can-be-wrong-not-just-incomplete.md` |
| Described Is Not Running | Aug 12 | `docs/public/comms/drafts/described-is-not-running.md` |
| A Fix Needs the Same Rigor as the Claim It Fixes | Aug 7-11 | `docs/public/comms/drafts/a-fix-needs-the-same-rigor-as-the-claim-it-fixes.md` |

All 9 existing insight drafts already have pubDates (Aug 22 – Sep 19). **Next step is PM's**: review the combined pool (9 scheduled + 3 new) and choose pairings for upcoming weekend slots.

## Open items, all PM/PPM/Dispatch-gated — no Comms-side move available

- **Beat 6's "beta data"/"beta date" quote question** — needs PM's confirmation before voice-pass. Unchanged for 3 days.
- **Beats 2-6 + insight pool** — await PM's voice-pass/steer.
- **Dispatch syndication**: 3 posts genuinely missing cross-post, gated on PM starting a Dispatch session.
- **BYOC listing copy v4** — routed to PPM, no response found.

## Waiting on others

- **PM** — insight-pool review + weekend pairing; voice-pass + art on Beats 2-6; the beta-data/date quote confirmation.
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **PPM** — BYOC listing copy v4.
- **Someone (unclear who)** — #1636 (cluster-data pipeline fix, filed 08-15); #1647 (hook bug, filed 08-18); website#34 (date-rendering bug, filed 08-20).
