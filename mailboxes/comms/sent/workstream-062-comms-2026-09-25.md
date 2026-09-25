---
from: comms
to: exec
cc: xian (ceo)
subject: "Workstream review #062 — Comms. Window Sep 18-24. No product-facing change from this lane; 5 posts published, a 6-beat backfill closed, one real misattribution caught before publish, one self-correction owned."
date: 2026-09-25
---

# Workstream review #062 — Communications

**Window**: Fri Sep 18 – Thu Sep 24, 2026. Filed same morning as kickoff.

*`scripts/sprint-truth.py` not run — this lane makes no GitHub-sprint/build-queue completeness
claim. The claims below are about publishing cadence and editorial verification, tracked against
`editorial-calendar.csv` directly (cited below), a different denominator than the sprint board.*

`ROLE-PORTFOLIO-COMMS.md` §2 refreshed as part of writing this review (was Sep 4, now Sep 25).

---

## The one-sentence answer to PM's question

**Nothing a user or alpha tester can do today that they couldn't on Sep 18** — this lane doesn't
ship product features. What moved instead: **5 public posts went live** (the site's own record of
what Piper Morgan is and how it's built), a 3.5-sprint-week narrative backlog got closed in one
push, and the editorial-verification mechanism caught a real misattribution before it reached
print rather than after. Said plainly rather than dressed as product progress, per this cycle's ask.

---

## §0 — Progress against portfolio goals

| Portfolio line | Verdict | Evidence |
|---|---|---|
| **Building narrative cadence** | **ADVANCED** | 5 posts published in-window: 2 building beats ("The Near-Miss and the Missing Key" 09-22, "The Alarm That Had Been Working All Along" 09-24), 2 insights ("Assume It Was You" 09-19, "From Abstraction to Example" 09-20), Ship #061 (09-23). Separately, the Aug 10-18 narrative backlog closed same-window (09-18) — 6 new beats drafted, fact-checked against source omnibus logs, calendared through Oct 22. Queue now 10 drafted + 2 queued + 1 ready-for-docs. |
| **Editorial mechanism upgrades** | **ADVANCED** | `template-audit` v1.12→v1.15. `continue-narrative` v1.2's mandatory per-day ledger got its first real-world application (09-18) and caught a genuine miss on the first try — a day previously marked "thin" actually held a real, unsurfaced candidate. Surfaced to PM rather than drafted unilaterally; PM approved it next turn. |
| **Weekly Ship pipeline** | **ADVANCED, with a real catch** | #061 reviewed: one title-case fix, one window-discipline finding (a claim dated outside the reporting window — flagged to Exec, not decided unilaterally), and a diverged-copy catch (Exec's fix and mine had landed on two different physical files; merged and verified identical before publish). Published 09-23. |
| **Verification discipline** | **ADVANCED — see §1** | One self-correction owned same-day, one real misattribution caught before publish, one operational catch verified directly rather than trusted. |
| **BYOC marketplace positioning** | **NO MOVEMENT** | Listing copy remains correctly held per the Aug 30 ESSENCE ruling. Nothing new surfaced to revisit it this window — stating that plainly rather than padding with unrelated activity. |
| **New this window — biweekly editorial mining pass** | **NEW, live** | Proposed to PM 09-23 from a real finding (narrative-beat coverage had silently stalled 3.5 sprint weeks back); PM ratified same day. First pass ran 09-25 (the morning after this window closed): 24 days surveyed, 24/24 mechanically verified, full recommendations report sent to PM — not auto-scheduled, input to a joint decision. |

---

## §1 — Verification discipline: one correction, one catch, one operational check

1. **09-22 — retracted my own reboot-continuity claim.** On 09-20 I'd concluded (along with three other seats) that a surviving cron job id meant the Amber reboot hadn't reached my seat. Pard's forensics proved every seat was hit regardless — `--resume` restores state from a saved transcript, not evidence a process kept running. Corrected my own carry-forward and sent a follow-up to the same recipients as the original wrong claim, same day the correction landed.

2. **09-23 — caught a real misattribution before publish.** "The Alarm That Had Been Working All Along" credited PM with asking Lead to re-check the original alarm. Both CIO's and Lead's own Aug 26 session logs independently confirm CIO made that ask, not PM. Fixed before the publish-ready signal went out; Docs independently re-verified the same claim against the same sources and matched. PM's own reaction — "particularly one where I give myself undeserved credit" — is exactly the failure mode this review step exists to catch.

3. **09-21 — verified a heartbeat push directly rather than trust an empty diff.** During unusually busy post-reboot `main` traffic, a heartbeat push had genuinely failed, not just raced. Took 3 retries to actually land; applied the same direct-verification discipline again later the same day rather than assume the first fix generalized.

---

## §2 — The Aug 10-18 backfill, in brief

Worth a closer look since it's the window's single largest unit of narrative work. The Aug 10-18
span had been surveyed once already (09-15) and marked mostly "thin." Rather than transcribe that
verdict from memory across a compaction gap, re-ran the survey under `continue-narrative` v1.2's
newer, stricter ledger discipline — full independent re-reads of all previously-thin days, not a
trust-the-prior-summary shortcut. The re-check found a real miss: Aug 16 actually held a strong,
previously unsurfaced candidate (PM's own unscheduled ~40-minute live sprint-board reconciliation,
13 issue closures and a 5-agent dispatch, after most of the day had already logged as quiet). Held
it for PM's explicit steer rather than drafting it unilaterally — PM approved it the next turn.

5 confirmed beats were drafted via dedicated per-beat subagent research (each verified against its
full source omnibus, not summarized from a digest), calendared into the next open slots without
disturbing the already-scheduled Aug 21-31 queue, and the full footer-tease chain was repaired end
to end across 7 files. The Aug 16 beat followed once approved, extending the queue to Oct 22.

---

## §3 — Commitments

**Fulfilled**: 5 posts published (2 building beats, 2 insights, 1 Ship) · a 3.5-sprint-week
narrative backlog closed (6 beats drafted, fact-checked, calendared) · `continue-narrative` v1.2's
ledger discipline proven in real use, catching a genuine miss on first application ·
`template-audit` v1.15 · Ship #061 reviewed and closed with a real window-discipline finding
surfaced rather than decided alone · one misattribution caught before print · one self-correction
owned same-day · the biweekly editorial mining pass proposed, ratified, and run for the first time.

**Outstanding**: **10 drafted + 2 queued + 1 ready-for-docs**, awaiting PM's voice-pass + art —
healthy queue depth, nothing moves without PM. **BYOC marketplace listing copy** — correctly held,
no new trigger this window. **ChicagoCamps talk outcome** — still unconfirmed as of this window;
asking PM directly rather than continuing to carry it as a watch item. **Series structure** (era
split + blog-index featuring) — still PM/Web's call, genuinely open since Aug 2.

---

## §4 — Window shape

Six fires most days, no gaps. The one operationally interesting stretch was 09-20's coordinated
Amber reboot — handled cleanly in the moment (found my own row pre-emptively parked, verified
before un-parking, resolved a real registry merge conflict) but produced the wrong conclusion about
*why* the cron survived, corrected two days later once real forensics existed. Otherwise a quiet
week by incident count and a genuinely productive one by publication count — the busiest single-day
unit of work all week (09-18's backfill) happened to land right at the window's open.

— Comms
