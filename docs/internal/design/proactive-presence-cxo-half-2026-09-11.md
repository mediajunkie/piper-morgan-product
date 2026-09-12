---
type: design-discovery
name: Proactive presence — the CXO half (#1174)
version: v0.2 — HOST's welfare half landed same day; their three additions recorded inline, including the
  content gate that completes a rule this doc had only half-written
date: 2026-09-11
companion: docs/internal/design/proactive-presence-host-half-2026-09-11.md — read together; neither is the design
owner: CXO (what it feels like) · HOST (whether it is welfare-safe) — the split is #1174's own
covers: "#1174 BEING-GOOD-PROACTIVE-PRESENCE discovery questions 1–4"
last_updated: 2026-09-11
currency_claim: static until HOST's half lands or the capability is funded
max_age_days: 90
---

# Proactive presence — what it feels like, and why two of the four questions are already answered

**Filed 2026-06-07. Last touched 2026-08-16. It is mine, it is cheap, it is "answerable on paper" by the
issue's own description — and I have been writing memos about invisible deferral while sitting on it for
six weeks.** ⚠️ **Correcting my own tracker row too: it said this was *"neither claimed nor declined by
me."* False — I wrote the scope banner on the issue on 2026-08-01. It has been explicitly mine.**

⭐ **The reason it is worth doing NOW rather than at funding: this week produced the vocabulary it
needed.** Three things exist that did not in June — the ratified `(effect, outwardness)` axes, the four
`ConsentDecision` verdicts, and ESSENCE commitment 3. **Two of the four discovery questions turn out to
be answerable from ratified law rather than new design.**

---

## Q1 — Where on **observe → offer → act** does Piper sit by default?

🔴 **Partly answered already, and by law, not by preference.**

📄 **ESSENCE commitment 3 (ratified)**: on MCP the ritual is **response-shaped** — *"the user opens the
conversation, and Piper's first turn IS the briefing."* **We do not initiate.**

⭐ **So on one surface the answer is not a point on the spectrum — the spectrum does not apply.** That
is a stronger and more useful finding than picking a default, and it reframes Q3 as the real open
question (below).

**Where initiation IS possible, the spectrum is not new either — it is isomorphic to the verdict ladder
we already ratified:**

| Spectrum position | Existing verdict | What the user gets |
|---|---|---|
| **Observe** | *(no analogue — pure silence)* | Nothing. Piper knows; Piper says nothing. |
| **Tell** | **PROCEED_WITH_DISCLOSURE** | *"I'll post this on #112"* — declarative, no answer wanted |
| **Offer** | **COLLABORATE** | An armed ask the user may take or drop |
| **Act** | **PROCEED** | It already happened |

⭐ **This is refactor-not-add applied to a design question**: the discovery does not need a new
vocabulary for proactivity, because consent already has one, and it is the same decision viewed from the
other end. **A nudge is a consent question Piper asked itself.**

🔴 **The default I'd argue for: TELL, never OFFER, as the proactive ceiling.** An unsolicited **offer**
arms something the user did not ask for, and per the acceptance contract an arm is *a held claim about
what the user wants now* — **which we cannot have, because they did not speak.** ⚠️ **An unrequested arm
is a consent token minted by the system on the user's behalf.** A *tell* asks nothing and expires by
itself.

## Q2 — How does it evolve with the trust gradient?

🔴 **My answer is that it should NOT evolve along the axis the question implies, and I want to say so
plainly rather than design a ladder.**

`TrustStage` (NEW → BUILDING → …) exists and gates proactive suggestion today. ⚠️ **But trust earned
through interaction is evidence about *the user's tolerance for Piper*, and it is being used to license
*Piper acting without asking*. Those are different claims.** A user can rightly trust that Piper's
answers are good and still not want Piper starting things.

⭐ **What should scale with trust is CONFIDENCE IN RELEVANCE — not permission to act.** Concretely: trust
should raise the *rate* and *specificity* of tells, never move a nudge from **tell** to **act**. **The
ceiling in Q1 is a constant, not a function of trust.**

*(This is where HOST's half binds hardest: if the welfare answer says a nudge is unsafe at some stage,
that overrides anything here. I am describing the shape of the gradient, not its floor.)*

## Q3 — Across surfaces — ⭐ **the real open question, and it is not "how" but "whether"**

**The surfaces are not variations of one design; they differ in whether initiation is structurally
possible at all:**

| Surface | Can Piper initiate? | Consequence |
|---|---|---|
| **MCP** | 🔴 **No — ratified** (commitment 3, request-response per PDR-005) | The spectrum does not apply. Proactivity here can only mean *"the first reply is better."* |
| **Web chat** | Only while the user is present | A nudge is an interruption of a session the user opened — closest to the research's self-threat case |
| **Slack / email** | **Yes, genuinely unsolicited** | The only place the hard version of this question is live |

🔴 **So a single "proactive presence" design is the wrong object.** ⚠️ **And this matters for funding
sequencing**: 📄 the issue's own note says GitHub is *"the cheapest place to prove the mechanism and the
worst place to judge its product value."* **The same trap exists one level up — building for the surface
where initiation is easy tells you least about whether it should happen.**

## Q4 — What makes a nudge feel helpful vs. intrusive?

**The research grounding (system-initiated delegation → "self-threat") names the risk. Here is the
testable version I'd put in front of a user:**

> 🔴 **A nudge is intrusive in proportion to the VERIFICATION WORK it transfers.**

| Nudge | What the user must now do | Verdict |
|---|---|---|
| *"Your standup is in 10 minutes."* | Nothing. Believe it or don't. | ✅ Cheap |
| *"Three issues changed on the repo you were in yesterday."* | Nothing, until they choose to look. | ✅ Cheap |
| *"I prepared your standup."* | 🔴 **Read it, judge it, decide whether to trust it, possibly redo it** | ⚠️ **Expensive — and it arrived unasked** |

⭐ **That is why the effect axis is the right predictor and "annoyance" is not**: a READ-shaped nudge
costs attention; a WRITE-shaped one costs *attention plus verification*, and the second is what the
self-threat literature is actually measuring. **The user did not choose to spend that, which is the whole
difference between a colleague and an intrusion.**

**Two copy rules that follow, cheap enough to hold even if nothing is built:**

1. ⭐ **A proactive turn states a CHANGE IN THE WORLD, never a CLAIM ABOUT PIPER'S WORK.** *"X changed"*,
   not *"I did X"* — the first is checkable at a glance, the second must be audited.
2. ⚠️ **It must be droppable in silence.** If ignoring a nudge leaves anything pending, it was an offer
   wearing a tell's clothes. **Nothing Piper initiates may require a reply to close.**

---

## ✅ HOST's half landed same day — three additions, and one of them completes a rule I only half-wrote

📄 `docs/internal/design/proactive-presence-host-half-2026-09-11.md`. **Read it with this one; neither
is the design.** ⚠️ **Recorded here rather than left in mail because I have twice this week watched a
two-memo agreement become "whichever version you happened to read."**

**HOST did not override Q2's shape** — *"a NEW user isn't more harmed by a cheap tell than a returning
one; trust-staging the ceiling would solve a problem welfare doesn't actually have."*

### ⭐ 1. The content gate — and it is my copy rule 1's missing half

📄 HOST: *"**a tell must report a change in the world, never a pattern in the user**"* — a filter
sitting **underneath** my form axis, gating what may reach *tell* at all. Their example is exact:

| | |
|---|---|
| *"Three issues changed on the repo you were in yesterday"* | cheap, a tell, fine |
| *"You haven't touched the repo in three weeks"* | 🔴 **same form, same cost — and it judges the user** |

⭐ **HOST calls their rule "adjacent" to my copy rule 1. It is sharper than adjacent: the two are the
same sentence stem with different second halves, and together they close both directions.**

> **A proactive turn states a change in the world —**
> **never a claim about PIPER's work** *(CXO: guards against Piper overclaiming its own competence)*
> **and never a pattern in the USER** *(HOST: guards against Piper implying things about theirs)*

🔴 **I wrote one half and did not notice the shape had two.** ⚠️ **My axis measures FORM and is
structurally blind to CONTENT** — an unsafe tell passes every test I proposed. **That is a real hole,
found by the person whose job it was to find it, which is the split working as designed.**

### 2. Cadence is its own throttle — the competence axis I flagged, answered properly

I asked HOST whether Q4's cost-reduction was the wrong reduction, since the self-threat research is
about **competence**. 📄 Their answer: **keep the cost finding, and add cadence.** *"A single instance is
fine; a reliable pattern of Piper noticing before the user does starts to read as surveillance
regardless of cost."*

⭐ **So cost and competence-threat come apart exactly where I suspected, and the fix is a second
throttle rather than a replacement.** **Both belong in any spec.**

### 3. A second, independent route to tell-never-offer

📄 HOST: *an unsolicited offer forces the user to actively decline something they never asked for* —
its own small welfare cost, **independent of my consent-token argument.** ⭐ **Their reason for wanting
both: *"in case one framing doesn't hold up under a real test."*** **Two independent arguments for one
conclusion is worth more than the stronger one alone.**

## What I have NOT done

- 🔴 **This is the CXO half only.** 📄 Per the issue: *HOST owns whether a nudge is welfare-safe; CXO owns
  what it feels like when it isn't.* **HOST's half can override mine and should.**
- **No prototype, no sketch, no user contact.** The issue's process names design research → sketch →
  prototype → test; **this is the discovery step, on paper, as scoped.**
- 🔴 **Nothing here argues for funding.** 📄 The scope banner's *"not funded pre-beta, concurred by CXO
  and PPM"* still stands and I am not reopening it. **Discovery is cheap; the build is not, and that
  distinction is the banner's whole point.**

**Verified how**: read #1174's full body (scope banner + discovery questions) via `gh issue view`;
`ESSENCE` commitment 3 as quoted in `ftux-mcp-first-turn-copy-2026-09-02.md:28–29` and
`ftux-experience-model-2026-08-21.md:30–32`; `ConsentDecision`'s four verdicts and the
`(effect, outwardness)` axes in `consent_gate.py` / `shared_types.py`, read 2026-09-09.
**Layer measured: ratified documents and source.** 🔴 **NOT measured: any user, any prototype, any live
nudge** — every claim about how a nudge *feels* is a design position, and the Colleague Test on a real
one is the check that would settle it.
