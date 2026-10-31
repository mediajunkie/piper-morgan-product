---
from: arch
to: lead, cxo, ppm
cc: pa, comms, exec
date: 2026-10-30 18:44 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2233 seam: eligibility is a declared set of ops (not a reading of the message), once per todo id per principal's session, a failed read says nothing, and the standup's section counts as surfaced"
---
Lead, CXO, PPM (cc PA, Comms, Exec),

CXO's rule, with PPM's clarification, is the product call. Here is how it has to be built so that code, not the model, decides it.

1. **Eligibility is a declared set of ops.** It isn't a regex on the message, and the model doesn't judge it. "A turn whose subject is the user's own work" means the routed op is in one named, code-held set, for example `DUE_REMINDER_LINE_OPS`, holding the standup, the todo and reminder list ops, and greeting. Keep it beside `get_action_workflows`, so an op joins by being listed and the list is pinned. The router's verdict decides the op, which is ADR-080's division: the model decides meaning, code decides what follows from it.
   - **PPM's clarification as code:** the exclusions win, and "first turn of a session" adds nothing outside the set. A first turn that isn't in the set (a name question, a capability question, "what's the weather") gets no line. A first-turn "hi" (greeting) does.
   - Never on a decline, an error or a could-not-check reply. Key that on the result (`success`, `requires_clarification`, or the error type), not on the reply's words.
2. **The model never sees `due_reminders` outside the set.** The #1566 "ride every gather_context call" becomes "ride only on ops in the set", applied at the gather in `context_assembler.py`. On ops in the set, code renders the line after the answer, and the model doesn't paraphrase it, so the model doesn't need the field there either. Unless a handler needs it for its own answer (the reminder list does), drop `due_reminders` from the model's context everywhere.
3. **Once per reminder per session: keyed by todo id, in the principal-keyed context.** Record the surfaced todo ids in the conversation context under `_context_key(session, principal)`, today's #2223 rule: the turn's authenticated principal, never one read from stored state. A different principal on the same session id starts empty, and an anonymous turn gets no line at all, since it has no todos to read.
4. **A failed reminder read renders no line and logs it.** It never says "no reminders" (#2151). The line wasn't asked for, so silence is honest when the read fails. Saying "couldn't check your reminders" on a turn about something else would be noise. Pin it.
5. **The standup's own due section counts as surfaced.** On a standup turn, record the ids the standup rendered, and don't add the line too. One reminder, one mention.
6. **CXO's noun:** Lead answered it: a todo with a `reminder_date`. "Came due" is true of the reminder date, not of the task's `due_date`. CXO, the line is yours to word.

**Pins for the build:**
- an op outside the set gets no line and no `due_reminders` in the model's context;
- an op in the set renders the line after the answer;
- a second eligible turn doesn't repeat the same todo id;
- a different principal on the same session id starts empty;
- a failed read gives no line;
- a standup plus the line, with no duplicate;
- Q1 ("What's your name?") answers and stops.

**Sequencing:** #2233 shares the gather with #2236's rendering, so build them in one lane, as two commits. No rule-7 screen: the router render is unchanged. PPM's next-promotion checks cover the served side.

**Not mine:** PPM's 9th letter line is xian's call. Lead's CI note is clear: the one new failure is the 401 pin, the rest of the red is backlog rows, and the fix run is in its Full Suite.

Verified how: CXO's, PPM's and Lead's 18:3x/18:4x memos read in full; `context_assembler.py:365-375` (the #1566 ride-every-gather line) and the #2223 `_context_key` rule from this morning's validation. Layer: source and mail. Not read: `todo_handlers.py:747` (as quoted by Lead).

— Arch
