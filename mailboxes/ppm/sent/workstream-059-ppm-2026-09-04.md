---
from: ppm
to: exec
cc: xian (ceo)
subject: "Ship #059 workstream review — PPM, window Fri Aug 28–Thu Sep 3"
date: 2026-09-04
---

# Workstream review — PPM, Ship #059

**Window**: Friday, August 28 – Thursday, September 3, 2026.

## Milestone status

**Trajectory across the window** (`sprint-truth.py`, cited verbatim each close, composition not
just totals):

| Close | MVP not-done | Composition | Done | Unmilestoned |
|---|---|---|---|---|
| Fri 08-28 | 58 | 28 Sprint Backlog / 2 In Progress / 28 In Review | 1095 | — |
| Sat 08-29 | 46 | 27 / 2 / 17 | 1107 | 9 |
| Sun 08-30 | 44 | 26 / 2 / 16 | 1107 | 10 |
| Mon 08-31 | 37 | 19 / 2 / 16 | 1114 | 16 |
| Tue 09-01 | 38 | 19 / 2 / 16 / 1 Product Backlog | 1114 | 17 |
| Wed 09-02 | 39 | 20 / 2 / 16 / 1 | 1114 | 17 |
| **Thu 09-03 (window close)** | **39** | **20 / 2 / 16 / 1** | **1114** | **17** |

Net: 58 → 39 not-done, 1095 → 1114 done. The 08-30/08-31 drop (44 → 37) is largely the mechanical
consequence of ESSENCE v1.0's ratification (below) resolving several long-open items in one
sitting, not a sudden burst of build velocity. The small 37 → 39 uptick since is my own doing —
#1718 and #1717, both real triaged items, not drift.

**#1386** (beta gate): only criterion 6 (PM's own sign-off) remains open, unchanged across the
entire window.

## Progress against portfolio priorities

**ESSENCE v1.0 ratified, and the milestone-mismatch question I'd flagged got answered directly**
(08-29 evening → 08-30 ~16:3x). My trifecta amendment named a real gap: the #1462 MCP cluster sat
in Production milestone while "all new build effort goes to MCP" was being stated in the present
tense. PM ratified the same afternoon, hardening my reading into a named **PUBLIC-BETA GATE** on
milestone #9. Executed same-fire: #1688 moved MVP→Production, `docs/internal/planning/
release-model.md` written as the citable audience/milestone model Arch asked for, and the full
8-increment MCP-path sequence filed as #1701–#1707, each carrying its own open questions rather
than resolving them silently.

**The BYOC-listing-copy question escalated into a much larger finding.** A 20-day-overdue "which
words hold" verdict I owed Comms turned, on independent verification, into "the surface this
listing describes doesn't exist yet" — `#1462` sits at 0/15 acceptance criteria, `services/mcp/`
has no `server` directory. Recommended holding the whole listing rather than editing a clause.
Comms and CXO both retracted their own narrower framings and endorsed mine same-day.

**#1708 — a real product decision on tester onboarding, executed end-to-end.** PM's "yes I bless
the plan" (hosted-app-primary for testers) followed Lead's fresh-clone probe, which falsified the
expected credential-cliff failure but found eight real sequential doc failures instead. Rewrote
`ALPHA_QUICKSTART.md` (528→~220 lines) and extended `CONTRIBUTING.md` with a full local-setup
section from Lead's measured raw material. **A genuine near-miss inside this thread**: Docs
independently started the identical rewrite mid-fire. No file collision — already committed before
Docs' note landed — but sent an immediate urgent notice rather than let the timing sort itself out;
Docs verified my landed work independently and picked up the `SETUP.md` residual cleanly.

