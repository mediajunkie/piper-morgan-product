---
from: PPM (Principal Product Manager)
to: Lead Developer
cc: CEO (xian)
date: 2026-06-18
subject: "#1240 unblocked — People entity-model delivered. RadarEntity contract for PeopleEntitySource. ETA: now. Separate from #1270."
in-reply-to: memo-lead-to-ppm-cc-pm-expedite-people-entity-model-gates-1240-1237-beta-radar-2026-06-17.md
priority: high — unblocking Lead on #1240/#1237
response-requested: Lead — confirm contract is build-ready; flag if backend source (ADR-071 path) reshapes any field
---

# People entity-model — delivered. Build #1240 against this.

## ETA

Now. The People entity model was specified in `ppm-spec-radar-layer2-entity-model-2026-06-15.md` §3; what was missing was the concrete RadarEntity mapping (the EntitySource contract layer). That's what this memo delivers.

## Separate from #1270

The #1270 work is the Document source-facet model and the ArtifactSourceType reconcile. People entity-model is a distinct deliverable — the PPM spec for the People entity type in the typed entity catalog. Parallel tracks; neither blocks the other.

## RadarEntity contract for PeopleEntitySource

Build `#1240 PeopleEntitySource.fetch(user_id)` to return `list[RadarEntity]` with this shape:

```python
RadarEntity(
    entity_type = "people",
    title       = person.display_name,  # "First Last" or handle if no full name
    lifecycle_state = LifecycleState(
        label = <see table below>,
        tone  = <see table below>,
    ),
    provenance = Provenance(
        status = "observed" | "inferred",
        source = <see table below>,
    ),
    meta = {
        "personhood_type": "human" | "agent" | "stakeholder",
        "context_notes": str | None,  # brief note on who this person is in user's context
    },
    attention = None,   # People attention scoring is post-MVP; omit for beta
    ref = {"entity_type": "people", "entity_id": person.id},
)
```

## Lifecycle state mapping

| State | label | tone | When |
|---|---|---|---|
| `ACTIVE_COLLABORATOR` | "Active collaborator" | `"active"` | Person mentioned/interacted with in recent sessions |
| `KNOWN` | "Known" | `"neutral"` | Person Piper knows; not recently active |
| `DORMANT` | "Quiet recently" | `"quiet"` | Was active; has dropped off |
| `MENTIONED` | "Mentioned" | `"faint"` | Appeared once or twice; lower confidence |

Use `ACTIVE_COLLABORATOR` / `KNOWN` for `provenance.status = "observed"` (user explicitly introduced or confirmed). Use `MENTIONED` for `provenance.status = "inferred"` (Piper extracted from session without explicit confirmation).

## Provenance source mapping

| How Piper learned about this person | `provenance.status` | `provenance.source` |
|---|---|---|
| User explicitly told Piper ("my manager is Sarah") | `"observed"` | `"user_confirmed"` |
| Session extraction (mentioned in conversation) | `"observed"` | `"session_extracted"` |
| Piper inferred a relationship (not explicitly stated) | `"inferred"` | `"inferred"` |

## ADR-071 note (for your build decision, not a PPM gate)

My 6/16 alignment confirm flagged that the stakeholder/People data store may lack `user_id` owner stamps, same as Document/WorkItem. PPM's object-model is now delivered — the ADR-071 anchoring path is your architectural call. If the current People data store IS owner-stamped (or if you have an anchored path), build now. If not, flag it and PPM will note the People EntitySource as ADR-071-gated in the same way Documents is. The model above is correct either way; only the backend source varies.

## What this unblocks

- **#1240 PeopleEntitySource** — mirrors #1238 DocumentEntitySource; use the same `_build_feed` / per-source isolation pattern. The RadarEntity contract above is the spec.
- **#1237 4-type Radar umbrella** — People is the 4th type (WorkItem, Document, Conversation, People). PPM's model for all four is now formally delivered.

Build when your anchoring path is clear. Flag me if any field in the contract above needs revision once you're in the code.

— PPM, 2026-06-18
