# Beta Gate Standard (frozen-list rule)

**Owner**: PPM
**Status**: **RATIFIED 2026-10-05** (v0.1). PM, verbatim, relayed by Exec 08:58 PDT: *"yes, I ratify the frozen beta-gate standard."* Origin: Spec's evaluation report R1 (`docs/internal/audits/2026-10-spec-project-evaluation.md`), PM endorsed the idea on 2026-10-03/04 and asked PPM for a view and a formal version.
**Ratified 2026-10-05 ~17:20 PDT (PM, via Exec 17:35)**: v0.2 class-4 wording (decision 2: yes), and the slip-rule additions c, symmetry and brake (decision 6: yes, "re-confirmed, treat as final"). The slip rule is now in force in full. The parallel-records question is settled by PM's 10-05 ruling (see "One source of truth").
**First application**: `beta-gate-pass-2026-10-05.md` v2 (31 of 31 bodies and their comment threads read; proposal, nothing applied).
**Supersedes**: the "Maintenance discipline" paragraph and three-way-sync rule in `beta-blockers.md` (see "One source of truth" below).

## Why

The old bar ("does it block an external tester from safely and honestly using the product?") is sound but open-ended: every internal test round can mint new issues that arguably meet it, so the gate is defined by an unbounded test space. The fix is to make admission a closed list of classes, tagged at filing, so that "does the gate grow?" becomes a count, not an argument.

## One source of truth

**The MVP milestone is the gate.** Open issues in the MVP milestone are the gate list; nothing else is. PM's ruling (10-05, relayed by Exec): PM does not use labels; PM uses board sprints; "open in the MVP milestone" means the same thing as the "Beta Blockers" Sprint value today; **for now, verify against the milestone.** Consequences:
- The `beta:<epic>` labels are not a record and are not relied on.
- The Sprint value is not edited by PPM; Sprint-field changes stay PM-confirmed. Once issues leave the milestone, the Sprint value will diverge from it, and the milestone wins.
- `beta-blockers.md` is the only parallel record worth touching: corrected 2026-10-05 to point at the milestone (a doc edit, not a board edit); its Epics A-G history is kept below its banner.
- Later, once Production starts, which sprint an issue is in will matter again (Exec tracks that lane item).

## Admission: four classes, tagged at filing

An issue enters the MVP milestone only if its body carries a one-line `Gate class:` naming one of:

1. **Data loss or unconsented irreversible action.** User data destroyed, corrupted, or exposed across users; or an irreversible action executed without the confirmation the product promises.
2. **Security.** Authentication, authorization, tenant isolation, credential or token exposure.
3. **Honesty.** The product tells the user something false about its own state, actions, or capabilities: claims done what was not done, shows a count that contradicts the list beneath it, says it learned or saved something it did not. *Not honesty:* failing to understand a request (capability), awkward wording, missing features.
4. **Golden-path blocker.** An invited tester cannot complete signup, add a key, connect an integration, or hold a first useful conversation. The golden path is the scenarios in #1386 **plus every integration the beta invitation tells testers to connect** (v0.2, PM-ratified 2026-10-05; which integrations the invitation names is still PM's open call, decision 3). Anything outside that is not covered by this class.

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

## Slip rule (RATIFIED 2026-10-05: PM's (a) and (b) at ~10:00, additions (c), symmetry and brake at ~17:20)

Base: Exec's proposal, as PM asked for it ("the beta date will slip if it needs to... we also need to question endless slippage"). The target date moves only when **(a)** the measured gate list grows by an admission carrying a `Gate class:` line, or **(b)** Epic 0's tranche changes. Every slip is logged with its named cause and the gate count before and after. A slip with no named cause is not recorded and the date does not move.

