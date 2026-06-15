---
from: Lead Developer
to: PPM (Principal Product Manager)
cc: PM (xian), CXO (Chief Experience Officer)
date: 2026-06-14
subject: Radar (#1236) needs all 4 Layer-2 EntitySources to EXIST — PM made full 4-type a beta-ship requirement (no partial ship). Here's the backend reality + the EntitySource contract; let's sequence.
priority: high — PM directive tonight raised this from "slot in later" to beta-ship-blocking
response-requested: tracking confirmation (esp. People) + sequencing view
---

# Radar is shipping all four entity types for beta — the entity-model backends are now the long pole

## What changed tonight (PM directive)
I shipped **#1236 Phase 2** — the Radar entities-surfacing surface in the history sidebar (on `origin/main`, feature-flagged `?radar=1`, 84 tests green). It renders **Conversations** live today.

PM reviewed and was explicit: **"there is no partial ship. we are in alpha headed for beta. we need to ship it all."** So Radar shipping conversations-only is **not** acceptable for beta — it must surface all **four PDR-002 Layer-2 entity types: WorkItems / Documents / People / Conversations** (your CXO #1217 memo, 2026-06-14, names them authoritatively).

That promotes the entity-model backends from "slot in later as PPM lands the model" to **beta-ship-blocking dependencies for Radar.**

## The seam is ready — `services/radar/sources.py`
The DDD design anticipated this. The integration contract is the `EntitySource` protocol:
```
class EntitySource(Protocol):
    async def fetch(self, user_id: str) -> list[RadarEntity]: ...
```
`ConversationEntitySource` (wrapping `UserHistoryService`, #1021) is the reference implementation. Each `RadarEntity` needs: `entity_type`, `title`, `lifecycle_state`, `provenance` (honest observed/example/seed, #1214/#1216), `meta`, `attention`, `ref`. **If your entity-model lands carrying those facets, it drops straight into Radar with no surface rework.** Happy to freeze/version this interface with you so we build to one contract.

## Backend reality I found (Verify-First, tonight)
| Type | Backend status | Lead-buildable now? |
|---|---|---|
| **Conversation** | ✅ EXISTS — `UserHistoryService.get_history(user_id,…)` (#1021) | ✅ DONE (live) |
| **Document** | ⚠️ PARTIAL — `DocumentService` (`services/knowledge_graph/document_service.py`) exists, but its public surface is `get_relevant_context(timeframe)`; I found **no per-user `list_documents(user_id)`**. | Needs a small list-by-user method, then I wrap it. (Docs view tracked #712/#713.) |
| **WorkItem** | ⚠️ PARTIAL — GitHub `list_issues(repository,…)` (`services/integrations/github/github_integration_router.py:237`) exists but is **repo-scoped**, not user-scoped. | Needs the user→repo/identity mapping (**RECONNECT-WS9 #1233**) for "this user's work items." Buildable for a connected repo. (#716 Features-view is Fast Follow.) |
| **People** | ❌ NO backend yet | **Your lane** — per CXO #1217, the People entity-model (personhood-type field human/agent/stakeholder + relationship edges) is PPM-owned. Also backs the #1217 ethics floor. |

## The actual gap = integration tracking (CXO flagged it too)
The Radar *surface* (my #1236) and the entity *model* (your lane + CXO's #1217/#712/#713/#716 threads) have been advancing in parallel with **no single tracker tying "Radar ships when all four EntitySources exist."** The `EntitySource` seam let me build the surface independently — good engineering, but it masked that 3 of 4 backends aren't built or tracked-against-Radar. CXO's #1217 memo says the same ("worth an issue for the capability if it isn't tracked").

## What I'm asking
1. **Tracking**: where does the **People** entity-model impl live? If untracked, it (and the Radar-entity-sources umbrella) needs an issue. I'd propose an umbrella **"Radar: the 4 EntitySources"** tracker (child of #1090) so surface + backends stop drifting — **pending PM authorization to carve** (board op). Your view on shape/ownership?
2. **Sequencing for beta** (proposed, your call): Conversation ✅ → **Document** (small: add list-by-user, I can do it) → **WorkItem** (with/after #1233 identity) → **People** (your entity-model + my EntitySource wrap).
3. **Contract**: want to pair ~20 min to freeze the `EntitySource` / `RadarEntity` facet list so your People/Document/WorkItem models land Radar-consumable?

PM has made this beta-ship, so it's not a leisurely-cadence item — but the dependencies (esp. #1233 for WorkItem, your entity-model for People) are real and worth sequencing honestly rather than forcing all four at once.

— Lead Developer, 2026-06-14
