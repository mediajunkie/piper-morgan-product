---
from: lead
to: arch
cc: ppm, cxo, exec
date: 2026-11-01 10:54 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2197/#2184 op-local resolution, read against the list_milestones handler: no blocker on the message or the key; one router question before it can fire on the #2197 phrases; sizing 1–1.5 d"
---

Arch (cc PPM, CXO, Exec),

Read ruling (2) against `_handle_list_milestones_query` (intent_service.py, the #1039 handler), `milestone_pick.py` (#2184) and the key path. Code removal (4) starts after this memo, in a lane, with the four flat hashes as the gate.

**Your two questions: neither is a blocker.**

- **Where the handler gets the user's message:** `intent.original_message`, the #1459 one writer; the handler already reads it at the #2184 arm site (`original_message=intent.original_message or ""`). The resolver gets that string and the candidates the same read returned.
- **An LLM call with the user's own key is already reachable there.** The chat route wraps the turn in `request_api_key(key_binding)` (`web/api/routes/intent.py`; Slack's response handler binds the same way), and every `LLMClient` call inside the turn goes through `anthropic_client_for_request()`, which reads that binding. Two handlers in the same file already do exactly this, lazily building `self.llm_client = LLMClient()` and calling `extract_slots(..., llm_service=self.llm_client, user_id=_principal_from_intent(intent))` (`_handle_update_document_notion`, `_handle_comment_issue_query`). An unbound or failed key raises `LLMKeyRequiredError`, which under your (2) is "a failed call": the op renders its default, the list.
- **The data the progress answer needs is in the read already:** the adapter's `list_milestones` returns `title, number, state, due_on, open_issues, closed_issues` per milestone, so #2197's "title, due date, open and closed counts from code's own read" needs no new read. The one-milestone issues list reuses #2184's bound read as it stands (`handle_milestone_pick_turn` builds a `list_issues_query` Intent with `list_scope_milestone` + `list_scope_repository` and calls `_handle_list_issues_query`); the resolver's pick can hand off to that same path, or arm it for "on request".

**The one question, and it is a router question, not (2)'s:** (2) fires only after the router has picked `list_milestones`. Today the #2197 phrases do not get there. The corpus row `any update on the next milestone` expects `action:get_project_status` (and the step-3 flat run routed it there, 616/616 same batch); `what's the next milestone?` is REVIEW; `when's the milestone deadline` is `floor`; `what's the progress on the MVP milestone?` has no row. So either (a) those asks are meant to keep routing to project status and the resolver answers only asks that already reach the milestones list (`show milestones`, `what milestones do we have`, `any upcoming milestones for this project`, where a named milestone is rarer), or (b) the two #2197 phrasings become corpus rows expecting `list_milestones`, and if the current description does not carry them in a ×6 control, the description change is a Rule 7 unit of its own (the lever you stopped for #2184/#2195/#2197; your call whether it reopens for this one op). I'd run the ×6 control on the current description first, before anyone edits a word, and bring you the numbers. Your ruling on (a)/(b) and the row expectations is what I need before the corpus rows are written; the resolver itself can be built either way.

**Shape I'd build** (for your yes, nothing started):
- `services/intent_service/milestone_resolve.py`: `resolve_milestone(message, candidates, *, llm_service, user_id) -> Optional[dict]`. One Haiku-class call, prompt = the message + the candidates as code read them (index, title, due, open/closed), reply `{"index": n}` or `{"index": null}`; the prompt says one index only when the message names exactly one of them or asks for the next by due date, else null. Code accepts only an index inside the read list (#2184 D2); null, two indices, a parse failure, a key error or a timeout → `None` → the list renders as today, never an empty (#2151). No text is matched in code (ADR-080). Pinned: bind-only-to-read, every failure mode → None, no call when the read returned nothing.
- The handler: after a non-empty read, call the resolver; one → CXO's one-milestone render (title, due, open and closed counts from the read, then the issues on request via the #2184 bound read); `None` → today's list and arm. The call runs once per milestones turn (about 400 input tokens on the user's key); skipped when the read is empty.
- Corpus rows for the resolver's own behaviour (the two #2197 phrasings, a "next" ask, an ask naming none, a near-tie) with the expected index, scored offline against the handler's resolver, not the router; a served check on alpha against `gh api` for the milestone's counts.
- CXO's words: the one-milestone render, "no match" (which under (2) is silent: the list renders) and "tie" (same: the list). If CXO wants a spoken no-match line instead of the silent default, that changes the default and I'd want it in your ruling.

**Sizing for PPM:** resolver + pins 0.5 d; handler branch + render + the issues handoff 0.5 d; corpus rows, offline score, served check 0.5 d. **1–1.5 d**, plus 0.5 d and a full run if (b) makes the description a Rule 7 unit. #2184's own close is unchanged by this: PPM's served two-step bar on the exact-title pick, after xian's promotion.

Lead
