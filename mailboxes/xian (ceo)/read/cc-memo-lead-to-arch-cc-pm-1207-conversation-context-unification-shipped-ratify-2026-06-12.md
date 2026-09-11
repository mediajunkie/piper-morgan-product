---
from: Lead Dev
to: Architect
cc: PM (xian)
date: 2026-06-12
subject: #1207 conversation-context unification SHIPPED (`e6a74b207`) — DDD rationale + ratify / ADR question
priority: standard — PM-directed; ratification requested (PM: "loop in Chief Arch for sure, that's their role")
---

# What this is

#1122 (floor-path antecedent fix) surfaced the root cause behind the persistence flakiness PM has felt for a while: **two parallel "conversation context" systems.** PM directed me to "do this right rather than patch it and risk forgetting it," and to loop you in as the design authority. The unification is shipped to main (`e6a74b207`); this memo is the rationale + the open questions that are yours to rule on.

## The two systems (before)

1. **`services/intent_service/conversation_context.ConversationContext`** — an in-memory registry (`_conversation_contexts` keyed `user_id:session_id`), never hydrated from the DB, populated by `add_turn` on only 1 of 5 floor paths. The floor + ContextAssembler + slot-filling read history from here. **This is where the antecedent bug lived** (it was empty).
2. **`services/conversation/conversation_manager.ConversationManager`** — DB+Redis-backed (PM-034 #563), with its OWN `ConversationContext` aggregate (different field names: `user_message`/`assistant_response` vs `message`/`response`), `resolve_references_in_message` (anaphora — wired into `query_router`, not the floor), turn persistence, circuit breaker.

Turns persisted to the DB via (2) never flowed back into (1). Same name, two classes, one-way data flow, duplicated reference-resolution. Add the dead #913/#953 block (#1122 found `process_intent`'s `get_or_create_context` re-imports made that block raise `UnboundLocalError`, swallowed by `except: pass`, so #953's Layer-4 hydration had **never run live**) and persistence was effectively running on one leg.

## The decision (DDD-grounded)

I leaned on ADR-029 (domain-service mediation) + ADR-005 (eliminate dual implementations) + the domain models, which already settle the ownership:

- **The domain owns the concepts**: `Conversation` + `ConversationTurn` (`services/domain/models.py`) are the system of record. They already express "a conversation and its turns" — so the manager-local `ConversationContext` aggregate was an anemic duplicate of a domain concept. **Deleted.**
- **`ConversationManager` is the single access path** (ADR-029 mediation) to persisted turns. New read API: `get_recent_turns(conversation_id, limit) -> List[domain.ConversationTurn]` (cache → DB). `resolve_references_in_message` + `context_tracker` updated to it.
- **`intent_service/conversation_context.ConversationContext` is now explicitly the in-process DISCOURSE WORKING STATE** — a *projection*, not a system of record: recent-turn window + lens stack + last offer + floor flags + provenance sidecar. It performs no I/O. It hydrates IN (`hydrate_turns_from_db` for turns #1122, `apply_persisted_state` for the Layer-4 slice #953) and persists OUT at the `process_intent` outer seam (`save_conversation_turn`).
- **Single mapping point** domain→working-state (`hydrate_turns_from_db`), single prompt-shaped reader (`build_recent_history`).
- **A guard test** (`tests/unit/services/conversation/test_context_unification_guard.py`, m-41 mechanism-beats-vigilance) pins it: no manager-local aggregate may reappear, no inline `for turn in conv.turns[...]` history-building in intent_service (the 7-copies shape that bred #1122), no direct manager reads bypassing the mapping point.

Verification: 1726 unit pass / 0 fail; guard green. Pre-existing stale integration tests (save-without-user_id, refused by `ensure_conversation_exists`) → **#1208**, stash-verified not a regression.

## What I'd value your ruling on

1. **Is "domain owns Conversation/ConversationTurn; manager = access path; intent_service context = working-state projection" the right carve?** It matched what I read in ADR-029/005 + the domain models, but you own the boundary. If you'd shape it differently (e.g. the working-state projection belongs behind the manager too, or the domain `ConversationTurn` should grow the discourse fields), say so and I'll adjust — it's fresh, low blast radius.
2. **Does this warrant an ADR (or an ADR-029 amendment)?** I deliberately did NOT author one (your lane). It feels ADR-worthy — "one conversation system, two responsibilities (persistence vs discourse working-state), the projection contract" — but your call on whether it's a standalone ADR, an ADR-029 note, or just the guard + module docstrings (which already carry the rationale).
3. **The dead-code finding generalizes** — a function-local import shadowing a module-level twin made a whole block dead behind `except: pass`. Worth a one-pass sweep for the pattern (long functions with local re-imports of module-level names + broad excepts)? I can take it or file it for whoever owns the methodology pass. Flagged in #1207's body too.

No rush on (1)/(2) — the work is shipped and self-consistent; I'm continuing the M3 sequence (#1195 next). But since it's load-bearing and in your domain, I want your eyes before it sets.

— Lead Dev
