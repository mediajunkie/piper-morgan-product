# Usage-correlation model — first empirical pass (commits vs. token spend)

**Author**: PA. **Filed**: 2026-09-21 (13:12 fire). **Status**: EXPLORATORY, UNCALIBRATED —
correlating two proxies against each other, not against PM's ground truth. Read this alongside
`dev/active/usage-correlation-model-prior-art-2026-09-20.md`, which explains why that distinction
matters (errors-in-variables literature: internal consistency ≠ calibration).

## Why this exists now, not sooner

Exec answered the data-source question this fire (`mailboxes/pa/inbox/ack-exec-to-pa-cc-pm-agree-
option-2-2026-09-21.md`): keep the two threads separate, use `scripts/usage-audit.py` as an input,
"build your own correlation layer rather than wait on mine." **Q1 (calibration-shape, does Lead's
usage-per-account proposal get built) is still unanswered** — so this is exploratory proxy-to-proxy
work, explicitly not the calibrated model. Doing it now because it's unblocked, not because it
substitutes for the still-open question.

## Method

Ran `scripts/usage-audit.py` (Exec's, rerun rather than re-derived) for the current weekly window
(2026-09-18 05:00Z onward). Cross-referenced against `git log --oneline --all --since=<same window>`,
counting commits per role-tag (`(role)` in each commit subject — this cohort's own convention).
Eleven seats, both figures pulled live this fire.

## The numbers

| seat | commits | weighted tokens (M) | token share |
|---|---|---|---|
| lead | 123 | 87.7 | 16.8% |
| docs | 84 | 84.5 | 16.2% |
| host | 88 | 53.7 | 10.3% |
| exec | 178 | 48.6 | 9.3% |
| comms | 87 | 47.4 | 9.1% |
| ppm | 58 | 41.9 | 8.0% |
| cxo | 75 | 35.7 | 6.8% |
| cio | 41 | 33.4 | 6.4% |
| pa | 61 | 30.7 | 5.9% |
| arch | 64 | 30.1 | 5.8% |
| web | 79 | 28.4 | 5.4% |

**Pearson r (commits, tokens) = 0.435** — moderate. **Spearman rho (rank correlation) = 0.664** —
notably stronger. The gap between the two is itself informative: the relationship looks more
monotonic-but-nonlinear than linear, consistent with token cost per turn varying by role/task type
(context-heavy work vs. many-small-commits work) more than by raw "how much got done."

**Biggest residuals from a naive linear fit** (commits predicting tokens):
- **docs** (+37.3M) and **lead** (+31.1M) spend far more tokens per commit than the fleet average —
  plausible given Lead's known large average context (478k/turn per Exec's audit) and Docs'
  synthesis-heavy work (reading many source logs per commit).
- **exec** (−21.4M) is the sharpest negative outlier — most commits on the fleet (178) but
  mid-pack token share. Commits are cheap for Exec relative to the average, i.e. many small,
  low-context commits rather than few token-heavy ones.

## What this does and doesn't show

**Does show**: commits and token spend are related but not interchangeable proxies for "how much
work happened" — a role can lead on one axis and lag on the other, and the direction of the gap is
informative about *how* a role works (many-cheap-commits vs. few-expensive-ones), not just *how much*.

**Doesn't show**: anything about PM's actual usage/engagement, which is the thing standing item #3
was originally tasked to explain. Commits and tokens are both internal proxies; this is exactly the
"internally consistent, not calibrated" case the prior-art pass warned about. **Do not read this as
progress toward answering PM's original question** — it's progress toward having a correlation
*layer* ready to calibrate once Q1 is answered, per Exec's own framing.

**n=11, one week, one snapshot.** No claim about stability over time or across a different week
(e.g. a week with a big one-off dispatch would shift this substantially — see Exec's own audit
noting `isSidechain=0` this particular week, ruling out the 09-14-style dispatch-concentration
pattern for this window specifically, which won't hold every week).

## Next steps, not yet done

- Re-run in a future week to see if the commits/tokens relationship is stable or this week's
  specific.
- Add session-log line growth and mail volume as further proxy dimensions (Exec's original list) —
  not done this fire, scope-bounded to the two dimensions already in hand.
- Still waiting on Q1 for any actual calibration against PM's usage reading.

**Verified how**: `scripts/usage-audit.py` run live this fire, output pasted directly above, not
summarized. Commit counts from a live `git log` this fire, same window, cross-checked the role-tag
convention against several commits by eye before trusting the grep. Correlation math run via a
one-off Python script this fire (Pearson + Spearman, standard formulas, no library dependency
beyond `statistics`) — **not independently reviewed by a second method**, so treat the exact
coefficients as indicative, not final.
