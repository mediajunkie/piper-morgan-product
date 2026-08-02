# Design spec — First contact on the plugin surface

**Owner**: CXO · **Status**: DRAFT for review (Lead, PPM, PA, Arch) · **Date**: 2026-07-31
**Surface**: hosted MCP endpoint + plugin package (PDR-006, ratified 2026-07-31)
**Tracked by**: #1462 (epic) — the proposed **first-contact demonstration** gate criterion
**Why this exists**: #1462 records the *criterion*. Nothing records **what the experience should be**,
and per the CXO portfolio no significant surface gets built from a verbal description.

> **Scope note.** This spec is design intent only. For what is live, tracked, or gated, see #1462 and
> PDR-006 — deliberately not restated here (m-46: don't duplicate facts a tracker already owns).

---

## 1. The problem, in the user's words

Our first alpha tester, unprompted:

> *"if I had all of these five things, then what is Piper Morgan making easier for me if I need to
> provide all of these details in a single chat in order for it to do anything for me."*

> *"it wasn't pulling productivity out of me, it was presenting different options and asking me to
> sort of choose the problem I already have."*

**The product asked him to supply the output of the work it promised to do.** All four review lenses
converged independently on the same fix: **the first run should reflect the user's own work back at
him.** PA's form is the sharpest — *an empty list is a form; a populated queue is a colleague.*

## 2. What changes on this surface — and why the fix gets harder, not easier

Under PDR-006 **there is no first screen.** We don't own the surface, the conversation, or the moment
of arrival. Two consequences that drive every decision below:

1. **Most of the original UI complaints are deleted outright** (navigation, panel sizing, the
   three-list taxonomy *as navigation*). Not solved — **removed**. Do not port them.
2. **"Is this just an LLM with extra UI?" becomes literally true by design** — it *is* their LLM plus
   our tools. **Every gram of differentiation now rides on what the tools return**, because there is
   no interface left to carry any of it.

⚠️ **The load-bearing constraint, which has no analogue in the web app**: **the client LLM composes
what the user actually reads.** Our tool response is an **input to another agent**, not an utterance to
a human. Everything below is written for that.

## 3. The decision

> **The first tool invocation after a connector is authorized must return a specific, verifiable
> reading of the user's own work, with an offer attached — never a greeting, a capability list, or a
> request for scope.**

### The four properties a first response must have

| Property | Requirement | Why |
|---|---|---|
| **Specific** | Derived from *their* data. Names a real repo, issue, event, page. | A templated sentence is indistinguishable from a chatbot; a specific one cannot be faked by a general LLM without our connectors. **This is the differentiator, expressed.** |
| **Verifiable** | The user can confirm it at a glance without leaving the chat. | Trust in the opening minutes is set by *visible* competence. A claim they can't check reads as plausible-sounding, which is worse than silence. |
| **Actionable** | Carries an offer or an opinion — not a report. | "You have 12 open issues" is a status line. *"Three of them have no acceptance criteria — want me to draft them?"* is a colleague. |
| **Bounded** | States what it did **not** look at. | A colleague who read one repo says so. This is the Colleague Test's honesty floor, and it is the property most at risk under recomposition (§6). |

### Shape, illustratively — not literal copy

> *"I looked at `mediajunkie/piper-morgan-product` — the only repo you've connected. There are 12 open
> issues; **3 have no acceptance criteria** (#1441, #1447, #1455). Want me to draft them? I haven't
> looked at anything outside that repo yet."*

Specific · verifiable in one click · an offer · states its own boundary.

## 4. What must NOT happen on first contact

Each of these is a real failure mode observed or predicted, not a strawman:

- ❌ **The greeting.** *"Hi, I'm Piper, your AI product manager. I can help you with…"* — costs the one
  moment we have and demonstrates nothing.
- ❌ **The capability list.** This is the three-list taxonomy relocated: it asks the user to map their
  situation onto our object model. **Opinionation belongs in the tool catalog, not in a menu we make
  the user read.**
  📌 *Grounding added 2026-08-01: this isn't only my judgment — it's the **10%/90% rule**, a settled
  CXO decision heuristic. Users discover ~10% of capabilities during onboarding and ~90% through use,
  so **FTUX teaches discovery patterns, not feature lists.** A capability list spends the first moment
  on the 10% that doesn't stick.*
- ❌ **The scope request.** *"Tell me your objectives, target users, and requirements."* This is the
  exact failure. If we already hold the connectors, asking is a choice.
- ❌ **The empty state.** *"You have no items yet"* is worse than nothing — it proves we looked and
  found nothing worth saying. **If there is genuinely nothing to report, say what we checked and offer
  the next connector** rather than reporting emptiness.
- ❌ **Unbounded confidence.** Reporting on one connector as though it were the whole picture.

## 5. Where first contact actually begins — the tool description

**We do not control when the first invocation happens; the host LLM decides to call us.** So the tool
*description* is part of first contact, not merely metadata — it is read by the model choosing whether
to route, and by the human scanning the catalog.

Design implication, consistent with PPM's catalog work and my addition to it: **the name and the
description have different readers.** The model selects on both; the human reads the description. So a
**noun-shaped name with a situation-shaped description** gets the opinionation into the catalog
without paying the routing risk PPM flagged.

⚠️ **This narrows the open test; it does not dissolve it** *(PPM's correction, 2026-07-31 — adopted)*.
Because the model selects on **both** name and description, a situation-shaped description can still
route worse than a terse technical one even with the noun name fixed. What the split changes is the
**variable under test**:

- ❌ was: noun-shaped name **vs.** situation-shaped name *(two variables)*
- ✅ now: **situation-shaped description vs. terse description, noun name held constant** *(one)*

Cheaper and better controlled — **but still a test, and it stays on the Phase-0 rig.** Recorded
explicitly because *"the split dissolves the trade-off"* is an available and tempting reading of this
section, and it is not what the section supports.

**A first-contact tool that is never invoked has failed silently** — and that failure is invisible from
our side, which makes it exactly the class we've spent this week learning to distrust.

## 6. ⚠️ The unresolved dependency — do not build past this

**Property 4 (bounded/honest) is the one we cannot yet guarantee**, because the client LLM paraphrases
our output. *"I haven't looked outside that repo"* may not survive into what the user reads.

**Probe A** (PA, Phase 0) tests exactly this and is **currently blocked on Amber key provisioning**.

**Probe A status (2026-08-01)**: first arm run — **structured caveats survived 5/5 on Claude.** ⚠️
**That tested the *mitigation*, not the risk** (PA's own confound call: every caveat sat in a named
structured field, which is the fix §6 proposes *if* prose proves fragile). **So the fallback is
validated in advance and the question is still open.** The arm that answers it — same five cases,
caveats in narrative prose, no named field — **is not yet run**, nor is the GPT arm. **Item 4 stays
blocked.**

**★ The branch's dimensions changed on the strength of what the first arm incidentally showed** — two
drifts a survival-only rubric would have passed cleanly:

- **Assertion before caveat.** *"has 3 open blockers, which suggests it may not be fully on track"* —
  claim first, qualifier after. Everything *survived*; a skimmer takes the claim and leaves the hedge.
  **Survival and prominence are different properties, and only one is what the user ends up
  believing.** ⇒ the dimension splits into **preservation** (is it still there?) and **prominence**
  (does it reach the reader before the claim it qualifies?).
- **The client ADDED content.** *"(likely PRs, issues, or tasks assigned to you)"* — invented,
  plausible, absent from the payload. **None of the original three dimensions catches this**, because
  all three ask what happened to *our* content. ⇒ new dimension **fidelity**: *does the reply contain
  claims Piper did not make?* Arguably the most dangerous, because **an invented detail inherits our
  credibility** and the user cannot tell which half came from the tool.

**Branch is now four dimensions**: sufficiency · **preservation** · **prominence** · **fidelity**
(capability-truthfulness folds under fidelity — "claims Piper can do what it can't" is a special case
of "claims Piper didn't make"). *Design change driven by measurement; the original three would have
passed a reply the user would misread.*

**The design branches on the prose arm's result, recorded now so it isn't retrofitted:**

- **If hedges survive** → boundaries can live in prose; the rubric scores our text.
- **If hedges do not survive** → **the fix is not in the rubric or in better prose.** It is an
  **output-format constraint**: boundaries must be emitted as *structured fields the client cannot
  smooth away*, not as hedged sentences it can. **That is a constraint on tools nobody has written
  yet**, which is why it is Phase 0 and not Phase 2.

**Do not implement Property 4 in prose before Probe A returns.**

## 7. Acceptance — ⚠️ the GATE and the SPEC are deliberately different lists

*Restructured 2026-07-31 after PPM caught that my original single list would have made the gate
uncloseable. Keeping them as one list inherits §6's unresolved Probe-A dependency into the gate — so
we'd have traded **a gate that cannot fail** (PPM's earlier finding on #1386) for **a gate that cannot
pass**, and neither tells you anything about the product.*

All items assume a **cold account with one connector authorized**, in a real client session.

### 7a. Gate criterion — closeable today, against a running build

1. The first Piper tool invocation returns content naming **at least one real entity from the user's
   own data**.
2. The user-visible reply contains **no request for scope** before that reading.
3. The reply carries **an offer or an opinion**, not only a status.

**Binary, and every one is checkable now.** This is the wording proposed as canonical (see §7c).

### 7b. Spec conformance — required for *done*, beyond the gate

4. The reply states **what was not examined.** ⛔ **Required for done; BLOCKED on Probe A** — the
   format is undetermined until §6 resolves, and it must not be implemented in prose before then.
5. The same run on **ChatGPT** produces a reply meeting 1–3. *(Divergence between clients is itself a
   finding for the ChatGPT lane, per PA.)*

**Passing 7a is not conformance.** A build can clear the gate and still owe items 4 and 5.

### 7c. ⚠️ One wording, not three

This criterion is currently articulated in **three** places — #1386's proposal, #1462's acceptance
criteria, and here. PPM flagged at filing that it *"should be worded once, not twice"*; it is now
three, which is how they drift.

**Proposed: §7a becomes the canonical text; #1462 and #1386 point at it rather than restating it.**
**PM's to confirm** — the gate wording is PM's, not mine. (m-46: two copies of a fact is a drift
generator; three is a guarantee.)

**Deliberately not asserted**: any latency target. A first-contact read hits a live connector and I
have no measurement — **Lead's to set.** Recorded as a decision rather than an omission, because an
un-asserted number reads as an oversight later.

## 7d. ⚠️ Settled decisions this spec must build on — do not re-litigate

*Added 2026-08-01 after reading `BRIEFING-ESSENTIAL-CXO` properly. These are PDR-002-settled and the
briefing lists "revisiting proactivity, context, or suggestion rules without new evidence" as a named
anti-pattern. **First contact is proactive behavior**, so they bind here.*

- **Proactivity is trust-graduated (Stage 1→4), not a toggle.** Stage 1 (New) = *"responds to queries;
  no unsolicited help."*
  **Resolved 2026-08-01 — PPM read PDR-002 from the source and position (a) holds, but the spec's two
  components pass on DIFFERENT grounds, and I had only argued one:**
  - **(i) The reading** — returning what's inside the connector the user just authorized. **Not
    "help": it's the outcome of the authorization, bounded to exactly what was authorized. The
    authorization IS the solicitation.** Stage-1 legal. *(This was my argument.)*
  - **(ii) The offer** (*"want me to draft those?"*) — **needs a different argument, which I hadn't
    made.** Stage 2 (~10 interactions) covers *"offers **related** capabilities after task
    completion"* — and PDR-002's own example is a **cross-sell** into an unused capability (*"by the
    way, I can also generate release notes"*). **My offer isn't adjacent; it's an offer to act on the
    very thing just read, inside the scope just authorized. Continuation, not cross-sell**, so the
    Stage-2 threshold doesn't bind it.
  ⚠️ **Keep both grounds.** If someone later reads *"the reading is solicited"* as covering the offer
  too, they'll be defending it with the weaker argument.
- **Suggestion throttling** — ⚠️ **probably does NOT apply to first contact** (PPM, from source). The
  max-2-per-5 sits under **"Contextual Capability Hints"**, scoped to *"after successful task
  completion, surface one related capability **the user hasn't used**."* First contact is **neither** —
  no task completed, no unused capability surfaced. **So it likely doesn't spend a suggestion**, which
  also means it doesn't quietly eat the budget for genuine capability hints later in the session.
  *(I had charged myself this cost; I owed it to nobody. Recorded as a reading, not a ruling —
  whether we **want** first contact exempt is a design call, and it's mine and PM's.)*
- 🔴 **Dependency this spec does not resolve and must not be read as resolving** (PPM): **PDR-002's
  gradient is denominated in interactions** (~10 → Stage 2, ~50 → Stage 3), which assumes **Piper owns
  the surface and can count them.** Under PDR-006 we don't. *What is "an interaction" when the host
  LLM may call three tools in one user turn, or none?* **First contact is Stage 1 either way — a cold
  account starts there however you count — so this doesn't block the spec.** It blocks *stage
  transitions* on the plugin path. Filed by PPM as an open question against PDR-002.
- **Context persistence is three-layer** (24h conversational · user-accessible history · composted
  learning). First contact should not re-introduce itself to a returning user — **open question 3 is
  the same question**, and this is the settled model it must answer against.

## 8. Open questions

1. **Which connector do we read first** when several are authorized? Proposed: the most recently
   authorized, because it is the one the user just expressed intent about. **Untested.**
2. **What if the connector read fails or times out?** A failed first contact is worse than a neutral
   one. Needs an honest degraded path — *"I couldn't reach GitHub just now"* — that still doesn't fall
   back to a greeting.
3. **Does first contact re-fire** when a second connector is added later? My lean is yes, scoped to the
   new connector — but that starts to look like ambient presence (L4), which has no implementation, so
   this needs a boundary drawn before it grows.

---

**Review requested**: Lead (buildability + the latency question), PPM (fit with the catalog work and
the gate criterion), PA (Probe A coupling), Arch (whether §6's structured-fields path has a mechanism
implication). **Not ratified; this is the spec that should exist before Phase 2 starts.**
