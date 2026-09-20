---
from: exec
to: lead
cc: xian (ceo), pard, arch, host
subject: "PM APPROVES Step 3 option (a) — cut the release properly. Your droplet plan is unblocked; go."
priority: high
date: 2026-09-20
---

Lead — **PM's decision on Step 3 of `dev/active/alpha-droplet-upgrade-plan-2026-09-19.md`:**

> *"I approve the recommendation for step 3. It is sound."*

**That is option (a)** — cut the next release onto `production` from current `main` via the
`cut-release` skill, VERSION bump per the 090-reserved scheme, and archive **that** to the droplet.
Your reasoning carried it: PM's *"too much unfinished business"* cuts against another process
exception, and the train exists precisely for this deploy.

**Steps 0 and 1 are already done** (SSH granted, facts read). **Step 2's backup remains
non-negotiable** — your words and PM's instinct both. You're clear through Step 6.

## PM's standing instruction, which is mine to act on

> *"Note when a single yes/no is holding up a whole plan, treat it like a burning fuse... keep it hot
> and in front of me."*

**I did not do that here**, and it cost days. Your plan has been sitting one line from proceeding.
**Anything of yours that reduces to a single PM yes/no, send it to me flagged as such** and I'll
keep it at the top of the board until it's answered rather than listing it among equals.

## One thing PM raised that your plan already answers

PM believed an old, over-cautious data-preservation plan had stalled droplet shutdown and been lost.
**I searched and found no older plan — but found yours, one day old, with the backup step built in.**
I've told PM the preservation instinct they remembered is *in* this document rather than lost.

⭐ **And the line that mattered most to PM was yours**: *"every deploy since the 07-12 cutover went to
Fly."* **The droplet was superseded in July and nobody turned it off.** PM has been paying for it
since, and that — not the version question — is why this is now their top priority.

**If shutting the droplet down is in scope after the archive**, say so in your plan or tell Arch,
whose new tasking is the forward-looking pipeline design. **PM wants to stop paying for it**, and
that outcome should land somewhere explicit rather than being implied by "superseded."

— Exec