PPM's three additions (PM yes, final):
1. **(c) A measured unknown resolving larger than assumed.** The unknowns are named in the pass doc (#1889 size, #1386 re-run duration, Epic 0 Phase 3 tail). An entry under (c) cites the sizing evidence and names which unknown it is.
2. **Symmetry.** Un-admissions and closes are logged too, so the count is a ledger with both sides.
3. **A brake.** If cumulative slip against the baseline passes 7 days, or a second slip is logged, PPM does not propose another date; PPM brings PM an explicit choice, cut named scope or accept the later date as a decision.

PM alone moves the design-partner date and the hard stop. PPM proposes with the entry drafted.

**Slip ledger** (PPM keeps it, here):

| Entered | Design partners | Hard stop | Cause | Issues | Gate count before → after | Evidence |
|---|---|---|---|---|---|---|
| 2026-10-05 (baseline) | Fri 10-23 | Fri 10-30 | none: baseline | n/a | 31 in the milestone; 9 under the pass proposal (4 firm + 5 pending rulings) | `beta-gate-pass-2026-10-05.md` |
| 2026-10-05 21:33 (close, symmetry entry) | Fri 10-23 (unchanged) | Fri 10-30 (unchanged) | close: Lead closed the gate-work-landed issue about calendar free blocks and truncated lists at 19:30 PDT; its last residue stays with #1776 | #1880 | 31 → 30 in the milestone; pass proposal 9 → 9 (it was in the close-or-split bucket, not the 9) | `sprint-truth.py` delta 21:3x (done 1229 → 1230); closing comment on #1880 |
| 2026-10-06 06:33 (close, symmetry entry) | Fri 10-23 (unchanged) | Fri 10-30 (unchanged) | close: Lead closed the Slack health-endpoint test issue at 04:50Z on Arch's Rule-0 GO (no such route exists) | #1832 | 30 → 29 in the milestone; pass proposal 9 → 9 (it sat in the Production bucket, not the 9) | `sprint-truth.py` delta 06:3x (done 1230 → 1231); closing comment on #1832 |
| 2026-10-06 ~14:30 (admission, FIRST SLIP ENTRY, PM yes via Exec 14:03) | Fri 10-23 (unchanged) | Fri 10-30 (unchanged) | **(b) Epic 0 tranche change**: Arch's 10-05 router-args ruling (ADR-080 D1/D4) added the `complete_todo` and clear-family flip, the enforcement test, and the Phase 3 corpus rows to the epic's completion tail. PM kept the dates; the 10-08 tail estimate and Lead's #1889 size (both Wed 10-07 / Thu 10-08) are the measurements | #1942, #1943, #1951 (each now carries a `Gate class:` line, Epic 0 completion tail, and `Owner: lead`) | 29 → 32 before the removals below | Exec relay 14:03 PDT; `sprint-truth.py` delta 15:4x ("arrived: #1942 #1943 #1951"). #1949 stayed OUT of the gate (corpus row, Production, evidence under #1595) |
| 2026-10-06 ~15:00 (close, symmetry entry) | unchanged | unchanged | close: PM ruled four closed (the #1930 and #1885 work had landed; #1867 closed on Arch's rule; #1925's open question moved to Ongoing issue) | #1930, #1885, #1867, #1925 | 32 → 28 | PM rulings via Exec 14:03; closing comments on each; `sprint-truth.py` delta |
| 2026-10-06 ~15:15 (un-admission, symmetry entry) | unchanged | unchanged | un-admission: the pass's Production bucket (11 issues moved; #1832 was already closed and stays in MVP as closed) plus PM's Decision B (invitation is GitHub only: #1852 out) and rulings C1 and C2 (#1735 and #1907 to Production, #1735 not descoped) | 11 Production-bucket issues, #1852, #1735, #1907 | 28 → 14 | PM rulings via Exec 14:03; `gh issue edit --milestone` per issue; `sprint-truth.py` 15:4x: 14 open in MVP, 0 unmilestoned; criteria-line gap empty, denominator 14 |

Net 2026-10-06: gate 29 → 14. Slips against baseline: 1 logged (the admission above), 0 days moved. The brake (cumulative slip over 7 days, or a second slip) has not triggered. The six Epic 0 evidence issues (#1579, #1623, #1771, #1783, #1843, #1860) are held in place by PM as a watch item, not un-admitted.

## Class 4 v0.2 (RATIFIED 2026-10-05)

**Decision B (PM, 2026-10-06, relayed by Exec 14:03): the beta invitation names GitHub only.** Slack and Google leave the gate and #1852 leaves with them. Invitation wording: the initial beta release supports only the GitHub connector, and during the beta additional connectors are expected before the 1.0 production release. So "every integration the invitation names" currently means GitHub; adding a connector to the invitation is a gate change and goes through admission.

**Class 4 rulings the same day (PM via Exec):** C1 #1735 goes to Production and is not descoped (removing the personality-saving controls, option C, needs a formal proposal from an advocate); C2 #1907 goes to Production, with a note that the CEO uses an iPad and questions the front-end viewport handling; C3 #1925 closed, its open question moved to an Ongoing issue; C4 #1946 goes to Production (and becomes the first entry on the known-issues list for the invitation).

The class-4 text above carries the v0.2 wording. Original v0.1 defined the golden path as exactly the #1386 scenarios, which contain no Slack or Google Calendar, so "connect an integration" could never be satisfied for them. Which integrations the invitation names (decision 3) decides whether #1852 and similar issues are gate items.

## Illustrative application (title-level only, NOT body-verified, SUPERSEDED by the measured pass)

The real pass is `beta-gate-pass-2026-10-05.md` v2: 31 bodies and their comments read; 4 firm gate, 5 needing a PM ruling, 4 close or split (work landed), 6 epic-0 evidence, 12 Production. The title-level guess below was wrong on several (e.g. #1917 is a product ask, not epic-0 evidence; #1817 is a dated assumption, not a live security defect; #1885, #1735 and #1880 read as live but their gate-class defect had landed in the comments). Kept for the record of how far a title-level read can be trusted.

Reading the 30 open MVP titles on 2026-10-03: roughly 8 look like classes 1-3 (#1885, #1817, #1926, #1913, #1889, #1880, #1632, #1735), 3 like class 4 or the close-out gate (#1852, #1916, #1386), about 10 look like epic-0 evidence (#1579, #1771, #1783, #1843, #1860, #1867, #1886, #1623, #1891, #1917), 7 look post-beta (#1832, #1907, #1911, #1915, #1625, #1522, #1698), and 2 are the epic's own scope (#1595, #1925). That sums to 30. A real pass reads each body; several of these could move on a read.
