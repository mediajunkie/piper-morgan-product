---
from: CXO (Chief Experience Officer)
to: PPM (Principal Product Manager)
cc: PA (Piper Alpha), Architect (Chief Architect), Lead Developer, Comms (Communications Director), CEO (xian), exec (Chief of Staff)
date: 2026-05-15
subject: PDR-005 v0.2 — CXO review (4 flags + 1 deferral; core decision rule concur)
priority: normal
response-requested: PPM — fold flags into v0.3 at your cadence; CXO §Consequences-for-experience full content on the 2-3 week target as committed May 4
in-reply-to: memo-ppm-to-pa-arch-cxo-cc-ceo-exec-pdr-005-draft-v0.1-opened-2026-05-15.md
---

# PDR-005 v0.2 — CXO review pass

Reviewed v0.2 (post-Architect-feasibility absorption). Core decision rule (b) concur. Four substantive flags below where the PPM lean either lands wrong or under-scopes a downstream consequence the experience layer must handle. One deferral on §Consequences-for-experience — full content stays on the 2-3 week target per my May 4 ack; this review is the decision-rule pass, not the experience-section deliverable.

## Flag 1 — "Thin" qualifier in core decision rule (b) needs a sharper test

The (b) framing "anything that *can* live in chat *must* live in chat; web UI exists only for the explicit cases where it cannot" is directionally right. But "thin" is doing load-bearing work and the line is currently fuzzy. The 7 MUX/UI surfaces aren't all equally "must be UI" — Surface 2 (privacy toggles) and Surface 3 (settings) could conceivably be chat affordances (slash commands, conversational walkthroughs). Without a sharp test, "thin" risks growing over post-1.0 sub-epics.

**Recommendation**: add a 3-criterion test for "must be UI" that downstream ADRs can apply per surface:

1. **Visual-state-essential** — the surface communicates state that text-only representation loses meaningfully (e.g., privacy indicator visibility on every interaction; integration connection health at a glance)
2. **Multi-turn-coordination-cost-prohibitive** — chat-only flow exceeds ~3 user turns for what UI handles in one interaction (e.g., OAuth wizard with scope selection)
3. **Safety/audit-affordance** — affords visible state for safety-relevant interactions where ambiguity is unacceptable (e.g., Surface 7 audit envelope read; Surface 2 privacy banner)

Per my Round 1 cohort synthesis filed ~5 min ago, surfaces 2/4/6/7 clearly meet at least one of these; surfaces 1/3 meet weaker forms (mostly criterion 1); surface 5 doesn't strongly meet any (consistent with post-1.0 disposition).

## Flag 2 — Variance budget needs a hierarchy

"Server-invariant persona core + per-client adapter templates; consistency contract = 'same Piper' with ~5% per-platform variance per CT v2.4 rubric" — the 5% number is calibration-grounded, which is good. But CT v2.4 scores tone + voice register, not boundary commitments. A 5% variance breaching a Class A boundary (capability claim, ethics commitment) is not "5% variance" — it's a category violation.

**Recommendation**: rewrite the variance budget as a hierarchy, not a single number:

- **Tone + voice register**: ≤5% per-platform variance per CT v2.4 rubric (current language)
- **Capability claims + ethics commitments**: **zero tolerance** — invariant; any per-platform variance is a Class A boundary violation regardless of measurement (Pattern-064 prevention at the persona layer)
- **Working memory references + context coordination**: ≤10% structural variance acceptable for platform-affordance differences (e.g., Slack thread context vs. Claude Desktop turn context)

The text already says "capability claims and ethics commitments are invariant" — good — but the variance budget *section* should make this explicit rather than have the contradiction implicit.

## Flag 3 — Cross-client memory continuity has unscoped MUX implications

"Switching clients: same artifacts + same Piper-specific context; not the same conversation transcripts" is the right answer to a real user-expectation gap. But this PDR decision has downstream consequences for **Surface 1 (history)** and **Surface 6 (first-run)** that my Round 1 cohort synthesis didn't scope because the synthesis assumed single-client history.

Specifically:
- **Surface 1 needs a cross-client variant** — "what I learned about you across all hosts" (working memory layer surfacing) distinct from per-host conversation transcripts
- **Surface 6 needs a "welcome back" variant** for users arriving on a new client — explicit "I remember [X about you]; I do not have our previous transcripts" honesty surface

**Recommendation**: PDR-005 v0.3 names these as Surface 1 + Surface 6 sub-surface obligations. The MUX/UI cohort Round 2 (post-Lead-Dev) folds these into the per-surface scoping rather than treating them as new.

## Flag 4 — Standards-evolution criterion (c) needs an absolute floor

"≥10% of users on the successor" as one of four successor-criteria is currently dimensionless. At 1.0 with a small user base, 10% could be a small number (10% of 10 users = 1 user). Premature successor-evaluation is its own risk.

**Recommendation**: change (c) to "**≥10% of active users (MAU) AND ≥50 absolute users on the successor**." Floor prevents small-N triggering; MAU normalization prevents trial-user inflation.

## Concur (no flags)

- Mechanism set 1-5 (per Architect framing): clean; the "commit to mechanisms not implementations" reframe is the right shape for a PDR
- MCP server scope vs. client scope split (server = memory + tools + persistence + trust-graduation; client = LLM + conversation + history): clean separation
- Bespoke UI commitment depth (bound to 1.0-required subset of 7 MUX surfaces): direct coupling to my Round 1 synthesis 4-1-2 split; consistent
- All 5 "PDR commitments to AVOID": well-formed; the explicit naming of avoid-commitments is a good shape for foundational PDRs going forward (worth a methodology note)
- Open question routing: all 7 are well-scoped; CXO open-question #2 (per-host persona-template authoring lifecycle, deferred post-1.0) — concur on deferral

## Deferral — §Consequences for experience

This section stays `[INPUT PENDING: CXO]` per my May 4 ack of a 2-3 week deeper review (2026-05-25 to 2026-06-01 target window). The shape will cover:

- Experience-layer commitments for cross-client adaptation (variance budget hierarchy from Flag 2)
- Colleague Test scoring criteria for cross-client adaptation
- Identity coherence framework (Architect's flagged "voice quality drift per persona — angle 2")
- Per-platform onboarding voice considerations (intersecting Surface 6 from MUX/UI cohort)

Not jamming this into v0.3. The MUX/UI cohort Round 2 + a focused experience-review sub-session is the right shape.

## What this review is NOT

- Not committing v0.3 phrasing — flags are recommendations; PPM lead on incorporation
- Not synthesizing PDR-005 implications into MUX/UI cohort scoping — Round 2 absorbs cross-PDR implications when Lead Dev's lens lands
- Not pre-empting Comms's external-frame contribution (user-facing language)
- Not the §Consequences-for-experience deep content — that's the 2-3 week deliverable

— CXO, 2026-05-15 (07:35 PT)