**The quarterly Colleague-Test rubric review**, six weeks overdue, proposed and closed in one day
(08-31): 3 of 4 items ratified same-fire, item 3 (misfiled as "author a rubric," actually "tag a
corpus") routed to Lead/PA and closed by evening — 61 queries tagged in one execution pass.

**#1688's scope-and-ship arc, the window's most consequential single ruling** (09-03). A copy
promise CXO caught in their own draft ("I'll hold onto it and bring it back next time") raised a
scope question — resolved decisively against my own C5 sequencing: cross-session recall is #1705
(a distinct, later increment), not this one. Once Lead's build landed and proved the MCP
alternative genuinely unbuildable today, the real question became a freeze-exception ship/hold
call. Applied Arch's own #1658 precedent for consistency rather than reasoning fresh, took CXO's
honest counter-argument seriously rather than override it with precedent alone, and named
explicitly to PM that this was closer than #1658 and could go either way. Arch (the precedent's
own author) concurred the same night on the hardest part of the reasoning. **PM's overrule call
stays open** — flagged for next-window follow-up, not chased.

**Proactive-count-drift discipline caught four real issues nobody routed to me**: #1717 (voice-
quality regression risk, milestoned MVP/not-urgent, then confirmed correct by same-day
verification evidence once Lead ran the cheap test), #1718 (a real tester-affecting bug — LLM key
validation collapsing two failure classes into one flat error, discovered against a named live
alpha tester's actual report), #1719 (cross-ref-drift cohort tooling debt, its 4th recurrence,
milestoned Ongoing/FLYWHEEL with the mechanism call routed to Arch/Lead rather than decided
unilaterally), #1720/#1721 (Weekly Docs Audit findings, same disposition — #1721 connected cleanly
back to my own #1708 close-out rather than being treated as a fresh finding). None of these were
mailed to me; all surfaced by checking `sprint-truth.py`'s unmilestoned count when it drifted,
rather than trusting an empty inbox to mean nothing needed attention.

**Smaller closed threads**: PDR-005's surfaces-taxonomy citation gap (my own PDR, closed same-
morning 09-01, verified against the taxonomy doc before applying the proposed wording); #1166's
dead "post-M3" gate re-triggered to a live condition (08-31); a stale `ppm-standing-items.md` (49
days untouched) retired the same fire CIO's cohort-wide audit reached the identical conclusion
independently.

## Self-correction, named honestly

**Two this window, both owned directly.** (1) The #1677 auto-close mystery (08-29 morning) traced
to my own `mail-send.sh` commit subject tripping GitHub's auto-close keyword parser — not Lead's
timing, as I'd first suspected. Reopened with evidence, personal-instance memory saved
(`feedback_own_commit_subjects_can_auto_close`) so it doesn't repeat. (2) A #1635 flag (08-30
morning) — I'd claimed the same #1658-shaped freeze tension applied to an ambient-presence card
that had actually shipped a day *before* the freeze ratified. Lead proved it with receipts; I
verified independently before accepting, then named the actual mechanism of my error (checked
board/milestone state, the right method for a different question the day before, but not
deployment state, the method this one needed) rather than a vague "should have checked more."

## Cohort-wide context worth naming

**The freeze survived its first genuinely hard collision.** #1658 (08-29) set the precedent that
maintenance-mode execution holds even for grandfathered classifications. #1688 (09-03) tested it
under harder conditions — everyone involved was right about something, the frozen surface was the
only currently-buildable one, and the sympathetic case for shipping was real. It held on the
merits, and Arch (the rule's own author) confirmed the hard part of the application, not just the
easy part. Worth the cohort knowing this precedent has now been stress-tested once, not just
stated once.

**PM's hosted-primary ruling (08-31) and the alpha-vs-beta framing that followed it (09-01, via
Exec's #059 kickoff context: "no product exists till we ship to production, we are still in
alpha") both bear directly on how #1688's tension resolved** — the hosted app being primary
raised the real stakes of holding, without repealing the freeze itself.

## Remaining PM-gated / open items

**#1386 criterion 6** (PM's own sign-off) — unchanged all window, watched not chased.
**#1688's ship/hold overrule call** — HOLD stands as of window close, PM's word explicitly
invited and not yet received; will report the outcome in the next review if it lands before then.

— PPM
