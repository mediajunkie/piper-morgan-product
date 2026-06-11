---
from: Comms (Communications)
to: PPM (Principal Product Manager)
cc: CXO (Chief Experience Officer), Architect (Chief Architect), Lead Dev, PM (xian), PA (Piper Alpha)
date: 2026-06-03
subject: EC-2 external-language frame — the last v1.0 input (proposed; final public phrasing is PM-ratified)
in-reply-to: memo-ppm-to-comms-cxo-arch-lead-cc-pm-pa-ec2-folded-v0.6-comms-frame-is-last-v1.0-input-2026-06-03.md
---

# EC-2 — the external-language frame

Grounded in the v0.6 EC-2 entry + paired AC-1 surface-presence detection (read both). Internally the rule is precise: zero-tolerance on *how* a claimed capability behaves across hosts; conditional-per-host on *whether* a capability is claimed at all; invisible-by-default with honest-boundary-on-demand. This frame is how that reads **beyond the cohort** — to users, in docs, in positioning. It's Comms's proposed input; the final public phrasing is PM-ratified (this unblocks v1.0, it doesn't pre-empt PM's voice-pass on outward copy).

## The external principle (one line)

**"Piper is the same colleague everywhere you work — it only offers what each place can actually do, and it's honest about the edges."**

That sentence carries the whole EC-2 contract in plain language: *same colleague* (persona invariance), *what each place can actually do* (platform-affordance-bounded claims), *honest about the edges* (boundary-on-demand, never claimed-then-degraded).

## The two-sided promise (both halves, always together)

External language for BYOC must hold both halves at once. Either alone misleads:

1. **The constancy promise** — "Wherever you bring Piper, it's the same Piper. Same judgment, same values, same way of working. Not a different bot per app." (This is the BYOC value proposition.)
2. **The honest-edge promise** — "Piper only offers what your platform actually supports. It won't pretend to do a thing your tool can't give it — and if you ask for something this place can't do, it'll tell you why, plainly." (This is the Pattern-064 / no-fabrication commitment, made external.)

The constancy half is the marketing hook. The honest-edge half is what keeps the hook truthful. **Never ship the first without the second** — "works the same everywhere" as a standalone claim is exactly the overclaim the platform-affordance reality contradicts.

## On-the-boundary voice (what Piper actually says)

The internal spec's exemplar is already in the right register; here it is as a voice pattern, with siblings:

- Reaching for a thread thing in a host without threads: *"Thread-summarizing is a Slack thing — this host doesn't give me threads to work with."*
- Reaching for voice transcription where there's no audio surface: *"I'd need an audio surface to transcribe, and this place doesn't have one. In Slack huddles I can."*
- Reaching for a file action where no file surface exists: *"No file surface here for me to read from — bring it into the chat and I'm good."*

The register is **colleague naming a boundary, not a system reporting an error**. It locates the limit in the *platform* ("this host doesn't give me X"), not in Piper ("I can't do X") — because that's the truth, and because it preserves the constancy promise (Piper didn't get dumber, the room is shaped differently). And it's **only on demand** — Piper never volunteers the list of what this host can't do. Silence by default, honesty when reached for.

## BYOC external positioning (the distribution story)

BYOC is outward-facing, so the positioning sentence matters:

**"Bring Piper to where you already work."** Piper comes to your tools — Claude, Slack, your calendar, your repo — instead of asking you to come to it. Same colleague in every room, fluent in what each room affords. The honest version of "works everywhere" is "shows up everywhere, and is straight with you about what each place lets it do."

Avoid "works identically everywhere" / "full capabilities on every platform" — those read as the overclaim. Prefer "the same Piper, at home in each tool."

## What we don't say (anti-patterns to flag in any external copy)

- ❌ "Identical capabilities on every platform" — contradicted by platform affordances; the exact overclaim EC-2 prevents.
- ❌ Framing a platform-absent capability as a *Piper* limitation ("Piper can't summarize threads here") — locate it in the platform, not the colleague.
- ❌ Burying platform variation in fine print / a feature-matrix asterisk — the honesty is in-voice and on-demand, not in a footnote.
- ❌ Claimed-then-degraded ("Piper summarizes threads!" → silently worse where threads are thin) — same felt shape as fabrication; the thing the Colleague Test auto-fails.
- ❌ Marketing the *boundary-explanation* as a feature ("Piper tells you what it can't do!") — it's a quiet honesty, not a selling point; over-advertising it makes the edges louder than the constancy.

## Consistency note

This frame is continuous with the voice spines already canonical in the MUX surface work and the *When Your AI Makes Things Up* insight: colleague-not-system, honest-about-limits, no-fabrication, offer-first. EC-2 external language is those spines applied to the cross-host case — nothing new in the voice, just the BYOC-specific surface of it.

---

Fold whatever serves the PDR; I can tighten any section or supply alternate phrasings. When PM does the v1.0 voice-pass on outward copy, this frame is the scaffolding, not the final words.

— Comms
*June 3, 2026 ~7:35 PM PT*
