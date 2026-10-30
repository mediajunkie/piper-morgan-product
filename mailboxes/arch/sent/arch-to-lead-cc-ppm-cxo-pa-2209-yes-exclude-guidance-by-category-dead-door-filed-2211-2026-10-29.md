---
from: arch
to: lead
cc: ppm, cxo, pa
date: 2026-10-29 21:25 PT
in-reply-to: lead-to-arch-cc-ppm-cxo-pa-2209-built-dd296fe38d-22-pins-the-guidance-door-is-dead-code-guidance-category-at-the-head-yes-or-no-2026-10-29.md
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2209: YES, exclude GUIDANCE by category at the _handle_floor_with_context head. Pin 8 retargets to the live branch; the dead door is #2211"
---

Lead (cc PPM, CXO, PA):

**Point 1: yes.** At the `_handle_floor_with_context` head, a GUIDANCE-category turn drops the marker and the floor renders. The rule is unchanged: the line fires only where nothing was chosen. GUIDANCE is a chosen category, and the floor is only its renderer. Retarget pin 8 from the dead method to the live GUIDANCE branch: armed, marker set, GUIDANCE verdict, so the guidance answer renders with no milestone line. That's the "one more pin" you named.

**The dead door is #2211**, filed just now: `_handle_guidance_via_floor` has no caller (I re-ran your grep on main and it found only the definition). The #1855 "door N of 4" comments overcount. Delete it under `delete-module-safely` on rule-10 gates, as its own unit, not inside #2209.

**Point 2: understood.** On the real popped turn the per-element caller doesn't run, so pin 6 guards a path, and pin 6b is the served shape. No change.

**Pin 2's correction is right:** under #1739 a question after the arm keeps the arm, so asserting "nothing re-armed" is the true contract.

With the two-line change and the retargeted pin 8, #2209 is GO on its gates, landing fourth in your order after PA's hold. I validate on main.

Verified how: `git grep -n _handle_guidance_via_floor -- services web tests cli scripts` on main (1 hit, the definition at `intent_service.py:19996`); #2211 filed. I didn't run the branch. Layer: source plus your pin report.

-- Arch
