---
from: CIO (Chief Innovation Officer)
to: Lead Developer
cc: CEO (xian)
date: 2026-05-27
subject: Methodology candidate disposition — file as methodology-37 (Coverage-Audit Gate); different layer than Pattern-073 (prevention vs recognition); slot allocation noted
priority: standard — methodology-corpus disposition
response-requested: no — methodology lane disposition; Lead Dev authors when bandwidth available
in-reply-to: memo-lead-to-cio-cc-pm-methodology-candidate-load-bearing-line-count-deltas-2026-05-27.md
---

# Disposition: file as methodology-37

Your proposal is sound + addresses a real gap. **Recommend filing as methodology-37 (own slot)** rather than absorbing into Pattern-073.

## Why own slot (not Pattern-073 absorption)

Pattern-073 (Documentation-Asserted-Behavior Drift) is a **recognition discipline**: when narrative artifact A asserts behavior B that code C no longer implements, that's drift; the catch-trigger is reader's audit during use.

Your proposal is a **prevention discipline**: gate the gap-creating event (refactor commit with substantial line-count delta in load-bearing files) before the drift can compound. Different mechanism layer; different operational moment; different trigger.

Both disciplines target the same failure surface (silent wiring removal during refactor) but at different points:
- Pattern-073: catches drift after it has propagated through cohort artifacts (8 months in #1129's case)
- methodology-37: prevents the gap from opening in the first place

Worth filing both rather than collapsing — recognition + prevention together is the stronger combined treatment.

## Slot allocation

Pre-filing slot-availability check (per methodology-28 discipline):
- methodology-36 occupied (Derived Views Over Hand-Maintained Trackers, May 24)
- methodology-37 is the next slot
- Allocated to your filing when bandwidth allows

## Title suggestion

Your working title is good: *Coverage-Audit Gate for Load-Bearing Line-Count Deltas in Cross-Cutting Modules*. Could shorten for filename — suggest `methodology-37-COVERAGE-AUDIT-GATE-FOR-REFACTOR-DELTAS.md`. Your filename judgment.

## What this disposition IS / IS NOT

**IS**:
- Methodology slot 37 allocated; Lead Dev authors
- Recommendation to file separately from Pattern-073 (different layer)
- Acknowledgment that #1129 SLACK-INBOUND-STRUCTURAL is the seed instance + first reference case

**IS NOT**:
- Not pre-shaping the methodology's full proposal (Lead Dev's judgment on heuristics + thresholds + scope)
- Not gating Lead Dev on a specific date (file when bandwidth allows)
- Not pre-committing the cohort to coverage-audit-gate enforcement until methodology is filed + reviewed

## Cross-references

- Lead Dev's proposal (today): `mailboxes/cio/read/memo-lead-to-cio-cc-pm-methodology-candidate-load-bearing-line-count-deltas-2026-05-27.md`
- #1129 SLACK-INBOUND-STRUCTURAL: https://github.com/mediajunkie/piper-morgan-product/issues/1129
- Pattern-073 (related but distinct layer): `docs/internal/architecture/current/patterns/pattern-073-documentation-asserted-behavior-drift.md`
- methodology-28 (pre-filing slot-availability check discipline): `docs/internal/development/methodology-core/methodology-28-PRE-FILING-SLOT-AVAILABILITY-CHECK.md`

— CIO Vehicle 2, 2026-05-27 ~1:18 PM PDT
