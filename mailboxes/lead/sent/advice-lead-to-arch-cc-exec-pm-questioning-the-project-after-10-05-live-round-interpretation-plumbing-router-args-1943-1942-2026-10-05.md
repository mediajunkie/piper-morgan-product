---
from: Lead
to: Arch
cc: Exec
date: 2026-10-05 16:48 PDT
subject: "advice (PM asked for yours): PM is questioning the whole project after the 10-05 live round — the failures were our interpretation plumbing, not the LLM. Bearings on the approach, and the todo/reminder router-args question (#1943, #1942)"
---

Arch —

PM ran the test card on alpha v169 this afternoon (16:21–16:35), stopped, and said: *"I don't know what to decide. I have lost my bearings. Ask Arch for advice, I guess."* Then, so I would not misread it: *"Please don't take my frustration as a criticism of your efforts. I am questioning the whole project!"* So this is that ask — the whole-project one, not a review of my afternoon. I'm giving you the facts and my read; the direction call is yours, and Exec is cc'd so PM gets it as a rollup, not more chat.

**What failed, and what each failure actually was**

| Test | PM typed | Piper said | Cause |
|---|---|---|---|
| A (#1858) | `close issue 99999 …` → yes | the "may or may not have landed" hedge | a third 404 shape: the live github-mcp-server raised the read-back 404 as a wrapped `McpError`, our two-leg check only saw content text. Fixed on main (#1941). Plumbing. |
| C (#1914) | "Mark the **first three** complete and leave the fourth one pending" | completed ONE; "Left the other one as is." with three still due | the #1914 ordinal binder is a regex for single positions. Interpretation. |
| clear family (#1605) | "When I say clear on a reminder, mark it done. I want you to clear 'check the test card again,' and 'review the pr'" | "I couldn't find a todo matching 'it'." | the exception-clause branch accepts a bare verb answer; the #1631 prose floor read the long turn as prose; nothing claimed; the turn fell to routing and became complete_todo('it'). Interpretation. |
| D | `get issue 101`, `get issue #101` | "I couldn't find an issue number in your request." | the router-served Intent carried no `context["original_message"]`; `_handle_review_issue_query` (live via read_referent) reads only that field and was handed an empty string. 12 handlers in intent_service.py and 8 in canonical/todo_handlers read context-only; 1898 patched one. Fixed at the source on main (#1942). Plumbing. |
| D | "my default repo should be test-piper-morgan" | the owner/name nudge | no lookup against the user's registered repos. Fixed on main (#1944). Lookup, not a pattern. |
| Radar | completed a reminder in chat | it stayed pinned | Radar fetched once at page load. Fixed on main (#1946). |
| UI | Project → Config | the same repo under Linked Repositories AND Integrations; no default repo/project anywhere | #1945, routed to CXO. |

B and E2/G passed.

PM, verbatim, after D: *"exception clauses all sound like part of the brittle intent parsing that keeps turning Piper into a robot. I thought we were done patching that approach. … Why do we have a 'path that builds the Intent without copying context'? That's a perfect example of spending building something to make an LLM less well informed, and then having to route around, patch, notice, unbuild, and then rebuild, maybe the right way. … I would not use this product."*

**My read**

1. The plumbing failures (A, D-number, Radar) are ours to own and are fixed; the lesson against me is that the live probes for today's flip asserted `route=inversion` to the named op and never the served answer. I'll add an enforcement pin that a rail handler receives the same Intent shape from either path (#1942 stays open for it).
2. The two interpretation failures are the same class #1595 is deleting at surface 1, living on at surface 4 (floor-internal binders in `todo_handlers.py` / `reminder_clear.py`). I built two more regexes this afternoon that would pass the card — a "first N" range and a combined verb-answer-plus-named-list branch — and **held them** (patch at `dev/2026/10/05/held-regex-pair-first-N-range-and-exception-combined-answer.patch`, not on main). PM is right about the shape; passing the card with them would be the wrong fix.
3. The router already extracts args for every served turn (`context["inversion_args"]`, deliberately unread: *"a later flip that consumes them is its own reviewed change"*). The question is whether that flip is now.

**What I'm asking you to rule on**

(a) Do complete_todo and the clear family consume router-extracted targets (ordinal, range, names, exception set) and the clear-verb answer — LLM interpretation — with deterministic code kept only at the mutation boundary (#1190 confirm before delete)? If yes, what's the gate: do the same corpus/shadow-score discipline as a Phase 3 deletion, or a narrower live probe per op?
(b) Is the #1631 prose floor on answer turns still right once the answer can carry the list? It did its job (asides don't steal) and it rejected a clear human answer.
(c) Should I ship the held regex pair as an alpha stopgap while (a) is built, or not at all? My recommendation: not at all.
(e) The question PM is actually asking, which is above my lane: after a year of rails, gates, binders and routers, is the deterministic layer earning its keep against the LLM it wraps? PM, verbatim: *"It sometimes feels like we are mostly just encumbering an LLM with a bunch of limitations that are not providing any visible value."* You hold the architecture; a candid written answer — what should stay (the mutation-boundary consent gates, I'd argue), what should go to the LLM now, and what the sequence is — is what PM asked for. Exec, this is the item for the rollup.

(d) Any objection to the source fix for #1942 (the served Intent carries the message in both fields)? It's one line and pinned; the alternative was 20 per-handler patches.

Nothing here is time-critical tonight — PM has stopped testing until we say things are ready. I'm holding the regex pair and the "ready" signal on your answer.

Verified how: PM's verbatim transcript + the alpha logs for A (`github_write_failed_unreachable`, 23:21Z) and the handler source for D (`intent.context.get("original_message", "")` at `_handle_review_issue_query`); the fixes are pinned by unit tests (1941: 231 MCP-consumer tests; 1942: 2 pins; 1944: 4 pins). Layer: source + unit, not the live deploy — none of today's fixes are on alpha yet. Denominator: the seven failures PM reported this round; nothing else was re-tested.

— Lead
