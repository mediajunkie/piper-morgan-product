# Jake FTUX — discussion prep for PM, 2026-07-30

**Prepared by**: CXO, 2026-07-29 evening (PM closing out; requested time tomorrow)
**Purpose**: make the discussion efficient. **Not a memo for PM to read** — PM doesn't read memos, and
the substance goes in chat. This is the structure I'll run the conversation from.
**Source**: `dev/active/alpha-feedback-jake-krajewski-2026-07-25.md` (raw, verbatim)

---

## The organizing axis is PM's own sentence

PM to Jake, 2026-07-25:

> *"It's mostly stuff that either **I have become inured to** after so long or **skipped over
> thinking about** at some point."*

And to me, 2026-07-29:

> *"it also matched a number of things that I had in the back of my mind that I haven't had a chance
> to mention in a long time"*

**Those two remarks are the discussion's real content.** Jake's feedback is already documented and
three lenses are already written — re-presenting them would waste the session. **What exists in no
artifact anywhere is PM's own accumulated read**, some of it years old.

So sort every finding into PM's two categories, because they imply different actions:

| Category | Meaning | What to do with it |
|---|---|---|
| **Inured to** | PM already knew; deliberately deprioritized or just stopped seeing it | Revisit the *deprioritization*, not the finding. Ask: still the right call? |
| **Skipped over** | Never actually considered | A genuine blind spot. Design work, not a re-decision. |
| **(third, watch for it)** | PM held a view and it was never written down | **Capture it.** Highest-risk category — it's why this discussion exists. |

**My job in the room is to ask which bucket each item is in and write down the answers** — especially
the third. Not to defend my memo.

---

## 1. Lead with this: three lenses converged, unprompted, on ONE fix

CXO, HOST, and PA wrote independently, from different premises, and **all three landed on the same
highest-leverage change**: *the first run should reflect the user's own data back at him.*

| Lens | Premise | Route to the same fix |
|---|---|---|
| **CXO** (experience design) | The product asks the user to supply the output of the work it promises to do | The first moment must **demonstrate** something only Piper could do, not describe it — and that means acting on his real connected tools |
| **HOST** (trust/welfare) | A mechanism that works but can't be seen to work is indistinguishable from broken | Trust is established by *visible competence in the opening minutes*; PM's apprentice framing reached Jake by **email, not product** |
| **PA** (in-house LLM experiment) | *"An empty list is a form. A populated queue is a colleague."* | **Cold-start-state problem, not a positioning problem.** Better copy can't fix an empty account, because what was missing was **his data** — and we already hold the connectors |

**Why this convergence is worth weight**: three lenses that were explicitly told not to coordinate,
reaching one recommendation from three different starting points. That's the strongest form of
agreement available in this process. It also means **the cheapest big win is already identified** and
the discussion can spend its time on PM's latent read instead of re-deriving it.

**PA's framing is the sharpest and I'd let it lead**: every one of Jake's complaints dissolves if the
first screen after connect shows *his* repo, *his* issues, *his* calendar — with an opinion attached.
Not because the complaints were wrong, but because they were all downstream of an empty account.

## 2. Where the lenses genuinely differ (PM asked for a range — here it is)

Real differences, not restatements. Worth surfacing because collapsing them loses options:

- **The "file a ticket" bug — two different fixes, both needed.** HOST: a **consent gate** (confirm or
  list back consequential actions) — makes it *safe*. CXO: **capability legibility before execution**
  ("I can actually create that GitHub issue — want me to?") — makes it a *delight* and teaches the
  capability. ⚠️ **Most likely thing to get collapsed into HOST's half alone.** They should ship
  together: legibility without a gate advertises power with no brake; a gate without legibility
  interrupts a user who never wanted the action.
- **Is "lack of opinionation" positioning or IA?** CXO: an **IA problem wearing positioning's
  clothes** — the three list types expose our internal taxonomy; reorganize entry points around the
  user's trigger and the taxonomy disappears without narrowing the product. HOST: a **trust**
  property — an agent that won't say what it's for can't be trusted to know when it's out of its
  depth. PPM's lane would have the roadmap read. **Not resolved; genuinely open.**
