# Mock-Adapter Ground-Truth Harness — Plan

**Author**: Lead Developer · 2026-06-13
**Status**: BUILDING — ✅ **calendar slice shipped 2026-06-13** (`6874834ef`): `TestCanonicalGroundTruthMocked` with reflect / empty / degradation, all verified (3 passed). Pattern proven. **Remaining: GitHub slice** (same shape on `GitHubMCPSpatialAdapter.list_*`).
**Parent**: #1213 (canonical suite expansion) · follow-on to **P1** (ground-truth)
**Why this is separate from shipped P1**: P1 seeds *app-controlled* data (todos) deterministically. **External-data** queries (GitHub issues/PRs/milestones, Google Calendar) can't be seeded that way — the data lives in real external services. This harness makes them ground-truth-testable by **mocking the integration adapter** to return known data, then asserting the query response reflects it.

---

## Goal

Catch the same wiring-bug class P1 catches (route + structure fine, but data is stale/empty/wrong) for **external-data** queries — deterministically, every PR, no live external calls.

The unit under test is the **handler → formatter wiring**: *given* the adapter returns known data, does the user-facing response faithfully reflect it (and degrade honestly when the adapter returns empty/errors)? The real external API call is a separate integration concern, deliberately out of scope here.

## Design

Patch the adapter's **public fetch method** (class-level) to return known data for the duration of a single in-process request, then assert on the rendered response. In-process patching works because the canonical suite's `ASGITransport` runs the handler in the *same* process + event loop as the test, so a `patch.object(...)` context manager around the `await client.post(...)` is visible to the handler.

### Real patch points (verified 2026-06-13)

**Calendar** — `services/mcp/consumer/google_calendar_adapter.py::GoogleCalendarMCPAdapter`:
- `get_todays_events(user_id)` · `get_next_meeting(user_id)` · `get_current_meeting(user_id)` · `get_free_time_blocks(user_id)` · `get_temporal_summary(user_id)` · `get_events_in_range(start, end)`
- (The `calendar_integration_router` delegates to these, e.g. line 296 `await integration.get_events_in_range(...)`.)

**GitHub** — `services/mcp/consumer/github_adapter.py::GitHubMCPSpatialAdapter`:
- `list_github_issues_direct(...)` · `get_closed_issues(...)` · `list_milestones(...)` · `list_releases(...)` · `list_labels(...)` · `list_branches(...)`

All are **async** → patch with `AsyncMock(return_value=<known data>)`.

### Reusable helper (sketch)

```python
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, patch

@asynccontextmanager
async def mock_adapter(target, method, return_value):
    """Patch an adapter's async fetch method for one request. `target` is the
    adapter CLASS (patches all instances regardless of per-request vs cached)."""
    with patch.object(target, method, new=AsyncMock(return_value=return_value)):
        yield
```

### Scenario shape (calendar example — recommended first slice)

```python
async def test_week_reflects_known_events(e2e_client, e2e_auth_headers):
    known = [{"summary": "MOCK-EVT-7f3a", "start": "...", "duration_min": 30}]
    async with mock_adapter(GoogleCalendarMCPAdapter, "get_events_in_range", known):
        d = await send_canonical_query(e2e_client, "what's my week look like?", "mt-cal", e2e_auth_headers)
    assert "MOCK-EVT-7f3a" in d.get("message", "")   # data flows through
```

## Scenarios this enables

1. **Reflect**: adapter returns known item → query response contains it (calendar "what's my week", GitHub "show stale PRs" / "what shipped this week").
2. **Empty-state honesty**: adapter returns `[]` → response says "nothing" honestly, doesn't fabricate.
3. **Degradation** (folds in P2's per-action detector): adapter raises → response degrades with a specific, honest message, NOT a generic catch-all (and not silently swallowed).

## Risks / tradeoffs

- **Patch-point maintenance, NOT runtime flakiness** — mocking *reduces* flakiness vs hitting live GitHub/Calendar. The real cost is keeping the patch target aligned if an adapter method is renamed; mitigate by patching the narrowest stable public method.
- **Scope**: mocking the adapter means the test does NOT exercise the real external call (auth/transport) — that's intentional (this targets handler→formatter wiring). The live-call path stays a separate manual/integration concern.
- **Verify-at-build**: confirm which adapter method each target handler actually calls (e.g., does "what's my week" go through `get_events_in_range` or `get_temporal_summary`?) — a quick instrument-the-handler pass, like the #1122 probe.

## Effort

- Pin handler→adapter method mapping (verify-first): **S**
- Reusable `mock_adapter` helper + known-data builders: **S**
- Calendar slice (reflect + empty + degradation): **M**
- GitHub slice (issues/PRs/milestones): **M**
- **Total: M** (focused half-day). Recommended first slice: **calendar reflect** (calendar is freshly connected + relatable), then empty-state, then GitHub.

## Decision

Build now / defer as tracked follow-on / focus elsewhere — PM's call. Tracked under #1213 (this plan referenced from the #1213 status comment).
