# Comms carry-forward

*Rewritten at the 2026-08-13 06:5x PT fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

✅ **ARMED — job `6d5f873a`.** Same expression `12 6,9,12,15,18,21 * * *`. Auto-expires ~2026-08-19.

## The one thing to do first next session

⭐ **Register/voice pass, tier 3: `docs/guides/` (15 files) + `docs/public/getting-started/README.md` — deferred deliberately, with a real reason, not "no rush."**

Tiers 1 (`dev-tips/`, the CIO obligation) and 2 (five `ALPHA_*` docs, highest-traffic) are **done and pushed** this fire — see below. Tier 3 is a different kind of task: spot-checked `canonical-handlers-architecture.md` and it's dense internal architecture documentation (commit hashes, ADR cross-references, internal code paths, terms like "M1 floor inversion" used without gloss) — 4,313 lines across 16 files. This isn't a tone problem like `dev-tips/` was; it's a real question of whether an external reader can follow architecture prose written for engineers, which needs fresh, careful attention rather than being squeezed in at the end of an already-substantial fire. **Named trigger: a fresh session, because the remaining surface is architecturally dense and deserves undivided focus, not because of time pressure** (this fire still had capacity — mail stayed empty throughout).

Authoritative surface list: KEEP section of `docs/internal/operations/docs-site-scoping-proposal-2026-08-12.md`. Parallel with Docs' own staleness+link pass remains fine.

## Done this fire (2026-08-13 morning)

- ✅ **`dev-tips/` (5 files) — the CIO obligation, discharged.** Fixed: hardcoded personal paths/aliases that don't generalize (PM's own checkout path, the `piper` shell alias, "already in ~/.zshrc"), an internal-only skill-name example, "our"/"team" possessives. Two files (`landing-the-plane-checklist.md`, `version-bump-and-venv-fix.md`) are genuinely internal-process/historical-incident content — added one-line framing notes rather than rewriting the substance out of content that's honestly "how this team works." Commit `d5b1eca37`.
- ✅ **Five `ALPHA_*` docs — reviewed, mostly clean.** `ALPHA_KNOWN_ISSUES.md`, `ALPHA_AGREEMENT_v2.md`, `ALPHA_QUICKSTART.md` needed no register changes — already correctly addressed to an external tester with the right "we/you" distinction. `ALPHA_FEATURE_GUIDE.md`: glossed "Gall's Law," linked 2 bare issue refs to match the doc's own convention. `ALPHA_TESTING_GUIDE.md`: all 22 issue references were bare (unlike its siblings) — linked systematically; glossed "SEC-RBAC" (unexplained internal shorthand) twice. Commit `9f6ab1732`.
- 🆕 **Filed #1610**: `ALPHA_AGREEMENT_v2.md` ships with a literal `[contact email]` placeholder in a legal agreement — gap open since Oct 2025, duplicated in 2 other docs (`privacy-policy-DRAFT.md`, `email-template.md`). Didn't fix it myself (don't know the real address, and guessing on a legal doc is worse than the visible placeholder). Needs a PM decision, then one fix applied across all three files.

## PM capacity note — may still apply this morning

PM has been running the team on borrowed DesignXProduct tokens; own account access was expected to resume ~10pm 08-13. If PM-gated items below are quiet, check whether access has resumed before reading it as a stall.

## Open items, all PM/CXO/PPM/Dispatch-gated — no Comms-side move available

- ⭐ **Beats steer.** 8 candidates for 7 slots; narrative queue runs dry after Aug 18. Artifact: `docs/internal/planning/comms/upcoming-beats-plan.html`.
- **Beats 22–23** (Aug 13/18) still need PM's voice-pass + art.
- **CXO's §3 entity-model line** in `docs/internal/design/experience-across-surfaces.md` — flagged 3×, still pending.
- **Dispatch syndication**: 3 fully unsyndicated posts, 1 partial. Checked repeatedly, nothing new.
- **BYOC listing copy v4** — open question routed to PPM.
- 🆕 **#1610** (above) — needs PM's contact-email decision.

## Waiting on others

- **PM** — Beats 24–28 steer; voice-pass + art on Beats 22–23; #1610's contact email.
- **PPM** — BYOC listing copy v4 blocker.
- **CXO/PM** — entity-model ratification.
- **Dispatch** — syndication for the 4 posts above.
