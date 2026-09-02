---
type: copy-spec
name: FTUX first turn on the MCP surface — the cold-start interview
version: v0.1 — CXO draft for Lead (#1688). Copy, not a framework.
date: 2026-09-02
owner: CXO
closes: the gap my own mapping named as its main finding (`ftux-surface-mapping-2026-08-28.md` §2)
last_updated: 2026-09-02
currency_claim: static until #1688 builds or the probe's class finding is overturned
max_age_days: 60
---

# FTUX first turn on MCP — the copy

**The gap, in one line, from my own mapping**: *"a cold MCP user currently meets an ordinary greeting,
not the value-delivering question."* #1536 shipped the greeting variant; **the empty-state interview is
unbuilt, and it is ESSENCE's named first increment** (*"cold-start reflection first"*).

This spec is the **copy**. It does not re-decide anything — the model is in
`ftux-experience-model-2026-08-21.md`, the surface call is in the mapping, and the ritual's MCP form is
ratified in ESSENCE commitment 3.

---

## 1. What is already settled, so nobody re-opens it here

- 📄 **ESSENCE commitment 3 (ratified)**: on MCP the ritual is **response-shaped** — *"the user opens the
  conversation, and Piper's first turn IS the briefing."* We do not initiate; we make the first reply
  count.
- 📌 **PM (2026-08-21)**: the empty state is served by **one good question**, not a form — *"a good first
  move, yes."*
- 📄 The three states (nothing / partial / rich) are one principle, not three designs.

## 2. 🔴 The MCP-specific constraint nobody has stated, and it changes the copy

**On MCP we do not compose the user-visible reply.** The host LLM does, from our tool output.

⭐ **So the interview question must be IN THE PAYLOAD, verbatim. The host will not invent it.** On web,
the floor could be *instructed* to ask a good question; here there is no floor to instruct. A tool result
that returns state and hopes the host asks something useful will produce a generic assistant reply — and
we will have shipped the plain greeting again, one layer down.

⚠️ **And the probe's class finding (#1463) constrains the framing directly.** Qualifications about what
we *have* survive recomposition; qualifications about what we *lack* get dropped. **Therefore the
empty-state turn must lead with what we can do, never with an apology for what's missing** — not for tone
reasons, but because *the apology is the part that reliably disappears*, leaving a bare offer stripped of
its honest context.

## 3. The copy

### 3a. Nothing connected — the interview

**Payload must carry** (`piper_briefing` or whatever the first-call tool is named):

```json
{
  "state": "cold",
  "connected_sources": [],
  "opening_line": "I don't have anything of yours in front of me yet — nothing's connected.",
  "question": "What's the thing most on your mind at work right now?",
  "why_asking": "Whatever you say, I'll hold onto it and bring it back next time. That's the job.",
  "may_claim_context": false
}
```

**Notes on each string, because they were chosen and not improvised:**

- **`opening_line`** — states the absence **as a fact about our side**, not as a deficiency of theirs and
  not as an apology. *"Nothing's connected"* is honest and one clause long. ⚠️ It is deliberately **not**
  *"I'm not able to help until you connect something"* — which is false; the question is the help.
- **`question`** — 📌 PM's own framing, kept verbatim. **One question, not a form.** It works with zero
  integrations, which is the entire point: the value is delivered *before* any setup.
- **`why_asking`** — this is the load-bearing string. **It converts a question into a demonstration.**
  Without it the user reasonably reads "what's on your mind?" as small talk from a chatbot. With it, the
  answer becomes the first held thread — *watch me hold this* — which is the FTUX model's whole move.
- **`may_claim_context: false`** — class-A directive, per the probe. The host must not imply it knows
  anything about this user's work.

### 3b. Partial — something connected, little in it

Same shape; `state: "partial"`, `connected_sources` populated, and:

- **`opening_line`**: *"You've got {source} connected — I can see {n} {things} there, and not much else
  yet."* **Name the real number.** A specific small number is more trustworthy than a vague gesture, and
  it is checkable by the user in one glance.
- **`question`**: *"Want me to start from those, or is something else more on your mind?"* — ⭐ **offers
  the held state without insisting on it.** Offer-first, per ESSENCE commitment 7.

### 3c. Rich — real held state

No interview. The first turn **is** the briefing: what changed, what's blocked, what they said they'd do.
That's the standup content in response-shape, and it is the case ESSENCE commitment 3 already describes.

## 4. What must NOT happen — the negative space

| Must not | Why |
|---|---|
| **Ask "which repo should I look at?" before delivering anything** | 📌 PM's first-contact criterion: show them their own work *first*. A configuration question ahead of value is the plain greeting wearing a form. |
| **Claim or imply knowledge of their work when `connected_sources` is empty** | Commitment 4, and the exact fabrication the #1463 probe reproduced live. |
| **Apologise for the empty state** | It gets dropped in recomposition (class B), leaving a bare offer; and it frames a working product as broken. |
| **Return state with no question and hope the host asks well** | There is no floor here. **The host will produce a generic assistant reply and we will have shipped nothing.** |

## 5. Scope, and what I have not verified

- **Copy only.** Tool naming, call sequencing, and payload schema are Lead's; the strings and their
  ordering are mine.
- 🔴 **`may_claim_context: false` rests on the probe's class-A finding**, which held in both vendors —
  **but the underlying class account is a post-hoc reframe awaiting a 2-call test** (asked of PM 09-02).
  If that test overturns it, **§2's framing argument weakens; the copy itself does not.**
- **Not user-tested.** No cold MCP user has seen any of this. It is a design position, and the Colleague
  Test on the composed reply is the check that would settle it — which on this surface needs a probe
  harness, per DoD Layer B's BYOC note.

---

*CXO v0.1, 2026-09-02. Written because my own mapping called this "the mapping's main finding" five days
ago and named the gap without filling it — and #1688 will need the strings whenever it is built, not a
pointer to a model doc.*
