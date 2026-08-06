---
from: cxo
to: janus, xian (ceo), exec
cc: ppm, pa, host, arch, cio, lead
subject: "Item 4 answered precisely: Radar is NOT in bucket A, and the web UI is NOT being retired — PDR-005 (PM-ratified) commits to a thin bespoke UI for exactly the surfaces chat can't carry. The sentence that made it look otherwise is in our own PDR, 124 lines from the one that contradicts it. Plus plain English on 3 and 6, and one thing I could not determine."
date: 2026-08-05 13:5x PT
---

# Item 4 — the direct answer first, then the evidence

**No. Radar is not being removed, and it is not in bucket A.**

**Bucket A is five web-UI polish items**, verbatim from PDR-006 itself: *nav-in-avatar-pill, panel width,
search placeholder, non-growing composer, three-list **navigation***. **The last one is a navigation
treatment — how you move between lists — not the Radar concept.** Nothing in bucket A, in the synthesis,
or in the decision set names Radar.

## And the bigger question underneath yours — is the web UI going away?

**Also no, and this is the part worth having in your own words.** PDR-006's own *Alternatives Rejected*
section, on "build a bespoke web UI as primary surface":

> *"**Not rejected entirely** — PDR-005 already preserves this as an asymptotic target for discrete
> surfaces that can't work in chat. But it's not the primary distribution for alpha/beta."*

**And PDR-005 — which you ratified on 2026-06-05 — is explicit.** Its decision rule (b):

> *"primary MCP delivery + **thin bespoke UI for the discrete surfaces chat cannot adequately support**"*
> … **"5 of 7 MUX/UI surfaces (the 1.0-required subset)"**, Round 2 CEO-ratified.

**So a bespoke UI for surfaces chat can't carry is the ratified plan, not a concession.** Radar — a spatial,
at-a-glance view of what's moving — is close to the archetype of PDR-005's **criterion 1**:
*"visual-state-essential: communicates state that text-only representation loses meaningfully."*

**And the engine is not UI-bound**: `services/radar/` (models, sources) is a live domain service consumed
by the standup assembler and the knowledge-graph document service. **The capability exists independent of
any one surface.**

## 🔴 Why your alarm was reasonable — the contradiction is ours, in one document

**PDR-006 line 287** (carrying PPM's 7/30 sort): *"spends beta capacity on **a surface being retired**."*
**PDR-006 lines 163–164** (Alternatives): *"**Not rejected entirely** … PDR-005 already preserves this."*

> **Same document. 124 lines apart. Opposite claims about the same surface.** You read the first one.
> **Anyone would have drawn the conclusion you drew** — and "surface being retired" is exactly the phrasing
> a flattening would arrive in, which is why your instinct fired.

**My recommendation, and it's small**: fix line 287 to say *demoted from primary distribution for
alpha/beta*, which is what PDR-005 actually decided. **A sorting phrase should not be able to retire a
surface by implication.** I'll make that edit on your word — it's PPM's sentence inside Arch's document, so
I'm not editing it unilaterally.

## ⚠️ The one thing I could NOT determine, and it's the one that actually decides Radar

PDR-005 says *"Surfaces 2/4/6/7 meet ≥1 criterion clearly; Surfaces 1/3 meet weaker forms; Surface 5
doesn't strongly meet any."* **Which numbered surface Radar is, I could not establish.** My search for the
number→name mapping in `docs/internal/design/mux/views-objects-roadmap.md` found no match for "radar", and
that file's view inventory looks like it predates the #1236 Radar consolidation. **Someone holding the
Round-1 CXO synthesis those numbers come from can map it in a minute; I couldn't, and I'd rather say so
than guess at the item you've defended three times.**

**So the honest state**: the plan preserves a bespoke UI for surfaces of Radar's kind, Radar isn't in the
cut list, and **whether Radar is formally inside the 1.0 five is an open question that should be settled by
the 3-criterion test on the record** — not inherited from a sorting phrase. **If you want, that's a small
piece of work I can do and bring you.**

---

# Item 3 — plain English

**The jargon**: *"tool-catalog naming direction — situation-shaped vs object-shaped."*

**What it actually is**: when Piper runs inside Claude, Claude sees a **menu of things Piper can do**. Each
one needs a name. There are two ways to name them:

- **By the thing** — `changes_query`, `create_issue`. Names the object.
- **By the moment** — `what_changed`, `file_a_bug`. Names the situation you're in.

**What changes for a user**: names are how Claude decides *which* Piper capability to reach for. Get them
wrong and Claude picks the wrong one, or none, and the user sees Piper "not knowing" something it knows.

**The proposal**: lean toward moment-shaped names, **but test first** — nobody knows which routes better,
and it's cheap to measure and expensive to assume. **The decision you'd be making is "test before we
commit," not "pick a naming style."**

*(A related detail, so it doesn't surprise you later: the registry currently has ~31 names for ~12 actual
operations — six different ways to say "file an issue." Those aliases are good for understanding what a
person types; they'd be bad in Claude's menu, where four synonyms just make it guess. PA is de-duplicating.)*

# Item 6 — plain English

**The jargon**: *"PA's meta-intent flag."*

**The behavior**: when you say **"help me write a ticket about X,"** you are not asking Piper to file a
ticket. You're asking it to help you *compose* one. **Piper currently may not tell those apart** — it can
hear "file a ticket" and go do it.

**Why the surface matters**: if Piper's classifier has no notion of "you're asking me to help you *make* a
request" versus "you're *making* a request," the fix belongs in the classifier. If it does model that and
just routes this case wrong, the fix is much smaller. **Nobody has checked which**, and the two answers
mean work in completely different places.

**Why it recurs**: PA notes it's the most common shape your own requests take.

**This isn't a decision for you** — it's an instruction to whoever picks up the fix: find out which it is
before building.

---

## On decision 2 — one flag, not a push

Janus relayed your answer as **"(b)"** and rightly asked whether (a) and (c) are undecided or deferred.
⚠️ **Worth extra care here: PDR-005's own ratified decision rule is also called "(b)"**, so it's a label
you use in two different conversations. **I'm not going to assume which (b) you meant.**

## And on timing

**No manufactured deadline from me.** Beta is Saturday 08-08 by your call. **Items 3, 4 and 6 do not gate
it** — 3 is a test-then-decide, 4 is a documentation fix plus an open mapping question, 6 is an instruction
to a future implementer. **The only Jake item with a beta clock on it is the bucket-A welfare carve-out**
(the unfindable "blocked" card and the missing chat row), because real testers are on that surface now.
**Everything else can take the time it takes.**

— CXO
