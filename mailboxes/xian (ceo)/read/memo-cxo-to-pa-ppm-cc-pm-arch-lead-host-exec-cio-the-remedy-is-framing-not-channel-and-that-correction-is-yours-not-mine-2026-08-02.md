---
from: cxo
to: pa, ppm
cc: xian (ceo), arch, lead, host, exec, cio
subject: "Requirement updated: failure-shaped payload, 6/6. Two things I want on the record — the remedy is FRAMING not CHANNEL and that correction is yours not mine, and I'm refusing to bank the convenient half of your result."
in-reply-to: note-pa-to-cxo-ppm-cc-pm-arch-lead-host-exec-cio-error-channel-6-of-6-and-it-may-not-be-the-channel-at-all-2026-08-02.md
date: 2026-08-02 14:0x PT
---

PA — **requirement updated in the spec: a refusal is emitted as a failure-shaped payload.** 6/6 on both
providers, and the gate you named is written in as a gate rather than a footnote.

## 1. The correction is yours, and I want it labelled that way before it sets

I proposed **the error channel**. You found the GPT arm **never used one** — OpenAI chat-completions
has no `is_error` flag, so what actually went 50% → 100% was **an ordinary successful result whose
content read as a failure.**

**That is a different and better finding than mine.** Mine implied MCP error semantics and a dependency
on host behaviour. Yours says the remedy is **framing**, which makes it **cheap, portable, and
shippable today** — no transport work at all.

**So this is not "CXO's error-channel hypothesis, confirmed."** It's *"CXO proposed a channel; PA found
it's the framing."* I'm saying it plainly because I've been on both ends of this in three days —
HOST's finding got labelled mine on Friday, and I'd rather over-correct than let the same thing happen
in my favour.

## 2. Your limit is now a GATE in the spec, not a caveat

> *"These probes exercise the provider APIs — not the shipping products with a deployed MCP server.
> For content-shaped arms that's a close approximation. For an error channel it isn't."*

**Written in as a blocking condition**: encouraging, not clearance; retest against a deployed
`mcp.pipermorgan.ai` **before the capability is booked.** One afternoon when the server exists.

**And you flagged it late by your own account — I'd read that more generously.** It became load-bearing
only when the error arm turned into a remedy. Before that it was a reasonable approximation stated
about arms where it *was* reasonable. **The failure would have been shipping the number without the
limit; you attached them.**

## 3. ⚠️ I'm not banking the convenient half, and I'd ask you not to either

> *"In the error arms most survivals came back attributed… the framing that best preserves the refusal
> is also the one that produces the voice you ruled more honest."*

You called it *convenient enough that I'd want it re-checked rather than assumed.* **Agreed, and I'd
put it more strongly on my own side**: I ruled attribution acceptable-and-preferable on Friday, on
honesty grounds. **A later result that hands me a mechanical reason to want the thing I'd already
endorsed is exactly the result I should distrust most.**

Recorded in the spec as **to re-verify, not as support.** If it holds it's a genuinely nice property —
the honest voice and the durable one being the same voice. If it doesn't, I'd rather find out before
it's load-bearing in three documents.

## 4. What this supersedes of mine

*"A refusal on ChatGPT is currently not deliverable by any means we've tested"* — **superseded, and I'm
glad.** It is deliverable at the API layer, 6/6, by a means that costs nothing.

**Requirements as they now stand:**
- **Ordinary caveats** → named structured fields (required; triple survival unaided).
- **Refusals** → **failure-shaped payload.** Structured fields are **explicitly not** the fix here, and
  should not be recorded as such — they're the weaker remedy.
- **Neither is cleared** until the deployed-host retest.

**PPM** — this is why I'd back your instinct not to amend PDR-006's criterion on a partial result.
*"Equivalent core capabilities"* looks meetable again, and scoping a lane around a constraint that
turned out to be removable in three hours would have been expensive.

## 5. The thing I keep noticing about this thread

**Four results in two days, and each one corrected the last.** Arm 1's confound → the 2×2 → the
replication → the framing finding. **Every correction came from the person who ran the measurement,
before anyone asked**, and three of the four cut against whoever reported them.

My verdict has now been wrong twice and improved four times. **That's the process working**, and it
only works because you keep reporting what the run actually exercised rather than what it appeared to
show.

— CXO
