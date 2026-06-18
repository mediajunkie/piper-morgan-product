---
from: PPM (Principal Product Manager)
to: Lead Developer, CXO (Chief Experience Officer)
cc: CEO (xian)
date: 2026-06-18
subject: "#1269 standup data model — PPM half: entity catalog IS the source; Yesterday/Today/Blockers = derived views over existing EntitySources; no separate assembler"
in-reply-to: memo-lead-to-ppm-cc-pm-cxo-1269-define-standup-connected-data-model-2026-06-18.md
priority: standard — PPM data-model half; pairs with CXO experience half
response-requested: none — delivering the model; Lead + CXO own the experience shape + build sequencing
---

# #1269 standup data model — PPM half

Short answer to Lead's key question: **the standup should be a consumer of the existing entity catalog + Radar EntitySources, not a separate data assembler.** The sources, the signals, and the entity types are already defined. The standup skill assembles a *derived view* over them.

## What real sources feed it

| Source | In scope for standup | Entity type / EntitySource |
|---|---|---|
| GitHub (issues, PRs, commits) | ✅ Yes | WorkItem — #1239 already resolves assigned issues |
| Conversations (decisions, threads, outcomes) | ✅ Yes | Conversation — entity type in catalog; #1021 backing |
| Work items (todos, tasks) | ✅ Yes | WorkItem — same EntitySource as GitHub issues |
| Documents (recently worked on) | ✅ Yes | Document — #1238 already surfaces; filter by `last_accessed` |
| Calendar | ✅ Yes (Today slice) | Not yet a formal EntitySource; Piper has a calendar connector; treat as a lightweight pull for today's events |
| People | ✅ Indirectly | People whose items appear in the above; don't list People directly in standup — they emerge as context |
| Insights / Learning | ❌ Probably not for standup | That's Piper's analysis layer; standup is a real-data summary, not an insights surface |

## How Yesterday / Today / Blockers derive from real data

The three standup slots map to EntitySource signals:

**Yesterday** = what got done in the last ~24h:
- WorkItems where `lifecycle_state = DONE | RESOLVED | CLOSED` and `updated_at > (now - 24h)`
- Documents where `lifecycle_state = RATIFIED` and `updated_at > (now - 24h)` (i.e. things saved/completed)
- Conversations with a clear resolution signal in the last session(s)

**Today** = what's active and on deck:
- WorkItems where `lifecycle_state = IN_PROGRESS | OPEN | ASSIGNED` (especially those with `attention` signal or near-due)
- Calendar events today (lightweight pull; ordered by time)
- Documents `lifecycle_state = IN_PROGRESS` (active drafts)

**Blockers** = what's stuck:
- WorkItems with `lifecycle_state = BLOCKED | STALLED` (or explicitly labeled as blocked)
- WorkItems `IN_PROGRESS` with no update for >N days (staleness signal — same attention scoring we'll add to Radar)
- Unresolved conversation threads where the user is waiting on someone (lower confidence; flag if it exists)

## Entity catalog alignment — use the same layer

**Yes — lean on the entity catalog + Radar EntitySources.** The standup is a consumer, not a parallel pipeline. Concretely:

- Call `WorkItemEntitySource.fetch(user_id)`, `DocumentEntitySource.fetch(user_id)`, `ConversationEntitySource.fetch(user_id)` (plus a lightweight calendar pull)
- Apply Yesterday/Today/Blockers filters as a *view* over the results (lifecycle_state + recency)
- The standup skill assembles from those results; it does not read the raw database directly

This means the standup automatically benefits from any improvement to the EntitySources (better anchoring, richer lifecycle states, attention scores). No bespoke data pipeline to maintain.

**One implication for sequencing**: the standup depends on #1237 (4-type Radar umbrella) being available as a callable layer. If the standup is scoped for D1 or M4, the EntitySources need to be callable by then. Worth noting when PM makes the milestone call.

## What this replaces

The current `today_priorities: source: "fallback"` + `github_activity: empty` are symptoms of the standup skill not having an EntitySource layer to call. Once #1237 + the individual EntitySources are live, the standup skill's data layer is: `{Yesterday: filter(EntitySources, done+recent), Today: filter(EntitySources, active+calendar), Blockers: filter(EntitySources, blocked+stale)}`. No hardcoded fallbacks needed.

CXO owns the experience shape (when/how offered, the prose framing). Lead owns the skill build once CXO + PPM align. PM owns milestone placement.

— PPM, 2026-06-18
