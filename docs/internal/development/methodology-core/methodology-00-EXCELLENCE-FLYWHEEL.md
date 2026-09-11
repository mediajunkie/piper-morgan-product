# The Excellence Flywheel — Methodology-00

**Status**: v3.0 — Layer 2 re-derived for autonomous agent-pull operation (Sept 11, 2026)
**v3.0 source**: PM-approved re-evaluation, triggered by PM naming "something has been lost despite this huge autonomy improvement" (Sept 8) — Exec scope → 7 independent reads → Arch synthesis → challenge round (5 amendments) → PM ratification Sept 11 ("The flywheel v3 layer 3 text looks good. I approve it" — referring to the Layer 2 replacement text; recorded as-stated per the ratifying memo). Full record: `dev/active/flywheel-v3-synthesis-2026-09-08.md`.
**Predecessor**: v2.0 — Three-layer reformulation (Apr 26, 2026), itself superseding v1.0 "Four Pillars" (July 2025 – Apr 2026). Layer 1 (Concept) and Layer 3 (Mnemonic) are unchanged in v3.0; only Layer 2 (Practice) and the review-trigger were in scope.

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

## Layer 2: Practice (Five Practices) — v3.0

These are the behaviors that instantiate the cycle under **autonomous, agent-pull operation**
(eleven agents waking on timers, selecting their own work). They are enumerable and they evolve;
v3.0 re-derives them from the autonomous period's operational evidence (June–September 2026).
**This layer is an index with teeth**: each practice states its claim, names its live
enforcement, and points into the methodology corpus for detail. **The corpus is canonical
detail; this layer is how you find it.**

**The maturity gate** (governs what this layer absorbs): canon absorbs entries that have
stopped moving, not entries that are new. An entry still shrinking under its own author's
scrutiny stays in the corpus catalog until it stabilizes.

### 1. Verify Before Building

Check what exists before creating. Most code is 75% complete then abandoned; most patterns are
already partially implemented; most "missing" documents exist under another number. This applies
to ALL work — code, issues, memos, specs, citations — and its autonomous-era form is sharpened
by m-52: **open the artifact; a summary (or your memory of one) is not its contents.**

**Enforced**: extraction/protocol ratchet tests (CI-behavioral) · supersession-gate standing ask
· CLAUDE.md §Verify-First (prose norm — Present, not machine-checked).
**See also**: m-07 (Verification-First — canonical for this principle), m-30 (Consumer-Trace-Verification, an m-07 specialization), m-42 (Reflexive Verification — the self-exemption failure mode), m-16 (Stop Conditions), m-14 (Documentation-Standards — this principle applied to docs). *(Docs-verified 2026-09-10.)*

### 2. Test What Matters, Not What's Easy

Write tests that verify user-visible behavior, not code paths. Mocked unit tests are necessary
and insufficient (Pattern-045); different layers catch different failure modes, and the Colleague
Test plus fresh-account UAT are part of "testing" alongside pytest. *(Content deliberately
unchanged from v2.0 — the one practice whose text stayed more current than its corpus.)*

**Enforced**: Colleague-Test rubric (PM-ratified invariants, DoD-gated) · canonical suite
(executed, context-requirement-tagged) · BYOC recomposition branch **Present — cannot yet issue
a pass** (T-axis pending probe; honesty per the v3.0.2 relabeling).

### 3. Coordinate Through Structure — **bidirectional** *(the v3.0 rewrite)*

Multi-agent work runs on durable coordination surfaces, in **both directions**:

- **Produce**: leave artifacts other agents can pick up — mailboxes, session logs, handoff
  memos, omnibus logs. "Never work alone" means durable artifacts, not synchronous channels.
- **Consume** *(the half v2.0 never wrote, and the 2026-09 intake gap was its cost)*: **read the
  shared work surfaces.** A role's available work is its enumerated consumed surfaces — inbox,
  standing items, and (for build-capable roles) the sprint backlog — each with a stated
  denominator, so a missing surface announces itself instead of hiding behind "no work."

**Sub-clause (m-53, chokepoint-vs-bolt-on)**: a coordination duty survives only where skipping
it visibly breaks work already in progress. A duty that can be skipped without visible cost will
decay regardless of how it is worded — position duties on rails that cannot be skipped, or
expect to rediscover their absence by incident.

**Honesty note carried in the text**: this practice **broke once** — under the matured duty
cycle, session logs accreted nothing for 6 of 9 cycling roles (m-41, discovered 2026-06); the
fix (single-log discipline) lives in CLAUDE.md. A practice that broke and was silently patched
elsewhere is worse than one that says so here.

**Enforced**: produce side — mail machinery, MANIFESTs, heartbeat/watchdog (observed daily) ·
consume side — duty-cycle-tick v1.32 intake step + the eligibility denominator (**Present — not
yet observed firing**; flips to Enforced on the first observed pull) · work-scoping boundary:
Product→Sprint promotion is permanently a human scope act.
**See also**: m-20 (omnibus), m-22 (roundtable), m-25 (workstream cadence), m-31 (append-only
cycle git architecture), m-41 (the breakage), m-53.

### 4. Track to Completion with Evidence

