# Usage-correlation model — current approach (overview)

**Author**: PA. **Filed**: 2026-09-22, at PM's direct request for a single consolidated reference.
This doc synthesizes two working documents rather than replacing them — see "Full detail" below
for the underlying evidence.

## The task, restated

PM (via Exec, 2026-09-20): stop hand-waving about what correlates with usage — build a real,
evidence-based model, and research prior art first. No deadline.

## Where this stands today, in one paragraph

Prior art is done and points to one clear design constraint: any model built from internally
measurable proxies (commits, tokens, mail volume, fires) needs to be **calibrated against a real
ground-truth reading of PM's actual usage**, or it's only internally consistent, not actually
informative about usage. A first exploratory pass (commits vs. token spend, all 11 seats) is done
and shows a real but moderate relationship — useful as a first data point, explicitly not a
finished answer. The model is genuinely blocked on one open question: **does a mechanism to
capture real usage readings get built** (see Q1, below) — without it, there's no way to calibrate
anything, ever, no matter how many more proxy dimensions get added.

## The four-step approach

1. **Prior art** (`dev/active/usage-correlation-model-prior-art-2026-09-20.md`) — four external
   fields converge on the same answer: software-engineering productivity metrics (the SPACE
   framework: no single metric is trustworthy alone), statistics (errors-in-variables/regression-
   calibration: cheap proxies need a validation subsample of paired ground-truth readings),
   LLM-fleet cost-observability tooling (trace-based per-agent attribution, the practitioner
   layer), and product-analytics leading-indicator frameworks (validate an indicator against
   history before trusting it). The load-bearing finding was internal, not external: Lead's own
   `usage-per-account-capture-2026-09-19.md` proposal already designs the exact calibration
   mechanism needed, and it has zero rows captured — unimplemented.

2. **Q1 — the calibration-shape question, sent to Exec/PM 09-20, still open.** Does Lead's
   proposal (or something like it) get built? This is the actual current blocker, not "no ground
   truth exists in principle" — the mechanism exists on paper, just not in practice.

3. **Q2 — resolved 09-21.** A separate, adjacent data source surfaced (Exec's own weekly
   token-usage audit, parsed from local Claude Code transcripts) — agreed with Exec to keep the
   two questions/models separate rather than merge them, using Exec's script as one input.

4. **First empirical pass, done 09-21** (`dev/active/usage-correlation-model-first-pass-
   2026-09-21.md`): commits vs. weighted token spend, all 11 seats, one week. Pearson r=0.435,
   Spearman rho=0.664 — a real, moderate relationship, with informative outliers (Exec: many cheap
   commits; Lead/Docs: fewer, more expensive ones). **Explicitly labeled exploratory and
   uncalibrated throughout** — this correlates two proxies against each other, not against PM's
   actual usage, and is not itself an answer to PM's original question.

## What's next, and what it's waiting on

- **If Q1 resolves yes** (the capture mechanism gets built): once even a handful of paired
  (proxy, real-usage) readings exist, the model becomes genuinely calibratable — build it then,
  not before.
- **If Q1 resolves no**: the honest, complete answer becomes "the proxies can't support a
  calibrated model without PM's numbers" — itself a useful finding, per Exec's own framing of the
  original tasking.
- **Independent of Q1**: the dispatch-tier dimension can still be developed further using Exec's
  transcript-parsing method, since it doesn't need PM's dashboard specifically.

## Full detail (not duplicated here)

- `dev/active/usage-correlation-model-prior-art-2026-09-20.md` — the full literature/tooling
  survey, two addenda, the dispatch-tier finding.
- `dev/active/usage-correlation-model-first-pass-2026-09-21.md` — the full empirical write-up,
  method, numbers, and caveats.
- `mailboxes/pa/sent/question-pa-to-exec-cc-pm-calibration-shape-for-usage-model-and-leads-
  unimplemented-proposal-2026-09-20.md` — Q1 as originally sent.
- `dev/active/usage-per-account-capture-2026-09-19.md` — Lead's original proposal (the thing Q1 is
  actually asking about).

**Verified how**: this is a synthesis of PA's own prior work this week, re-read in full before
writing this overview rather than summarized from memory. No new research run for this document.
