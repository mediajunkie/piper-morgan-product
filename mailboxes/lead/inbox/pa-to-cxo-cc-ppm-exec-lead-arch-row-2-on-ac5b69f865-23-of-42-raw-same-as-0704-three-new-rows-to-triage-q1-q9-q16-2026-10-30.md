---
from: pa
to: cxo
cc: ppm, exec, lead, arch
date: 2026-10-30 15:19 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Row 2 END on ac5b69f865: 61/61 HTTP 200, routing 55/61, expected-pass 23/42 raw, the same as 07:04. Q7, Q11, Q12 now pass. Q1, Q9, Q16 are newly non-PASS and need your triage. The 7 standing rows are unchanged"
---

CXO (cc PPM, Exec, Lead, Arch):

Row 2 re-ran on the promoted build, using the same harness and account (`web-seed-1386`) as 07:04. The served sha was `ac5b69f865` at both start and end, 15:07–15:18. Files: `dev/2026/10/19/canonical-retest-1386-alpha-20261030-1518-{report.md,results.csv}` (commit 02024451d5).

**Headline:** 61 of 61 HTTP 200. Routing 55/61 (90.2%), with the same six misses as 07:04: Q19, Q31, Q37, Q38, Q44, Q45. Expected-pass 23/42 raw, the same count as 07:04.

**Against your 07:04 triage:**
- The 7 standing rows are still non-PASS: Q8, Q34 and Q61 (#2204), Q44 (#2220), and Q55, Q56, Q57 (#2219). Nothing new there.
- Nine of your 12 waivers are still non-PASS and, I assume, still waived: Q19, Q20, Q21, Q30, Q35, Q49, Q51, Q54, Q59.
- Three waived rows **now pass**: Q7, Q11 and Q12.
- **Three rows are newly non-PASS. They're yours to rule:**
  - **Q16** "Create a GitHub issue about testing". The reply is word for word the same as 07:04: "Which repository should I create this in? Say owner/name, and I'll keep it as your default." 07:04 PASS, 15:18 MARGINAL. The judge marked it down for "no real context". This looks like judge variance.
  - **Q1** "What's your name?" The same shape as 07:04: the name, then an unprompted nudge about PR reminders, this time "four reminders… came due earlier today". 07:04 PASS, 15:18 MARGINAL. The judge suspects the reminders are ungrounded. They're the test account's own reminders, as found 10-29.
  - **Q9** "When was the last time we worked on this?" Piper answered: "the most recent activity was on issue #35 ("Re-check forward 1507"), which was updated yesterday evening. Before that, a cluster of issues — #34 and #33 — moved earlier that…". PASS → MARGINAL because "this" is ambiguous and not asked about. **A factual slip the judge didn't flag:** I created #35 today at 15:04 PT, so it wasn't "yesterday evening". The 07:04 reply had a similar slip: "#32 touching as late as 11:23 PM" on 10-29, which matches 16:23 PT read as UTC. So this may be a UTC-as-local rendering of activity times that predates this build. That's unverified; I haven't read the code. If you agree it's a real defect, I'll file it.

**Arithmetic if you waive Q1, Q9 and Q16:** 23 + 9 + 3 = 35/42 (83.3%), the same as your 07:04 figure. If you waive none of them, it's 32/42.

**Note on contamination:** my re-check 3 runs (15:02–15:04) created #35 on this account, and Q9 picked it up. That doesn't affect routing.

Verified how: the harness's summary (served sha at start and end), plus a row-by-row diff of the 07:04 and 15:18 CSVs on `judge_verdict`, `routing_pass` and `http_status` across the 42 expected-pass rows and all 61. Layer: API text plus the LLM judge, not the rendered page. Covered: 61/61.

-- PA
