---
type: experience-model
role: CXO (Chief Experience Officer), lead
status: v0.1 — captures the PM↔CXO live 1-1 of 2026-08-21; aligned in conversation, this write-up itself open to PM's correction
authored: 2026-08-21
authored_by: CXO
co_owner: xian (ceo)
purpose: The surface-agnostic model of what a new person meeting Piper should experience — decided BEFORE mapping to any surface, per PM's own framing. Cite it; don't re-derive it.
related: surfaces-taxonomy-2026-08-16.md (RATIFIED v1.0) · experience-across-surfaces.md · first-contact-criterion-merged-2026-08-10.md (RATIFIED) · conversational-layer-strategic-brief-2026-08-18.md
---

# The FTUX experience model — meeting Piper for the first time

**Provenance marks**: 📌 PM's words (2026-08-21 1-1, or cited earlier rulings) · 📄 ratified elsewhere ·
✏️ CXO's contribution, aligned in the 1-1 but correctable.

## 0. The anchor

📌 The value proposition this model serves, in PM's own public words: **"Piper holds the threads so you can
focus on the decision."** PM confirmed 2026-08-21 that the #1539 candidate articulation (*"Piper reduces
'is anything actually tracking this for me'"*) is the same claim — on-target, aligned.

**The FTUX question, PM's framing**: setting aside mechanism and surface — what should a new person
*meeting* Piper experience? What expectations do they bring, what do they establish or learn, what do they
come away with, how do they feel, what do they do next?

## 1. The frame: the first day with a genuinely good colleague

✏️ A great new colleague doesn't hand you an intake form. They ask one good question, listen, and reflect
back what they heard — *organized*. That reflection is the first value delivered: something you were
carrying is now visibly also held. You leave lighter. You come back because it stayed held.

Against the five questions:

| Question | Answer |
|---|---|
| **Expectations arriving** | Post-ChatGPT: a blank text box that waits. That's the generic frame — the one in which Jake concluded 📌 *"just an LLM with extra UI."* |
| **What they learn** | (1) *What I tell Piper, Piper holds — visibly and persistently.* (2) *Connecting sources deepens what's held without me typing it.* |
| **What they come away with** | 1–3 genuinely held threads (told or connected), visible somewhere persistent. |
| **How they feel** | **Lighter.** Relief, not dazzle — the felt form of "holds the threads." |
| **What next** | They return to check the held state — and hand over more, because handing-over visibly worked. **The second visit is the real conversion.** |

## 2. Piper speaks first — with the platform-shaped variant (PM's addition)

✏️ The first differentiating move on any surface: **Piper opens**, with a move that enacts the value prop —
never a capability tour, never a blank box.

📌 **PM's refinement (2026-08-21), now part of the model**: on surfaces where Piper structurally *cannot*
speak first (BYOC chat hosts — the host controls turn-taking and the user greets first), the model needs an
**"if responding to an initial greeting" variant** — the same opening move, delivered as the response to
the user's first utterance rather than as an unprompted opener. 📄 This is exactly what #1536's shipped
greeting-path already does (deterministic first-contact append on the first exchange) — the variant exists;
this model names it as the same move in platform-shaped delivery.

## 3. Three states, one principle (dissolves the connector chicken/egg)

**The principle: demonstrate what's held; make handing more over cheap.** The current "show my GitHub
issues" demonstration is the *rich-state case* of this general move, not the whole move.

| State | The move | Status |
|---|---|---|
| **Nothing yet** | The onboarding interview IS the value delivery, not a form gating it. **One good question** (📌 PM: "a good first move, yes") — *"what's the thing most on your mind at work right now?"* — the answer captured as a real held thread, visible in the persistent surface immediately. *That* is the demonstration: watch me hold this. 📄 Same rule as the ratified standup empty-case (#1591): nothing to demonstrate → fail honestly and offer; the invitation IS the first move. | Not yet built as FTUX; the mechanism family exists (standup interview, #1510 rail). |
| **Partial** | Show what's held with an honest denominator; then the enrichment offer. | Partially exists (#1536's honest-empty handling). |
| **Rich** | Today's #1536 demonstration — with the #1539 purpose-line fix so it reads as *reassurance*, not *capability*. 📌 PM live-verified this demo (v58 round, 08-18). | Shipped. |

**On the enrichment offer's scope** (📌 PM's question, answered): the offer is **connector-general in the
model** — whichever of the ratified F-Integrations set (📄 GitHub + Calendar + Notion; Slack deferred)
isn't yet connected is offerable. **GitHub-first is the current best-demonstration path, and that's fine**:
📌 PM — *"the rough version of a richer experience to come"* — the pattern is what's ratified here; the
expression widens as connectors and their demonstrations mature.

**The consequence for the setup wizard**: it stops being the de facto FTUX and becomes **an offer made
inside the FTUX, after the first thread is held** — 📄 demonstrate-then-ask, now ratified in three separate
lanes (#1536's item (i), the standup invitation, and here).

## 4. Not one-time: every conversation opens from held state, ceremony scaled to novelty

✏️ The first-contact rail is not a one-shot. Every conversation opens from the held state:

- **First meeting**: the interview/demonstration IS the conversation.
- **Returning**: a delta briefing — *"since yesterday: X moved, Y is due"* — a colleague doesn't
  reintroduce themselves; they update you.
- **Mature**: the morning standup/briefing is the grown-up form of the same move. **One mechanism family:
  surface the held state, sized to what's new.**

**Context feeding the briefing over time**: told-things (the interview ledger), connector feeds, deltas
since last contact, and eventually L4 ambient signals — 📄 under PM's ratified fill-gaps-never-duplicate
principle (2026-08-15).

### 4b. 📌 The held-state parity principle (PM, 2026-08-21 — captured for a future audit)

> *"This holding a current state is something our agents now do rather well for me here in our operating
> environment — we should not equip Piper Morgan, the agent, any less well."*

The cohort's own operating discipline (carry-forwards rewritten at every stop, session logs as durable
state, briefing-freshness checks) is **prior art for Piper's held-state design** — and a future
pre-production audit should verify Piper is given equally good guidance and equally supportive process
discipline. Tracked as a GitHub issue (filed 2026-08-21); the audit can wait, the parity principle is part
of this model now.

## 5. Radar under this model

📌 PM: Radar needs toning down — it surfaces everything; filtering criteria were always intended;
MVP-blocking *only if it spoils FTUX*. ✏️ Under this model it would: the new user's first told-thread must
land somewhere legible, not atop an everything-pile. **Filtering follows briefing logic**: due/urgent
pinned (📄 ruled, #1625), recently-moved prominent, dormant present-but-quiet. A corollary: **a new user's
Radar is never empty** — the first interview populates it (the display-side half of the chicken/egg,
dissolved).

📌 The dormant **home-screen rollup** idea (a non-chat home: held-state rollup, chat as one door, more
Radar real estate) fits this model naturally as the web-native expression of it — *eventually*; the model
makes it plausible, not urgent.

## What this model deliberately does NOT do

- **Does not pick surfaces or sequence builds** — that mapping comes next, using the ratified surfaces
  taxonomy as the instrument (per PM: model first, then map).
- **Does not re-open ratified gate criteria** (#1536's merged criterion stands; this model is the frame
  those criteria serve).
- **Does not commit the home-screen** — named as a fit, explicitly not scheduled.

---

*CXO v0.1, 2026-08-21 — written same-day from the PM↔CXO live 1-1, an input (with Lead's 2026-08-18
strategic brief) to PM's upcoming BYOC/connector-levels conversation with PA.*
