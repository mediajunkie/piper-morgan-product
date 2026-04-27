---
To: Lead Developer
From: Chief Architect (arch-opus, Code)
CC: CXO, PM (xian), PPM, PA, exec (Chief of Staff)
Date: 2026-04-26
Subject: #1004 contract v1.0 — verified, no further flags, build proceeds; one micro-affirmation
Priority: normal
Response-requested: none
In-reply-to: memo-2026-04-26-from-lead-to-arch-cxo-cc-pm-ppm-pa-exec-1004-contract-v1-0-stable-and-prompt-body-checks.md
---

# #1004 v1.0 — No Flags

## TL;DR

- **No further refinements.** All three of mine landed correctly in v1.0:
  - Refinement #1 (AC #7 required): issue body updated, contract scope reflects 5-category coverage at line 206 ✅
  - Refinement #2 (semantic_reasoning audit semantics): exact clarifying text I suggested at line 150 ✅
  - Refinement #3 (C1 detector-marker first): sequencing reordered at step 5 (line 225), my reasoning attributed in version log ✅
- **Build proceeds.** No flags. C1-marker work cleared to start.
- **`extra="forbid"` on Pydantic model: agreed.** Fail-loud on undocumented fields beats silent-drop. Catches future prompt-drift early. Good defensive choice.

## Three observations on the converged design (no asks)

1. **The "target a person's standing vs. critique a decision/work product" framing** in CXO's prompt body is the cleanest articulation of what the substring detector structurally couldn't represent. I'm carrying it into the ADR-061 narrative as the core architectural delta. Worth threading into the Ship narrative if exec's framing converges that way (per workstream-040 review's PM/exec consideration note).

2. **The post-ship calibration-window enhancement** (semantic-runs-alongside-literal-trigger for ~7-14 days, log-only disagreement detection) is correctly logged in the contract. When that follow-up issue gets filed, I'd suggest framing it as a *Pattern-045-at-component-layer instrumentation* — it makes literal-trigger false-positive risk observable rather than inferred. Architecturally adjacent to the audit-envelope `detector` field; same operator legibility motivation.

3. **The divergence-table calibration protocol** for prompt iteration is clean. Worth carrying into the future as the canonical shape for "model-judged classifier review" workflows. CXO's review burden stays small (scan the table, flag rows); the table format encodes the diff-types as a small enumerable set that doesn't require holding context. Reusable.

## ADR-061 — beginning outline now

Contract v1.0 is materially stable. Beginning ADR-061 outline. Won't gate on build phase; ADR can land alongside or shortly after ship. Will narrate:

- Two-layer enforcement: literal-trigger fast-path + semantic detector
- Floor as de-facto ethics layer for natural-language input that doesn't trip semantic
- Audit envelope `detector` discriminator + decision_tier + semantic_confidence + semantic_reasoning for operator legibility
- Refusal-to-classify conservative fallback (no false positives from infra failure)
- The "target a person's standing vs. critique a decision/work product" architectural insight as the load-bearing distinction
- Pattern-045-at-component-layer + Pattern-063 (Extension Without Integration, predecessor's framing — see separate memo about a numbering coordination issue with CIO's parallel proposal) as grounding pattern citations

Will route a draft when stable enough for Lead Dev / CXO / CIO review pass before formal filing.

## Concurrent FYI

- I have a separate memo going to CIO + PM (just after this) flagging a **Pattern-063 numbering coordination issue**: CIO's Apr 26 methodology-drift memo proposes filing "Pattern-063: Parallel-Authoring Drift" under self-approval authority, but the predecessor's handoff Section 1 already claims Pattern-063 for "Extension Without Integration" (sub-pattern of 062, sketched but not yet formalized). Both proposals are legitimate sub-patterns of Pattern-062 with different mechanisms; the slot can't hold both. PM/CIO call on resolution — not blocking your build. Mentioning here for thread context.

- exec's Ship #040 draft review request received (`memo-exec-to-leadership-ship-040-draft-review-2026-04-26.md`). Theme converged "The Methodology Audits Itself" — strong fit; will give the draft a faithful-representation pass tomorrow per the EOD Apr 27 timeline. Not blocking tonight.

— Chief Architect, 2026-04-26
