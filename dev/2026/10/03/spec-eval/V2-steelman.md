---
type: verification
title: "V2: steelman of the current process vs. the synthesis draft"
author: V2 (independent verifier)
date: 2026-10-03
inputs: synthesis-draft.md, D0-history-metrics.md, metrics/m1_monthly.csv, metrics/h4_monthly.csv, F-operating-model.md, G-strategy-vs-reality.md, decisions.log, omnibus logs 2026-09-01..03
---

# Steelman: the process is what is working

Each point is rated for how well the evidence supports it. Points the evidence does not support are marked as such rather than inflated.

## S1. Product throughput grew because of the cohort. NOT SUPPORTED (and it cuts against the synthesis too)

Source: `metrics/m1_monthly.csv`. Product commits (PC) per month:

| period | PC per month |
|---|---|
| 2025-06 to 2025-09 | 53, 52, 33, 22 |
| 2025-10, 2025-11 | 80, **205** |
| 2025-12 to 2026-03 (the baseline window is Jan–Mar) | 37, 97, 45, 67 |
| 2026-04 to 2026-07 (cohort/mail ramp) | 52, 127, **257**, 130 |
| 2026-08, 2026-09 | 187, 192 |

- 205 PCs in Nov 2025, with zero mail or heartbeat commits, is as high as Aug–Sep 2026.
- June 2026 (257) is higher than anything since.
- The 12-month mean (Oct 2025 – Sep 2026) is about 123 PCs a month. Aug–Sep is about 190, which is 1.5×, not 2.7×.
- The 2.7× comes from choosing Jan–Mar as B. Jan–Mar is a trough: 45–97 PCs a month, the post-burst lull after Nov.
- Lines changed: Jan 2026 was 68k, above Aug 52k and Sep 41k.
- No honest causal story "cohort → more product" survives. Equally, "cohort → stagnation" is not shown.

**Consequence for the synthesis.** The sentence "Product output did grow (PCs ~70/month → ~190/month)" and the headline "product commits grew about 2.7 times" both lean on a trough baseline. That helps the steelman's opponent *and* overstates the contrast.

## S2. Mechanisms prevented losses. PARTIAL: real, but invisible to a count of incidents

