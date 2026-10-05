# Beta Gate Standard (frozen-list rule)

**Owner**: PPM
**Status**: **RATIFIED 2026-10-05** (v0.1). PM, verbatim, relayed by Exec 08:58 PDT: *"yes, I ratify the frozen beta-gate standard."* Origin: Spec's evaluation report R1 (`docs/internal/audits/2026-10-spec-project-evaluation.md`), PM endorsed the idea on 2026-10-03/04 and asked PPM for a view and a formal version.
**Not yet covered by the ratification**: retiring the parallel records (below). That edits the board and needs PM's separate explicit yes (Exec is asking).
**First application**: `beta-gate-pass-2026-10-05.md` (all 31 bodies read; proposal, nothing applied).
**Supersedes**: the "Maintenance discipline" paragraph and three-way-sync rule in `beta-blockers.md` (see "One source of truth" below).

## Why

The old bar ("does it block an external tester from safely and honestly using the product?") is sound but open-ended: every internal test round can mint new issues that arguably meet it, so the gate is defined by an unbounded test space. The fix is to make admission a closed list of classes, tagged at filing, so that "does the gate grow?" becomes a count, not an argument.

## One source of truth

**The MVP milestone is the gate.** Open issues in the MVP milestone are the gate list; nothing else is. The Sprint-field value "Beta Blockers - Hard Gates Only", the `beta:<epic>` labels, and the status tables in `beta-blockers.md` stop being parallel records. They have already drifted (beta-blockers.md last updated 2026-07-09 and describes 8 open issues; the milestone held 30 open on 2026-10-03). Retiring them is a PM decision (Sprint-field and milestone edits are PM-confirmed); until then the milestone wins any disagreement.

## Admission: four classes, tagged at filing

An issue enters the MVP milestone only if its body carries a one-line `Gate class:` naming one of:

1. **Data loss or unconsented irreversible action.** User data destroyed, corrupted, or exposed across users; or an irreversible action executed without the confirmation the product promises.
2. **Security.** Authentication, authorization, tenant isolation, credential or token exposure.
3. **Honesty.** The product tells the user something false about its own state, actions, or capabilities: claims done what was not done, shows a count that contradicts the list beneath it, says it learned or saved something it did not. *Not honesty:* failing to understand a request (capability), awkward wording, missing features.
4. **Golden-path blocker.** An invited tester cannot complete signup, add a key, connect an integration, or hold a first useful conversation. The golden path is exactly the scenarios in #1386; anything outside them is not covered by this class.

Class 4 is an addition to the three PM endorsed. Without it, "tester cannot connect Slack" (e.g. #1852) meets none of 1-3 and the standard would eject a true blocker. PM may strike it; if so, those issues need an explicit ruling each.

## Epic 0 clause

Interpretation-layer failures (routing, classification, pattern-phrasing misses) do not enter the gate as standalone issues. They become corpus rows or evidence under #1595, per the supersession gate (PM 2026-08-29). Two boundaries:

- **The epic's own completion tail is in the gate by definition** (Phase 3 deletions, contract-test pins broken by those deletions). It is scope, not evidence.
- **The clause covers a failure only if epic 0's planned wave fixes it by construction.** A routing failure whose *consequence* is class 1-3 and which the epic will not fix (e.g. #1926, destructive unlink without confirm) is gated on its class.

## Everything else

Production milestone (post-beta), as today. No "low-priority MVP" tier.

## Per-surface instantiation (R7, PM ruling 2026-10-05, relayed by Spec)

No surface "is" the MVP. The MVP is Piper Morgan offering a core set of capabilities, with varying degrees of instantiation depending on the surface. The beta target is beta.pipermorgan.ai. The admission classes above apply to the core capability set; the required level per surface is:

| Surface | Required for beta | How it is held |
|---|---|---|
| Hosted web UI (beta.pipermorgan.ai) | **Yes.** The MVP has always included it. | The gate: the four classes, the MVP milestone. |
| MCP / plugin | **No.** Released and tested during the beta period, which starts when the MVP milestone closes and Production-milestone work begins. | A cheap demand probe (PA packages it; PM tests before anything is listed). MCP-surface issues go to Production unless they meet class 1-3 (data loss, security, honesty on that surface). |
| BYOC / local | **Not ruled.** PM said the idea that BYOC becomes the primary usage scenario "has likely taken hold and perhaps distorted" the thinking; no ruling makes it a beta surface. | Not a gate surface unless PM rules otherwise. |

What this changes in application (PPM's reading of the ruling, flagged for PM correction): a defect is admitted by its class on the surface the beta ships, not by surface. An MCP-only polish issue (e.g. consent-page branding, #1911) is Production. An MCP-surface issue that loses data, exposes a credential, or states something false would still be class 1-3 and gated. "What has to be working in the MVP to release the beta" stays PM's open call; this standard bounds how the gate list may grow, it does not decide the capability set.

## Exits and freeze mechanics

- A gate issue leaves only by closing or by explicit PM ruling.
- On ratification: one PM-confirmed pass applies the classes to the current 30, producing a dated frozen list. After that, additions need a `Gate class:` tag and PPM's same-fire triage (already the board-hygiene loop).
- PPM reports weekly in the rollup: admissions by class, closes, net. This is the measurement the premise lacked.

## Illustrative application (title-level only, NOT body-verified, SUPERSEDED by the body-read pass)

The real pass is `beta-gate-pass-2026-10-05.md`: 31 bodies read, 10 stay, 1 closes, 6 epic-0 evidence, 2 held for Arch, 12 Production. The title-level guess below was wrong on several (e.g. #1917 is a product ask, not epic-0 evidence; #1817 is a dated assumption, not a live security defect). Kept for the record of how far a title-level read can be trusted.

Reading the 30 open MVP titles on 2026-10-03: roughly 8 look like classes 1-3 (#1885, #1817, #1926, #1913, #1889, #1880, #1632, #1735), 3 like class 4 or the close-out gate (#1852, #1916, #1386), about 10 look like epic-0 evidence (#1579, #1771, #1783, #1843, #1860, #1867, #1886, #1623, #1891, #1917), 7 look post-beta (#1832, #1907, #1911, #1915, #1625, #1522, #1698), and 2 are the epic's own scope (#1595, #1925). That sums to 30. A real pass reads each body; several of these could move on a read.
