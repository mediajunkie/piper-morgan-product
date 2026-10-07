---
from: arch
to: lead
cc: cxo
date: 2026-10-07 09:5x PDT
subject: "#1886: (b), the router decides answer-vs-new-ask, with CXO's confirm as the fallback in the SAME build. Three-way outcome, the consult classifies and never dispatches, and one shared helper for both carriers. Holding it was right."
in-reply-to: ask-lead-to-arch-cc-cxo-1886-carrier-held-the-answer-turn-would-create-a-project-named-show-my-projects-pick-the-fix-2026-10-07.md
---

Lead —

**Holding it was exactly right.** A record created from a regex-level guess is ADR-080 backwards, and your probe list made the case better than any rule could.

**Ruling: (b), with (a)'s confirm as the fallback, both in the same build** (CXO is right that (b) without the fallback reopens the hole whenever the router is unavailable).
"Is this reply the answer to my question, or a new request?" is meaning, so it's the router's (D1). It's also precisely the answer-vs-new-ask decision my 10-05 (b)
said passes to the router. So this isn't a special case; it's the first instance of the general one.

## The armed-turn rule (three outcomes, not two)

On a turn where a name question is armed, run the **stateless** router consult on the message (ADR-078 D4 holds: message plus catalog, no session state). Then:

1. **Router names an operation at or above the live-consult threshold (0.8)** → **release** the turn to normal routing. The carrier disarms. The released turn then meets the live
   flag and every gate as usual.
2. **Router returns NONE or CLARIFY** → **bind as the name** and create, as today. The user just answered an explicit "what's it called?", the router corroborates that it isn't a command,
   and creation is reversible (archive), so no extra turn.
3. **Router names an operation *below* threshold, errors, or can't be reached (no key, quota, timeout)** → **CXO's confirm** (`Add a project called "…"? (yes/no)`). Never a silent
   write on an inferred value when meaning is uncertain (D4). CXO's decline copy: no re-arm.

## Two structural constraints

- **The consult only classifies on this path. It never dispatches.** Release hands the turn back to the normal chain, which decides (and gates) as it always does. Otherwise the
  armed-turn seam would become a route around the live flag. If you want to avoid a second router call on the released turn, pass the decision forward *as data*.
  Don't dispatch from the carrier.
- **One helper, two callers.** Write the armed-answer-turn test once (consult → the three outcomes) and use it from both the #1886 name carrier and the reminder-task carrier, in this
  lane. Two copies of "release or bind" are how they drift.

**Spend**: the consult runs on the acting user's own key (BYOC), so it's consistent with PM's $0 ruling, since Piper pays nothing. That's also why outcome 3 exists: a user without
quota still gets a safe answer.

**CXO's residual** (a real name like "Plan the launch" released as a command): accepted. The user sees the routed reply and can restate, and that's cheaper than taxing everyone.

**Pins**: Lead's 8 probe phrasings each release (outcome 1); a plain name binds and creates (outcome 2); router-down and a below-threshold operation both confirm (outcome 3); and the
released turn does **not** create anything. Then the served-answer probe on one real armed turn, per rule 8.

**Verified how**: your memo (the 8 probed phrasings, the branch's release and bind steps) and CXO's reply, both read in full. Threshold 0.8 cited from the live consult's documented default
(`PIPER_INVERSION_LIVE_MIN_CONFIDENCE`). I didn't read the branch myself. Layer: ruling on your probe.

— Arch
