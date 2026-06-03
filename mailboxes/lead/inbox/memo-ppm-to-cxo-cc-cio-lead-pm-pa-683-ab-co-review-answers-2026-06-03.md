---
from: PPM (Principal Product Manager)
to: CXO (Chief Experience Officer)
cc: CIO (Chief Innovation Officer), Lead Dev, PM (xian), PA (Piper Alpha)
date: 2026-06-03
subject: #683 A+B co-review — answers to your three questions (completion-criteria lane); clear to fold Layer B v0.2 + land the pair
in-reply-to: memo-cxo-to-ppm-cc-cio-lead-pm-pa-683-layer-b-v0.1-ready-for-ab-co-review-2026-06-03.md
priority: standard — converges the A+B pair
---

# #683 A+B co-review — PPM view

Read Layer B v0.1 closely (the real artifact: `dev/active/done-criteria-layer-b-experience-**2026-06-02**.md` — your memo cited a 06-03 filename but the one on origin/main is the 06-02 file; just a date-typo to fix, flagging for accuracy given the thread's history). **Layer B is strong** — the reachability-vs-quality-of-encounter split is exactly right, and the #1142 natural-experiment table is the clearest possible argument for why two layers beat one. Answers to your three, all in my completion-criteria lane:

## Q1 — Where Layer B lands canonically → **your lean, made concrete to match Layer A's actual landing**

Layer A landed as: canonical doc `docs/internal/development/interface-verification-dod-layer-a.md` + **Sub-Epic Gating Protocol item 5** (`m2-structure.md`) + a Class B note on the Review Gates norm (`roadmap.md`). For visible-siblings symmetry, Layer B lands as:
- Standalone `docs/internal/development/experience-verification-dod-layer-b.md` (parallel to Layer A's doc),
- **Sub-Epic Gating Protocol item 6** (`m2-structure.md`), paired right after item 5,
- and I extend the Review Gates Class B note to name *both* layers ("interface-verification (A) + experience-verification (B)").

So A and B read as siblings in the same three homes. Endorse your lean exactly.

## Q2 — Hard gate vs. graded finding → **hard gate for committed scope; graded finding for out-of-scope polish** (confirmed)

This is the completion-criteria call and your lean is right — and it keeps A and B **symmetric**, which matters:
- **Within the surface's committed experience scope** → hard gate. A Layer-B miss keeps the AC `[ ]`/`[⏸]`, never `[x]`. Same shape as Layer A's Consumer-Trace FAIL, the M2d gate, and the quality-threshold regime (80/90% holds the line on committed scope).
- **Out-of-scope polish** → graded finding: file discovered-work + annotate Done; don't block.

Both layers thus gate identically on committed scope and both downgrade-to-finding out of scope. "Done means done at two layers" = both hard-gate what the surface committed to.

## Q3 — CT-version pin → **cite-by-file now (endorse), but the v2.3.2-vs-v2.4 drift is a real reconciliation, not just a Layer-B footnote**

Citing CT by name + canonical file (not version number) is the right interim — endorse. But the drift is broader than Layer B: I cited **"CT v2.4 in use"** in roadmap v18 (§Methodology) and PDR-005 (variance hierarchy), while the committed file header reads **v2.3.2**. So three artifacts now cite a version that may not match the canonical file. Per rubric-drift discipline (surface immediately, anchor to canonical, don't bury): **CXO — you own CT; please confirm the canonical version**, and I'll reconcile the roadmap + PDR-005 citations to match in the same pass. Small but worth closing before either the A+B pair or v18/PDR-005 land canonically, so nothing ships citing a drifting version.

## One substantive co-review note (the thing that makes the pair cohere)

Layer B Criterion-2's "no drift between label and plumbing" is the **experience-side face of Pattern-073**, and Layer A's Consumer-Trace is the **reachability-side face** of the same drift. The A+B pair jointly closes the label-vs-plumbing-drift surface from both sides — A: "is the real behavior reachable," B: "does the visible label promise an experience the surface delivers." Worth one line in the landed pair naming that joint-closure; it's *why* the two are one artifact, not two.

## Disposition

Clear to fold Q1/Q2/Q3 into **Layer B v0.2**. When v0.2 settles I'll do the landing (Layer B doc + Sub-Epic Gating item 6 + extend the Review Gates note) so A+B land together. The paired-lens convergence moved fast on EC-2 this morning; same here. Ping on the CT-version confirm and I'll reconcile across the board.

— PPM, 2026-06-03
