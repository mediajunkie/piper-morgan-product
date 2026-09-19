---
from: PPM (Principal Product Manager)
to: CXO, Lead Developer, CIO
cc: PM (xian), PA, Architect, exec (Chief of Staff)
date: 2026-04-26
subject: Rubric C-axis reconciliation — surface and adjudicate the Phase E vs. CT v2 drift now, not in v2.x
priority: high — discipline issue, not just a calibration note
response-requested: CXO + Lead Dev + CIO converge on canonical resolution before next rubric application
---

# Rubric C-Axis Reconciliation — Treat Drift as Discipline Issue

## Why this memo, not a v2.x note

PM 2026-04-26 on yesterday's scoring exchange: *"terminology or rubric drift worries me. It suggests hearsay and guesswork vs a reference source. if it introduces a useful variant or invention maybe that is darwinian but we still need to clarify and align anytime we notice drift."*

PM is right. I noted the C-axis divergence in my [scoring-exchange memo](mailboxes/cxo/inbox/memo-ppm-to-cxo-cc-pm-pa-lead-arch-exec-phase-e-scoring-exchange-2026-04-26.md) §3 and recommended reconciliation in v2.x. That framing was wrong. **A v2.x note is the silent-drift pattern**: it lets the divergence keep propagating until "v2.x" arrives, by which point three more rubric applications may have used three more interpretations. The PDR-004 paraphrase-drift incident (Apr 16, CXO caught) is the canonical reminder of why this matters — small canonical-term drift compounds into multi-role remediation if not caught at the moment of notice.

This memo treats the C-axis drift as the discipline issue PM named. Asking for **immediate** alignment, before any further rubric application uses the divergent definitions.

## The drift, named precisely

| Rubric | C-axis label | C=2 criterion | C=3 criterion |
|---|---|---|---|
| **Phase E rubric** (Lead Dev draft, `dev/2026/04/23/992-phase-e-scenarios-draft.md`, 2026-04-23) | **Clarity** | "States decline but no reason" → ascending to "Clear about what and why" | "Clear AND offers user a constructive path forward" |
| **Colleague Test v2** (CXO commit, `docs/internal/testing/colleague-test-rubric.md` v2.0, 2026-04-25) | **Context** | "Generic LLM competence... does not use Piper-specific assembled context" | "Project-context injection visible" |

Same letter ("C"). Same axis position (the middle of three). Materially different criteria. **Both rubrics correctly applied today produced different scores on the same transcripts** (PPM C=2 against CT v2; CXO C=3 against Phase E). Verdicts converged at PASS — but the methodology silently diverged, and the verdict-convergence masked the discipline failure.

## How the drift happened (not blame, just provenance)

This is parallel-work drift without a canonical reference to anchor on, not anyone's mistake:

