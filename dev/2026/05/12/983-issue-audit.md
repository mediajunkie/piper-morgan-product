# #983 CONTEXT-BLOCKED — Phase 0 audit

**Issue**: [#983](https://github.com/mediajunkie/piper-morgan-product/issues/983) — Identify and surface blocked items in floor context
**Scope**: M2f-E (first GitHub-API-via-cache surface; establishes pattern for #985 + #986)
**Branch**: `claude/983-context-blocked` (worktree `piper-morgan-product-983`)
**Author**: Lead Developer
**Date**: 2026-05-12

---

## Pattern-067 check

**Body's premise**: `_gather_blocked_items_context(user_id)` helper does not yet exist; floor formatter has no `blocked_items` key.

**Verified**: `grep "_gather_blocked\|blocked_items" services/intent_service/context_assembler.py services/intent_service/conversational_floor.py` returns only false positives (anti-fabrication prompt text mentioning "blocked" in the wrong sense, line 154/167 of conversational_floor.py).

**Conclusion**: NEGATIVE. Premise accurate; cleanly greenfield work.

---

## Canonical label (resolved)

`status: blocked` (namespaced with the space) — per PM disposition 2026-05-05 + Architect correction 2026-05-10. Documented at `docs/internal/operations/labels-reference.md`. Verified live: `gh label list` shows `status: blocked	Blocked items	#b60205`.

Currently 5 open+all issues carry this label (4 legacy `[PM-001/002/003/004]` + #983 itself). The query will work end-to-end with real data the moment the helper lands.

---

## Existing infra inventory

### GitHub access

`GitHubIntegrationRouter` (`services/integrations/github/github_integration_router.py`):
- `list_issues(repository, **kwargs)` — generic list, delegates to MCP adapter
- `get_open_issues(project, limit, owner, repo)` — gets open issues, no label filter in current signature (line 445)
- `repo_resolver` resolves the default repo when caller doesn't pass `owner`/`repo` explicitly

`GitHubAdapter` (`services/mcp/consumer/github_adapter.py`):
- `list_github_issues_direct(repo, owner)` — line 264; calls `repos/{owner}/{repo}/issues?state=all&per_page=100` and returns dicts with `labels` extracted as `[label["name"] for label in issue.get("labels", [])]`. **Labels are surfaced directly** — Python-side filtering is straightforward.
- No native server-side label-filter param plumbed through (could be added: GitHub API supports `?labels=status:%20blocked`).

**Conclusion**: client-side filtering of the `labels` list is the path of least resistance. No new GitHub-API plumbing needed.

### Cache infra (just landed in #984)

`ContextCache` + `cache_invalidation` modules. Pattern from `_get_*_cached` source-level helpers in `context_assembler.py` directly applies. Eager-invalidation hook surface: there isn't one — blocked-state changes happen on GitHub.com, out-of-band. **TTL-only invalidation** is the right call here (consistent with PM Q3=c — TTL-only on non-user-mutable data).

### Floor formatter

`conversational_floor.py` `_format_domain_context` (or equivalent) is the place to add the `blocked_items` key surface. Not yet inspected in detail — will do in Phase 1.

---

## Open design questions

### Q1 — Repo scope

- **(a) Single-repo, resolved via `repo_resolver`**: Today's reality — Piper Morgan tracks one repo (`mediajunkie/piper-morgan-product`). Simplest. Matches `get_open_issues` pattern.
- **(b) Multi-repo, "all tracked repos"** (per body framing): forward-looking; no multi-repo registry exists yet. Would couple this issue to building one.

**Recommendation**: **(a)** today. Multi-repo is a generalization that can land when there's a second repo to demonstrate need. (Filing #983-followup if/when applicable.)

### Q2 — Issue state filter

- **(a) Open only** — "what's blocked NOW"
- **(b) Open + Closed** — surface closed blocked issues too (probably noisy — many resolutions are "we unblocked and shipped")
- **(c) Open + recently-closed** — last N days of closed-blocked

**Recommendation**: **(a) Open only**. Closed-blocked is a history-query, not a status-query.

### Q3 — Limit

- Body silent. Most other surfaces cap at 5–10. Calendar/pending_todos cap at 10.

**Recommendation**: **Top 10** by `updated_at desc` (matches the existing pattern in context_assembler).

### Q4 — Sort order

- **(a) Most-recently-updated (desc)** — what's been touched lately
- **(b) Oldest-blocked (asc)** — what's been stalled the longest (often the more useful PM signal)
- **(c) Surface both buckets** — would require schema split

**Recommendation**: **(a) Most-recently-updated**. Simplest, matches GitHub's default. If PM later wants "longest-stalled" we can sort differently in a follow-up.

### Q5 — Which intent categories trigger this?

Body says PRIORITY. STATUS is a near-neighbor. UNKNOWN-fallback hits status_priority.

- **(a) PRIORITY only**: minimum scope
- **(b) PRIORITY + STATUS**: matches the "what's the state of things" framing
- **(c) Also UNKNOWN-fallback**: gets surfaced as part of the data-defaulting path

**Recommendation**: **(b) PRIORITY + STATUS**. Cleanest mapping to how users ask. UNKNOWN-fallback already calls `_gather_status_priority_context`, so adding to that method auto-covers (c).

### Q6 — Cache TTL

Body's #984 notes suggest GitHub TTL ~5min. Blocked items change rarely.

**Recommendation**: **TTL 300s (5min)**, key `context:blocked_items:{user_id}`. TTL-only invalidation (out-of-band GitHub mutations — no local hook to fire). Consistent with the projects/user_context surfaces.

---

## Suggested gameplan shape (pending PM yes/no on Q1–Q6)

Conditional on PM picking recommended answers (most are obvious):

- **Phase 1** (~30 min): build `_gather_blocked_items_context(user_id)` as a thin wrapper over `_get_blocked_items_cached(user_id)`. Cached helper calls `_compute_blocked_items` which:
  - Resolves the default repo via `repo_resolver`
  - Calls `list_github_issues_direct(repo, owner)`
  - Filters to `state == "open"` AND `"status: blocked" in labels`
  - Sorts by `updated_at desc`, caps at 10
  - Returns `{"blocked_items": [...], "blocked_count": N}` or `None`
- **Phase 2** (~15 min): wire into `_gather_status_priority_context` (covers STATUS, PRIORITY, and UNKNOWN-fallback).
- **Phase 3** (~30 min): add formatter for `blocked_items` in `conversational_floor.py` so the floor LLM gets it as a structured snippet.
- **Phase 4** (~30 min): unit tests — label-match path (issue surfaces), no-match path (empty), GitHub-API-error path (graceful empty), caching path (second call hits cache).
- **Phase 5** (~10 min): merge + close. **Remove `status: blocked` label from #983** itself as part of close (otherwise we'd surface the meta-issue forever).

**Total**: ~2 hr.

---

## Risks (carried forward from #984 + new)

1. **The meta-issue self-reference** (new): #983 itself is currently labeled `status: blocked`. After it ships, the label should come off, or it'll surface as a perpetual "what's blocked?" hit. Phase 5 includes label removal.
2. **Legacy `[PM-001..004]` noise** (new): 4 old issues are labeled `status: blocked` but may not represent real current blockers. Two options:
   - **(i)** Surface as-is — let user see; PM can clean up legacy labels separately
   - **(ii)** Filter out issues older than N days
   - **Recommendation**: (i). Cleaning up legacy labels is a separate PM action; the helper should faithfully surface what's labeled. If the legacy items annoy the floor responses, we can revisit.
3. **Repo-config implicit**: `repo_resolver` falls back to `mediajunkie/piper-morgan-product` per existing convention; if no repo is resolvable (test env, fresh install), return empty list silently.

---

## Audit-cascade Phase 0 self-check

| Template requirement | Status |
|---|---|
| Issue number referenced | ✅ #983 |
| Pattern-067 check | ✅ NEGATIVE — confirmed greenfield |
| Body-vs-reality | ✅ premise accurate |
| Infra inventory | ✅ GitHub adapter + cache pattern + floor formatter |
| Scope questions surfaced | ✅ Q1–Q6 above |
| Risk assessment | ✅ meta-issue label + legacy noise + repo-config |
| Recommended path forward | ✅ small (~2 hr) helper + status_priority wire + formatter + tests |

---

## STOP — awaiting PM decision on Q1–Q6

Most have clear-recommended answers. The least obvious is Q5 (categories that trigger). Most consequential is Q2 (state filter — open vs. open+closed). Standing by.

— Lead Developer
