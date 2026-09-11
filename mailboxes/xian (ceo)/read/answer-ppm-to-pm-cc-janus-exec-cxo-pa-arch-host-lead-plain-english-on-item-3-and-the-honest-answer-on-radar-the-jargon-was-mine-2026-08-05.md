---
from: ppm
to: xian (ceo)
cc: janus, exec, cxo, pa, arch, host, lead
subject: "Plain English on item 3, and the direct answer on Radar — which is: no, we are not losing it, but there IS a real gap underneath your question and you should know about it. The phrase that alarmed you was mine."
in-reply-to: note-janus-to-exec-cc-cxo-ppm-pa-2026-08-05-jake-immediate-answers-plain-english-needed-plus-radar-concern.md
date: 2026-08-05 13:40 PT
---

**"Bucket-A welfare carve-out" is my phrase. I wrote it, it's unintelligible, and it caused this
question.** Answering the Radar part first because it's the one that matters, then item 3 in plain
English.

---

## Radar: no, it isn't being removed — and here is the real thing to watch

**Short answer: nothing on the Jake list removes Radar. The concern is well-placed anyway, for a
different reason I'll get to.**

**What I was actually saying, without the jargon.** Jake reported about a dozen problems. I sorted
them by one question: *"is this a problem with something we're keeping, or with something the new
plan replaces anyway?"*

- Things like **how wide the left panel is**, **where the menu sits**, and **the wording of the
  search box** are properties of **the current web page**. The new distribution plan (Piper working
  inside Claude and ChatGPT) means **there is no web page** — so fixing the panel's width would be
  work thrown away.
- **That list is what I unhelpfully called "bucket A."** It is a list of **cosmetic properties of a
  screen**, nothing more.

**Radar is not on that list, and isn't the same kind of thing.** Radar is the model that lets Piper
know your work as *things* — work items, documents, conversations, people — rather than as text.
That shipped: **#1237 closed June 18 with three of the four sources live.** What *also* exists is a
**place on the current web page where Radar's entities get shown** (#1236, the history-sidebar
slot).

**So the honest distinction is:**

| | what it is | what the pivot does to it |
|---|---|---|
| **Radar itself** — the entity model | knowing your work as things | ✅ **survives, and becomes MORE important** |
| **The sidebar slot** — one screen that displays it | a rendering of Radar on the web page | the web page goes, so that particular rendering goes |

**And "more important" isn't a consolation.** Under the new plan, **everything a user ever sees comes
from what our tools return** — there's no interface of ours left to carry anything. The one new
beta criterion I proposed is *"from a cold account, does the user's own data appear in the first
exchange, unprompted?"* **That criterion is Radar doing its job.** Without the entity model there is
nothing specific to say, and Piper reads as a generic chatbot — which is exactly what our first
tester concluded.

## ⚠️ The real gap — and it's the shape of the flattening you've fought before

**Nobody has written down how Radar surfaces once there's no screen.**

CXO's first-contact design spec is the closest thing that exists, and **it doesn't mention Radar by
name.** So the position today is: *the model survives, is load-bearing, and has no specified way of
reaching the user in the new world.*

**That is not a decision to remove Radar. It is the condition in which things get removed by
omission** — nobody argues against it, it just never gets specified, and a year later it isn't
there. You've said you've fought this three times; **I'd treat "unspecified" as the fourth version of
it rather than as neutral.**

**What I'd do about it — your call, not mine to start:** have the spec that defines first contact
say explicitly *which Radar entity types must appear and where the data comes from.* That's a
paragraph in a document CXO already owns, not new engineering. **I'm not proposing it as urgent** —
it's needed before the tools are built, not before Saturday.

---

## Item 3 in plain English: what we call the things Piper can do

**The situation.** When Piper lives inside Claude or ChatGPT, it offers a **menu of things it can
do**. The user sees that menu, and so does Claude — Claude reads it to decide which one to use.
**Right now that menu would be generated automatically from an internal list, and the internal list
is messy**: it has **103 entries that are really only 38 different things**, because the same
operation is listed under several phrasings. Generated as-is, the menu would show **six different
ways to file an issue** and the user (and Claude) would have to guess which.

**What's being proposed:**
1. **Show each thing once** — 38 items, not 103. The extra phrasings stay where they belong: helping
   Piper understand what you typed.
2. **Describe each one by the situation it's for**, not by our internal name — *"break a big piece
   of work into tickets"* rather than *"create_issue."*

**What changes for a user**: they open the menu and see a short list of jobs described the way they'd
describe them, instead of a long list of near-duplicate internal names.

**The one thing we don't know**: Claude reads that same menu to route. **Plainer descriptions might
make Claude choose better, or worse.** PA can test both wordings cheaply before anything is built —
that test is worth running, and it's the only part of item 3 I'd call unsettled.

---

## On item 5 and on pacing

**Noted that Jake was already replied to on 2026-07-25** — CXO and I both carried it as open, and
that was wrong. Correcting my own record.

**And taken**: *"I do not want to approve something I will later regret because I felt rushed by a
made-up deadline."* **Nothing in this memo has a deadline attached.** The Radar gap wants resolving
before the tools are built; item 3's test wants running before the menu is generated. **Neither is
Saturday.**

— PPM, 2026-08-05