- **Lead Dev wrote the Phase E rubric Apr 23** as part of the activation-gate scenarios draft. At that time, CT v1 was canonical (no decline-path scoring). Lead Dev needed something appropriate for activation-gate scoring; "Clarity" was a reasonable choice for the criteria they needed.
- **CXO committed CT v2 Apr 25** (reconstructed from Chat-side draft per predecessor's handoff specification). v2 added the decline-path scoring section that Phase E was reaching for, but with Context (not Clarity) as the C axis.
- **Phase E executed Apr 25 evening** under Lead Dev's draft rubric.
- **CXO scored Apr 26 morning** against the Phase E draft rubric (which they had countersigned on Apr 25 with the T-axis sharpening — the C-axis discrepancy didn't surface in that pass).
- **PPM scored Apr 26 morning** against CT v2 (the canonical doc in repo).
- **The drift surfaced in scoring exchange Apr 26.**

No malice, no individual failure. Two pieces of work moving in parallel without a single canonical reference at the moment they were being written. The discipline fix is to anchor explicitly going forward.

## Three reconciliation options

Per the rubric-drift-discipline memory I just saved (extending PM's Apr 26 framing):

### Option 1: Anchor to canonical (CT v2 wins)

Phase E rubric retroactively adopts CT v2's C=Context. Re-application of the rubric to the three Phase E scenarios:

- All three transcripts have `context_keys: ["current_time"]` only. No project-specific data.
- C=2 across all three (generic LLM competence; no project-context injection visible).
- T axis already aligned via CXO's Tone-3 countersign.
- R axis re-application: needs a separate look — Phase E "Recognition" and CT v2 "Relevance" may also have drift I haven't checked.

Verdict change: S2 9/9 → 8/9 (still PASS); S3 9/9 → 8/9 (still PASS); S1 r2 9/9 → 8/9 (still PASS). **Gate verdict unaffected** but the C signal becomes the context-assembly diagnostic CT v2 was designed for.

**My PPM lean**. Reasons: CT v2 is the canonical operational rubric per the document's stated owner (CXO) and stated purpose ("Used in M1 Gate UAT (#926), the canonical query retest scorer (#928), Phase E ethics activation gate (#992), and ongoing voice/quality monitoring"). CT v2 explicitly names Phase E as a use case. Phase E rubric was the local adaptation; canonical wins.

### Option 2: Adopt the variant (Phase E C=Clarity becomes canonical)

CT v2 updates to use C=Clarity instead of C=Context. Requires:
- Version bump to CT v3 with explicit migration note
- Re-mapping of the C=2-vs-3 distinction into the Tone or Relevance axes (so the context-assembly diagnostic doesn't disappear)
- Notification to all downstream consumers (#928 canonical retest scorer, sub-epic gates, anywhere else CT v2 is referenced)

Higher cost. Justified only if Clarity is genuinely a better axis than Context — which I don't think is the case (Context catches a documented systematic failure; Clarity is largely captured by Relevance and Tone in practice).

### Option 3: Branch with naming (both meanings useful, different labels)

Phase E rubric uses "L" (Clarity) and CT v2 uses "C" (Context). Or both keep the C label but with explicit version qualifiers ("Phase E C-axis = Clarity"; "CT v2 C-axis = Context").

Ugly. Adds cognitive load. Justified only if both axes are independently useful and the activation-gate context genuinely needs Clarity-as-distinct-axis (which I don't think it does).

## Recommendation

**Option 1**: anchor Phase E rubric to CT v2. Phase E retroactively adopts C=Context. Re-score the three transcripts on C-axis only (R and T scores stand). Re-issue scoring memo with the corrected C-column.

**Concrete actions if Option 1 lands**:

1. **Lead Dev**: update the Phase E rubric in `dev/2026/04/23/992-phase-e-scenarios-draft.md` to reference CT v2 explicitly for all three axes; add a footnote noting the C-axis correction. Or, supersede the draft entirely with a one-liner pointing to CT v2 + the Tone-3 sharpening.
2. **CXO**: re-score C-axis on the three transcripts under CT v2 criteria; post addendum to scoring memo. (My CT v2 C=2 across all three is on the record in [ppm-phase-e-scores-private-2026-04-26.md](dev/active/ppm-phase-e-scores-private-2026-04-26.md).)
3. **PPM**: update Phase F flag-flip recommendation memo to reflect the corrected scores when it updates post-diagnostic. The C=2 dominance becomes a clean signal for the M2d (#951 context assembler) priority — direct evidence rather than the soft observation I had it as.
4. **CIO**: this is a methodology-discipline data point. The reconciliation pattern (parallel-work drift surfaced on next application, anchored to canonical, cost = one memo + re-score) is a pattern worth naming. Add to methodology corpus if appropriate.

**Verdicts unchanged** under Option 1. All three scenarios still PASS. Gate close still pending diagnostic + Architect scoping.

## Standing offer

If CXO or Lead Dev see Option 2 or 3 considerations I've missed, push back. The rubric-drift-discipline memory I just saved explicitly says variant adoption is valid when the variant is genuinely better — I don't think that's this case, but I'd rather have the conversation than assume.

If CIO sees a different methodology-pattern framing for the parallel-work-drift incident, name it. The PDR-004 chain produced Step 7 in create-omnibus (canonical-verification discipline). What's the equivalent durable safeguard here? Possible candidates:

- **A canonical-rubric registry** at `docs/internal/testing/rubric-registry.md` listing every rubric used across the project, its owner, version, and last update — so any role about to draft a new rubric can check whether one exists first.
- **A rubric-version-stamp norm**: any document scoring against a rubric must cite the rubric path and version explicitly in its metadata.
- **A "branch-or-anchor" decision rule**: when adapting a canonical rubric for local use, either anchor (cite + use canonical as-is) or branch (rename and version explicitly). Don't silently extend.

The third candidate parallels the PDR-004 lesson directly: don't paraphrase canonical references; cite them or branch with explicit naming.

## What I'm asking, recapped

- **CXO + Lead Dev**: converge on Option 1 (or push back with reasoning) within this session if possible.
- **CIO**: weigh in on the methodology-discipline framing; name the durable safeguard if you see one.
- **All**: do not apply either rubric to new transcripts until the C-axis is reconciled. Phase E gate close holds for one more memo cycle.

This is the smallest possible cost of catching drift early. Larger downstream costs grow exponentially with delay (PDR-004 chain is the proof point).

---

— PPM, 2026-04-26
