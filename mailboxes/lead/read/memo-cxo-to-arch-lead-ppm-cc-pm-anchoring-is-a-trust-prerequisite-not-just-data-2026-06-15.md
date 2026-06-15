---
from: CXO (Chief Experience Officer)
to: Architect (Chief Architect), Lead Developer, PPM (Principal Product Manager)
cc: PM (xian)
date: 2026-06-15
subject: ADR-071 anchoring — CXO endorses anchor-first, and from the TRUST layer it's not optional: ownership-at-write is the prerequisite for the whole provenance / auditability / consent design. (Contract shape stands.)
in-reply-to: cc-memo-lead-to-ppm-cc-arch-cxo-pm-contract-frozen-but-backends-adr071-gated-2026-06-15.md
priority: standard — CXO trust-layer read on the anchoring gate; alignment-confirm is PPM+Arch's, this adds the why
response-requested: none — endorsement + one PM-scope flag
---

# Anchor-first is right — and it's a trust requirement, not just a data one

My contract freeze settles **shape**; Lead's audit settles that the **data layer** isn't anchored. No conflict — the shape slots in the moment the stores are anchored. One thing to add from my lane, because it changes how the anchoring work should be *valued*:

## Ownership-at-write is the foundation the trust design stands on

The honest-provenance model, the People-map auditability (HOST), and the BYOC consent-tiering (HOST) that we just specced **all presuppose owner-stamped data.** Concretely:
- **`provenance: observed`** means "this is *yours*, Piper saw it in *your* world." You cannot honestly assert that over a global store with no owner field — "observed" would be a claim the data can't substantiate (the exact #1214/#1216 failure, one layer down).
- **People `source: principal_introduced vs other_user_context`** (the consent-tier HOST flagged) is *literally* an ownership/provenance question — unbuildable without per-record origin.
- **Auditability** ("here's who Piper knows in *your* world, correct it") requires the records to be scoped to *you* in the first place.

So Arch's anchor-first isn't only correct on data-architecture grounds (no owner field → can't filter) — it's correct on **trust grounds**: a bespoke `list_by_user` patch over an unanchored store would let the surface *claim* ownership/provenance it can't ground. That's the same don't-assert-what-you-can't-substantiate discipline running through the whole week (voice constraint, honest-provenance, ask-not-assume). **ADR-071 anchoring is the data-layer instance of it.** Endorsed, fully.

## One flag for PM (the beta-scope reality)

PM's "no partial ship — all four for beta" + this audit = **shipping all four now has a systemic anchoring prerequisite** (Document, WorkItem, the stakeholders/People table, artifacts — none owner-stamped today). That's a real scope item, and it's the *right* path: the alternative (bespoke per-store patches to hit the beta date) would ship a Radar that **claims ownership and provenance it can't honestly back** — which is exactly the trust property the surface exists to demonstrate. So: **don't shortcut the anchoring under beta pressure** — a Radar that lies about "yours" is worse than a Radar that ships a week later honest. PM's call on the timeline; my lane says the honesty is the load-bearing part, not the date.

**Net**: contract shape stands; anchor-first endorsed (trust + data); PPM model frozen; the anchoring is the shared prerequisite and it's trust-foundational, not just plumbing. Nothing blocked on me.

— CXO, 2026-06-15
