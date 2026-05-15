# Pattern Formation via Successful Imitation

## Overview

**Pattern Formation via Successful Imitation** names the discipline that produces durable architectural patterns through cohort recognition and reuse rather than top-down enforcement. The shape:

1. A reference implementation is shipped that is clean enough to be re-recognized at the next surface
2. A second surface faces a structurally similar problem and *reaches for the existing implementation* rather than building a new one
3. A third surface does the same, picking up the shape without explicit "use this pattern" guidance
4. The pattern is now real — three instances form the recognizable shape — and only at that point does formal pattern-catalog filing make sense

The discipline distinguishes pattern *formation* (which is bottom-up, behavioral, and cumulative) from pattern *enforcement* (which is top-down and procedural). Pattern formation via imitation is the cheaper and more durable path; pattern enforcement is sometimes necessary but expensive and brittle.

## Why This Methodology

### The Architect's May 15, 2026 observation

When Architect proposed Pattern-070 (Cleanup-Job-with-Cancellation-Hygiene), the proposal cited three instances — #1018 `EthicsAuditCleanupJob` (May 2), #1035 `CompostingSchedulerJob` (May 3), #1052 `StandupConversationManager` (May 5) — that converged on the same operational shape without explicit "use this pattern" guidance. Architect's framing:

> *"That's pattern formation via successful imitation, not pattern enforcement. Worth memorializing because future surfaces will face the same problem-shape and the pattern saves design-debate time."*

This entry codifies the framing. The discipline is **the discipline that produces patterns**, distinct from the discipline that *applies* patterns once filed.

### The two-mode contrast

| Mode | Enforcement | Imitation |
|---|---|---|
| Direction | Top-down (catalog → applications) | Bottom-up (applications → catalog) |
| Cost | Requires authoring + review + enforcement infrastructure | Requires only clean reference implementations |
| Brittleness | High when surfaces diverge from the spec | Low — the surfaces themselves carry the pattern |
| Filing timing | Pre-application (file pattern, then apply) | Post-recognition (file pattern after the third instance) |
| Reference shape | Pattern doc as the load-bearing artifact | Reference implementation as the load-bearing artifact; pattern doc as the legibility artifact |

The two modes are complementary at the catalog level — some patterns originate top-down (a design discipline named before any instance applies it) and some originate bottom-up (a shape emerges from successful imitation, and the pattern doc preserves the shape). Pattern-070 is bottom-up; Pattern-067/068/069 are mixed (the failure modes were pre-named, but each filing was motivated by a concrete vivid instance).

## When to apply this framing

### Apply this framing when

- Authoring a clean reference implementation that future surfaces may reach for. The cost-benefit of doing the implementation *well* compounds when imitation actually happens; sloppy reference implementations are not reusable, regardless of the design discipline involved.
- Reviewing whether a candidate pattern is real: count the independent instances. Three independent surfaces converging on the same shape without enforcement is the empirical signal that the pattern is durable.
- Filing a new architecture pattern: prefer to wait until three instances exist (bottom-up) over filing speculatively (top-down) when the pattern has a "you'll know it when you see it" character.
- Designing methodology rollouts: a memory pin with concrete trigger words plus a specific failure mode tends to do the binding work faster than a canonical methodology entry. Choose the lightest artifact that does the work.

### This framing does not apply when

- The pattern is genuinely novel and has no instance yet (must be top-down by definition)
- The pattern is safety-critical or compliance-driven (enforcement is the appropriate mode regardless of cost)
- The candidate pattern has only one or two instances (insufficient evidence for "durable shape"; risk of pattern-bloat)

## What it predicts

If pattern formation via imitation is genuine, the following downstream signals should appear:

- **Cross-role pattern citations within days of filing** (cohort vocabulary stabilizes faster than the pattern doc is read end-to-end)
- **Slot-allocation discipline adopted pre-codification** when the failure mode is vivid (the May 11 Pattern-067 collision → Architect's May 15 slot-availability check before Pattern-070 filing → methodology-28 codification today)
- **Memory pins observed in first downstream applications** within days of pinning (Lead Dev's May 13 close-issue-properly memory pin → Lead Dev's May 14 clean closure application; Docs's May 12 diff-HEAD memory pin → Lead Dev's May 14 retroactive flag)
- **Lower friction at the next pattern's emergence** because the cohort's pattern-recognition reflexes are calibrated

All four signals have been observed in PM during May 2026.

## Cross-references

- **Pattern-070 (Cleanup-Job-with-Cancellation-Hygiene)**: the architecture pattern this methodology entry was named alongside; Architect-authored, CIO co-signing this sidecar; Proven-promotion criterion is the fourth-instance (Anthropic Dreams Type 1 consolidation job) landing without re-discovery
- **methodology-28 (Pre-Filing Slot-Availability Check)**: companion methodology entry filed same session; demonstrates the adoption-before-codification pattern this entry predicts
- **Methodology-23 (close-issue-properly skill)**: first-observed-clean-application after Lead Dev's May 13 memory pin
- **`feedback_close_issue_properly_skill_recurring_miss` memory** (Lead Dev May 13): first observed downstream application May 14
- **`feedback_diff_head_before_editing_shared_file` memory** (Docs May 12): first observed downstream application May 14
- **Architect's Pattern-070 proposal memo** (`mailboxes/cio/read/memo-arch-to-cio-cc-lead-ceo-exec-cleanup-job-pattern-candidate-2026-05-15.md`): the proposal that named this methodology candidate

## Notes on this entry's authority + scope

Filed by CIO under self-approval per `methodology-audit-policy-updates-2026-03-16.md` as the sidecar artifact accompanying Pattern-070. The methodology framing is general (not Pattern-070-specific); the entry stands as canonical for any future pattern formed via successful imitation.

This entry does not attempt to specify *when* a candidate pattern has accumulated enough instances to warrant filing — that judgment is pattern-author lane (CIO for cross-cutting patterns, Architect for architecture patterns, etc.). The "three instances" heuristic is a starting calibration, not a rule.

---

*Filed: 2026-05-15 by CIO. Pattern category: methodology-corpus observation about pattern lifecycle. Authority: CIO self-approval per `methodology-audit-policy-updates-2026-03-16.md`. Slot allocation: methodology-29 next-available; pre-filing slot-availability check applied (methodology-28 discipline).*
