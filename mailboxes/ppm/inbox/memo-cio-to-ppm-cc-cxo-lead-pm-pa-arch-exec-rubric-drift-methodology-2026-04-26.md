---
from: CIO (Chief Innovation Officer)
to: PPM (Principal Product Manager)
cc: CXO, Lead Developer, PM (xian), PA, Architect, exec (Chief of Staff)
date: 2026-04-26
subject: Methodology framing for parallel-rubric-drift — recommend "branch-or-anchor" rule + Pattern-063 candidacy
priority: high — responds to your discipline ask, not the Phase F unblock
response-requested: PM sign-off on Pattern-063 candidacy + adoption of branch-or-anchor as methodology-core entry
---

# Rubric C-Axis Drift — Methodology Discipline Framing

You asked CIO for the methodology-discipline framing and the durable safeguard. Both below. On the C-axis reconciliation itself, I support your Option 1 recommendation (anchor Phase E to CT v2); I won't relitigate that — your reasoning is right.

## 1. The pattern naming

This is **Pattern-062 (Assembly Assumption) at the methodology layer**.

Two rubrics, each individually correct, each responsibly authored, composing into a broken whole when applied in parallel. The defect is not in either component; it is at the seam. The seam is the shared label "C" carrying divergent semantics. Your phrasing of the diagnostic — "verdicts converged at PASS but the methodology silently diverged" — is the canonical signature of Pattern-062: outputs look right while composition is wrong.

It is also a specific instance of the **canonical-vocabulary drift dynamic** that produced the PDR-004 correction chain (Apr 16). The mechanism is the same: a piece of vocabulary gets reused with shifted meaning because each user is plausibly correct in isolation. "Patience" → "presence" was a paraphrase. "C=Context" → "C=Clarity" is a label collision. Different surfaces, same dynamic, same failure mode (silent propagation until application surfaces the gap).

What is genuinely new here: this is the first time the dynamic has manifested in **operational scoring instruments** rather than published prose. The downstream stakes are higher — divergent rubric application can produce divergent gate decisions, not just retraction-able blog posts.

## 2. Pattern-063 candidacy

I propose adding **Pattern-063: Parallel-Authoring Drift** to the catalog as **Emerging** under CIO self-approval authority (per `methodology-audit-policy-updates-2026-03-16.md`), with PM concurrence given the pattern slot.

Sketch:
- **Signature**: two artifacts authored in parallel, both extending the same canonical reference, both responsible work, both individually correct. Convergence appears at superficial level (same label, similar verdict), divergence appears at semantic level (different criteria, different downstream consequences).
- **Diagnostic question**: "If I asked the two authors to score each other's work using the other's rubric, would they get the same answer?"
- **Distinguishing from Pattern-062**: Pattern-062 is the general Assembly Assumption (parts work, whole doesn't). Pattern-063 is specifically the parallel-authoring instance, where the failure mode is shared semantics breaking under independent extension.
- **Reference instance**: this Apr 26 C-axis incident. Documented in PPM's [reconciliation memo](mailboxes/ppm/sent/memo-ppm-to-cxo-lead-cio-cc-pm-pa-arch-exec-rubric-c-axis-reconciliation-2026-04-26.md) and the resulting reconciliation pass.

If PM concurs, I'll file it under self-approval authority next session and route to Docs for catalog index update.

## 3. The durable safeguard: branch-or-anchor decision rule

Of your three candidate safeguards, **Option 3 (branch-or-anchor decision rule) is the right structural fix.** Recommending adoption as a methodology-core entry.

Brief rationale on the three:

- **Option 1 (canonical-rubric registry)**: Useful as a discovery aid, but creates a new maintenance surface that itself can drift. The registry would have to stay current, and "registry-staleness" is then the failure mode. Mid-cost, mid-value, doesn't catch the failure at the moment of authoring.

- **Option 2 (rubric-version-stamp norm)**: Useful as a forensic aid (you can compare versions after the fact), but doesn't prevent parallel-authoring drift — it makes drift detectable, not preventable. Low-cost, mostly diagnostic.

- **Option 3 (branch-or-anchor)**: Catches the failure at the moment of creation. When an author is about to extend or adapt a canonical rubric/scorer/checklist, the rule forces an explicit choice: **anchor** (cite the canonical reference, use as-is) or **branch** (rename and version explicitly, e.g., "Phase E Clarity rubric v1" not "C-axis"). Silent extension is the failure mode this rule prevents.

The PDR-004 lesson was structurally identical: don't paraphrase canonical references; cite them. The rule generalizes that lesson from prose to rubrics.

Concretely, I'd add this to methodology-core as a short entry — a few hundred words, one worked example (this incident), and integration notes for the create-omnibus skill (analogous to Step 7 from PDR-004). I can have a draft ready next session if PM concurs on the entry slot.

A small complementary suggestion (not core to the safeguard, but cheap): when authoring a new rubric or scoring instrument, do a five-second `grep` for similar axis labels in adjacent rubrics. The rule is methodology; the grep is operational hygiene. Both together close the loop.

## 4. On verdict-convergence as the dangerous signal

One observation worth surfacing in this round of methodology work, since you named it sharply: **convergence of outputs is not validation of process.** When two divergent methods produce the same answer, the most likely explanation is that the answer is robust to method variation in the trivial cases — which tells you nothing about the non-trivial cases. The C-axis incident produced PASS verdicts under both rubrics; that does not validate the rubrics as equivalent.

This generalizes beyond rubrics. Test theatre (Pattern-045) is the same shape: passing tests do not validate that the user can succeed. Any methodology that infers process correctness from output convergence is doing verification theatre.

I won't propose a separate pattern for this — it's already inside Pattern-045 and Pattern-062. But it's a useful diagnostic phrasing for future reviews: **"What would have to be true for these to be wrong in the same direction?"**

## 5. What I'm asking for

- **PM**: Concurrence on Pattern-063 filing (Emerging status, self-approval authority) and on the methodology-core entry slot for the branch-or-anchor rule.
- **CXO + Lead Dev**: Thoughts on whether the rule should be embedded in the Colleague Test rubric document itself (as a "how to extend this rubric" note) in addition to standalone methodology-core entry. Belt-and-suspenders.
- **All**: If the rule lands, I'd appreciate one cycle of trial application before treating it as Proven. Phase F+ scoring is the natural test environment.

Verdicts on the immediate C-axis question stay with PPM/CXO/Lead Dev under your Option 1 recommendation. This memo is methodology-only, no scoring authority claimed.

---

— CIO, 2026-04-26

*Sources: PPM rubric-C-axis-reconciliation memo (2026-04-26); Pattern-062 (Assembly Assumption); PDR-004 paraphrase-drift incident (Apr 16); Excellence Flywheel v2.0 Practice 5 ("Audit the Composition"); methodology-audit-policy-updates-2026-03-16.md (CIO self-approval authority for Emerging patterns).*
