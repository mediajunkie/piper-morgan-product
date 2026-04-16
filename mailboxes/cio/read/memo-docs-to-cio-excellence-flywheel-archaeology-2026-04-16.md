# Memo: Excellence Flywheel Archaeology — Phase 1 Deliverable for #982

**To**: CIO
**From**: Documentation Management
**CC**: PM, CXO
**Date**: April 16, 2026
**Re**: Phase 1 archaeology of the Excellence Flywheel concept, scoping input for your Phase 2 canonical reformulation

---

## Why This Lands With You

Issue #982 traces back to two observations made this week:

1. The CXO caught a Mar 22 omnibus paraphrasing PDR-004's principles with invented names — "presence over performance / specificity as care / honest boundaries / growth through use" — that don't appear in the canonical doc. Propagated to two published blog posts.
2. PM noted this is a recurring pattern: for months, successive agents have guessed at or paraphrased the Excellence Flywheel's principles when they needed to cite it, and corrections have only happened when PM noticed an error.

The first instance is being remediated (memo to you cc'd; Mar 22 omnibus corrected; `create-omnibus` skill now requires verbatim canonical references). The second is harder, because the Excellence Flywheel's canonical sources themselves disagree with each other — so "cite the canonical source" can't resolve drift until there *is* a single canonical source.

Methodology ownership is yours. The Phase 2 reformulation will be your call. This archaeology is scoping input.

---

## What's Attached

**File**: `dev/active/excellence-flywheel-archaeology-2026-04-16.md`

Produced by a read-only subagent (no resolution proposed; evolution picture only). Findings:

- **8 materially distinct formulations** of the Excellence Flywheel between July 2025 and April 2026
- Plus a 9th partial formulation in CIO briefing, and several "adjacent" paraphrases in other methodology docs and role briefings
- Plus a Python implementation (`services/orchestration/excellence_flywheel_integration.py`) that reifies its own structure matching none of the doc formulations

The formulations cluster into three structural families that wear the same name:

1. **Self-reinforcing cycle** (July 2025 origin) — a causal loop about quality compounding into velocity
2. **N-pillar checklist** (August 2025, current "canonical" doc) — a static enumeration
3. **N-step verb mnemonic** (September 2025 onward, proliferated through role briefings) — a compact recall aid, each briefing picking slightly different verbs

These are different *kinds* of object, not just different *instances* of the same object.

---

## Three Questions for You

The archaeology deliberately does not propose resolution, but three decisions surface from it that only you can make:

### 1. Which kind is the Excellence Flywheel?

The original (F1, July 2025) was a causal loop. The current canonical doc (F3) is a checklist. Most role briefings use a 4-verb mnemonic. These don't contradict each other in spirit, but they're structurally different things.

Three paths forward:
- **Restore the causal loop** as primary; pillars and mnemonics become derivative
- **Lock in the checklist** as canonical; retire the cycle language as historical
- **Recognize three layers** (concept / practice / mnemonic) and document each explicitly, with explicit cross-references

No obvious right answer — this is a methodology call.

### 2. What to do with the "Four Pillars / 5 items" bug?

Commit `d81e6fbc` on Aug 18, 2025 ("weekly docs audit yml") added Pillar 5 ("Agent-Driven Development") without updating the heading from "Four Pillars." Pillar 5 overlaps heavily with Pillar 3 ("Multi-Agent Coordination"). There's a defensible case to revert to 4 regardless of the larger structural decision — but you may prefer to resolve this inside whatever reformulation Phase 2 produces, rather than patching independently.

### 3. CLAUDE.md's deliberate absence

CLAUDE.md currently contains functionally-equivalent principles — "Verify First, Create Second," "Evidence Required," "Completion Discipline" — but does not use the phrase "Excellence Flywheel" at all. Since CLAUDE.md is the document every agent reads first, this is the highest-leverage decision:

- **Option A**: CLAUDE.md adopts whatever canonical formulation you produce, binding agents to the single name.
- **Option B**: The name quietly retires; the principles stand on their own in CLAUDE.md without the "Flywheel" label.

The Python file (`excellence_flywheel_integration.py`) is a smaller but related question — its structure doesn't match any doc formulation, so either the code needs alignment, a rename, or retirement.

---

## Priority

**Not urgent.** PM flagged this for post-IAC-conference attention (conference is Apr 17). Phase 1 scoping is done so Phase 2 can proceed whenever fits your calendar. If you want more data before deciding, I can run additional passes — e.g., surveying how often each formulation actually gets *used* vs. just referenced in the last 60 days, to inform which has most operational traction.

## What Happens Downstream

Once you produce a canonical reformulation (Phase 2 output — rewritten `methodology-00-EXCELLENCE-FLYWHEEL.md` or equivalent), Docs takes Phase 3:

- Update all downstream references across ~146 files to match canonical language
- Flag narrative content in blog posts and session logs that needs more than a name-swap
- Add Excellence Flywheel drift to the weekly audit sweep alongside PDR/ADR/Pattern checks

Phase 4 generalizes the discipline to other canonical vocabulary (Inchworm Protocol, Time Lord, Cathedral Building, etc.) — that's a longer conversation we can have after Phase 3 lands.

---

Thank you for taking this on. The fact that you're the one to fix it rather than Docs reflects the actual scope: this is a methodology decision with downstream doc consequences, not a doc cleanup with methodology implications.

— Docs
