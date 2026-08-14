# Comms carry-forward

*Rewritten at the 2026-08-13 21:44 PT STOP fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

✅ **ARMED — job `45eae89f`, re-armed at 2026-08-13 STOP via delete-then-create** (was `6d5f873a`). Same expression `12 6,9,12,15,18,21 * * *`. `CronList`-verified exactly one job. Auto-expires ~2026-08-20.

## The one thing to do first tomorrow

⭐ **Values doc with HOST — drafting is what's deferred, not the whole thread.** HOST delivered a genuine first pass tonight: three identity-defining commitments (structural no-cross-user-learning enforced by ADR-079's CI ratchet + the #1366 precedent; the user-visible ethics-audit read surface, ADR-063/PM-087; the hash-only audit-log design from Pattern-071), each tested against "would a fork dropping this quietly still look like us." Also caught a real landmine before I walked into it: **don't reach for "you control your data" as a strength claim** — account deletion doesn't exist, conversation deletion is soft-only (`docs/legal/data-retention-policy-DRAFT.md`). Replied tonight confirming the list and absorbing the caution — mail `131d95252`. **What's actually deferred**: producing the document's real prose, deliberately, because that deserves undivided attention, not the tail of a six-fire day. No deadline from PM either way.

## pmorgan.tech register pass — status, still holding

Tiers 1–6 done. **Tier 6 surfaced 2 real content bugs** (broken install tutorial — wrong folder name + missing clone step; an Amber/Pard internal-infra warning leaked into a tester-facing file) — sent to Docs+CIO+PM, commit `b3417c12e`, **no reply yet as of STOP**. Next per Docs' order would be `api/` + `public/api-reference/`, then `testing/`+`releases/` last — **but check for their reply on the tier-6 bugs first**, don't restart tier 7 unprompted a second time in a row.

## Filed/flagged, not fixed

- **#1610**: ✅ CLOSED (PM decided addresses, Docs fixed all 4 docs).
- **#1611**: `mac-dock-integration.md` architecture question, routed to Lead by Docs.
- **~30 broken links** across tiers 3-6 — most already repointed by Docs; tier 5's 2 + tier 6's 1 sent, unconfirmed.
- Systemic "Documentation Home → repo-root README" link pattern (64 files) — flagged, Docs already sweeping.

## Beat 22, "Alpha Launches" — ✅ fully closed, published + distributed

Live at `https://pipermorgan.ai/blog/alpha-launches/`, Medium cross-post done, calendar shows `distributed` (Docs actioned PM's direct calendar-update request — confirmed via git log, not touched by me, correctly out of scope per the 07-29 process change). Nothing left here.

## LinkedIn cover-image automation — dead, documented

Both automation paths (MCP file-upload, clipboard paste) confirmed dead by PM 08-12; manual upload is now the documented default, not a fallback. Added a one-line note to `content-publishing-run-of-show.md` Step 7 so future handoffs don't re-attempt or file a bug for it. Closed.

## Open items, all PM/CXO/PPM/Dispatch-gated — no Comms-side move available

- ⭐ **Beats steer.** 8 candidates for 7 slots; narrative queue runs dry after Aug 18. Artifact: `docs/internal/planning/comms/upcoming-beats-plan.html`.
- **Beat 23** (Aug 18) still needs PM's voice-pass + art.
- **CXO's §3 entity-model line** in `docs/internal/design/experience-across-surfaces.md` — flagged 3×, still pending.
- **Dispatch syndication**: 3 fully unsyndicated posts, 1 partial. Checked repeatedly, nothing new.
- **BYOC listing copy v4** — open question routed to PPM.

## Waiting on others

- **Me, next fresh session** — actually drafting the values doc, once picked up deliberately.
- **PM** — Beats 24–28 steer; voice-pass + art on Beat 23.
- **PPM** — BYOC listing copy v4 blocker.
- **CXO/PM** — entity-model ratification.
- **Dispatch** — syndication for the 4 posts above.
- **Docs** — reply on tier-6 bugs (broken tutorial's missing Steps 9-10, the Amber/Pard warning's proper home); tier 7 priority confirmation.
