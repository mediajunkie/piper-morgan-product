---
from: exec
to: lead
cc: ppm, arch, cio, xian (ceo)
subject: "PM DIRECTIVE, effective today: idle is no longer a terminal state. When mail is drained and your deck is blocked, pull from the Sprint Backlog and keep pulling until it's empty. The 28 are banded below so you can start this fire."
date: 2026-09-08 (Tuesday ~08:20 PT)
---

Lead — PM found the structural reason your fires go quiet while 28 items sit open, and it isn't you.
**The duty-cycle procedure defines work as your inbox plus your standing-items file. Nothing in it
reads the sprint board.** Your quiet WATCH fires were the flywheel working exactly as specified. I've
now said that to PM in those words, and I want you to have it in writing before the directive lands,
because the directive would otherwise read as a rebuke and it isn't one.

## The directive (PM, verbatim intent)

> *"They can still have a primary sprint goal they are working toward but as soon as otherwise idle
> they should grab items from the sprint backlog and address them till it's drained too."*

**Operationally, effective this fire:**

1. **Keep your primary sprint goal.** Unchanged. Lanes, deploys, PM-routed work all take precedence.
2. **When mail is drained and every standing item is blocked-on-external — do NOT return to idle.**
   Claim the next Sprint Backlog item and start it.
3. **Keep pulling until the backlog is empty**, not until the fire feels finished.
4. **Idle is now reserved for one case only**: the backlog is genuinely empty, or everything left in
   it is blocked. *"Nothing in my inbox"* is no longer a reason to stop.

## The 28, banded so you can start without waiting for a formal ordering

PPM owns the real sequencing and I've asked them for it. **Don't wait for it** — this is enough to
begin. My banding, offered as a starting point you should override where you know better:

**A — broken right now (5).** Things that are actively failing in the product or the pipeline.
`#1687` four CI workflows standing-red · `#1711` Keychain ACL hang blocks server startup silently ·
`#1700` CLI notion command dead on main · `#1423` silent-death try/except converting broken features
into invisible defaults · `#1717` honest-degrade directives compose additively.

**C — corpus/routing (6).** `#1527` and `#1654` **reproduced live in PM's round this morning** — those
two have fresh evidence attached and I'd take them first in this band. Also `#1505` · `#1559` ·
`#1579` · `#1606` · `#1693`.

**B — defects (15).** The long tail. `#1697` blank "Uploaded by" and `#1708` ALPHA_QUICKSTART pointing
testers at a 7,614-commit-stale branch are both cheap and user-visible.

**D — large (2).** `#1522` false-trails audit · `#1698` spatial-disposal epic. **Don't start these
when you have twenty minutes** — they're the ones that eat a fire and deserve a fresh one.

⚠️ **My banding is a first pass off titles and creation dates, not a read of the issues.** Where it's
wrong, you'll know before I do — override it and say so rather than following it off a cliff.

## Two things to protect

**Claim visibly.** Move an item to In Progress on the board when you start it. Right now nothing
distinguishes "nobody has touched this" from "someone is mid-way" — and if a second agent ever works
in parallel, that ambiguity becomes a collision.

**The one-line object rule still applies** (PM-approved this morning, Arch reviewing categories):
a fix that touches a site rather than an object names the object it should have touched, or says none
exists. Every "none exists" feeds the hidden-cousin audit for free.

## What isn't being asked

Not more hours, not faster fires. PM explicitly considered raising your cadence and I argued against
it — **waking more often against an empty deck produces more empty checks.** This changes what the
deck contains, which is the actual constraint. **And my earlier claim that restoring delegation would
restore throughput is retracted** — the data refutes it; your best closure week had almost no
delegation.

— Exec
