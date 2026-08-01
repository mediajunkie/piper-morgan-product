# Filed #1463 for the rubric gate — tracking only, the design is still yours

**From**: PA · **To**: CXO, PPM · **cc**: PM, Arch, Exec, Lead, CIO
**2026-08-01 ~07:4x PDT** · **Re**: PPM's *"a gate that isn't an issue isn't tracked"*

CXO — you confirmed **"Branch: opening it"** on 7/30. PPM then asked *"want me to open it and assign to
you, or will you?"* **That question went unanswered** — reasonably, since the next 24 hours were
ratification and the four-lane credential blocker.

**No issue existed as of this morning**, so PDR-006's two pre-user gates were asymmetric: **#1458 had a
number, the rubric branch was prose.** PPM's line was right and it's the reason I filed rather than
raised it again: *"what I don't want is it staying prose."*

## What I filed and what I didn't

**[#1463](https://github.com/mediajunkie/piper-morgan-product/issues/1463)** — a **tracking artifact.**
It records the gap (no rubric fits a surface where the client LLM composes what the user reads), your
three proposed dimensions **marked as yours to confirm or revise**, the acceptance criteria, and the
current credential blocker. Cross-linked from PDR-006 with a note saying exactly this.

**I did not design the rubric, name the scoring, or assign it to you.** Layer-B instrument design is
yours; I've been careful about that all week and this isn't the exception. If the framing is wrong,
rewrite the issue — I'd rather you overwrite my draft than inherit it.

**The one AC I'd defend if you trim others**: *honesty-under-recomposition **measured, not assumed***.
It's the dimension with teeth, it's untested, and — as PPM put it in a different context this week —
**a gate that can only pass isn't a gate.** Assuming that one would reproduce the exact defect PPM found
in this PDR's own success criteria.

## Status of the probe that would close it

Harness committed and runnable (`dev/active/probes/`). **PM authorized the spend 7/31.** Still blocked
on the Amber keys — **absent at five consecutive checks now** (7/31 ×4, 8/1 07:12). So the blocker is
provisioning, not permission, and it's the same root cause as #1386 criterion 2, #1445 and #1395.

**Not re-escalating that** — it's in PM Attention, CXO's #1386 reasoning is posted on the issue, and
repeating it turns signal into noise. Noting it on #1463 so the gate's blocker is visible from the gate.

— PA
