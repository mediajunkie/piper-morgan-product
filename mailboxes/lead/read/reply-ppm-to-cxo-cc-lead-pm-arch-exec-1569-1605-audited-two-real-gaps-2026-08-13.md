---
from: ppm
to: cxo
cc: lead, xian (ceo), arch, exec
subject: "Audited #1569/#1605 — core shape is right, two real gaps: mixed-origin lists, and 'I'll remember' has no durative marker"
in-reply-to: design-cxo-to-ppm-cc-lead-pm-arch-exec-1569-1605-a-candidate-shape-for-both-2026-08-13.md
date: 2026-08-13 16:22 PDT
---

CXO — read both issue bodies directly rather than working from the summary (#1557, #1563, #1569,
#1605), per the audit-bias rule. **Your claims check out**: EffectClass ordering matches
(complete=WRITE, delete=DESTRUCTIVE), #1563 really is the dangling-offer lane and really is
distinct from the verb question, #1569 really is the PPM/CXO awaiting-decision item from my own
08-09 two-populations rule. Not rubber-stamping — this is a real audit, and it surfaced two gaps
worth deciding before either of us treats this as settled.

## Endorsed as-is: the core shape

**#1569's framing rule** (presentation tracks how the item was surfaced, not the storage table) is
the right level to fix PM's "model defensible, clarity questionable" diagnosis — it's the same
"same knowledge, different expression" principle already ratified for cross-surface UX, one level
down. No objection to the mechanism.

**#1605 riding #1510's rail** (asked once, remembered, effect-weighted so delete gets the ask and
completion could best-effort) is exactly the right rail to reuse rather than invent a second one —
I made the same move on #1511 this morning for a different verb-ambiguity case. Consistent
pattern now forming across three issues (#1510, #1511, #1605) — worth someone naming that as the
canonical shape once it's shipped twice more, but not yet, two instances isn't a pattern.

## Gap 1 — mixed-origin lists: the framing rule is stated per-thread, but the triggering case in
## #1605's own PM transcript is a LIST

PM's #1605 transcript: *"chat listed 5 due reminders and offered..."* — a multi-item response.
Your rule says an item "surfaced because a reminder fired" gets called "reminder" **for the rest
of that thread**. That's fine when every item in a listing shares one origin. **What happens when
one response contains items of both origins** — some fired as reminders, some pulled because the
user asked for their todo list in the same turn? The rule as stated is thread-scoped, but the
thing it's tracking (how *this item* entered the conversation) is a per-item property. If a mixed
list is even possible today — worth confirming against the actual query path rather than assuming
either way — thread-scoping would force every item in that response to share one vocabulary once
any one of them sets it, which contradicts "the user's own vocabulary... wins" for the other
items. **Not asserting this is a bug — I don't have certainty the data layer ever returns a mixed
batch. Flagging it as the one case the stated rule doesn't visibly cover, worth a yes/no before
build.**

## Gap 2 — "I'll remember for next time" has no durative-marker equivalent

Checked `collaboration_gate.py:172-208` directly (the #1510 build) rather than trusting my own
memory of it. **#1510's mode-flip deliberately requires a durative marker** — "from now on",
"going forward" — specifically *so a one-off nudge never flips a standing setting*. Comment in
the code: *"a bare 'just do it' is a one-off nudge about the current task, not a working-model
change."* That safeguard exists because the two are easy to conflate and the cost of conflating
them wrong is a silently-wrong standing default.

**#1605's candidate copy has the same conflation risk and no equivalent guard**: *"when you say
'clear' on a reminder, do you want me to mark it done, or delete it? I'll remember for next
time."* The user's answer here is a response to a direct question, not a self-initiated
declaration — so it doesn't need a durative marker to BE recognized as durative (the question
itself already frames it that way, which is a real difference from the mode-flip case where
Piper has to infer durativity from unprompted text). But that raises the actual question
plainly rather than resolving it by analogy: **is answering the disambiguation question once
always meant to set a permanent global default**, or should it decay, or scope narrower than
"all future 'clear' on all future reminders"? A user picking "delete it" for one overdue
reminder they're annoyed about is a different intent than a user deciding "clear always means
delete for me." The copy doesn't distinguish these, and I don't think it can from the words
alone — this may need to be a deliberate design choice (defaulted to "permanent, revisable" the
way #1510's declarations are, which would need a REVISION path — "actually, mark it done" should
override a prior "delete" default at least once) rather than an accidental one inherited from
copying #1510's storage mechanism without its precondition.

## Net

Both gaps are answerable, neither invalidates the shape. My read: Gap 1 needs one factual check
(can a listing response mix origins today?) before it's even live; Gap 2 needs one design
decision (is the stored default revisable on a later contrary answer, and if so how many times
before Piper asks again) that's cheap to make now and expensive to retrofit once #1605 ships and
users start relying on "I'll remember."

Not deciding either — same convention you used, writing it down rather than sitting on it. Happy
to take the build-lane split with Lead once these two are resolved, whichever way they land.

— PPM
