# Comms carry-forward

*Rewritten at the 2026-08-13 09:48 PT fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

✅ **ARMED — job `6d5f873a`.** Same expression `12 6,9,12,15,18,21 * * *`. Auto-expires ~2026-08-19.

## pmorgan.tech register pass — status

**Tiers 1–3 all touched. Not the whole ~160-file KEEP surface — naming the denominator:**

- ✅ **Tier 1, `dev-tips/` (5 files, the CIO obligation)** — done. Commit `d5b1eca37`.
- ✅ **Tier 2, five `ALPHA_*` docs** — done. Commit `9f6ab1732`.
- ✅ **Tier 3, `guides/` (15) + `getting-started/` (3 current files)** — 17 of 18 done, 1 (`mac-dock-integration.md`) deliberately left untouched, filed as #1611. Commit `c6dcc2074`.
- ⬜ **Not started**: the rest of the KEEP list — `public/user-guides/` (16), `installation/` (7), `features/` (5), `integrations/` (3), `configuration/` (2), `setup/` (2), `troubleshooting/` (2) + `troubleshooting.md`, `api/` (3), `public/api-reference/` (7), and more. Docs hasn't named a next priority within this remainder yet — check for a follow-up memo before picking a starting point, since their own staleness+link pass may surface a better order.

## Filed this morning, not fixed — need someone else

- **#1610**: `ALPHA_AGREEMENT_v2.md` ships with a literal `[contact email]` placeholder — open since Oct 2025, duplicated in 2 other docs. Needs PM's actual address.
- **#1611**: `mac-dock-integration.md` is built around PM's own "6:00 AM PT standup" routine and describes what looks like a stale two-process architecture (port 8081) contradicting every current doc. Needs architecture verification + a scoping call, not a register fix.
- **18 broken links** (9 files) pointing at content the scoping proposal excluded — sent to Docs as a memo (`2026-08-13-comms-to-docs-cc-cio-pm-tier-3-findings-broken-links-plus-two-filed-issues.md`) with the full file:line list, not fixed myself (their dimension, and 18 instances is too many to guess a repointing pattern for).

## PM capacity note — may still apply this morning

PM has been running the team on borrowed DesignXProduct tokens; own account access was expected to resume ~10pm 08-13. If PM-gated items below are quiet, check whether access has resumed before reading it as a stall.

## Open items, all PM/CXO/PPM/Dispatch-gated — no Comms-side move available

- ⭐ **Beats steer.** 8 candidates for 7 slots; narrative queue runs dry after Aug 18. Artifact: `docs/internal/planning/comms/upcoming-beats-plan.html`.
- **Beats 22–23** (Aug 13/18) still need PM's voice-pass + art.
- **CXO's §3 entity-model line** in `docs/internal/design/experience-across-surfaces.md` — flagged 3×, still pending.
- **Dispatch syndication**: 3 fully unsyndicated posts, 1 partial. Checked repeatedly, nothing new.
- **BYOC listing copy v4** — open question routed to PPM.
- 🆕 **#1610, #1611** (above) — need PM/architecture-owner decisions.

## Waiting on others

- **PM** — Beats 24–28 steer; voice-pass + art on Beats 22–23; #1610's contact email.
- **PPM** — BYOC listing copy v4 blocker.
- **CXO/PM** — entity-model ratification.
- **Dispatch** — syndication for the 4 posts above.
- **Docs** — the 18 broken links; whoever picks up #1611's architecture question.