Evidence in the record:
- **Diff-before-reset worked.** 2026-09-02 omnibus (L287, L310, L322): "Two near-misses averted zero data loss: ~60MB of PM's uncommitted faoilean work preserved via a diff-before-reset check." This is the rule that CLAUDE.md wrote after the 06-21 and 08-08 incidents. It is one clean prevent-after-rule instance.
- **Guards firing live.**
  - The #1716 guard caught a mail recipient miss live (omnibus 09-01 L163).
  - The rollup's live-state pass caught the Ship #062 count error (43/34 → 91/57) before publication.
  - "Inversion never served a live turn" was caught in workstream-063.
  - The bearer lint found live tokens (#1885, #1845).
  - `mail-send.sh` removed the sweep and strand failure class.
- **The watchdog's real hits.** F §3 records 178 of 180 role-alerts as git-consistent real silences. F §4 then says "about 4–6 identifiable catches". Those two numbers are in the same report and conflict. Whether a silence mattered is a separate question, but 178 is not 4–6.
- **Structural asymmetry in the F §4 tally.**
  - Incidents are *recorded on purpose* as lessons: CLAUDE.md and `claude-md-history.log` exist to hold them.
  - Prevented events leave no incident. The 09-02 near-miss survives only because an omnibus noticed it.
  - F itself says "outcome language in logs is inconsistent" and "not searched exhaustively".
  - So 25 to 4–6 is a lower-bound-vs-undercount comparison, not a rate.
- **The 25 incidents are not all caused by the machinery.**
  - #3 is the subscription cap.
  - #10 is the usage freeze.
  - #19 is credentials.
  - #24 is a PM cc habit.
  - #23 is a missing memo.
  - #25 is churn, and it is the *same thing* as #22.
  - Several are "the machinery had a bug", which is the cost of any mechanism, and no baseline of incidents without the machinery exists.

**What the steelman cannot claim.** There is no evidence that *quality* improved (see S4). It can only say the safety-class rules have a plausible prevent record, which is exactly what R6/R7 already protect.

## S3. Coordination volume is cheap, because it is automated one-line commits. PARTIAL

Support:
- Of the 7,318 September coordination commits, `hb` 724 + `hb-last-invoked` 1,909 + `stop` 183 = 2,816 (38%) are machine-written one-liners. They cost almost no tokens. `mail` 1,755 and `log` 1,416 are real prose, but each is small.
- Git commit count is the wrong cost unit, and the synthesis says "commit counts measure granularity, not work".
- The 94.6× and 266× are partly an artifact: the baseline conventions did not exist (the synthesis admits this).

Limits (so it does not carry the whole argument):
- Real costs exist at other layers:
  - 63 fires a day × ~36k+ fixed tokens (D-1, F §1);
  - a 96% weekly cap (F §6);
  - 43 image builds in 9h, ~85% from heartbeat/log commits (F #22, medium confidence);
  - PM reading load.
- Those costs are not commit counts. The synthesis should price them directly, and not lean on the 38× C/P headline.

## S4. The defect proxy rise is an artifact. PARTIAL

`metrics/h4_monthly.csv`, d1+d2 per PC:
- 2025-08: 0.30; 2025-11: 0.34; 2025-12: **0.43**; 2026-01: 0.27; 2026-03: 0.21.
- 2026-05: 0.13; 2026-06: 0.24; 2026-07: 0.45; 2026-08: 0.35; 2026-09: 0.58.

Support for "artifact":
- "Rose from 0.21 (Mar) to 0.58 (Sep)" picks a local low as the start. Pre-mail Dec 2025 was already 0.43. The series is noisy, 0.05–0.58, with no clean monotone trend.
- d2 (a `fix` on a file touched in the last 72h) rises mechanically when a live system is under daily tester-in-the-loop use. In Sep, PM was testing the live card (decisions.log 09-30, #1906) and the alpha was live. Small iterative fixes are healthy there.
- The metric is a message-and-file-overlap proxy (D0 §Limits).

Against the artifact reading:
- d1 (reverts) is 0.172 in Sep, the highest ever, 33 reverts. That is not simply "iterative fixing".
- Sep is the series maximum.

Verdict: the rise is *ambiguous*, not clearly worse, and not clearly an artifact.

## S5. "No users" was a deliberate sequencing choice by the PM. LARGELY SUPPORTED

Evidence:
- decisions.log 2026-09-25 (lines about 2176–2181), PM verbatim:
  - "It's not urgent… we can wait til they try and fail."
  - "Getting to beta and getting the mcp to alpha testing are more important to me, relatively, than prompting the alpha testers."
  - "…recent testers should end up with genuinely working access."
- G-U5: the invite was ready 09-13 and held twice for BYOC defects (#1810, #1814). That is a deliberate quality hold. Reissues were then deferred, and the #1885 burn was a security item.
- G: a local alpha with 5–6 named testers ran Oct 2025 – Mar 2026, so the project has not been user-averse historically.
- The sprint theme was "getting to beta and getting the mcp to alpha testing" (09-25).
- PM's MVP criterion: "whether [new epics] are needed for the MVP… even if the date has to move again."

Limits:
- The 09-21 invite was sent with a *dead code*. That was a defect, not a choice.
- PM's choice to defer is exactly what R1 asks PM to reverse. That is a legitimate recommendation, but it is a priority disagreement, not an oversight the machine made.

## S6. Logs and mail are the memory that made this evaluation possible. SUPPORTED

- E (flywheel history), G (user timeline: June "first external tester" correction via omnibus 2026-07-16), F (incident table from `claude-md-history.log`, registry headers) and D0 (commit classes) were all reconstructed from these records.
- Counterpoint: the evaluation needed session logs and decisions.log, not 63 fires a day and 1,141 memos in 4 weeks. The synthesis's R3 and R7 already keep logs. The steelman supports "keep logs", not "keep volume".

## S7. Would R3/R4/R6 cause unpriced regressions? YES, several

- **R3 step 1 (heartbeats out of git).**
  - `duty-cycle-freeze-check.sh` reads git heartbeats (F §7 row B: "would need a local reader; off-machine visibility lost").
  - The watchdog, rollup Step 0, and `heartbeat-interior-coverage.py` all consume that signal.
  - The draft's "first step this week: move heartbeats out of git for every seat" does not price rewriting the reader.
  - Done blind, it creates a false-clear (the incident class listed as #9, #20).
- **R3 step 2 (cron to event wakes).**
  - F §7 row C lists the status-quo steelman: the cron catches work nobody signalled.
  - Event wakes need a dispatcher that does not yet exist.
  - Row D (fewer roles) is explicitly flagged by F as losing cross-role checking, the thing that caught #062 (this is one of the 4–6 catches).
- **R3 step 3 (retire watchers).** The 178-of-180 watchdog precision is not in the synthesis. Retire the ones with documented false-clears. Do not touch the per-role liveness watchdog before an event-wake replacement exists.
- **R3 success metric is gameable.** Coordination commits per PC "38 → <10" is met by step 1 alone, with no change in token cost, fires or reading load. Add a token or fire metric.
- **R3 owner.** CIO owns the watchdogs and is the 1,318-commit role. Co-owning the cut is a conflict of interest; PM or Lead should co-sign.
- **R4.** Mostly survives (it follows PM's own 09-11 ruling). The risk is a single point of failure in the rollup compiler. `check-unboarded-pm-items.sh` mitigates it, and the draft should name it.
- **R6 step 3 (drop BRIEFING-CURRENT-STATE from required reading).** The briefing is agent-facing in practice (F §2). The staleness mandate exists because roles used stale state (#13: audit on a checkout 33 commits stale). Dropping it needs a replacement shared-state surface and a check that roles are not re-deriving state, which would raise load.
- **R6 steps 1, 5.** A destructive-git guard is exactly what the steelman's best evidence (the 09-02 near-miss and the 06-21 and 08-08 losses) supports. The probe-gate on the slim CLAUDE.md is good practice. Hooks remain advisory, so the draft's "0 destructive-git incidents" metric should not be read as proof the hook works.

## Per-item assessment

| item | result | what must change |
|---|---|---|
| **H1** coordination cost dominates | **QUALIFY** | Keep SUPPORTED on the literal rule. Drop "product output did grow (~70 → ~190)" and "grew ~2.7×" as headlines: the B window is a trough (Nov 2025 = 205, Jun 2026 = 257; 12-mo mean ~123, so ~1.5×). State that 38% of Sep coordination commits are automated one-liners, so cost lives in tokens/fires/reading (S3), not in the 266×. |
| **H1b** redundancy | **SURVIVES** | Untouched by the steelman. |
| **H2** ruleset costly / poor fit | **SURVIVES** | Add one sentence: the safety-class rules have a plausible prevent record (09-02 near-miss), so the target is load and contradictions, not the rules' existence. |
| **H3** doc drift | **SURVIVES** (not contested) | none |
| **H4** process buys quality | **QUALIFY** | "Inconclusive" stands. Replace "0.21 (Mar) to 0.58 (Sep)" with the series range: 0.05–0.58, Dec 2025 already 0.43 before mail; Sep is the max and d1 reverts 0.17 is the least-ambiguous part. Add that d2 rises mechanically under live testing. Replace "Defects per product change rose rather than fell" in the opening bullets with "the defect proxy is noisy and at its maximum in Sep, which is not evidence of benefit." |
| **R1** users in 30 days | **QUALIFY** | Recast as a PM sequencing decision. Cite PM's 09-25 verbatim ("not urgent… wait til they try and fail"; beta and MCP more important than prompting testers) and the two BYOC-defect holds. Keep the substance (signup gate, feedback button), since the one invitee was sent a dead code. Do not describe the hold as neglect. |
| **R2** CI gate | **SURVIVES** | No process dependency; steelman is neutral. |
| **R3** cut coordination | **QUALIFY (substantive)** | Step 1 must include a replacement liveness reader first. Step 2 must name the dispatcher as a prerequisite and keep a 1×/day START. Step 3 must price watchdog precision (178/180). Replace the metric with fires/day and tokens/fire. Owner needs a non-CIO co-signer. Soften "25 incidents vs 4–6 catches" to a lower-bound comparison with the asymmetry caveat. |
| **R4** one PM channel | **SURVIVES** | Add the rollup single-point-of-failure note. Cites PM's own 09-11 ruling. |
| **R5** security hygiene | **SURVIVES** | Process-neutral. Credit the bearer lint and autoclose guard as working mechanisms (they caught the leaks). |
| **R6** ruleset refactor | **QUALIFY** | Steps 1, 2, 4, 5, 6 survive. Step 3 needs a replacement shared-state surface and a measure that roles are not re-deriving it. The "0 destructive-git incidents" metric should note that hooks are advisory. |
| **R7** primary surface; keep what works | **SURVIVES** | The steelman strengthens its "keep" list. |

## Wording changes for the synthesis

1. **Opening bullets.**
   - Replace "Total commits grew about 48 times (coordination commits about 266 times) while product commits grew about 2.7 times" with: "Coordination commits grew from near zero to ~7,300/month (38% are automated one-line heartbeats); product commits were ~190/month in Aug–Sep, comparable to Nov 2025 (205) and below Jun 2026 (257)."
   - Replace "Defects per product change rose rather than fell as the process mechanisms were added" with "The defect proxy is noisy (0.05–0.58, already 0.43 in Dec 2025, before mail) and at its maximum in Sep. It gives no evidence that the added mechanisms reduced defects."
2. **Opening paragraph.** After "very little at users", add: "In part this was deliberate: PM held invites for BYOC defects and ruled on 09-25 that beta and MCP outrank prompting testers (decisions.log). R1 asks PM to revisit that call."
3. **H1 row.** Delete "Product output did grow (PCs ~70/month → ~190/month)". Add "Product commits are ~1.5× the 12-month mean, and Nov 2025 and Jun 2026 were higher; the 2.7× rests on a trough baseline."
4. **H4 row.** Replace "0.21 (Mar) to 0.58 (Sep)" as described above. Add "reverts (d1) 0.17 in Sep is the least ambiguous signal". Add the two missing "demonstrably buys" items: the 09-02 diff-before-reset near-miss and the Ship #062 count correction.
5. **R3 Why.** Replace "≥25 recorded incidents … against ~4–6 recorded catches" with: "≥25 recorded incidents (not all machinery-caused) against 4–6 catches that were identified without an exhaustive search; incidents are recorded by design and prevented events are not, so this is a lower-bound comparison. The watchdog separately logged 178 git-consistent silence alerts of 180."
6. **R3 Change.** Add as a precondition to step 1: "ship a non-git liveness reader for freeze-check, the watchdog and the rollup first". Add as a precondition to step 2: "build the event dispatcher". Replace the metric (commits per PC) with "fires/day and tokens/fire".
7. **R6 step 3.** Add: "…after naming the replacement shared-state surface, and checking for the stale-state class (#13)".
8. **Do-nothing baseline and H1 text.** Say that the cohort at 96% of its cap is a token cost of fires. It is not evidence about commit counts.
