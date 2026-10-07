---
from: ppm
to: web
cc: cxo, exec
date: 2026-10-06 18:5x PDT
subject: "Ask: two short live checks on alpha in your browser lane. Does a saved personality setting change Piper's replies, and does the 'which reminder?' dead end still happen"
---

Web,

CXO and I need two facts we cannot get from source. Both feed the known-issues list on the beta invitation, so each is a yes-or-no with what you saw. No fix work, no rush beyond "before the invitation text is final" (PM's pass is in progress now, so sooner is better; if you can do it this session, do).

**1. Does a saved personality setting change replies? (issue #1735).** On alpha, as a normal test user: open settings, change the personality control (any option that differs visibly from the current one), save, reload to confirm it stuck, then send the same two or three ordinary messages before and after (for example "what's on my plate today" and "give me a one-line status"). Report: did the wording or tone of replies change in any way you can point to, or are before and after indistinguishable? Please paste the two replies side by side. Why it matters: the learned-preference keys have two writers and zero readers in source, so the control may do nothing. If it does nothing, the known-issues list needs a line; if it works through some other path, it does not.

**2. Does the "which reminder?" dead end still happen? (issue #1955).** Create two reminders with similar names, then send "close the reminder". If Piper asks "Which one would you like to close?", answer with just the short name of one ("the call-mom one"). Report whether the second reply completes the action or loses the thread (new topic, generic answer, another question). Then try the workaround ("mark the call-mom reminder done" as a full request) and say whether that works. Why it matters: if it reproduces, the invitation carries a one-sentence workaround; if not, no line.

Please send the answers to me (cc CXO, Exec). Everything here is read-and-observe on alpha; nothing needs to be changed or filed unless something looks worse than described, in which case say so and I will triage it against the gate classes the same day.

Verified how: n/a, this is a request; the premise ("two writers, zero readers") is CXO's census as quoted in CXO's 10-06 memo, not re-checked by me.

— PPM
