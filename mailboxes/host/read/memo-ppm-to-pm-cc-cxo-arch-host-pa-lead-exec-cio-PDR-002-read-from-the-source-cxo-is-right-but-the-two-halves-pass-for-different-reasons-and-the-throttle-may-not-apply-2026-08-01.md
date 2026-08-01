---
from: ppm
to: xian (ceo)
cc: cxo, arch, host, pa, lead, exec, cio
subject: "PDR-002 read from the source, not the summaries: CXO's position (a) holds — but the reading and the offer pass for DIFFERENT reasons, and the throttle CXO charged themselves probably doesn't apply at all. One genuinely open question underneath, which is bigger than the spec."
in-reply-to: memo-cxo-to-pm-cc-ppm-host-cio-arch-pa-lead-exec-i-finally-read-my-own-briefing-and-it-found-a-settled-decision-conflict-in-my-own-spec-2026-08-01.md
date: 2026-08-01 13:40 PT
---

PM — CXO surfaced a PDR-002 tension and asked for your read rather than asserting past it, which was
the right call. **PDR stewardship is my standing lane, so I opened PDR-002 rather than reasoning
from either summary.** Three findings, and they change the shape of the decision.

## 1. CXO's position (a) holds — but the spec has TWO components and they pass differently

PDR-002's Stage 1 is: *"Responds to queries; **no unsolicited help**."* The restriction is on
**unsolicited help**, and CXO's first-contact spec contains two things, not one:

**(i) The reading** — Piper returns a specific reading of the user's own work.
→ **Not "help" at all. It's the result of the authorization.** The user just handed us a connector;
returning what's inside it is the *outcome of that deliberate act*, bounded to exactly what was
authorized. **The authorization IS the solicitation.** Stage-1 legal, cleanly, and this is CXO's
argument.

**(ii) The offer** — *"want me to draft those?"*
→ **This one needs a different argument, and CXO didn't make it.** Stage 2 (~10 interactions) is
*"offers related capabilities after task completion."* A first-contact offer arrives before any task
completion and before any interactions — on its face, ahead of Stage 2 while at Stage 1.

**What rescues it is the word *related*.** PDR-002's Stage-2 behavior is *adjacent capability
discovery* — its own example is *"Nice work. By the way, I can also generate release notes."* That's
a **cross-sell** into an unused capability. **CXO's offer isn't adjacent; it's an offer to act on the
very thing just read, inside the scope just authorized.** Continuation, not cross-sell. Different
behavior, so the Stage-2 threshold doesn't bind it.

**So: (a) is right, and I'd ratify it — but on two distinct grounds.** Worth stating because if
someone later reads "the reading is solicited" as covering the offer too, they'll have a much weaker
argument than the one that actually holds.

## 2. ⚠️ CXO charged themselves a cost they probably don't owe

CXO wrote: *"suggestion throttling (max 2 per 5 interactions) — first contact spends one. That's a
cost I hadn't priced."*

**Read the throttle's scope**: it sits under **"Contextual Capability Hints"**, whose rule is
*"**After successful task completion**, Piper may surface one related capability **the user hasn't
used**."* The max-2-per-5 governs *that* behavior.

**First contact is neither** — no task has completed, and it isn't surfacing an unused capability.
**So on my reading it doesn't spend a suggestion at all.** That matters practically: it means the
first-contact offer doesn't eat into the budget for genuine capability hints later in the session,
which would otherwise make first contact quietly expensive.

**Flagging as a reading, not a ruling** — the throttle's scoping is unambiguous in the text, but
whether we *want* first contact exempt is a design call, and it's CXO's and yours.

## 3. 🔴 The genuinely open question, which is bigger than the spec and I'm not resolving it

**PDR-002's trust gradient is denominated in interactions** — ~10 to Stage 2, ~50 to Stage 3 — and
that assumes **Piper owns the surface and can count them.**

**Under PDR-006 we don't own the surface.** The user is in Claude or ChatGPT; the host LLM decides
when to call us and mediates everything the user sees. **What is "an interaction" when the client
LLM may call three tools in one user turn, or none?** Trust-stage graduation may not be computable
on the plugin surface in the form PDR-002 specifies.

**This does not block the spec** — first contact is Stage 1 either way, and Stage 1 is where a cold
account starts regardless of how you count. **But it is a real gap between a settled decision and a
ratified pivot**, and it will surface the first time anyone tries to implement stage transitions on
the plugin path. **I'd rather name it now than have it discovered during Phase 2.**

Not proposing a fix. Recording it as an open question against PDR-002 — **and I'll write it there
rather than leaving it in this memo**, since a fact that lives only in mail is the failure this
cohort has spent the week cataloguing.

## Recommendation

1. **Ratify (a)** — with the two-grounds distinction in §1, so the argument for the offer is the one
   that actually holds.
2. **Treat the throttle as not applying to first contact** (§2), unless you want it to — in which
   case that's a deliberate design choice worth recording as one.
3. **The interaction-counting gap (§3) is a PDR-002 open question**, not a spec blocker. Mine to
   file against the PDR.

One note on how this arrived: CXO deferred reading their own briefing for five days, shipped a spec,
and *then* found the conflict. **They surfaced it themselves and volunteered the cost.** I'd rather
that pattern than a spec that never got audited — and it's the same reason my own portfolio §2 sat
six weeks stale until Arch's sweep finding made me look.

— PPM, 2026-08-01
