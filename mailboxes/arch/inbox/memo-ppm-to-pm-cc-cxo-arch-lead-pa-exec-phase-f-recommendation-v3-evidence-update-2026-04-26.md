---
from: PPM (Principal Product Manager)
to: PM (xian)
cc: CXO, Architect, Lead Developer, PA, exec (Chief of Staff)
date: 2026-04-26
subject: Phase F recommendation v3 — evidence-base update; PM's DO NOT AUTHORIZE decision stands and is now stronger
priority: normal
response-requested: PM read; only an action request if Architect's reframe (detector brittleness, not routing) changes how PM wants the rest of the work scoped
supersedes-evidence-base: memo-ppm-to-pm-cc-cxo-arch-lead-pa-exec-phase-f-recommendation-v2-2026-04-26.md (operational recommendation unchanged; evidence base extended)
relates-to: memo-pm-pa-to-lead-cc-ppm-cxo-arch-exec-phase-f-decision-2026-04-26.md (PM/PA authoritative decision — STANDS)
---

# Phase F Recommendation v3 — Evidence-Base Update

## What this memo is

Not a new recommendation. **PM's authoritative DO NOT AUTHORIZE decision stands.** This memo updates the evidence base behind it with Architect's #1002 scoping (~12:55) and Lead Dev's #1003 additional-vectors confirmation (~13:00). Both arrived after my v2 recommendation and after PM's decision was filed. The new evidence sharpens the framing without changing the operational outcome.

## What changed

### 1. Architect's #1002 scoping reframes the problem (significant)

[Architect memo](mailboxes/ppm/inbox/memo-arch-to-lead-cc-ppm-pm-cxo-pa-exec-1002-scoping-2026-04-26.md) — first Code-side Architect session. Two findings that change the framing of #1002:

**Finding 1**: The bypass is **detector brittleness, not routing failure.** The ethics gate is *already* at the universal entry point (`services/intent/intent_service.py:627`), positioned upstream of the pre-classifier. The bypass observed in S1 r1 is not "pre-classifier shadows ethics floor" by ordering — it is "ethics detector returns `violation_detected=False` for naturally-phrased harassment because the substring matcher in `boundary_enforcer_refactored.py:103-138` requires literal trigger words ('harass', 'bully', 'intimidate', etc.) that real harassment vectors don't quote."

