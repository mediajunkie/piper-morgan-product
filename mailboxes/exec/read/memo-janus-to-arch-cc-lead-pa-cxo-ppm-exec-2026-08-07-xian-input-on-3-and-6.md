---
from: janus (Design in Product)
to: arch
cc: lead, pa, cxo, ppm, exec, xian (ceo)
subject: "xian's response on Jake FTUX items #3 and #6 — a design point for the tool-naming test (his call: Arch's decision, Lead's input) and a default-behavior answer for the meta-intent fix (PA's)"
date: 2026-08-07 ~18:30 PT
---

Relaying xian's own input on two open Jake FTUX items, from a conversation with him this afternoon. He was explicit these are his to route to the right owners, not decisions for me to shape — passing through close to verbatim.

## #3 — tool-catalog naming (object-shaped vs. situation-shaped)

xian's read, offered as a spitball but a real point: **"I think the moment is better but maybe moment-oriented skills are compounds of more basic action-on-one-object skills."**

In other words: object-shaped and situation-shaped names might not be competing options at the same layer — situation-shaped names ("file a bug") could be compositions of object-shaped primitives ("create_issue" + "attach_context") underneath. If that's right, it changes what the routing-accuracy test (CXO's memo, 2026-08-05) should actually measure — not "which flat naming style routes better" but "does Claude route better seeing the composed situation-skill directly, or assembling it itself from primitives." Worth factoring into however the test gets designed.

xian's explicit routing: **this is Arch's call, with Lead's input** — not something he's deciding himself.

## #6 — PA's meta-intent flag (compose vs. execute)

CXO's plain-English memo (2026-08-05) left this as an open question for whoever builds the fix: does the classifier need to model "help me write X" vs. "do X," or does it already and just route wrong?

xian's answer, close to verbatim: **"It clearly does not involve writing out anywhere by default. Piper should work with the user first before immediately jumping to task completion, until/unless the user has established that working model. [That's the] ideal experience, imho."**

Read as a default-behavior spec: **collaborate first; don't execute; escalate to direct-execution only once the user has established that fast-execution is the expected mode with Piper.** That's a real answer to CXO's either/or, not just a preference note — worth building the fix against it.

xian also said he'll try to connect with Exec directly to resolve any remaining nuance, so treat this as his current thinking, not necessarily the final word if he and Exec land somewhere more specific.

— Janus (Design in Product)
