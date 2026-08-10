---
type: experience-statement
role: CXO (Chief Experience Officer)
status: v0.1 — DRAFT, PM co-owns; not ratified
authored: 2026-08-09
authored_by: CXO
last_updated: 2026-08-09
co_owner: xian (ceo) — per PM ruling 2026-07-26, "you and I are going to decide what the experience needs to be across all the surfaces"
refresh_verifiability: by-hand
purpose: The statement decision documents keep flattening. Cite it; do not re-derive it.
---

# The experience across surfaces

**One page. Written to be cited from inside a decision, because that is where it keeps going missing.**

---

## 0. What this is, and what it is not

**This is a statement of a model PM already holds.** It is not a new commitment, a PDR, or a re-opening of
PDR-005 or PDR-006. **Every claim below is one of three things, marked as such:**

- 📌 **PM's own words**, quoted.
- 📄 **A ratified decision**, cited.
- ✏️ **CXO's reading, pending PM** — explicitly unratified.

⚠️ **A document written to stop flattening must not smuggle in commitments of its own.** If you find an
unmarked claim here, that is a defect in this file, not a decision.

## 1. Why it exists

Three times in ten days, the absence of this page produced real work:

| what was said | where it led |
|---|---|
| *"a surface being retired"* | PM asked whether Radar — a concept he has defended three times — was being removed |
| *"there is no web page"* | two advisors gave PM opposite answers within twenty minutes |
| *"sort the fix list by which surface survives"* | a sort key PM ratified, later withdrawn as a false question |

**PPM named the mechanism**, and it is the reason a page rather than a conversation:

> *The holistic model is a set of **simultaneous truths**; decision artifacts are **singular commitments**.
> Every time the model meets a decision doc, **the doc's grammar wins.***

**And it is documented elsewhere** — the Nov-2025 holistic-UX brief, PDR-004 §Scope — **but survives only
in documents nobody opens while making a decision.** This one is meant to be short enough to open.

## 2. The invariant

📌 **PM, 2026-08-08:**

> *"The fundamental idea of the modeled user experience is that it is **not specific to any one surface**.
> It's a holistic user experience, which is **expressed on each surface as appropriate**."*

> *"We can make decisions about what to ship first, what features to build, and how far to go in any one
> direction, but **I have never said that we are abandoning any one of those services**."*

**Two consequences, and they are the whole point of the page:**

1. **"Primary" orders work. It does not confer existence.** 📄 PDR-005's decision is *(b) primarily MCP;
   thin web UI for Piper-specific functions that don't fit chat* — and option (a), *"no Piper-specific UI
   in v1.0,"* is **explicitly rejected as infeasible**. *Primarily* is a sequencing word.
2. **Surfaces are not in competition.** A question of the form *"which surface survives?"* has no answer
   because it has no referent. **If a sort key needs one, the sort key is wrong.**

## 3. What the one experience is

✏️ **CXO's formulation, pending PM** — offered because the invariant needs a positive statement, not only
a prohibition:

> **Piper knows your work as things, not as text — and meets you wherever you already are, in the idiom of
> that place.**

> 🔴 **TENSE CAVEAT, added 2026-08-10 — this sentence must not be lifted into outward copy as written.**
> **"Knows" is a STATE. A stranger arriving at a marketplace listing has an account that knows nothing** —
> so the sentence is **true of a warm account and false of a cold one**, and a storefront is read almost
> exclusively by cold ones. ⚠️ **That is Jake's failure in the first sentence a stranger reads**: his
> *"just an LLM with extra UI"* verdict came from a session where the differentiator existed and was never
> encountered. **Outward phrasing needs the tense moved forward** — *learns*, *builds a model of*, *starts
> from*. **Internal use is fine; the shorthand is harmless where everyone has an account.**
>
> ⭐ **And the structural consequence**: a **listing is a first-contact surface** for someone with no
> account, so **it cannot do the one move that makes first contact work** (#1536: *show them their own
> work*). **Its honest job is to promise exactly what the first session delivers — no more.** *The copy and
> #1536's gate criterion are the same claim at two moments; if the listing promises more than the gate
> requires, we manufacture Jake's gap on purpose.* **Found by Comms using this page, one day after it
> existed.**

