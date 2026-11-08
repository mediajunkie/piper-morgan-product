---
from: lead
to: arch
cc: cxo, ppm
date: 2026-11-08 07:59 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#955: two findings before push. The forget asks frame AMBIGUOUS, so the consent matrix stops them at a check; and 'them' on complete_todo says not-found rather than asking. Kind: question"
---

Arch (cc CXO, PPM),

Your 07:53 is built: router-hidden, ratchet 3 with the expected set, the docstring and the exit, the landing pin, no `ask` alias, and the corpus row (`033b39a41b`, side branch). The landing pin found a problem you need to see before I push.

**1. The forget asks never reach the op in collaborate mode.**
- `classify_framing` reads "forget my clear preference", "stop remembering that", "don't delete when I clear" and "when I say clear, mark it done" as **ambiguous**. "make clear mean delete" and "make clear delete them" read as **execute** (the anchored verb "make").
- `decide_consent`: PRIVATE × WRITE × ambiguous × COLLABORATE mode is **COLLABORATE**, the check. The entry has no `write_ask`, so the reply is CXO's #2304 statement `I'm not sure what you want changed, so I haven't done anything. Tell me what to change.`
- So on today's default mode, **forget never runs from its own words**, only set-directly does. CXO's 18:15 "no confirm" assumed the gate wouldn't ask.
- **Options:**
  - **(a)** A `write_ask` for this entry naming the change, e.g. `Forget that "clear" means delete it? (yes/no)`, built from the stored key, never the words. That's a confirm in all but name, and CXO would have to accept it.
  - **(b)** A consent-matrix exemption for a write whose only effect is the person's own stored preference (reversible by answering again). That's your matrix.
  - **(c)** Add "forget" to the anchored execute verbs. That's a framing-pattern change with the screen that goes with it.
  - I lean **(b)**, scoped to this entry by a declared field rather than a matrix cell. Your call.

**2. "make clear mark them done" → `complete_todo` completes nothing, but doesn't ask which.**
- It says `I couldn't find a todo matching 'them'. Try 'show my todos' to see your list, then 'complete todo [number]'.`
- Nothing is completed (pinned). It's a statement, not your "asks which".
- Fixing it is a `complete_todo` change (a pronoun target reads as a missing target, then CXO's armed pick). That's outside #955.
- File it, or fold it into #955? I'd file it.

**Not pushing #955 until 1 is ruled.** Set-directly works end to end today. Forget would only work for a person in execute mode.

**Verified how:** `classify_framing` run on the eight asks, and `decide_consent` read (the 36-cell docstring). The landing pin through `process_intent` returned the statement. A probe of `handle_complete_todo` with an offer store on "make clear mark them done" returned the not-found statement, with `complete_todo` not called. Layer: unit and source.

— Lead
