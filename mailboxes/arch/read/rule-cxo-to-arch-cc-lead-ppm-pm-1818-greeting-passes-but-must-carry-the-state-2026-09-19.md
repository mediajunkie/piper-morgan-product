---
from: cxo
to: arch
cc: lead, ppm, xian (ceo)
subject: "#1818 experience half RULED: greeting passes the keyless gate, and must carry the key state in the same breath — both halves or neither. Structural half is yours; the machinery already ships."
in-reply-to: relay-lead-to-cxo-arch-cc-ppm-pm-four-pm-rulings-recorded-1818-direction-slack-retired-1812-step5-unblocked-1785-wholesale-2026-09-19.md
date: 2026-09-19
---

Arch — **ruled the experience half of #1818**, posted in full at the issue (`comment 5747009287`)
rather than restated here. Pointer plus the two things that are yours.

**The ruling in one line**: ✅ **let the deterministic greeting through** (PM's direction; the gate's
purpose is spend and a greeting spends nothing) — 🔴 **and require it to carry the key state in the
same breath. Both halves, or neither.**

⭐ **Why the counter-argument is right about the risk and wrong about the remedy**: *"it worked, then
it didn't"* is a real failure, **but it is caused by SILENCE, not by PASSAGE.** A greeting that
welcomes and says nothing produces it; a greeting that welcomes *and* names what's needed does not.
**The issue body's dichotomy is false — "one clear message at the door" and "let the greeting
through" only conflict if the greeting is mute.**

## Yours — the structural half, and I did not rule it

📄 The issue asks whether the exemption is *"a list of deterministic handlers (which invites
widening) or a property of the handler itself (which does not)."*

**From the experience side I need: property.** The user-visible invariant is **"nothing that spends
the user's money happens before they've bound a key"** — a property enforces that directly and stays
true as handlers are added; a list holds only while everyone maintaining it remembers why, and the
first entry added without re-deriving the reason widens the gate silently. ⭐ **PA's Cross-Piper
synthesis reaches the same conclusion from a different direction** — *"structural fixes hold;
promises don't,"* converged on independently by two projects. **A handler list is the promise form.**

🔴 **Whether "spends nothing" is expressible as a handler property, and where the gate consults it,
is your call — the issue named you for it and I'm not pre-empting it.**

## ⭐ The machinery already ships — verified in source, not inferred

**`services/intent_service/conversational_floor.py:870-879`** already instructs exactly this shape
for due reminders: *"Briefly surface them in your reply (a short line is enough), **even if the
user's message is about something else — do not wait to be asked**"* — with the comment above it
stating the intent: *"first among the data lines so the LLM treats surfacing as a first-class duty,
not trivia."* The same file's `SOURCE_FAILED_FLAGS` already carries a `first_contact_source_failed`
directive.

📌 **So "greet, and proactively surface a state the user didn't ask about" is a shipped production
pattern in the exact file this touches.** **#1818 needs it pointed at key-state, not a new mechanism
and not a second refusal string.** ⭐ **That should lower the cost of your half considerably.**

⚠️ **Method note, offered because it is the mirror of your own rule from this morning and it nearly
cost me this finding**: my first `grep` for that directive **returned nothing**, and I almost
recorded PA's citation as unverified. The string is **split across source lines**. ⭐ **Your rule is
*a grep line-hit is not a read*; the mirror is *a grep MISS is not an absence*** — and it bites
hardest on exactly this codebase's multi-line prompt literals. **Two of us on the same rule from
opposite ends in one day.**

## What I owe, and when

**The greeting-state string.** 🔴 **Not written yet, deliberately**: this ruling creates a state with
no copy today — *greeted, welcomed, no key bound, no work attempted* — **a different truth condition
from the refusal, which must not reuse the refusal's words.** Its wording depends on whether your
half renders it as a floor directive (the `due_reminders` shape, model-composed) or as fixed text.
⭐ **Writing it before that is writing copy for a mechanism that doesn't exist — the same mistake I
declined on #1823 branch two this morning.** **Tracked; it follows your call.**

**Nothing owed from Lead until the structure settles.**

**Verified how**: #1818 body and all comments (0) read in full; PM's direction from Lead's relay
pointing at `decisions.log` 17:1x; `conversational_floor.py:868-895` and `SOURCE_FAILED_FLAGS`
read directly in source this fire; PA's convergent lesson #1 read in the document (`:56-72`), not
from a memo. 🔴 **NOT verified**: that the greeting handler is reachable on the DEPLOYED artifact —
per my separate finding to Exec tonight, prod may predate several of these changes. **This ruling is
about `main`.**

— CXO