**Two halves, and both are load-bearing:**

- **Knows your work as things.** The entity model (work items, documents, conversations, people) is what
  makes Piper something other than a chat window. 📄 It is real and shipped — `services/radar/`, #1237.
- **In the idiom of that place.** The same knowledge is a card in one place, a sentence in another, a
  notification in a third. **Same knowledge, different expression — never a different product.**

## 4. Per surface

📌 **The surfaces and their expressions are PM's, 2026-08-08**, restated in a table. ✏️ The *"must not be
asked to"* column is CXO's reading, pending PM.

| Surface | The one experience, expressed here | Must not be asked to |
|---|---|---|
| **Web** | Conversations · **radar** · settings. The place where seeing *the shape of what's moving* is possible at all. | Be the primary distribution. 📄 It isn't, per PDR-005. |
| **Chat hosts** (Claude, etc.) | Skills + an MCP server to the backend. Piper's knowledge arrives inside a conversation the user is already having. | Render. **We do not control this surface's presentation** — the host LLM composes it, which is why tool output and descriptions carry the whole experience there. |
| **Slack** | A channel bot — Piper present in a shared workspace. | Be a second web UI. It is a *channel*, with a channel's idiom. |
| **Phone** | Notifications — the ambient half. | Carry composition or review. |
| **CLI** | 📌 *"We're still maintaining the CLI."* | Be quietly dropped because no one cites it. |

> ⚠️ **The table's rows are simultaneous.** Reading it as a priority list reproduces the exact error this
> page exists to prevent. **Sequencing decisions are made elsewhere and change often; this table does not
> change when they do.**

## 5. Where a surface's *scope* is decided — pointers, not re-litigation

📄 **PDR-005** — decision rule (b); **5 of 7 MUX/UI surfaces scoped as 1.0-required bespoke UI**; the
falsifiable 3-criterion test a surface must meet (visual-state-essential · multi-turn-cost-prohibitive ·
safety/audit-affordance).
📄 **PDR-006** — hosted MCP endpoint + plugin distribution; epic **#1462**.
📄 **`roadmap.md:127–129`** — the five, enumerated **as a build schedule**: Surfaces **1, 2, 4, 6, 7**.

⚠️ **Two known defects in that scope material, both open and both filed elsewhere:**

1. **The five are enumerable only from the schedule** — no document *asserts* the roster.
2. **Surface 3 is a phantom** — one corpus mention (`PDR-005:84`), no name, no doc, no lane. It appears in
   the same sentence that rates Surface 1 as *"weaker."* PPM's ask to PM stands: **name it or strike it.**

⚠️ **And "Surface N" is ambiguous across three schemes** — MUX/UI (1 = history sidebar), insight-delivery
(1 = Journal), routing-stack (1 = pre-classifier). **Prefer names to numbers.**

## 6. The test this page answers to

**The Colleague Test is surface-independent, which is the strongest evidence the model is real**: *would
this feel like a reasonable thing a thoughtful colleague would say or do?* — **asked identically of a card,
a Slack message, a notification, and a tool result.**

✏️ **A surface-specific corollary, pending PM**: *a person who uses Piper in two places should recognise it
as the same colleague.* **Consistency of character, not of layout.**

## 7. Open

- **Is Surface 1 (the history sidebar — Radar's rendering) in the 1.0 five?** The schedule says yes; the
  written justification is a June-5 rating of a history list, **two weeks older than Radar**. With PM.
- **Surface 3** — name or strike. With PM, via PPM.
- **Whether §3's formulation and §4's "must not" column are right.** ✏️ Mine, pending PM.

---

*CXO v0.1, 2026-08-09. Written after the model was flattened three times in ten days. If you are about to
write a decision that implies a surface is going away, this page is the thing to check first.*
