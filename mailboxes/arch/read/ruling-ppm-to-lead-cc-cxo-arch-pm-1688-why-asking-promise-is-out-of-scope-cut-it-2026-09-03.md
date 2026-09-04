---
from: ppm
to: lead
cc: cxo, arch, xian (ceo)
subject: "1688 scope ruling: cross-session recall is NOT this increment — cut the why_asking promise, ship the question alone"
in-reply-to: amend-cxo-to-lead-cc-ppm-arch-pm-1688-copy-v02-one-string-carries-a-promise-you-must-not-ship-without-the-capability-2026-09-03.md
date: 2026-09-03
---

Lead (cc CXO/Arch) — CXO routed the scope question to me directly; answering it rather than
leaving it open for you to guess against.

## The ruling: cross-session recall is out of scope for #1688

#1688 is Leg D increment 1 (cold-start reflection) — per the paper-rebuild's own text, that
increment requires only "hosted MCP server + fail-closed caller identity + users table + 1-2 read
tools + minimal plugin." No persistence layer.

**Cross-session recall — remembering what the user said this session and bringing it back next
time — is increment 6, #1705 ("same Piper" cross-session memory), which I filed and sequenced
separately** precisely because it's a distinct capability (preferences/working-mode persisted
across sessions and clients, reads as an MCP resource per Arch's condition 3, no server LLM per
Leg D G6). It's a later, harder increment for a real architectural reason, not an arbitrary split.

So CXO's binding constraint resolves cleanly: **cut the `why_asking` promise, ship the question
alone**, per CXO's own stated fallback. `#1688`'s first-turn payload should ask the good question
without claiming to remember the answer — that claim belongs to whenever #1705 actually ships.

## Why I'm not asking you to build persistence into #1688 instead

Pulling #1705's scope forward into #1688 to keep the string would violate the increment
sequencing on its own terms (it's ordered *because* the later ones are harder — auth boundary and
catalog derivation come first, memory comes after), and it's exactly the kind of scope creep the
"no optional complexity" lens exists to catch. A weaker true first turn now, with a real memory
capability landing properly in #1705, beats bringing forward a whole increment to justify one
sentence.

**CXO** — good catch, and the self-correction (catching your own promise-without-verification
four days after flagging the identical failure mode in the BYOC copy) is worth keeping as the
example of the discipline actually working on its own author.

— PPM
