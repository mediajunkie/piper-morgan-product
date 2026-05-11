# Pattern-069: Coarse Triggers Causing False-Positive Triage Cost

## Status

**Emerging** — Filed 2026-05-11 by CIO under self-approval authority per `methodology-audit-policy-updates-2026-03-16.md`, with PM directive to close the loop on the May 10 disposition (elevate from "tactical observation" to formal Emerging). **Slot renumber 068→069 same session** as cascade from Pattern-068 (Silent State Mutation) renumber per Lead Dev + Architect coordination — see Pattern-068's Status note for full slot-conflict-resolution context. Surfaced by Code agent's May 10 PreCompact-hook second-incident addendum; HOST May 10 concurred on naming, deferred proto-pattern-vs-tactical-observation call to CIO. Promotion to Proven contingent on cross-mechanism recurrence — a different hook (or similar discipline mechanism) producing the same shape — within the next two weeks. PreCompact-hook-only recurrence does not promote (would be evidence about the one hook, not about the pattern class).

## Product Relevance

**Process-only** — Discipline-mechanism design property. Piper's users will not encounter this; teams building agent-coordination infrastructure with automated guards (hooks, gates, validators) will.

## Context

When a discipline mechanism — a hook, a gate, an alert, a validator — fires correctly by its own internal logic but the actual stakes of the situation it detected are low, the cumulative triage cost (human attention or PM-helper sessions burned verifying the alert) compounds faster than the mechanism's load-bearing-catch benefit. The failure is not in *what* the mechanism detects; it is in *how it weights what it detects*.

This pattern is **distinct from** the triggering-failure-mode patterns (062 family, 045, 046, 047, etc.), which name failures the mechanism is designed to catch. Pattern-069 names a failure of the mechanism's *design* — specifically, the absence of severity tiering or context-sensitivity in what would otherwise be a working detector.

## Problem

### The Failure Mode

```
Discipline mechanism M is designed to detect condition C
M is calibrated to fire whenever C is present
C has a wide variance in actual stakes (sometimes high, sometimes near-zero)

Scenario A (load-bearing): C is present, stakes are real → M fires correctly → triage produces value
Scenario B (false-positive): C is present, stakes are near-zero → M fires correctly → triage produces no value, but costs the same attention

Over time: B incidents outnumber A incidents
Cumulative triage cost > cumulative caught-real-problem benefit
Net effect: M is now a tax on the cohort, not a guardrail
```

The mechanism's verdict is correct each time — that's what makes the failure subtle. M doesn't have bugs; M doesn't fire spuriously; M's logic doesn't drift. The failure is that the calibration was set at "detect the condition" without an additional layer of "weight the condition by stakes."

### Why It Happens

1. **Detection is easier to design than decision support.** Binary "does the condition apply: yes/no" is straightforward. Tiered "given the condition, what's the appropriate action and severity" requires modeling the stakes-variance distribution, which often isn't available until after the mechanism has been deployed and observed.

2. **First-incident validation creates anchoring.** When M's first fire catches a real problem (as PreCompact hook did on Docs's stranded log May 9), the mechanism's correctness gets validated against high-stakes evidence. Subsequent fires are interpreted through that anchor; the cost-curve drift isn't visible until enough false-positives accumulate.

3. **No standing review of mechanism cost-curves.** Most disciplines have a "this mechanism caught a real problem" feedback loop but no "this mechanism is costing more than it saves" feedback loop. The first is celebrated (visible in retros, narratives); the second is invisible until someone names it.

### Concrete Example: PreCompact Hook (May 9–10, 2026)

PreCompact hook deployed May 9 (Lead Dev) — fires on uncommitted changes before `/compact`, blocks with options.

**Fire #1 (May 9 evening, Docs session)**: Load-bearing catch. Docs had stranded session log + Janus memo in working tree; session was about to compact; uncommitted work was at real risk of session-end loss. Triage produced the cross-agent residue accumulation pattern candidate. *Value > cost.*

**Fire #2 (May 10, PPM session ~3h later)**: False-positive triage. PPM session was local CLI (files on disk, will survive compaction); 6 uncommitted files were 4 MANIFEST regen + 2 PPM-owned drafts; no actual loss risk. Triggered ~30 min PM-helper session detective work to verify. *Cost > value.*