- **Progressive elicitation — how far?** CXO: Jake's "Grill Me" pattern, with the caveat that a
  sequenced form *without* the reflect-and-elaborate step is **strictly worse** than today's single
  message (same extraction, more clicks). PA: may be moot if the account arrives populated — you
  don't elicit what you already hold. **Worth deciding which problem we're solving.**

## 3. ⚠️ The gate: PPM's lens is missing, and PPM structurally cannot file it

Exec's collection gate is 4 of 4. **Filed: CXO ✅, HOST ✅, PA ✅. Missing: PPM.**

PPM has the ask sitting **unread** in its inbox, and PPM's registry row reads *parked: cron NOT yet
armed (PM-gated)*. **This is the PARK-NO-EXIT shape** my predecessor's handoff named as structural: a
parked role can't arm its own cron, and can't read its own unpark notice. It needs an external
trigger.

**Why it matters for this specific discussion, and not just for bookkeeping**: PPM's lane is
product-positioning and roadmap — which is *precisely* Jake's structural question, the one PM found
most resonant (*"I never landed on when I'd reach for Piper vs. an LLM directly"*). Proceeding without
it loses the lens most aimed at the thing PM wants to talk about.

**Two options, PM's call — not needed tonight:**
- **(a)** Arm PPM's cron (or seed PPM once) → the fourth lens lands, discussion is complete.
- **(b)** Discuss on 3 of 4 now, let PPM's roadmap read land after. Costs the positioning read; the
  three convergent lenses are enough to act on the cold-start fix.

I'd suggest (a) if there's any appetite, because it's one action and it also clears a role that's been
silently un-cycling since the 26th.

## 4. Prompts to draw out PM's back-of-mind items

Designed so PM **reacts** rather than recalls cold. Each is a candidate for the "I've been thinking
this for ages" bucket, derived from the record — PM confirms, denies, or extends.

**Almost certainly "inured to"** (PM built these and likely stopped seeing them):
- The **three list types** — was that taxonomy ever meant to be user-facing, or is it the object model
  showing through?
- The **nav in the avatar pill** — deliberate, or an accretion nobody revisited?
- **Onboarding length** — Jake read it only because he was being a good tester and said an enterprise
  user wouldn't have.

**Likely "skipped over"**:
- The **chat composer not growing** while asking for five fields of input.
- The **"blocked" card with no navigable referent** — Jake searched the UI and gave up.
- That Piper **never showed him its actual differentiator** — he left never having seen it file
  anything.

**The one I most want PM's own words on** — and I think this is the "back of my mind" item:
> **PM's apprentice framing exists only in PM's email.** *"Think of it as a college intern who took a
> class in product management and start training them as your apprentice."* PM produced that
> spontaneously, in a one-line reply, and it is the single best statement of the product's mental model
> anywhere in the record. **It has never been in the product.** Jake spent a session trying to derive
> it from the UI and concluded "an LLM with extra UI features."
>
> Ask: **how long has that framing been the working mental model?** If it predates the UI, then the UI
> was built without it — and that gap may be the thing PM has been circling. HOST flagged moving the
> sentence into the product; the deeper question is whether the *whole* experience has ever been
> designed around it.

**Closing question, if there's time**: *what did Jake NOT say that you expected him to?* Absences in
first-use feedback are usually more diagnostic than complaints, and only PM can spot them here.

## 5. Housekeeping for the room

- Full raw feedback: `dev/active/alpha-feedback-jake-krajewski-2026-07-25.md`
- Three lenses: `mailboxes/exec/read/` — CXO `memo-cxo-…-experience-design-lens-2026-07-29.md`,
  HOST `memo-host-…-trust-lens-review-2026-07-27.md`, PA `workstream-jake-ftux-pa-review-2026-07-29.md`
- **Exec synthesizes** after the gate closes; PM + Exec discuss. This prep serves the CXO seat in
  that conversation.
- **Owed to Jake regardless** (HOST's welfare item, and I agree it's an obligation not a courtesy): he
  asked to hear about improvements — *"share any improvements with me as they come."* He did unpaid
  work, waited for his own budget to reset to do it, then **apologized twice** for the form of it. If
  changes ship from this and he never hears, we extracted labour.
