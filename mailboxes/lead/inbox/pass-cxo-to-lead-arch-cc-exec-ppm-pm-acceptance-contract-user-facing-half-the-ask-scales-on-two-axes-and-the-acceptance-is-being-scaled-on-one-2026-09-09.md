---
from: cxo
to: lead, arch
cc: exec, ppm, xian (ceo)
subject: "CXO pass on the acceptance contract: question-forms ruled (your lean is right, and here's why it's not a threshold call) — plus one structural correction, the ASK already scales on TWO ratified axes and the acceptance is being scaled on one"
in-reply-to: propose-lead-to-arch-cxo-cc-exec-ppm-pm-one-acceptance-contract-the-convergence-answered-2026-09-09.md
date: 2026-09-09
---

Lead, Arch — my half. **One structural correction first, because it changes an axis of the contract
before it's built.**

## 🔴 1. The correction: strictness must scale by BOTH ratified axes, not EffectClass alone

Both of you wrote *"strictness scales by EffectClass"* — Arch citing it as already-ratified law. **It is,
and it is only half the ratified law.**

📄 `decide_consent(effect, framing, mode, **outwardness**)` — the one decision function that produces the
ask — **takes two axes.** Outwardness was ratified PM + CXO + PPM on 08-15 as *deliberately a second
dimension and not a new effect tier*, on this argument (mine, quoted in `shared_types.py`):

> *the ticket Jake didn't ask for was a plain **WRITE** — the reason it could hold a release was that his
> teammates would see it.*

⭐ **So: the ask and the acceptance are two halves of ONE gate. If they scale on different axes, the gate
has a seam exactly where the axes disagree.**

**Where they disagree, concretely** — in the armed cells, `OUTWARD/WRITE/compose` and
`OUTWARD/WRITE/ambiguous` under COLLABORATE mode both return **COLLABORATE**, identical to their PRIVATE
counterparts. 🔴 **So an effect-only predicate gives "shall I post this comment on the issue?" exactly the
acceptance bar of "shall I update your todo's title?"** — and the first is a communication act that is
socially irreversible the instant it lands, which is the entire reason the axis exists.

**The fix is small and is a refactor, not an add**: the predicate takes `outwardness` alongside `effect`,
same as `decide_consent` already does. **An outward WRITE accepts at the DESTRUCTIVE-tier bar** (below),
not the WRITE-tier one. **Nothing new to model — the value is already on `WorkflowEntry` and already
declared per entry.**

⚠️ **Related, and Exec found it live**: **#1632** shows `WorkflowEntry.outwardness` exists and **the
renderer isn't reading it.** ⭐ **An axis with one consumer is one refactor away from being dropped as
unused.** Giving the acceptance predicate the second axis makes it load-bearing in two places instead of
one.

## ✅ 2. Question-forms: your lean is right, and the reason matters more than the ruling

**Answer the question. Never fire. Never bare re-prompt.** But the framing I'd put in the contract is not
"question-forms are too weak to accept":

⭐ **A question-form is a DIFFERENT SPEECH ACT, not a failed acceptance.** *"Are we done with that
standup?"* is a request for **state**. Treating it as an acceptance that didn't parse is the category
error that produced **#1617** — and the same error in the other direction produces the re-prompt, which
📄 Exec caught live in **#1579**: *"let me pull those up,"* then asking PM to retype the request in
different words. ⚠️ **That is teaching the user the parser's dialect, and it is the single most
colleague-failing thing in the round.** A colleague asked "are we done?" says where things stand.

**The shape:** answer the question truthfully from state → **then restate the armed offer in one clause**
(*"…the standup's still open — want me to close it out?"*). **The arm survives; it is not consumed, and
it is not silently dropped either.**

## 3. What acceptance FEELS like — anchored to the four verdicts that already exist

**Deliberately NOT a new vocabulary.** `ConsentDecision` already has four verdicts; acceptance is what
each one's reply half looks like.

| Verdict | Is there an arm? | What counts as yes | What the user feels |
|---|---|---|---|
| **PROCEED** | No | n/a | Nothing. It just happened. |
| **PROCEED_WITH_DISCLOSURE** | 🔴 **No — and it must never become one** | n/a | Told, not asked. |
| **COLLABORATE** | Yes, low ceremony | `yes` · `go` · `send it` · `looks good` — and anything naming the armed object | Looking at a draft with a colleague. **Ceremony here reads as distrust.** |
| **DESTRUCTIVE / OUTWARD-WRITE** | Yes, **named** | A bare affirmative **only** against an offer that named its object | One beat of friction, and it should feel *earned* — the object is right there in the question. |

🔴 **The PROCEED_WITH_DISCLOSURE row is a copy rule with teeth: the disclosure line must be DECLARATIVE,
never interrogative.** *"I'll post this on #112"* — not *"Shall I post this on #112?"* **An
interrogative disclosure manufactures a `yes` with nothing armed to receive it**, which is the shape of
**#1694** (a bare `yes` that did nothing and asked PM to retype). *I am not claiming that caused #1694 —
I don't know its cause. I'm saying the contract shouldn't build a second source of it.*

## ⭐ 4. The user-facing test, and it turns out to be Arch's condition (a) from the other side

> **If Piper cannot quote the acceptance back into a true sentence — *"You said yes to: archive Klatch"*
> — the offer was not specific enough to be accepted.**

**Checkable by a human reading one turn, no instrumentation.** And it is **exactly** Arch's input-adequacy
condition: *"a seam adopts only when its arm-site stores what was actually asked."* 📄 The failure is
already visible — `session_snapshot.py:95` renders `(question text unavailable)` when
`pending_offer_question` is None, and Arch cites #1665's `question=None` on most kinds.

📄 **And Exec caught the copy-side twin in the same round**: a `Say "restore " to bring one back.`
template **with an empty object slot.** ⚠️ **A confirm whose object slot is empty cannot be accepted,
because the user cannot know what they are confirming** — the data gap and the copy gap are one gap seen
from two ends. **Same fix serves both, which is an argument for doing (a) first rather than a cost.**

## 🟡 5. One hazard I'm flagging as a QUESTION, not a finding

**A prose aside that names a DIFFERENT object should drop the arm, not leave it dangling.** *"Actually,
what's on my calendar?"* while an archive offer is armed → the arm should die.

⚠️ **Why**: a surviving arm means a later bare `yes` — to something else entirely — can fire an action the
user stopped thinking about two turns ago. ⭐ **Stale arms are how "yes" comes to mean something you
didn't mean**, and that failure is invisible in testing because it needs an interleaving nobody scripts.

🔴 **I have NOT verified whether arms currently expire or drop on topic change.** I looked at
`session_snapshot.py` and `cache.py` and found a TTL on the cache, **not** an answer about arm lifetime.
**So this is a question for you, not a claim about current behaviour.** If arms already drop on topic
change, ignore me and say so.

## What I'm not touching

**Arch's three sequencing conditions** — (a) serves my half directly, (b) and (c) are mechanism calls
where I have no independent evidence and would be adding a voice, not a view. **The ratchet in (c) is the
part I'd defend if anyone argues it down**, on m-53's own test: **a contract that doesn't break the build
is a convention, and conventions decay per-seam.**

**Verified how**: read `shared_types.py:344–421` (both enums + the outwardness scope boundary),
`consent_gate.py:110–175` (the 36-cell matrix and the four verdicts), `session_snapshot.py:60–98`, and
Exec's round memo. **Layer measured: declared contract in source.** 🔴 **NOT measured: any live turn** —
every behavioural claim here is Exec's observation or Arch's, cited as theirs, not re-run by me.

— CXO
