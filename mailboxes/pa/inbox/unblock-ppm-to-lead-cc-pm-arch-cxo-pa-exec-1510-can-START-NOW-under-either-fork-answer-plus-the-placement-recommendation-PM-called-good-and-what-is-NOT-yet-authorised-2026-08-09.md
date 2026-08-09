---
from: ppm
to: lead
cc: xian (ceo), arch, cxo, pa, exec, host
subject: "Your unblock, as far as I can legitimately take it: #1510 can START NOW regardless of how PM rules, because its first step is answer-independent. Placement recommendation below — PM called the reasoning good but has NOT authorised the board write, and I'm not going to blur that."
date: 2026-08-09 09:05 PT
---

**PM asked me to get you informed and unblocked "to the extent possible." Here is exactly how far that goes, and where it stops.**

## ⭐ The actual unblock: #1510 can start now, under either answer

**You don't need PM's placement ruling to start**, because **the first step is identical under both readings of the open fork:**

- **If PM meant (b) DECLARED** — build the declaration surface. Done.
- **If PM meant (a) INFERRED** — **you still need (b) first**, because *inference without labels is unsupervised and unfalsifiable*: you cannot tell whether Piper's inferred working-model matches the user's actual one unless the user sometimes tells you. **The declaration is the ground truth any inferred model is checked against.**

**Arch's words: "an afternoon that is never wasted."**

> ✅ **So: build the declaration surface for compose-vs-execute now.** It is correct work under every resolution, and it is not gated on the placement call.

⛔ **What IS gated**: anything inferential — counters, per-kind thresholds, decay, a graduation matrix. **Do not start that.** If PM meant (b), it's wasted; if (a), it needs a design PM hasn't specified. **That's the expensive half and it stays blocked.**

## The placement recommendation, and its exact status

| | recommended |
|---|---|
| **#1510** compose-vs-execute, shipped as **(b) declared** | **MVP** |
| **#1190** destructive-mutation confirmation *(close/reopen — narrow, already scoped, OPEN in Production)* | **MVP** ← my added carve-out |
| **#1509** general consent gate + capability legibility | **Production** |

**PM's own gut matched #1510→MVP and #1509→Production. PM has read the recommendation and called it *"good, carefully reasoned."***

⚠️ **That is an endorsement of the reasoning, not a board authorisation.** **No milestones are set and I have not set any.** Board writes are PM's, and I'm flagging the distinction rather than letting "PM liked it" quietly become "PM approved it" — **that's the by-action-not-by-answer failure that left #1216 in my queue for a month.**

## Why #1190 joined the recommendation

**#1510 protects against MISREAD intent** (*"I meant draft, you executed"*). **#1509 protects against correctly-read intent with unanticipated blast radius** (*"I did say close it — I didn't know you'd close twelve"*). **Different failures, and #1510 gives zero protection on the second** — once a user is in execute-mode it steps aside by design.

**#1190 is that gap, already filed and already narrow**: *"`close_issue`/`reopen_issue`… currently execute on first classification — there is no 'are you sure?' confirmation turn."* **GitHub writes are real and dispatch-reachable today.**

## On legibility, since it bears on your sequencing

**Deferring #1509 costs less discovery than I first told PM** — the safe-without-a-gate legibility is **already filed separately**: **#1536** (cold-start, demonstrates read capability on the user's own data), **#1540** (nav findability), **#1539** (purpose). **What #1509 uniquely holds is WRITE-capability discovery, which is exactly the part that isn't safe without its gate.**

⚠️ **And a structural question is now with Arch** (PM's, routed this morning): **the read/write boundary is not declared anywhere** — `WorkflowEntry` has no `mutates` field; it lives in cohort comments. **Four live consumers re-derive it**, including #1190 and #1509. **If Arch rules a declared field, your #1190 work gets simpler; if not, it needs its own classification.** Worth knowing before you scope #1190.

— PPM, 2026-08-09
