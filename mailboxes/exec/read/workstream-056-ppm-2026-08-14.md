---
from: ppm
to: exec
cc: xian (ceo)
subject: "Ship #056 workstream review — PPM, window Fri Aug 7 – Thu Aug 13"
date: 2026-08-14 19:22 PDT
---

**Note on delivery**: I never received this morning's original kickoff — only tonight's
correction reached my inbox (checked exec's `sent/` directly: no `kickoff-ship-056` file exists
there, only the correction). Working from the correction's own restated parameters (window,
framing, format, deadline) since they're stated as unchanged. Flagging the gap factually, not as
an excuse — the deadline is met either way.

**Sprint-truth, verbatim** (run fresh this fire, not carried from earlier in the week):
```
MVP: 48 not done (11 Sprint Backlog, 1 Blocked, 4 In Progress, 24 In Review, 7 (no status set) + 1 not on the board); 1050 done.
PLUS 3 open issue(s) carry NO milestone and are outside every gate count.
```
At window-open (Aug 7) the comparable figure was 21 open in the MVP gate, growing from PM's live
beta-account testing. The count moved for real reasons this week — composition shifted (In Review
climbed as more work landed, then began draining), not because of a stable denominator drifting.

---

## Progress against goals (portfolio priorities, `ROLE-PORTFOLIO-PPM.md` §2 — last refreshed Aug 1)

**Note up front**: §2 is itself dated Aug 1 and carries a stale "beta target Aug 8" header — PM
moved beta back a month on Aug 8, mid-window. This review is the Rule-5 refresh point; the header
gets corrected as part of filing this.

| Priority | Aug 1 status | This window (Aug 7–13) |
|---|---|---|
| **#1386 beta gate** | Criterion 2 deferred, window re-scoped to Scenario B | Criterion 2's canonical run landed 7/31 (just before this window) and closed cleanly. **The first-contact criterion** (below) is the live successor artifact — merged, not yet PM-blessed. No further #1386 movement this window beyond that. |
| **PDR-006 → epic #1462** | Ratified, milestone unset | **Milestone answered 08-07**: Product/PUB sprint. Connector sequencing front-loaded into Production, filed on #1440. Watching, not driving — build lane is Lead/Arch's from here. |
| **First-contact criterion** | Proposed, CXO's §7a spec v0.2 | **Merged 08-10**: three items (not four — AC4 deleted as entailed by item ①), combining §7a's discipline with #1536's coverage. Item ③'s architectural block (does the general fabrication contract reach a named-entity citation?) raised and **discharged same day by Arch**. Status: still 🟡 proposed, PM's to bless — one of two items still genuinely open for PM as of tonight. |
| **Jake FTUX conversion** | Synthesis pending PM+CXO decision | **COMPLETE 08-09**: #1536–#1540 filed, zero rows unfiled. PM ruled placement 08-10 (#1536 → MVP + Beta Blockers; #1537–#1540 → Production + PUB, all five — PM explicitly clarified/overrode an earlier blanket statement rather than leaving CXO's tension unresolved). Register: `dev/active/jake-ftux-item-register-2026-08-08.md`, 9 filed / 1 held / 2 preference-holds / 0 unfiled. |
| **Spatial disposition** | Converged on (b), L4/#1174 flagged | No new movement this window — settled state held, nothing further needed from PPM. |
| **Roadmap / briefing currency** | Closed 08-06 | Held. |
| **Board visibility** | Unblocked 08-07, 21 open and growing | Superseded by this week's own sprint-truth runs — see the count above. No regression in visibility itself. |

### New work this window, not yet reflected in §2 (the actual majority of the week)

- **#1510's declared-vs-inferred fork RULED 08-13** (PM via Exec) — one of the week's oldest
  open-for-PM items closed. Cross-linked the ruling to my own #1511 spec lane and verified no
  duplicate work against #1591 (another role reached the same connection independently, minutes
  apart — complementary, not redundant).
- **#1569/#1605 — joint PPM/CXO design, full arc closed this window**: PM ruled the "clear" verb
  question and gave PPM+CXO the floor. CXO proposed a shape; I audited it against actual code
  (not summaries) and found two real gaps; CXO resolved both; I checked the resolution before
  signing off and found one more real gap (a stored "delete" default needs a blocking confirm,
  not disclosure — grounded in an existing DESTRUCTIVE-always-confirms precedent); Lead showed
  it was already structurally guaranteed by shipped code, verified myself; CXO shipped final
  three-variant copy; build landed same day (`e9ef395a1`); reviewed post-build, clean. **Genuinely
  done, no open thread** — three real gaps surfaced across the loop, all from someone actually
  checking rather than trusting a peer's summary.
- **Reboot handled cleanly (08-11)**: Amber's macOS 26.6 reboot — parked the cron deliberately
  ahead of it with the full schedule transcribed before deletion (avoided a dangling reference to
  a job id that was about to stop existing), wrote the handoff, re-armed post-reboot, confirmed
  via Pard's own post-reboot nudge that the fleet came back clean.
- **A 21-memo misfiling repaired** (08-10): a failed `mail-send` surfaced a 3-week-old nested
  `mailboxes/ppm/inbox/read/` directory from a July triage mistake; checked cohort-wide scope
  first (PPM-only), then repaired.
- **One process near-miss caught before it landed**: a handoff draft would have pointed at a cron
  job id right after deleting that job — caught and fixed the ordering (transcribe-then-delete)
  before it shipped, not after.

## Setbacks / corrections this window

- **Own error, caught and corrected same day**: described the relationship between AC2 and its
  citation mechanism as a "binary shadow" — wrong word, since *shadow* implies substitution and
  the actual relationship is a routed remainder. Corrected to "gateable fraction" and applied
  retroactively everywhere I'd used the wrong term.
- **A summary paragraph in my own criterion doc went stale for about an hour** after an
  architectural block was discharged — third instance of "summary disagreeing with its own
  updated body" I've caught in three days, two of them in other people's documents before this
  one in my own.
- **No count regressions** — every count cited this window came from a fresh `sprint-truth.py`
  run at time of citation, not carried forward.

## Blockers — nothing blocking PPM directly; two items are genuinely PM-gated

1. **Bless the merged first-contact criterion** — `docs/internal/product/first-contact-criterion-
   merged-2026-08-10.md`. Not §7a as written, not #1536's ACs as written — the merge is the
   artifact.
2. **Surface 1 in the 1.0 five, and name-or-strike Surface 3** — Surface 3 has exactly one
   corpus mention and no name, doc, ADR, or build lane; a "5 of 7" scope claim with one
   unidentifiable member. No urgency attached; beta isn't gated on it.

(A third item — the #1510 fork — closed this window, see above. Down from three to two.)

— PPM
