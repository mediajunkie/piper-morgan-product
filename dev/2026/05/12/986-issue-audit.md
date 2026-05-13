# #986 CONTEXT-ACTIVITY — Phase 0 audit

**Issue**: [#986](https://github.com/mediajunkie/piper-morgan-product/issues/986) — Recent activity feed in floor context
**Scope**: M2f-E (closes out the post-floor-coverage cohort)
**Branch**: `claude/986-context-activity` (worktree `piper-morgan-product-986`)
**Date**: 2026-05-12

---

## Pattern-067 check

- `_gather_recent_activity_context`: not in `services/intent_service/` ✓
- `recent_activity` key: not in `conversational_floor._format_domain_context` ✓
- **Subtle Pattern-067 hit on adjacent surface**: `GitHubIntegrationRouter.get_recent_activity(days)` (line 626) exists but has no underlying adapter implementation — its `_get_integration("get_recent_activity")` would AttributeError at runtime against `mcp_adapter`. The spatial fallback (`spatial_github`) module is also missing from the codebase (`find services -name "spatial_github*"` returns nothing). Existing callers (`standup_orchestration_service.py`) presumably never exercise it or eat the error.

**Conclusion**: `_gather_recent_activity_context` is greenfield. **Do NOT use** the router's `get_recent_activity` — build on `list_github_issues_direct` directly.

---

## Strong existing infra

`GitHubAdapter.list_github_issues_direct(repo, owner)` already returns issues (and PRs as issues per GitHub API conventions) with `state=all&per_page=100`. The normalized dict includes `updated_at`, `state`, `number`, `title`, `labels`, `assignees`, `milestone`, `uri` (html_url).

**Live data check** (last 7 days, `since=2026-05-05`): ~20+ issues touched — well under the 100/page cap. Single API call suffices.

**Note**: the adapter's normalized dict **does not preserve the `pull_request` field** from GitHub's raw response. So distinguishing issue-vs-PR requires either (a) a 1-line adapter addition or (b) skipping the distinction for first ship.

---

## Open design questions

### Q1 — Cross-integration aggregation (the body's framing)

Body: "across GitHub + Slack + calendar". Reality check:
- **GitHub**: working (adapter exists, data is rich)
- **Slack**: integration exists for messaging but **no activity-feed surface** — would require new plumbing
- **Calendar**: existing `_gather_calendar_context` already covers "what's coming up"

**Recommendation**: **GitHub-only for first ship**. Defer Slack to a follow-up if user feedback says floor responses lack Slack activity. The body's framing is forward-looking; matching today's reality keeps scope tight (same shape as #985 — small first ship, iterate).

### Q2 — Activity types

GitHub `/issues` endpoint returns BOTH issues and pull-requests (GitHub treats PRs as a kind of issue). Commits + comments are separate APIs.

- **(a) Issues + PRs combined** (everything from `/issues` endpoint, single call)
- **(b) Issues only** — filter out items with `pull_request` field
- **(c) Plus commits** — second API call to `/commits`

**Recommendation**: **(a) Issues + PRs combined, distinguished in the schema** (so floor can say "3 PRs merged + 5 issues closed"). Requires the 1-line adapter addition mentioned above OR raw `pull_request` field in the API response surfaced through.

Sub-question: if we go (a), do we add the `pull_request` field to the adapter's normalized dict, or skip the distinction? Recommendation: **add the field** (1-line change) for cleaner floor responses.

### Q3 — Time window

Body suggests `window_days=7`. Options:
- 7 days (week) — recent enough to be "recent" but not so wide it's noisy
- 14 days — bi-weekly cadence
- Parameterize (caller decides)

**Recommendation**: **7 days, hardcoded for first ship**. Parameterization adds API surface without obvious payoff today.

### Q4 — Limit

**Recommendation**: **top 10** by `updated_at` desc. Matches #983 / #985.

### Q5 — Intent categories that trigger

Body says TEMPORAL and STATUS.

- **TEMPORAL** — "what happened yesterday?" / "what did we accomplish this week?"
- **STATUS** — "what's going on lately?"
- **UNKNOWN-fallback** inherits via status_priority (per the existing pattern)

**Recommendation**: wire into **both `_gather_temporal_context` AND `_gather_status_priority_context`**. Same pattern as #985.

### Q6 — TTL

Same family as #983 / #985 (5min). Activity data churns more than milestones do — but 5min is short enough that the staleness is acceptable.

**Recommendation**: **TTL 300s**, key `context:recent_activity:{user_id}`. TTL-only invalidation (GitHub mutations out-of-band).

### Q7 — Schema

```python
context["recent_activity"] = [
    {
        "number": 1078,
        "title": "Refresh endpoint cookie-clearing silently dropped...",
        "state": "open",  # "open" | "closed"
        "type": "issue",  # "issue" | "pr"
        "updated_at": "2026-05-12T01:52:18Z",
        "url": "https://github.com/...",
    },
    ...  # sorted by updated_at desc, capped at 10
]
context["recent_activity_count"] = N  # total in 7-day window before slicing
context["recent_activity_window_days"] = 7
```

**Recommendation**: this shape.

---

## Suggested gameplan shape (pending PM yes on Q1–Q7)

Conditional on PM picking recommended answers:

- **Phase 1** (~10 min): 1-line addition to `github_adapter.py:list_github_issues_direct` — preserve `pull_request` field in the normalized dict (e.g., `"pull_request": issue.get("pull_request") is not None`).
- **Phase 2** (~30 min): `_gather_recent_activity_context` thin wrapper + `_get_recent_activity_cached` + `_compute_recent_activity` (calls `list_github_issues_direct`, filters by `updated_at >= now - 7d`, sorts desc, caps at 10, distinguishes issue/pr).
- **Phase 3** (~10 min): wire into `_gather_status_priority_context` AND `_gather_temporal_context`.
- **Phase 4** (~15 min): `recent_activity` formatter in `conversational_floor.py`.
- **Phase 5** (~30 min): unit tests — no-user-id / no-activity / window-filter-applied / type-distinction / cap-at-10 / API-failure-graceful / cache-second-call-hits.
- **Phase 6** (~10 min): merge + close.

**Total**: ~1.75 hr. The 1-line adapter change is the only "new surface" — everything else is pattern-extension.

---

## Risks

1. **`pull_request` field unverified**: I'm assuming GitHub's `/issues` response carries `pull_request: {url, ...}` on PRs and absent on issues. Live test confirmed: response has `"pull_request": ...` key on PRs (verified via `gh api repos/.../issues`). Safe to use.
2. **>100 issues in 7 days**: would require pagination. Not the case today, but cap-aware. Filed as a follow-up if observed.
3. **Slack-deferred risk**: PM might want Slack activity. If so, this becomes a multi-source helper. Per Q1 rec, defer.
4. **`recent_activity_window_days` in floor context**: adding this metadata key risks the floor LLM mentioning "in the last 7 days" verbatim. Acceptable — it's accurate framing.

---

## Audit-cascade Phase 0 self-check

| Template requirement | Status |
|---|---|
| Issue number referenced | ✅ #986 |
| Pattern-067 check | ✅ NEGATIVE (with adjacent-surface note on broken `router.get_recent_activity`) |
| Body-vs-reality | ✅ premise accurate; cross-integration aggregation deferred for scope reasons |
| Infra inventory | ✅ list_github_issues_direct + cache pattern + floor formatter |
| Live-data verification | ✅ ~20 issues touched in last 7 days; well under cap |
| Scope questions | ✅ Q1–Q7 |
| Risk assessment | ✅ pagination + Slack-deferred + window metadata |
| Recommended path | ✅ ~1.75 hr (6 phases including 1-line adapter prep) |

---

## STOP — awaiting PM on Q1–Q7

Most-consequential: Q1 (cross-integration scope — recommending GitHub-only) and Q2 (issue vs PR distinction — recommending yes via 1-line adapter change).

— Lead Developer
