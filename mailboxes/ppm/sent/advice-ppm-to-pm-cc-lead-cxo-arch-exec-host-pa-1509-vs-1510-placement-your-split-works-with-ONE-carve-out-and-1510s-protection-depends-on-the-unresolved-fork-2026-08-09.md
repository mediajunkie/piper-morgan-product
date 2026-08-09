---
from: ppm
to: xian (ceo)
cc: lead, cxo, arch, exec, host, pa
subject: "#1509/#1510 placement — your split works and I'd sharpen it two ways: #1510 is MORE protective than 'mechanical' suggests, but only under one of the two open readings; and there's a beta-reachable gap it gives zero protection on, already filed as #1190."
date: 2026-08-09 08:35 PT
---

**PM asked for advice on: #1510 → MVP (mechanical, some protection); #1509 → maybe Production (deeper fix), if #1510 is "safety enough for most cases."**

## ✅ Agree on #1510 → MVP — and it's stronger than "mechanical" implies

**Not because it's cheap. Because it's a BLANKET DEFAULT, not an ambiguity detector.** It doesn't have to *recognise* that Jake's *"file a ticket"* was ambiguous — **it drafts regardless.** That covers the misread-intent class broadly rather than case-by-case, which is why it's worth more than its build cost.

## 🔴 But its protection is conditional on the fork you haven't answered — and that's the real unblock

- **Under (b) DECLARED** — the user says *"just do it."* Protection holds until they revoke it. **Stable.**
- **Under (a) INFERRED** — the system graduates people on its own counter. ⚠️ **The protection decays silently, precisely as the system grows confident** — and per Arch, *"the user cannot revoke a counter they can't see."*

> **So "is #1510 safety enough" is not answerable independently of the fork.** Under (a), the safety story you're buying erodes on its own schedule.

⭐ **Which argues FOR your split rather than against it**: **ship #1510 in MVP as (b).** Arch established (b) is *"an afternoon that is never wasted"* and a prerequisite for validating (a) later. **That makes your plan cheaper, not more expensive.**

## 🔴 The gap #1510 gives ZERO protection on — and it's the worse incident

- **#1510** protects against **misread intent** — *"I meant draft, you executed."*
- **#1509** protects against **correctly-read intent with unanticipated blast radius** — *"I did say close it. I didn't know you'd close twelve."*

**Different failures.** And **once a user establishes execute-mode — under either reading — #1510 steps aside by design.** That is exactly when blast-radius surprises happen.

**This is not hypothetical, and it is already filed**: **#1190** *(Multi-turn confirmation gate for destructive issue mutations — close/reopen)*, **OPEN, milestone Production**:

> *"`close_issue` / `reopen_issue` are dispatch-migrated onto the action rail and work today… they perform a destructive state change and **currently execute on first classification — there is no 'are you sure?' confirmation turn**."*

**GitHub writes are real and dispatch-reachable today** (decisions.log v18.5, PM-verified). **So a beta user can have issues closed on first classification with no confirmation, and #1510 will not stop it once they're in execute-mode.**

## ⭐ My recommendation — your split, plus one narrow carve-out

| | |
|---|---|
| **#1510** — drafts by default *(misread intent)*, shipped as **(b) declared** | **MVP** |
| **#1190** — confirm before destructive writes *(blast radius, narrow, already scoped)* | **MVP** ← the carve-out |
| **#1509** — general consent gate + capability legibility *(the deep fix)* | **Production** |

**That buys a coherent safety floor for beta without the month-long build**, and it's closer to your instinct than either extreme. **#1190 was moved to Production as "narrow UX-polish"** — which was right when #1509 looked imminent, and reads differently now that the general gate is deferring.

## ⚠️ One complication against my own recommendation, which you should have

**#1509 bundles the gate WITH capability legibility as one feature** — CXO's ruling, all four lenses: *"legibility without the gate is dangerous; the gate without legibility is merely safe. Ship together."*

**So deferring #1509 wholesale also defers legibility — and legibility is half of Jake's headline complaint** (he couldn't tell what Piper could do). **That's a discovery cost, not a safety cost, and it doesn't show up in a safety-framed decision.**

⛔ **I'm not proposing to split #1509 to rescue that** — CXO's reason for bundling is that making capabilities discoverable *without* a gate means users find more things Piper will do unasked. **Splitting has a real risk they named.** Flagging it so the trade is visible: **the Production deferral costs discovery as well as depth.** **That's yours and CXO's call.**

## What Lead needs from you, in one line

**"#1510 → MVP as (b) declared; #1190 → MVP; #1509 → Production"** — or your variant. **I'll set the fields the moment you say it**; board writes are yours to authorise and I won't presume them.

— PPM, 2026-08-09
