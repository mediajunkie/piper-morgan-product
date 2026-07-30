# CXO carry-forward — ephemeral session state

**Owner**: CXO | **Updated**: 2026-07-30 11:2x PT (Fire 2, WORK)
**Read at**: every fire START. **Rewritten at**: the end of every substantive fire.
**Durable owed/queued work lives in** `cxo-standing-items.md` — this file is *current* state only.

> Created 2026-07-30. The duty-cycle skill expects this file at every fire and it did not exist for
> this seat — I'd been carrying everything in `cxo-standing-items.md`. That conflates *durable queue*
> with *current state*, and the skill reads them for different purposes.

## Cron

- **Job `2e808691`** — `47 6,9,12,15,18,21` (6×/day, 06:47–21:47). Armed 2026-07-29 at PM's direction.
- ⚠️ **Session-only AND auto-expires ~2026-08-05**; both deaths are silent. **Run `CronList` at every
  START** — the registry row records *intent*, not a live job.
- Registry row: **un-parked**, `active_since 2026-07-29`.
- **STOP today** = the 21:47 fire (next fire after it is 06:47 tomorrow → different date).

## Live PM threads

| Thread | State | Next |
|---|---|---|
| **Jake FTUX discussion** | PM asked for time **today** (07-30). Prep staged: `dev/active/jake-ftux-discussion-prep-2026-07-30.md`. | **Wait for PM.** Don't re-present the lenses — the session's value is PM's latent read. |
| **Jake collection gate** | 3 of 4 filed (CXO ✅ HOST ✅ PA ✅). **PPM missing and structurally cannot file** — parked, cron un-armed (PM-gated). | PM's call: arm/seed PPM, or synthesize on 3. Raised 07-29; **unanswered.** |
| **Spatial committed-theory review** | Hold RELEASED 07-30. Arch's layer map is canonical. My options review filed. Converged on **(b)**. | **Watch.** Deciding unknown is **Lead's L4 cost estimate**. PM rules on disposing the 10-module cold island (protected-surface rule — nothing deleted until then). |
| **PDR-006** | **CXO review filed 07-30: RATIFY.** Only PPM's review outstanding. | Watch for ratification; 3 design items are mine to pick up (below). |

## Awaiting a ruling from others (filed by me, not mine to advance)

- **m-46** (`methodology-46-PROMOTION-IS-A-RE-VERIFICATION-EVENT.md`) — **PROPOSED, not filed.**
  CIO + HOST have the filing call. Rename/renumber/refold is theirs.
- **Colleague Test tier status** — routed to PPM + PM: does the instrument warrant PDR standing while
  DoD Layer B (which depends on it) is treated as binding? My weak lean: sufficient as-is.
- **PDR-006 rubric branch (B′)** — the plugin surface has no fitting rubric. Mine to design once PPM
  weighs in; the exposure is **honesty-under-recomposition** (untested).

## Owed to me / awaiting others

- **PPM** — Jake lens; PDR-006 review; spatial roadmap-dependency slice. All blocked on PPM being un-parked.
- **Lead** — L4-monitoring-loop cost estimate over `github_spatial` (my stated flip condition).
- **Arch** — ADR-038 amendment draft; asked me to review the options from the experience side **before
  it goes to PM** (done for the costed options; the amendment draft is still coming).
- **CIO** — Step-0 `DAY-CLOSED` grep fix; m-44 candidate.

## PM-attention items (escalations)

1. **PPM is un-armed and it is blocking the Jake synthesis.** One action clears it.
2. **My L4-on-GitHub proposal carries a risk I flagged against myself** — GitHub is where ambient
   presence is *least* differentiating (its notifications already do it well). Don't let a small cost
   estimate be read as "ship it on GitHub and we're done."

## Environment notes for this seat

- **Sync before reading mail.** 07-29: worktree 271 behind, inbox read *empty*, a Ship kickoff and a
  PM-directed ask both invisible.
- **`cd` persists across Bash calls** — twice produced false-empty reads. Absolute paths.
- **Hook status**: Pard's real `pre-commit` is installed in the **common** dir (07-29), delegating to
  `check-branch.sh` — covers every worktree by construction. **v1.22 retired the probe: verify the
  hook exists, do NOT probe.** The compound-vs-standalone advice in my cron prompt is **obsolete**;
  update it at the next re-arm.
