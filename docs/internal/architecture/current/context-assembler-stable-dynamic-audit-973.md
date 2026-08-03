# Context assembler: STABLE vs DYNAMIC layer audit (#973 Phase 1)

**Status**: Architect-drive half COMPLETE, 2026-08-03. Implementation half is Lead's.
**Issue**: [#973](https://github.com/mediajunkie/piper-morgan-product/issues/973) MEM-CACHE-AUDIT — OPEN, milestone **Production** (verified live, not read off a doc).
**Method**: layer set enumerated from the class **AST**, not from a recalled list; cache paths detected by resolving `_TTL_*` constants and `get_or_compute` / `*_cached` call edges. Re-derivable — see §Method.

---

## ⚠️ First finding: most of what #973 asked for has already been done, by other issues

#973 (filed ~May 19) asked for three things. **Two are substantially complete by accretion**, delivered piecemeal by later issues while #973 sat open:

| #973's ask | State |
|---|---|
| **per-method TTL suggestions** | ✅ **DONE** — 10 named `_TTL_*` constants exist with per-type rationale and issue citations (#983 blocked-items, #984 the TTL-defaults set + PM approval 2026-05-12, #985 milestones, #986 recent-activity, #1155 high-priority-issues) |
| **pipeline reorder** | ⚪ **not assessed here** — no evidence it was done; also no evidence it's still wanted |
| **STABLE/DYNAMIC labelling** | ❌ **NOT DONE — zero occurrences of either word in the file.** This is the real remaining ask |

**The general shape is worth naming**: an issue can be **completed by other work without anyone closing it**, and the residue looks identical to an untouched issue from the outside. Same class as PDR-006's Q2 (a question PM had already answered) and #972 (closed six weeks while I carried it as open work).

---

## The layer map — 13 gather layers, 9 cached, 4 not

**Cached (9)**: `trust` (`_TTL_TRUST` 1h) · `calendar` (60s) · `reminder` (30s) · `temporal` (via pending/completed-todos + projects caches) · `status_priority` (via pending-todos + user-context caches) · `blocked_items` (300s) · `high_priority_issues` (300s) · `active_milestones` (300s) · `recent_activity` (300s)

**Uncached (4)**: `identity` · `discovery` · `memory` · `insight_pull`

### The classification — and only one of the four is uncached by *judgment*

| layer | class | evidence | disposition |
|---|---|---|---|
| **`memory`** | 🔴 **DYNAMIC** | reads in-memory conversation context (mutates **every turn**) + UserHistoryService | ✅ **correctly uncached.** Caching per-turn conversation state would serve stale turns — this is judgment, not omission. **Leave it.** |
| **`identity`** | 🟢 **STABLE (registry) + SLOW (user anchor)** | capabilities **derived from the workflow-dispatcher and plugin registries** (#923 — "in sync with runtime truth"), plus per-user anchoring data (#950) | **Cache candidate, and the strongest one.** ⭐ The registry-derived half is **process-lifetime stable** — it changes only on deploy/registration, so it arguably wants *compute-once-per-process*, not a TTL at all. The user-anchor half wants an ordinary slow TTL. **These are two different volatilities inside one layer** and that is the interesting result. |
| **`discovery`** | 🟢 **STABLE — it is an alias** | body is literally `return await self._gather_identity_context(user_id)` | **No separate work.** Caching `identity` caches this for free. Note the layer count overstates distinct sources: **13 layers, 12 data sources.** |
| **`insight_pull`** | 🟢 **STABLE** | composted insights from `InsightRepository`, banded by confidence (#1030). **Composting is a scheduled batch process** (`services/mux/composting_pipeline.py` — deterministic aggregation, no LLM, runs on a scheduler), so insights change when composting runs, **not per request** | **Cache candidate**, and the TTL should key on **composting cadence**, not on minutes. A 5-minute TTL here would be arbitrary; the honest bound is "until the next compost run." |

---

## Recommendation to Lead (implementation half)

1. **Cache `identity` — and split it.** The registry-derived capability set is process-lifetime stable; the user anchor is slow-changing per-user. **One layer, two volatilities.** Splitting them is more valuable than picking a single compromise TTL, and it makes `discovery` free.
2. **Cache `insight_pull`, keyed to composting cadence** rather than an arbitrary interval. If composting emits an event or a run timestamp, that's the invalidation signal; a TTL is the fallback.
3. **Leave `memory` uncached** and **say so in the code** — this audit's whole point is that an uncached DYNAMIC layer and an uncached-by-omission layer are indistinguishable from the outside. **A one-line `# DYNAMIC — per-turn, deliberately uncached` comment converts a silence into a decision.**
4. **Add the STABLE/DYNAMIC label to every gather layer**, which is #973's literal ask and currently at zero. The label is cheap; its value is that the *next* uncached layer is visibly either a decision or a gap.

---

## Confidence, stated

**High** on the layer map and cache-path detection — derived from the AST, re-runnable, and it corrected my own first attempt (a `sed`-based extraction misreported `trust` as uncached; I discarded those numbers rather than report them).

**Medium** on the volatility classifications — they rest on **docstrings and read-paths, not on measured mutation rates**. Nobody has instrumented how often identity's user-anchor data or the insight bands actually change. **If a TTL choice turns out to matter, measure before tuning** — the classification is sound enough to decide *whether* to cache and much weaker for deciding *at what interval*.

**Not assessed**: the pipeline-reorder third of #973. No evidence it was done; no evidence it's still wanted. **Someone should decide whether it's still in scope rather than leaving it as the reason the issue stays open.**

## Method (re-derivable)

```python
# layer set + cache edges, from the AST rather than a recalled list
import ast; tree = ast.parse(open('services/intent_service/context_assembler.py').read())
# ContextAssembler methods starting with _gather_; a layer counts as cached if it
# references a _TTL_* constant or calls get_or_compute / a *_cached helper.
```
