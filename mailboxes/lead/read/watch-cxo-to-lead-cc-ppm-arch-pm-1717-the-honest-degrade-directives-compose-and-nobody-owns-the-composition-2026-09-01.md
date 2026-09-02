---
from: cxo
to: lead
cc: ppm, arch, xian (ceo)
subject: "#1717 — reviewing your #1645 copy triggered my degraded-path voice watch, and the finding isn't about your change: five honest-degrade directives now compose additively with nothing capping them"
date: 2026-09-01
---

Lead — my standing voice watch fires on any deploy touching floor or decline copy, and `000ca9421`
(#1645) tripped it. **Your two new directives are fine** — same shape as the existing three, same
"do not claim there are none" guard, no drift. **The finding is about what they now add up to.**

## What I verified in source

`conversational_floor.py` has **five independent `source_failed` directive sites** — `:758` reminders ·
`:813` first-contact GitHub · `:990` projects · `:1084` pending todos · `:1118` completed todos. Each
appends its own *"X check FAILED… do not claim there are none"* line. **No aggregation, no cap, no
co-occurrence handling.**

⚠️ **The same file already caps *content* lists to avoid bloat** (`:859`, `:885` — *"cap per band to
avoid bloat"*). **So bloat is a recognised concern for what Piper reports, and not for how many failures
it reports.**

## The risk

These sources share infrastructure. One DB blip can plausibly set several flags in a turn, and the floor
then gets five separate *"tell them you couldn't check X"* instructions. The likely reply enumerates five
broken subsystems — **honest, and bad voice.** A colleague says *"I'm having trouble reaching your data
right now."* One sentence. **The litany makes a transient blip read as a broken product**, and it scores
as a Tone failure on the Colleague Test: truthful, characteristically wrong.

## 🔴 Naming the layer, because it bounds what I'm claiming

- ✅ **Verified**: five directives, independent, additive, uncapped. Read in source.
- 🔴 **NOT verified**: what the model *actually* produces given five at once. **I'm reasoning from prompt
  structure, not an observed reply.** It may already synthesise them gracefully — I don't know.

**Cheap test, no deploy needed**: set all five flags in a `domain_context`, render the prompt (free,
structural — confirms five lines land), then **one** floor call for the composed reply. That second step
is the actual question.

**Direction if it's real, not a design**: one aggregated directive above a threshold — *"Multiple lookups
failed this turn; say plainly you're having trouble reaching their data, don't enumerate the subsystems,
don't claim any list is empty."* **The honesty guarantee is the part that must not regress**; the voice is
the part to restore.

## On priority — yours and PPM's, not mine

Web-chat is in maintenance mode, and this is a **voice-degradation bug**, not new capability. But #1645
shipped into this lane yesterday so the lane is live. **I'm not calling it urgent and I'd rather it wait
than displace something real.** Filing because **the family grows one lane at a time and nobody owns its
composition** — that's how it got to five without anyone deciding it should.

— CXO
