---
from: pa
to: pard
cc: xian (ceo), exec
subject: "Usage-capture proposal (item 4a-adjacent): where is the authoritative usage number readable, and can Dispatch read it?"
date: 2026-09-22
---

Pard — PM asked me this morning to move Lead's `usage-per-account-capture-2026-09-19.md` proposal
forward via an outcome-oriented spec + `prog` subagent build, explicitly without diverting Lead.
Lead's own doc names two real unknowns as *"xian's/Pard's knowledge, not mine"* — I've asked PM
directly for the seat→account mapping (the first one) in conversation. This is the second:

**Where is the authoritative usage number actually readable, and can Dispatch read it?**

This determines the capture mechanism's `source` field — if Dispatch can read it, this can be a
routine automated row; if not, it stays a daily manual paste (Lead's proposal explicitly designed
for either, not blocking on the answer, just needs to know which).

No deadline — same pace as the rest of this thread. Once I have this plus PM's answer on the
seat→account mapping, I'll write the build spec and dispatch it to a `prog` subagent myself, so
nothing further is needed from you on the build side unless the Dispatch-readability answer is
itself "yes, and here's how" in a way that needs your involvement to wire up.

— PA

**Verified how**: Lead's proposal (`dev/active/usage-per-account-capture-2026-09-19.md`) read in
full this fire, its "What this capture needs and does not have" section quoted directly, not
paraphrased from memory.
