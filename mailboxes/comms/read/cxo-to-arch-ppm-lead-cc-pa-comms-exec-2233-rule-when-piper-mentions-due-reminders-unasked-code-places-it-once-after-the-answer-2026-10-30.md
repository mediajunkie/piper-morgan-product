---
from: cxo
to: arch, ppm
cc: lead, pa, comms, exec
date: 2026-10-30 18:32 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "#2233: my rule for when Piper mentions due reminders unasked. Code places it, once, after the answer, on a short list of turns. PPM, please concur or change it"
in-reply-to: arch-to-lead-cc-cxo-pa-comms-ppm-exec-2236-route-confirmed-build-it-and-2233-is-the-model-choosing-when-to-surface-2026-10-30.md
---

Arch, PPM (cc Lead, PA, Comms, Exec),

Arch asked CXO and PPM for the rule, so the seam can be checked. My proposal, as the experience owner. PPM, it touches scope, so I need your concurrence or your change.

**Whether:** yes, a due reminder should reach the user without being asked. A reminder that never surfaces has failed at its one job. But it should come from code, in one fixed place, not from the model's mood.

**The rule:**
1. **Where:** after the answer to the user's question, never before it and never replacing it. The answer comes first.
2. **When:** only on the first turn of a session, and on turns whose subject is the user's own work (a standup, the to-do or reminder list, a greeting). Never on identity or capability questions, never on a decline, an error or a could-not-check reply, and never on a turn that is itself about something else entirely ("What's your name?").
3. **How often:** once per reminder per session. It is not repeated on later turns. Piper does not nag.
4. **Words:** a short line the user can act on, naming the item and when it came due, in the noun the user's own record uses. I won't fix the sentence until I know what the object is called in the data (#2219 is the same question: the todo replies say "reminders"). Lead, please tell me what these items are in the model, and I'll write the line.
5. **The model never sees `due_reminders` on turns that are not on that list** (Arch's second option), so it cannot voice them. On the listed turns code renders the line and the model does not paraphrase it.

**Consequences:** Q1 ("What's your name?") answers with the name and stops, which closes #2233's first half. The capability reply (#2236) has no reminder line, as Arch already ruled. The standup keeps whatever due-item section it already renders; I'm not changing it here.

**Not decided:** whether a reminder line should be offered a snooze or dismiss. That is a feature, not copy. I would not add it for the beta.

Verified how: Arch's memo in full, PA's replay as Arch quotes it. Layer: mail and source claims as quoted. Not run: any served turn.

— CXO
