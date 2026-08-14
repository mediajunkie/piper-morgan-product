# Comms carry-forward

*Rewritten at the 2026-08-13 18:4x PT fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

✅ **ARMED — job `6d5f873a`.** Same expression `12 6,9,12,15,18,21 * * *`. Auto-expires ~2026-08-19.

## New assignment: PM's public values/ethics document (with HOST) — just kicked off

PM decided today to open-source Piper Morgan under Apache 2.0 (patent grant + trademark carve-out, paired with a separate trademark process PM is running with Themis). The real worry is an "evil Piper" fork stripping the ethical architecture — no license can prevent that (checked: Open Source/Free Software definitions both require unrestricted use-purpose; Hippocratic License ruled out too, not OSI-recognized). **The actual mechanism is reputational: a public values document specific enough that a fork visibly diverging from it can't credibly claim to still be Piper Morgan.**

Relayed by Exec (`kickoff-pm-to-comms-host-...md`). PM's ask: HOST + Comms draft it together, no shape specified, **no deadline** — "a considered scaffold beats a fast one." Proposed split (Exec's frame, not fixed): HOST = substance (what the commitments are), Comms = form (voice, placement, introduction). Replied to Exec, reached out to HOST directly proposing we start with a short list of the genuinely identity-defining commitments before drafting anything — mail `a5fcf68e7`. **Waiting on HOST's response.** This is real work, deliberately not rushed — don't manufacture urgency here.

## pmorgan.tech register pass — status

**Tiers 1–6 done, per Docs' priority order. Not the whole ~160-file KEEP surface — naming the denominator:**

- ✅ Tiers 1–6 all complete — see prior carry-forward history / session log for commits.
- ⬜ **Next per Docs' order**: `api/` + `public/api-reference/`, then `testing/` + `releases/` last. **Still holding** — Docs hadn't replied to the tier-6 bug report (broken install tutorial, internal-infra leak) as of this fire. Check for their reply before continuing; don't restart tier 7 unprompted a second time.

## Tier 6's two real bugs — sent to Docs+CIO+PM, commit `b3417c12e`, no reply yet

1. Manual install tutorial was broken (wrong folder name + missing clone step in `step-by-step-installation.md`; also missing Steps 9-10, not invented, pointed elsewhere instead).
2. `llm-api-keys-setup.md` had an internal-infrastructure warning (Amber/Pard/resident-sessions) with no relevance to human alpha testers — removed, flagged since it may be the only copy of real internal safety guidance.

## Filed/flagged, not fixed

- **#1610**: ✅ CLOSED (PM decided addresses, Docs fixed all 4 docs).
- **#1611**: `mac-dock-integration.md` architecture question, routed to Lead by Docs.
- **~30 broken links** across tiers 3-6 — most already repointed by Docs; tier 5's 2 + tier 6's 1 sent, unconfirmed.
- Systemic "Documentation Home → repo-root README" link pattern (64 files) — flagged, Docs already sweeping.

## Beat 22, "Alpha Launches" — ✅ PUBLISHED, syndication in progress

Live at `https://pipermorgan.ai/blog/alpha-launches/`. PM cross-posted to Medium directly this evening and sent Docs a calendar-update request (`memo-xian-to-docs-calendar-update-alpha-launches-2026-08-13.md`) — **that's addressed to Docs, not me, per the 2026-07-29 process change (only Docs writes the calendar now). Deliberately not touching it myself.** Nothing left here on my end.

## Open items, all PM/CXO/PPM/Dispatch-gated — no Comms-side move available

- ⭐ **Beats steer.** 8 candidates for 7 slots; narrative queue runs dry after Aug 18. Artifact: `docs/internal/planning/comms/upcoming-beats-plan.html`.
- **Beat 23** (Aug 18) still needs PM's voice-pass + art.
- **CXO's §3 entity-model line** in `docs/internal/design/experience-across-surfaces.md` — flagged 3×, still pending.
- **Dispatch syndication**: 3 fully unsyndicated posts, 1 partial. Checked repeatedly, nothing new.
- **BYOC listing copy v4** — open question routed to PPM.

## Waiting on others

- **HOST** — values-doc kickoff, awaiting their read on the identity-defining-commitments list.
- **PM** — Beats 24–28 steer; voice-pass + art on Beat 23.
- **PPM** — BYOC listing copy v4 blocker.
- **CXO/PM** — entity-model ratification.
- **Dispatch** — syndication for the 4 posts above.
- **Docs** — reply on tier-6 bugs (broken tutorial, Amber/Pard warning's home); tier 7 priority confirmation; calendar update for Alpha Launches' Medium cross-post (PM's direct ask, not mine to action).
