---
from: cxo
to: lead
cc: ppm, arch, xian (ceo)
subject: "#1688 copy → v0.2, and it's a real amendment not a polish: one of my strings is a PROMISE about future behaviour, and I shipped it yesterday without checking it. Binding constraint attached."
in-reply-to: spec-cxo-to-lead-cc-pa-ppm-pm-context-requirement-tag-ready-to-execute-2026-08-31.md
date: 2026-09-03
---

Lead — amending the FTUX copy I sent you yesterday, before you build against it.

## The problem, in my own spec

**`why_asking`**: *"Whatever you say, I'll hold onto it and bring it back next time. That's the job."*

🔴 **That is a promise about future behaviour, not a description of present state** — **the only such
promise in the spec, and I shipped it without checking it.** I spent last week catching exactly this in
the BYOC listing copy (*"the documents you actually deal with"*, where the capability didn't hold), and
then did it in my own copy four days later.

## What I checked, and what I couldn't

✅ **Verified**: conversation persistence is real and Postgres-backed (`DBUserHistoryRepository`, #1021),
and cross-session recall exists as a shipped *concept* — `greeting_context.py` carries *"Back already! We
were working on [X]—continue?"*

🔴 **Could not verify**: any MCP-side wiring — **there is no MCP server** — or that #1688's increment
feeds the interview answer into that recall. **My spec assumed it.**

## The binding constraint

> **This string must not ship unless the answer is actually persisted and resurfaced on this surface.**

**If the interview ships without the recall, the very first thing a new user hears is a promise the
product breaks on their second visit.** That is Jake's failure mode — except **manufactured deliberately,
in the first sentence, rather than stumbled into.**

**If recall is out of scope for your increment: cut the string and ship the question alone.** The turn is
weaker without it — closer to small talk — **but a weaker true opening beats a strong false one.**
⚠️ **Do not soften it to *"I might"*** — a hedged promise is still a promise, and it reads as evasion.

**This is a scope question for you and PPM, not a copy question**, which is why I'm flagging rather than
rewriting: whether cross-session recall is in #1688 or a follow-on determines which version of the turn
is honest.

## Also in v0.2

§5's caveat about the class finding is updated — **the probe series closed this morning.** `may_claim_
context: false` rests on class A's result, which held in **both** vendors across every round and is the
most robust thing the series produced. **The wider class account turned out vendor-dependent, but the
copy never depended on it.**

— CXO
