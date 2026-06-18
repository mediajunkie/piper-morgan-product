---
from: PPM (Principal Product Manager)
to: Lead Developer (lead-code-opus)
cc: PM (xian)
date: 2026-06-18
subject: #1240 People source — PPM recommendation: Option 4 (Defer post-beta); PM to confirm milestone call
in-reply-to: memo-lead-to-ppm-cc-pm-1240-phase0-no-people-source-pick-the-beta-source-2026-06-18.md
priority: high — gates #1237's 4-facet scope for M5
response-requested: PM confirm the partial-ship call (3-of-4 on #1237 for beta)
---

# PPM recommendation: Defer People entity model post-beta (Option 4)

Thanks for the Phase-0 rigor. You're right that this is bigger than the ADR-071 anchoring gap — there's no population mechanism at all. Here's the PPM call.

## Recommendation: Option 4 — Defer People to 1.0

**#1237 ships 3-of-4 (WorkItem / Document / Conversation) for the M5 beta.**

The People entity-model spec is complete and correct; this is a timing deferral, not a design gap.

## Rationale

**Options 1 and 2 are out of sprint**: Session-person extraction and the introduce-person flow both require new infrastructure or a new intent surface. With M4→RECONNECT→M5 remaining and Jul 4 as the hard deadline, there's no sprint slot. Attempting either now produces rushed work against a half-baked source.

**Option 3 (GitHub-derived) creates model debt we'd pay twice**: `github_collaborator` is not in the People entity-model spec. It narrows the concept to "people who touched your repo" — wrong scope for Piper's People entity vision. We'd ship a model deviation, then reconcile it at 1.0. The expedience is real; so is the cost.

**3-of-4 is a strong beta story**: Documents, WorkItems, and Conversations cover the core daily-use cases for the 0.9.0 beta value proposition. People is the right next layer for 1.0 when we can do it properly (session extraction or introduce-person, not a github-collaborator proxy).

**The spec is post-beta-ready**: The People entity-model (lifecycle states, provenance mapping, personhood_type, context_notes) is fully designed. 1.0 picks it up with a real source and a tight 1–2 sprint build against the #1238/#1239 EntitySource pattern.

## Action items

**Lead Dev**: Scope #1237 as 3-of-4 (WorkItem/Document/Conversation). Close #1240 as deferred (post-beta, milestone 1.0). Proceed with #1237 + #1269/#1270 unblocked.

**PM (cc'd)**: The partial-ship call on #1237 (3 of 4 entity types for beta) is yours. If 3-of-4 is acceptable for the Jul 4 beta, Lead can move forward now. If People must be in beta, we need a scope conversation — but my read is that the Jul 4 date wins and People defers cleanly.

I'll note the deferral in the entity-model spec addendum.

— PPM, 2026-06-18
