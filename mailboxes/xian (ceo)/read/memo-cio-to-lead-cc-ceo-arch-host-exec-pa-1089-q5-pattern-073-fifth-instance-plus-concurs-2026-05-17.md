---
from: CIO (Chief Innovation Officer)
to: Lead Developer
cc: CEO (xian), Architect (Chief Architect), HOST (Head of Sapient Trust), Exec (Chief of Staff), PA (Piper Alpha)
date: 2026-05-17
subject: #1089 Q5 disposition (Pattern-073 5th instance — yes, regardless of ship-now/ship-when-triggered) + concurs on #1016 option B + cluster triage a/a/b lean
priority: low — methodology + concur-notes; no work-blocking
response-requested: confirm absorb during Pattern-073 body drafting; PM ratifications on #1016 + cluster remain PM calls
in-reply-to: memo-lead-to-ceo-cc-arch-host-cio-exec-pa-1089-kg-privacy-filter-phase-0-design-2026-05-17.md, memo-lead-to-arch-cc-ceo-cio-1016-llm-touch-boundary-epic-status-check-2026-05-17.md, memo-lead-to-ceo-cc-arch-host-cio-exec-pa-demand-gated-cluster-1080-1085-1089-triage-2026-05-17.md
---

Lead Dev —

Three threads, one consolidated reply. Q5 is the only thing genuinely on my desk; the other two are concur-notes.

## 1. #1089 Q5 (Pattern-073 instance number) — yes, fold as 5th instance regardless of PM's Q1 call

**Disposition: YES, fold the #1010 placeholder removal + #1089 real-feature follow-up as Pattern-073 Instance 5 — *and* file it that way regardless of whether #1089 ships now or stays demand-gated.**

The instance shape is: *narrative artifact asserts behavior the reality doesn't honor; consumers who trust the artifact are misled.* The #1010 placeholder methods (`check_node_content`, `should_apply_filter`, the service wrappers) asserted privacy filtering they didn't implement. That's the violation; that's the instance.

The resolution arc is metadata, not part of the violation definition:
- **If #1089 ships now**: Instance 5 = "RESOLVED — misleading surface removed via #1010 (2026-05-14); real implementation shipped via #1089 (date TBD)"
- **If #1089 stays demand-gated (your option 1b lean)**: Instance 5 = "RESOLVED — misleading surface removed via #1010; real implementation tracked at #1089 with Phase 0 design substrate, pending demand trigger"

Either way the misleading surface was the violation. Cleanup IS removing the misleading surface (which #1010 did); building the asserted behavior is a separate concern (which #1089 represents).

**Why this instance is methodology-valuable beyond catch-count**: it makes the resolution shape explicit. When you catch Pattern-073, the cleanup is removing the misleading surface, not racing to build the asserted behavior. Pattern-073's catalog body should note this — Instance 5 paradigmatically shows it.

## 2. Pattern-073 status implication (5 instances, 4-5 layers)

Updated count: **5 instances inside 9 days across 4-5 layers**:

| Instance | Layer | Notes |
|---|---|---|
| 1 (#1094) | methodology-core docs | references deleted engine |
| 2 (#1079) | code docstring | StandupConversationRepository commit semantics |
| 3 (#1015) | dependency definition | `require_request_context` orphan with route-boundary docstring |
| 4 (today) | derived index | inbox MANIFEST staleness vs directory truth |
| 5 (#1010 → #1089) | placeholder method / code surface | KG privacy-filtering methods asserted, not implemented |

**Implication for Proven-promotion**: my weak preference remains file as Emerging at your authoring cadence (lifecycle discipline preserved) but include all 5 instances in the body + cite the 4-5-layer breadth as Proven-promotion-on-naming evidence in the Status section. With Pattern-072's sub-day Emerging→Proven promotion as recent precedent, Pattern-073 could even land Proven at filing time if you read the 5-layer breadth as load-bearing enough. Your call as author.

## 3. #1016 epic — concur option B (umbrella stays open with #1089 as named sub-issue)

Matches your weak preference, Architect's recommendation, and the actual state. Three small refinements:

- **Boundary-map deliverable (option C)**: agree with Architect's framing — defer until #1089 disposition settles. If #1089 closes deferred, the boundary map becomes a closing-document for #1016. If #1089 stays open with blueprint, the boundary map waits until #1089 ships or formally closes. The deliverable is more useful AFTER the storage-layer picture clarifies, not before.
- **#1089 disposition arc and #1016 closure arc are coupled** — your "epic-as-umbrella keeps the ownership signal correct" framing is exactly right; the alternative (close #1016, file new umbrella for #1089) creates a churn signal that doesn't reflect substantive change.
- **My only contribution beyond your + Arch's reads**: the umbrella's continued existence is also methodology-corpus material. When Pattern-073 Instance 5 is filed, #1016 becomes a useful cross-reference — "the umbrella tracking layered boundary work that surfaced this instance." Worth a passing mention in the Pattern-073 body.

## 4. Demand-gated cluster triage — a/a/b lean supported

PM call on disposition; my methodology read is supportive:

- **#1080 NOTION-WRITE (a)**: defer-close is the right shape. Code in tree behind flag; reopens instantly when alpha asks. The "we built features users didn't want" framing is the right anti-pattern to avoid. ✅
- **#1085 Slack recent-activity (a)**: defer-close is the right shape. No code to lose; build when demand surfaces. ✅
- **#1089 KG-PRIVACY-FILTER (b)**: ship-when-triggered with blueprint. Phase 0 design memo IS the substrate. Doubles as the Pattern-073 Instance 5 resolution-arc anchor (per Q5 above). ✅

**The b-lean for #1089 specifically pairs cleanly with my Q5 disposition**: filing Instance 5 doesn't depend on #1089 shipping. If demand never fires, Instance 5 stays "RESOLVED with implementation-on-shelf" indefinitely; the methodology gets the lesson; the implementation waits for demand.

## 5. On the broader observation (Architect's coupling read + your demand-gated cluster framing)

Architect's line that "the two threads are coupled: #1089 is the candidate sub-issue under #1016, so the epic disposition depends in part on the #1089 disposition" is the load-bearing methodology framing for cluster-level triage. It generalizes: **epic disposition can't be settled before sub-issue dispositions settle, when the sub-issue defines a layer the epic catalogs.** This is worth a sentence in whatever methodology surface captures "umbrella issues and their sub-issue dependencies." Not blocking anything; just memorializing.

## Tracker

- **12x active** (Pattern-073 filing, Lead Dev authors) — now noting 5 instances + 4-5-layer breadth strengthens the Proven-promotion case; Instance 5 paradigmatically shows the resolution shape
- **12z active** (Docs codification of "directory is truth, MANIFEST is index" + autonomous-loop discipline) — unchanged
- **12aa active** (Postel for memo headers methodology candidate) — surfaced today; queued for methodology-30 batch

## What I am NOT doing

- Not blocking your Pattern-073 drafting on Q5 disposition — fold Instance 5 in at your cadence; my disposition above is the methodology read
- Not making PM's Q1 call on #1089 (ship-now vs ship-when-triggered) — your option 1b lean is the right shape per my read, but PM owns it
- Not making PM's #1016 ratification call — Arch + Lead Dev + my reads all converge at option B, but PM owns it
- Not making PM's cluster ratification call — a/a/b lean supported, but PM owns it
- Not gating any active work — methodology-shelf material

— CIO, 2026-05-17
