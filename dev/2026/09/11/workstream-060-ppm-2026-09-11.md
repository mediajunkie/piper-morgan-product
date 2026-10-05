# Workstream Review — Ship #060 (PPM)

**Window**: Friday 04 September → Thursday 10 September 2026
**Filed**: 2026-09-11 (same-fire as kickoff)

## One paragraph, if that's all PM reads

The week's real shape was two things: proactive triage kept finding real unrouted work
(`#1718`→`#1745`, none of it routed by mail), and PPM took on direct product ownership for the
first time at this scale — building `dev/active/mvp-epic-order-2026-09-09.md`, the ordered-epics
artifact Lead now actually works from, after PM's real-data correction to Exec's throughput
narrative named PPM directly. The week's most important moment wasn't a finding about someone
else's work, though — it was catching two of my own repeating mistakes (an overclaim on `#1688`'s
render state, and a mailbox-structure defect that had silently recurred for a month, 9x bigger)
and fixing the second one structurally rather than cleaning it up a fourth time.

## What moved

- **`#1386` (public-beta gate)**: framing corrected twice this week under real scrutiny —
  criterion 3 confirmed as the oldest evidence in the gate (2026-07-12), the shape tightened from
  "only criterion 6 remains" to "criteria 2/3/4/5 all re-run fresh at MVP close, only criterion 1
  unqualified." Not a criterion closed — the gate's own accuracy improved, which matters more
  going into MVP close.
- **`#1688` (FTUX interview)**: PM overruled PPM's HOLD ("flip ftux"), fully closed both threads
  by 09-08 — the flag confirmed live via render check, and an adjacent honesty finding (a
  pre-existing promise-shaped line) resolved to a cut matching PPM's own 09-03 scope ruling.
- **The ordered-epics directive (09-09)**: PM's real-data correction to Exec's throughput
  narrative (MVP averaged ~25/week, not the 4-7 quoted; the collapse was plausibly verification-
  gating during PM's absence, not chronic under-targeting) produced four directives naming PPM
  directly. Built `dev/active/mvp-epic-order-2026-09-09.md` from Arch's cause-factoring — 37
  items, 8 dependency-ordered epics, 6 honest singletons — and kept it current all week as three
  items closed and two epics' shapes corrected under real findings.
- **The scope-guard (09-09/10)**: named as an open mechanism question rather than fake-solved
  same-day; CIO+Arch answered it within 24 hours with PPM as the named consumer (flags land as
  mail, not an unwatched issue comment). Its real synthetic test caught a genuine false-clear
  (bot couldn't push to protected main, a retry loop was swallowing the failure) before the
  advisory period rather than during it. As of Thursday: blocked on one PM repo-settings decision,
  not a PPM call.
- **`#1743`/`#1745` (mailbox structure)**: found and fixed a genuine, month-old recurring defect
  in my own triage practice — a nesting-mistake fixed once on 08-10, silently repeated for a
  month, 9x bigger by 09-10. Installed a CI-enforced structural invariant this time rather than a
  fourth manual cleanup, verified by watching the actual GitHub Actions run go green.

## What didn't move

- **`#1731`** (a `mail-send.sh` silent-drop PPM reported): still genuinely open and unconfirmed.
  CIO's good-faith repro attempt this week didn't reproduce it. No urgency from anyone in the
  thread; not something I'm chasing.
- **The flywheel re-evaluation**: contributed Q1 (adopted verbatim as D6 in the ratified text) but
  the workstream itself was Arch's to lead — PM ratified the text this morning (09-11, just
  outside this window), so it closes cleanly right at the boundary.

## Progress toward milestone status, not activity

`sprint-truth.py` across the week (Pacific, same tool each time, not hand-counted): opened the
window around `MVP: 50 not done; 1116 done` (09-06 close) and closed it at
`MVP: 45 not done (35 Sprint Backlog, 3 In Progress, 7 In Review); 1133 done` (09-10 close, 0
unmilestoned). Real net progress — fewer not-done, 17 more done — despite the count fluctuating
mid-week as new issues were filed and triaged (a milestone-scoped count going up when work is
being found, not lost, is the correct behavior, not a regression; see `#1718`-class proactive
finds above). **Excluding this claim from anything stronger**: this reflects the whole cohort's
closures, not PPM's own work product — PPM's own contribution this week was triage, ordering, and
process infrastructure (the epic order, the scope-guard, the nesting invariant), not code that
closes MVP issues directly.

## What I'd want PM to know that isn't in a bullet above

Two corrections landed on my own work this week, both real and both handled the same way: verify
the claim myself before accepting or defending, then fix the actual cause rather than the
symptom. The `#1688` overclaim was caught and corrected same-day. The mailbox defect took a month
to surface as a pattern rather than three isolated incidents, and the difference this time was
installing a check that would catch a fourth recurrence without anyone having to remember to look.
