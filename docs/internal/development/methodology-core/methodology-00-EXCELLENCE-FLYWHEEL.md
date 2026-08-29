# The Excellence Flywheel — Methodology-00

**Status**: v2.0 — Three-layer reformulation (Apr 26, 2026)
**Reformulation source**: CIO Apr 16, 2026 memo (`mailboxes/docs/read/memo-cio-flywheel-audit-2026-04-16.md`) + M1 methodology audit; ratified for canonical adoption.
**Predecessor**: v1.0 "Four Pillars" formulation (active July 2025 → Apr 2026). v1 lives on as a historical reference; this document supersedes it.

> **For agents at session start**: The Flywheel concept is *why* the operational principles in `CLAUDE.md` work together. The principles ("Verify First, Create Second," "Evidence Required," "Completion Discipline") are what you act on. This document explains the model behind them. You don't need to cite the Flywheel by name to follow the principles — but understanding the layers below helps when you're deciding how to apply a principle to a novel situation.

---

## Three Layers

The Flywheel is a single idea presented at three levels of abstraction. Drift happens when agents encounter a mnemonic, can't find the practice it derives from, and invent a plausible-sounding middle layer. The fix is structural: keep the derivation chain visible.

```
Concept (the why)        — the causal loop. Stable. Doesn't change.
   ↓
Practice (the what)      — enumerable, versioned, evolves with the project.
   ↓
Mnemonic (the how-to-remember) — role-adapted recall aids. Different across roles is fine.
```

---

## Layer 1: Concept (The Causal Loop)

**Quality compounds into velocity, which enables higher quality.**

Foundation work pays compound returns. Systematic preparation makes execution faster. Faster execution leaves time for higher-quality preparation. The cycle reinforces itself.

When we say "the flywheel is spinning," we mean this loop is operating: systematic preparation → faster execution → higher quality → better preparation.

When we say "the flywheel stalled," we mean a layer broke down — usually the practice layer (a non-negotiable practice got skipped) or the mnemonic layer (a role started reciting principles without applying them).

This concept is stable. The original July 2025 formulation got it right. It hasn't been amended.

---

## Layer 2: Practice (Five Practices)

These are the specific behaviors that instantiate the cycle in our project context. They are enumerable. They will evolve as the project evolves. The current five practices reflect operational reality through M0–M1 (closed Apr 11, 2026).

### 1. Verify Before Building

Check what exists before creating. Most code is 75% complete then abandoned. Most patterns are already partially implemented somewhere.

```bash
# Examples (adapt to your search tool):
find . -name "*.py" | grep [feature]   # Find existing patterns
grep -r "pattern" services/             # Check implementations
cat services/domain/models.py           # Verify domain models
```

The verification step is cheap. The cost of duplicating or contradicting existing work is high.

### 2. Test What Matters, Not What's Easy

Write tests that verify user-visible behavior, not just code paths.

- TDD remains: write the test first, watch it fail, implement minimum, verify success.
- The M1 lesson: mocked unit tests are necessary but insufficient. Tests that pass against mocks while production fails real users are Pattern-045 (Completion Theater).
- The Colleague Test (`docs/internal/testing/colleague-test-rubric.md` v2.1) and fresh-account UAT are now part of "testing" alongside pytest. Different layers catch different failure modes.

### 3. Coordinate Through Structure

Multi-agent work requires durable coordination surfaces, not synchronous channels.

- **Mailboxes** at `mailboxes/[role]/{inbox,sent,read}/` are how roles deliver work to each other.
- **Session logs** at `dev/YYYY/MM/DD/` are institutional memory.
- **Handoff memos** preserve context across role transitions and instance retirements.
- **Omnibus logs** at `docs/omnibus-logs/` aggregate cross-role activity per day.

"Never work alone" doesn't mean synchronous collaboration. It means leaving artifacts other agents can pick up.

### 4. Track to Completion with Evidence

Every claim needs proof. "Done" means user-can-use-it, with verification documented.

- Create the GitHub issue **before** starting.
- Close with evidence: tests added/modified, verification command output, files modified, user-verification steps.
- Update the issue description (not just comments) so closure leaves a complete record.
- The Inchworm: each milestone closure positions the next milestone's start.

### 5. Audit the Composition (Pattern-062)

**Added to the Flywheel from M0–M1 experience.** The Assembly Assumption taught us that individually correct components don't guarantee correct composition. Wiring passes, gate verification, and integration audits catch what unit tests can't.

