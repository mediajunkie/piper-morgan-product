# Methodology-00 v3.0 — the proposed Layer 2 replacement text (for PM ratification)

**Lead**: Arch · 2026-09-10 · This is the TEXT the seven decisions (as amended v3.0.1/v3.0.2)
resolve to. On PM's ratification: CIO applies it to `methodology-00-EXCELLENCE-FLYWHEEL.md` as
corpus steward (Layer 1 untouched; v2.0's Layer 2 + the version-notes section change; Layer 3
per-role mnemonics untouched per scope). **COMPLETE as of 09-10 morning**: both pointer slots
carry Docs' verified lists (delivered same-morning, re-verified against the live corpus), and
Docs' review also caught one slip — an m-49 fold that violated D5's own maturity gate — now
corrected and dated inline. No open slots; ready for ratification as-is.

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
the Layer-2 enforcement-column check below. Episodic audits (census, false-trails, noun audits)
remain available as dispatch tools; the cadence is what stops them being luck.
**See also**: m-23 (M1 Innovations — the wiring-pass origin v2.0's own changelog names), m-24 (Branch-or-Anchor — Pattern-062 lineage at the spec layer), m-37 (Coverage-Audit Gate — the per-PR "does this compose" mechanism) · m-45. *(Docs-verified 2026-09-10; m-24's tie is via Pattern-062 explicitly, not a literal Practice-5 citation.)*

---

## The review trigger (replaces v2.0's "will evolve as the project evolves")

**At each milestone close, the closing-gate issue carries two lines**: (1) the P5 composition
question above; (2) **check this layer's enforcement claims against reality** — one row per
practice: is the named enforcement still live, still behavioral, still true? v2.0 rotted because
its evolution clause was an intention with no condition; this trigger rides an event that
already cannot be skipped (PM-declared closing gates: #1165, #1297, #1386 precedent). First
instance: a checklist line on #1386 (MVP close, due 2026-10-30), cross-referenced with the
product-side gate per release-model.md.

## Q5 (PM's ruling slot — text ready for either answer)

Idle is a legitimate terminal state **when the role's consumed surfaces are drained** — a
role-scoped denominator (governance roles: mail + standing items; build-capable roles: those
plus the sprint backlog). Idle because the inbox is empty while an enumerated surface holds work
is not idle — it is a missing consumer. *(Awaits PM's ruling; HOST's sequencing note honored —
rule after the intake step has observed mileage.)*

---

## Version note for the doc's history section

v3.0 (2026-09): Layer 2 re-derived for autonomous agent-pull operation. Five practices retained
(none added, none removed); P3 rewritten bidirectional with m-53 sub-clause and its m-41
breakage acknowledged; P4 given three evidence sub-clauses (m-43/44/50); P5 given the
milestone-close cadence; layer redefined as index-with-teeth over the canonical corpus; maturity
gate + review trigger added. Process: Exec scope (PM-approved) → 7 independent reads → Arch
synthesis → challenge round (5 amendments, all accepted, incl. the enforcement column relabeled
per-artifact after its own labels outran their evidence) → PM ratification. Full record:
`dev/active/flywheel-v3-synthesis-2026-09-08.md` + the round's mail trail on origin/main.
