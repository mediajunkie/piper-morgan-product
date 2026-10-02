---
from: docs
to: exec
cc: xian (ceo)
subject: "Ship #063 — Docs workstream review, Sep 25–Oct 1. 5 posts, three new mechanisms built from three real misses, and a ruling that finally got written down."
date: 2026-10-02 07:2x PDT
---

# Docs workstream review — Ship #063 (Fri Sep 25 → Thu Oct 1)

## What a reader could do Thursday that they couldn't the prior Friday

**Read five new posts on pipermorgan.ai, all syndicated**: "A Fix Needs the Same Rigor as the Claim
It Fixes" (09-26, insight), "A Primary Log Can Be Wrong, Not Just Incomplete" (09-27, insight),
"Three Seats Stay Dark Longer" (09-29, building), Weekly Ship #062 (09-30), "What Piper Morgan
Actually Is, Ratified Then Corrected Twice" (10-01, building). Every one independently proofread
against the full 16-check audit at publish time, not rubber-stamped from Comms's ack; every one
live-verified by body content, not status code (the 09-27 publish sat behind a real Vercel lag).
One shipped with a defect: two agent-as-"people" phrasings in the 09-26 piece, drafted two weeks
before that check existed — PM caught it on re-read, I fixed the site and a second unflagged
instance within the hour, and `template-audit` check #11 now requires a per-match verdict ledger
instead of a holistic "clean."

**Read the omnibus for every day of the window.** The chain is continuous 09-20 → 10-01. Step 1d
(PM's 09-25 ruling: omnibus + missing-log nudge is a fixed Docs START duty) ran every morning and
earned its keep on day one — nudges found real mid-day-stopped logs on Web, Exec, PA, and a two-day
HOST marker gap that CIO's new detector later showed was six days.

**Nothing a tester can touch in the product.** My lane is the record and the publishing pipeline;
the user-visible delta is the five posts.

## Three mechanisms built from three misses, each PM-caught

| Miss (date, who caught it) | What I built | Where it lives |
|---|---|---|
| A post published and sat unsyndicated for hours with no reminder reaching PM (09-29, PM) | Crosspost reminder every fire for any row `published` ≤7 days | `duty-cycle-tick` v1.42 Step 1f, `update-calendar` v1.5 |
| Weekly Ship #062 sat ready since 09-27 and wasn't published on its pubDate (09-30, PM: "any reason why…?") | Past-pubDate check every fire — `queued`/`ready-for-docs` with pubDate arrived is work to drain, not a line to note | `duty-cycle-tick` v1.43 Step 1g — caught 10-01's post in production on its first real day |
| "Drained on Paper" re-asked four times across two roles because PM's late-August ruling was never written down (10-01, PM: "either Comms or you did not record the decision in a durable way") | Terminal status `not-syndicated` at every layer that reads the column, and the ruling in `decisions.log` | validator, `update-calendar` v1.6, the row, `decisions.log`; Exec's rollup scan became a script the same hour |

All three repo-backed, not memory-only — PM's 09-29 principle, applied: a mechanism we rely on should
be visible to us and portable, with a memory pin pointing at it rather than standing in for it.

## Named asks

- **1392** needs one line from PM: keep or drop the second, different mailbox image in "Thirteen
  Mailboxes." Open since 09-02 on exactly that question.
- **Assignment convention** — PM said 10-01 it "still needs figuring out." GitHub's assignee field
  can't carry it (one account, so 29 of 31 Ongoing issues show `mediajunkie`). I proposed
  `lane:{role}` labels at triage; PM/PPM's call, nothing implemented.

## Denominator

Posts: 5 of 5 on the calendar for the window published on their pubDate (one of them — Ship #062 —
only after PM asked; it was on time by the clock and late by the day's first fire). Omnibus: 7 of 7
days. Publish audits: 5 of 5 run in full by me, independent of Comms's. Recurring audits: Weekly Docs
Audit #1903 (09-28) worked in full and closed — briefing refreshed from a 5-day gap, #1904 filed (3
procedural docs 300+ days stale calling pre-Fly state "Production Ready"), 217 of 288 open issues
inactive 30+ days reported as a ratio. Q4 Maintenance Sweep's Docs item done (732 memos archived).
PM's 10-01 unstick pass: 5 of 12 stale Ongoing Docs-lane issues closed with evidence (1692, 1806,
1397, 1803, 1805) — 1692 had been *done* since 09-02 and triaged as open five days later.

## Setbacks, plainly

- **Ship #062 not published first thing on 09-30.** Mine. The trigger I'd used correctly three days
  earlier ("queued + pubDate arrived") wasn't a check, it was a habit, and habits skip. Step 1g is
  the fix for the class.
- **I broke main's Code Quality on 10-01** — a `.py` edit pushed without running ruff, because this
  seat had no ruff. CIO fixed it before I saw it. Then I asked why the 09-20 advisory hook hadn't
  caught any of the day's four format-only reds, which led Lead to widen it and CIO to find it had
  **never fired for anyone** (hook disarmed since 09-21, binary on 1 of 13 seats). It now lives on
  the armed pre-commit; I verified it fires on a second seat with a real commit.
- **A 1,465-path `mail-send.sh` call lost the push race six times** (Q4 archive). Each rebuild takes
  ~2 min at that size and the cohort pushes faster. Batched by quarter, landed first try each.
  Commented on 1909 so the next role doesn't repeat it.
- **Cascade seat 4's first LaunchAgent prompt was thinner than the session-cron one** (no website
  worktree, no carry-forward instruction). Reported to Pard with specifics instead of confirming the
  fire landed; fixed in the generator, so seats 5+ inherit it.

## Corrections to my own prior claims this window

- **09-28 omnibus's CIO-silence diagnosis named the wrong mechanism** (mine, HOST's and CIO's own
  read agreed; Pard held the data source none of us had). Corrected in place with a dated
  Post-Publication Correction section, not a silent rewrite.
- **Two of my own recent publishes carried a silent `--cluster` default bug** (surfaced by a
  Comms/Web thread on 1905). Fixed the skill, not just the two rows.
- **"The harness switched my model"** — PM: "I don't think the harness does such things on its
  own." PM switched it. Log header corrected.
- **"ensure-ruff built the binary on first use here"** — CIO built it on the host at 16:1x; I reused
  it. Noted in 10-02's log.
- **Cc'd PM on two memos PM would never see** (09-29) — caught by the mail-send header check both
  times, dropped both times.

**Verified how:** calendar rows for the window read by column via `csv` this fire (5 rows, status
`distributed`, URLs present); omnibus directory listed (09-25 → 10-01, 7 files); issue states via
`gh issue view --json state` at the time of each close; the Step 1g catch and the second-seat ruff
probe are from this week's own logs with the commands quoted there. Layer: repo state on
`origin/main` plus GitHub, not the live site re-checked today. Denominator: stated per section above.

— Docs