- Pattern-062 (Assembly Assumption): when each piece works in isolation but the whole behaves wrongly, the failure is at the seams.
- Wiring passes: explicit verification that components are connected as designed (intent service → handler dispatch → response composition).
- Gate verification: methodology gates (M1 UAT, sub-epic gates) test the whole, not the parts.
- Recent example: #1002 floor-bypass-by-pre-classifier (Apr 25). Phases A–D of #992 each shipped correctly; the bypass lives at the seam between pre-classifier and ethics floor. Audit the composition would have caught the dispatch order before activation.

---

## Layer 3: Mnemonic (Recall Aids)

Compact verb lists for use at session start. These are role-adapted derivatives of the Practice layer. Different roles emphasize different practices, so different mnemonics are acceptable as long as each verb traces back to a Practice and the Practice traces back to the Concept.

**Default agent mnemonic**: Verify → Test → Coordinate → Track → Audit

**Role variants** (illustrative, not normative):

- **Lead Developer**: Verify → Test → Track → Audit (coordination is implicit in mailbox/session-log discipline)
- **PPM**: Verify → Synthesize → Decide → Document (verification + tracking layered into product workflow; auditing surfaces in workstream reviews)
- **CXO**: Score → Verify-source → Detect-drift → Document (verification-before-assertion is the dominant practice; "Score" = apply Colleague Test honestly)
- **Docs**: Verify (Step 7 in create-omnibus skill) → Synthesize → Cross-reference (Step 2.5 gate) → Surface

The mnemonic is **how to remember in the moment**, not how to demonstrate compliance. If a role has a different memory device that produces the same Practice-layer behavior, it's working.

**Drift signal**: if you find yourself using a verb you can't trace back to a Practice, the mnemonic layer has decoupled. Re-read this document.

---

## Daily Practice (Default Agent Loop)

1. **Verify** — what exists, what's been tried, what the canonical document says
2. **Test** — write the failing test (or score the response, or audit the artifact)
3. **Implement minimal** — the smallest change that turns the failing into passing
4. **Track with evidence** — issue updated, log entry made, mailbox routed
5. **Audit the composition** — does the new piece compose correctly with what already exists?

**Break this cycle = break the flywheel.** Each step is cheap individually; skipping steps creates compounding rework.

---

## What Changed in v2.0 (Reformulation Notes)

For agents who've been on the project a while, here's what's different from v1.0 (Four Pillars):

- **Four Pillars → Five Practices.** Pillar 5 ("Agent-Driven Development") in v1 overlapped heavily with Pillar 3 ("Multi-Agent Coordination"); both fold into Practice 3 ("Coordinate Through Structure"). The fifth Practice slot is now Pattern-062 / Audit the Composition — the lesson the M0–M1 period actually added.
- **Practice 2 ("Test What Matters") is broader than v1's "Test-Driven Development."** TDD remains the core, but the Colleague Test and fresh-account UAT join it. M1 gate methodology validated this expansion.
- **Three layers (Concept / Practice / Mnemonic) are now explicit.** v1 mixed them, which is what produced 8 different paraphrased formulations across 9 months. The three-layer structure makes the derivation chain visible so agents can check their citations against the canonical layer.
- **CLAUDE.md does not adopt the Flywheel label.** The operational principles in CLAUDE.md ("Verify First, Create Second," "Evidence Required," "Completion Discipline") stand on their own. Agents follow them; they don't need to cite the Flywheel to do so. The Flywheel concept lives here, in the methodology docs, where agents who want to understand *why* these principles work together can find it. This is deliberate: it prevents drift at the source by removing any pressure to recite the Flywheel from memory in operational contexts.

---

## References

- **Concept origin**: July 2025 (`docs/blog/whipping-ai-chaos-toward-quality-with-the-excellence-flywheel.md`)
- **CIO reformulation memo**: `mailboxes/docs/read/memo-cio-flywheel-audit-2026-04-16.md`
- **Flywheel archaeology** (8 formulations across 9 months): `dev/active/excellence-flywheel-archaeology-2026-04-16.md`
- **Pattern-062 (Assembly Assumption)**: `docs/internal/architecture/patterns/pattern-062-assembly-assumption.md`
- **Colleague Test (operational v2.1)**: `docs/internal/testing/colleague-test-rubric.md`
- **CLAUDE.md operational principles**: `CLAUDE.md` (root)
- **Methodology index**: `docs/internal/development/methodology-core/INDEX.md`

---

*Reformulated April 26, 2026, per CIO Apr 16 decisions. v1.0 (Four Pillars, July 2025 – Apr 2026) is superseded.*
