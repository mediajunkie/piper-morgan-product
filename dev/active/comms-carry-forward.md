# Comms carry-forward

*Rewritten at the 2026-08-13 15:5x PT fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

✅ **ARMED — job `6d5f873a`.** Same expression `12 6,9,12,15,18,21 * * *`. Auto-expires ~2026-08-19.

## pmorgan.tech register pass — status

**Tiers 1–6 done, per Docs' priority order (given after tier 4). Not the whole ~160-file KEEP surface — naming the denominator:**

- ✅ **Tier 1, `dev-tips/`** (the CIO obligation) — `d5b1eca37`.
- ✅ **Tier 2, five `ALPHA_*` docs** — `9f6ab1732`.
- ✅ **Tier 3, `guides/` + `getting-started/`** — `c6dcc2074`. (1 file, `mac-dock-integration.md`, deliberately untouched, #1611.)
- ✅ **Tier 4, `public/user-guides/`** — `f7bab9aa0`.
- ✅ **Tier 5, `features/`+`integrations/`+`configuration/`** — `da3abb64a`.
- ✅ **Tier 6, `installation/`+`setup/`+`troubleshooting/`** — `285f2a0c1`. **Found 2 real content-integrity bugs here, not just tone** — see below.
- ⬜ **Next per Docs' order**: `api/` + `public/api-reference/` (dev-tips/ already done in tier 1). Then `testing/` + `releases/` last. **Check for a Docs reply first** — today's tier-6 findings were substantial enough (a broken install tutorial, an internal-infra leak) that Docs/PM may want to redirect before I continue.

## Tier 6's two real bugs (not tone) — sent to Docs+CIO+PM, commit `b3417c12e`

1. **The manual install tutorial was broken.** `quick-reference.md`: `cd piper-morgan` after cloning into `piper-morgan-product` — wrong folder name, 3 instances, fixed. `step-by-step-installation.md`: the `git clone` step was **missing entirely** (numbering jumps 2→5) — wrote it since it was unambiguous. **Steps 9-10 are also missing** (verify + start server) — did NOT invent these, pointed to `quick-reference.md`'s equivalent instead. Someone who can verify against a live install should write the real ones.
2. **`llm-api-keys-setup.md` had an internal-infrastructure warning** (Amber/Pard/resident-sessions/Max-subscription — the internal agent cohort's own billing-safety concern) sitting in a guide for human alpha testers. Removed, replaced with a generic version of the real caution. **Couldn't find this recorded elsewhere in the repo** — flagged since it may be the only copy of real safety guidance that needs a proper internal home.

## Filed/flagged, not fixed — need someone else

- **#1610**: ✅ **CLOSED.** PM decided the addresses (support@/privacy@/xian@pipermorgan.ai), Docs fixed all 4 docs in one pass. Confirmed via `gh issue view`, don't re-flag.
- **#1611**: `mac-dock-integration.md`'s stale-architecture question. Docs verified the port-8081 pattern is genuinely still live in code despite every current doc contradicting it — routed to Lead. File stays in KEEP untouched until Lead attests which way it resolves.
- **~30 broken links total** across tiers 3-6, pointing at now-excluded content. **All 18 from tier 3 + 6 from tier 4 already repointed by Docs** (absolute GitHub URLs). Tier 5's 2 (ADR-038) and tier 6's 1 (windows-setup-guide.md) sent, not yet confirmed.
- **Systemic link pattern, tier 5 finding**: 64 files site-wide link "Documentation Home" to repo-root README instead of `docs/README.md` (same bug Docs caught in `guides/README.md`). ~10-15 in KEEP scope. Flagged as a pattern, not fixed file-by-file — Docs is already sweeping this class.
- **`PM-NNN` legacy ticket-ID pattern** — Docs investigated, added a historical-IDs gloss in 3 files. Closed.

## Beat 22, "Alpha Launches" — reviewed and publish-ready, still NOT live as of 15:5x PT

Reviewed PM's edits, fixed 4 mechanical defects, marked PUBLISH-READY, sent to Docs directly — `bc1e6196b`, `a92e93c2b`, mail `f96becc04`. **Checked again at 15:5x — calendar still shows `drafted`, not yet published.** Not chasing; Docs has been visibly busy with the tier-5/6 findings. If still unpublished by tomorrow morning, worth a gentle check-in, not before.

## Open items, all PM/CXO/PPM/Dispatch-gated — no Comms-side move available

- ⭐ **Beats steer.** 8 candidates for 7 slots; narrative queue runs dry after Aug 18. Artifact: `docs/internal/planning/comms/upcoming-beats-plan.html`.
- **Beat 23** (Aug 18) still needs PM's voice-pass + art.
- **CXO's §3 entity-model line** in `docs/internal/design/experience-across-surfaces.md` — flagged 3×, still pending.
- **Dispatch syndication**: 3 fully unsyndicated posts, 1 partial. Checked repeatedly, nothing new.
- **BYOC listing copy v4** — open question routed to PPM.

## Waiting on others

- **PM** — Beats 24–28 steer; voice-pass + art on Beat 23.
- **PPM** — BYOC listing copy v4 blocker.
- **CXO/PM** — entity-model ratification.
- **Dispatch** — syndication for the 4 posts above.
- **Docs** — publish "Alpha Launches"; tier-6's broken links; whoever picks up #1611 (routed to Lead); the missing install-tutorial Steps 9-10; a home for the Amber/Pard safety warning I pulled from `llm-api-keys-setup.md`.