Every claim needs proof, and **the autonomous era redefines "proof"** — no human reviews every
claim, so evidence quality is load-bearing. Three named sub-clauses, each a specific failure
mode of unreviewed evidence:

- **Name the layer** (m-43): say what your check actually measured — a curl 200 is not a render
  test; a config file's presence is not a live hook.
- **State the denominator** (m-44): "all clear" and "4 of 10 clear" are different claims; every
  coverage statement names what it covered out of what exists.
- **A self-report is not evidence** (m-50): a compliance record counts only if machine-written
  at the moment of invocation — a hand-narrated claim, however honest, is testimony.

Create the issue before starting; close with evidence in the description; "Verified how:" is a
required field on completion claims — method, layer, denominator.

**Enforced**: "Verified how:" bounce-back norm (behaviorally observed — claims get bounced) ·
issue-closure protocol · provenance-tagged heartbeat markers (observed firing) · board-status
discipline.
**See also**: m-43, m-44, m-50 — and m-49/m-51/m-52 when they clear the maturity gate. *(Corrected 09-10: an earlier draft folded m-49 here, against D5's own ruling that m-49/51/52 wait — Docs caught the slip without even re-litigating it.)*

### 5. Audit the Composition (Pattern-062)

Individually correct components don't guarantee correct composition — when each piece works in
isolation and the whole behaves wrongly, the failure is at the seams. The autonomous era added
the social seam: independent agents sharing a procedural confound compose into false
corroboration (m-45), and per-site fixes compose into un-modeled-noun recurrence (the 2026-09
audit).

**Enforced** *(v3.0: this practice takes D7's cadence — it is no longer episodic-by-luck)*: the
composition question — "does this milestone's work compose, and what got fixed per-site that
should have been fixed per-class?" — **is a named line on every milestone-close gate**, alongside
this layer's own enforcement-column check. Episodic audits (census, false-trails, noun audits)
remain available as dispatch tools; the cadence is what stops them being luck.
**See also**: m-23 (M1 Innovations — the wiring-pass origin v2.0's own changelog names), m-24 (Branch-or-Anchor — Pattern-062 lineage at the spec layer), m-37 (Coverage-Audit Gate — the per-PR "does this compose" mechanism) · m-45. *(Docs-verified 2026-09-10; m-24's tie is via Pattern-062 explicitly, not a literal Practice-5 citation.)*

---

## The review trigger (replaces v2.0's "will evolve as the project evolves")

**At each milestone close, the closing-gate issue carries two lines**: (1) the Practice-5
composition question above; (2) **check this layer's enforcement claims against reality** — one
row per practice: is the named enforcement still live, still behavioral, still true? v2.0 rotted
because its evolution clause was an intention with no condition; this trigger rides an event that
already cannot be skipped (PM-declared closing gates: #1165, #1297, #1386 precedent). First
instance: a checklist line on #1386 (MVP close, due 2026-10-30), cross-referenced with the
product-side gate per release-model.md.

## Q5 (PM's ruling slot — text ready for either answer)

Idle is a legitimate terminal state **when the role's consumed surfaces are drained** — a
role-scoped denominator (governance roles: mail + standing items; build-capable roles: those
plus the sprint backlog). Idle because the inbox is empty while an enumerated surface holds work
is not idle — it is a missing consumer. *(Awaits PM's ruling; HOST's sequencing note honored —
rule after the intake step has observed mileage. Note, 2026-09-11: PM's separate same-morning
work-queue ruling — carried work + mail + newly-observed GitHub issues, idle only when all three
are empty — likely resolves this in substance, but per Exec's explicit caution this text is left
as ratified rather than pre-empting Arch's read of the connection.)*

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

## What Changed in v3.0 (Sept 11, 2026)

Layer 2 re-derived for autonomous agent-pull operation (eleven agents waking on timers,
selecting their own work — a mode of operation v2.0 predates entirely). Five practices retained
(none added, none removed): Practice 3 rewritten bidirectional with the m-53 (chokepoint-vs-
bolt-on) sub-clause and its own m-41 breakage acknowledged in the text rather than hidden;
Practice 4 given three named evidence sub-clauses (m-43/44/50); Practice 5 given the
milestone-close cadence (D7) rather than remaining episodic-by-luck. The layer is now framed
explicitly as an index with teeth — each practice states its live enforcement and points into
the methodology corpus for detail, rather than being the detail itself. The maturity gate
(canon absorbs entries that have stopped moving, not entries that are new) and the review
trigger (replacing v2.0's un-conditioned "will evolve as the project evolves") are both new.
Process: Exec scope (PM-approved) → 7 independent reads → Arch synthesis → challenge round (5
amendments, all accepted, including the enforcement column being relabeled per-artifact after
its own labels outran their evidence) → PM ratification.

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
- **v3.0 synthesis record**: `dev/active/flywheel-v3-synthesis-2026-09-08.md` (kickoff, 7 reads, challenge round) + `dev/active/flywheel-v3-layer2-text-2026-09-10.md` (ratified text, this document's source)

---

*v3.0 applied September 11, 2026, per PM ratification. v2.0 (Apr 26, 2026 – Sept 11, 2026) and v1.0 (Four Pillars, July 2025 – Apr 2026) are both superseded; this document is the sole canonical current version.*
