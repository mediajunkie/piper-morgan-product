# #985 CONTEXT-SPRINT — Phase 0 audit

**Issue**: [#985](https://github.com/mediajunkie/piper-morgan-product/issues/985) — Surface GitHub sprint/milestone data in floor context
**Scope**: M2f-E (extends the #984 cache + #983 GitHub-gatherer patterns)
**Branch**: `claude/985-context-sprint` (worktree `piper-morgan-product-985`)
**Author**: Lead Developer
**Date**: 2026-05-12

---

## Pattern-067 check

- `_gather_sprint_context` / `_gather_milestone_context`: not present in `services/intent_service/`
- `"sprint"` / `"milestone"` / `"active_milestone"` keys: not present in `conversational_floor._format_domain_context`

**Conclusion**: NEGATIVE. Cleanly greenfield.

---

## Strong existing infrastructure

### GitHub access (already there)

`GitHubIntegrationRouter.list_milestones_via_mcp(state="open", owner=None, repo=None)` — exists, repo-resolves, normalizes the response:

```python
{
    "title": str, "number": int, "state": "open"|"closed",
    "due_on": ISO8601 | None,
    "open_issues": int, "closed_issues": int,
    "html_url": str, "description": str,
}
```

`GitHubAdapter.list_github_issues_direct(repo, owner)` returns issues with a `"milestone"` field set to the milestone TITLE (or None) — perfect for client-side filter by milestone.

### Live data check

```
$ gh api "repos/mediajunkie/piper-morgan-product/milestones?state=open"
4 open milestones:
  - MVP            (open 75, closed 680, due 2026-05-27)
  - Fast Follow    (open 35, closed 2,   due 2026-07-31)
  - Post-MVP       (open  6, closed 0,   due 2026-10-30)
  - Enterprise     (open 13, closed 0,   due 2027-04-15)
```

The "current sprint" framing maps cleanly to **the open milestone with the nearest `due_on`** (MVP today). Production data is rich.

### Cache infra (from #984)

`ContextCache` directly applies. Pattern: `_get_sprint_cached(user_id, ...)` + `_compute_sprint(user_id)`. TTL-only (sprint mutations are out-of-band on GitHub).

### Floor formatter (#911)

Same shape as `blocked_items` (just shipped in #983). Add `active_milestone` block to `_format_domain_context`.

---

## Open design questions

### Q1 — "Active milestone" selection rule

The repo has 4 open milestones. The floor should know about the active one. Options:

- **(a) Single milestone = open with nearest `due_on`**. Skips milestones without `due_on`. Simple, deterministic.
- **(b) All open milestones, sorted by due_on**. Surface up to N (e.g., 4); let the floor LLM pick what's relevant.
- **(c) Heuristic: the one with the highest open_issues + closed_issues count** (proxy for "most active"). MVP wins here today.

**Recommendation**: **(b)**, list all open milestones (capped at 5). Cheap, lets the floor compose accurate answers when the user asks about a specific milestone by name. Single-milestone surfacing limits the floor's options if the user query is "how's Fast Follow tracking?"

### Q2 — Include issues in the milestone(s)?

Body says "fetch active milestone **and issues in that milestone**". Options:

- **(a) Just milestone counts** (`open_issues`, `closed_issues`) — already in the normalized milestone object. Zero extra API calls. Floor can answer "75 open issues in MVP" but can't name them.
- **(b) Plus top N issue titles** per milestone — adds 1 API call per milestone (or 1 broader call + client-side filter). Floor can answer "what's open in MVP? — #984, #985, …"
- **(c) Plus high-priority issues** within each milestone — same as (b) but filtered by `priority: high`/`critical` label.

**Recommendation**: **(a) for first ship**. Counts are sufficient for the "how's tracking?" use case. (b)/(c) is a follow-up if user feedback says floor responses lack specificity. Sticking with (a) keeps the API call surface to 1 — `list_milestones_via_mcp` — and matches #983's "go small, ship, iterate" cadence.

### Q3 — Which intent categories trigger?

Body says STATUS, PRIORITY, maybe TEMPORAL.

- **STATUS / PRIORITY** ✓ — "how's MVP tracking?" / "what should I focus on?"
- **TEMPORAL** — "what's due this week?" / "what's the agenda?" The `due_on` field is temporal-relevant.

**Recommendation**: **Wire into `_gather_status_priority_context` AND `_gather_temporal_context`**. Both legitimately benefit. UNKNOWN-fallback inherits via status_priority.

### Q4 — Cache TTL

Milestones change rarely (typically once/sprint when a new one's added or due_on shifts). Issues being added/removed from a milestone is the more frequent change, but we're only showing counts (Q2=a) so even that's coarse.

**Recommendation**: **TTL 300s (5min)** — same as `blocked_items`. Consistent with the "external-state surfaces share a TTL family" intuition. Out-of-band invalidation (no local hook fires when someone closes an issue on GitHub.com).

### Q5 — Schema for the floor context

```python
context["active_milestones"] = [
    {
        "title": "MVP",
        "number": 5,
        "due_on": "2026-05-27T00:00:00Z",
        "open_issues": 75,
        "closed_issues": 680,
        "url": "https://github.com/.../milestone/5",
    },
    ...  # sorted by due_on ascending, capped at 5
]
context["active_milestone_count"] = 4
```

Key name: **`active_milestones`** (plural, since we're surfacing the list per Q1=b). Avoids the term "sprint" since GitHub doesn't have a first-class sprint concept — milestone IS the GitHub primitive.

### Q6 — Sort order

- **(a) due_on ascending** — nearest deadline first. "What's next" framing.
- **(b) most-recently-updated** — but milestones don't have an `updated_at` directly; would need fallback.
- **(c) highest open count first** — "most active first."

**Recommendation**: **(a) due_on ascending**, nulls (no-due-on) at the end. Floor can compose "MVP due 2026-05-27 has 75 open of 755 total…"

---

## Suggested gameplan shape (pending PM yes on Q1–Q6)

Conditional on PM picking recommended answers:

- **Phase 1** (~30 min): `_gather_active_milestones_context` thin wrapper + `_get_active_milestones_cached` + `_compute_active_milestones` (calls `list_milestones_via_mcp(state="open")`, sorts by due_on asc, returns up to 5).
- **Phase 2** (~10 min): wire into `_gather_status_priority_context` AND `_gather_temporal_context`.
- **Phase 3** (~15 min): `active_milestones` formatter in `conversational_floor.py` — title + due_on + open/closed counts per line.
- **Phase 4** (~30 min): unit tests — no-milestones path / single-milestone / multi-milestone-sort / API-failure-graceful / cache-second-call-hits.
- **Phase 5** (~10 min): merge + close. No legacy label hygiene needed for this one.

**Total**: ~1.5 hr (faster than #983 because the GitHub plumbing is more mature for milestones).

---

## Risks

1. **Milestone-flood**: if the repo has 50+ open milestones (it doesn't, has 4), the cap at 5 keeps things bounded. Sort by due_on asc ensures we surface the most actionable ones.
2. **Stale-due-on**: if a milestone is past its due_on but still open (post-deadline), it surfaces. That's correct behavior — user should know it's overdue. Floor can compose "MVP is past its 2026-05-27 due date with 75 open issues remaining."
3. **No description-in-context**: `description` field is dropped from the schema to keep context compact. If a user asks "what's MVP about?", the floor will give a generic answer rather than reading the description. Filed as a possible follow-up.

---

## Audit-cascade Phase 0 self-check

| Template requirement | Status |
|---|---|
| Issue number referenced | ✅ #985 |
| Pattern-067 check | ✅ NEGATIVE |
| Body-vs-reality | ✅ premise accurate |
| Infra inventory | ✅ list_milestones_via_mcp + adapter + #984 cache |
| Live-data verification | ✅ 4 open milestones, MVP most-imminent |
| Scope questions surfaced | ✅ Q1–Q6 |
| Risk assessment | ✅ flood + stale-due + description |
| Recommended path | ✅ ~1.5 hr (4 phases) |

---

## STOP — awaiting PM disposition on Q1–Q6

Most have clear recs. Most consequential: Q1 (single vs. all milestones) and Q2 (counts vs. issue titles). Defaulting to "go small, ship, iterate" on both.

— Lead Developer
