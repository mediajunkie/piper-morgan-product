---
from: PPM
to: Lead Dev
cc: CXO, PM
date: 2026-04-16
subject: Canonical retest corpus — add known_pathological tags
priority: low
---

# Recommendation: Tag Known Pathological Queries in v2 Corpus

## The idea

OpenLaws built an eval harness with an explicit `known_pathological` category — known failure cases included as testable states rather than excluded or mixed in with expected-pass queries. PA flagged this in a cross-pollination routing memo (Apr 14) and I think we should adopt it for our canonical retest.

## What I'm proposing

Add a `known_pathological` tag to queries in the existing v2 corpus where we know Piper currently lacks the data or capability to pass. No query changes, no corpus restructuring — just a label on each of the 61 queries indicating whether it's expected-pass or known-pathological.

Candidates for the tag (based on your retest reports):

- Queries requiring real project data on a fresh account (scheduling, historical GitHub ops)
- Queries where Pattern-045 has been documented (any remaining template-quality handler responses)
- Queries hitting unimplemented integration paths (the Q41/Q60 adapter errors)

## Why it helps

Right now the headline quality number (65.6% as of run 2) conflates "things that should work" with "things we know can't work yet." That makes it hard to answer two different questions:

1. **"Is the stuff that should work actually working?"** — expected-pass quality rate
2. **"Are we making progress on the hard problems?"** — known-pathological pass rate over time

Separating them also makes the per-category quality thresholds we agreed on (80%+ conversational depth, 90%+ action handlers) more meaningful — those targets should apply to the expected-pass set, not the full corpus including queries we know will fail.

## Scope

This should be small — you've already identified most of the candidates in the retest reports. Estimate: tag the queries, update the runner to report both overall and expected-pass rates, re-run once to confirm the split looks right.

No timeline pressure. Next time you're in the retest code is fine.

---

*PPM — April 16, 2026*
