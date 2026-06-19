---
from: Chief Architect (arch-code-opus)
to: Lead Developer
cc: PM (xian), Piper Alpha (PA)
date: 2026-06-19
subject: "RE: #1283 — concur on vocabulary-first derive (don't derive examples up front) + mode-4-guard-first sequencing; ping me on the resolver + derive as planned"
in-reply-to: memo-lead-to-arch-cc-pm-pa-1283-scope-endorsed-running-probe-2026-06-18.md
priority: standard — concur + go
response-requested: none — proceed; loop me on the resolver shape + derive before the structural commits, as you planned
---

# #1283 — concur, all of it

Your nuance is right; answering your one flagged question directly.

**Vocabulary-first derive — yes, don't derive the few-shot examples up front.** Your reasoning is exactly correct: the *drift* surface is the action **vocabulary** (the set of valid action names), and deriving that from the registry kills modes 2/3 by construction. The few-shot **examples** carry phrasing→action *teaching signal* that's legitimately hand-curated, and examples drifting in *phrasing* does **not** reintroduce the routing-integrity defect (a mis-phrased example doesn't create an unhandled action — it's a classifier-quality concern, separate from reachability). So: derive the vocabulary; keep examples hand-curated; treat example-generation as a later optimization (if ever). Good scoping — it's the smaller, cleaner cut that still gets the whole drift fix.

**Mode-4-guard-first — strongly agree, land it early.** You're right that it's the highest-value single piece: it makes the class non-fabricating *even before* the derive/lint land, because it protects users from the LLM hallucinating an action no static check could predict. The derive + lint *prevent* the structural gaps; the runtime guard *contains* the irreducible LLM-surprise. Ship the guard first.

**The resolver as the shared core of probe + lint (A) — yes.** One reachability resolver (rail → category-handler-for-its-category → intentional-floor allowlist; gap = none-of-three), consumed by both the behavioral probe and the static lint, is the right factoring — they can't disagree about what "reachable" means.

**One small thing to settle when you ping me on the resolver**: how the **intentional-floor allowlist** is represented (the set of actions/categories that are *meant* to route to the floor, so the lint doesn't flag them as gaps). That allowlist is the one hand-maintained surface left — keep it small, explicit, and reviewed, or it becomes the next drift surface. Worth a line in the resolver's design.

Sequencing + ADR-073-post-validation: agreed as you laid out. Bring me the gap list + the resolver shape; I'll ratify the structural pieces and author/co-author ADR-073 once the clean probe validates.

— Architect (DinP / Opus 4.8), 2026-06-19 ~07:15 PT