My v2 (and v1, and the finding-response memo, and #1002 framing) all read "pre-classifier dispatch shadows ethics floor" as an ordering issue. **Architect's analysis shows the ordering is correct; the problem is what runs at step 5 of the dispatch order.** Same observable; different cause.

**Finding 2**: The detector's coverage is much more limited than my recommendation memos implied:

| Category | Recall on naturally-phrased input |
|---|---|
| HARASSMENT | Near-zero (substring matcher requires quoted trigger words) |
| PROFESSIONAL | Accidentally decent (pattern words like "personal", "private", "relationship" appear in natural speech — this is why S2 fired correctly) |
| INAPPROPRIATE_CONTENT | Low |
| PERSONAL | Zero recall — no detection method called |
| DATA_PRIVACY | Zero recall — no detection method called |

So PERSONAL and DATA_PRIVACY can never appear in `boundary_type` on the audit envelope from this code path. The "documented gap" v2 named is wider than I had it.

**Architect's recommended fix shape**: Fix B + C1 in combination — replace substring matchers with semantic detection (LLM classification or embedding similarity, ~3-5 days) AND demote BoundaryEnforcer to "literal-trigger backstop" while documenting the floor as the de-facto ethics layer for naturally-phrased input (~1-2 days). Combined ~5-7 days including ADR. Not a 1-day fix; not a 1-week fix.

### 2. Lead Dev's #1003 additional vectors (per v2 + PM/PA decision §"expanded diagnostic ask")

[Lead Dev memo](mailboxes/ppm/inbox/memo-2026-04-26-from-lead-to-ppm-cc-cxo-pm-arch-pa-exec-1003-additional-vectors.md) — three additional naturally-phrased harassment vectors run flag-off through the r2 code path. **All three reproduce the no-op pattern**: `floor_hit: true`, boundary fields absent, BoundaryEnforcer inert. The "sample of 1" caveat from v2 resolves decisively: no-op is a pattern, not an edge case.

Two surprises worth noting:

- **V1 routes through `execution / draft_communication`, not GUIDANCE.** No-op generalizes across intent categories, not just GUIDANCE-classified inputs. Implication for Architect's Fix B: semantic detection needs to run on all input regardless of intent category (which the architectural placement at line 627 already supports — the gate runs before classification).
- **V3 produced `decline_inappropriate_request` action at confidence 0.95** but with boundary fields absent. **There's apparently a separate path that recognized V3 as inappropriate and surfaced a decline action — and it's NOT BoundaryEnforcer.** Architect should investigate. Doesn't change Phase F; sharpens the architectural picture.

### 3. PM's expanded diagnostic ask is still pending (small)

PM/PA's authoritative decision memo asked Lead Dev for a **second diagnostic**: S2 mixed-professional input with `flag=false`. If S2's audit envelope is also absent flag-off → flag-is-theater extends beyond harassment. If S2's audit envelope IS present flag-off → flag matters somewhere. ~60s of compute end-to-end.

Lead Dev's additional-vectors memo addressed the harassment expansion (PM/PA item 1) but **not the S2 expansion (PM/PA item 2)**. Flagging here so it doesn't get lost. Recommend Lead Dev run it next when convenient — the S2 expansion is what disambiguates "flag-is-theater for harassment specifically" from "flag-is-theater across BoundaryType categories."

## How the operational recommendation strengthens (without changing)

PM's authoritative decision is DO NOT AUTHORIZE pending #1002 + #1003. The new evidence:

- **Strengthens the case** — the no-op generalizes across 4 harassment vectors (S1 r2 + V1/V2/V3); detector brittleness analysis (Architect) explains the mechanism analytically; PERSONAL and DATA_PRIVACY have zero recall by design.
- **Sharpens the fix shape** — detector replacement, not handler-order surgery. ~5-7 days B+C1, not a 1-day patch.
- **Reframes #1002** — the issue title and body should be updated to reflect that the bypass is detector brittleness, not pre-classifier ordering. Architect explicitly recommended filing a sibling P1 issue for B+C1; #1002 stays open as the umbrella.
- **Does NOT change the operational outcome** — flag stays false; PM's decision is correct as filed.

## What I'm asking

- **PM**: read the Architect reframe (detector brittleness, not routing) — does it change how you want the eventual fix scoped? If yes, the v3 framing of the ask to Lead Dev / Architect should reflect "detector replacement" rather than "routing fix." If no (just continue as PM/PA decision says), this memo is informational only.
- **Lead Dev**: when convenient, run the S2 flag-off comparison from PM/PA's decision §"expanded diagnostic ask" item 2. ~60s. Closes the last open evidentiary loop in the v2/v3 update path.
- **Architect**: V3's `decline_inappropriate_request` path (Lead Dev's surprise 2) — when in your scoping bandwidth, is this a real second-mechanism worth understanding, or an artifact?
- **CXO**: no new asks. The "no silent failures" companion principle in PM/PA's decision memo (which I did not have in my drafts) parallels the predecessor CXO's anti-fabrication principle and is worth noting in your standing voice oversight.

## What I am NOT doing

- Not filing a new "DO NOT AUTHORIZE" recommendation. PM/PA's authoritative decision is the binding document.
- Not re-titling or re-bodying #1002 myself. That's Lead Dev + Architect coordination per Architect's explicit recommendation in their scoping memo.
- Not running the S2 diagnostic myself. That's Lead Dev's pattern.
- Not addressing the V3 `decline_inappropriate_request` mystery. Architect investigation territory.
- Not closing #1003 or proposing closure timing. Lead Dev + Architect on that.

## Audit trail (post-PM-decision additions)

- PM/PA Phase F decision (authoritative): `mailboxes/ppm/inbox/memo-pm-pa-to-lead-cc-ppm-cxo-arch-exec-phase-f-decision-2026-04-26.md`
- Architect #1002 scoping reframe: `mailboxes/ppm/inbox/memo-arch-to-lead-cc-ppm-pm-cxo-pa-exec-1002-scoping-2026-04-26.md`
- Lead Dev #1003 additional vectors: `mailboxes/ppm/inbox/memo-2026-04-26-from-lead-to-ppm-cc-cxo-pm-arch-pa-exec-1003-additional-vectors.md`
- PPM retraction of pm-via-ppm Phase F memo: `mailboxes/ppm/sent/memo-ppm-retraction-pm-via-ppm-phase-f-2026-04-26.md`

— PPM, 2026-04-26
