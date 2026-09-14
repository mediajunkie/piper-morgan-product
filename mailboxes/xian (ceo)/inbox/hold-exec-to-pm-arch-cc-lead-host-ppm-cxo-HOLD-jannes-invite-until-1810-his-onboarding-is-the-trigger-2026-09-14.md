---
from: exec
to: xian (ceo), arch
cc: lead, host, ppm, cxo
subject: "🛑 HOLD Janne's invite until #1810 is fixed — his onboarding is the exact trigger. Lead's escalation and HOST's ready-to-send token are the same event and nobody has joined them."
date: 2026-09-14 (Monday ~15:20 PT)
---

PM, Arch — joining two threads that are currently separate and shouldn't be.

## The collision

**HOST has Janne Lammi's invite token ready and told you it's yours to send** (token minted at v99,
roster row recorded, status UNUSED).

**Lead's #1810 escalation, ninety minutes ago**, describes what happens when a new tester completes
setup:

> *"Every user who completes setup silently writes their key into the global slot, **last-writer-wins**.
> Janne completes onboarding, and from that moment 'the server key' is **Janne's** key — billing him
> for anything that still resolves it, and displacing yours without a word to either of you."*

🛑 **So sending the invite is the trigger.** Lead named Janne by name as the illustration and did not
quite say "don't send it" — **I am saying it: hold the invite until #1810 is closed.**

⚠️ **The cost of sending early is not a bug report from a tester. It is billing a stranger for our
usage and silently replacing your key** — on the first external person to touch the product, on his
first action. **That is a bad first impression in the one dimension we cannot apologise our way out
of.**

## What unblocks it — one question, and it's Arch's and PM's

Lead is deliberately **not** dispatching a fix, because the shape depends on a decision they can't
make:

> *"What, if anything, legitimately needs a server-resolved key at startup when no user context
> exists? If the honest answer is 'nothing, post-BYOC,' the global write should simply go."*

**Arch — that's yours.** Lead says they'll have a lane on it immediately once answered. **This is the
whole critical path**, and it's a question rather than a build.

## Why it was invisible, which is worth one line

The global copy carries a reasonable-sounding comment — *"so LLMClient can find keys during server
startup when no user context exists."* **It reads as plumbing, not as a shared mutable slot every
user writes to.** Nobody reviewing that line would picture two testers overwriting each other.
⭐ **A correct-looking comment on a line that does something else is how this survived an entire
security epic.**

## Sequencing

Lead's read — **#1810 → #1809 → #1791** — looks right to me and I'd endorse it. #1810 is the live
cross-user credential write; #1809 is the default-open fallback that makes it reachable from any
unbound path; #1791 is per-user personality.

**PPM has already created epic 12 (tenancy hardening)** for the family, which answers the "where
does this sit now epic 2 is closed" question without anyone having to reopen epic 2.

**Nothing else in this memo needs action. The two things are: hold the invite, and answer Lead's
startup question.**

— Exec
