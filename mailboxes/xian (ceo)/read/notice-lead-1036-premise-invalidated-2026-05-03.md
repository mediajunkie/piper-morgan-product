# NOTICE: #1036 premise invalidated — `/api/v1/lists` GET is already wired

**From**: Lead Developer (Claude Code Opus, `lead-code-opus`)
**To**: PM (xian, CEO)
**Date**: Sunday, May 3, 2026
**Subject**: STOP-on-source-gap discipline triggered: #1036 was filed on incomplete spike data; the endpoint it would build already exists

---

## Summary

While starting execution of #1036 LISTS-LISTING-WIRE, I discovered that `/api/v1/lists` GET is **already fully implemented** at `web/api/routes/lists.py:216`, mounted via `web/app.py:221` (`web.api.routes.lists`), and backed by `services/repositories/universal_list_repository.py:94` `UniversalListRepository.get_lists_by_owner`. Auth-scoped via JWTClaims.

Per "STOP when finding gaps in sources" discipline (PM Apr 26: "We need to develop a rule that you STOP when you find gaps in sources. You don't cover for that."), I reverted my in-progress changes and stopped to surface this rather than building a parallel implementation.

## What the May 3 Phase -1 spike actually found

The spike at `dev/2026/05/03/m2d-phase-minus-1-infra-spike.md` Gap A flagged `services/api/todo_management.py:644` (a stub at `/api/v1/todos/lists`) as the lists-listing endpoint. **That's a different, parallel namespace** — also a stub, also under a misnomer (lists nested under `/api/v1/todos`), but **not the endpoint the frontend actually calls**. The frontend at `templates/lists.html:248` calls `/api/v1/lists` (no `/todos/` prefix), which routes to the working implementation.

The spike methodology missed a parallel route file (`web/api/routes/lists.py`) because the grep was scoped to `services/api/` rather than searching the full `web/api/routes/` directory. Saving as a feedback memory: when investigating endpoint coverage, search the full route-mounting tree, not just the apparent service directory.

## Implications

### #1036 LISTS-LISTING-WIRE
**Premise invalid — recommend close as "implementation already exists; #1036 was filed on incomplete spike data."** No code change needed; the endpoint works. Cross-reference: `web/api/routes/lists.py:216` is the live implementation.

### #714 MUX-LISTS-STALENESS-UI Q1 STOP-flag
The audit walkthrough disposition (Q1 → Option A: file pre-work for #1036) was based on the same wrong premise. **#714 can proceed without #1036 dependency.** The lists endpoint already returns user data; staleness signal can be added on top via the existing `web/api/routes/lists.py` GET handler.

### Open question — what (if anything) was actually broken about lists.html?
The Phase -1 spike report said "Frontend `templates/lists.html:248-261` calls this endpoint, gets `lists=[]`, and falls into the empty-state render. Lists view always shows 'No lists yet.'" — but if the real `/api/v1/lists` endpoint works, this observation may have been:
- (a) tested without authentication (endpoint returns 401 / empty for unauthenticated users)
- (b) tested against a DB with no list rows for the test user
- (c) tested against the wrong `/api/v1/todos/lists` URL path (the stub)
- (d) something else I didn't investigate

I haven't done the investigation that would distinguish these. **Recommendation**: defer until #714 actually executes, at which point Phase 0 will surface what (if anything) is wrong. The "lists page shows empty" observation may have been correct for a wrong reason.

## What I've done

- Reverted in-progress `ListRepository` addition on `claude/1036-lists-listing` (worktree clean; no commit on the branch)
- Worktree branch can be deleted; nothing pushed
- Filing this notice + recommending #1036 close

## What I recommend you do

1. Close #1036 with a comment cross-referencing `web/api/routes/lists.py:216` as the existing implementation
2. Approve removing the Q1 STOP-flag dependency from #714's gameplan (`dev/2026/05/03/714-gameplan.md`); allow #714 to proceed without #1036
3. (Optional) ratify the methodology lesson — feedback memory about endpoint discovery would help future spikes

## Filed by

Lead Developer 2026-05-03 per STOP-on-source-gap discipline.
