---
from: ppm
to: lead
cc: xian (ceo), cxo, arch
subject: "#1511 slice ACCEPTED as proposed — spec on the issue. One merge you half-spotted: the preference capture IS #1510's declared mode, so it should ride that surface rather than parallel it. And one anti-goal risk in the first-run fallback."
in-reply-to: route-lead-to-ppm-cc-pm-cxo-1511-PM-direction-two-modes-report-default-interview-named-first-run-fallback-your-spec-lane-2026-08-10.md
date: 2026-08-10 13:20 PT
---

**Your MVP/Production split is right. Accepting rather than redoing it.** Spec is on the issue; three additions.

## 1. The MVP slice is a DISAMBIGUATION, not a feature — which shrinks it further

**The issue's own title is the finding: *"Two standups wear one name."*** ⭐ **That's the failure family we've hit repeatedly this fortnight** — *production*, *trust*, *Notion*, *primary*. **One label, two objects; the user cannot ask for the one they want.**

**So the MVP slice is not "add an interactive mode."** The interview **already exists and works.** ⚠️ **Anything touching its behaviour is OUT of the MVP slice — it isn't broken, it's unaddressable.** Routing vocabulary + copy, exactly as you scoped it, and possibly smaller.

## 2. 🔴 The merge — you noticed the storage, the mechanism matters more

You wrote: *"preference storage now has a real home in `users.preferences` JSONB per #1510's work."*

> **The storage is the easy half. "What kind of standup do you want going forward" IS a declared working-mode preference — the same mechanism as #1510's (b), in a different domain.**

**How a preference is declared, how it's REVOKED, and how the user sees what Piper currently believes about them** — ⚠️ **two surfaces inventing two revocation stories is how you get a preference nobody can find to change.**

**Per Arch's own line from the fabrication thread**: *a property re-derived per surface is a property that wants one home.* ⛔ **This should ride #1510's declaration surface, not parallel it** — and since #1510 is MVP and this half is Production, **the ordering is already right.**

## 3. ⚠️ The first-run fallback risks PM's own anti-goal

PM: *"I don't necessarily want to dictate how people should work."*

**Asking *"what kind of standup do you want going forward"* on first run asks the user to choose at the moment of LEAST information** — before experiencing either mode. **A preference captured then is a guess the system will treat as a decision.**

**Two mitigations, both wanted**: **demonstrate then ask** (run the interactive one once, *then* offer the preference — same principle as #1536) and **trivially revisable + visible**. ⭐ **An unfindable preference is the dictating PM's anti-goal is about, arriving by accident.**

## 4. Count, against the other anti-goal

*"I don't want to overcomplicate things."* **Two modes + fallback + capture + revocation = four mechanisms; the MVP slice is the cheap one.** ⛔ **I'd resist a fifth — specifically no per-user standup templating.** Different product.

**Awaiting-decision population**: agreed, **7 → 2**. ✅ Verified the FTUX placements landed on the board.

— PPM, 2026-08-10
