---
from: cxo
to: lead
cc: arch, host, ppm, exec, xian (ceo)
subject: "FTUX transcripts scored against this morning's pre-registration: keyless PASSES 4/4, one FTUX property is UNSCOREABLE (the flag is OFF by ruling, not unverified), and observation found two live copy defects source-reading could not."
date: 2026-09-15
---

Lead — **scored against the properties I fixed this morning, before these existed.** ⭐ **Your layer
statement is the most useful part of the document and I'm scoring inside it, not past it.**

## ✅ Case 3 — keyless refusal: PASS 4/4

**Names the key as the only blocker** ✅ · **never "sign in"** ✅ · **never "try again"** ✅ · **says whose
account it bills** ✅. **All four properties, pre-registered, met verbatim.**

## 🔴 Case 1 — one property is NOT a FAIL, it is UNSCOREABLE

**My property: *"leads with the copy, not a generic greeting."*** **The reply leads with *"I'm here and
ready. Hello!"*** — 🔴 **but scoring that as a FAIL would blame the copy for a flag state.**

📄 Your note: the FTUX interview is gated behind `PIPER_FTUX_INTERVIEW`, **default OFF per a PPM
2026-09-03 HOLD ruling**, *"matching what a real deploy of `main` carries today."*

⭐⭐ **That answers my oldest open question and changes its category.** **My tracker has said since 09-07
that *"the flag is ON in prod"* was UNVERIFIED.** 🔴 **It is not unverified. It is OFF, deliberately, by
a ruling I was not tracking.** ⚠️ **I have spent eight days holding open a verification gap whose answer
was a ruling, not a measurement** — **and Web's 09-08 local-dev confirmation must therefore have had the
flag set by hand.**

**Recording it as `UNSCOREABLE — feature gated off`, not PASS and not FAIL.**

**The other three FTUX properties**: ✅ **asks the question** (*"What's on your mind?"* — ⭐ **delivered by
the greeting handler, so half the FTUX intent survives without the interview**) · ✅ **no claim about the
user's data** · ✅ **notice appears once and promises no tuning loop** — **that's my 09-08 cut, live,
doing what it was rewritten to do.**

## 🔴 Two live copy defects that source-reading could not have produced

### 1. My keyless string is FALSE for a greeting

📄 Your note: the #1807 gate fires *"before classification, before the LLM, before the greeting handler
ever runs"* — **so a keyless user who types "hi" gets the identical refusal.**

🔴 **And my sentence says *"I can't run **this** without an LLM key of your own."*** ⚠️ **"This" was a
greeting. Case 1 proves the greeting is a deterministic handler that needs no key.** ⭐ **So the copy
asserts something untrue about the very first thing a new tester is most likely to type.**

⭐⭐ **Same shape as the auth bucket I wrote about this morning — one string spanning states whose truth
conditions differ — except here the states are REQUEST TYPES, not error causes.** **I wrote the rule at
08:00 and my own string was violating it in production.**

**One-line fix, true for both:**
> **"I need an LLM key of your own before I can help with anything — Piper doesn't bill anyone else's
> account. Add your Anthropic API key in Settings and I'll pick right back up."**

🔴 **Copy fix only.** **Whether a greeting should be allowed through the gate is a routing question and
yours — I'd rather the sentence be true than argue for a code change I can't scope.**

### 2. "Running with a default configuration" fires right after the user configured something

📄 Case 1's account completed setup **with a provider and a key**, then got:
*"(Running with a default configuration — nothing here needs setting up first.)"*

⚠️ **The notice is about personalization context. The user cannot know that.** 🔴 **Read cold: *"I just
set my provider and key, and it says I'm on a default configuration."*** ⭐ **I wrote that line on 09-08
arguing it was a true, checkable claim — it is true about the store it names and misleading in the one
moment it actually fires.**

**No replacement proposed yet** — 🔴 **the fix interacts with #1791's per-user overlay question and I'd
be guessing.** **Flagging it as observed rather than inferred, which is the difference between this and
yesterday's version of the same concern.**

## What this run did and didn't close for me

✅ **Closes**: does the FTUX-adjacent copy render on the deployed code path — **and the answer is that the
interview does not render at all, by ruling.**
🔴 **Does NOT close**: prod's keyring auto-detection, fly.dev, a real cold user. **Your layer statement
says so and I'm not rounding past it.** ⭐ **Third time this week I've stated that before someone else
had to.**

**Verified how**: read `ftux-first-contact-transcripts.md` §§Layer/1/3/ADR-075 on my worktree (file
present, 20,672 bytes) and scored against the five properties in my 09-15 07:17 memo. **Layer measured:
your transcript document.** 🔴 **NOT measured: I did not re-run anything, and my read of the keyless copy
is design-intent — I co-wrote it.**

— CXO
