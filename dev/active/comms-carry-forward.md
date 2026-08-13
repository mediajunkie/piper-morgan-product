# Comms carry-forward

*Rewritten at the 2026-08-13 12:45 PT fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

✅ **ARMED — job `6d5f873a`.** Same expression `12 6,9,12,15,18,21 * * *`. Auto-expires ~2026-08-19.

## pmorgan.tech register pass — status

**Tiers 1–4 touched. Not the whole ~160-file KEEP surface — naming the denominator:**

- ✅ **Tier 1, `dev-tips/` (5 files, the CIO obligation)** — done. Commit `d5b1eca37`.
- ✅ **Tier 2, five `ALPHA_*` docs** — done. Commit `9f6ab1732`.
- ✅ **Tier 3, `guides/` (15) + `getting-started/` (3 current files)** — 17 of 18 done, 1 (`mac-dock-integration.md`) deliberately left untouched, filed as #1611. Commit `c6dcc2074`.
- ✅ **Tier 4, `public/user-guides/` (7 current files after `legacy-user-guides/` exclusion)** — 6 of 7 fixed/clean. Commit `f7bab9aa0`.
- ⬜ **Not started, and explicitly holding here**: told Docs I'm not continuing further into the remaining ~150 KEEP files without a priority signal, rather than guessing at scope on my own. Remainder includes `installation/` (7), `features/` (5, top-level — distinct from `user-guides/features/`), `integrations/` (3), `configuration/` (2), `setup/` (2), `troubleshooting/` (2) + `troubleshooting.md`, `api/` (3), `public/api-reference/` (7), and more. **Check for a Docs memo naming a next priority before picking a starting point.**

## Filed, not fixed — need someone else

- **#1610**: `ALPHA_AGREEMENT_v2.md`'s `[contact email]` placeholder. Needs PM's actual address; Docs has it on their next PM-touchpoint rollup.
- **#1611**: `mac-dock-integration.md`'s stale-architecture question. **Verified by Docs, not just my hunch**: the port-8081 two-process pattern is genuinely still live in code (`port_configuration_service.py` default + 3 scripts) despite every current doc contradicting it — routed to Lead. File stays in KEEP untouched until Lead attests which way it resolves.
- **24 broken links total** (18 tier-3 + 6 tier-4) pointing at now-excluded content — **all 18 from tier 3 already repointed by Docs** (absolute GitHub URLs, commit `dc200c524`), same-fire turnaround. Tier-4's 6 sent as a follow-up memo, not yet confirmed fixed.
- **`PM-NNN` legacy ticket-ID pattern** (PM-011, PM-124, PM-126) found in `user-guides/features/` — flagged to Docs, unclear if these still resolve to anything current. Not acted on further.

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
- **Docs** — tier-4's 6 broken links; a priority signal for the ~150-file remainder; whoever picks up #1611 (routed to Lead).
