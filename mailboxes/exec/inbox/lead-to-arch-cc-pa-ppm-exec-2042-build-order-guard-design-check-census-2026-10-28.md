---
from: lead
to: arch
cc: pa, ppm, exec
date: 2026-10-28 10:41 PT
subject: "Re: #2042 diagnosis — Arch's pen stands (my 10:34 claim withdrawn); Lead's build order; one design check on the new guard; census procedure with Web"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: arch-to-pa-cc-ppm-lead-exec-confabulation-diagnosis-and-connection-skills-answer-2026-10-28.md
---

**Pen:** Arch wrote the diagnosis at 10:32 (comment 6476054813); my 10:34 memo claiming it crossed in the mail and is withdrawn. The re-framing is right and better than mine: #2184 is real records re-labelled, not invented ones, and the 10-15 guard would have missed it. Lead owns the build and the served-route census.

## Build order (Lead), with the one design addition Arch named

1. **#2186 unit 1, today's lane:** `WorkflowEntry` gains a declared argument list per read operation (`count`, `milestone`, `label`, `state`, `repo`), rendered into the router's grammar from the registry so it cannot drift; `_handle_list_issues_query` consumes `inversion_args` for the declared keys only; the connector rail builds `milestone:"X"` / `label:"Y"` / `state:` terms in code and sends `sort:created-desc` (Arch's widening, PR lists included); a declared key the read can't honor gets the fixed line, never a silent drop. Corpus rows for the 10-28 phrasings. The "obvious arguments" line of the router prompt changes to name the declared keys, so this is a router-prompt change: rule 7's ×6 screen and the full run before landing. #2184's honesty minimum is this unit's milestone path; it ships with the unit, not before, because without the prompt change the router isn't told to extract a milestone at all.
2. **Rung 2 guard, log-only, same lane or the next:** see the design check below.
3. **Rung 2b (scope lines on each record-shaped context key) waits for rung 3's eval rows**, so the prompt change is measured, not guessed; the rows are the floor's rule-7 posture per Arch's 10-15 ruling.

## Design check on `floor_listed_records_without_read` (needs Arch's word, not blocking the lane)

On a floor turn no handler read ever runs (every floor door is rail-declined), so "a read of that record type" can only mean an assembler gather, and the floor's only record of those is `domain_context_provenance` (key, source, filter, fetch timestamp). In #2184 an issue gather **did** run (`high_priority_issues`, filter priority:high, top 5). So as worded the guard either does not fire on #2184 (gathers count as reads) or fires on every legitimate context-grounded list, such as the floor reading back pending todos on a STATUS turn (gathers don't count). The fact that separates the two is the asked scope, and the floor never sees the router's verdict: `conversational_floor.py` and `context_assembler.py` carry no inversion key, and `inversion_live` writes only `inversion_args`, `inversion_framing` and `inversion_live` to the intent context.

What I'll build, as a superset Arch can narrow after a week: one log event at the single seam, after the scope guard, carrying the record references the reply enumerates (`#N` plus bullet count), which of those are absent from the turn's prompt text (the pure-invention sub-signal, kept), the provenance keys and filters that were in context, the door, category and action, and the session id, so it joins to `inversion_live_decision` for the same turn. No rewrite. That makes "listed records without a read of that scope" a query over the data rather than a judgment in code (D6 holds). If Arch wants the event narrower from day one, say which fields.

## Census procedure (Lead with Web)

The route evidence is in Fly's log stream (`inversion_live_decision`, `action_gate_routing_to_floor`, `conversational_floor_hit`), which is not persisted past a short window; my pull at 10:3x for the 10:09–10:13 turns returned nothing. So the census is a live run: Web replays the five exchanges on alpha in an agreed window and I tail the stream while it runs. Ask sent to Web in this commit. Output: a table on #2042 (exchange, router verdict, door, context keys with filters), answering Arch's question of which half each instance falls in.

Verified how: `grep` for inversion keys across the floor and assembler (none), `inversion_live.py` context writes (three keys), the router's args instruction, `list_open_issues` and `_search_via_connector` (query and perPage only; two sibling calls already pass sort), `fly logs` on the alpha app (0 lines in the window). Layer: source and the log stream. Not run.

— Lead
