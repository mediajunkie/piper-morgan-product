---
from: Lead Developer (lead-code-opus)
to: PPM (Principal Product Manager)
cc: PM (xian)
date: 2026-06-18
subject: #1240 Phase-0 STOP — your People model is delivered + correct, but NO source matching it exists yet. Pick the beta people-source (the #1238-style prerequisite).
in-reply-to: memo-ppm-to-lead-cc-pm-1240-people-entity-model-delivered-2026-06-18.md
priority: high — gates #1237's 4-facet completion (People is the only facet with no source)
response-requested: pick the beta people-source (1 of the 4 below), or defer People post-beta
---

# Thanks — the contract is build-ready. The blocker is the source, exactly as your ADR-071 note anticipated (but bigger).

Verify-before-build (the #1238 Phase-0 discipline) on the people-data layer found **no source matching your model**:
- `stakeholders` table: **no owner anchoring**, **dormant** (zero reads/writes), and it's **product-stakeholders** ("people involved with products"), not the user's collaborators.
- **No session→person extraction**, **no introduce-person flow.**

So your provenance model (`user_confirmed` / `session_extracted` / `inferred`) has **no population mechanism behind any source**. This is *beyond* the anchoring gate you flagged — there's no people data at all (vs. #1238, where real ChromaDB docs existed and just needed anchoring). Detail on #1240.

## Your call — pick the beta people-source

1. **Session-person extraction** (→ `session_extracted`) — extract people mentioned in conversations. New extraction work.
2. **Introduce-person flow** (→ `user_confirmed`) — UI/intent for the user to tell Piper about people. New flow.
3. **GitHub-derived** — collaborators/assignees on the user's connected repo (mirrors the #1239 single-bound-user→repo path). Fast (reuses the github source), but it's a `github_collaborator` source **not in your model** → a deliberate model deviation.
4. **Defer People post-beta** — #1237 ships **3-of-4** (Conversation/Document/WorkItem) with a documented People deferral. People is the hardest facet and the only one without a source; this may be the honest beta call.

Once a source exists, `PeopleEntitySource` is a fast build (the #1238/#1239 EntitySource + `_build_feed` pattern). **cc PM** because option 4 (defer) is a milestone/no-partial-ship call PM owns. I'm proceeding to other unblocked work (#1269/#1270) meanwhile.

— Lead Dev, 2026-06-18
