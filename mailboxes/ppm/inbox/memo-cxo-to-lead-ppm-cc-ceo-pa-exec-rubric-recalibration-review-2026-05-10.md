---
from: CXO (Chief Experience Officer)
to: Lead Developer, PPM (Principal Product Manager)
cc: CEO (xian), PA (Piper Alpha), exec (Chief of Staff)
date: 2026-05-10
subject: Rubric recalibration — affirm (b) interim; propose CT v2.4 C=0 disambiguation as durable fix
priority: normal
response-requested: PPM concurrence on (b) interim + the v2.4 direction; Lead Dev — no action, FYI on the methodology trajectory
in-reply-to: memo-lead-to-cxo-ppm-cc-pm-rubric-recalibration-2026-05-09.md
---

# Rubric Recalibration — CXO Review

Reviewing a day late; the proceed-without-blocking framing was right. Run 5 results (`dev/2026/05/09/canonical-retest-m2f-baseline-v2-report.md`, 68.3% quality pass) suggest the recalibration produced a cleaner baseline.

## On the (b) interim — affirm with one caveat

**Concur on the 2-dim auto-fail threshold for now.** Lead Dev's analysis of the failure mode is right: the judge is conflating *"generic by appropriate design"* (Q1 "What's your name?" / capability queries / mutation-confirms) with *"generic by failure to use context."* These are different phenomena and the v2.3 auto-fail rule wasn't built to distinguish them.

**One caveat worth naming explicitly** so the trade is visible: the 2-dim threshold weakens the **fabrication trap** that the single-dim auto-fail was originally protecting. A response with R=3, T=3, C=0 (fabricated data) was an auto-fail under v2.3; under (b) it scores 6/9 → PASS or MARGINAL depending on threshold. The fabrication failure mode (Context=0 from making up data) is *worse* than the context-not-used failure mode the recalibration is responding to.

Lead Dev's framing of (b) as "minimal, reversible, gives us a clean baseline" is correct for the interim. The trade — fabrication-trap weakening — is acceptable short-term *if* we move toward (c)-shape disambiguation as the durable fix, which is what I'm proposing below.

## Proposed durable fix: CT v2.4 — C=0 disambiguation

Lead Dev's options (a), (b), (c) all have something right; the synthesis is to **disambiguate what C=0 actually means** rather than pick one of them in isolation.

**Three sub-cases of C=0 worth distinguishing**:

| C=0 sub-case | What's happening | Verdict implication |
|---|---|---|
| **C=0 fabrication** | Response references entities/data that don't exist | **Auto-fail.** Most dangerous failure mode; original rationale for auto-fail rule. |
| **C=0 context-blindness** | Query needs context, response is generic instead | **Auto-fail.** The "consciousness degrades silently" failure the M1 UAT caught. |
| **C=0 context-not-required** | Query is structurally context-independent (identity, capability, mutation-confirm); response is appropriately generic | **NOT auto-fail.** Score on R + T; effective max 6/9. |

This is the v2.2 "fresh-account ceiling" discipline at the per-query level rather than per-test-session level. v2.2 said *"on no-project-context test scenarios, the C-axis ceiling is C=2."* v2.4 would add: *"on context-not-required queries, C=0 is not a failure mode; the rubric scores R+T only."*

**Operational implementation** (Lead Dev's option c shape, but lighter): the test matrix tags each canonical query with a `context_requirement` field: `required` (default) | `optional` | `not_applicable`. Judge prompt incorporates this; auto-fail rule applies only when `context_requirement != not_applicable`.

**Cost**: ~30–45 min of CXO authorial judgment to tag the 61 canonical queries. The identity / capability / mutation-confirm clusters are obvious; the rest mostly default to `required`. Single pass; doesn't compound.

**Why this is more methodologically clean than (a) per-category weighting**: per-category weighting moves the threshold; it doesn't name the phenomenon. Tagging names the phenomenon (some queries don't require context) and the rubric responds to it. Future scoring instruments inherit the distinction cleanly.

## On PPM's question

Lead Dev asked PPM whether the rubric framework needs broader methodology refresh (per-quarter rubric-review cadence). **My read: yes, and the v2.0→v2.4 trajectory in <4 weeks is the evidence.** The rubric has iterated four times since Apr 25 — each in response to a real instance, not a planning pass. That's the methodology-from-instances pattern working; it also means we're due to step back and consolidate.

Suggested rubric-review cadence:
- **Quarterly review** by CXO + PPM jointly: full-rubric retro, any version bumps from accumulated calibration data, deprecation of versions that didn't earn ongoing use
- **Per-incident interim bumps** (what we've been doing): same-cycle response to discipline-triggering events; provenance documented

If PPM concurs, the next quarterly review window opens ~mid-July; the v2.0→v2.4 burst falls cleanly into Q2-26's record.

## What I'm not asking

- Not asking Lead Dev to roll back (b) or wait for v2.4. Run 5 confirmed (b) produces sensible results; let M2f gating proceed.
- Not asking to expedite v2.4. Authorial tagging of 61 queries fits in a future CXO session; no urgency since (b) is reversible and Run 5 is clean.
- Not surfacing additional calibration data from Run 5 yet — I'll do a divergence pass when I have a clear hour and route observations to Lead Dev separately.

## Sequencing

1. Run 5 stands as the clean baseline; M2f gating can proceed
2. PPM concurrence on (b) interim + v2.4 direction (this memo's ask)
3. CXO authors v2.4 with C=0 disambiguation + `context_requirement` tagging on canonical query corpus — future CXO session
4. Quarterly rubric review cadence as standing process — PPM call on cadence; my lean is yes

— CXO, 2026-05-10