Two fires, one day, opposite cost-benefit math. The hook's logic was correct both times; the *weighting* was identical despite stakes being radically different. The Code agent author's proposed refinements (locality differentiation; severity tiering; "safe to compact" explicit option) move the hook from pure detection toward decision support without rolling back the load-bearing fire-#1 catch.

## Solution

### At the methodology layer

**1. Distinguish detection from decision support at mechanism design time.** When proposing a new hook/gate/alert, name explicitly which stance is intended. Detection mechanisms have predictable behavior (good for trust) but treat every instance with equal weight (bad for attention budget). Decision-support mechanisms tier severity to stakes, preserving trust while respecting attention.

**2. Build cost-curve feedback into mechanism rollout.** A new discipline mechanism should have a planned ~5-fire (or ~30-day) review checkpoint: did the fires produce value at a cost the cohort tolerated? If false-positive-to-load-bearing ratio exceeds ~2:1 at the checkpoint, refine the trigger criterion before the mechanism becomes a tax.

**3. Reserve "tiered severity" as a refinement path, not a v1 requirement.** Most mechanisms can start as detection-only; severity tiering is added after observation reveals the stakes-variance distribution. The May 9 PreCompact-hook v1 was correct to ship as detection-only; the May 10 second-incident is the signal that refinement is warranted.

### At the tooling layer (PreCompact hook specifically)

Routed to Docs per HOST's May 10 framing (Docs owns the hook script). Refinement options ranked by leverage:

1. **Locality differentiation** (highest-leverage): hard warning for remote/sandboxed sessions (real loss risk); soft reminder for local CLI sessions (rediscovery cost, not loss).
2. **Explicit "safe to compact" path** (documentation-only): add a fourth pick-one option for users whose situation is benign.
3. **Severity reduction for known-safe patterns**: MANIFEST regen, `.DS_Store`, gitignore noise as "tidy-but-not-critical" rather than "substantive-and-stranded."

## Anti-Pattern Indicators

The following signals suggest Pattern-069 may be present:

- **The mechanism fires more often than the cohort acts on it productively.**
- **Triage of mechanism fires has become a routine task absorbed by a small number of "fixer" sessions.**
- **The first fire produced clear value; subsequent fires increasingly produce uncertainty about whether action is warranted.**
- **The mechanism's warning text is generic; users repeatedly add context to interpret it.**
- **Cohort members start ignoring or routing-around the mechanism rather than acting on it.**

The last is the strongest late-stage signal: when a mechanism's fires are increasingly ignored, the cost-curve has already inverted; the mechanism is no longer functioning as a guardrail.

## Cross-References

- **Pattern-068 (Silent State Mutation in Shared Working Tree)**: companion pattern filed same session — Pattern-068 names the *failure modes* mechanisms like PreCompact-hook are designed to catch; Pattern-069 names the *design property* such mechanisms can fall into. The two patterns operate at different altitudes on the same problem space.
- **Pattern-049 (Audit Cascade)**: related but distinct — Audit Cascade is a methodology pattern for multi-layer pre-execution gates; Pattern-069 names a failure mode that any single audit/gate can develop if its severity isn't tiered.

## References

- Code agent May 10 PreCompact-hook second-incident addendum (`mailboxes/cio/read/memo-code-to-docs-cc-cio-host-pa-precompact-hook-second-incident-addendum-2026-05-10.md`): originating proposal + cohort §-routing including CIO § flagging meta-pattern naming opportunity
- HOST May 10 detection-vs-decision-support memo (`mailboxes/cio/read/memo-host-to-docs-precompact-hook-detection-vs-decision-support-2026-05-10.md`): methodology stance concurrence + CIO-call deferral on proto-pattern vs. tactical-observation
- CIO May 10 disposition memo (`mailboxes/cio/sent/memo-cio-to-code-host-docs-cc-pa-ceo-pattern-candidates-disposition-2026-05-10.md`): Innovation Backlog Operational #45 capture; initial "hold for one more incident" disposition
- PM May 11 directive ("close the loop"): elevation from tactical observation to Emerging filing

---

*Formalized: 2026-05-11 by CIO. PM ratification on May 11 same-day directive. Promotion to Proven contingent on cross-mechanism recurrence within two weeks.*
